from dataclasses import dataclass, field
from mathutils import Vector
import random

PROPERTY_TYPE = {
				'FLOAT' : 'FloatProperty',
				'INT' : 'IntProperty',
				'BOOL' : 'BoolProperty',
				'STRING' : 'StringProperty',
				'COLOR' : 'ColorProperty',
				'VECTOR' : 'VectorProperty'
				}

MATERIAL_INPUT_INDEX =  {
						'Base Color' : 0,
						'Metallic' : 1,
						'Roughness' : 2,
						'IOR' : 3,
						'Alpha' : 4,
						'Normal' : 5,
						'Weight' : 6,
						'Subsurface Weight' : 7,
						'Subsurface Radius' : 8,
						'Subsurface Scale' : 9,
						'Subsurface IOR' : 10,
						'Subsurface Anisotropy' : 11,
						'Specular IOR Level' : 12,
						'Specular Tint' : 13,
						'Anisotropic' : 14,
						'Anisotropic Rotation' : 15,
						'Tangent' : 16,
						'Transmission Weight' : 17,
						'Coat Weight' : 18,
						'Coat Roughness' : 19,
						'Coat IOR' : 20,
						'Coat Tint' : 21,
						'Coat Normal' : 22,
						'Sheen Weight' : 23,
						'Sheen Roughness' : 24,
						'Sheen Tint' : 25,
						'Emission Color' : 26,
						'Emission Strength' : 27
						}

@dataclass
class Property():
	@property
	def index(self):
		if self.name not in MATERIAL_INPUT_INDEX:
			return None
		return MATERIAL_INPUT_INDEX[self.name]

@dataclass
class FloatProperty(Property):
	target : str
	label: str
	name: str
	value : float = 0.0
	weight: float = 1.0


@dataclass
class IntProperty(Property):
	target : str
	label: str
	name: str
	value : int = 0.0
	weight: float = 1.0

@dataclass
class BoolProperty(Property):
	target : str
	label: str
	name: str
	value : bool = False
	weight: float = 1.0

@dataclass
class StringProperty(Property):
	target : str
	label: str
	name: str
	value : str = 0.0
	weight: float = 1.0

@dataclass
class ColorProperty(Property):
	target : str
	label: str
	name: str
	value : tuple = (0.0, 0.0, 0.0, 1.0)
	weight: float = 1.0

@dataclass	
class VectorProperty(Property):
	target : str
	label: str
	name: str
	value : Vector = Vector((0.0, 0.0, 0.0))
	weight: float = 1.0


@dataclass
class Properties():
	properties: dict = field(default_factory=dict)

	@property
	def pick(self):
		def weights(list)->tuple:
			weights = tuple()
			for m in list:
				weights = weights + (m.weight,)
			return weights
		
		properties = []
		for prop in self.properties.values():
			if len(prop) > 1:
				picked = random.choices(prop, weights(prop))[0]
				properties.append(picked)
			else:
				properties.append(prop[0])

		return properties
	
	def add_property(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0, replace:bool=True):
		if not replace and target in self.properties.keys() and name in self.properties[target]:
			return
		
		prop = eval(PROPERTY_TYPE[value_type])(target=target, label=label, name=name, value=value, weight=weight)
		if name not in self.properties:
			self.properties[name] = [prop]
		else:
			self.properties[name].append(prop)

	def set_property(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0):
		if name in self.properties:
			prop = eval(PROPERTY_TYPE[value_type])(target=target, label=label, name=name, value=value, weight=weight)
			self.properties[name] = [prop]

	def keys(self):
		return list(self.properties.keys())
	
	def values(self):
		return list(self.properties.values())
	
	def items(self):
		return self.properties.items()
	
	def remove(self, name):
		del self.properties[name]

	def __len__(self):
		return len(self.properties.keys())
	
	def __iter__(self):
		yield len(self.properties.values())
		yield from self.properties.values()

	def __getitem__(self, key):
		return self.properties[key]
	
	def __contains__(self, item:str):
		for p in self.properties.values():
			if p.target == item:
				return True
		return False

	def __str__(self):
		text='Properties ['
		i = 0
		for p in self.properties.keys():
			text += r'{ ' + f'"{p}" : '
			text += f'{self.properties[p]}'
			if i < len(self.properties.keys()) - 1:
				text += '},\n'
			
			i += 1
		text += '}]'
		return text

@dataclass
class PropertyOverride():
	properties : dict = field(default_factory=dict)

	
	def add_property(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0, replace:bool=True):
		if not replace and target in self.properties.keys() and name in self.properties[target]:
			return
		
		if target not in self.properties.keys():
			prop = Properties()
			prop.add_property(target=target, value_type=value_type, label=label, name=name, value=value, weight=weight)
			self.properties[target] = prop
		else:
			self.properties[target].add_property(target=target, value_type=value_type, label=label, name=name, value=value, weight=weight)

	def set_property(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0):
		prop = eval(PROPERTY_TYPE[value_type])(target=target, label=label, name=name, value=value, weight=weight)
		self.properties[name] = [prop]


	def keys(self):
		return list(self.properties.keys())
	
	def values(self):
		return list(self.properties.values())
	
	def items(self):
		return self.properties.items()
	
	def remove(self, name):
		del self.properties[name]

	def __len__(self):
		return len(self.properties.keys())
	
	def __iter__(self):
		yield len(self.properties.values())
		yield from self.properties.values()

	def __getitem__(self, key):
		return self.properties[key]
	
	def __contains__(self, item:str):
		for p in self.properties.values():
			if p.target == item:
				return True
		return False

	def __str__(self):
		text='PropertyOverride ['
		i = 0
		for p in self.properties.keys():
			text += r'{ ' + f'"{p}" : '
			text += f'{self.properties[p]}'
			if i < len(self.properties.keys()) - 1:
				text += '},\n'
			
			i += 1
		text += '}]'
		return text

if __name__ == '__main__':
	pass
