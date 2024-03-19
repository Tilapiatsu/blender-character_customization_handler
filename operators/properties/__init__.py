from . import properties
from .properties import custo_label_properties, custo_slot_properties, custo_asset_properties
from . import custo_scene_properties

def register():
    properties.register()
    custo_scene_properties.register()


def unregister():
    custo_scene_properties.unregister()
    properties.unregister()
