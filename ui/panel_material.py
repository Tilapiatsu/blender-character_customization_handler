import bpy

class PT_MATERIAL_CustoLabelDefinitionSetup(bpy.types.Panel): 
	bl_space_type = 'PROPERTIES'
	bl_region_type = "WINDOW"
	bl_label = "Customization Label Definition Setup"
	bl_idname = 'MATERIAL_PT_Customization_Label_Definition_Setup'
	bl_context = 'material'

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		mat = context.object.active_material
		lc_idx = scn.custo_handler_settings.custo_label_category_definition_idx
		if mat is None:
			return
		
		main_row = layout.row()
		
		b = main_row.box()
		b.label(text='Label Categories')
		row = b.row()
		rows = 20 if len(scn.custo_handler_settings.custo_label_categories) > 20 else len(scn.custo_handler_settings.custo_label_categories) + 1
		row.template_list('OBJECT_UL_CustoLabelCategorieDefinition', '', mat, 'custo_label_category_definition', scn.custo_handler_settings, 'custo_label_category_definition_idx', rows=rows)

		b = main_row.box()
		b.label(text='Labels')
		row = b.row()
		rows = 20 if len(scn.custo_handler_settings.custo_label_categories[lc_idx].labels) > 20 else len(scn.custo_handler_settings.custo_label_categories[lc_idx].labels) + 1
		row.template_list('OBJECT_UL_CustoLabelDefinition', '', mat.custo_label_category_definition[lc_idx], 'labels', mat, 'custo_label_definition_idx', rows=rows)
		

classes = (PT_MATERIAL_CustoLabelDefinitionSetup,)

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