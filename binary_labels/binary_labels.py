from dataclasses import dataclass, field
import random


@dataclass
class BinaryLabel:
	name: str = ''
	value: bool = True
	valid_any: bool = False
	weight: float = 1.0
	
	def __str__(self):
		return f'BinaryLabel( name={self.name}, value={self.value}, valid_any={self.valid_any} )'

@dataclass
class LabelCategory:
	labels: dict = field(default_factory=dict)
	
	@property
	def valid_labels(self)->dict:
		enabled = LabelCategory()

		for l in self.labels.values():
			if not l.value or not l.weight:
				continue
			enabled.add_binary_label(l)

		return enabled

	@property
	def valid_any(self)->BinaryLabel:
		for l in self.labels.values():
			if l.valid_any and l.weight:
				return l
		return None
	
	@property
	def not_valid_any(self)->list[BinaryLabel]:
		labels = []
		for l in self.labels.values():
			if not l.valid_any and l.weight:
				labels.append(l)
		label_category = LabelCategory()
		label_category.add_labels(labels)
		return label_category
	
	@property
	def is_valid_any(self)->bool:
		if self.valid_any is None:
			return False
		
		return self.valid_any.value
	
	def set_invalid_label(self)->None:
		self.categories['__invalid__'] = None

	def add_label(self, name:str, value:bool, weight:float=1.0, valid_any:bool=False, replace:bool=True, unique:bool=False)->None:
		if not replace and name in self.labels.keys():
			return
		
		if unique and replace:
			self.labels.clear()

		if not replace and unique and len(self.labels.keys()):
			return
		
		elif valid_any and self.valid_any is not None:
			self.valid_any.valid_any = False

		label = BinaryLabel(name=name, value=value, valid_any=valid_any, weight=weight)
		
		self.labels[name] = label
	
	def add_binary_label(self, label:BinaryLabel, replace:bool=True, unique:bool=False)->None:
		self.add_label(label.name, label.value, valid_any=label.valid_any, weight=label.weight, replace=replace, unique=unique)

	def remove_label(self, label:BinaryLabel)->None:
		if label.name in self.labels.keys():
			del self.labels[label.name][label]

	def add_labels(self, labels:list, replace:bool=True, unique:bool=False)->None:
		for l in labels:
			self.add_label(name=l.name, value=l.value, valid_any=l.valid_any, weight=l.weight, replace=replace, unique=unique)
		
	def labels_intersection(self, label1:list[BinaryLabel], label2:list[BinaryLabel]):
		"""
		Args:
			label1 (list)
			label2 (list)

		Returns:
			list[BinaryLabel]: return the list of labels that are Identical in both inputed label list
		"""
		result = LabelCategory()
		for l in label1.values():
			if not l.value:
				continue
			if l.name not in label2:
				continue
			
			if l.value == label2[l.name].value:
				result.add_binary_label(l)

		return result

	def resolve(self, labels:list[BinaryLabel]):
		valid_labels = self.not_valid_any
		if self.is_valid_any:
			for l in valid_labels.values():
				l.value = True
		else:
			valid_labels = valid_labels.enabled

		return self.labels_intersection(valid_labels, labels)
	
	def keys(self):
		return self.labels.keys()
	
	def values(self):
		return self.labels.values()
	
	def items(self):
		return self.labels.items()
	
	def __len__(self):
		return len(self.labels.keys())
	
	def __iter__(self):
		yield len(self.labels.values())
		yield from self.labels.values()

	def __getitem__(self, key):
		return self.labels[key]
	
	def __contains__(self, item:str):
		for l in self.labels.values():
			if l.name == item:
				return True
		return False

	def __str__(self):
		text='LabelCategory ['
		i = 0
		for l in self.labels.keys():
			text += r'{ ' + f'"{l}" : '
			text += f'{self.labels[l]}'
			if i < len(self.labels.keys()) - 1:
				text += '}, '
			
			i += 1
		text += '}]'
		return text

@dataclass
class LabelCombinaison:
	categories : dict = field(default_factory=dict)

	@property
	def as_dict(self):
		return {lc : l for lc, l in self.items()}
	
	@property
	def variation(self):
		variation = LabelVariation()

		for lc, l in self.categories.items():
			variation[lc] = random.choice(list(l.labels.values()))
		
		return variation
	
	@property
	def weights(self)->tuple:
		weights = tuple()
		for l in self.categories.values():
			weights += (l.weight,)
		return weights
	
	def from_dict(self, input_dict:dict):
		for lc, l in input_dict.items():
			if not isinstance(lc, str):
				print('Wrong Format Inputed')
				return
			if isinstance(l, BinaryLabel):
				self.add_binary_label(lc, l)
			elif isinstance(l, dict):
				self.add_label(lc, l['name'], l['value'], l['valid_any'])
			else:
				print('Wrong Format Inputed')
				return
	
	def set_invalid_label(self):
		self.categories['__invalid__'] = None

	def add_label(self, category:str, name:str, value:bool, weight:float=1.0, valid_any=False, replace=True, unique=False):
		if category not in self.categories.keys():
			LabelCombinaison.set_label(self, category, name, value, weight=weight, valid_any=valid_any, replace=replace, unique=unique)
		else:
			label_category = self.categories[category]
			label_category.add_label(name, value, weight=weight, valid_any=valid_any, replace=replace, unique=unique)

	def add_binary_label(self, category:str, label:BinaryLabel, replace=True, unique=False):
		if category not in self.categories.keys():
			LabelCombinaison.set_binary_label(self, category, label, replace=replace, unique=unique)
		else:
			label_category = self.categories[category]
			label_category.add_binary_label(label, replace=replace, unique=unique)

	def set_label(self, category:str, name:str, value:bool, weight:float=1.0, valid_any=False, replace=True, unique=False):
		if not replace and category in self.categories.keys():
			return
		
		label_category = LabelCategory()
		label_category.add_label(name=name, value=value, weight=weight, valid_any=valid_any, replace=replace, unique=unique)
		self.categories[category] = label_category

	def set_binary_label(self, category:str, label:BinaryLabel, replace=True, unique=False):
		if not replace and category in self.categories.keys():
			return
		
		label_category = LabelCategory()
		label_category.add_binary_label(label=label, replace=replace, unique=unique)
		self.categories[category] = label_category

	def items(self):
		items = [(lc, list(l.values())) for lc, l in self.categories.items()]
		return items
	
	def keys(self):
		return self.categories.keys()
	
	def values(self):
		return [l.values() for l in self.categories.values()]
	
	def __len__(self):
		return len(self.categories.keys())
	
	def __iter__(self):
		yield len(self.categories.values())
		yield from self.categories.values()

	def __getitem__(self, key):
		return self.categories[key].labels.values()
	
	def __setitem__(self, key, value):
		if isinstance(value, LabelCategory):
			self.categories[key] = value
		elif isinstance(value, BinaryLabel):
			self.add_binary_label(key, value, replace=True)
		else:
			print('Wrong Format Inputed')
		
	def __contains__(self, item:str):
		for l in self.categories.values():
			if l.name == item:
				return True
		return False

	def __str__(self):
		text = f'{self.__class__.__name__} : ' + r'{'
		i=0
		for lc, l in self.categories.items():
			text += f'"{lc}" : {l}'
			if i < len(self.categories.keys()) - 1:
				text += ', '
			i += 1
		text += r'} '
		return text

@dataclass
class LabelVariation(LabelCombinaison):
	categories : dict = field(default_factory=dict)

	@property
	def variation(self):
		pass

	@property
	def combinaison(self):
		combinaison = LabelCombinaison()

		for lc, l in self.categories.items():
			combinaison.add_binary_label(lc, list(l.values())[0])

		return combinaison

	def set_invalid_label(self):
		self.categories['__invalid__'] = None

	def add_label(self, category:str, name:str, value:bool, weight:float=1.0, valid_any:bool=False, replace:bool=False):
		super().add_label(category, name, value, weight=weight, valid_any=valid_any, replace=replace, unique=True)

	def add_binary_label(self, category:str, label:BinaryLabel, replace:bool=False):
		super().add_binary_label(category, label, replace=replace, unique=True)

	def set_label(self, category:str, name:str, value:bool, weight:float=1.0, valid_any:bool=False, replace:bool=False):
		super().set_label(category, name, value, weight=weight,valid_any=valid_any, replace=replace, unique=True)

	def set_binary_label(self, category:str, label:BinaryLabel, replace:bool=False):
		super().set_binary_label(category, label, replace=replace, unique=True)
	
	def items(self):
		items = [(lc, list(l.values())[0]) for lc, l in self.categories.items()]
		return items
	
	def keys(self):
		return self.categories.keys()
	
	def values(self):
		return [list(l.values())[0] for l in self.categories.values()]
	
	def __len__(self):
		return len(self.categories.keys())
	
	def __iter__(self):
		yield len(self.categories.values())
		yield from self.categories.values()
	
	def __contains__(self, item:str):
		for l in self.categories.values():
			if l.name == item:
				return True
		return False
	


if __name__ == '__main__':
	# ref = LabelCategory()
	# ref.add_label('tutu', False)
	# ref.add_label('tutu', True)
	# ref.add_label('titi', False)
	# ref.add_label('tonton', False)
	# ref.add_label('tyty', False)
	# ref.add_label('tata', True)
	# ref.add_label('toutou', False, valid_any=True)
	# # print(ref)

	# lc_in = LabelCategory()
	# lc_in.add_label('tutu', True)
	# lc_in.add_label('tata', True)

	# # print(ref.resolve(lc_in))

	# combi = LabelCombinaison()

	# combi['ref'] = ref
	# combi['input'] = lc_in

	# combi.add_label('ref', 'tutu', False)
	# combi.add_label('ref', 'super', True)
	# combi.add_label('ref', '1231231123132', True)
	# combi.set_label('ref', 'super', False)

	# print(combi)
	
	variation = LabelVariation()

	variation.add_label('gender', 'male', True)
	variation.add_label('etnicity', 'cau', True)
	variation.add_label('age', 'adult', True)
	variation.add_label('age', 'child', False, replace=True)
	variation.add_label('bodytype', 'average', True)
	variation.set_label('etnicity', 'afr', True, replace=True)

	# print(variation)

	# for lc,l in variation.items():
	# 	print(lc, l)

	# variation['gender'] = BinaryLabel('female', False, False)

	# for lc,l in variation.items():
	# 	print(lc, l)

	# print(variation.as_dict)

	v2 = LabelVariation()

	v2.from_dict(variation.as_dict)

	print(v2)