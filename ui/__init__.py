from . import pannel_3dview, pannel_object, pannel_scene

def register():
    pannel_3dview.register()
    pannel_object.register()
    pannel_scene.register()

def unregister():
    pannel_scene.unregister()
    pannel_object.unregister()
    pannel_3dview.unregister()