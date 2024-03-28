import bpy
from bpy.types import Node
from .node import CustomizationTreeNode
from .node_attributes import LabelCombinaison
from .operators.properties.node_label_properties import NodeAssetLabelProperties

class MaterialsFilterByLabelsNode(CustomizationTreeNode, Node):
	# === Basics ===
	# Description string
	'''Materials Filter By Labels node'''
	# Optional identifier string. If not explicitly defined, the python class name is used.
	bl_idname = 'MaterialsFilterByLabelsNodeType'
	# Label for nice name display
	bl_label = "Filter Materials By Labels"
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

	# Explicit user label overrides this, but here we can define a label dynamically
	def draw_label(self):
		return "Filter Materials By Labels"
	
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
			label_categories = [a.asset.asset_type.asset_type.material_label_category.name] + [lc.name for lc in a.asset.asset_type.asset_type.material_variation_label_categories]
			for label in self.labels:
				if not len(label.name):
					continue
				for lc in label_categories:
					if label.name not in ch_settings.custo_label_categories[lc].labels:
						continue
					a.attributes.add_label(category=lc, name=label.name, value= not label.invert)

		return assets

classes = (MaterialsFilterByLabelsNode,)

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


