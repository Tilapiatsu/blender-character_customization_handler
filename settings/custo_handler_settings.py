import bpy
from ..operators.properties.custo_asset_properties import CustoAssetTypeProperties, CustoAssetProperties, CustoLabelEnumProperties, CustoLabelCategoryDefinitionProperties
from ..operators.properties.custo_slot_properties import CustoSlotProperties, CustoPartSlotsProperties
from ..operators.properties.custo_label_properties import CustoLabelPropertiesDisplay, CustoLabelCategoryProperties
from ..customization_node import TREE_NAME

def update_label_category(self, context):
	context.scene.custo_handler_settings.custo_labels.clear()
	for l in context.scene.custo_handler_settings.custo_label_categories[context.scene.custo_handler_settings.custo_label_categories_idx].labels:
		label = context.scene.custo_handler_settings.custo_labels.add()
		label.name = l.name
		label.valid_any = l.valid_any
		
def do_update_label_category_definition(context, prop, prop_source):
	prop.clear()
	
	if not len(prop_source):
		return
	
	label_to_remove=[]
	category_name = prop_source[context.scene.custo_handler_settings.custo_label_category_definition_idx].name

	for i,l in enumerate(prop_source[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels):
		for c in context.scene.custo_handler_settings.custo_label_categories:
			if c.name != category_name:
				continue

			if l.name not in c.labels:
				label_to_remove.append(i)

	for l in label_to_remove:
		prop_source[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels.remove(l)

	for l in prop_source[context.scene.custo_handler_settings.custo_label_category_definition_idx].labels:
		label = prop.add()
		label.name = l.name
		label.checked = l.checked
	
def update_label_category_definition(self, context):
	do_update_label_category_definition(context, context.object.custo_label_definition, context.object.custo_label_category_definition)
	for s in context.object.material_slots:
		if s.material is None:
			continue
		do_update_label_category_definition(context, s.material.custo_label_definition, s.material.custo_label_category_definition)

def is_customization_tree(self, context):
	return context.bl_idname == TREE_NAME

class CustoObjectProperties(bpy.types.PropertyGroup):
	object : bpy.props.PointerProperty(name='Object', type=bpy.types.Object)

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
	custo_labels : bpy.props.CollectionProperty(type=CustoLabelPropertiesDisplay)
	custo_labels_idx : bpy.props.IntProperty(default=0)
	custo_label_categories : bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
	custo_label_categories_idx : bpy.props.IntProperty(default=0, update=update_label_category)
	custo_label_category_definition_idx : bpy.props.IntProperty(default=0, update=update_label_category_definition)
	
	# Custo Tree
	custo_spawn_tree : bpy.props.PointerProperty(name='Spawn Tree', type=bpy.types.NodeTree, poll=is_customization_tree)
	custo_spawn_root : bpy.props.PointerProperty(name='Spawn Root', type=bpy.types.Object)
	custo_spawn_count : bpy.props.IntProperty(name='Spawn Count', default=1, min=1)
	custo_spawn_max_per_row : bpy.props.IntProperty(name='Max Spawn per Row', default=10, min=1)
	exclude_incomplete_mesh_combinaison : bpy.props.BoolProperty(name='Exclude Incomplete Combinaison', default=True)
	
	# Spawn
	spawned_mesh_instance : bpy.props.CollectionProperty(type=CustoObjectProperties)

classes = (CustoObjectProperties, CustoHandlerSettings, )

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