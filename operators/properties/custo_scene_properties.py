import bpy
from .properties.custo_asset_properties import CustoAssetTypeProperties, CustoAssetProperties, CustoLabelEnumProperties, CustoLabelCategoryDefinitionProperties
from .properties.custo_slot_properties import CustoSlotProperties, CustoPartSlotsProperties
from .properties.custo_label_properties import CustoLabelProperties, CustoLabelCategoryProperties

def update_label_category(self, context):
	context.scene.custo_handler_settings.custo_labels.clear()
	for l in context.scene.custo_handler_settings.custo_label_categories[context.scene.custo_handler_settings.custo_label_categories_idx].labels:
		label = context.scene.custo_handler_settings.custo_labels.add()
		label.name = l.name
	
def update_label_category_definition(self, context):
	context.object.custo_label_definition.clear()
	
	if not len(context.object.custo_label_category_definition):
		return
	
	label_to_remove=[]
	category_name = context.object.custo_label_category_definition[context.scene.custo_handler_settings.custo_label_category_definition_idx].name

	for i,l in enumerate(context.object.custo_label_category_definition[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels):
		for c in context.scene.custo_handler_settings.custo_label_categories:
			if c.name != category_name:
				continue

			if l.name not in c.labels:
				label_to_remove.append(i)

	for l in label_to_remove:
		context.object.custo_label_category_definition[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels.remove(l)

	for l in context.object.custo_label_category_definition[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels:
		label = context.object.custo_label_definition.add()
		label.name = l.name
		label.checked = l.checked

class CustoHandlerSettings(bpy.types.PropertyGroup):
	# Asset Properties
	custo_asset_types : bpy.props.CollectionProperty(type=CustoAssetTypeProperties)
	custo_asset_types_idx : bpy.props.IntProperty(default=0)
	custo_assets : bpy.props.CollectionProperty(type=CustoAssetProperties)
	custo_assets_idx : bpy.props.IntProperty(default=0, min=0)
	current_asset_id : bpy.props.CollectionProperty(type=CustoLabelEnumProperties)
	current_asset_id_idx : bpy.props.IntProperty(default=0, min=0)
	current_asset_name : bpy.props.StringProperty()
	current_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)

	# Slot Property ?
	custo_slots : bpy.props.CollectionProperty(type=CustoSlotProperties)
	custo_slots_idx : bpy.props.IntProperty(default=0)
	current_edited_asset_slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
	current_edited_asset_slots_idx : bpy.props.IntProperty(default=0)

	# Label Property
	custo_labels : bpy.props.CollectionProperty(type=CustoLabelProperties)
	custo_labels_idx : bpy.props.IntProperty(default=0)
	custo_label_categories : bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
	custo_label_categories_idx : bpy.props.IntProperty(default=0, update=update_label_category)
	custo_label_category_definition_idx : bpy.props.IntProperty(default=0, update=update_label_category_definition)

classes = (CustoHandlerSettings, )

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Scene.custo_handler_settings = bpy.props.PointerProperty(type=CustoHandlerSettings)


def unregister():

	del bpy.types.Scene.custo_handler_settings
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()