import bpy
from .properties.custo_label_properties import CustoLabelCategoryEnumProperties, CustoLabelCategoryEnumCollectionProperties

def get_asset_type(context):
	idx = context.scene.custo_asset_types_idx
	asset_types = context.scene.custo_asset_types

	active = asset_types[idx] if len(asset_types) else None

	return idx, asset_types, active

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
		row.prop(property_data[i], 'label_category_name', text='')
		# row.prop_search(property_data[i], 'label_category_pointer', source_data, source_name, text='')

	layout.separator()

class UI_MoveAssetType(bpy.types.Operator):
	bl_idname = "scene.move_customization_asset_type"
	bl_label = "Move Asset type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Asset_type up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_asset_types)

	def execute(self, context):
		idx, asset_type, _ = get_asset_type(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(asset_type) - 1)

		asset_type.move(idx, nextidx)
		context.scene.custo_asset_types_idx = nextidx

		return {'FINISHED'}


class UI_ClearAssetTypes(bpy.types.Operator):
	bl_idname = "scene.clear_customization_asset_types"
	bl_label = "Clear All Asset_types"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Asset types"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_asset_types)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_asset_types.clear()
		return {'FINISHED'}


class UI_RemoveAssetType(bpy.types.Operator):
	bl_idname = "scene.remove_customization_asset_type"
	bl_label = "Remove Selected Asset_type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected asset type"
	
	index : bpy.props.IntProperty(name="asset_type index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_asset_types
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, asset_types, _ = get_asset_type(context)

		asset_types.remove(self.index)

		context.scene.custo_asset_types_idx = min(self.index, len(context.scene.custo_asset_types) - 1)

		return {'FINISHED'}


class UI_DuplicateAssetType(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_asset_type"
	bl_label = "Duplicate Selected Asset_type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Asset type"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_asset_types

	def execute(self, context):
		_, asset_type, _ = get_asset_type(context)

		s = asset_type.add()
		s.name = asset_type[self.index].name+'_dup'
		asset_type.move(len(asset_type) - 1, self.index + 1)
		return {'FINISHED'}


class UI_EditAssetType(bpy.types.Operator):
	bl_idname = "scene.edit_customization_asset_type"
	bl_label = "Edit Asset_type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization asset type"

	index : bpy.props.IntProperty(name="Asset_type Index", default=0)
	name : bpy.props.StringProperty(name="Asset_type Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Asset_type Name')
	
	def invoke(self, context, event):
		current_asset_type = context.scene.custo_asset_types[self.index]
		self.name = current_asset_type.name
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)
	
	def execute(self, context):
		s = context.scene.custo_asset_types[self.index]
		s.name = self.name
		return {'FINISHED'}


class UI_AddAssetType(bpy.types.Operator):
	bl_idname = "scene.add_customization_asset_type"
	bl_label = "Add Asset Type"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization asset type"

	name : bpy.props.StringProperty(name="Asset Type Name", default="")
	asset_label_category_count : bpy.props.IntProperty(name="Asset Label Category Count", default=1, min=1)
	asset_label_categories : bpy.props.PointerProperty(name="Asset Label Categories", type=CustoLabelCategoryEnumCollectionProperties)
	mesh_variation_label_category_count : bpy.props.IntProperty(name="Mesh Variation Label Category Count", default=1, min=1)
	mesh_variation_label_categories : bpy.props.PointerProperty(name="Mesh Variation Label Categories", type=CustoLabelCategoryEnumCollectionProperties)
	material_label_category : bpy.props.PointerProperty(name="Material Label Category", type=CustoLabelCategoryEnumProperties)
	material_variation_label_category : bpy.props.PointerProperty(name="Material Variation Label Category", type=CustoLabelCategoryEnumProperties)
	
	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Name')

		draw_label_categories(col, 'Asset:', self, 'asset_label_category_count', 'asset_label_categories', context.scene, 'custo_label_categories')
		draw_label_categories(col, 'Mesh Variation:', self, 'mesh_variation_label_category_count', 'mesh_variation_label_categories', context.scene, 'custo_label_categories')
		col.prop(self.material_label_category, 'label_category_name', text='Material')
		col.prop(self.material_variation_label_category, 'label_category_name', text='Material Variation')

	def invoke(self, context, event):
		wm = context.window_manager
		self.name = ''
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_asset_types.add()
		s.name = self.name
		for l in self.asset_label_categories.label_category_enums:
			asset_label = s.asset_label_categories.add()
			asset_label.name = l.label_category_name
		
		for l in self.mesh_variation_label_categories.label_category_enums:
			asset_label = s.mesh_variation_label_categories.add()
			asset_label.name = l.label_category_name

		s.material_label_category.name = self.material_label_category.label_category_name
		s.material_variation_label_category.name = self.material_variation_label_category.label_category_name

		return {'FINISHED'}

classes = ( UI_MoveAssetType, 
			UI_EditAssetType, 
			UI_ClearAssetTypes, 
			UI_AddAssetType,
			UI_RemoveAssetType,
			UI_DuplicateAssetType)

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