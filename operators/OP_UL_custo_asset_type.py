import bpy
from .properties.custo_label_properties import CustoLabelCategoryEnumProperties, CustoLabelCategoryEnumCollectionProperties, draw_label_category_search, label_enum
from .properties.custo_asset_properties import asset_type_enum

def get_asset_type(context):
	idx = context.scene.custo_handler_settings.custo_asset_types_idx
	asset_types = context.scene.custo_handler_settings.custo_asset_types

	active = asset_types[idx] if len(asset_types) else None

	return idx, asset_types, active

def draw_label_categories(layout, label, label_count, data, property_count, property_name):
	property_count_value = getattr(data, property_count)
	property_data = getattr(data, property_name).label_category_enums
	
	# Add or remove Label Category
	label_category_count = len(property_data)
	if label_category_count > property_count_value:
		property_data.remove(label_category_count-1)
	elif label_category_count < property_count_value:
		property_data.add()
	
	# Draw Category
	layout.separator()
	box = layout.box()
	
	row = box.row(align=True)
	row.label(text=label_count)
	row.prop(data, property_count, text='')
	row = box.row()
	row.label(text=label)

	col = row.column()
	for i in range(property_count_value):
		col.prop(property_data[i], 'name', text='')

	layout.separator()

def revert_asset_types_parameters(self):
	self.material_variation_label_categories.label_category_enums.clear()
	self.mesh_variation_label_categories.label_category_enums.clear()
	self.material_variation_label_categories_count = 0
	self.mesh_variation_label_category_count = 0
	ch_settings = bpy.context.scene.custo_handler_settings
	ch_settings.current_material_variation_label_categories.label_category_enums.clear()
	ch_settings.current_mesh_variation_label_categories.label_category_enums.clear()
	ch_settings.current_mesh_slot_label_category.name = ch_settings.current_asset_label_category.name
	ch_settings.current_material_slot_label_category.name = ch_settings.current_asset_label_category.name
	ch_settings.current_material_label_category.name = ch_settings.current_asset_label_category.name



class UI_MoveAssetType(bpy.types.Operator):
	bl_idname = "scene.move_customization_asset_type"
	bl_label = "Move Asset Type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Asset type up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_asset_types)

	def execute(self, context):
		idx, asset_type, _ = get_asset_type(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(asset_type) - 1)

		asset_type.move(idx, nextidx)
		context.scene.custo_handler_settings.custo_asset_types_idx = nextidx

		return {'FINISHED'}


class UI_ClearAssetTypes(bpy.types.Operator):
	bl_idname = "scene.clear_customization_asset_types"
	bl_label = "Clear All Asset types"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Asset Types"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_asset_types)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_handler_settings.custo_asset_types.clear()
		return {'FINISHED'}


class UI_RemoveAssetType(bpy.types.Operator):
	bl_idname = "scene.remove_customization_asset_type"
	bl_label = "Remove Selected Asset type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected asset type"
	
	index : bpy.props.IntProperty(name="asset type index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_asset_types
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, asset_types, _ = get_asset_type(context)

		asset_types.remove(self.index)

		context.scene.custo_handler_settings.custo_asset_types_idx = min(self.index, len(context.scene.custo_handler_settings.custo_asset_types) - 1)

		return {'FINISHED'}


class UI_DuplicateAssetType(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_asset_type"
	bl_label = "Duplicate Selected Asset Type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Asset Type"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_asset_types

	def execute(self, context):
		_, asset_type, _ = get_asset_type(context)

		s = asset_type.add()
		s.name = asset_type[self.index].name+'_dup'
		asset_type.move(len(asset_type) - 1, self.index + 1)
		return {'FINISHED'}

class UI_EditAssetType(bpy.types.Operator):
	bl_idname = "scene.edit_customization_asset_type"
	bl_label = "Edit Asset Type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization asset type"

	index : bpy.props.IntProperty(name="Asset Type Index", default=0)
	name : bpy.props.StringProperty(name="Asset Type Name", default="")
	mesh_variation_label_category_count : bpy.props.IntProperty(name="Mesh Variation Label Category Count", default=1, min=1)
	mesh_variation_label_categories : bpy.props.PointerProperty(name="Mesh Variation Label Categories", type=CustoLabelCategoryEnumCollectionProperties)
	material_variation_label_category_count : bpy.props.IntProperty(name="Material Variation Label Category Count", default=1, min=1)
	material_variation_label_categories : bpy.props.PointerProperty(name="Material Variation Label Category", type=CustoLabelCategoryEnumCollectionProperties)

	def draw(self, context):
		layout = self.layout
		
		ch_settings = context.scene.custo_handler_settings
		col = layout.column()
		layout.use_property_split = True
		layout.use_property_decorate = False
		col.prop(self, 'name', text='Name')

		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_asset_label_category.name', text=ch_settings.current_asset_label_category.name, label='Asset ID: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_mesh_slot_label_category.name', text=ch_settings.current_mesh_slot_label_category.name, label='Mesh Slots: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_material_slot_label_category.name', text=ch_settings.current_material_slot_label_category.name, label='Material Slot: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_material_label_category.name', text=ch_settings.current_material_label_category.name, label='Material: ')
		draw_label_categories(col,'Mesh Variations:', 'Mesh Variation Count:', self, 'mesh_variation_label_category_count', 'mesh_variation_label_categories')
		draw_label_categories(col, 'Material Variations:','Material Variation Count:', self, 'material_variation_label_category_count', 'material_variation_label_categories')
	
	def invoke(self, context, event):
		ch_settings = context.scene.custo_handler_settings
		ch_settings.current_mesh_variation_label_categories.label_category_enums.clear()
		ch_settings.current_material_variation_label_categories.label_category_enums.clear()

		self.current_asset_type = context.scene.custo_handler_settings.custo_asset_types[self.index]
		self.name = self.current_asset_type.name
		self.old_name = self.current_asset_type.name

		ch_settings.current_asset_label_category.name = self.current_asset_type.asset_label_category.name
		ch_settings.current_mesh_slot_label_category.name = self.current_asset_type.mesh_slot_label_category.name

		self.mesh_variation_label_category_count = len(self.current_asset_type.mesh_variation_label_categories)

		for lc in self.current_asset_type.mesh_variation_label_categories:
			label_category = self.mesh_variation_label_categories.label_category_enums.add()
			label_category.name = lc.name
			label_category = ch_settings.current_mesh_variation_label_categories.label_category_enums.add()
			label_category.name = lc.name

		ch_settings.current_material_slot_label_category.name = self.current_asset_type.material_slot_label_category.name
		ch_settings.current_material_label_category.name = self.current_asset_type.material_label_category.name
		self.material_variation_label_category_count = len(self.current_asset_type.material_variation_label_categories)

		for lc in self.current_asset_type.material_variation_label_categories:
			label_category = self.material_variation_label_categories.label_category_enums.add()
			label_category.name = lc.name
			label_category = ch_settings.current_material_variation_label_categories.label_category_enums.add()
			label_category.name = lc.name
	
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)
	
	def execute(self, context):
		ch_settings = context.scene.custo_handler_settings
		self.current_asset_type.name = self.name
		self.refresh_assets_asset_types(context)

		self.current_asset_type.asset_label_category.name = ch_settings.current_asset_label_category.name
		
		self.current_asset_type.mesh_slot_label_category.name = ch_settings.current_mesh_slot_label_category.name
		
		self.current_asset_type.mesh_variation_label_categories.clear()
		for l in self.mesh_variation_label_categories.label_category_enums:
			asset_label = self.current_asset_type.mesh_variation_label_categories.add()
			asset_label.name = l.name

		self.current_asset_type.material_slot_label_category.name = ch_settings.current_material_slot_label_category.name
		self.current_asset_type.material_label_category.name = ch_settings.current_material_label_category.name

		self.current_asset_type.material_variation_label_categories.clear()
		for l in self.material_variation_label_categories.label_category_enums:
			asset_label = self.current_asset_type.material_variation_label_categories.add()
			asset_label.name = l.name

		revert_asset_types_parameters(self)
		return {'FINISHED'}
	
	def refresh_assets_asset_types(self, context):
		for asset in context.scene.custo_handler_settings.custo_assets:
			if asset.asset_type.name == self.old_name:
				asset.asset_type.name = self.name	
	

class UI_AddAssetType(bpy.types.Operator):
	bl_idname = "scene.add_customization_asset_type"
	bl_label = "Add Asset Type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization asset type"

	name : bpy.props.StringProperty(name="Asset Type Name", default="")
	asset_label_category : bpy.props.PointerProperty(name="Asset Label Categories", type=CustoLabelCategoryEnumProperties)
	mesh_variation_label_category_count : bpy.props.IntProperty(name="Mesh Variation Label Category Count", default=1, min=1)
	mesh_variation_label_categories : bpy.props.PointerProperty(name="Mesh Variation Label Categories", type=CustoLabelCategoryEnumCollectionProperties)
	material_variation_label_category_count : bpy.props.IntProperty(name="Material Variation Label Category Count", default=1, min=1)
	material_variation_label_categories : bpy.props.PointerProperty(name="Material Variation Label Category", type=CustoLabelCategoryEnumCollectionProperties)
	

	def draw(self, context):
		layout = self.layout
		
		ch_settings = context.scene.custo_handler_settings
		col = layout.column()
		layout.use_property_split = True
		layout.use_property_decorate = False
		col.prop(self, 'name', text='Name')

		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_asset_label_category.name', text=ch_settings.current_asset_label_category.name, label='Asset ID: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_mesh_slot_label_category.name', text=ch_settings.current_mesh_slot_label_category.name, label='Mesh Slots: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_material_slot_label_category.name', text=ch_settings.current_material_slot_label_category.name, label='Material Slot: ')
		draw_label_category_search(col, 'context.scene.custo_handler_settings.current_material_label_category.name', text=ch_settings.current_material_label_category.name, label='Material: ')
		draw_label_categories(col,'Mesh Variations:', 'Mesh Variation Count:', self, 'mesh_variation_label_category_count', 'mesh_variation_label_categories')
		draw_label_categories(col, 'Material Variations:','Material Variation Count:', self, 'material_variation_label_category_count', 'material_variation_label_categories')

	def invoke(self, context, event):
		wm = context.window_manager
		revert_asset_types_parameters(self)
		self.name = ''
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		ch_settings = context.scene.custo_handler_settings
		s = context.scene.custo_handler_settings.custo_asset_types.add()
		s.name = self.name

		s.asset_label_category.name = ch_settings.current_asset_label_category.name
			
		s.mesh_slot_label_category.name = ch_settings.current_mesh_slot_label_category.name
		
		for l in self.mesh_variation_label_categories.label_category_enums:
			asset_label = s.mesh_variation_label_categories.add()
			asset_label.name = l.name

		s.material_slot_label_category.name = ch_settings.current_material_slot_label_category.name
		s.material_label_category.name = ch_settings.current_material_label_category.name
		
		for l in self.material_variation_label_categories.label_category_enums:
			asset_label = s.material_variation_label_categories.add()
			asset_label.name = l.name
			
		revert_asset_types_parameters(self)
		return {'FINISHED'}

class UI_SearchAssetType(bpy.types.Operator):
	bl_idname = "scene.search_asset_type"
	bl_label = "Search Asset Type"
	bl_property = "enum"

	property_name : bpy.props.StringProperty(name='Property Name')
	enum: bpy.props.EnumProperty(name="Label", description="", items=asset_type_enum)

	def execute(self, context):
		command = f'{self.property_name} = "{self.enum}"'
		exec(command, {'context':context})
		return {'FINISHED'}

	def invoke(self, context, event):
		wm = context.window_manager
		wm.invoke_search_popup(self)
		return {'FINISHED'}


classes = ( UI_MoveAssetType, 
			UI_EditAssetType, 
			UI_ClearAssetTypes, 
			UI_AddAssetType,
			UI_RemoveAssetType,
			UI_SearchAssetType)

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