import bpy

def in_range(ui_list, index):
	return index > -1 and len(ui_list) and len(ui_list) < index

def update_label_definition(self, context):
	for o in context.selected_objects:
		for i, l in enumerate(o.custo_label_category_definition[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels):
			if i > len(context.object.custo_label_definition) - 1:
				return
			l.checked = context.object.custo_label_definition[i].checked

def label_categories_enum(self, context):
	items = [(l.name, l.name, '') for l in context.scene.custo_handler_settings.custo_label_categories]
	return items

def label_enum(self, context):
	items = [(l.name, l.name, '') for l in context.scene.custo_handler_settings.custo_label_categories[self.label_category_name].labels]
	return items


class CustoLabelCategoryEnumProperties(bpy.types.PropertyGroup):
	name : bpy.props.EnumProperty(name="Label Category Name", items=label_categories_enum)


class CustoLabelEnumProperties(bpy.types.PropertyGroup):
	label_category_name : bpy.props.StringProperty(name='Label Category Name')
	name : bpy.props.EnumProperty(name="Label Name", items=label_enum)


class CustoLabelCategoryEnumCollectionProperties(bpy.types.PropertyGroup):
	label_category_enums : bpy.props.CollectionProperty(name="Label Category Enums", type=CustoLabelCategoryEnumProperties)


class CustoLabelProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	checked : bpy.props.BoolProperty(default=False)
	keep_lower_layer_slot : bpy.props.BoolProperty(default=False)


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


class CustoLabelDefinitionProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	checked : bpy.props.BoolProperty(default=False, update=update_label_definition)
	

class CustoLabelCategoryDefinitionProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelProperties)


class UL_CustoLabel(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoLabels"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
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
		row.prop(item, 'checked', text='')
		row.separator()
		row.label(text=f'{item.name}')
		

class UL_CustoPartLabelCategoryDefinition(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoLabelCategorieDefinition"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')


classes = ( CustoLabelProperties, 
			CustoLabelCategoryProperties,
			CustoLabelEnumProperties,
			CustoLabelDefinitionProperties,
			CustoLabelPropertiesPointer,
			CustoLabelCategoryDefinitionProperties,
			CustoLabelCategoryEnumProperties,
			CustoLabelCategoryEnumCollectionProperties,
			UL_CustoLabel, 
			UL_CustoLabelCategory,
			UL_CustoLabelDefinition,
			UL_CustoPartLabelCategoryDefinition)


def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Object.custo_label_definition = bpy.props.CollectionProperty(type=CustoLabelDefinitionProperties)
	bpy.types.Object.custo_label_definition_idx = bpy.props.IntProperty(default=0)
	bpy.types.Object.custo_label_category_definition = bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)
	

def unregister():
	del bpy.types.Object.custo_label_definition
	del bpy.types.Object.custo_label_definition_idx
	del bpy.types.Object.custo_label_category_definition
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()