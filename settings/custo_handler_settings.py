import bpy
from ..operators.properties.custo_asset_properties import CustoAssetTypeProperties, CustoAssetProperties, CustoLabelEnumProperties, CustoLabelCategoryDefinitionProperties, CustoAssetTypeEnumProperties
from ..operators.properties.custo_slot_properties import CustoSlotProperties, CustoPartSlotsProperties
from ..operators.properties.custo_label_properties import CustoLabelPropertiesDisplay, CustoLabelCategoryProperties, NodeAssetTypeLabelCategories
from ..node_tree import TREE_NAME

def update_label_category(self, context):
	context.scene.custo_handler_settings.custo_labels.clear()
	for l in context.scene.custo_handler_settings.custo_label_categories[context.scene.custo_handler_settings.custo_label_categories_idx].labels:
		label = context.scene.custo_handler_settings.custo_labels.add()
		label.name = l.name
		label.valid_any = l.valid_any

def is_customization_tree(self, context):
	return context.bl_idname == TREE_NAME

class CustoObjectProperties(bpy.types.PropertyGroup):
	object : bpy.props.PointerProperty(name='Object', type=bpy.types.Object)

class CustoMaterialProperties(bpy.types.PropertyGroup):
	material : bpy.props.PointerProperty(name='Material', type=bpy.types.Material)

class CustoHandlerSettings(bpy.types.PropertyGroup):
	# Asset Properties
	custo_asset_types : bpy.props.CollectionProperty(type=CustoAssetTypeProperties)
	custo_asset_types_idx : bpy.props.IntProperty(default=0)
	custo_assets : bpy.props.CollectionProperty(type=CustoAssetProperties)
	custo_assets_idx : bpy.props.IntProperty(default=0, min=0)
	current_asset_id : bpy.props.PointerProperty(type=CustoLabelEnumProperties)
	current_asset_type : bpy.props.PointerProperty(type=CustoAssetTypeEnumProperties)
	current_asset_name : bpy.props.StringProperty()
	current_label_category : bpy.props.CollectionProperty(type=CustoLabelCategoryDefinitionProperties)

	# Slot Property ?
	custo_slots : bpy.props.CollectionProperty(type=CustoSlotProperties)
	custo_slots_idx : bpy.props.IntProperty(default=0)
	current_edited_asset_slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
	current_edited_asset_slots_idx : bpy.props.IntProperty(default=0)

	# Label Property
	custo_labels : bpy.props.CollectionProperty(type=CustoLabelPropertiesDisplay)
	custo_labels_idx : bpy.props.IntProperty(default=0)
	custo_label_categories : bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
	custo_label_categories_idx : bpy.props.IntProperty(default=0, update=update_label_category)
	custo_label_category_definition_idx : bpy.props.IntProperty(default=0, min=0)
	
	# Custo Tree
	custo_spawn_tree : bpy.props.PointerProperty(name='Spawn Tree', type=bpy.types.NodeTree, poll=is_customization_tree)
	custo_spawn_root : bpy.props.PointerProperty(name='Spawn Root', type=bpy.types.Object)
	custo_spawn_count : bpy.props.IntProperty(name='Spawn Count', default=1, min=1)
	custo_spawn_max_per_row : bpy.props.IntProperty(name='Max Spawn per Row', default=10, min=1)
	exclude_incomplete_mesh_combinaison : bpy.props.BoolProperty(name='Exclude Incomplete Combinaison', default=True)
	
    # Node
	custo_asset_types_label_categories : bpy.props.CollectionProperty(type=NodeAssetTypeLabelCategories)
	
	# Spawn
	spawned_mesh_instance : bpy.props.CollectionProperty(type=CustoObjectProperties)
	spawned_material_instance  : bpy.props.CollectionProperty(type=CustoMaterialProperties)

classes = (CustoObjectProperties, CustoMaterialProperties, CustoHandlerSettings)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Scene.custo_handler_settings = bpy.props.PointerProperty(type=CustoHandlerSettings)
	bpy.types.WindowManager.custo_label_definition_object_updated = bpy.props.BoolProperty(default=True)
	bpy.types.WindowManager.custo_label_definition_material_updated = bpy.props.BoolProperty(default=True)


def unregister():

	del bpy.types.Scene.custo_handler_settings
	del bpy.types.WindowManager.custo_label_definition_object_updated
	del bpy.types.WindowManager.custo_label_definition_material_updated
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()