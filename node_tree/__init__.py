from . import sockets
from . import node_tree, node_categories, node_operators
from . import nodes
from .node_tree import CustomizationTree
from .node_const import TREE_NAME

def register():
    sockets.register()
    node_tree.register()
    node_categories.register()
    node_operators.register()
    nodes.register()

def unregister():
    nodes.unregister()
    node_operators.unregister()
    node_categories.unregister()
    node_tree.unregister()
    sockets.unregister()
