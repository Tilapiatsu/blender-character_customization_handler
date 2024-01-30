import bpy

def update_keep_lower_part_slots(self, context):
	for s in context.object.custo_part_slots:
		# print(s.name)
		if s.name not in context.object.custo_part_keep_lower_slots:
			if s.checked:
				print(f'adding {s.name}')
				oslot = context.object.custo_part_keep_lower_slots.add()
				oslot.name = s.name

	i = 0
	for s in context.object.custo_part_keep_lower_slots:
		if s.name not in context.object.custo_part_slots:
			context.object.custo_part_keep_lower_slots.remove(i)
		else:
			if not context.object.custo_part_slots[s.name].checked:
				context.object.custo_part_keep_lower_slots.remove(i)
		i += 1

class CustoSlotProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Slot Name', default='')
	
class CustoPartSlotsProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Slot Name', default='')
	checked : bpy.props.BoolProperty(default=False, update=update_keep_lower_part_slots)
	
class CustoPartSlotsKeepLowerLayerProperties(bpy.types.PropertyGroup):
	name : bpy.props.StringProperty(name='Slot Name', default='')
	checked : bpy.props.BoolProperty(default=False)
	
class UL_CustoSlot(bpy.types.UIList):
	bl_idname = "SCENE_UL_CustoSlots"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.label(text=f'{item.name}')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		row.operator('scene.edit_customization_slot', text='', icon='GREASEPENCIL').index = index
		row.operator('scene.duplicate_customization_slot', text='', icon='COPYDOWN').index = index
		row.operator('scene.remove_customization_slot', text='', icon='X').index = index
	
class UL_CustoPartSlots(bpy.types.UIList):
	bl_idname = "OBJECT_UL_CustoPartSlots"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(item, 'checked', text='')
		row.separator()
		row.label(text=f'{item.name}')
		# row.operator('scene.lm_remove_texture_channel', text='', icon='X').index = index


classes = ( CustoSlotProperties,
            CustoPartSlotsProperties, 
            CustoPartSlotsKeepLowerLayerProperties, 
            UL_CustoSlot,
            UL_CustoPartSlots)

def register():
	
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
	
    bpy.types.Scene.custo_slots = bpy.props.CollectionProperty(type=CustoSlotProperties)
    bpy.types.Scene.custo_slots_idx = bpy.props.IntProperty(default=0)
    
    # TODO : Need to find the proper place to store Layers and slots for Asset. This info should stored per Assets,
	# but Assets are dynamically composed using Label Categories which can't be stored properly
    bpy.types.Object.custo_part_layer = bpy.props.IntProperty(default=0, min=0)
    bpy.types.Object.custo_part_slots = bpy.props.CollectionProperty(type=CustoPartSlotsProperties)
    bpy.types.Object.custo_part_slots_idx = bpy.props.IntProperty(default=0)
    bpy.types.Object.custo_part_keep_lower_slots = bpy.props.CollectionProperty(type=CustoPartSlotsKeepLowerLayerProperties)
    bpy.types.Object.custo_part_keep_lower_slots_idx = bpy.props.IntProperty(default=0)
	

def unregister():
    del bpy.types.Scene.custo_slots
    del bpy.types.Scene.custo_slots_idx

    del bpy.types.Object.custo_part_layer
    del bpy.types.Object.custo_part_slots
    del bpy.types.Object.custo_part_slots_idx
    del bpy.types.Object.custo_part_keep_lower_slots
    del bpy.types.Object.custo_part_keep_lower_slots_idx
	
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)	

if __name__ == "__main__":
    register()