import bpy
from ..settings.custo_handler_settings import update_label_category_definition

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
				self.add_label_category(context.object.custo_label_category_definition, lc)
			else:
				self.edit_label_category(context.object.custo_label_category_definition, lc)
			
			if not context.object.active_material:
				continue
			for m in context.object.data.materials:
				if lc.name not in m.custo_label_category_definition:
					self.add_label_category(m.custo_label_category_definition, lc)
				else:
					self.edit_label_category(m.custo_label_category_definition, lc)
		
		self.clean_label_category(context.object.custo_label_category_definition)
		if context.object.active_material:
			for m in context.object.data.materials:
				self.clean_label_category(context.object.active_material.custo_label_category_definition)
		
		self.reorder_label_category(context, context.object.custo_label_category_definition)
		if context.object.active_material:
			for m in context.object.data.materials:
				self.reorder_label_category(context, context.object.active_material.custo_label_category_definition)

		update_label_category_definition(self, context)
		return {'FINISHED'}
	
	def add_label_category(self, prop, label_category):
		# print(f'adding {lc.name}')
		lcategory = prop.add()
		lcategory.name = label_category.name
		for l in label_category.labels:
			# print(f'adding {l.name}')
			label = lcategory.labels.add()
			label.name = l.name

	def edit_label_category(self, prop, label_category):
		olc = prop[label_category.name].labels
		for l in label_category.labels:
			if l.name not in olc:
				# print(f'adding {l.name}')
				label = olc.add()
				label.name = l.name

	def clean_label_category(self, prop):
		for i, lc in enumerate(prop):
			if lc.name not in prop:
				prop.remove(i)
			if lc.name not in bpy.context.scene.custo_handler_settings.custo_label_categories:
				prop.remove(i)
	
	def reorder_label_category(self, context, prop):
		source_label_categories = []
		for lc in context.scene.custo_handler_settings.custo_label_categories:
			source_label_categories.append(lc.name)
		
		target_label_categories = []
		for lc in prop:
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
			prop.move(src_index, i)

	
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