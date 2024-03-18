from . import sockets
from . import node_tree, node_categories, node_operators
from . import nodes

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
