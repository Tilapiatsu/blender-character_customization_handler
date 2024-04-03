import bpy
from dataclasses import dataclass, field
import random

dataclass
class MatterialAttribute():
	material: bpy.types.Material
	weight: float=1.0
	
	def __str__(self):
		return f'material={self.material.name}, weight={self.weight}'

@dataclass
class MaterialList():
	materials: dict = field(default_factory=dict)

	@property
	def pick(self):
		return random.choices(list(self.materials.values()), weights=self.weights)[0]

	@property
	def weights(self)->tuple:
		weights = tuple()
		for m in self.materials.values():
			weights = weights + (m.weight,)
		return weights
		
	def add(self, material:bpy.types.Material, weight:float=1.0):
		mat = MatterialAttribute()
		mat.material = material
		mat.weight = weight
		self.materials[material.name] = mat

	def filter_by_label_combinaison(self, label_combinaison:dict, replace_weight:bool=True)->list:
		result_list = MaterialList()
		if not len(label_combinaison.keys()):
			return self

		for lc, l in label_combinaison.items():
			for label in l:
				for d in self.materials.values():
					if d.material.custo_label_category_definition[lc].labels[label.name].value:
						if replace_weight:
							weight = label.weight
						else:
							weight = d.weight
						result_list.add(material=d.material, weight=weight)

		return result_list
	
	def keys(self):
		return list(self.materials.keys())
	
	def values(self):
		return list(self.materials.values())
	
	def items(self):
		return self.materials.items()
	
	def remove(self, name):
		del self.materials[name]

	def __len__(self):
		return len(self.materials.keys())
	
	def __iter__(self):
		yield len(self.materials.values())
		yield from self.materials.values()

	def __getitem__(self, key):
		return self.materials[key]
	
	def __contains__(self, item:str):
		for l in self.materials.values():
			if l.name == item:
				return True
		return False

	def __str__(self):
		text='Materials ['
		i = 0
		for m in self.materials.keys():
			text += r'{ ' + f'"{m}" : '
			text += f'{self.materials[m]}'
			if i < len(self.materials.keys()) - 1:
				text += '},\n'
			
			i += 1
		text += '}]'
		return text