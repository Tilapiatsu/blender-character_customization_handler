import bpy

def update_label_category(self, context):
	context.scene.custo_labels.clear()
	for l in context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels:
		label = context.scene.custo_labels.add()
		label.name = l.name
	
def update_part_label_category(self, context):
	context.object.custo_part_labels.clear()
	
	if not len(context.object.custo_part_label_categories):
		return
	
	label_to_remove=[]
	category_name = context.object.custo_part_label_categories[context.object.custo_part_label_categories_idx].name

	for i,l in enumerate(context.object.custo_part_label_categories[context.object.custo_part_label_categories_idx].labels):
		for c in context.scene.custo_label_categories:
			if c.name != category_name:
				continue

			if l.name not in c.labels:
				label_to_remove.append(i)

	for l in label_to_remove:
		context.object.custo_part_label_categories[context.object.custo_part_label_categories_idx].labels.remove(l)

	for l in context.object.custo_part_label_categories[context.object.custo_part_label_categories_idx].labels:
		label = context.object.custo_part_labels.add()
		label.name = l.name
		label.checked = l.checked

def update_part_labels(self, context):
	i=0
	for l in context.object.custo_part_label_categories[context.object.custo_part_label_categories_idx].labels:
		if i > len(context.object.custo_part_labels) - 1:
			return
		l.checked = context.object.custo_part_labels[i].checked
		i+=1


class CustoLabelProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	checked : bpy.props.BoolProperty(default=False)
	
class CustoLabelCategoryProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Category', default='')
	labels : bpy.props.CollectionProperty(type=CustoLabelProperties)

class CustoPartLabelProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	checked : bpy.props.BoolProperty(default=False, update=update_part_labels)
	
class CustoPartLabelCategoryProperties(bpy.types.PropertyGroup):
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

class UL_CustoPartLabel(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoPartLabels"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(item, 'checked', text='')
		row.separator()
		row.label(text=f'{item.name}')
		
class UL_CustoPartLabelCategory(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoPartLabelCategories"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		

classes = ( CustoLabelProperties, 
            CustoLabelCategoryProperties,
            CustoPartLabelProperties,
            CustoPartLabelCategoryProperties,
            UL_CustoLabel, 
            UL_CustoLabelCategory,
            UL_CustoPartLabel,
            UL_CustoPartLabelCategory)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
		
    bpy.types.Scene.custo_labels = bpy.props.CollectionProperty(type=CustoLabelProperties)
    bpy.types.Scene.custo_labels_idx = bpy.props.IntProperty(default=0)
    bpy.types.Scene.custo_label_categories = bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
    bpy.types.Scene.custo_label_categories_idx = bpy.props.IntProperty(default=0, update=update_label_category)

    bpy.types.Object.custo_part_layer = bpy.props.IntProperty(default=0, min=0)
    bpy.types.Object.custo_part_labels = bpy.props.CollectionProperty(type=CustoPartLabelProperties)
    bpy.types.Object.custo_part_labels_idx = bpy.props.IntProperty(default=0)
    bpy.types.Object.custo_part_label_categories = bpy.props.CollectionProperty(type=CustoPartLabelCategoryProperties)
    bpy.types.Object.custo_part_label_categories_idx = bpy.props.IntProperty(default=0, update=update_part_label_category)

def unregister():
    del bpy.types.Scene.custo_labels
    del bpy.types.Scene.custo_labels_idx
    del bpy.types.Scene.custo_label_categories
    del bpy.types.Scene.custo_label_categories_idx

    del bpy.types.Object.custo_part_layer
    del bpy.types.Object.custo_part_labels
    del bpy.types.Object.custo_part_labels_idx
    del bpy.types.Object.custo_part_label_categories
    del bpy.types.Object.custo_part_label_categories_idx
	
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
	

if __name__ == "__main__":
    register()