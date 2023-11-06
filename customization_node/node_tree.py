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