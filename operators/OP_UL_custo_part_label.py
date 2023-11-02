import bpy


class UI_RefreshPartLabels(bpy.types.Operator):
	bl_idname = "object.refresh_part_labels"
	bl_label = "Refresh Part labels"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Refresh Part Labels From the Label Definition"

	def invoke(self, context, event):
		return context.object

	def execute(self, context):
		# print(f'refreshing {context.object.name} part slots')
		for lc in context.scene.custo_label_categories:
			# print(s.name)
			if lc.name not in context.object.custo_part_label_categories:
				print(f'adding {lc.name}')
				lcategory = context.object.custo_part_label_categories.add()
				lcategory.name = lc.name
				for l in lc.labels:
					print(f'adding {l.name}')
					label = lcategory.labels.add()
					label.name = l.name
			else:
				for l in lc.labels:
					if l.name not in context.object.custo_part_label_categories[lc.name]:
						print(f'adding {l.name}')
						label = lc.labels.add()
						label.name = l.name
		i = 0
		for lc in context.object.custo_part_label_categories:
			if lc.name not in context.scene.custo_label_categories:
				context.object.custo_part_label_categories.remove(i)
			i += 1
		return {'FINISHED'}