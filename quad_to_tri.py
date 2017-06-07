import bpy, os

quad_models = os.listdir("./quads")
print("Found")
print(quad_models)

for file in quad_models:
    beetle_path = file
    for scene in bpy.data.scenes:
        for obj in scene.objects:
            scene.objects.unlink(obj)
    if os.path.splitext(file)[-1].lower() == ".obj":
        print(file+" Gogogo")
    else:
        continue

    #beetle_path = "/Users/zhongshi/Desktop/quads/beetle_tri-remeshed.obj"
    bpy.ops.import_scene.obj(filepath = "./quads/"+ beetle_path)

    bpy.ops.export_scene.obj(filepath = "./tris/" + beetle_path, use_triangles = True)
