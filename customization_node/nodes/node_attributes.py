from ...operators.properties.properties.custo_asset_properties import CustoAssetProperties
from dataclasses import dataclass, field
import random

@dataclass
class NodeBinaryLabel:
	label: str
	positive: bool = True
	
	def __str__(self):
		return f'{self.label} : {self.positive}'

@dataclass
class NodeAttributes:
	labels : dict = field(default_factory=dict)

	def add_label_combinaison(self, label_combinaison:dict):
		for lc, l in label_combinaison.items():
			if lc not in self.labels.keys():
				self.labels[lc] = [NodeBinaryLabel(label=l)]
			else:
				self.labels[lc].append(NodeBinaryLabel(label=l))
	
	def get_label_combinaison(self):
		label_combinaison = {}

		for lc in self.labels.keys():
			label_combinaison[lc] = random.choice(self.labels[lc])

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
	
	def mesh_variation(self, variations:dict, exclude=[]):
		return self.asset.mesh_variation(variations, exclude=exclude)
	
	def is_valid_mesh(self, ob, variations:dict):
		return self.asset.is_valid_mesh(ob, variations)

	def has_mesh_with_labels(self, variations:dict):
		return self.asset.has_mesh_with_labels(variations)

