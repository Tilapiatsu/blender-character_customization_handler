import bpy
from .custo_properties import CustoProperty

class CustoObjectAttributesProperties(bpy.types.PropertyGroup, CustoProperty):
	name : bpy.props.StringProperty(name='Object Attribute Name', default='')
	
	@property
	def object(self):
		# from https://blender.stackexchange.com/questions/301937/accessing-the-parent-propertygroup-that-stores-another-propertygroup-pointer
		path = repr(self).rsplit(".", 1)[0]
		return eval(path)

	def materials(self, asset_type)->list:
		materials = []

		for m in bpy.data.materials:
			mesh_variations_labels = self.valid_mesh_variations(asset_type, self.object)
			materials_variations_labels = self.valid_mesh_variations(asset_type, m)

			if self.is_compatible_label_combinaison(mesh_variations_labels, materials_variations_labels):
				materials.append(m)

		return materials
	
	def valid_labels(self, data, include_label_category:list=None):
		valid_labels = {}
		for lc in data.custo_label_category_definition:
			if include_label_category is not None:
				if lc.name in include_label_category:
					valid_labels[lc.name] = self.valid_label_catgory_labels(data, lc)
			else:
				valid_labels[lc.name] = self.valid_label_catgory_labels(data, lc)

		return valid_labels
	
	def valid_mesh_variations(self, asset_type, data):
		mesh_variation_label_category = [lc.name for lc in asset_type.asset_type.mesh_variation_label_categories]
		mesh_variation_label_category += [lc.name for  lc in asset_type.asset_type.asset_label_categories]
		return self.valid_labels(data, include_label_category=mesh_variation_label_category)

	def valid_label_catgory_labels(self, data, category):
		return [l for l in data.custo_label_category_definition[category.name].labels if l.checked]

classes = (CustoObjectAttributesProperties, )

def register():
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)

	bpy.types.Object.custo_attributes = bpy.props.PointerProperty(type=CustoObjectAttributesProperties)
	

def unregister():

	del bpy.types.Object.custo_attributes
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)
	

if __name__ == "__main__":
	register()