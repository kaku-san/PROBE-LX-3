# Regenerates the README renders from cad/PROBE-LX-3.blend (Blender 5.0, Cycles).
#
# Usage:
#   blender -b cad/PROBE-LX-3.blend --python tools/render_images.py -- <view> <out.png> [distance_factor] [samples]
#
# Views: hero, hero_lidar, internals, exploded, parts
# Suggested: hero 0.95 | hero_lidar 1.0 | internals 0.8 | exploded 1.0 | parts 1.25   (samples 128)

import bpy, sys, math
from mathutils import Vector
argv = sys.argv[sys.argv.index("--")+1:]
view, out = argv[0], argv[1]
sc = bpy.context.scene
print("UNITS", sc.unit_settings.system, sc.unit_settings.scale_length)

def mat(name, rgb, rough=0.45, metal=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m
M = {
 "DOME": mat("pla_dome", (0.80,0.81,0.83), 0.5),
 "BASE": mat("pla_base", (0.045,0.047,0.055), 0.55),
 "TRAY": mat("pla_tray", (0.30,0.12,0.55), 0.5),
 "PLATE": mat("pla_plate", (0.12,0.12,0.14), 0.55),
 "BRACKET": mat("pla_bracket", (0.30,0.12,0.55), 0.5),
 "ADAPTER": mat("pla_adapter", (0.30,0.12,0.55), 0.5),
}
def setmat(o, m):
    o.data.materials.clear(); o.data.materials.append(m)
parts = {"DOME | printable":"DOME","BASE | printable":"BASE","ELECTRONICS TRAY | printable":"TRAY",
         "DRIVE PLATE | printable":"PLATE","CAM BRACKET | printable":"BRACKET","LIDAR ADAPTER | printable":"ADAPTER"}
for n,k in parts.items(): setmat(bpy.data.objects[n], M[k])
rub=mat("rubber",(0.03,0.03,0.03),0.8); dflt=mat("dflt",(0.06,0.06,0.07),0.4)
for o in sc.objects:
    if o.type!="MESH" or o.name in parts: continue
    if "TIRE" in o.name: setmat(o,rub)
    elif o.name.startswith(("LIDAR |","B0385")) and "mounting plate" not in o.name: setmat(o,dflt)
    elif len(o.data.materials)==0 or all(m is None for m in o.data.materials): setmat(o,dflt)

# hide cutters, keepouts, placeholders, encoder parts
cut = bpy.data.collections["PRINT TOOLS (cutters)"]
for o in sc.objects:
    hide = (o.name in cut.all_objects) or o.name.startswith(("KEEPOUT","PLACEHOLDER")) or "Encoder" in o.name
    o.hide_render = hide or o.hide_render and o.name.startswith("MOTOR")
lidar = [o for o in sc.objects if o.name.startswith(("LIDAR |","RPLIDAR","LIDAR ADAPTER"))]
audio = [o for o in sc.objects if "WM8960" in o.name or "SPEAKER" in o.name or "8ohm" in o.name]
def show(objs, v):
    for o in objs: o.hide_render = not v
show(lidar, view in ("hero_lidar","parts"))
show(audio, False)
if view == "internals":
    show([o for o in sc.objects if o.name.startswith(("DOME","LOGO","B0385","VL53L1X","CAM BRACKET"))], False)

def group(n):
    if n.startswith(("DOME","CAM BRACKET","B0385","VL53L1X","LOGO","LIDAR","RPLIDAR")): return "dome"
    if n.startswith(("BONNET","ADAFRUIT")): return "bonnet"
    if n.startswith(("PI5",)): return "pi"
    if n.startswith(("X1200","GEEKWORM")): return "ups"
    if n.startswith(("ELECTRONICS TRAY","4AA")): return "tray"
    if n.startswith("BASE"): return "base"
    return "plate"
if view == "exploded":
    off = {"plate":0,"base":60,"tray":130,"ups":185,"pi":235,"bonnet":285,"dome":380}
    for o in sc.objects:
        if o.parent is None and not o.hide_render or (o.parent is None and o.type=="EMPTY"):
            o.location.z += off[group(o.name)]
if view == "parts":
    show([o for o in sc.objects], False)
    layout = {"DOME | printable":(-150,90,0),"BASE | printable":(150,90,0),"DRIVE PLATE | printable":(160,-150,0),
              "ELECTRONICS TRAY | printable":(-160,-150,0),"CAM BRACKET | printable":(-10,-80,0),"LIDAR ADAPTER | printable":(0,-190,0)}
    for n,(x,y,z) in layout.items():
        o = bpy.data.objects[n]; o.hide_render=False
        bb=[o.matrix_world @ Vector(c) for c in o.bound_box]
        cx=sum(v.x for v in bb)/8; cy=sum(v.y for v in bb)/8; mz=min(v.z for v in bb)
        o.location += Vector((x-cx, y-cy, -mz))

bpy.context.view_layer.update()
vis=[o for o in sc.objects if o.type=="MESH" and not o.hide_render]
pts=[o.matrix_world @ Vector(c) for o in vis for c in o.bound_box]
lo=Vector((min(p.x for p in pts),min(p.y for p in pts),min(p.z for p in pts)))
hi=Vector((max(p.x for p in pts),max(p.y for p in pts),max(p.z for p in pts)))
ctr=(lo+hi)/2; size=(hi-lo).length
print("BOUNDS",lo,hi)

# ground
bpy.ops.mesh.primitive_plane_add(size=size*20, location=(ctr.x,ctr.y,lo.z))
g=bpy.context.object; g.data.materials.append(mat("floor",(0.09,0.09,0.10),0.6))
# camera
cam_dirs={"hero":(-0.55,-1,0.42),"hero_lidar":(0.55,-1,0.45),"internals":(-0.5,-0.9,0.9),"exploded":(-0.6,-1,0.35),"parts":(0,-0.35,1)}
d=Vector(cam_dirs[view]).normalized()
cd=bpy.data.cameras.new("cam"); cd.lens=85; cd.clip_start=1; cd.clip_end=size*50
cam=bpy.data.objects.new("cam",cd); sc.collection.objects.link(cam); sc.camera=cam
fov=2*math.atan(cd.sensor_width/2/cd.lens)
dist=(size*0.5)/math.tan(fov/2)*float(argv[2]) if len(argv)>2 else (size*0.5)/math.tan(fov/2)*1.05
cam.location=ctr+d*dist
cam.rotation_euler=(ctr-cam.location).to_track_quat('-Z','Y').to_euler()
# lights
for rot,e,ang in [((math.radians(50),0,math.radians(-35)),3.2,8),((math.radians(65),0,math.radians(140)),1.4,20),((math.radians(75),0,math.radians(60)),0.9,30)]:
    ld=bpy.data.lights.new("sun","SUN"); ld.energy=e; ld.angle=math.radians(ang)
    lo_=bpy.data.objects.new("sun",ld); lo_.rotation_euler=rot; sc.collection.objects.link(lo_)
w=sc.world or bpy.data.worlds.new("w"); sc.world=w; w.use_nodes=True
bg=w.node_tree.nodes["Background"]; bg.inputs[0].default_value=(0.05,0.05,0.06,1); bg.inputs[1].default_value=0.6
sc.render.engine="CYCLES"; sc.cycles.samples=int(argv[3]) if len(argv)>3 else 96; sc.cycles.use_denoising=True
sc.view_settings.view_transform="AgX"; sc.view_settings.look="AgX - Medium High Contrast"
sc.render.resolution_x=1200 if view=="exploded" else 1600; sc.render.resolution_y=1500 if view=="exploded" else 1000; sc.render.resolution_percentage=100
sc.render.filepath=out; sc.render.image_settings.file_format="PNG"
bpy.ops.render.render(write_still=True)
