import bpy
from .properties.custo_scene_properties import update_label_category_definition

class UI_RefreshLabelDefinition(bpy.types.Operator):
	bl_idname = "object.refresh_label_definition"
	bl_label = "Refresh Part labels"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Refresh Part Labels from the Label Definition"

	def execute(self, context):
		if context.object is None:
			return {'FINISHED'}
		# print(f'refreshing {context.object.name} part slots')
		
		for lc in context.scene.custo_handler_settings.custo_label_categories:
			# print(s.name)
			if lc.name not in context.object.custo_label_category_definition:
				# print(f'adding {lc.name}')
				lcategory = context.object.custo_label_category_definition.add()
				lcategory.name = lc.name
				for l in lc.labels:
					# print(f'adding {l.name}')
					label = lcategory.labels.add()
					label.name = l.name
			else:
				olc = context.object.custo_label_category_definition[lc.name].labels
				for l in lc.labels:
					if l.name not in olc:
						# print(f'adding {l.name}')
						label = olc.add()
						label.name = l.name
		
		
		for i, lc in enumerate(context.object.custo_label_category_definition):
			if lc.name not in context.scene.custo_handler_settings.custo_label_categories:
				context.object.custo_label_category_definition.remove(i)
		
		self.reorder_label_category(context)

		update_label_category_definition(self, context)
		return {'FINISHED'}
	
	def reorder_label_category(self, context):
		source_label_categories = []
		for lc in context.scene.custo_handler_settings.custo_label_categories:
			source_label_categories.append(lc.name)
		
		target_label_categories = []
		for lc in context.object.custo_label_category_definition:
			target_label_categories.append(lc.name)
		
		# print(source_label_categories)
		# print(target_label_categories)

		for i, lc in enumerate(source_label_categories):
			if lc == target_label_categories[i]:
				continue
			
			# Get index of element to move
			src_index = target_label_categories.index(lc)
			target_label_categories.insert(i, target_label_categories.pop(src_index))

			# Move Element to the proper index
			# print(f'Moving "{lc}" from {src_index} to {i}')
			context.object.custo_label_category_definition.move(src_index, i)

	
classes = ( UI_RefreshLabelDefinition, 
			)

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