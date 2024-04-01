import bpy
from bpy.types import NodeSocket
from .node_sockets import CustomizationSocket

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
		return (0.5, 0.5, 0.5, 1.0)

classes = (PercentageSocket,)


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