import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .node_attributes import LabelCombinaison
from .operators.properties.node_label_properties import NodeAssetLabelProperties

class AssetsFilterByLabelsNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Labels node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByLabelsNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Labels"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	labels: bpy.props.CollectionProperty(name="Labels", description="Labels", type=NodeAssetLabelProperties)
	labels_idx: bpy.props.IntProperty(name='Index', default=0, min=0)
	
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
		return "Filter Assets By Labels"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):		
		# filtering by label
		filtered = []
		assets = super().get_assets()
		
		# skip node if muted
		if self.mute:
			return assets
		
		ch_settings = bpy.context.scene.custo_handler_settings

		for a in assets:
			labels = LabelCombinaison()
			for label in self.labels:
				if not len(label.name):
					continue
				found=False
				for lc in ch_settings.custo_label_categories:
					for l in lc.labels:
						if label.name.lower() not in l.name.lower():
							continue
						
						labels.set_label(category=lc.name, name=label.name, value=not label.invert)
						found = True
						
				if not found:
					labels.set_invalid_label()
					
			if a.has_mesh_with_labels(variations=labels):
				a.attributes.add_labels(labels)
				filtered.append(a)

		return filtered

classes = (AssetsFilterByLabelsNode,)

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


