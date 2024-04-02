from dataclasses import dataclass, field

@dataclass
class FloatOveride():
	value : float = 0.0

	

@dataclass
class PropertyOverride():
	properties : dict = field(default_factory=dict)
	
