import bpy
from bpy.types import Node
from .node import CustomizationTreeNode

class AssetsFilterByLabelNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Assets Filter By Label node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'AssetsFilterByLabelNodeType'
	# Label for nice name display
	bl_label = "Filter Assets By Label"
	# Icon identifier
	bl_icon = 'NODETREE'
	
	label: bpy.props.StringProperty(name="Label", description="Label", default="")
	invert: bpy.props.BoolProperty(name="Not", description="Invert rule", default=False)
	label_count: bpy.props.IntProperty(name="Label Count", description="Number of label to input", default=1, min=1)

	@property
	def assets(self):
		return self.get_assets()

	def init(self, context):
		self.inputs.new('AssetsSocketType', "Assets")
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
		layout.prop(self, 'label_count')
		row = layout.row(align=True)
		row.alignment = 'LEFT'
		row.prop(self, "invert")
		row.alignment = 'EXPAND'
		row.prop(self, "label", text='')
		
	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Filter Assets By Label"
	
	# Makes sure there is always one empty input socket at the bottom by adding and removing sockets
	def update_inputs(self):
		pass
	
	def get_assets(self):		
		# filtering by label
		filtered = []
		assets = super().get_assets()

		if not len(self.label):
			if self.invert:
				return assets
			else:
				return []
		
		for o in assets:
			for lc in o.custo_part_label_categories:
				for l in lc.labels:
					if self.label not in l.name:
						continue
					if l.checked and not self.invert or not l.checked and self.invert:
						filtered.append(o)

		return filtered

classes = (AssetsFilterByLabelNode,)

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


