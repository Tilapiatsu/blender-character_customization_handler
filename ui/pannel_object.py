import bpy

class PT_CustoLabelDefinitionSetup(bpy.types.Panel): 
	bl_space_type = 'PROPERTIES'
	bl_region_type = "WINDOW"
	bl_label = "Customization Label Definition Setup"
	bl_idname = 'OBJECT_PT_Customization_Label_Definition_Setup'
	bl_context = 'object'

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		ob = context.object
		
		main_row = layout.row()
		
		b = main_row.box()
		b.label(text='Label Categories')
		row = b.row()
		rows = 20 if len(scn.custo_label_categories) > 20 else len(scn.custo_label_categories) + 1
		row.template_list('OBJECT_UL_CustoLabelCategorieDefinition', '', ob, 'custo_label_category_definition', ob, 'custo_label_category_definition_idx', rows=rows)

		b = main_row.box()
		b.label(text='Labels')
		row = b.row()
		rows = 20 if len(scn.custo_labels) > 20 else len(scn.custo_labels) + 1
		row.template_list('OBJECT_UL_CustoLabelDefinition', '', ob, 'custo_label_definition', ob, 'custo_label_definition_idx', rows=rows)
		

classes = (PT_CustoLabelDefinitionSetup,)

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