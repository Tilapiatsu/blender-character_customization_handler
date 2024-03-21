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
					if not len(a.all_mesh_variations):
						continue
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
					if a.slots[slot].checked and not a.slots[slot].keep_lower_layer_slot:
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
			if not len(asset.all_mesh_variations):
				continue
			slots = [s for s in asset.slots if s.checked]
			for slot in slots:
				if slot.name not in self._assets_per_slot.keys():
					self._assets_per_slot[slot.name] = [asset]
				else:
					self._assets_per_slot[slot.name].append(asset)

	def init_spawned_assets_per_slot(self, context) -> None:
		'''
		Init value for spawned_assets_per_slots
		'''
		self._spawned_assets_per_slot = {}
		for slot in self.available_asset_slots:
			self._spawned_assets_per_slot[slot] = None

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
		self.layer_collection_root = context.view_layer.layer_collection

	def execute(self, context):
		self.init(context)

		for node in self.nodes:
			node.print_assets()
		
		self.collection = self.create_spawn_collection()
		for i in range(self.spawn_count):
			self.spawn_assembly()
		
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
		
		layer_collection = self.get_layer_collection_per_name(SPAWN_COLLECTION, self.layer_collection_root)
		layer_collection.hide_viewport = True

		self.spawn_root.instance_type = 'COLLECTION'
		self.spawn_root.instance_collection = collection

		return collection

	def spawn_assembly(self):
		'''
		Spawn one model, ensuring the model is complete and is without overlapping
		'''
		self.first_asset = True
		self.mesh_variation = {}
		self.spawned_meshes = []
		while len(self.available_slots):
			available_slots = self.available_slots.copy()
			
			# Randomly pick one slot
			random.shuffle(available_slots)
			slot = available_slots.pop()
			print(f'Spawn slot : {slot}')
			
			# Pick one asset for selected slot
			asset = random.choice(self.assets_per_slot[slot])
			
			# Spawn Mesh
			self.spawn_mesh(asset, slot)

	def spawn_mesh(self, asset, slot):
		# Lock mesh variation : pick one mesh and store mesh variation combinaison for all future asset spawn
		if not self.lock_mesh_variation(asset):
			# if no valid mesh found, pick another asset
			return False
		
		mesh = asset.mesh_variation(self.mesh_variation, self.spawned_meshes)
		
		self.remove_asset_per_slot(asset)
		self.update_spawned_assets_per_slot(asset)

		if mesh is None:
			print(f'No valid mesh found for this mesh variation')
			return False


		# add Object to Collection : Spawning !
		print(f'Spawning Mesh : {mesh.name}')
		self.spawned_meshes.append(mesh)
		self.collection.objects.link(mesh)
		return True
	
	def remove_asset_per_slot(self, asset):
		for s in self.assets_per_slot.keys():
			if asset in self.assets_per_slot[s]:
				self.assets_per_slot[s].remove(asset)
	
	def update_spawned_assets_per_slot(self, asset):
		for s in asset.slots:
			if s.name not in self.spawned_assets_per_slot.keys():
				continue
			if self.spawned_assets_per_slot[s.name] is None:
				self.spawned_assets_per_slot[s.name] = []
			self.spawned_assets_per_slot[s.name].append(asset)

	def lock_mesh_variation(self, asset) -> bool:
		'''
		The First Asset need to lock one mesh variation combinaison to only spawn mesh from this combinaison for the next parts.
		This method is storing the combinaison defined by this first asset to reuse it on other assets.
		'''
		if self.first_asset:
			# Lock Mesh Variation
			self.first_asset = False
			valid_mesh = False
			asset_meshes = asset.all_mesh_variations
			# print(asset.valid_labels)
			print(asset.attributes.labels)
			asset_valid_label_attributes = asset.attributes.labels
			while not valid_mesh:
				picked_variation_mesh = random.choice(asset_meshes)
				asset_meshes.remove(picked_variation_mesh)
				self.mesh_variation = {}
				for mesh_category in asset.asset_type.asset_type.mesh_variation_label_categories:
					valid_labels = []

					for l in picked_variation_mesh.custo_label_category_definition[mesh_category.name].labels:
						if not l.checked:
							continue
						
						if mesh_category.name in asset_valid_label_attributes.keys():
							pass

						valid_labels.append(l)
							
					valid_labels = [l for l in picked_variation_mesh.custo_label_category_definition[mesh_category.name].labels if l.checked]

					if not len(valid_labels):
						print(f'Invalid Mesh : {picked_variation_mesh.name}, skipping')
						break
					
					valid_mesh = True
					self.mesh_variation[mesh_category.name] = random.choice(valid_labels).name
				
				if not len(asset_meshes):
					return False
			print(f'Current Mesh Variation =', self.mesh_variation)
		return True
	
	def get_layer_collection_per_name(self, collection_name, layer_collection):
		'''
		Recursivelly search through "layer_collection" the collection with the given "collection_name" and returns it. Returns None if not found
		'''
		found = None
		if (layer_collection.name == collection_name):
			return layer_collection
		for layer in layer_collection.children:
			found = self.get_layer_collection_per_name(collection_name, layer)
			if found:
				return found

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