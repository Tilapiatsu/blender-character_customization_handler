from . import node_assets_append, node_assets_filter_by_labels, node_assets_get_from_collection

def register():
    node_assets_append.register()
    node_assets_filter_by_labels.register()
    node_assets_get_from_collection.register()


def unregister():
    node_assets_get_from_collection.unregister()
    node_assets_filter_by_labels.unregister()
    node_assets_append.unregister()