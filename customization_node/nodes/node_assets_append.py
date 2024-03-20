import bpy
from bpy.types import Node
from .node import CustomizationTreeNode

class AssetsAppendNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Append node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsAppendNodeType'
	# Label for nice name display
	bl_label = "Append Assets"
	# Icon identifier
	bl_icon = 'NODETREE'

	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
		self.outputs.new('AssetsSocketType', "Assets")

	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		self.layout_header(layout, context)

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Append Assets"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		CustomizationTreeNode.update_inputs(self, 'AssetsSocketType', "Assets")

classes = (	AssetsAppendNode,)

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


