import bpy
import random
from .spawn_const import SPAWN_COLLECTION

class AssetsPerSlot:
	def __init__(self):
		pass

class SpawnCustomizationTree(bpy.types.Operator):
	bl_idname = "scene.customization_spawn"
	bl_label = "Spawn Customization Tree"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Spawn Objects Using Customization Tree"


	@property
	def assets(self) -> list:
		'''
		Returns a list of all assets that can be spawned
		'''
		if self._assets is None:
			self._assets = []
			for node in self.spawn_tree.nodes:
				self._assets += [a for a in node.assets if node.spawn and a not in self._assets]
		
		return self._assets
	
	@property
	def nodes(self) -> list:
		'''
		Returns a list of all nodes that can be spawned
		'''
		if self._nodes is None:
			self._nodes = [node for node in self.spawn_tree.nodes if node.spawn]
		
		return self._nodes

	@property
	def assets_per_layer(self) -> list:
		'''
		Returns a list containing assets ordered by layers:
		assets_per_layer[layer] -> [asset1, asset2, asset3]
		'''
		if self._assets_per_layer is None:
			assets = self.assets.copy()
			self._assets_per_layer = []
			layer = 0

			while len(assets):
				self._assets_per_layer.append([])
				for a in self.assets:
					if a.custo_part_layer == layer:
						self._assets_per_layer[layer].append(a)
						assets.remove(a)
				
				layer += 1
		
		return self._assets_per_layer
	
	@property
	def assets_per_slot(self) -> dict:
		'''
		Returns a dict containing all assets identified per slots:
		assets_per_slot["slot_name"] -> [asset1, asset2, asset3]
		'''
		return self._assets_per_slot

	@assets_per_slot.setter
	def assets_per_slot(self, key, value):
		self._assets_per_slot[key] = value
	
	@property
	def spawned_assets_per_slot(self) -> dict:
		'''
		Returns a dict containing all spanwed assets identified per slots:
		spawned_assets_per_slot["slot_name"] = [asset1, asset2, asset3]
		'''
		return self._spawned_assets_per_slot

	@spawned_assets_per_slot.setter
	def spawned_assets_per_slot(self, key, value):
		self._spawned_assets_per_slot[key] = value

	@property
	def is_all_slots_spawned(self) -> bool:
		'''
		Returns True if no slots is available
		'''
		entirely_spawned = True

		for s in self.assets_per_slot.values():
			if s is None:
				return False

		return entirely_spawned

	@property
	def available_slots(self) -> list:
		'''
		The list of slots which have no assets plug into
		'''
		available = []
		for slot, assets in self.spawned_assets_per_slot.items():
			if assets is None:
				available.append(slot)
			else:
				is_available = True
				for a in assets:
					if a.custo_part_slots[slot].checked and not a.custo_part_keep_lower_slots[slot].checked:
						is_available = False
						break
				if is_available:
					available.append(slot)

		return available
	
	@property
	def available_asset_slots(self) -> list:
		'''
		The list of slots that can be covered by the availabe assets
		'''
		return list(self.assets_per_slot.keys())

	def print_assets_per_layer(self) -> None:
		print('---------------------------------------')
		for i,l in enumerate(self.assets_per_layer):
			print('layer =', i)
			print('objects = ', l)
		print('---------------------------------------')

	@classmethod
	def poll(cls, context):
		return context.scene.custo_spawn_root is not None and context.scene.custo_spawn_tree is not None and context.scene.custo_spawn_count
	
	def init_assets_per_slot(self, context) -> None:
		'''
		Init value for assets_per_slots
		'''
		self._assets_per_slot = {}
		for asset in self.assets:
			slots = asset.custo_part_slots
			for slot in slots:
				if not slot.checked:
					continue
				if slot.name not in self._assets_per_slot.keys():
					self._assets_per_slot[slot.name] = [asset]
				else:
					self._assets_per_slot[slot.name].append(asset)

	def init_spawned_assets_per_slot(self, context) -> None:
		'''
		Init value for spawned_assets_per_slots
		'''
		self._spawned_assets_per_slot = {}
		for slot in context.scene.custo_slots:
			self._spawned_assets_per_slot[slot.name] = None

	def init(self, context):
		'''
		Init all values to be able to start spawning process correctly. 
		'''
		self.spawn_root = context.scene.custo_spawn_root
		self.spawn_tree = context.scene.custo_spawn_tree
		self.spawn_count = context.scene.custo_spawn_count
		self._assets = None
		self._assets_per_layer = None
		self._assets_per_slot = None
		self.init_assets_per_slot(context)
		self._spawned_assets_per_slot = None
		self.init_spawned_assets_per_slot(context)
		self._nodes = None

	def execute(self, context):
		self.init(context)

		for node in self.nodes:
			node.print_assets()
		
		collection = self.create_spawn_collection()
		for i in range(self.spawn_count):
			self.spawn_assets(collection)
		
		return {'FINISHED'}
	
	def create_spawn_collection(self):
		'''
		Creates a new collection to instance assets into. Reuse existing one if found
		'''
		if SPAWN_COLLECTION not in bpy.data.collections:
			collection = bpy.data.collections.new(name=SPAWN_COLLECTION)
			bpy.context.scene.collection.children.link(collection)
		else:
			collection = bpy.data.collections[SPAWN_COLLECTION]
			for o in collection.objects:
				collection.objects.unlink(o)

		self.spawn_root.instance_type = 'COLLECTION'
		self.spawn_root.instance_collection = collection

		return collection

	def spawn_assets(self, collection):
		'''
		Spawn one complete model, ensureing the model is complete and without overlapping
		'''
		while len(self.available_slots):
			available_slots = self.available_slots.copy()
			random.shuffle(available_slots)
			slot = available_slots.pop()

			if slot not in self.assets_per_slot.keys():
				print(f'No Asset(s) available for {slot} slot')
				return {'CANCELLED'}
			
			asset = random.choice(self.assets_per_slot[slot])
			self.assets_per_slot[slot].remove(asset)

			if self.spawned_assets_per_slot[slot] is None:
				self.spawned_assets_per_slot[slot] = []

			self.spawned_assets_per_slot[slot].append(asset)

			# add Object to Collection
			collection.objects.link(asset)
			

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