import bpy
from dataclasses import dataclass, field
import random

dataclass
class MatterialAttribute():
	material: bpy.types.Material
	weight:float=1.0

@dataclass
class MaterialList():
	materials: dict = field(default_factory=dict)

	@property
	def pick(self):
		return random.choices(self.materials.values(), weights=self.weights)[0]

	@property
	def weights(self)->tuple:
		weights = tuple()
		for m in self.materials.values():
			weights = weights + (m.weight,)
		return weights
		
	def add(self, material:bpy.types.Material, weight:float=1.0):
		self.materials[material.name] = MatterialAttribute(material, weight)

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