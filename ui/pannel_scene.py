import bpy

class PT_CustoLabelSetup(bpy.types.Panel): 
	bl_space_type = 'PROPERTIES'
	bl_region_type = "WINDOW"
	bl_label = "Customization Label Setup"
	bl_idname = 'SCENE_PT_Customization_Label_Setup'
	bl_context = 'scene'

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		ob = context.object
		
		main_row = layout.row()
		
		b = main_row.box()
		b.label(text='Label Categories')
		row = b.row()
		rows = 20 if len(scn.custo_handler_settings.custo_label_categories) > 20 else len(scn.custo_handler_settings.custo_label_categories) + 1
		row.template_list('SCENE_UL_CustoLabelCategories', '', scn.custo_handler_settings, 'custo_label_categories', scn.custo_handler_settings, 'custo_label_categories_idx', rows=rows)
		col = row.column(align=True)
		col.operator('scene.add_customization_label_category', text="", icon='ADD')

		col.separator()
		col.operator("scene.move_customization_label_category", text="", icon='TRIA_UP').direction = "UP"
		col.operator("scene.move_customization_label_category", text="", icon='TRIA_DOWN').direction = "DOWN"

		col.separator()
		col.operator("scene.clear_customization_label_categories", text="", icon='TRASH')
		

		b = main_row.box()
		b.label(text='Labels')
		row = b.row()
		rows = 20 if len(scn.custo_handler_settings.custo_labels) > 20 else len(scn.custo_handler_settings.custo_labels) + 1
		row.template_list('SCENE_UL_CustoLabels', '', scn.custo_handler_settings, 'custo_labels', scn.custo_handler_settings, 'custo_labels_idx', rows=rows)
		col = row.column(align=True)
		col.operator('scene.add_customization_label', text="", icon='ADD')

		col.separator()
		col.operator("scene.move_customization_label", text="", icon='TRIA_UP').direction = "UP"
		col.operator("scene.move_customization_label", text="", icon='TRIA_DOWN').direction = "DOWN"

		col.separator()
		col.operator("scene.clear_customization_labels", text="", icon='TRASH')

class PT_CustoAssetSetup(bpy.types.Panel): 
	bl_space_type = 'PROPERTIES'
	bl_region_type = "WINDOW"
	bl_label = "Customization Asset Setup"
	bl_idname = 'OBJECT_PT_Customization_Asset_Setup'
	bl_context = 'scene'

	def draw(self, context):
		layout = self.layout
		scn = context.scene

		b = layout.box()
		b.label(text='Asset Types')
		row = b.row()
		

		rows = 20 if len(scn.custo_handler_settings.custo_asset_types) > 20 else len(scn.custo_handler_settings.custo_asset_types) + 1
		row.template_list('SCENE_UL_CustoAssetTypes', '', scn.custo_handler_settings, 'custo_asset_types', scn.custo_handler_settings, 'custo_asset_types_idx', rows=rows)
		
		col = row.column(align=True)
		col.operator('scene.add_customization_asset_type', text="", icon='ADD')

		col.separator()
		col.operator("scene.move_customization_asset_type", text="", icon='TRIA_UP').direction = "UP"
		col.operator("scene.move_customization_asset_type", text="", icon='TRIA_DOWN').direction = "DOWN"

		col.separator()
		col.operator("scene.clear_customization_asset_types", text="", icon='TRASH')

		b = layout.box()
		b.label(text='Assets')
		row = b.row()

		rows = 20 if len(scn.custo_handler_settings.custo_assets) > 20 else len(scn.custo_handler_settings.custo_assets) + 1
		row.template_list('SCENE_UL_CustoAssets', '', scn.custo_handler_settings, 'custo_assets', scn.custo_handler_settings, 'custo_assets_idx', rows=rows)
		
		col = row.column(align=True)
		col.operator('scene.add_customization_asset', text="", icon='ADD')

		col.separator()
		col.operator("scene.move_customization_asset", text="", icon='TRIA_UP').direction = "UP"
		col.operator("scene.move_customization_asset", text="", icon='TRIA_DOWN').direction = "DOWN"

		col.separator()
		col.operator("scene.clear_customization_assets", text="", icon='TRASH')
		

classes = (PT_CustoLabelSetup,
		   PT_CustoAssetSetup)

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