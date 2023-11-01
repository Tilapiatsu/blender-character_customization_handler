from bpy.types import NodeTree

# Implementation of custom nodes from Python


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
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'CustomizationTree'


