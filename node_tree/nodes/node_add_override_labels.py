import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .operators.properties.node_label_properties import NodeAssetLabelProperties

class AddOverrideLabelsNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Add/Override Labels node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AddOverrideLabelNodeType'
	# Label for nice name display
	bl_label = "Add/Override Labels"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	labels: bpy.props.CollectionProperty(name="Labels", description="Labels", type=NodeAssetLabelProperties)
	labels_idx: bpy.props.IntProperty(name='Index', default=0, min=0)
	
	@property
	def category_name(self):
		return 'other_label_category'
	
	@property
	def label_names(self):
		return [l.name for l in self.labels]

	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
		self.outputs.new('AssetsSocketType', "Assets")
		self.labels.add()

	# Copy function to initialize a copied node from an existing one.
	def copy(self, node):
		print("Copying from node ", node)

	# Free function to clean up on removal.
	def free(self):
		print("Removing node ", self, ", Goodbye!")

	# Additional buttons displayed on the node.
	def draw_buttons(self, context, layout):
		self.layout_header(layout, context)
		self.draw_labels(layout)

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Add/Override Labels node"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):		
		assets = super().get_assets()
		
		# skip node if muted
		if self.mute:
			return assets
		
		ch_settings = bpy.context.scene.custo_handler_settings

		for a in assets:

			for label in self.labels:
				if not len(label.name):
					continue
				
				a.attributes.add_label(category=label.label_category, name=label.name, value= not label.invert, weight=label.weight)

		return assets

classes = (AddOverrideLabelsNode,)

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


