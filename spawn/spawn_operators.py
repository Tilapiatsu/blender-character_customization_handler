import bpy

class SpawnCustomizationTree(bpy.types.Operator):
	bl_idname = "scene.customization_spawn"
	bl_label = "Spawn Customization Tree"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Spawn Objects Using Customization Tree"

	@classmethod
	def poll(cls, context):
		return context.scene.custo_spawn_root is not None and context.scene.custo_spawn_tree is not None and context.scene.custo_spawn_count

	def execute(self, context):
		self.spawn_root = context.scene.custo_spawn_root
		self.spawn_tree = context.scene.custo_spawn_tree
		self.spawn_count = context.scene.custo_spawn_count

		for node in self.spawn_tree.nodes:
			if node.spawn:
				node.print_assets()

		return {'FINISHED'}

classes = ( SpawnCustomizationTree,
			)


def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)
	
	bpy.types.Scene.custo_spawn_tree = bpy.props.PointerProperty(name='Customization Tree', type=bpy.types.NodeTree)
	bpy.types.Scene.custo_spawn_root = bpy.props.PointerProperty(name='Root', type=bpy.types.Object)
	bpy.types.Scene.custo_spawn_count = bpy.props.IntProperty(name='Spawn Count', default=1)


def unregister():
	del bpy.types.Scene.custo_spawn_count
	del bpy.types.Scene.custo_spawn_root
	del bpy.types.Scene.custo_spawn_tree

	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()