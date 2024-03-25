from . import panel_3dview, panel_material, panel_object, panel_scene

def register():
    panel_3dview.register()
    panel_object.register()
    panel_material.register()
    panel_scene.register()

def unregister():
    panel_scene.unregister()
    panel_object.unregister()
    panel_material.unregister()
    panel_3dview.unregister()