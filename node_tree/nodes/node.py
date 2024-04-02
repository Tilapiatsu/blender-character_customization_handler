import bpy
from ..sockets import node_socket_asset
from .node_const import SPAWN_COLOR, INVALID_COLOR
from ..node_const import TREE_NAME
from ...operators.properties.custo_label_properties import CustoLabelCategoryProperties


# Follow an input link through any reroutes
def follow_input_link(link):
	if link.from_node.type == 'REROUTE':
		if link.from_node.inputs[0].is_linked:
			try: # During link insertion this can have weird states
				return follow_input_link(link.from_node.inputs[0].links[0])
			except:
				pass
	return link


def update_values(self, context):
	self.update_color()

class CustomizationTreeNode:
	spawn : bpy.props.BoolProperty(name="Spawn", description="The Assets output of this tree will used dirring the spawning phase", default=False, update=update_values)
	asset_count : bpy.props.IntProperty(default=0)
	label_type = 'DEFAULT'
	_assets = []

	@property
	def category_name(self):
		return ''

	@property
	def spawned_assets(self):
		return [a for a in self.assets if a.spawn]
	
	@property
	def assets(self):
		self._assets = self.get_assets()
		self.update_asset_count()
		return self._assets
	
	@classmethod
	def poll(cls, ntree):
		return ntree.bl_idname == TREE_NAME
	
	@property
	def node_tree(self):
		ch_settings = bpy.context.scene.custo_handler_settings
		space = bpy.context.space_data
		node_tree = getattr(space, 'node_tree', None)

		if node_tree is None:
			if ch_settings.custo_spawn_tree is None:
				return None
			else:
				node_tree = ch_settings.custo_spawn_tree
				
		return node_tree
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self, socket_type=None, socket_name=None, sub_socket_dict=None, ui_list_callback=None):
		if socket_type is None:
			return
		idx = 0
		sub = 0
		if sub_socket_dict:
			sub = len(sub_socket_dict.keys())
		for socket in self.inputs:
			if socket.bl_idname != socket_type:
				idx = idx + 1
				continue
			if socket.is_linked or (hasattr(socket, 'value') and socket.value):
				if len(self.inputs) == idx + 1 + sub:
					self.inputs.new(socket_type, socket_name)
					if sub_socket_dict:
						for key in sub_socket_dict.keys():
							self.inputs.new(sub_socket_dict[key][0], key)
							self.inputs[len(self.inputs)-1].hide = sub_socket_dict[key][1]
					if ui_list_callback:
						ui_list_callback['add'](node_name=self.name)
			else:
				if len(self.inputs) > idx + 1 + sub:
					self.inputs.remove(socket)
					rem = idx
					idx = idx - 1
					if sub_socket_dict:
						for key in sub_socket_dict.keys():
							self.inputs.remove(self.inputs[rem])
							idx = idx - 1
					if ui_list_callback:
						ui_list_callback['remove'](node_name=self.name, index=idx + 1)
			idx = idx + 1

	# Update inputs and links on updates
	def update(self):
		self.update_color()
		self.update_inputs()
		# Update _assets variable
		self.assets
		# Links can get inserted without calling insert_link, but update is called.
		for socket in self.inputs:
			if socket.is_linked:
				self.insert_link(socket.links[0])

	def update_asset_count(self):
		self.asset_count = len(self._assets)

	# Validate incoming links
	def insert_link(self, link):
		if link.to_node == self:
			if follow_input_link(link).from_socket.bl_idname in link.to_socket.valid_inputs() and link.is_valid:
				link.to_socket.valid = True
			else:
				link.to_socket.valid = False
	
	def transfer_attributes(func):
		def transfer(self):
			print('transfering attributes')
			for input in self.inputs:
				input_node = follow_input_link(input.links[0]).from_node
				self.temp_labels += input_node.temp_labels
			return func(self)

		return transfer
	
	def get_assets(self):
		input_assets = []
		for input in self.inputs:
			if input.bl_idname != node_socket_asset.AssetsSocket.bl_idname:
				continue
			
			if not input.is_linked or not len(input.links):
				continue
			
			input_node = follow_input_link(input.links[0]).from_node
			if input_node.mute:
				return input_node.get_assets()
			
			if 'get_assets' not in dir(input_node):
				continue
			
			current_input_assets = input_node.get_assets()
			input_assets += current_input_assets
		
		return input_assets
	
	def print_assets(self):
		print(f'{len(self.assets)} asset(s) found')
		print('---------------------------------------')
		for a in self.assets:
			print(a.name)
			print(a.attributes)
		print('---------------------------------------')

	# Follows through reroutes
	def islinked(self):
		if self.is_input_linked and not self.is_output:
			try: # During link removal this can be in a weird state
				node = self.links[0].from_node
				while node.type == "REROUTE":
					if node.inputs[0].is_input_linked and node.inputs[0].links[0].is_valid:
						node = node.inputs[0].links[0].from_node
					else:
						return False
				return True
			except:
				pass
		return False
	
	def is_input_linked(self):
		linked = False

		for input in self.inputs:
			if input.bl_idname != node_socket_asset.AssetsSocket.bl_idname:
				continue

			if not input.is_linked or not len(input.links):
				continue

			linked = True
			break

		return linked
	
	def update_color(self):
		if self.spawn and self.is_input_linked():
			self.use_custom_color = True
			self.color = SPAWN_COLOR
		elif not self.is_input_linked():
			self.use_custom_color = True
			self.color = INVALID_COLOR
		else:
			self.use_custom_color = False
	
	def layout_header(self, layout, context, asset_count=True):
		layout.prop(self, 'spawn')
		row = layout.row(align = True)
		if asset_count:
			row.label(text=f'{self.asset_count} asset(s) found')
		else:
			row.label(text='')
		op = row.operator("node.print_asset_list", text='', icon='ALIGN_JUSTIFY')
		op.node_name = self.name
		layout.separator()

	def draw_labels(self, layout):
		row = layout.row(align=True)
		rows = 20 if len(self.labels) > 20 else len(self.labels) + 3
		row.template_list('NODE_UL_AssetLabelNode', '', self, 'labels', self, 'labels_idx', rows=rows)
		row.separator()
		col = row.column(align=True)
		col.operator('node.add_asset_label', text="", icon='ADD').node_name = self.name

		col.separator()
		d = col.operator("node.move_asset_label", text="", icon='TRIA_UP')
		d.node_name = self.name
		d.direction = "UP"

		d = col.operator("node.move_asset_label", text="", icon='TRIA_DOWN')
		d.node_name = self.name
		d.direction = "DOWN"

		col.separator()
		d = col.operator("node.clear_asset_labels", text="", icon='TRASH')
		d.node_name = self.name
		
	def draw_override(self, layout):
		row = layout.row(align=True)
		rows = 20 if len(self.properties) > 20 else len(self.properties) + 3
		row.template_list('NODE_UL_AssetOverrideNode', '', self, 'properties', self, 'properties_idx', rows=rows)
		row.separator()
		col = row.column(align=True)
		col.operator('node.add_asset_property', text="", icon='ADD').node_name = self.name

		col.separator()
		d = col.operator("node.move_asset_property", text="", icon='TRIA_UP')
		d.node_name = self.name
		d.direction = "UP"

		d = col.operator("node.move_asset_property", text="", icon='TRIA_DOWN')
		d.node_name = self.name
		d.direction = "DOWN"

		col.separator()
		d = col.operator("node.clear_asset_properties", text="", icon='TRASH')
		d.node_name = self.name