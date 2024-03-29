import bpy
from ...operators.properties.custo_asset_properties import CustoAssetProperties
from dataclasses import dataclass, field
import random


@dataclass
class NodeBinaryLabel:
	name: str
	value: bool = True
	valid_any: bool = False
	
	def __str__(self):
		return f'{self.name} : {self.value}'


@dataclass
class LabelCombinaison:
	labels : dict = field(default_factory=dict)

	def set_invalid_label(self):
		self.labels['__invalid__'] = None

	def set_label(self, category:str, name:str, value:bool, replace=True, valid_any=False):
		if not replace and category in self.labels:
			return
		
		self.labels[category] = NodeBinaryLabel(name=name, value=value, valid_any=valid_any)

	def set_binary_label(self, category:str, binary_label:NodeBinaryLabel, replace=True):
		if not replace and category in self.labels:
			return
		
		self.labels[category] = binary_label

	def items(self):
		return self.labels.items()
	
	def keys(self):
		return self.labels.keys()
	
	def values(self):
		return self.labels.values()
	
	def as_dict(self):
		return_dict = {}

		for lc, l in self.labels.items():
			return_dict[lc] = [l]

		return return_dict
	
	def __getitem__(self, key):
		return self.labels[key]
	
	def __len__(self):
		return len(self.labels)
	


@dataclass
class NodeAttributes:
	labels : dict = field(default_factory=dict)
	
	def add_label(self, category:str, name:str, value:bool, valid_any=False):
		if category not in self.labels.keys():
			self.labels[category] = [NodeBinaryLabel(name=name, value=value, valid_any=valid_any)]
		else:
			label = NodeBinaryLabel(name=name, value=value, valid_any=valid_any)
			if label in self.labels[category]:
				return
			
			self.labels[category].append(NodeBinaryLabel(name=name, value=value, valid_any=valid_any))

	def add_labels(self, labels:dict, unique=False):
		for lc, l in labels.items():
			if unique and lc in self.labels.keys():
				continue
			else:
				self.add_label(lc, name=l.name, value=l.value, valid_any=l.valid_any)

	def add_label_combinaison(self, label_combinaison:LabelCombinaison):
		for lc, l in label_combinaison.items():
			self.add_label(lc, l.name, True, valid_any=l.valid_any)
	
	def get_label_combinaison(self, label_categories:list=None):
		label_combinaison = LabelCombinaison()
		
		for lc in self.labels.keys():
			if label_categories is not None:
				if lc not in label_categories:
					continue
			label = random.choice(self.labels[lc])
			label_combinaison.set_binary_label(lc, binary_label=label)

		return label_combinaison
	
	def get_labels(self, label_categories:list=None):
		labels = {}
		
		for lc in self.labels.keys():
			if label_categories is not None:
				if lc not in label_categories:
					continue
			labels[lc] = self.labels[lc]

		return labels
	
	def __str__(self):
		return f'Attributes : {self.labels}'


@dataclass
class NodeAsset:
	asset : CustoAssetProperties
	attributes : NodeAttributes = field(default_factory=NodeAttributes)

	@property
	def name(self):
		return self.asset.name
	
	@property
	def asset_type(self):
		return self.asset.asset_type
	
	@property
	def asset_id(self):
		return self.asset.asset_id
	
	@property
	def layer(self):
		return self.asset.layer
	
	@property
	def slots(self):
		return self.asset.slots
	
	@property
	def asset_name(self):
		return self.asset.asset_name
	
	@property
	def valid_labels(self):
		return self.asset.valid_labels
	
	@property
	def all_mesh_variations(self):
		return self.asset.all_mesh_variations
	
	@property
	def materials(self)->dict:
		return self.asset.materials
	
	def mesh_variation(self, variations:LabelCombinaison, exclude=[]):
		return self.asset.mesh_variation(variations, exclude=exclude)
	
	def is_valid_mesh(self, ob, variations:LabelCombinaison):
		return self.asset.is_valid_mesh(ob, variations)

	def has_mesh_with_labels(self, variations:LabelCombinaison):
		return self.asset.has_mesh_with_labels(variations)

