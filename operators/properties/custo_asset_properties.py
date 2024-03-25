import bpy
import random
from .custo_label_properties import CustoLabelPropertiesPointer, CustoLabelEnumProperties, CustoLabelCategoryDefinitionProperties
from .custo_slot_properties import CustoPartSlotsProperties

class CustoAssetTypePointer(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type', default='')
	
	@property
	def asset_type(self):
		return bpy.context.scene.custo_handler_settings.custo_asset_types[self.name]

def asset_type_enum(self, context):
	items = [(l.name, l.name, '') for l in context.scene.custo_handler_settings.custo_asset_types]
	return items

def get_asset_name(asset_ids):
	def joined(strings):
		result = ''
		i = 0
		for s in strings:
			if i < len(strings)-1:
				s += '_'
			result += s
			i += 1
		return result
	labels = [getattr(getattr(l, "label", "NULL"), "name", "NULL") for l in asset_ids]
	return joined(labels)

def update_current_asset_properties(self, context):
	asset_names = [a.asset_name for a in context.scene.custo_handler_settings.custo_assets]
	# update Asset ID
	context.scene.custo_handler_settings.current_asset_id.clear()
	for i, lc in enumerate(context.scene.custo_handler_settings.custo_asset_types[self.name].asset_label_categories):
		id_enum = context.scene.custo_handler_settings.current_asset_id.add()
		id_enum.label_category_name = lc.name
		
		if context.scene.custo_handler_settings.current_asset_name in asset_names:
			asseet_id = context.scene.custo_handler_settings.custo_assets[context.scene.custo_handler_settings.current_asset_name].asset_id[i]
			if asseet_id.label_category_name == id_enum.label_category_name:
				id_enum.name = asseet_id.name

	# Update Slots
	context.scene.custo_handler_settings.current_edited_asset_slots.clear()
	for s in context.scene.custo_handler_settings.current_label_category[context.scene.custo_handler_settings.custo_asset_types[self.name].slot_label_category.name].labels:
		slot = context.scene.custo_handler_settings.current_edited_asset_slots.add()
		slot.name = s.name
		slot.checked = s.checked
		slot.keep_lower_layer_slot = s.keep_lower_layer_slot

class CustoAssetTypeEnumProperties(bpy.types.PropertyGroup):
	name : bpy.props.EnumProperty(name="Asset Type", items=asset_type_enum, update=update_current_asset_properties)

class CustoAssetLabelCategoryPointer(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Category Name', default='')
	
	@property
	def label_category(self):
		return bpy.context.scene.custo_handler_settings.custo_label_categories[self.name]

class CustoAssetTypeProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type', default='')
	asset_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	slot_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	mesh_variation_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	material_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	material_variation_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	
	@property
	def slots(self) -> list:
		"""return the list of slots of the current asset type

		Returns:
			list: ["slot1", "slot2", "slot3"]
		"""
		ch_settings = bpy.context.scene.custo_handler_settings
		return [s.name for s in ch_settings.custo_label_categories[self.slot_label_category.label_category.name].labels]
	
	def get_assets_per_slot(self, slot:str)->list:
		"""Returns a list of asset that covers the slot inputed given

		Args:
			slot (str): name of the slot

		Returns:
			list: [Asset1, Asset2, Asset3]
		"""
		ch_settings = bpy.context.scene.custo_handler_settings
		assets = []

		for a in ch_settings.custo_assets:
			if a.asset_type.name != self.name:
				continue

			slots = [s.name for s in a.slots if s.checked]

			if slot not in slots:
				continue

			assets.append(a)

		return assets

	def is_viable_mesh_variation(self, variation:dict)->True:
		valid = True
		for s in self.slots:
			assets = self.get_assets_per_slot(s)
			valid_slot = False
			for a in assets:
				mesh_variation = a.mesh_variation(variation)
				if mesh_variation is not None:
					valid_slot = True
					break
			
			if not valid_slot:
				valid = False
				break

		return valid
	
	
class CustoAssetProperties(bpy.types.PropertyGroup):
	asset_type : bpy.props.PointerProperty(type=CustoAssetTypePointer)
	asset_id : bpy.props.CollectionProperty(type=CustoLabelPropertiesPointer)
	layer : bpy.props.IntProperty(name='Layer', default=0)
	slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
	
	@property
	def asset_name(self):
		return get_asset_name(self.asset_id)
	
	@property
	def all_mesh_variations(self):
		'''
		Returns the list of all mesh variations in the current asset
		'''
		meshes = [o for o in bpy.data.objects]
		for id_label in self.asset_id:
			for o in bpy.data.objects:
				if id_label.label_category_name not in o.custo_label_category_definition:
					if o in meshes:
						meshes.remove(o)
					continue

				if id_label.name not in o.custo_label_category_definition[id_label.label_category_name].labels:
					if o in meshes:
						meshes.remove(o)
					continue

				if not o.custo_label_category_definition[id_label.label_category_name].labels[id_label.name].checked:
					if o in meshes:
						meshes.remove(o)
					continue

		return meshes
	
	@property
	def valid_labels(self, exclude:dict={}):
		'''
		Returns a list of labels enabled in all mesh variations contains in this asset.
		In other terms picking one of this label will give you at least one valid mesh to spawn.
		'''
		def add_valid_mesh_label(label_set, mesh, label_category, exclude:dict={}):
			labels = []
			for l in mesh.custo_label_category_definition[label_category].labels:
				if not l.checked:
					continue
				
				if label_category in exclude.keys():
					if l.name in exclude[label_category]:
						continue
				
				labels.append(l.name)

			if label_category not in label_set.keys():
				label_set[label_category] = set(labels)
			else:
				for l in labels:
					label_set[label_category].add(l)

		valid_labels = {}
		ch_settings = bpy.context.scene.custo_handler_settings

		# Adding Slot
		slot_category = self.asset_type.asset_type.slot_label_category.label_category.name
		for slot in self.slots:
			if not slot.checked:
				continue
			
			if slot_category in exclude.keys():
				if slot.name in exclude[slot_category]:
					continue

			if slot_category not in valid_labels.keys():
				valid_labels[slot_category] = set([slot.name])
			else:
				valid_labels[slot_category].add(slot.name)

		all_meshes_variations = self.all_mesh_variations
		asset_label_categories = [lc.name for lc in self.asset_type.asset_type.mesh_variation_label_categories] + [slot_category]

		other_label_category = [lc.name for lc in ch_settings.custo_label_categories if lc not in asset_label_categories]

		for m in all_meshes_variations:
			# Adding Mesh variation Label Categories
			for mesh_category in self.asset_type.asset_type.mesh_variation_label_categories:
				add_valid_mesh_label(valid_labels, m, mesh_category.name, exclude = exclude)

			# Add all other labels
			for lc in other_label_category:
				add_valid_mesh_label(valid_labels, m, lc, exclude = exclude)

		return valid_labels

	def valid_labels_from_mesh(self, mesh):
		valid_labels = {}

		for lc in mesh.custo_label_category_definition:
			valid_labels[lc.name] = self.valid_label_catgory_labels_from_mesh(mesh, lc)

		return valid_labels
	
	def valid_label_catgory_labels_from_mesh(self, mesh, category):
		return [l for l in mesh.custo_label_category_definition[category.name].labels if l.checked]


	def mesh_variations(self, variations:dict, exclude=[]):
		'''
		Returns all valid meshs matching the inputed label combinaison
		'''
		all_variations = self.all_mesh_variations

		valid_meshes = [m for m in all_variations if m not in exclude and self.is_valid_mesh(m, variations)]

		if not len(valid_meshes):
			return None
		else:
			return valid_meshes
	
	def mesh_variation(self, variations:dict, exclude=[]):
		'''
		Returns one valid mesh matching the inputed label combinaison
		'''
		valid_variations = self.mesh_variations(variations, exclude=exclude)
		if valid_variations is None:
			return None
		elif not len(valid_variations):
			return None
		else:
			return random.choice(valid_variations)
	
	def is_valid_mesh(self, ob, variations:dict):
		'''
		Check that the mesh matches the inputed label combinaison.
		'''
		valid = True
		ch_settings = bpy.context.scene.custo_handler_settings
		for c,l in variations.items():
			if c not in ob.custo_label_category_definition.keys() or c not in ch_settings.custo_label_categories.keys():
				valid = False
				break

			ob_category = ob.custo_label_category_definition[c]
			ch_category = ch_settings.custo_label_categories[c]

			if l.label not in ob_category.labels.keys() or l.label not in ch_category.labels.keys():
				valid = False
				break
			
			if ch_category.labels[l.label].valid_any:
				continue

			if ob_category.labels[l.label].checked != l.value:
				valid_any_label = ch_category.valid_any
				if valid_any_label is not None:
					if ob_category.labels[valid_any_label.name].checked:
						continue
				valid = False
				break

		return valid

	def has_mesh_with_labels(self, variations:dict):
		'''
		Returns True if the asset contains at least one mesh with given variation combinaison
		'''
		all_variations = self.all_mesh_variations

		valid_meshes = [m for m in all_variations if self.is_valid_mesh(m, variations)]
		
		return True if len(valid_meshes) else False
	

class UL_CustoAssetType(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssetTypes"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_asset_type', text='', icon='GREASEPENCIL').index = index
		# row.operator('scene.duplicate_customization_asset_type', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_asset_type', text='', icon='X').index = index

class UL_CustoAsset(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssets"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.asset_name}')
		row.separator()
		row.label(text=f'|  layer={item.layer}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_asset', text='', icon='GREASEPENCIL').index = index
		# row.operator('scene.duplicate_customization_asset', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_asset', text='', icon='X').index = index

classes = ( CustoAssetLabelCategoryPointer,
			CustoAssetTypeProperties,
			CustoAssetTypeEnumProperties,
			CustoAssetTypePointer,
			CustoAssetProperties,
			UL_CustoAssetType,
			UL_CustoAsset)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()