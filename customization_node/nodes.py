import bpy
from bpy.types import Node
from .node_tree import CustomizationTreeNode

   

# Derived from the Node base type.
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

    def reinit_inputs(self, context):
        input_count = len(self.inputs)
        if input_count > self.input_number:
            for i in range(input_count - self.input_number):
                self.inputs.remove(self.inputs[input_count-i-1])
        elif input_count < self.input_number:
            for _ in range(self.input_number - input_count):
                self.inputs.new('AssetsSocketType', "Assets")
            

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # https://docs.blender.org/api/current/bpy.props.html
    input_number: bpy.props.IntProperty(name='Inputs', default=2, min=2, update=reinit_inputs)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('AssetsSocketType', "Assets")
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
        layout.prop(self, "input_number")

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
        self.inputs.new('NodeSocketCollection', "Collection")

        self.outputs.new('AssetsSocketType', "Assets")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    # def draw_buttons(self, context, layout):
    #     layout.label(text="Node settings")
    #     layout.prop(self, "my_float_prop")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_float_prop")
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "my_string_prop")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "Get Assets From Collection"

classes = ( AssetsAppendNode, 
            AssetsGetFromCollectionNode)

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


