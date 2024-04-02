import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .node_attributes import LabelVariation, LabelCombinaison
from .operators.properties.node_label_properties import NodeAssetLabelProperties

class AssetsFilterByNameNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Name node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByNameNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Name"
	# Icon identifier
	bl_icon = 'NODETREE'
	bl_width_default = 400
	
	labels: bpy.props.CollectionProperty(name="Labels", description="Labels", type=NodeAssetLabelProperties)
	labels_idx: bpy.props.IntProperty(name='Index', default=0, min=0)
	
	@property
	def category_name(self):
		return 'asset_label_category'

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
		return "Filter Assets By Name"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):	
		filtered = []	

		assets = super().get_assets()
		
		# skip node if muted
		if self.mute or not len(self.labels):
			return assets
		
		for a in assets:
			for label in self.labels:
				if not len(label.name):
					continue
				
				if a not in filtered and ( label.weight and ((a.name == label.name and not label.invert) or (a.name != label.name and label.invert))):
					filtered.append(a)

		return filtered

classes = (AssetsFilterByNameNode,)

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


