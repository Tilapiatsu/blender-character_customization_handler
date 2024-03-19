import bpy
from .node_operator import NodeOperator

class UI_MoveLabel(bpy.types.Operator, NodeOperator):
	bl_idname = "node.move_asset_label"
	bl_label = "Move Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Label up or down.\nThis controls the position in the List."

	node_name: bpy.props.StringProperty(name='Node Name', default='')
	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_labels)

	def execute(self, context):
		self.tree = context.space_data.node_tree
		idx, label, _ = self.labels

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(label) - 1)

		self.node.labels.move(idx, nextidx)
		self.node.labels_idx = nextidx

		return {'FINISHED'}


class UI_ClearLabels(bpy.types.Operator, NodeOperator):
	bl_idname = "node.clear_asset_labels"
	bl_label = "Clear All Labels"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Labels"

	node_name: bpy.props.StringProperty(name='Node Name', default='')

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_labels)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		self.tree = context.space_data.node_tree
		self.node.labels.clear()
		return {'FINISHED'}


class UI_RemoveLabel(bpy.types.Operator, NodeOperator):
	bl_idname = "node.remove_asset_label"
	bl_label = "Remove Selected Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected label"
	
	node_name: bpy.props.StringProperty(name='Node Name', default='')
	index : bpy.props.IntProperty(name="label index", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_labels
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		self.tree = context.space_data.node_tree
		_, labels, _ = self.labels

		labels.remove(self.index)

		self.node.labels_idx = min(self.index, len(self.node.labels) - 1)
		return {'FINISHED'}


class UI_DuplicateLabel(bpy.types.Operator, NodeOperator):
	bl_idname = "node.duplicate_asset_label"
	bl_label = "Duplicate Selected Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Label"
	
	node_name: bpy.props.StringProperty(name='Node Name', default='')
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_labels

	def execute(self, context):
		self.tree = context.space_data.node_tree
		_, label, _ = self.labels

		s = label.add()
		s.name = label[self.index].name+'_dup'
		label.move(len(label) - 1, self.index + 1)
		
		s = self.node.labels.add()
		s.name = label[self.index].name+'_dup'
		self.node.labels.move(len(label) - 1, self.index + 1)
		return {'FINISHED'}


class UI_AddLabel(bpy.types.Operator, NodeOperator):
	bl_idname = "node.add_asset_label"
	bl_label = "Add Label"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a label"

	node_name: bpy.props.StringProperty(name='Node Name', default='')
	name : bpy.props.StringProperty(name="Label Name", default="")

	def execute(self, context):
		self.tree = context.space_data.node_tree
		s = self.node.labels.add()
		s.name = self.name
		return {'FINISHED'}
	
classes = ( UI_MoveLabel, 
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