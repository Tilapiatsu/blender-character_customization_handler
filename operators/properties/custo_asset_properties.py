import bpy
from .custo_label_properties import CustoLabelCategoryProperties
from .custo_slot_properties import CustoPartSlotsProperties

class CustoAssetTypeProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Type', default='')
	asset_label_categories : bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
	mesh_variation_label_categories : bpy.props.CollectionProperty(type=CustoLabelCategoryProperties)
	material_label_category : bpy.props.PointerProperty(type=CustoLabelCategoryProperties)
	material_variation_label_category : bpy.props.PointerProperty(type=CustoLabelCategoryProperties)
	
class CustoAssetProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Asset Name', default='')
	asset_type : bpy.props.PointerProperty(type=CustoAssetTypeProperties)
	layer : bpy.props.IntProperty(name='Layer', default=0)
	slots : bpy.props.CollectionProperty(type=CustoPartSlotsProperties)

class UL_CustoAssetType(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssetTypes"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_asset_type', text='', icon='GREASEPENCIL').index = index
		row.operator('scene.duplicate_customization_asset_type', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_asset_type', text='', icon='X').index = index

class UL_CustoAsset(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoAssets"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
        

classes = ( CustoAssetTypeProperties,
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
	bpy.types.Scene.custo_assets_idx = bpy.props.IntProperty(default=0)

def unregister():
	del bpy.types.Scene.custo_assets
	del bpy.types.Scene.custo_assets_idx
	del bpy.types.Scene.custo_asset_types
	del bpy.types.Scene.custo_asset_types_idx
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()