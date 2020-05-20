# BlenderScripts
Some python scripts I scratched with Blender

#
```python
# Replace linked object
import bpy
topobjs = [i for i in D.objects if 'top' in i.name]

for i in topobjs:
    bpy.ops.import_mesh.ply(filepath='/Users/zhongshi/Workspace/nutshell_data/abc_gallery/'+i.name+'.ply')
    imported = bpy.context.selected_objects[0]
    i.data = imported.data
    bpy.ops.object.select_all(action='DESELECT')
```

```python
# Assign material to object
mat = D.materials['name']
if ob.data.materials:
    # assign to 1st material slot
    ob.data.materials[0] = mat
else:
    # no slots
    ob.data.materials.append(mat)
```
