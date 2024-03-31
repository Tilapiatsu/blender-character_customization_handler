import bpy
from ...operators.properties.custo_asset_properties import CustoAssetProperties
from ...binary_labels.binary_labels import LabelCategory, LabelCombinaison, LabelVariation
from dataclasses import dataclass, field
import random

@dataclass
class NodeAttributes:
	labels : LabelCombinaison = field(default_factory=LabelCombinaison)
	
	def add_label(self, category:str, name:str, value:bool, valid_any=False, unique=False):
		self.labels.add_label(category=category, name=name, value=value, valid_any=valid_any, replace=unique)


	def add_labels(self, labels:dict, unique=False):
		for lc, l in labels.items():
			self.add_label(lc, name=l.name, value=l.value, valid_any=l.valid_any, unique=unique)

	def add_label_combinaison(self, label_combinaison:LabelCombinaison):
		for lc, l in label_combinaison.items():
			self.add_label(lc, l.name, l.value, valid_any=l.valid_any, unique=True)
	
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
	
	def mesh_variation(self, variations:LabelVariation, exclude=[]):
		return self.asset.mesh_variation(variations, exclude=exclude)
	
	def is_valid_mesh(self, ob, variations:LabelVariation):
		return self.asset.is_valid_mesh(ob, variations)

	def has_mesh_with_labels(self, variations:LabelVariation):
		return self.asset.has_mesh_with_labels(variations)

