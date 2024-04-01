import bpy
from bpy.types import NodeSocket
from .node_sockets import CustomizationSocket

def get_asset_types(self, context):
	if len(context.scene.custo_handler_settings.custo_asset_types):
		return [(a.name, a.name, '') for a in context.scene.custo_handler_settings.custo_asset_types]
	else:
		return[('NONE', 'No Assets', '')]

# Asset socket type
class AssetTypesSocket(CustomizationSocket, NodeSocket):
	# Description string
	"""Asset Type socket type"""
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetTypeSocketType'
	# Label for nice name display
	bl_label = "Asset Type Node Socket"

	input_value : bpy.props.EnumProperty(items=get_asset_types)

	# Optional function for drawing the socket input value
	def draw(self, context, layout, node, text):
		# if self.is_output or self.is_linked:
		layout.prop_search(self, "input_value", context.scene.custo_handler_settings, "custo_asset_types", text='')
		# else:
		#     layout.prop(self, "input_value", text=text)

	# Socket color
	@classmethod
	def draw_color_simple(cls):
		return (1.0, 1.0, 0.0, 1.0)

classes = (AssetTypesSocket,)


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