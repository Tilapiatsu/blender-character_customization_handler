import bpy
from .custo_label_properties import CustoLabelPropertiesPointer, CustoLabelEnumProperties, CustoPartLabelCategoryProperties
from .custo_slot_properties import CustoPartSlotsProperties

class CustoAssetTypePointer(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type', default='')
	
	@property
	def asset_type(self):
		return bpy.context.scene.custo_asset_types[self.name]

def asset_type_enum(self, context):
	items = [(l.name, l.name, '') for l in context.scene.custo_asset_types]
	return items

def get_asset_name(asset_ids):
	def joined(strings):
		result = ''
		i = 0
		for s in strings:
			if i < len(strings)-1:
				s += '_'
			result += s
			i += 1
		return result
	labels = [l.label.name for l in asset_ids]
	return joined(labels)

def update_current_asset_properties(self, context):
	asset_names = [a.asset_name for a in context.scene.custo_assets]
	# update Asset ID
	context.scene.current_asset_id.clear()
	for i, lc in enumerate(context.scene.custo_asset_types[self.name].asset_label_categories):
		id_enum = context.scene.current_asset_id.add()
		id_enum.label_category_name = lc.name
		
		if context.scene.current_asset_name in asset_names:
			id_enum.name = context.scene.custo_assets[context.scene.current_asset_name].asset_id[i].name

	# Update Slots
	context.scene.current_edited_asset_slots.clear()
	for s in context.scene.current_label_category[context.scene.custo_asset_types[self.name].slot_label_category.name].labels:
		slot = context.scene.current_edited_asset_slots.add()
		slot.name = s.name
		slot.checked = s.checked
		slot.keep_lower_layer_slot = s.keep_lower_layer_slot

class CustoAssetTypeEnumProperties(bpy.types.PropertyGroup):
	name : bpy.props.EnumProperty(name="Asset Type", items=asset_type_enum, update=update_current_asset_properties)

class CustoAssetLabelCategoryPointer(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Category Name', default='')
	
	@property
	def label_category(self):
		return bpy.context.scene.custo_label_categories[self.name]

class CustoAssetTypeProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type', default='')
	asset_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	slot_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	mesh_variation_label_categories : bpy.props.CollectionProperty(type=CustoAssetLabelCategoryPointer)
	material_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	material_variation_label_category : bpy.props.PointerProperty(type=CustoAssetLabelCategoryPointer)
	
class CustoAssetProperties(bpy.types.PropertyGroup):
	asset_type : bpy.props.PointerProperty(type=CustoAssetTypePointer)
	asset_id : bpy.props.CollectionProperty(type=CustoLabelPropertiesPointer)
	layer : bpy.props.IntProperty(name='Layer', default=0)
	slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
	
	@property
	def asset_name(self):
		return get_asset_name(self.asset_id)

class UL_CustoAssetType(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssetTypes"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_asset_type', text='', icon='GREASEPENCIL').index = index
		# row.operator('scene.duplicate_customization_asset_type', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_asset_type', text='', icon='X').index = index

class UL_CustoAsset(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssets"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.asset_name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_asset', text='', icon='GREASEPENCIL').index = index
		# row.operator('scene.duplicate_customization_asset', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_asset', text='', icon='X').index = index

classes = ( CustoAssetLabelCategoryPointer,
			CustoAssetTypeProperties,
			CustoAssetTypeEnumProperties,
			CustoAssetTypePointer,
			CustoAssetProperties,
			UL_CustoAssetType,
			UL_CustoAsset)

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	
	bpy.types.Scene.custo_asset_types = bpy.props.CollectionProperty(type=CustoAssetTypeProperties)
	bpy.types.Scene.custo_asset_types_idx = bpy.props.IntProperty(default=0)
	bpy.types.Scene.custo_assets = bpy.props.CollectionProperty(type=CustoAssetProperties)
	bpy.types.Scene.custo_assets_idx = bpy.props.IntProperty(default=0, min=0)
	bpy.types.Scene.current_asset_id = bpy.props.CollectionProperty(type=CustoLabelEnumProperties)
	bpy.types.Scene.current_asset_id_idx = bpy.props.IntProperty(default=0, min=0)
	bpy.types.Scene.current_asset_name = bpy.props.StringProperty()
	bpy.types.Scene.current_label_category = bpy.props.CollectionProperty(type=CustoPartLabelCategoryProperties)

def unregister():
	del bpy.types.Scene.current_label_category
	del bpy.types.Scene.current_asset_name
	del bpy.types.Scene.current_asset_id
	del bpy.types.Scene.current_asset_id_idx
	del bpy.types.Scene.custo_assets
	del bpy.types.Scene.custo_assets_idx
	del bpy.types.Scene.custo_asset_types
	del bpy.types.Scene.custo_asset_types_idx
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()