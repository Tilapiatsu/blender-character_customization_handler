from . import properties
from . import   (   OP_UL_custo_part, 
                    OP_UL_custo_label,
                    OP_UL_custo_label_category,
                    OP_UL_custo_part_label,
                    OP_UL_custo_slot,
                    OP_UL_custo_asset_type
                )

def register():
    properties.register()
    OP_UL_custo_part.register()
    OP_UL_custo_label.register()
    OP_UL_custo_label_category.register()
    OP_UL_custo_part_label.register()
    OP_UL_custo_slot.register()
    OP_UL_custo_asset_type.register()

def unregister():
    OP_UL_custo_asset_type.unregister()
    OP_UL_custo_part.unregister()
    OP_UL_custo_label.unregister()
    OP_UL_custo_label_category.unregister()
    OP_UL_custo_part_label.unregister()
    OP_UL_custo_slot.unregister()
    properties.unregister()