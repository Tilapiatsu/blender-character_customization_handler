import bpy
from bpy.types import NodeTree
from . import node_sockets
from .const_node_color import SPAWN_COLOR, INVALID_COLOR

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
	print('update')


# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class CustomizationTree(NodeTree):
	# Description string
	'''Let you define the rules for assembling the final asset'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'CustomizationTree'
	# Label for nice name display
	bl_label = "Customization Tree"
	# Icon identifier
	bl_icon = 'NODETREE'
	


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class CustomizationTreeNode:
	spawn : bpy.props.BoolProperty(name="Spawn", description="The Assets output of this tree will used dirring the spawning phase", default=False, update=update_values)

	@classmethod
	def poll(cls, ntree):
		return ntree.bl_idname == 'CustomizationTree'
	
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