import bpy
	
class UI_RefreshPartSlots(bpy.types.Operator):
	bl_idname = "object.refresh_part_slots"
	bl_label = "Refresh Part Slots"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Refresh Part Slots From the Slots Definition"

	@classmethod
	def poll(cls, context):
		return context.object is not None

	def execute(self, context):
		# print(f'refreshing {context.object.name} part slots')
		for s in context.scene.custo_slots:
			# print(s.name)
			if s.name not in context.object.custo_part_slots:
				print(f'adding {s.name}')
				oslot = context.object.custo_part_slots.add()
				oslot.name = s.name
		i = 0
		for s in context.object.custo_part_slots:
			if s.name not in context.scene.custo_slots:
				context.object.custo_part_slots.remove(i)
			i += 1
		return {'FINISHED'}