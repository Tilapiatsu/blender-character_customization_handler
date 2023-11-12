import bpy
from .const_node import TREE_NAME

class PrintAssetListOperator(bpy.types.Operator):
	"""Print All assets in current node"""
	bl_idname = "node.print_asset_list"
	bl_label = "Print Asset List"
	bl_options = {'REGISTER'}

	node_name: bpy.props.StringProperty(default="", name="Node", description="Name of the node")

	def node(self, context):
		self.tree = context.scene.custo_spawn_tree
		if self.tree:
			return self.tree.nodes.get(self.node_name)
		
	@classmethod
	def poll(cls, context):
		space = context.space_data
		return space.type == 'NODE_EDITOR' and context.scene.custo_spawn_tree is not None and context.scene.custo_spawn_tree.bl_idname == TREE_NAME

	def execute(self, context):
		self.node(context).print_assets()
		return {'FINISHED'}
	

classes = ( PrintAssetListOperator,
			)


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