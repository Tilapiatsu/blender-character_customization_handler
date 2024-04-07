from . import node_label_properties, node_override_properties


def register():
    node_label_properties.register()
    node_override_properties.register()


def unregister():
    node_override_properties.unregister()
    node_label_properties.unregister()
