import bpy

class NodeAssetOverrideProperties(bpy.types.PropertyGroup):
	target: bpy.props.EnumProperty(name='Override Targer', items=[('MATERIAL', 'Material', '')])
	type: bpy.props.EnumProperty(name='Type', items=[('FLOAT', 'Float', ''), ('INT', 'Int', ''), ('BOOL', 'Bool', ''), ('STRING', 'String', ''), ('COLOR', 'Color', ''), ('VECTOR', 'Vector', '')])
	slot: bpy.props.StringProperty(name='Slot', default='Slot')
	name: bpy.props.StringProperty(name='Name', default='Property Name')
	foat_value: bpy.props.FloatProperty(name='value', default=0.0)
	int_value: bpy.props.IntProperty(name='value', default=0)
	bool_value: bpy.props.BoolProperty(name='value', default=False)
	string_value: bpy.props.StringProperty(name='value', default='')
	color_value: bpy.props.FloatVectorProperty(name='value', default=[0.0,0.0,0.0], subtype='COLOR')
	vector_value: bpy.props.FloatVectorProperty(name='value', default=[0.0,0.0,0.0], subtype='XYZ')
	weight : bpy.props.FloatProperty(default=1.0, min=0)

class UL_AssetOverrideNode(bpy.types.UIList):
	bl_idname = "NODE_UL_AssetOverrideNode"

	def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
		ch_settings = context.scene.custo_handler_settings
		row = layout.row(align=True)
		row.prop(item, 'target', text='')
		row.prop_search(item, "slot", ch_settings.custo_asset_types[data.node_tree.asset_type].material_slot_label_category.label_category, "labels", text='')
		row.prop(item, 'type', text='')
		row.prop(item, 'name', text='')
		if item.type == 'FLOAT':
			row.prop(item, 'foat_value', text='')
		if item.type == 'INT':
			row.prop(item, 'int_value', text='')
		if item.type == 'BOOL':
			row.prop(item, 'bool_value', text='')
		if item.type == 'STRING':
			row.prop(item, 'string_value', text='')
		if item.type == 'COLOR':
			row.prop(item, 'color_value', text='')
		if item.type == 'VECTOR':
			row.prop(item, 'vector_value', text='')
		row.separator()
		row.alignment = 'EXPAND'
		row.prop(item, "weight", text='w')
		row = layout.row(align=True)
		row.alignment = 'RIGHT'
		o = row.operator('node.remove_asset_property', text='', icon='X')
		o.index = index
		o.node_name = data.name

classes = (NodeAssetOverrideProperties,
		   UL_AssetOverrideNode)

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