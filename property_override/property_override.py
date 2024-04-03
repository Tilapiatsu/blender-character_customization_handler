from dataclasses import dataclass, field
from mathutils import Color, Vector
from enum import Enum

PROPERTY_TYPE = {
				'FLOAT' : 'FloatProperty',
				'INT' : 'IntProperty',
				'BOOL' : 'BoolProperty',
				'STRING' : 'StringProperty',
				'COLOR' : 'ColorProperty',
				'VECTOR' : 'VectorProperty'
				}

@dataclass
class FloatProperty():
	target : str
	label: str
	name: str
	value : float = 0.0
	weight: float = 1.0

@dataclass
class IntProperty():
	target : str
	label: str
	name: str
	value : int = 0.0
	weight: float = 1.0

@dataclass
class BoolProperty():
	target : str
	label: str
	name: str
	value : bool = False
	weight: float = 1.0

@dataclass
class StringProperty():
	target : str
	label: str
	name: str
	value : str = 0.0
	weight: float = 1.0

@dataclass
class ColorProperty():
	target : str
	label: str
	name: str
	value : Color = Color((0.0, 0.0, 0.0))
	weight: float = 1.0
	
@dataclass
class VectorProperty():
	target : str
	label: str
	name: str
	value : Vector = Vector((0.0, 0.0, 0.0))
	weight: float = 1.0
	
@dataclass
class PropertyOverride():
	properties : dict = field(default_factory=dict)
	
	def add_property(self, target:str, value_type:str, label:str, name:str, value:any, weight:float=1.0, replace:bool=True):
		if not replace and target in self.properties.keys() and name in self.properties[target]:
			return
		
		prop = eval(PROPERTY_TYPE[value_type])(target=target, label=label, name=name, value=value, weight=weight)
		if target not in self.properties.keys():
			self.properties[target] = {name : prop}
		else:
			self.properties[target][name] = prop

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
