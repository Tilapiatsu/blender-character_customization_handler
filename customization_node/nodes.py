import bpy
from bpy.types import Node
from .node_tree import CustomizationTreeNode


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
	# === Custom Properties ===
	# These work just like custom properties in ID data blocks
	# Extensive information can be found under
	# https://docs.blender.org/api/current/bpy.props.html

	# === Optional Functions ===
	# Initialization function, called when a new node is created.
	# This is the most common place to create the sockets for a node, as shown below.
	# NOTE: this is not the same as the standard __init__ function in Python, which is
	#       a purely internal Python method and unknown to the node system!

	def init(self, context):
		# Inputs
		self.inputs.new('NodeSocketCollection', "Collection")

		# Outputs
		self.outputs.new('AssetsSocketType', "Assets")

	@property
	def assets(self):
		return self.get_assets()
	
	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")
	
	def get_assets(self):
		all_assets = []
		collection = self.inputs[0].default_value
		if collection is None:
			return
		all_assets += [o for o in collection.all_objects if o.type in self.object_types]
		children_collections = collection.children_recursive
		for c in children_collections:
			all_assets += [o for o in c.all_objects if o.type in self.object_types]

		# print("all assets =", all_assets)
		return all_assets

	def update_inputs(self):
		pass

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		layout.label(text=f'{len(self.assets)} asset(s) found')
		pass

	# Detail buttons in the sidebar.
	# If this function is not defined, the draw_buttons function is used instead
	def draw_buttons_ext(self, context, layout):
		pass
		# layout.prop(self, "my_float_prop")
		# my_string_prop button will only be visible in the sidebar
		# layout.prop(self, "my_string_prop")

	# Optional: custom label
	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Get Assets From Collection"


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
			
	# === Custom Properties ===
	# These work just like custom properties in ID data blocks
	# Extensive information can be found under
	# https://docs.blender.org/api/current/bpy.props.html
	# input_number: bpy.props.IntProperty(name='Inputs', default=2, min=2, update=reinit_inputs)

	# === Optional Functions ===
	# Initialization function, called when a new node is created.
	# This is the most common place to create the sockets for a node, as shown below.
	# NOTE: this is not the same as the standard __init__ function in Python, which is
	#       a purely internal Python method and unknown to the node system!
	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
		self.outputs.new('AssetsSocketType', "Assets")

	
	@property
	def assets(self):
		return self.get_assets()


	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		layout.label(text=f'{len(self.assets)} asset(s) found')

	# # Detail buttons in the sidebar.
	# # If this function is not defined, the draw_buttons function is used instead
	# def draw_buttons_ext(self, context, layout):
	#     layout.prop(self, "my_float_prop")
	#     # my_string_prop button will only be visible in the sidebar
	#     layout.prop(self, "my_string_prop")

	# Optional: custom label
	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Append Assets"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		CustomizationTreeNode.update_inputs(self, 'AssetsSocketType', "Assets")


class AssetsFilterByLabelNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Label node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByLabelNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Label"
	# Icon identifier
	bl_icon = 'NODETREE'
			
	# === Custom Properties ===
	# These work just like custom properties in ID data blocks
	# Extensive information can be found under
	# https://docs.blender.org/api/current/bpy.props.html
	# input_number: bpy.props.IntProperty(name='Inputs', default=2, min=2, update=reinit_inputs)

	# === Optional Functions ===
	# Initialization function, called when a new node is created.
	# This is the most common place to create the sockets for a node, as shown below.
	# NOTE: this is not the same as the standard __init__ function in Python, which is
	#       a purely internal Python method and unknown to the node system!
	label: bpy.props.StringProperty(name="Label", description="Label", default="")
	invert: bpy.props.BoolProperty(name="Not", description="Invert rule", default=False)

	@property
	def assets(self):
		return self.get_assets()

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
		layout.label(text=f'{len(self.assets)} asset(s) found')
		layout.prop(self, "invert")
		layout.prop(self, "label")

	# # Detail buttons in the sidebar.
	# # If this function is not defined, the draw_buttons function is used instead
	# def draw_buttons_ext(self, context, layout):
	#     layout.prop(self, "my_float_prop")
	#     # my_string_prop button will only be visible in the sidebar
	#     layout.prop(self, "my_string_prop")

	# Optional: custom label
	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Filter Assets By Label"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):		
		# filtering by label
		filtered = []
		assets = super().get_assets()

		if not len(self.label):
			if self.invert:
				return assets
			else:
				return []
		
		for o in assets:
			for lc in o.custo_part_label_categories:
				for l in lc.labels:
					if self.label not in l.name:
						continue
					if l.checked and not self.invert or not l.checked and self.invert:
						filtered.append(o)

		# print(f'filtered input =', filtered)

		return filtered


classes = ( AssetsAppendNode, 
			AssetsGetFromCollectionNode,
			AssetsFilterByLabelNode)

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


