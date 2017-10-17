import bpy
import os
import sys
import glob
import tarfile
import shutil
import random

argv = sys.argv[sys.argv.index("--") + 1:]
input_model_dir = '/mnt/ilcompf8d0/user/zhjiang/MixamoChars/'+argv[0]+'/'
skin_dir ='/mnt/ilcompf8d0/user/zhjiang/skin_pick/' +argv[0]+'.fbx'
out_model_path ='/mnt/ilcompf8d0/user/zhjiang/MixamoOut/' + argv[0] + '/'

def crop_timeline_to_action():
    # check if actions is empty
    assert bpy.data.actions, 'no_actions'
    # get all actions
    act = bpy.data.actions[0]
    keys = act.frame_range
    scn = bpy.context.scene
    # assign new starting frame
    scn.frame_start = keys[0]
    # assign new end frame
    scn.frame_end = keys[1]

def restore_empty():
    bpy.ops.wm.read_factory_settings()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def process_single_arma_fbx(fbx_file):
    pose_name = os.path.splitext(fbx_file)[0]
    output_dir = out_model_path +'/out_' +  pose_name + '/'
    if os.path.isfile(output_dir[:-1]+'.tar.gz') or os.path.isdir(output_dir):
        return
    bpy.ops.import_scene.fbx(filepath=input_model_dir + fbx_file)
    current_armatures = [m for m in bpy.data.objects if m.type=='ARMATURE' and m != base_arm]
    curr_arm = current_armatures[0]
    bpy.ops.object.select_all(action='SELECT')
    base_arm.select = False
    bpy.context.scene.objects.active = curr_arm
    bpy.ops.object.parent_set(type='ARMATURE')

    crop_timeline_to_action()

    if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    bpy.ops.export_scene.obj(filepath = output_dir + pose_name + '.obj', check_existing=False, use_animation=True, use_materials=False, use_triangles=True)

    bpy.ops.object.select_all(action='DESELECT')
    curr_arm.select = True
    bpy.ops.object.delete()

    act = bpy.data.actions[0]
    act.user_clear()
    bpy.data.actions.remove(act)
    #os.remove(input_model_dir + fbx_file)
    with tarfile.open(output_dir[:-1]+'.tar.gz','w:gz') as tar:
        tar.add(output_dir, arcname=os.path.basename(output_dir))
    shutil.rmtree(output_dir)

if __name__ == '__main__':
    skin_fbx = skin_dir

    restore_empty()
    bpy.ops.import_scene.fbx(filepath=skin_fbx)

    base_meshes = [m for m in bpy.data.objects if m.type=='MESH']
    base_armatures = [m for m in bpy.data.objects if m.type=='ARMATURE']
    assert len(base_armatures) == 1, "Multiple Base Armature Exists"

    base_arm = base_armatures[0]

    bpy.ops.object.select_all(action='DESELECT')
    for m in base_meshes:
        m.select = True
    base_arm.select = True
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

    poses = random.sample([os.path.split(p)[1] for p in glob.glob(input_model_dir+'*.fbx')], 50)
    for p in poses:
        if p == 'skin.fbx':
                continue
        process_single_arma_fbx(p)
