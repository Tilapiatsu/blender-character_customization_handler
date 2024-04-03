import bpy
from .node_operator import NodeOperator

class UI_MoveProperty(bpy.types.Operator, NodeOperator):
	bl_idname = "node.move_asset_property"
	bl_label = "Move Property"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Move Property up or down.\nThis controls the position in the List."

	node_name: bpy.props.StringProperty(name='Node Name', default='')
	direction: bpy.props.EnumProperty(items=[("UP", "Up", ""), ("DOWN", "Down", "")])

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_labels)

	def execute(self, context):
		self.tree = context.space_data.node_tree
		idx, property, _ = self.props

		if self.direction == "UP":
			nextidx = max(idx - 1, 0)
		elif self.direction == "DOWN":
			nextidx = min(idx + 1, len(property) - 1)

		self.node.properties.move(idx, nextidx)
		self.node.properties_idx = nextidx

		return {'FINISHED'}


class UI_ClearProperty(bpy.types.Operator, NodeOperator):
	bl_idname = "node.clear_asset_properties"
	bl_label = "Clear All Properties"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Clear All Properties"

	node_name: bpy.props.StringProperty(name='Node Name', default='')

	@classmethod
	def poll(cls, context):
		return len(context.scene.custo_handler_settings.custo_labels)
	
	def invoke(self, context, event):
		wm = context.window_manager
		return wm.invoke_confirm(self, event)

	def execute(self, context):
		self.tree = context.space_data.node_tree
		self.node.properties.clear()
		return {'FINISHED'}


class UI_RemoveProperty(bpy.types.Operator, NodeOperator):
	bl_idname = "node.remove_asset_property"
	bl_label = "Remove Selected Properties"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Remove selected Properties"
	
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
		_, properties, _ = self.props

		properties.remove(self.index)

		self.node.properties_idx = min(self.index, len(self.node.properties) - 1)
		return {'FINISHED'}


class UI_DuplicateProperty(bpy.types.Operator, NodeOperator):
	bl_idname = "node.duplicate_asset_property"
	bl_label = "Duplicate Selected Propertiy"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Duplicate selected Propertiy"
	
	node_name: bpy.props.StringProperty(name='Node Name', default='')
	index : bpy.props.IntProperty(name="Operator ID", default=0)

	@classmethod
	def poll(cls, context):
		return context.scene.custo_handler_settings.custo_labels

	def execute(self, context):
		self.tree = context.space_data.node_tree
		_, properties, _ = self.props

		s = properties.add()
		s.name = properties[self.index].name+'_dup'
		properties.move(len(properties) - 1, self.index + 1)
		
		s = self.node.properties.add()
		s.name = properties[self.index].name+'_dup'
		self.node.labels.move(len(properties) - 1, self.index + 1)
		return {'FINISHED'}


class UI_AddProperty(bpy.types.Operator, NodeOperator):
	bl_idname = "node.add_asset_property"
	bl_label = "Add Property"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Add a label"

	node_name: bpy.props.StringProperty(name='Node Name', default='')
	name : bpy.props.StringProperty(name="Label Name", default='Property Name')

	def execute(self, context):
		self.tree = context.space_data.node_tree
		s = self.node.properties.add()
		s.name = self.name
		return {'FINISHED'}
	
classes = ( UI_MoveProperty, 
			UI_ClearProperty, 
			UI_AddProperty,
			UI_RemoveProperty,
			UI_DuplicateProperty)

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