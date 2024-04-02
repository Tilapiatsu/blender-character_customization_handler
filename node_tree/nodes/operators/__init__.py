from . import OP_UL_node_asset_label, OP_UL_node_asset_property
from . import properties

def register():
    properties.register()
    OP_UL_node_asset_label.register()
    OP_UL_node_asset_property.register()


def unregister():
    OP_UL_node_asset_property.unregister()
    OP_UL_node_asset_label.unregister()
    properties.unregister()