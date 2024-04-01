import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .node_const import SPAWN_COLOR

class AssetsGetFromCollectionNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Get From Collection node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsGetFromCollectionNodeType'
	# Label for nice name display
	bl_label = "Get From Collection Assets"
	# Icon identifier
	bl_icon = 'NODETREE'

	object_types = ['MESH', 'CURVE', 'SURFACE', 'META']

	def init(self, context):
		# Inputs
		self.inputs.new('NodeSocketCollection', "Collection")

		# Outputs
		self.outputs.new('AssetsSocketType', "Assets")
	
	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")
		
	def islinked(self):
		return False
	
	def get_assets(self):
		collection = self.inputs[0].default_value
		if collection is None:
			return []
		
		all_assets = []
		all_assets += [o for o in collection.all_objects if o.type in self.object_types]
		children_collections = collection.children_recursive
		for c in children_collections:
			all_assets += [o for o in c.all_objects if o.type in self.object_types]

		return all_assets

	def update_inputs(self):
		pass

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		self.layout_header(layout, context)

	# Detail buttons in the sidebar.
	# If this function is not defined, the draw_buttons function is used instead
	def draw_buttons_ext(self, context, layout):
		pass
		# layout.prop(self, "my_float_prop")
		# my_string_prop button will only be visible in the sidebar
		# layout.prop(self, "my_string_prop")

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Get Assets From Collection"
	
	def update_color(self):
		if self.spawn:
			self.use_custom_color = True
			self.color = SPAWN_COLOR
		else:
			self.use_custom_color = False


classes = ( AssetsGetFromCollectionNode,)

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


