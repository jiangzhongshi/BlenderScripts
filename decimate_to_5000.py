import bpy
import os
import glob
import operator
import sys
import shutil

argv = sys.argv
argv = argv[argv.index("--") + 1:]  # get all args after "--"

input_path = argv[0]
result_path = input_path + '_out'
exception_path = input_path + '_problem'

raw_models = [(os.path.getsize(f), f) for f in glob.iglob(input_path + '/*.[oO][bB][jJ]')]
raw_models.sort(key=lambda x:x[0], reverse=False) # Small to large

if not os.path.isdir(result_path):
    os.mkdir(result_path)
    os.mkdir(exception_path)

for _, input_model in raw_models:
    bpy.ops.wm.read_factory_settings()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath=input_model)

    mesh_object = [(o, len(o.data.polygons)) for o in bpy.data.objects if o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')

    for ind, (main_object, f_n) in enumerate(mesh_object):
        bpy.context.scene.objects.active = main_object
        if not main_object.data.uv_layers:
            continue
        if f_n < 10:
            continue
        if f_n > 5000:
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
            bpy.context.object.modifiers["Decimate"].ratio = 4900 / f_n

        main_object.select = True
        # only select this obj and export it
        bpy.ops.export_scene.obj(filepath=result_path +  os.path.basename(input_model) + str(ind)
                                 + '.obj', use_triangles=True, use_selection=True,
                                 use_materials=False)
        main_object.select = False
    os.remove(input_model)
