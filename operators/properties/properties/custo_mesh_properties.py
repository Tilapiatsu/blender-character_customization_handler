import bpy

class CustoMeshProperties(bpy.types.PropertyGroup):
	
	def is_valid(self, ob, variation:dict):
		valid = True
		
		for c,l in variation.items():
			if c not in ob.custo_label_category_definition.keys():
				valid = False
				break

			category = ob.custo_label_category_definition[c]

			if l not in category.labels.keys():
				valid = False
				break

			if not category.labels[l].checked:
				valid = False
				break


		return valid

classes = ( CustoMeshProperties, )

def register():
	
	from bpy.utils import register_class
	for cls in classes:
		register_class(cls)	

	bpy.types.Object.custo_mesh = bpy.props.PointerProperty(type=CustoMeshProperties)

def unregister():
	del bpy.types.Object.custo_mesh
	
	from bpy.utils import unregister_class
	for cls in reversed(classes):
		unregister_class(cls)	

if __name__ == "__main__":
	register()