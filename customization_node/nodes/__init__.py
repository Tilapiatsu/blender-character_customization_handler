from . import   (node_assets_append,
                node_assets_filter_by_labels, 
                node_assets_get_from_collection, 
                node_assets_selector, 
                node_assets_get_by_type, 
                node_assets_filter_by_layer,
                node_assets_filter_by_slots)
from . import operators

def register():
    operators.register()
    node_assets_append.register()
    node_assets_filter_by_labels.register()
    node_assets_filter_by_layer.register()
    node_assets_filter_by_slots.register()
    node_assets_get_from_collection.register()
    node_assets_selector.register()
    node_assets_get_by_type.register()


def unregister():
    node_assets_get_by_type.unregister()
    node_assets_selector.unregister()
    node_assets_get_from_collection.unregister()
    node_assets_filter_by_slots.unregister()
    node_assets_filter_by_labels.unregister()
    node_assets_filter_by_layer.unregister()
    node_assets_append.unregister()
    operators.unregister()
