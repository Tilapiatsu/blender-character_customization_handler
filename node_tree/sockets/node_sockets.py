import bpy
from bpy.types import NodeTreeInterfaceSocket

class CustomizationSocket:
	valid: bpy.props.BoolProperty()
	def socket_label(self, text):
		if self.is_output or (self.is_linked and self.valid) or (not self.is_output and not self.is_linked):
			return text
		else:
			return text + " [invalid]"

	def socket_color(self, color):
		if not self.is_output and self.is_linked and not self.valid:
			return (1.0, 0.0, 0.0, 1.0)
		else:
			return color

	# Returns a list of valid bl_idnames that can connect
	def valid_inputs(self):
		return [self.bl_idname]

	# Follows through reroutes
	def islinked(self):
		if self.is_linked() and not self.is_output:
			try: # During link removal this can be in a weird state
				node = self.links[0].from_node
				while node.type == "REROUTE":
					if node.inputs[0].is_linked and node.inputs[0].links[0].is_valid:
						node = node.inputs[0].links[0].from_node
					else:
						return False
				return True
			except:
				pass
		return False


# Customizable interface properties to generate a socket from.
class AssetsInterfaceSocket(NodeTreeInterfaceSocket):
	# The type of socket that is generated.
	bl_socket_idname = 'AssetsSocketType'

	default_value = []

	def draw(self, context, layout):
		# Display properties of the interface.
		layout.prop(self, "default_value")

	# Set properties of newly created sockets
	def init_socket(self, node, socket, data_path):
		socket.input_value = self.default_value

	# Use an existing socket to initialize the group interface
	def from_socket(self, node, socket):
		# Current value of the socket becomes the default
		self.default_value = socket.input_value



classes = (AssetsInterfaceSocket, )


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