import bpy

def update_node_assets(self, context):
	node_tree = self.node_tree
	if node_tree is None:
		return
	
	for n in node_tree.custo_nodes:
		if n.mute: continue

		n.assets


class NodeAssetLabelProperties(bpy.types.PropertyGroup):
	label_category: bpy.props.StringProperty(name='Label Category', default='Label Category', update=update_node_assets)
	name : bpy.props.StringProperty(name='Label Name', default='', update=update_node_assets)
	invert : bpy.props.BoolProperty(default=False, update=update_node_assets)
	weight : bpy.props.FloatProperty(default=1.0, min=0, update=update_node_assets)

	@property
	def node_tree(self):
		ch_settings = bpy.context.scene.custo_handler_settings
		space = bpy.context.space_data
		node_tree = getattr(space, 'node_tree', None)

		if node_tree is None:
			if ch_settings.custo_spawn_tree is None:
				return None
			else:
				node_tree = ch_settings.custo_spawn_tree
				
		return node_tree

class UL_AssetLabelNode(bpy.types.UIList):
	bl_idname = "NODE_UL_AssetLabelNode"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		ch_settings = context.scene.custo_handler_settings
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'Not')
		row.prop(item, 'invert', text='')
		row.separator()
		row.alignment = 'EXPAND'
		
		if data.label_type == 'ASSET_NAME':
			row.prop_search(item, "name", ch_settings.custo_asset_types[data.node_tree.asset_type].asset_label_category.label_category, "labels", text='')
			row = layout.row(align=True)
			row.alignment = 'RIGHT'
			row.ui_units_x = 5
			row.prop(item, "weight", text='w')
		elif data.label_type == 'MESH_SLOT':
			row.prop_search(item, "name", ch_settings.custo_asset_types[data.node_tree.asset_type].mesh_slot_label_category.label_category, "labels", text='')
			row = layout.row(align=True)
			row.alignment = 'RIGHT'
			row.ui_units_x = 5
			row.prop(item, "weight", text='w')
		elif data.label_type == 'MATERIAL_SLOT':
			row.prop_search(item, "name", ch_settings.custo_asset_types[data.node_tree.asset_type].material_slot_label_category.label_category, "labels", text='')
			row = layout.row(align=True)
			row.alignment = 'RIGHT'
			row.ui_units_x = 5
			row.prop(item, "weight", text='w')
		else:
			row.prop_search(item, "label_category", ch_settings.custo_asset_types_label_categories[data.node_tree.asset_type], data.category_name, text='')
			if item.label_category in ch_settings.custo_label_categories.keys():
				row.prop_search(item, "name", ch_settings.custo_label_categories[item.label_category], "labels", text='')
				row = layout.row(align=True)
				row.alignment = 'RIGHT'
				row.ui_units_x = 5
				row.prop(item, "weight", text='w')
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