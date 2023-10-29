# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from .properties import (CustoSlotProperties, CustoPartSlotsProperties, CustoPartSlotsKeepLowerLayerProperties, UL_CustoSlot, UL_CustoPartSlots)
from .pannel import (PT_CustoSlotSetup, PT_CustoPartSetup)
from .OP_UL_custo_slot import (UI_AddSlot, UI_EditSlot, UI_DuplicateSlot, UI_MoveSlot, UI_ClearSlots, UI_RemoveSlot)
from .OP_UL_custo_part import (UI_RefreshPartSlots)

bl_info = {
    "name" : "Tila Character Customization Handler",
    "author" : "Tilapiatsu",
    "description" : "",
    "blender" : (2, 80, 0),
    "location" : "",
    "warning" : "",
    "category" : "Object"
}

def obj_selected_callback():
    bpy.ops.object.refresh_part_slots()

classes = (
            UI_AddSlot,
            UI_EditSlot,
            UI_DuplicateSlot,
            UI_MoveSlot,
            UI_ClearSlots,
            UI_RemoveSlot,
            UI_RefreshPartSlots,
            CustoSlotProperties,
            CustoPartSlotsProperties,
            CustoPartSlotsKeepLowerLayerProperties,
            UL_CustoSlot,
            UL_CustoPartSlots,
            PT_CustoSlotSetup,
            PT_CustoPartSetup
           )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.custo_slots = bpy.props.CollectionProperty(type=CustoSlotProperties)
    bpy.types.Scene.custo_slots_idx = bpy.props.IntProperty(default=0)

    bpy.types.Object.custo_part_slots = bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
    bpy.types.Object.custo_part_slots_idx = bpy.props.IntProperty(default=0)
    bpy.types.Object.custo_part_layer = bpy.props.IntProperty(default=0, min=0)
    bpy.types.Object.custo_part_keep_lower_slots = bpy.props.CollectionProperty(type=CustoPartSlotsKeepLowerLayerProperties)
    bpy.types.Object.custo_part_keep_lower_slots_idx = bpy.props.IntProperty(default=0)

    subscribe_to = bpy.types.LayerObjects, "active"
    bpy.types.Scene.object_selection_updater = object()
    bpy.msgbus.subscribe_rna(key=subscribe_to, owner=bpy.types.Scene.object_selection_updater, args=(), notify=obj_selected_callback) 

def unregister():

    del bpy.types.Scene.object_selection_updater

    del bpy.types.Object.custo_part_slots
    del bpy.types.Object.custo_part_slots_idx
    del bpy.types.Object.custo_part_layer
    del bpy.types.Object.custo_part_keep_lower_slots
    del bpy.types.Object.custo_part_keep_lower_slots_idx

    del bpy.types.Scene.custo_slots
    del bpy.types.Scene.custo_slots_idx

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
if __name__ == "__main__":
    register()