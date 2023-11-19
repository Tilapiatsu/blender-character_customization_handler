import bpy
from bpy.types import Node
from .node import CustomizationTreeNode


class AssetsSelectorNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Selector node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsSelectorNodeType'
	# Label for nice name display
	bl_label = "Asset Selector"
	# Icon identifier
	bl_icon = 'NODETREE'

	subsockets = {'Spawn Rate': 'PercentageSocketType'}

	@property
	def assets(self):
		return self.get_assets()
	
	@property
	def label_names(self):
		return [l.name for l in self.labels]

	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
		for name,socket in self.subsockets.items():
			self.inputs.new(socket, name)
		self.outputs.new('AssetsSocketType', "Assets")

	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		self.layout_asset_count(layout, context)
		# self.draw_labels(layout)
	
	def draw_labels(self, layout):
		row = layout.row(align=True)
		rows = 20 if len(self.labels) > 20 else len(self.labels) + 3
		row.template_list('NODE_UL_AssetLabelNode', '', self, 'labels', self, 'labels_idx', rows=rows)
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

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Asset Selector"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		CustomizationTreeNode.update_inputs(self, 'AssetsSocketType', "Assets", self.subsockets)
	
	def get_assets(self):
		# filtering by label
		filtered = []
		assets = super().get_assets()

		filtered = assets
		# for o in assets:
		# 	valid_labels = []
		# 	for i, label in enumerate(self.labels):
		# 		for lc in o.custo_part_label_categories:
		# 			for l in lc.labels:
		# 				if label.name.lower() not in l.name.lower():
		# 					continue
		# 				if l.checked and not label.invert or not l.checked and label.invert:
		# 					valid_labels.append(label.name)
			
		# 	valid_object = True
		# 	for l in self.label_names:
		# 		if l not in valid_labels:
		# 			valid_object = False
		# 			break
		# 	if valid_object:
		# 		filtered.append(o)

		return filtered

classes = ( AssetsSelectorNode,)

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