import bpy
import random, math, copy
from .spawn_const import SPAWN_COLLECTION, SPAWN_INSTANCE

class AssetsPerSlot:
	def __init__(self):
		pass

class SpawnCustomizationTree(bpy.types.Operator):
	bl_idname = "scene.customization_spawn"
	bl_label = "Spawn Customization Tree"
	bl_options = {'REGISTER', 'UNDO'}
	bl_description = "Spawn Objects Using Customization Tree"

	@property
	def ch_settings(self):
		return bpy.context.scene.custo_handler_settings

	@property
	def assets(self) -> list:
		'''
		Returns a list of all assets that can be spawned
		'''
		if self._assets is None:
			self._assets = []
			for node in self.spawn_tree.custo_nodes:
				self._assets += [a for a in node.assets if node.spawn and a not in self._assets]
		
		return self._assets
	
	@property
	def nodes(self) -> list:
		'''
		Returns a list of all nodes that can be spawned
		'''
		if self._nodes is None:
			self._nodes = [node for node in self.spawn_tree.custo_nodes if node.spawn]
		
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
			elif assets is False:
				pass
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
		return context.scene.custo_handler_settings.custo_spawn_root is not None and context.scene.custo_handler_settings.custo_spawn_tree is not None and context.scene.custo_handler_settings.custo_spawn_count
	
	def print_init_spawn_message(self, index):
		print('')
		print('========================================================')
		print(f'Spawn New Assembly {str(index).zfill(3)}')
		print(f'--------------------------------------------------------')

	def print_end_message(self):
		print('')
		print('========================================================')
		print(f'Spawn Completed')
		print(f'--------------------------------------------------------')

	def get_indexed_name(self, prefix, index):
		return f'{prefix}_{str(index).zfill(3)}'

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
		self.spawn_root = self.ch_settings.custo_spawn_root
		self.spawn_tree = self.ch_settings.custo_spawn_tree
		self.spawn_count = self.ch_settings.custo_spawn_count
		self.spawned_mesh_instance = self.ch_settings.spawned_mesh_instance
		self.spawn_max_per_row = self.ch_settings.custo_spawn_max_per_row
		self.exclude_incomplete_mesh_combinaison = self.ch_settings.exclude_incomplete_mesh_combinaison

		self._assets = None
		self._nodes = None
		self.layer_collection_root = context.view_layer.layer_collection

		self.clean_previous_generation()

	def clean_previous_generation(self):
		for o in self.spawned_mesh_instance:
			bpy.data.objects.remove(o.object, do_unlink=True)
		
		self.spawned_mesh_instance.clear()
		previous_generation = [o for o in bpy.data.objects if o.name.startswith(SPAWN_INSTANCE)]
		for o in previous_generation:
			bpy.data.objects.remove(o)
	
	def init_spawn(self, context):
		self._assets_per_layer = None
		self._assets_per_slot = None
		self.init_assets_per_slot(context)
		self._spawned_assets_per_slot = None
		self.init_spawned_assets_per_slot(context)

	def execute(self, context):
		self.init(context)

		for node in self.nodes:
			node.print_assets()
		
		for i in range(self.spawn_count):
			self.init_spawn(context)
			self.collection = self.create_spawn_collection(index=i)
			self.print_init_spawn_message(i)
			self.spawn_assembly()
		
		self.print_end_message()
		return {'FINISHED'}
	
	def create_spawn_collection(self, index=0):
		'''
		Creates a new collection to instance assets into. Reuse existing one if found
		'''
		spawn_collection_name = self.get_indexed_name(SPAWN_COLLECTION, index)
		if spawn_collection_name not in bpy.data.collections:
			collection = bpy.data.collections.new(name=spawn_collection_name)
		else:
			collection = bpy.data.collections[spawn_collection_name]
			for o in collection.objects:
				collection.objects.unlink(o)

		spawn_instance_name = self.get_indexed_name(SPAWN_INSTANCE, index)
		if spawn_instance_name not in bpy.data.objects:
			spawn_instance = self.create_spawn_instance(index=index)
		else:
			spawn_instance = bpy.data.objects[spawn_instance_name]

		spawn_instance.instance_type = 'COLLECTION'
		spawn_instance.instance_collection = collection

		return collection

	def create_spawn_instance(self, index:int=0)->bpy.types.Object:
		"""Create an empty object in the proper location based on its index

		Args:
			index (int): curent instance index

		Returns:
			bpy.types.Object: The Empty Object
		"""
		root_instance = bpy.data.objects.new(self.get_indexed_name(SPAWN_INSTANCE, index), object_data=None)
		self.spawn_root.users_collection[0].objects.link(root_instance)
		root_instance.empty_display_size = 0.2
		root_instance.parent = self.spawn_root
		# root_instance.show_name = True

		root_instance.location = self.get_root_instance_location(index)
		return root_instance

	def get_root_instance_location(self, index:int=0)->tuple:
		"""Returns the root instance coordinate to spawn each instance in a grid pattern

		Args:
			index (int): curent instance index

		Returns:
			tuple: (10, 20, 0)
		"""
		return (index % self.spawn_max_per_row, math.floor(index / self.spawn_max_per_row), 0)

	def spawn_assembly(self):
		'''
		Spawn one model, ensuring the model is complete and is without overlapping
		'''
		self.first_asset = True
		self.mesh_variation = {}
		self.spawned_meshes = []
		pick_new_slot = True

		while len(self.available_slots):
			available_slots = self.available_slots.copy()
			
			# Picking a new Slot
			if pick_new_slot:
				# Randomly pick one slot
				random.shuffle(available_slots)
				self.slot = available_slots.pop()
				print(f'Spawn slot : {self.slot}')
			
			# no more mesh in current Slot, invalidate and allow to pick a new slot
			if not len(self.assets_per_slot[self.slot]):
				pick_new_slot = True
				self.spawned_assets_per_slot[self.slot] = False
				continue
			# Pick one asset for selected slot
			else:
				asset = random.choice(self.assets_per_slot[self.slot])
			
			# Spawn Mesh
			if not self.spawn_asset(asset) and len(self.assets_per_slot[self.slot]):
				pick_new_slot = False

	def spawn_asset(self, asset):
		# Lock mesh variation : pick one mesh and store mesh variation combinaison for all future asset spawn
		if not self.lock_mesh_variation_combinaison(asset):
			# if no valid mesh found, pick another asset
			return None
		
		mesh = asset.mesh_variation(self.mesh_variation, self.spawned_meshes)
		
		self.remove_asset_per_slot(asset)
		
		if mesh is None:
			print(f'No valid mesh found for this mesh variation')
			return False

		self.update_spawned_assets_per_slot(asset)

		# add Object to Collection : Spawning !
		print(f'Spawning Mesh "{mesh.name}" to "{self.collection.name}" collection')
		self.spawned_meshes.append(mesh)
		object_instance = mesh.copy()

		instance = self.spawned_mesh_instance.add()
		instance.object = object_instance

		if len(object_instance.material_slots):
			
			# get all materials for Mesh Variations
			materials = mesh.custo_attributes.materials(asset.asset_type, variation=self.mesh_variation)
			print('Material List :', materials)
			if len(materials):
				# filter by attributes
				material_label_categories = asset.asset_type.asset_type.material_variation_categories
				attributes = asset.attributes.get_labels(label_categories = material_label_categories)
				materials_attribute_filtered = mesh.custo_attributes.filter_by_label_combinaison(materials, attributes)
				print(f'Attribute Filtered Material List :', materials_attribute_filtered, '\n', attributes)
				# Asstign the proper material to each slots
				for s in object_instance.material_slots:
					# Filter by Slots
					materials_slot_filtered = mesh.custo_attributes.filter_by_label_combinaison(materials_attribute_filtered, mesh.custo_attributes.valid_labels(s.material, include_label_category=[asset.asset_type.asset_type.material_slot_label_category.name]))
					print(f'Slot Filtered Material List :', materials_slot_filtered)
					if not len(materials_slot_filtered):
						continue
					material = random.choice(materials_slot_filtered)
					print(f'Assigning material "{material.name}" to "{object_instance.name}" object')
					s.material = material
		else:
			print(f'No Materials found of "{object_instance.name}" object')

		self.collection.objects.link(object_instance)
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
			elif self.spawned_assets_per_slot[s.name] is False:
				continue
			self.spawned_assets_per_slot[s.name].append(asset)

	def lock_mesh_variation_combinaison(self, asset) -> bool:
		'''
		The First Asset need to lock one mesh variation combinaison to only spawn meshes from this combinaison for the next parts.
		This method is storing the combinaison defined by this first asset to reuse it on other assets.
		'''

		def label_fake_intersection(label1:list, label2:list)->list:
			"""
			Args:
				label1 (list)
				label2 (list)

			Returns:
				list[str]: return the list of labels that are common to both inputed label list
			"""
			result = []
			for l in label1:
				if l not in label2:
					result.append(l)
				elif l in label2:
					result.append(l)
			return result
		
		if self.first_asset:
			# Lock Mesh Variation
			asset_attributes = asset.attributes
			asset_label_combinaison = asset_attributes.get_label_combinaison()
			asset_meshes = asset.asset.mesh_variations(asset_label_combinaison)
			
			if asset_meshes is None or not len(asset_meshes):
				return False
			
			self.first_asset = False
			valid_mesh = False
			print(f'Valid Labels for asset "{asset.name}" :\n{asset.valid_labels}')
			print(f'"{asset.name}" label attribute :\n{asset_label_combinaison}')
			
			while not valid_mesh:
				if not len(asset_meshes):
					return False

				picked_variation_mesh = random.choice(asset_meshes)
				asset_meshes.remove(picked_variation_mesh)
				valid_mesh_variation = False
				mesh_labels = asset.asset.valid_labels_from_mesh(picked_variation_mesh)
				

				while not valid_mesh_variation:
					valid_mesh_labels = False
					for mesh_category in asset.asset_type.asset_type.mesh_variation_label_categories:
						if not len(mesh_labels[mesh_category.name]):
							continue
						else:
							valid_mesh_labels = True
							break
					else:
						if not valid_mesh_labels:
							print(f'Incomplete variation :\n{self.mesh_variation}. skipping...')
							valid_mesh_variation = False
							break
					
					# Get asset label attribute
					self.mesh_variation = copy.deepcopy(asset_label_combinaison)

					# Parsing label to pick a random one to be use for all other slots
					for mesh_category in asset.asset_type.asset_type.mesh_variation_label_categories:		
						valid_labels = asset.asset.valid_label_catgory_labels_from_mesh(picked_variation_mesh, mesh_category)
						valid_labels = label_fake_intersection(valid_labels, mesh_labels[mesh_category.name])

						if not len(valid_labels):
							print(f'Invalid Mesh : {picked_variation_mesh.name}, skipping...')
							break

						picked_label = random.choice(valid_labels)
						
						if mesh_category.label_category.valid_any is not None:
							if mesh_category.label_category.valid_any.name == picked_label.name:
								not_any = mesh_category.label_category.not_valid_any
								mesh_labels[mesh_category.name] = not_any
								picked_label = random.choice(not_any)
								

						if len(mesh_labels[mesh_category.name]) > 0:
							if picked_label in mesh_labels[mesh_category.name]:
								mesh_labels[mesh_category.name].remove(picked_label)

						valid_mesh = True
						self.mesh_variation.set_label(category=mesh_category.name, name=picked_label.name, value=True, replace=False)

					# Check if other slots have at least one valid mesh that matches the previously picked label combinaison
					if self.exclude_incomplete_mesh_combinaison:
						viable = asset.asset_type.asset_type.is_viable_mesh_variation(self.mesh_variation)
						if not viable:
							print(f'Incomplete variation :\n{self.mesh_variation}. skipping...')
							valid_mesh = False

							for lc, l in mesh_labels.items():
								asset_id_label_category = asset.asset_type.asset_type.asset_label_category.name
								if lc == asset_id_label_category:
									continue
								if len(l) > 0:
									break
							else:
								print('All Label Variation tested, picking another mesh.')
								valid_mesh = False
								break
							
							continue

					valid_mesh_variation = True
				
			print(f'Current Mesh Variation :\n{self.mesh_variation}')
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


def unregister():
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)

if __name__ == "__main__":
	register()