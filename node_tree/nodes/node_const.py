from mathutils import Color

SPAWN_COLOR = Color((0.0,0.3,0.0))
INVALID_COLOR = Color((0.1, 0.1, 0.1))
NODE_ATTRIBUTE_TARGET_ITEMS = [('ALL', 'All', ''), ('MESHES', 'Meshes', ''), ('MATERIALS', 'Materials', '')]
NDOE_ATTRIBUTE_TARGETS = [i[0] for i in NODE_ATTRIBUTE_TARGET_ITEMS if i != 'ALL']