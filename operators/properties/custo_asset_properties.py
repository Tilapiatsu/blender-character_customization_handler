import bpy
import random
from itertools import product as iter_product
from .custo_label_properties import CustoLabelPropertiesPointer, CustoLabelEnumProperties, CustoLabelCategoryDefinitionProperties
from .custo_slot_properties import CustoPartSlotsProperties
from ...attributes.binary_labels.binary_labels import LabelVariationCombinaison, LabelVariation, LabelCombinaison, BinaryLabel

def draw_asset_type_search(layout, property_name, text='', label=''):
	row = layout.split(align=True, factor=0.2)

	row.label(text=label)
	op = row.operator('scene.search_asset_type', text=text)
	op.property_name = property_name

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
	ch_settings = context.scene.custo_handler_settings
	asset_names = [a.asset_name for a in ch_settings.custo_assets]
	# update Asset ID
	lc = ch_settings.custo_asset_types[self.asset_type].asset_label_category
	ch_settings.current_asset_id.label_category_name = lc.name
	if ch_settings.current_asset_name in asset_names:
		asset_id = ch_settings.custo_assets[ch_settings.current_asset_name].asset_id
		if asset_id.label_category_name == lc.name:
			ch_settings.current_asset_id.name = asset_id.name
		
	# Update Slots
	ch_settings.current_edited_asset_slots.clear()
	for s in ch_settings.current_label_category[ch_settings.custo_asset_types[self.asset_type].mesh_slot_label_category.name].labels:
		slot = ch_settings.current_edited_asset_slots.add()
		slot.name = s.name
		slot.value = s.value
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
	asset_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	mesh_slot_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	material_slot_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	mesh_variation_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	material_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	material_variation_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	
	@property
	def slots(self) -> list:
		"""return the list of slots of the current asset type

		Returns:
			list: ["slot1", "slot2", "slot3"]
		"""
		ch_settings = bpy.context.scene.custo_handler_settings
		return [s.name for s in ch_settings.custo_label_categories[self.mesh_slot_label_category.label_category.name].labels]
	
	@property
	def mesh_variation_categories(self):
		return [ self.mesh_slot_label_category.name ] + [ lc for lc in self.mesh_variation_label_categories.keys() ]
	
	@property
	def material_variation_categories(self):
		return [ self.material_label_category.name ] + [ lc for lc in self.material_variation_label_categories.keys() ]
	
	@property
	def key_label_categories(self):
		return [self.asset_label_category.label_category, self.mesh_slot_label_category.label_category, self.material_slot_label_category.label_category, self.material_label_category.label_category] + [lc.label_category for lc in self.mesh_variation_label_categories.label_categories] + [lc.label_category for lc in self.material_variation_label_categories.label_categories]

	@property
	def secoundary_label_categories(self):
		ch_settings = bpy.context.scene.custo_handler_settings
		key_label_categories = self.key_label_categories
		return [lc for lc in ch_settings.custo_label_categories if lc not in key_label_categories]

	@property
	def all_mesh_variations(self):
		all_mesh_variations = LabelVariationCombinaison()
		label_categories = []
		for lc in self.mesh_variation_label_categories:
			lc = lc.label_category
			label_categories.append([{'name':l.name, 'category':lc.name} for l in lc.labels if not l.valid_any])
		
		all_mesh_variations.create_variation_combinaison(label_categories)
		
		return all_mesh_variations

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
			
			if a.slots[slot].value:
				assets.append(a)

		return assets

	def is_viable_mesh_variation(self, variation:LabelVariation)->True:
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
	asset_id : bpy.props.PointerProperty(type=CustoLabelPropertiesPointer)
	layer : bpy.props.IntProperty(name='Layer', default=0)
	slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
	
	@property
	def asset_name(self):
		return self.asset_id.name
	
	@property
	def is_empty(self):
		return not len(self.all_mesh_variations)

	@property
	def all_mesh_variations(self):
		'''
		Returns the list of all mesh variations in the current asset
		'''
		meshes = [o for o in bpy.data.objects if o.type == 'MESH' and o.custo_attributes.is_asset]
		for o in bpy.data.objects:
			if self.asset_id.label_category_name not in o.custo_label_category_definition:
				if o in meshes:
					meshes.remove(o)
				continue

			if self.asset_id.name not in o.custo_label_category_definition[self.asset_id.label_category_name].labels:
				if o in meshes:
					meshes.remove(o)
				continue

			if not o.custo_label_category_definition[self.asset_id.label_category_name].labels[self.asset_id.name].value:
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
		valid_labels = LabelCombinaison()
		all_meshes_variations = self.all_mesh_variations

		for m in all_meshes_variations:
			labels = self.valid_mesh_variations_from_mesh(m, exclude)
			valid_labels.add_label_combinaison(labels)

		return valid_labels

	@property
	def valid_slots(self):
		return [s.name for s in self.slots if s.value]
		
	def valid_labels_from_mesh(self, mesh, include_label_category:list=None):
		valid_labels = LabelCombinaison()
		for lc in mesh.custo_label_category_definition:
			if include_label_category is not None:
				if lc.name in include_label_category:
					valid_labels.add_binary_labels(lc.name, self.valid_label_catgory_labels_from_mesh(mesh, lc))
			else:
				valid_labels.add_binary_labels(lc.name, self.valid_label_catgory_labels_from_mesh(mesh, lc))

		return valid_labels
	
	def valid_mesh_variations_from_mesh(self, mesh, exclude:dict={}):
		mesh_variation_label_category = [lc.name for lc in self.asset_type.asset_type.mesh_variation_label_categories if lc not in exclude.keys()]
		return self.valid_labels_from_mesh(mesh, include_label_category=mesh_variation_label_category)
	
	def valid_label_catgory_labels_from_mesh(self, mesh, category, split_any=True):
		ch_settings = bpy.context.scene.custo_handler_settings
		scene_category = ch_settings.custo_label_categories[category.name]
		valid = [l for l in mesh.custo_label_category_definition[category.name].labels if l.value]
		if split_any:
			new_valid = []
			for l in valid:
				if scene_category.valid_any is None or l.name != scene_category.valid_any.name:
					new_valid.append(BinaryLabel(l.name, l.value, l.valid_any, l.weight))
				else:
					for ll in scene_category.not_valid_any:
						new_valid.append(BinaryLabel(ll.name, True, ll.valid_any, ll.weight))
					
			valid = new_valid
		return valid

	def mesh_variations(self, variation:LabelVariation, exclude=[]):
		'''
		Returns all valid meshs matching the inputed label combinaison
		'''
		all_variations = self.all_mesh_variations

		valid_meshes = [m for m in all_variations if m not in exclude and self.is_valid_mesh(m, variation)]

		if not len(valid_meshes):
			return None
		else:
			return valid_meshes
	
	def mesh_variation(self, variation:LabelVariation, exclude=[]):
		'''
		Returns one valid mesh matching the inputed label combinaison
		'''
		valid_variations = self.mesh_variations(variation, exclude=exclude)
		if valid_variations is None:
			return None
		elif not len(valid_variations):
			return None
		else:
			return random.choice(valid_variations)
	
	def is_valid_mesh(self, ob, variation:LabelVariation):
		'''
		Check that the mesh matches the inputed label combinaison.
		'''
		valid = True
		ch_settings = bpy.context.scene.custo_handler_settings
		
		for c,l in variation.items():
			if c not in ob.custo_label_category_definition.keys() or c not in ch_settings.custo_label_categories.keys():
				valid = False
				break
			if c in self.asset_type.asset_type.material_variation_categories:
				continue

			ob_category = ob.custo_label_category_definition[c]
			ch_category = ch_settings.custo_label_categories[c]

			if l.name not in ob_category.labels.keys() or l.name not in ch_category.labels.keys():
				valid = False
				break
			
			if ch_category.labels[l.name].valid_any:
				continue
			
			# print(ob_category.labels[l.name].name, l.name)
			# print(ob_category.labels[l.name].value, l.value)

			if ob_category.labels[l.name].value != l.value:
				valid_any_label = ch_category.valid_any
				if valid_any_label is not None:
					if ob_category.labels[valid_any_label.name].value:
						continue
				valid = False
				break

		return valid

	def has_mesh_with_labels(self, variation:LabelVariation):
		'''
		Returns True if the asset contains at least one mesh with given variation combinaison
		'''
		all_variations = self.all_mesh_variations

		valid_meshes = [m for m in all_variations if self.is_valid_mesh(m, variation)]
		
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
		row.label(text=f'{item.asset_type.name} : ')
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