from . import node_sockets, node_socket_asset, node_socket_asset_type, node_socket_percentage


def register():
    node_sockets.register()
    node_socket_asset.register()
    node_socket_asset_type.register()
    node_socket_percentage.register()


def unregister():
    node_socket_percentage.unregister()
    node_socket_asset_type.unregister()
    node_socket_asset.unregister()
    node_sockets.unregister()
