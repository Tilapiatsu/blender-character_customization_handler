import bpy

class SpawnCustomizationTree(bpy.types.Operator):
	bl_idname = "scene.customization_spawn"
	bl_label = "Spawn Customization Tree"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Spawn Objects Using Customization Tree"


	@property
	def assets(self):
		if self._assets is None:
			self._assets = []
			for node in self.spawn_tree.nodes:
				self._assets += [a for a in node.assets if node.spawn and a not in self._assets]
		
		return self._assets
	
	@property
	def nodes(self):
		if self._nodes is None:
			self._nodes = [node for node in self.spawn_tree.nodes if node.spawn]
		
		return self._nodes

	@classmethod
	def poll(cls, context):
		return context.scene.custo_spawn_root is not None and context.scene.custo_spawn_tree is not None and context.scene.custo_spawn_count
    
	def init(self, context):
		self._assets = None
		self._nodes = None
		self.spawn_root = context.scene.custo_spawn_root
		self.spawn_tree = context.scene.custo_spawn_tree
		self.spawn_count = context.scene.custo_spawn_count

	def execute(self, context):
		self.init(context)

		for node in self.nodes:
			node.print_assets()
		
		for i in range(self.spawn_count):
			collection = self.create_spawn_collection()
			self.spawn_assets(collection)
		
		return {'FINISHED'}
	
	def create_spawn_collection(self):
		pass

	def spawn_assets(self, collection):
		for a in self.assets:
			print(a.custo_part_layer)



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