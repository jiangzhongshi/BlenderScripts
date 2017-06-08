import bpy, os, sys
import numpy as np
import random

sys.path.insert(0, "/Users/zhjiang/Workspace/libigl/python")

import pyigl as igl
from iglhelpers import *

model_path = "/Users/zhjiang/Data/EuclidOBJs_tri/easterChocolateBunny_02.obj"

V = igl.eigen.MatrixXd()
F = igl.eigen.MatrixXi()
TC, CN, C = igl.eigen.MatrixXd(),igl.eigen.MatrixXd(),igl.eigen.MatrixXd()
FTC, FN = igl.eigen.MatrixXi(),igl.eigen.MatrixXi()
igl.readOBJ(model_path,V,TC,CN,F,FTC,FN)

Z = V.col(1)
# Compute per-vertex colors
igl.jet(Z, True, C)

# parsing data
lV = e2p(V).tolist()
lF = e2p(F).tolist()
lC = e2p(C).tolist()

# feed to blender
obj_mesh = bpy.data.meshes.new("Bunny_mesh")
obj_mesh.from_pydata(lV,[],lF)
obj_obj = bpy.data.objects.new("Bunny_obj", obj_mesh)

# link
scene = bpy.context.scene  # get current scene
scene.objects.link(obj_obj) # link new object to current scene

# color
obj_mat = bpy.data.materials.new('Jet Color')
obj_obj.active_material = obj_mat
obj_mat.use_vertex_color_paint = True


if not obj_mesh.vertex_colors:
    obj_mesh.vertex_colors.new()

# or you could avoid using the color_layer name
color_layer = obj_mesh.vertex_colors.active

i = 0
for poly in obj_mesh.polygons:
    for idx in poly.vertices:
        color_layer.data[i].color = lC[idx]
        i += 1

obj_obj.active_material.use_raytrace = False

bpy.data.objects["Lamp"].location = bpy.data.objects["Camera"].location

