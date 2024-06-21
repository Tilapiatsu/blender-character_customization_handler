import bpy
from .properties.custo_asset_properties import update_current_asset_properties
from .properties.custo_label_properties import get_label_category_labels

def update_custo_slot(self, context):
    print(self.asset_type.name)

def get_asset(context):
    idx = context.scene.custo_handler_settings.custo_assets_idx
    assets = context.scene.custo_handler_settings.custo_assets

    active = assets[idx] if len(assets) else None

    return idx, assets, active

def draw_label_categories(layout, label, data, property_count, property_name, source_data, source_name):
    property_count_value = getattr(data, property_count)
    # property_data = getattr(data, property_name).label_category_collection
    property_data = getattr(data, property_name).label_category_enums
    
    # Add or remove Label Category
    label_category_count = len(property_data)
    if label_category_count > property_count_value:
        property_data.remove(label_category_count-1)
    elif label_category_count < property_count_value:
        property_data.add()
    
    # Draw Category
    row = layout.row()
    row.label(text=label)
    row.prop(data, property_count, text='')
    for i in range(property_count_value):
        row = layout.row()
        row.separator()
        row.prop(property_data[i], 'name', text='')

    layout.separator()

def revert_assets_parameters(self):
    self.layer = 0
    
def set_current_label_category(self, context):
    context.scene.custo_handler_settings.current_label_category.clear()

    category = context.scene.custo_handler_settings.current_label_category.add()
    category.name = context.scene.custo_handler_settings.custo_asset_types[self.asset_type].mesh_slot_label_category.name
    for l in context.scene.custo_handler_settings.custo_label_categories[category.name].labels:
        if l.name in context.scene.custo_handler_settings.custo_assets[self.index].slots:
            l = context.scene.custo_handler_settings.custo_assets[self.index].slots[l.name]

        label = category.labels.add()
        label.name = l.name
        label.value = l.value
        label.keep_lower_layer_slot = l.keep_lower_layer_slot

class UI_MoveAsset(bpy.types.Operator):
    bl_idname = "scene.move_customization_asset"
    bl_label = "Move Asset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Move Asset up or down.\nThis controls the position in the List."

    direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

    @classmethod
    def poll(cls, context):
        return len(context.scene.custo_handler_settings.custo_assets)

    def execute(self, context):
        idx, asset, _ = get_asset(context)

        if self.direction == "UP":
            nextidx = max(idx - 1, 0)
        elif self.direction == "DOWN":
            nextidx = min(idx + 1, len(asset) - 1)

        asset.move(idx, nextidx)
        context.scene.custo_handler_settings.custo_assets_idx = nextidx

        return {'FINISHED'}


class UI_ClearAssets(bpy.types.Operator):
    bl_idname = "scene.clear_customization_assets"
    bl_label = "Clear All Assets"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Clear All Asset types"

    @classmethod
    def poll(cls, context):
        return len(context.scene.custo_handler_settings.custo_assets)
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        context.scene.custo_handler_settings.custo_assets.clear()
        return {'FINISHED'}


class UI_RemoveAsset(bpy.types.Operator):
    bl_idname = "scene.remove_customization_asset"
    bl_label = "Remove Selected Asset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Remove selected asset type"
    
    index : bpy.props.IntProperty(name="asset index", default=0)

    @classmethod
    def poll(cls, context):
        return context.scene.custo_handler_settings.custo_assets
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_confirm(self, event)

    def execute(self, context):
        _, assets, _ = get_asset(context)

        assets.remove(self.index)

        context.scene.custo_handler_settings.custo_assets_idx = min(self.index, len(context.scene.custo_handler_settings.custo_assets) - 1)

        return {'FINISHED'}


class UI_DuplicateAsset(bpy.types.Operator):
    bl_idname = "scene.duplicate_customization_asset"
    bl_label = "Duplicate Selected Asset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Duplicate selected Asset type"
    
    index : bpy.props.IntProperty(name="Operator ID", default=0)

    @classmethod
    def poll(cls, context):
        return context.scene.custo_handler_settings.custo_assets

    def execute(self, context):
        _, asset, _ = get_asset(context)

        s = asset.add()
        s.name = asset[self.index].asset_name
        s.layer = context.scene.custo_handler_settings.custo_assets[self.index].layer
        self.asset_type = asset[self.index].asset_type
        set_current_label_category(self, context)
        update_current_asset_properties(self.asset_type, context)
        asset.move(len(asset) - 1, self.index + 1)
        return {'FINISHED'}
    

class UI_EditAsset(bpy.types.Operator):
    bl_idname = "scene.edit_customization_asset"
    bl_label = "Edit Asset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Edit current customization asset type"

    index : bpy.props.IntProperty(name="Asset Index", default=0)
    asset_type : bpy.props.StringProperty(name="Asset Type", default='Label Category')
    asset_id : bpy.props.StringProperty(name="Asset ID", default='Label Category')
    layer : bpy.props.IntProperty(name="Layer", default=0, min=0)

    def separator(self, layout, iter):
        for i in range(iter):
            layout.separator()

    def draw(self, context):
        ch_settings=context.scene.custo_handler_settings
        layout = self.layout
        col = layout.column()
        col.prop_search(self, "asset_type", ch_settings, "custo_asset_types", text='Asset Type')
        
        asset_id_labels = get_label_category_labels(self.asset_type, 'asset_label_category')
        col.prop_search(self, "asset_id", asset_id_labels, "labels", text='Asset ID')

        col.separator()
        col.prop(self, 'layer', text='Layer')
        col.separator()
        b = col.box()
        b.label(text='Slots')
        row = b.row()

        rows = 20 if len(ch_settings.current_edited_asset_slots) > 20 else len(ch_settings.current_edited_asset_slots) + 1
        row.template_list('OBJECT_UL_CustoPartSlots', '', ch_settings, 'current_edited_asset_slots', ch_settings, 'current_edited_asset_slots_idx', rows=rows)

    def invoke(self, context, event):
        wm = context.window_manager
        self.init_parameters(context)
        return wm.invoke_props_dialog(self, width=500)

    def execute(self, context):
        ch_settings=context.scene.custo_handler_settings
        s = ch_settings.custo_assets[self.index]
            
        s.asset_type.name = self.asset_type
        s.layer = self.layer

        s.asset_id.name = self.asset_id
        s.asset_id.label_category_name = context.scene.custo_handler_settings.current_asset_id.label_category_name
        
        s.slots.clear()
        for slot in context.scene.custo_handler_settings.current_edited_asset_slots:
            current_slot = s.slots.add()
            current_slot.name = slot.name
            current_slot.value = slot.value
            current_slot.keep_lower_layer_slot = slot.keep_lower_layer_slot

        s.name = s.asset_id.name

        revert_assets_parameters(self)
        return {'FINISHED'}
    
    def init_parameters(self, context):
        ch_settings = context.scene.custo_handler_settings
        
        self.layer = ch_settings.custo_assets[self.index].layer
        self.asset_id = context.scene.custo_handler_settings.custo_assets[self.index].asset_id.name
        
        asset_types = ch_settings.custo_asset_types.keys()
        if not len(asset_types):
            self.report({'ERROR'}, "No Asset Types")
            return {'CANCELLED'}
        elif self.asset_type not in asset_types:
            self.asset_type = asset_types[0]

        set_current_label_category(self, context)
        update_current_asset_properties(self, context)

class UI_AddAsset(bpy.types.Operator):
    bl_idname = "scene.add_customization_asset"
    bl_label = "Add Asset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Add a customization asset type"

    asset_type : bpy.props.StringProperty(name="Asset Type", default='Label Category')
    asset_id : bpy.props.StringProperty(name="Asset ID", default='Label Category')
    layer : bpy.props.IntProperty(name="Layer", default=0, min=0)

    def separator(self, layout, iter):
        for i in range(iter):
            layout.separator()

    def draw(self, context):
        ch_settings=context.scene.custo_handler_settings
        layout = self.layout
        col = layout.column()
        col.prop_search(self, "asset_type", ch_settings, "custo_asset_types", text='Asset Type')
    
        asset_id_labels = get_label_category_labels(self.asset_type, 'asset_label_category')
        col.prop_search(self, "asset_id", asset_id_labels, "labels", text='Asset ID')

        col.separator()
        col.prop(self, 'layer', text='Layer')
        col.separator()
        b = col.box()
        b.label(text='Slots')
        row = b.row()

        rows = 20 if len(context.scene.custo_handler_settings.current_edited_asset_slots) > 20 else len(context.scene.custo_handler_settings.current_edited_asset_slots) + 1
        row.template_list('OBJECT_UL_CustoPartSlots', '', context.scene.custo_handler_settings, 'current_edited_asset_slots', context.scene.custo_handler_settings, 'current_edited_asset_slots_idx', rows=rows)

    def invoke(self, context, event):
        wm = context.window_manager
        self.init_parameters(context)
        return wm.invoke_props_dialog(self, width=500)

    def execute(self, context):
        s = context.scene.custo_handler_settings.custo_assets.add()

        s.asset_type.name = self.asset_type
        s.layer = self.layer

        asset_id_labels = get_label_category_labels(self.asset_type, 'asset_label_category')
        s.asset_id.name = self.asset_id
        s.asset_id.label_category_name = asset_id_labels.name
        
        for slot in context.scene.custo_handler_settings.current_edited_asset_slots:
            current_slot = s.slots.add()
            current_slot.name = slot.name
            current_slot.value = slot.value
            current_slot.keep_lower_layer_slot = slot.keep_lower_layer_slot

        s.name = s.asset_id.name
        revert_assets_parameters(self)
        return {'FINISHED'}
    
    def init_parameters(self, context):
        ch_settings=context.scene.custo_handler_settings
        asset_types = ch_settings.custo_asset_types.keys()
        self.layer = 0
        if not len(asset_types):
            self.report({'ERROR'}, "No Asset Types")
            return {'CANCELLED'}
        elif self.asset_type not in asset_types:
            self.asset_type = asset_types[0]
        self.set_current_label_category(context)
        update_current_asset_properties(self, context)
    
    def set_current_label_category(self, context):
        context.scene.custo_handler_settings.current_label_category.clear()

        for lc in context.scene.custo_handler_settings.custo_label_categories:
            category = context.scene.custo_handler_settings.current_label_category.add()
            category.name = lc.name
            for l in lc.labels:
                label = category.labels.add()
                label.name = l.name
                label.value = l.value
                label.keep_lower_layer_slot = l.keep_lower_layer_slot


classes = ( UI_MoveAsset, 
            UI_EditAsset, 
            UI_ClearAssets, 
            UI_AddAsset,
            UI_RemoveAsset)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

if __name__ == "__main__":
    register()