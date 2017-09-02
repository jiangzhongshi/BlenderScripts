import bpy
import os
import glob
import operator

raw_models = glob.glob(os.path.expanduser('~/Desktop/*.obj'))
print("Found")
print(raw_models)
for file in raw_models:
    input_model_path = file
    bpy.ops.wm.read_factory_settings()
    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)

    bpy.ops.import_scene.obj(filepath = input_model_path)

    mesh_object = [(o,len(o.data.polygons)) for o in bpy.data.objects if o.type=='MESH' ]
    #mesh_face_count = np.array([len(o.data.polygons) for o in mesh_object])
    #main_object, f_n = max(mesh_object, key= operator.itemgetter(1))
    bpy.ops.object.select_all(action='DESELECT')

    for ind, (main_object, f_n) in enumerate(mesh_object):
        bpy.context.scene.objects.active = main_object
        if f_n < 10:
            continue
        if f_n > 5000:
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
            bpy.context.object.modifiers["Decimate"].ratio = 4900 / f_n
            print('Modified: '+input_model_path)

        main_object.select = True
        # only select this obj and export it
        bpy.ops.export_scene.obj(filepath = input_model_path + str(ind) + '.obj', use_triangles = True, use_selection=True, use_materials=False)
        main_object.select = False

