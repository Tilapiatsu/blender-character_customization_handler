import bpy

def get_label_category_labels(asset_type, prop_name):
	ch_settings = bpy.context.scene.custo_handler_settings
	category_name = getattr(ch_settings.custo_asset_types[asset_type], prop_name , None)
	if category_name is None:
		return None
	category_name = category_name.name
	return ch_settings.custo_label_categories[category_name]

def in_range(ui_list, index):
	return index > -1 and len(ui_list) and len(ui_list) < index

def update_label_definition_object(self, context):
	ch_settings = context.scene.custo_handler_settings
	if not ch_settings.custo_label_definition_object_updated: return
	
	ch_settings.custo_label_definition_object_updated = False

	for o in context.selected_objects:
		if o.name == context.object.name:
			continue

		for i, l in enumerate(o.custo_label_category_definition[ch_settings.custo_label_category_definition_idx].labels):
			if i > len(context.object.custo_label_category_definition) - 1:
				return
			l.value = context.object.custo_label_category_definition[ch_settings.custo_label_category_definition_idx].labels[i].value
			
	ch_settings.custo_label_definition_object_updated = True

def update_label_definition_material(self, context):
	return
	ch_settings = context.scene.custo_handler_settings
	for i, l in enumerate(context.object.material_slots[context.object.active_material_index].material.custo_label_category_definition[ch_settings.custo_label_category_definition_idx].labels):
		if i > len(context.object.material_slots[context.object.active_material_index].material.custo_label_definition) - 1:
			return
		l.value = context.object.material_slots[context.object.active_material_index].material.custo_label_definition[i].value

def label_categories_enum(self, context):
	ch_settings = context.scene.custo_handler_settings
	items = [(l.name, l.name, '') for l in ch_settings.custo_label_categories]
	return items

def label_enum(self, context):
	ch_settings = context.scene.custo_handler_settings
	items = [(l.name, l.name, '') for l in ch_settings.custo_label_categories[self.label_category_name].labels]
	return items

def update_label_category(self, context):
	ch_settings = context.scene.custo_handler_settings
	current_name = self.name

	ch_settings.custo_label_categories[ch_settings.custo_label_categories_idx].labels[current_name].valid_any = ch_settings.custo_labels[current_name].valid_any

	if ch_settings.custo_labels[current_name].valid_any:
		for l in ch_settings.custo_labels:
			if l.name == current_name:
				continue
			l.valid_any = False
			ch_settings.custo_label_categories[ch_settings.custo_label_categories_idx].labels[l.name].valid_any = False

def update_node_label_categories(asset_type):
	update_mesh_slot_label_categories(asset_type)
	update_materials_label_categories(asset_type)
	update_asset_name_label_categories(asset_type)
	update_other_label_categories(asset_type)
	update_override_label_category(asset_type)

def init_asset_type_label_category(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	if asset_type not in ch_settings.custo_asset_types_label_categories.keys():
		lc = ch_settings.custo_asset_types_label_categories.add()
		lc.name = asset_type
		return lc
	else:
		return ch_settings.custo_asset_types_label_categories[asset_type]

def update_mesh_slot_label_categories(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	lc = init_asset_type_label_category(asset_type)
	lc.mesh_slot_label_category.clear()
	asset_type = ch_settings.custo_asset_types[asset_type]
	category_names = [asset_type.mesh_slot_label_category.name]

	for c in category_names:
		cat = lc.mesh_slot_label_category.add()
		cat.name = c

def update_materials_label_categories(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	lc = init_asset_type_label_category(asset_type)
	lc.materials_label_category.clear()

	asset_type = ch_settings.custo_asset_types[asset_type]
	category_names = [asset_type.material_label_category.name] + [lc for lc in asset_type.material_variation_label_categories.keys()]

	for c in category_names:
		cat = lc.materials_label_category.add()
		cat.name = c

def update_asset_name_label_categories(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	lc = init_asset_type_label_category(asset_type)
	lc.asset_label_category.clear()

	asset_type = ch_settings.custo_asset_types[asset_type]
	category_names = [asset_type.asset_label_category.name]

	for c in category_names:
		cat = lc.asset_label_category.add()
		cat.name = c
		
def update_other_label_categories(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	lc = init_asset_type_label_category(asset_type)
	lc.other_label_category.clear()

	names = ch_settings.custo_label_categories.keys()
	asset_type = ch_settings.custo_asset_types[asset_type]
	exclude_label_category_name = [	asset_type.asset_label_category.name, 
							asset_type.mesh_slot_label_category.name, 
							asset_type.material_slot_label_category.name, 
							asset_type.material_label_category.name] + [lc for lc in asset_type.material_variation_label_categories.keys()]
	
	filtered = filter(lambda lc:lc not in exclude_label_category_name, names)

	for c in filtered:
		cat = lc.other_label_category.add()
		cat.name = c
		
def update_override_label_category(asset_type):
	ch_settings = bpy.context.scene.custo_handler_settings
	lc = init_asset_type_label_category(asset_type)
	lc.override_label_category.clear()
	
	category_names = [l.name for l in ch_settings.custo_asset_types_label_categories[asset_type].other_label_category.values()] + [l.name for l in ch_settings.custo_asset_types_label_categories[asset_type].materials_label_category.values()]
	
	for c in category_names:
		cat = lc.override_label_category.add()
		cat.name = c

class CustoLabelCategoryEnumProperties(bpy.types.PropertyGroup):
	name : bpy.props.EnumProperty(name="Label Category Name", items=label_categories_enum)


class CustoLabelEnumProperties(bpy.types.PropertyGroup):
	label_category_name : bpy.props.StringProperty(name='Label Category Name')
	name : bpy.props.EnumProperty(name="Label Name", items=label_enum)


class CustoLabelCategoryEnumCollectionProperties(bpy.types.PropertyGroup):
	label_category_enums : bpy.props.CollectionProperty(name="Label Category Enums", type=CustoLabelCategoryEnumProperties)

class CustoLabelProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	value : bpy.props.BoolProperty(default=False)
	keep_lower_layer_slot : bpy.props.BoolProperty(default=False)
	valid_any : bpy.props.BoolProperty(name='Valid Any', default=False)
	weight : bpy.props.FloatProperty(default=1.0, min=0)

class CustoLabelPropertiesDisplay(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	value : bpy.props.BoolProperty(default=False)
	keep_lower_layer_slot : bpy.props.BoolProperty(default=False)
	valid_any : bpy.props.BoolProperty(name='Valid Any', default=False, update=update_label_category)
	weight : bpy.props.FloatProperty(default=1.0, min=0)

class CustoLabelPropertiesPointer(bpy.types.PropertyGroup):
	label_category_name : bpy.props.StringProperty(name='Label Category Name', default='')
	name : bpy.props.StringProperty(name='Label Name', default='')
	
	@property
	def label(self):
		if self.label_category_name not in bpy.context.scene.custo_handler_settings.custo_label_categories:
			return None
		if self.name not in bpy.context.scene.custo_handler_settings.custo_label_categories[self.label_category_name].labels:
			return None
		return bpy.context.scene.custo_handler_settings.custo_label_categories[self.label_category_name].labels[self.name]
	

class CustoLabelCategoryProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelProperties)
	
	@property
	def valid_any(self):
		valid = None
		for l in self.labels:
			if l.valid_any:
				return l

		return valid

	@property
	def not_valid_any(self):
		valid_any = self.valid_any
		if valid_any is None:
			return self.labels
		else:
			return [l for l in self.labels if l != valid_any]

class CustoLabelDefinitionObjectProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	value : bpy.props.BoolProperty(default=False, update=update_label_definition_object)
	keep_lower_layer_slot : bpy.props.BoolProperty(default=False)
	valid_any : bpy.props.BoolProperty(name='Valid Any', default=False)
	weight : bpy.props.FloatProperty(default=1.0, min=0)

class CustoLabelDefinitionMaterialProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	value : bpy.props.BoolProperty(default=False, update=update_label_definition_material)
	keep_lower_layer_slot : bpy.props.BoolProperty(default=False)
	valid_any : bpy.props.BoolProperty(name='Valid Any', default=False)
	weight : bpy.props.FloatProperty(default=1.0, min=0)

class CustoLabelCategoryDefinitionObjectProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelDefinitionObjectProperties)

class CustoLabelCategoryDefinitionMaterialProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelDefinitionMaterialProperties)

class CustoLabelCategoryDefinitionProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelProperties)

class NodeAssetTypeLabelCategories(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type')
	asset_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)
	mesh_slot_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)
	materials_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)
	other_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)
	override_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)

class UL_CustoLabel(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoLabels"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row.separator()

		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.prop(item, 'valid_any')
		row.operator('scene.edit_customization_label', text='', icon='GREASEPENCIL').index = index
		row.operator('scene.duplicate_customization_label', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_label', text='', icon='X').index = index
		
		
class UL_CustoLabelCategory(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoLabelCategories"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_label_category', text='', icon='GREASEPENCIL').index = index
		row.operator('scene.duplicate_customization_label_category', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_label_category', text='', icon='X').index = index


class UL_CustoLabelDefinition(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoLabelDefinition"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(item, 'value', text='')
		row.separator()
		row.label(text=f'{item.name}')
		

class UL_CustoPartLabelCategoryDefinition(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoLabelCategorieDefinition"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')


classes = ( CustoLabelProperties, 
		   	CustoLabelPropertiesDisplay,
			CustoLabelCategoryProperties,
			CustoLabelEnumProperties,
			CustoLabelDefinitionObjectProperties,
			CustoLabelDefinitionMaterialProperties,
			CustoLabelCategoryDefinitionObjectProperties,
			CustoLabelCategoryDefinitionMaterialProperties,
			CustoLabelPropertiesPointer,
			CustoLabelCategoryDefinitionProperties,
			CustoLabelCategoryEnumProperties,
			CustoLabelCategoryEnumCollectionProperties,
			NodeAssetTypeLabelCategories,
			UL_CustoLabel, 
			UL_CustoLabelCategory,
			UL_CustoLabelDefinition,
			UL_CustoPartLabelCategoryDefinition)


def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Object.custo_label_definition_idx = bpy.props.IntProperty(default=0)
	bpy.types.Object.custo_label_category_definition = bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionObjectProperties)

	bpy.types.Material.custo_label_definition_idx = bpy.props.IntProperty(default=0)
	bpy.types.Material.custo_label_category_definition = bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionMaterialProperties)
	

def unregister():
	del bpy.types.Material.custo_label_definition_idx
	del bpy.types.Material.custo_label_definition_updated
	del bpy.types.Material.custo_label_category_definition

	del bpy.types.Object.custo_label_definition_idx
	del bpy.types.Object.custo_label_definition_updated
	del bpy.types.Object.custo_label_category_definition
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()