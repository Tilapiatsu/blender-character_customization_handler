from dataclasses import dataclass, field


@dataclass
class NodeBinaryLabel:
	name: str = ''
	value: bool = True
	valid_any: bool = False
	
	def __str__(self):
		return f'BinaryLabel( name={self.name}, value={self.value}, valid_any={self.valid_any} )'

@dataclass
class LabelCategory:
	name : str
	labels: dict = field(default_factory=dict)
	
	@property
	def enabled(self):
		enabled = LabelCategory(self.name + '_valid')

		for l in self.labels.values():
			if not l.value:
				continue
			enabled.add_binary_label(l)

		return enabled

	@property
	def valid_any(self)->NodeBinaryLabel:
		for l in self.labels.values():
			if l.valid_any:
				return l
		return None
	
	@property
	def not_valid_any(self):
		labels = []
		for l in self.labels.values():
			if not l.valid_any:
				labels.append(l)
		label_category = LabelCategory(self.name + '_not_valid_any')
		label_category.add_labels(labels)
		return label_category
	
	@property
	def is_valid_any(self)->bool:
		if self.valid_any is None:
			return False
		
		return self.valid_any.value

	def add_label(self, name:str, value:bool, valid_any=False, unique=False)->None:
		label = NodeBinaryLabel(name=name, value=value, valid_any=valid_any)
		if unique and label in self.labels.values():
			return
		
		if valid_any and self.valid_any is not None:
			self.valid_any.valid_any = False

		self.labels[name] = label
	
	def add_binary_label(self, label, unique=False)->None:
		self.add_label(label.name, label.value, label.valid_any, unique=unique)

	def remove_label(self, label)->None:
		if label.name in self.labels.keys():
			del self.labels[label.name]

	def add_labels(self, labels, unique=False)->None:
		for l in labels:
			self.add_label(name=l.name, value=l.value, valid_any=l.valid_any, unique=unique)
		
	def labels_intersection(self, label1, label2):
		"""
		Args:
			label1 (list)
			label2 (list)

		Returns:
			list[NodeBinaryLabel]: return the list of labels that are Identical in both inputed label list
		"""
		result = LabelCategory(label1.name + '_interstect_' + label2.name)
		for l in label1.values():
			if not l.value:
				continue
			if l.name not in label2:
				continue
			
			if l.value == label2[l.name].value:
				result.add_binary_label(l)

		return result

	def resolve(self, labels):
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
		return f'LabelCategory : {self.name} = [{", ".join([str(l.name)+"="+str(l.value) for l in self.labels.values()])}]'

@dataclass
class LabelCombinaison:
	categories : dict = field(default_factory=dict)

	def set_invalid_label(self):
		self.categories['__invalid__'] = None

	def add_label(self, category:str, name:str, value:bool, valid_any=False, unique=False):
		if category not in self.categories:
			self.set_label(category, name, value, valid_any)
		else:
			label_category = self.categories[category]
			label_category.add_label(name, value, valid_any, unique=unique)

	def add_binary_label(self, category:str, label:NodeBinaryLabel, unique=False):
		if category not in self.categories:
			self.set_binary_label(category, label)
		else:
			label_category = self.categories[category]
			label_category.add_binary_label(label, unique=unique)

	def set_label(self, category:str, name:str, value:bool, valid_any=False, unique=False):
		if unique and category in self.categories:
			return
		
		label_category = LabelCategory(category)
		label_category.add_label(name=name, value=value, valid_any=valid_any)
		self.categories[category] = label_category

	def set_binary_label(self, category:str, label:NodeBinaryLabel, unique=False):
		if unique and category in self.categories:
			return
		
		label_category = LabelCategory(category)
		label_category.add_binary_label(label=label)
		self.categories[category] = label_category

	def items(self):
		return self.categories.items()
	
	def keys(self):
		return self.categories.keys()
	
	def values(self):
		return self.categories.values()
	
	def as_dict(self):
		return self.categories	
	
	def __len__(self):
		return len(self.categories.keys())
	
	def __iter__(self):
		yield len(self.categories.values())
		yield from self.categories.values()

	def __getitem__(self, key):
		return self.categories[key]
	
	def __setitem__(self, key, value):
		self.categories[key] = value
	
	def __contains__(self, item:str):
		for l in self.categories.values():
			if l.name == item:
				return True
		return False

	def __str__(self):
		return f'LabelCombinaison : {", ".join([str(l) for l in self.categories.values()])}]'


if __name__ == '__main__':
	ref = LabelCategory('ref')
	ref.add_label('tutu', False)
	ref.add_label('titi', False)
	ref.add_label('tonton', False)
	ref.add_label('tyty', False)
	ref.add_label('tata', True)
	ref.add_label('toutou', False, valid_any=True)

	lc_in = LabelCategory('input')
	lc_in.add_label('tutu', True)
	lc_in.add_label('tata', True)

	print(ref.resolve(lc_in))

	combi = LabelCombinaison()

	combi['ref'] = ref
	combi['input'] = lc_in

	print(combi)