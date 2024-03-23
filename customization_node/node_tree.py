import bpy
from bpy.types import NodeTree
from .node_const import TREE_NAME

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class CustomizationTree(NodeTree):
	# Description string
	'''Let you define the rules for assembling the final asset'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = TREE_NAME
	# Label for nice name display
	bl_label = "Customization Tree"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	@property
	def custo_nodes(self):
		return [n for n in self.nodes if n.bl_static_type not in ['REROUTE']]


classes = ( CustomizationTree,
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