from .node_tree import (CustomizationTree,)
from .node_sockets import (AssetsSocket, AssetsInterfaceSocket )
from .nodes_asset_append import (AssetsAppendNode,)
from .nodes_assets_get_from_collection import (AssetsGetFromCollectionNode,)
from .node_categories import node_categories
import nodeitems_utils

classes = (
    CustomizationTree,
    AssetsSocket,
    AssetsInterfaceSocket,
    AssetsAppendNode,
    AssetsGetFromCollectionNode,
)



def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOMIZATION_NODES', node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOMIZATION_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)