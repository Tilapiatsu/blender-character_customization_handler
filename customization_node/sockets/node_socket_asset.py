import bpy
from bpy.types import NodeSocket
from .node_sockets import CustomizationSocket

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
		return (1.0, 0.4, 0.216, 1.0)


classes = (AssetsSocket,)


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