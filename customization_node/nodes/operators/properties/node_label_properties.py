import bpy

class NodeAssetLabelProperties(bpy.types.PropertyGroup):
	label_category: bpy.props.StringProperty(name='Label Category', default='Label Category')
	name : bpy.props.StringProperty(name='Label Name', default='')
	invert : bpy.props.BoolProperty(default=False)

class UL_AssetLabelNode(bpy.types.UIList):
	bl_idname = "NODE_UL_AssetLabelNode"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'Not')
		row.prop(item, 'invert', text='')
		row.separator()
		row.alignment = 'EXPAND'
		
		if data.label_type == 'MESH_SLOT':
			row.prop_search(item, "name", context.scene.custo_handler_settings.custo_asset_types[data.node_tree.asset_type].mesh_slot_label_category.label_category, "labels", text='')
		elif data.label_type == 'MATERIAL_SLOT':
			row.prop_search(item, "name", context.scene.custo_handler_settings.custo_asset_types[data.node_tree.asset_type].material_slot_label_category.label_category, "labels", text='')
		else:
			row.prop_search(item, "label_category", context.scene.custo_handler_settings.custo_asset_types_label_categories[data.node_tree.asset_type], data.category_name, text='')
			if item.label_category in context.scene.custo_handler_settings.custo_label_categories.keys():
				row.prop_search(item, "name", context.scene.custo_handler_settings.custo_label_categories[item.label_category], "labels", text='')
			else:
				row.label(text='')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		o = row.operator('node.remove_asset_label', text='', icon='X')
		o.index = index
		o.node_name = data.name

classes = (NodeAssetLabelProperties,
		   UL_AssetLabelNode)

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