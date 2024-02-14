from . import OP_UL_custo_label_definition, properties
from . import   (   OP_UL_custo_part, 
                    OP_UL_custo_label,
                    OP_UL_custo_label_category,
                    OP_UL_custo_slot,
                    OP_UL_custo_asset_type,
                    OP_UL_custo_asset
                )

def register():
    properties.register()
    OP_UL_custo_part.register()
    OP_UL_custo_label.register()
    OP_UL_custo_label_category.register()
    OP_UL_custo_label_definition.register()
    OP_UL_custo_slot.register()
    OP_UL_custo_asset_type.register()
    OP_UL_custo_asset.register()

def unregister():
    OP_UL_custo_asset.unregister()
    OP_UL_custo_asset_type.unregister()
    OP_UL_custo_part.unregister()
    OP_UL_custo_label.unregister()
    OP_UL_custo_label_category.unregister()
    OP_UL_custo_label_definition.unregister()
    OP_UL_custo_slot.unregister()
    properties.unregister()