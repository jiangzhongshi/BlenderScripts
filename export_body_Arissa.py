import bpy
import os
import glob
import operator

raw_models = glob.glob('/state/partition1/zj495/16_Arissa_out/*.obj')
result_path = '/state/partition1/zj495/16_Arissa_body/'
for file in raw_models:
    bpy.ops.wm.read_factory_settings()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    bpy.ops.import_scene.obj(filepath = file)

    mesh_object = [(o,len(o.data.polygons)) for o in bpy.data.objects if o.type=='MESH' ]
    #mesh_face_count = np.array([len(o.data.polygons) for o in mesh_object])
    #main_object, f_n = max(mesh_object, key= operator.itemgetter(1))
    bpy.ops.object.select_all(action='DESELECT')

    for ind, (main_object, f_n) in enumerate(mesh_object):
        bpy.context.scene.objects.active = main_object
        if ind > 0:
            break
        if f_n < 10:
            continue
        if f_n > 5000:
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
            bpy.context.object.modifiers["Decimate"].ratio = 4900 / f_n

        main_object.select = True
        # only select this obj and export it
        bpy.ops.export_scene.obj(filepath =result_path +  os.path.basename(file) + str(ind) + '.obj', use_triangles = True, use_selection=True, use_materials=False)
        main_object.select = False
    os.remove(file)

