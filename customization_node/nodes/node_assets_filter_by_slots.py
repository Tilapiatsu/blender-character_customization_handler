import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .operators.properties.node_label_properties import NodeAssetLabelProperties
from ...operators.properties.custo_label_properties import CustoLabelCategoryProperties

class AssetsFilterBySlotsNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Mesh Slots node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByMeshSlotsNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Mesh Slots"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	labels: bpy.props.CollectionProperty(name="Slots", type=NodeAssetLabelProperties)
	labels_idx: bpy.props.IntProperty(name='Index', default=0, min=0)
	label_type = 'MESH_SLOT'
	
	@property
	def category_name(self):
		return 'mesh_slot_label_category'
	
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
		return "Filter Assets By Mesh Slots"
	
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

		for a in assets:
			valid_labels = []
			slots = [s.name for s in a.slots if s.value]
			for i, label in enumerate(self.labels):
				if not len(label.name):
					continue
				
				if label.name in slots and not label.invert or label.name not in slots and label.invert:
					valid_labels.append(label.name)
			
			valid_object = True
			for l in self.label_names:
				if not len(l):
					continue
				if l not in valid_labels:
					valid_object = False
					break
			if valid_object:
				filtered.append(a)

		return filtered


classes = (AssetsFilterBySlotsNode,)

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


