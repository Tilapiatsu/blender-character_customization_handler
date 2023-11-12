from nodeitems_utils import NodeCategory, NodeItem
from .const_node import TREE_NAME


### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see scripts/startup/nodeitems_builtins.py

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class CustomizationCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == TREE_NAME
    
# all categories in a list
node_categories = [
    CustomizationCategory('INPUTS', "Input", items=[
        NodeItem("AssetsGetFromCollectionNodeType"),
    ]),
    # identifier, label, items list
    CustomizationCategory('ASSETS', "Assets", items=[
        NodeItem("AssetsAppendNodeType"),
        NodeItem("AssetsFilterByLabelNodeType"),
    ]),
    CustomizationCategory('OTHERNODES', "Other Nodes", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NOTE: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("AssetsAppendNodeType", label="Node A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("AssetsAppendNodeType", label="Node B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
]


classes = (  
            )


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    import nodeitems_utils
    nodeitems_utils.register_node_categories('CUSTOMIZATION_NODES', node_categories)


def unregister():
    import nodeitems_utils
    nodeitems_utils.unregister_node_categories('CUSTOMIZATION_NODES')
    
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()