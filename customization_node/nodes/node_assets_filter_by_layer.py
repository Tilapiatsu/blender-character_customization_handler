import bpy
from bpy.types import Node
from .node import CustomizationTreeNode

class AssetsFilterByLayerNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Layer node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByLayerNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Layer"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	operation: bpy.props.EnumProperty(name='operation', items=[('EQUAL', 'Equal', ''),
																('GREATER', 'Greater Than', ''),
																('LESS', 'Less Than', '')])
	layer: bpy.props.IntProperty(name="Layer", min=0, default=0)
	

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
		self.draw_main(layout)
	
	def draw_main(self, layout):
		layout.prop(self, 'operation', text='')
		layout.prop(self, 'layer')

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Filter Assets By Labels"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):
		assets = super().get_assets()
		
		# skip node if muted
		if self.mute:
			return assets
		
		if self.operation == 'EQUAL':
			return [a for a in assets if a.layer == self.layer]
		elif self.operation == 'GREATER':
			return [a for a in assets if a.layer > self.layer]
		elif self.operation == 'LESS':
			return [a for a in assets if a.layer < self.layer]


classes = (AssetsFilterByLayerNode,)

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


