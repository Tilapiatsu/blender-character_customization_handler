import bpy
from bpy.types import NodeSocket, NodeTreeInterfaceSocket

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


# Asset socket type
class AssetsSocket(CustomizationSocket, NodeSocket):
	# Description string
	"""Assets socket type"""
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsSocketType'
	# Label for nice name display
	bl_label = "Assets Node Socket"

	input_value = []

	# Optional function for drawing the socket input value
	def draw(self, context, layout, node, text):
		# if self.is_output or self.is_linked:
		layout.label(text=text)
		# else:
		#     layout.prop(self, "input_value", text=text)

	# Socket color
	@classmethod
	def draw_color_simple(cls):
		return (1.0, 0.4, 0.216, 0.5)

# Custom socket type
class PercentageSocket(CustomizationSocket, NodeSocket):
	# Description string
	"""Percentage socket type"""
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'PercentageSocketType'
	# Label for nice name display
	bl_label = "Percentage Node Socket"

	input_value: bpy.props.IntProperty(name='Percentage', default=100, min=0, max=100)

	# Optional function for drawing the socket input value
	def draw(self, context, layout, node, text):
		if self.is_output or self.is_linked:
			layout.label(text=text)
		else:
			layout.prop(self, "input_value", text=text)

	# Socket color
	@classmethod
	def draw_color_simple(cls):
		return (0.5, 0.5, 0.5, 0.5)

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


classes = ( AssetsSocket,
			PercentageSocket,
			AssetsInterfaceSocket )


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