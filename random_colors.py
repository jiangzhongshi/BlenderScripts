import bpy
import random

# start in object mode
obj = bpy.data.objects["Cube"]
mesh = obj.data
mat = bpy.data.materials.new('material_1')
obj.active_material = mat
mat.use_vertex_color_paint = True

if not mesh.vertex_colors:
    mesh.vertex_colors.new()

"""
    let us assume for sake of brevity that there is now
    a vertex color map called  'Col'
"""

color_layer = mesh.vertex_colors["Col"]

# or you could avoid using the color_layer name
# color_layer = mesh.vertex_colors.active

i = 0
for poly in mesh.polygons:
    for idx in poly.loop_indices:
        rgb = [random.random() for i in range(3)]
        color_layer.data[i].color = rgb
        i += 1

# set to vertex paint mode to see the result
bpy.ops.object.mode_set(mode='VERTEX_PAINT')
