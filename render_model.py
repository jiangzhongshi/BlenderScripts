bpy.data.worlds["World"].horizon_color = Color((1,1,1))

cam = bpy.data.objects['Camera']
origin = bpy.data.objects['Empty']

step_count = 32

for step in range(0, step_count):
    origin.rotation_euler[2] = radians(step * (360.0 / step_count))
    bpy.data.scenes["Scene"].render.filepath = '~/vr_shot_%d.jpg' % step
    bpy.ops.render.render(write_still=True)

