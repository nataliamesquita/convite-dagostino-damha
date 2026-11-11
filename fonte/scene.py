import bpy, math, sys, os
from mathutils import Vector
args = sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
MODE = args[0] if args else 'test'   # test | anim
FRAME = int(args[1]) if len(args)>1 else 60
HERE = os.path.dirname(os.path.abspath(__file__))

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def srgb(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda v: v/12.92 if v<=0.04045 else ((v+0.055)/1.055)**2.4
    return (f(c[0]),f(c[1]),f(c[2]),1)

def mat(name, col, rough=.5, metal=0, emit=None, es=0, coat=0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    b=m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value=srgb(col)
    b.inputs['Roughness'].default_value=rough
    b.inputs['Metallic'].default_value=metal
    if coat: b.inputs['Coat Weight'].default_value=coat; b.inputs['Coat Roughness'].default_value=.08
    if emit:
        b.inputs['Emission Color'].default_value=srgb(emit); b.inputs['Emission Strength'].default_value=es
    return m

def box(name, size, loc, m, bevel=0.0, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o=bpy.context.object; o.name=name; o.scale=size
    bpy.ops.object.transform_apply(scale=True)
    if bevel:
        mod=o.modifiers.new('bv','BEVEL'); mod.width=bevel; mod.segments=3
    o.data.materials.append(m)
    if parent: o.parent=parent
    return o

NAVY='#1C3C66'; INK='#0F2240'; CREAM='#F4EDE2'; OR='#E2700A'
m_wall=mat('wall',NAVY,.85)
m_trim=mat('trim',CREAM,.45)
m_door=mat('door',OR,.32,coat=.6)
m_brass=mat('brass','#D9A441',.22,metal=1)
m_floor=mat('floor','#14294A',.38)
m_inwall=mat('inwall','#C8742C',.9,emit='#E08A3A',es=.22)
m_bulb=mat('bulb','#FFF3DC',.5,emit='#FFE2B0',es=40)

W,H=1.6,2.3  # opening (porta dupla)
# wall in pieces around opening (wall face at y=0, thickness .2 towards +y)
T=.2
box('wl',(4,T,4.5),(-2-W/2,T/2,2.25),m_wall)
box('wr',(4,T,4.5),(2+W/2,T/2,2.25),m_wall)
box('wt',(W,T,4.5-H),(0,T/2,H+(4.5-H)/2),m_wall)
# reveal sides (inner jamb) trim colored
box('jl',(.03,T,H),(-W/2-.015,T/2,H/2),m_trim)
box('jr',(.03,T,H),(W/2+.015,T/2,H/2),m_trim)
box('jt',(W+.06,T,.03),(0,T/2,H+.015),m_trim)
# casing (front trim)
cw=.09
box('cl',(cw,.035,H+cw),(-W/2-cw/2,-.017,(H+cw)/2),m_trim,bevel=.006)
box('cr',(cw,.035,H+cw),(W/2+cw/2,-.017,(H+cw)/2),m_trim,bevel=.006)
box('ct',(W+2*cw,.042,cw),(0,-.019,H+cw/2+.001),m_trim,bevel=.006)
# floor
bpy.ops.mesh.primitive_plane_add(size=30,location=(0,0,0)); bpy.context.object.data.materials.append(m_floor)
# interior room
box('back',(6,.1,4),(0,3.4,2),m_inwall)
box('inL',(.1,3.4,4),(-2.0,1.8,2),m_inwall)
box('inR',(.1,3.4,4),(2.0,1.8,2),m_inwall)
bpy.ops.mesh.primitive_plane_add(size=1,location=(0,1.8,0.001)); bpy.context.object.scale=(4.0,3.2,1); bpy.context.object.data.materials.append(mat('infloor','#9E5A26',.35))
import random; random.seed(7)
m_shelf=mat('shelf','#F4EDE2',.6)
goods=[mat('g%d'%i,c,.5) for i,c in enumerate(['#24497A','#E2700A','#E98AA3','#F4EDE2','#3C7DC4','#F6A04D','#1C3C66'])]
for sx in (-0.75,0.75):
    box('side',(.03,.35,1.9),(sx-.55,3.0,.95),m_shelf); box('side',(.03,.35,1.9),(sx+.55,3.0,.95),m_shelf)
    for z in (.35,.8,1.25,1.7):
        box('sh',(1.1,.35,.025),(sx,3.0,z),m_shelf)
        x=sx-.5
        while x<sx+.45:
            w=random.uniform(.06,.16); h=random.uniform(.12,.34)
            box('g',(w,.2,h),(x+w/2,3.0,z+.0125+h/2),random.choice(goods),bevel=.006); x+=w+random.uniform(.01,.04)
# string lights (varal de lampadinhas)
m_wire=mat('wire','#2A2016',.6)
for (y,zc,sag) in ((0.55,2.18,.20),(1.6,2.35,.25)):
    n=22
    for i in range(n):
        x=-1.9+i*3.8/(n-1); z=zc-sag*(1-(x/1.9)**2)
        bpy.ops.mesh.primitive_uv_sphere_add(radius=.022,location=(x,y,z-.03)); bpy.context.object.data.materials.append(m_bulb)
# cocktail table with stretch cloth + champagne flutes
m_cloth=mat('cloth','#F7F2EA',.75)
bpy.ops.mesh.primitive_cone_add(vertices=48,radius1=.24,radius2=.21,depth=1.06,location=(0.48,1.45,.53)); bpy.context.object.data.materials.append(m_cloth)
bpy.ops.object.shade_smooth()
bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=.22,depth=.02,location=(0.48,1.45,1.07)); bpy.context.object.data.materials.append(m_cloth)
m_glass=bpy.data.materials.new('glass'); m_glass.use_nodes=True; gb=m_glass.node_tree.nodes['Principled BSDF']
gb.inputs['Transmission Weight'].default_value=1; gb.inputs['Roughness'].default_value=.02; gb.inputs['IOR'].default_value=1.45
m_champ=bpy.data.materials.new('champ'); m_champ.use_nodes=True; cb=m_champ.node_tree.nodes['Principled BSDF']
cb.inputs['Base Color'].default_value=srgb('#F2C04F'); cb.inputs['Transmission Weight'].default_value=.85; cb.inputs['Roughness'].default_value=.05
cb.inputs['Emission Color'].default_value=srgb('#F5B840'); cb.inputs['Emission Strength'].default_value=.6
for (fx,fy) in ((0.40,1.36),(0.52,1.32),(0.60,1.44),(0.45,1.52)):
    z0=1.08
    bpy.ops.mesh.primitive_cylinder_add(vertices=24,radius=.032,depth=.004,location=(fx,fy,z0+.002)); bpy.context.object.data.materials.append(m_glass)
    bpy.ops.mesh.primitive_cylinder_add(vertices=12,radius=.004,depth=.10,location=(fx,fy,z0+.05)); bpy.context.object.data.materials.append(m_glass)
    bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.006,radius2=.026,depth=.17,location=(fx,fy,z0+.10+.085),end_fill_type='NOTHING'); bpy.context.object.data.materials.append(m_glass); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_cone_add(vertices=24,radius1=.005,radius2=.021,depth=.12,location=(fx,fy,z0+.10+.065)); bpy.context.object.data.materials.append(m_champ); bpy.ops.object.shade_smooth()
# balloons (metallic, few)
m_bg=mat('bgold','#D9A441',.18,metal=1); m_bo=mat('borange','#E2700A',.2,coat=1); m_bc=mat('bcream','#F7F2EA',.25,coat=1); m_bn=mat('bnavy','#24497A',.2,coat=1)
for (bx,by,bz,m) in ((-0.62,2.0,1.62,m_bg),(-0.36,2.15,1.78,m_bo),(-0.58,2.3,1.98,m_bc),(0.62,2.4,1.85,m_bn),(0.40,2.55,2.02,m_bg)):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,radius=.16,location=(bx,by,bz)); o=bpy.context.object; o.scale=(1,1,1.18); bpy.ops.object.shade_smooth(); o.data.materials.append(m)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6,radius=.002,depth=bz-.19,location=(bx,by,(bz-.19)/2)); bpy.context.object.data.materials.append(m_wire)
# interior light
bpy.ops.object.light_add(type='AREA',location=(0,1.7,2.7)); L=bpy.context.object; L.data.size=3.2; L.data.color=(1,.62,.32)
L.rotation_euler=(math.radians(-55),0,0)
bpy.ops.object.light_add(type='POINT',location=(-.2,1.4,1.7)); P=bpy.context.object; P.data.color=(1,.62,.34); P.data.shadow_soft_size=.6

# Leo as image plane, feet on the floor
img=bpy.data.images.load(os.path.join(HERE,'leo.png'))
lw,lh=img.size; LH=1.05; LW=LH*lw/lh
bpy.ops.mesh.primitive_plane_add(size=1,location=(-0.12,0.86,LH/2-0.035),rotation=(math.radians(90),0,0))
leo=bpy.context.object; leo.scale=(LW,LH,1)
ml=bpy.data.materials.new('leo'); ml.use_nodes=True; nt=ml.node_tree; ns=nt.nodes; ns.clear()
out=ns.new('ShaderNodeOutputMaterial'); tex=ns.new('ShaderNodeTexImage'); tex.image=img
pb=ns.new('ShaderNodeBsdfPrincipled'); em=ns.new('ShaderNodeEmission'); em.inputs['Strength'].default_value=.38
add=ns.new('ShaderNodeAddShader'); tr=ns.new('ShaderNodeBsdfTransparent'); mix=ns.new('ShaderNodeMixShader')
nt.links.new(tex.outputs['Color'],pb.inputs['Base Color']); pb.inputs['Roughness'].default_value=.7
nt.links.new(tex.outputs['Color'],em.inputs['Color'])
nt.links.new(pb.outputs[0],add.inputs[0]); nt.links.new(em.outputs[0],add.inputs[1])
nt.links.new(tex.outputs['Alpha'],mix.inputs['Fac']); nt.links.new(tr.outputs[0],mix.inputs[1]); nt.links.new(add.outputs[0],mix.inputs[2])
nt.links.new(mix.outputs[0],out.inputs['Surface'])
leo.data.materials.append(ml)
leo.visible_shadow=False
# contact shadow under Leo's feet (soft ellipse)
bpy.ops.mesh.primitive_plane_add(size=1,location=(-0.07,0.90,0.003)); cs=bpy.context.object; cs.scale=(.62,.26,1)
mc=bpy.data.materials.new('cshadow'); mc.use_nodes=True; nt=mc.node_tree; ns=nt.nodes; ns.clear()
o2=ns.new('ShaderNodeOutputMaterial'); tc=ns.new('ShaderNodeTexCoord'); mp=ns.new('ShaderNodeMapping'); gr=ns.new('ShaderNodeTexGradient'); gr.gradient_type='SPHERICAL'
cr=ns.new('ShaderNodeValToRGB'); cr.color_ramp.elements[0].position=0.0; cr.color_ramp.elements[0].color=(1,1,1,1); cr.color_ramp.elements[1].position=.85; cr.color_ramp.elements[1].color=(.1,.1,.1,1)
mp.inputs['Location'].default_value=(-1,-1,0); mp.inputs['Scale'].default_value=(2,2,1)
bk=ns.new('ShaderNodeBsdfDiffuse'); bk.inputs['Color'].default_value=(.02,.01,.005,1); tr2=ns.new('ShaderNodeBsdfTransparent'); mx2=ns.new('ShaderNodeMixShader')
nt.links.new(tc.outputs['Generated'],mp.inputs['Vector']); nt.links.new(mp.outputs[0],gr.inputs['Vector'])
nt.links.new(gr.outputs['Fac'],cr.inputs['Fac'])
# fac: 0 at center -> transparent? we want dark center: use ramp output as transparency amount
nt.links.new(cr.outputs['Color'],mx2.inputs['Fac']); nt.links.new(tr2.outputs[0],mx2.inputs[2]); nt.links.new(bk.outputs[0],mx2.inputs[1])
nt.links.new(mx2.outputs[0],o2.inputs['Surface'])
cs.data.materials.append(mc)
# warm fill from the front on Leo and the table
bpy.ops.object.light_add(type='AREA',location=(0.2,-1.2,1.6)); F=bpy.context.object; F.data.size=1.2; F.data.energy=40; F.data.color=(1,.8,.6)
dd=Vector((-0.1,0.9,0.6))-F.location; F.rotation_euler=dd.to_track_quat('-Z','Y').to_euler()

# double doors, each built closed then joined with origin at its hinge; both swing INTO the room
def leaf(side):
    DW,DH,DT=W/2-.008,H-.02,.045
    x0=-W/2+.004 if side<0 else W/2-.004
    cxl=x0+DW/2 if side<0 else x0-DW/2
    parts=[]
    d=box('door',(DW,DT,DH),(cxl,T*.25,DH/2+.014),m_door,bevel=.004); parts.append(d)
    fy=T*.25-DT/2
    for zc,ph in ((DH*.70,DH*.40),(DH*.25,DH*.34)):
        parts.append(box('pan',(DW*.64,.014,ph),(cxl,fy-.006,zc),m_door,bevel=.008))
    hx=(x0+DW-.07) if side<0 else (x0-DW+.07)
    parts.append(box('pull',(.022,.03,.42),(hx,fy-.03,1.05),m_brass,bevel=.009))
    for o in parts:
        for m in o.modifiers:
            bpy.context.view_layer.objects.active=o; bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.ops.object.select_all(action='DESELECT')
    for o in parts: o.select_set(True)
    bpy.context.view_layer.objects.active=d; bpy.ops.object.join()
    ob=bpy.context.object
    sc.cursor.location=(x0,T*.25+DT/2,0); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    return ob
hinge=leaf(-1); hinge2=leaf(1)

# spot spilling light out through the doorway
bpy.ops.object.light_add(type='SPOT',location=(0.0,1.6,2.1)); S=bpy.context.object; S.data.spot_size=math.radians(80); S.data.spot_blend=.4; S.data.color=(1,.58,.26); S.data.shadow_soft_size=.15
dd=Vector((0.0,-1.6,0))-S.location; S.rotation_euler=dd.to_track_quat('-Z','Y').to_euler()
# glow leaking under the door
bpy.ops.mesh.primitive_plane_add(size=1,location=(0,.08,.0015)); g=bpy.context.object; g.scale=(W*.98,.12,1); g.data.materials.append(mat('leak','#FFB060',.5,emit='#FFB060',es=25))
# front soft key + rim so wall/door read
bpy.ops.object.light_add(type='AREA',location=(1.8,-3.5,3.2)); K=bpy.context.object; K.data.size=3; K.data.energy=90; K.data.color=(.82,.88,1)
K.rotation_euler=(math.radians(58),0,math.radians(28))

# world
w=bpy.data.worlds.new('w'); sc.world=w; w.use_nodes=True
w.node_tree.nodes['Background'].inputs[0].default_value=srgb(INK); w.node_tree.nodes['Background'].inputs[1].default_value=.15

# camera
bpy.ops.object.camera_add(location=(0.45,-5.6,1.3)); cam=bpy.context.object; sc.camera=cam
cam.data.lens=50
d=Vector((0.0,0.5,1.12))-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
cam.data.dof.use_dof=True; cam.data.dof.focus_distance=6.3; cam.data.dof.aperture_fstop=4

# animation
sc.frame_start=1; sc.frame_end=60; sc.render.fps=30
def key(f,ang,li,pi):
    hinge.rotation_euler=(0,0,math.radians(ang)); hinge.keyframe_insert('rotation_euler',frame=f)
    hinge2.rotation_euler=(0,0,math.radians(-ang)); hinge2.keyframe_insert('rotation_euler',frame=f)
    L.data.energy=li; L.data.keyframe_insert('energy',frame=f)
    S.data.energy=li*1.6; S.data.keyframe_insert('energy',frame=f)
    P.data.energy=pi; P.data.keyframe_insert('energy',frame=f)
key(1,0,120,20); key(10,2,140,25); key(52,86,300,60); key(60,87,300,60)
for fc in hinge.animation_data.action.layers[0].strips[0].channelbag(hinge.animation_data.action.slots[0]).fcurves if hasattr(hinge.animation_data.action,'layers') else hinge.animation_data.action.fcurves:
    for kp in fc.keyframe_points: kp.interpolation='BEZIER'; kp.easing='EASE_IN_OUT'

r=sc.render; r.engine='CYCLES'; sc.cycles.device='CPU'
sc.cycles.samples = 24 if MODE=='test' else 32
sc.cycles.use_denoising=True
sc.view_settings.view_transform='AgX'; sc.view_settings.look='AgX - Punchy'
r.resolution_x=640; r.resolution_y=800; r.resolution_percentage = 100 if MODE=='test' else 100
r.image_settings.file_format='PNG'
sc.cycles.max_bounces=6
if MODE=='test':
    sc.frame_set(FRAME); r.filepath=os.path.join(HERE,f'test_{FRAME}.png'); bpy.ops.render.render(write_still=True)
else:
    r.filepath=os.path.join(HERE,'frames2','f_'); bpy.ops.render.render(animation=True)
