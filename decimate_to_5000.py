import bpy
import os
import glob
import operator

raw_models = glob.glob("/Users/zhjiang/Data/AdobeCharOBJs/*.obj")
print("Found")
print(raw_models)
for file in raw_models:
    beetle_path = file
    bpy.ops.wm.read_factory_settings()
    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)

    bpy.ops.import_scene.obj(filepath = beetle_path)

    mesh_object = [(o,len(o.data.polygons)) for o in bpy.data.objects if o.type=='MESH' ]
    #mesh_face_count = np.array([len(o.data.polygons) for o in mesh_object])
    object, f_n = max(mesh_object, key= operator.itemgetter(1))

    bpy.context.scene.objects.active = object

    if f_n > 5000:
        bpy.ops.object.modifier_add(type='DECIMATE')
        bpy.context.object.modifiers["Decimate"].use_collapse_triangulate = True
        bpy.context.object.modifiers["Decimate"].ratio = 4900 / f_n
        print('Modified: '+beetle_path)

    for o in scene.objects:
        if o != object:
            scene.objects.unlink(o)

    bpy.ops.export_scene.obj(filepath = beetle_path + '_deci.obj', use_triangles = True)

