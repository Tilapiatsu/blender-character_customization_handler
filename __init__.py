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
from . import operators, ui, customization_node, spawn, settings

from bpy.app.handlers import persistent

bl_info = {
    "name" : "Tila Customization Handler",
    "author" : "Tilapiatsu",
    "description" : "",
    "blender" : (4, 0, 0),
    "location" : "",
    "warning" : "",
    "category" : "Object"
}

def obj_selected_callback():
    bpy.ops.object.refresh_label_definition('INVOKE_DEFAULT')

def mat_selected_callback():
    settings.custo_handler_settings.update_label_category_definition(None, bpy.context)

@persistent
def register_object_selected_callback(dummy):
    subscribe_to = bpy.types.LayerObjects, "active"
    bpy.types.Scene.object_selection_updater = object()
    bpy.msgbus.subscribe_rna(key=subscribe_to, owner=bpy.types.Scene.object_selection_updater, args=(), notify=obj_selected_callback)

    bpy.types.Scene.material_selection_updater = object()
    subscribe_to = bpy.types.Object, "active_material_index"
    bpy.msgbus.subscribe_rna(key=subscribe_to, owner=bpy, args=(), notify=mat_selected_callback)


def register():
    spawn.register()
    operators.register()
    ui.register()
    customization_node.register()
    settings.register()
    
    bpy.app.handlers.load_post.append(register_object_selected_callback)

def unregister():
    del bpy.types.Scene.object_selection_updater

    settings.unregister()
    customization_node.unregister()
    ui.unregister()
    spawn.unregister()
    operators.unregister()

    
if __name__ == "__main__":
    register()