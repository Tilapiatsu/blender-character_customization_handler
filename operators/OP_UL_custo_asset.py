import bpy
from .properties.custo_asset_properties import CustoAssetTypeEnumProperties, update_current_asset_properties, get_asset_name

def update_custo_slot(self, context):
	print(self.asset_type.name)

def get_asset(context):
	idx = context.scene.custo_assets_idx
	assets = context.scene.custo_assets

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

class UI_MoveAsset(bpy.types.Operator):
	bl_idname = "scene.move_customization_asset"
	bl_label = "Move Asset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Asset up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_assets)

	def execute(self, context):
		idx, asset, _ = get_asset(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(asset) - 1)

		asset.move(idx, nextidx)
		context.scene.custo_assets_idx = nextidx

		return {'FINISHED'}


class UI_ClearAssets(bpy.types.Operator):
	bl_idname = "scene.clear_customization_assets"
	bl_label = "Clear All Assets"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Asset types"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_assets)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_assets.clear()
		return {'FINISHED'}


class UI_RemoveAsset(bpy.types.Operator):
	bl_idname = "scene.remove_customization_asset"
	bl_label = "Remove Selected Asset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected asset type"
	
	index : bpy.props.IntProperty(name="asset index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_assets
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, assets, _ = get_asset(context)

		assets.remove(self.index)

		context.scene.custo_assets_idx = min(self.index, len(context.scene.custo_assets) - 1)

		return {'FINISHED'}


class UI_DuplicateAsset(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_asset"
	bl_label = "Duplicate Selected Asset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Asset type"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_assets

	def execute(self, context):
		_, asset, _ = get_asset(context)

		s = asset.add()
		s.name = asset[self.index].name+'_dup'
		asset.move(len(asset) - 1, self.index + 1)
		return {'FINISHED'}

class UI_EditAsset(bpy.types.Operator):
	bl_idname = "scene.edit_customization_asset"
	bl_label = "Edit Asset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization asset type"

	index : bpy.props.IntProperty(name="Asset Index", default=0)
	asset_type : bpy.props.PointerProperty(name="Asset Type", type=CustoAssetTypeEnumProperties)
	layer : bpy.props.IntProperty(name="Layer", default=0, min=0)

	def separator(self, layout, iter):
		for i in range(iter):
			layout.separator()

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self.asset_type, 'name', text='Asset Type')
		
		col.label(text='Asset ID:')
		if len(context.scene.current_asset_id):
			row = col.row(align=True)
			self.separator(row, 10)
			col1 = row.column(align=True)
			for asset_id in context.scene.current_asset_id:
				col1.prop(asset_id, 'name', text='')

		col.separator()
		col.prop(self, 'layer', text='Layer')
		col.separator()
		b = col.box()
		b.label(text='Slots')
		row = b.row()

		rows = 20 if len(context.scene.current_edited_asset_slots) > 20 else len(context.scene.current_edited_asset_slots) + 1
		row.template_list('OBJECT_UL_CustoPartSlots', '', context.scene, 'current_edited_asset_slots', context.scene, 'current_edited_asset_slots_idx', rows=rows)

	def invoke(self, context, event):
		wm = context.window_manager
		self.init_parameters(context)
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_assets[self.index]
			
		s.asset_type.name = self.asset_type.name
		s.layer = self.layer

		s.asset_id.clear()
		for label in context.scene.current_asset_id:
			current_label = s.asset_id.add()
			current_label.label_category_name = label.label_category_name
			current_label.name = label.name
		
		s.slots.clear()
		for slot in context.scene.current_edited_asset_slots:
			current_slot = s.slots.add()
			current_slot.name = slot.name
			current_slot.checked = slot.checked
			current_slot.keep_lower_layer_slot = slot.keep_lower_layer_slot

		s.name = get_asset_name(s.asset_id)

		revert_assets_parameters(self)
		return {'FINISHED'}
	
	def init_parameters(self, context):
		self.layer = context.scene.custo_assets[self.index].layer
		context.scene.current_asset_name = get_asset_name(context.scene.custo_assets[self.index].asset_id)
		self.set_current_label_category(context)
		update_current_asset_properties(self.asset_type, context)

	def set_current_label_category(self, context):
		context.scene.current_label_category.clear()

		category = context.scene.current_label_category.add()
		category.name = context.scene.custo_asset_types[self.asset_type.name].slot_label_category.name
		for l in context.scene.custo_assets[self.index].slots:
			label = category.labels.add()
			label.name = l.name
			label.checked = l.checked
			label.keep_lower_layer_slot = l.keep_lower_layer_slot

class UI_AddAsset(bpy.types.Operator):
	bl_idname = "scene.add_customization_asset"
	bl_label = "Add Asset"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization asset type"

	asset_type : bpy.props.PointerProperty(name="Asset Type", type=CustoAssetTypeEnumProperties)
	layer : bpy.props.IntProperty(name="Layer", default=0, min=0)

	def separator(self, layout, iter):
		for i in range(iter):
			layout.separator()

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self.asset_type, 'name', text='Asset Type')
		
		col.label(text='Asset ID:')
		if len(context.scene.current_asset_id):
			row = col.row(align=True)
			self.separator(row, 10)
			col1 = row.column(align=True)
			for asset_id in context.scene.current_asset_id:
				col1.prop(asset_id, 'name', text='')

		col.separator()
		col.prop(self, 'layer', text='Layer')
		col.separator()
		b = col.box()
		b.label(text='Slots')
		row = b.row()

		rows = 20 if len(context.scene.current_edited_asset_slots) > 20 else len(context.scene.current_edited_asset_slots) + 1
		row.template_list('OBJECT_UL_CustoPartSlots', '', context.scene, 'current_edited_asset_slots', context.scene, 'current_edited_asset_slots_idx', rows=rows)

	def invoke(self, context, event):
		wm = context.window_manager
		self.init_parameters(context)
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_assets.add()

		s.asset_type.name = self.asset_type.name
		s.layer = self.layer

		for label in context.scene.current_asset_id:
			current_label = s.asset_id.add()
			current_label.label_category_name = label.label_category_name
			current_label.name = label.name
		
		for slot in context.scene.current_edited_asset_slots:
			current_slot = s.slots.add()
			current_slot.name = slot.name
			current_slot.checked = slot.checked
			current_slot.keep_lower_layer_slot = slot.keep_lower_layer_slot

		s.name = get_asset_name(s.asset_id)
		revert_assets_parameters(self)
		return {'FINISHED'}
	
	def init_parameters(self, context):
		self.layer = 0
		self.set_current_label_category(context)
		update_current_asset_properties(self.asset_type, context)
	
	def set_current_label_category(self, context):
		context.scene.current_label_category.clear()

		for lc in context.scene.custo_label_categories:
			category = context.scene.current_label_category.add()
			category.name = lc.name
			for l in lc.labels:
				label = category.labels.add()
				label.name = l.name
				label.checked = l.checked
				label.keep_lower_layer_slot = l.keep_lower_layer_slot


classes = ( UI_MoveAsset, 
			UI_EditAsset, 
			UI_ClearAssets, 
			UI_AddAsset,
			UI_RemoveAsset,
			UI_DuplicateAsset)

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