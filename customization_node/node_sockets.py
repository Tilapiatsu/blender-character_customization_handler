import bpy
from bpy.types import NodeSocket, NodeTreeInterfaceSocket

# Custom socket type
class AssetsSocket(NodeSocket):
    # Description string
    """Assets socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'AssetsSocketType'
    # Label for nice name display
    bl_label = "Assets Node Socket"

    input_value: bpy.props.StringProperty(
        name="Value",
        description="Value when the socket is not connected",
    )

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "input_value", text=text)

    # Socket color
    @classmethod
    def draw_color_simple(cls):
        return (1.0, 0.4, 0.216, 0.5)


# Customizable interface properties to generate a socket from.
class AssetsInterfaceSocket(NodeTreeInterfaceSocket):
    # The type of socket that is generated.
    bl_socket_idname = 'AssetsSocketType'

    default_value: bpy.props.FloatProperty(default=1.0, description="Default input value for new sockets",)

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
