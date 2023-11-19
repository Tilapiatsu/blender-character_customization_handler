import bpy
from bpy.types import Node
from . import node_sockets
from .const_node import SPAWN_COLOR, INVALID_COLOR, TREE_NAME

# Follow an input link through any reroutes
def follow_input_link(link):
	if link.from_node.type == 'REROUTE':
		if link.from_node.inputs[0].is_linked:
			try: # During link insertion this can have weird states
				return follow_input_link(link.from_node.inputs[0].links[0])
			except:
				pass
	return link


def update_values(self, context):
	# self._assets = self.get_assets()
	self.update_color()


class CustomizationTreeNode:
	spawn : bpy.props.BoolProperty(name="Spawn", description="The Assets output of this tree will used dirring the spawning phase", default=False, update=update_values)
	
	@property
	def spawned_assets(self):
		return [a for a in self.assets if a.spawn]
	
	def node_tree(self, context):
		space = context.space_data
		node_tree = space.node_tree
		return node_tree

	@classmethod
	def poll(cls, ntree):
		return ntree.bl_idname == TREE_NAME
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self, socket_type=None, socket_name=None, sub_socket_dict=None):
		if socket_type is None:
			return
		idx = 0
		sub = 0
		if sub_socket_dict:
			sub = len(sub_socket_dict.keys())
		for socket in self.inputs:
			if socket.bl_idname != socket_type:
				idx = idx + 1
				continue
			if socket.is_linked or (hasattr(socket, 'value') and socket.value):
				if len(self.inputs) == idx + 1 + sub:
					self.inputs.new(socket_type, socket_name)
					if sub_socket_dict:
						for key in sub_socket_dict.keys():
							self.inputs.new(sub_socket_dict[key], key)
			else:
				if len(self.inputs) > idx + 1 + sub:
					self.inputs.remove(socket)
					rem = idx
					idx = idx - 1
					if sub_socket_dict:
						for key in sub_socket_dict.keys():
							self.inputs.remove(self.inputs[rem])
							idx = idx - 1
			idx = idx + 1

	# Update inputs and links on updates
	def update(self):
		self.update_color()
		self.update_inputs()
		# Links can get inserted without calling insert_link, but update is called.
		for socket in self.inputs:
			if socket.is_linked:
				self.insert_link(socket.links[0])

	# Validate incoming links
	def insert_link(self, link):
		if link.to_node == self:
			if follow_input_link(link).from_socket.bl_idname in link.to_socket.valid_inputs() and link.is_valid:
				link.to_socket.valid = True
			else:
				link.to_socket.valid = False
				
	def get_assets(self):
		input_assets = []
		for i,input in enumerate(self.inputs):
			if input.bl_idname != node_sockets.AssetsSocket.bl_idname:
				continue
			
			if not input.is_linked or not len(input.links):
				continue
			
			input_node = input.links[0].from_node
			current_input_assets = input_node.get_assets()
			input_assets += current_input_assets
		
		return input_assets
	
	def print_assets(self):
		assets = self.get_assets()
		print(f'{len(assets)} asset(s) found')
		print('---------------------------------------')
		for a in assets:
			print(a.name)
		print('---------------------------------------')

	# Follows through reroutes
	def islinked(self):
		if self.is_input_linked and not self.is_output:
			try: # During link removal this can be in a weird state
				node = self.links[0].from_node
				while node.type == "REROUTE":
					if node.inputs[0].is_input_linked and node.inputs[0].links[0].is_valid:
						node = node.inputs[0].links[0].from_node
					else:
						return False
				return True
			except:
				pass
		return False
	
	def is_input_linked(self):
		linked = False

		for input in self.inputs:
			if input.bl_idname != node_sockets.AssetsSocket.bl_idname:
				continue

			if not input.is_linked or not len(input.links):
				continue

			linked = True
			break

		return linked
	
	def update_color(self):
		if self.spawn and self.is_input_linked():
			self.use_custom_color = True
			self.color = SPAWN_COLOR
		elif not self.is_input_linked():
			self.use_custom_color = True
			self.color = INVALID_COLOR
		else:
			self.use_custom_color = False
	
	def layout_asset_count(self, layout, context):
		layout.prop(self, 'spawn')
		row = layout.row(align = True)
		row.label(text=f'{len(self.assets)} asset(s) found')
		op = row.operator("node.print_asset_list", text='', icon='ALIGN_JUSTIFY')
		op.node_name = self.name


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

	@property
	def assets(self):
		return self.get_assets()
	
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
		self.layout_asset_count(layout, context)

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
		self.layout_asset_count(layout, context)

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
	
	label: bpy.props.StringProperty(name="Label", description="Label", default="")
	invert: bpy.props.BoolProperty(name="Not", description="Invert rule", default=False)
	label_count: bpy.props.IntProperty(name="Label Count", description="Number of label to input", default=1, min=1)

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
		self.layout_asset_count(layout, context)
		layout.prop(self, 'label_count')
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(self, "invert")
		row.alignment = 'EXPAND'
		row.prop(self, "label", text='')
		
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


