import bpy

class NodeAssetLabelProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Label Name', default='')
	invert : bpy.props.BoolProperty(default=False)

class UL_AssetLabelNode(bpy.types.UIList):
	bl_idname = "NODE_UL_AssetLabelNode"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'Not')
		row.prop(item, 'invert', text='')
		row.alignment = 'EXPAND'
		row.prop(item, 'name', text='')
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