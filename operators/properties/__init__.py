from . import custo_label_properties, custo_slot_properties

def register():
    custo_label_properties.register()
    custo_slot_properties.register()

def unregister():
    custo_slot_properties.unregister()
    custo_label_properties.unregister()