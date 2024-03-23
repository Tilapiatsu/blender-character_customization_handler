import bpy

class PT_CustomizationHandler:          
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	bl_category = 'Customization Handler'
	bl_options = {"DEFAULT_CLOSED"}
		

class PT_CustoSpawnSetup(PT_CustomizationHandler, bpy.types.Panel): 
	bl_label = "Customization Spawn Setup"
	bl_idname = 'SCENE_PT_Customization_Spawn_Setup'

	def draw(self, context):
		layout = self.layout
		ch_settings = context.scene.custo_handler_settings
		ob = context.object
		b = layout.box()
		b.use_property_split = True
		b.use_property_decorate = False
		
		b.label(text='Customization Spawning')
		b.prop(ch_settings, 'custo_spawn_tree')
		b.prop(ch_settings, 'custo_spawn_root')
		b.prop(ch_settings, 'custo_spawn_count')
		b.prop(ch_settings, 'custo_spawn_max_per_row')
		b.prop(ch_settings, 'exclude_incomplete_mesh_combinaison')
		b.operator('scene.customization_spawn', text='Spawn')


class PT_CustoPartSetup(bpy.types.Panel): 
	bl_space_type = 'PROPERTIES'
	bl_region_type = "WINDOW"
	bl_label = "Customization Part Setup"
	bl_idname = 'OBJECT_PT_Customization_Part_Setup'
	bl_context = 'object'

	def draw(self, context):
		layout = self.layout
		scn = context.scene
		ob = context.object
		
		row = layout.row(align=True)
		row.prop(ob, 'custo_part_layer', text='layer')

		b = layout.box()
		b.label(text='Slots Coverage')
		row = b.row()

		rows = 20 if len(ob.custo_part_slots) > 20 else len(ob.custo_part_slots) + 1
		row.template_list('OBJECT_UL_CustoPartSlots', '', ob, 'custo_part_slots', ob, 'custo_part_slots_idx', rows=rows)

		b = layout.box()
		b.label(text='Keep Lower Layers Slots')
		row = b.row()

		rows = 20 if len(ob.custo_part_keep_lower_slots) > 20 else len(ob.custo_part_keep_lower_slots) + 1
		row.template_list('OBJECT_UL_CustoPartSlots', '', ob, 'custo_part_keep_lower_slots', ob, 'custo_part_keep_lower_slots_idx', rows=rows)
		
		splited_row = layout.row()
		b = splited_row.box()
		b.label(text='Label Categories')
		row = b.row()

		rows = 20 if len(ob.custo_part_label_categories) > 20 else len(ob.custo_part_label_categories) + 1
		row.template_list('OBJECT_UL_CustoPartLabelCategories', '', ob, 'custo_part_label_categories', ob, 'custo_part_label_categories_idx', rows=rows)

		b = splited_row.box()
		b.label(text='Labels')
		row = b.row()

		rows = 20 if len(ob.custo_part_labels) > 20 else len(ob.custo_part_labels) + 1
		row.template_list('OBJECT_UL_CustoPartLabels', '', ob, 'custo_part_labels', ob, 'custo_part_labels_idx', rows=rows)


classes = (PT_CustoSpawnSetup,)

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