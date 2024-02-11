import bpy
from .properties.custo_asset_properties import get_asset_name

def get_label(context):
	idx = context.scene.custo_labels_idx
	labels = context.scene.custo_labels

	active = labels[idx] if len(labels) else None

	return idx, labels, active


class UI_MoveLabel(bpy.types.Operator):
	bl_idname = "scene.move_customization_label"
	bl_label = "Move Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Label up or down.\nThis controls the position in the List."

	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_labels)

	def execute(self, context):
		idx, label, _ = get_label(context)

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(label) - 1)

		label.move(idx, nextidx)
		context.scene.custo_labels_idx = nextidx

		context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.move(idx, nextidx)
		bpy.ops.object.refresh_part_labels()
		return {'FINISHED'}


class UI_ClearLabels(bpy.types.Operator):
	bl_idname = "scene.clear_customization_labels"
	bl_label = "Clear All Labels"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Labels"

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_labels)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		context.scene.custo_labels.clear()
		context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.clear()
		bpy.ops.object.refresh_part_labels()
		return {'FINISHED'}


class UI_RemoveLabel(bpy.types.Operator):
	bl_idname = "scene.remove_customization_label"
	bl_label = "Remove Selected Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected label"
	
	index : bpy.props.IntProperty(name="label index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_labels
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		_, labels, _ = get_label(context)

		labels.remove(self.index)

		context.scene.custo_labels_idx = min(self.index, len(context.scene.custo_labels) - 1)

		context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.remove(self.index)
		bpy.ops.object.refresh_part_labels()
		return {'FINISHED'}


class UI_DuplicateLabel(bpy.types.Operator):
	bl_idname = "scene.duplicate_customization_label"
	bl_label = "Duplicate Selected Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Label"
	
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_labels

	def execute(self, context):
		_, label, _ = get_label(context)

		s = label.add()
		s.name = label[self.index].name+'_dup'
		label.move(len(label) - 1, self.index + 1)
		
		s = context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.add()
		s.name = label[self.index].name+'_dup'
		context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.move(len(label) - 1, self.index + 1)
		bpy.ops.object.refresh_part_labels()
		return {'FINISHED'}


class UI_EditLabel(bpy.types.Operator):
	bl_idname = "scene.edit_customization_label"
	bl_label = "Edit Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Edit current customization label"

	index : bpy.props.IntProperty(name="Label Index", default=0)
	name : bpy.props.StringProperty(name="Label Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='Label Name')
	
	def invoke(self, context, event):
		current_label = context.scene.custo_labels[self.index]
		self.name = current_label.name
		self.old_name = current_label.name
		wm = context.window_manager
		return wm.invoke_props_dialog(self, width=500)
	
	def execute(self, context):
		s = context.scene.custo_labels[self.index]
		s.name = self.name
		s = context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels[self.index]
		s.name = self.name
		self.label_category_name = context.scene.custo_label_categories[context.scene.custo_label_categories_idx].name
		bpy.ops.object.refresh_part_labels()
		self.refresh_asset_label_categories(context)
		return {'FINISHED'}

	def refresh_asset_label_categories(self, context):
		for asset_type in context.scene.custo_asset_types:
			for lc in asset_type.asset_label_categories:
				if lc.name != self.label_category_name:
					continue
				for l in lc.label_category.labels:
					if l.name == self.old_name:
						l.name = self.name

			for lc in asset_type.mesh_variation_label_categories:
				if lc.name != self.label_category_name:
					continue
				for l in lc.label_category.labels:
					if l.name == self.old_name:
						l.name = self.name
			
			for l in asset_type.slot_label_category.label_category.labels:
				if l.name == self.old_name:
					l.name = self.name

			for l in asset_type.material_label_category.label_category.labels:
				if l.name == self.old_name:
					l.name = self.name
			
			for l in asset_type.material_variation_label_category.label_category.labels:
				if l.name == self.old_name:
					l.name = self.name

		for asset in context.scene.custo_assets:
			for asset_id in asset.asset_id:
				if asset_id.name == self.old_name:
					asset_id.name = self.name
					asset_id.label_category_name = self.label_category_name

			for slot in asset.slots:
				if slot.name == self.old_name:
					slot.name = self.name
			
			asset.name = get_asset_name(asset.asset_id)

class UI_AddLabel(bpy.types.Operator):
	bl_idname = "scene.add_customization_label"
	bl_label = "Add Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a customization label"

	name : bpy.props.StringProperty(name="Label Name", default="")

	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.prop(self, 'name', text='name')

	def invoke(self, context, event):
		wm = context.window_manager
		self.name = ''
		return wm.invoke_props_dialog(self, width=500)

	def execute(self, context):
		s = context.scene.custo_labels.add()
		s.name = self.name
		s = context.scene.custo_label_categories[context.scene.custo_label_categories_idx].labels.add()
		s.name = self.name
		bpy.ops.object.refresh_part_labels()
		return {'FINISHED'}
	
classes = ( UI_MoveLabel, 
			UI_EditLabel, 
			UI_ClearLabels, 
			UI_AddLabel,
			UI_RemoveLabel,
			UI_DuplicateLabel)

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