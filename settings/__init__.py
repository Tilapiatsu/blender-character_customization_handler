from . import custo_handler_settings

def register():
    custo_handler_settings.register()

def unregister():
    custo_handler_settings.unregister()

if __name__ == "__main__":
    register()