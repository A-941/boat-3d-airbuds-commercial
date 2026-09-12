import bpy
import math
import os
import random

def clean_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for block in bpy.data.meshes:
        bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        bpy.data.materials.remove(block)
    for block in bpy.data.lights:
        bpy.data.lights.remove(block)
    for block in bpy.data.cameras:
        bpy.data.cameras.remove(block)

def parent_to(child, parent):
    bpy.context.view_layer.update()
    child.parent = parent
    child.matrix_parent_inverse = parent.matrix_world.inverted()

def apply_smooth(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.shade_smooth()

# ==========================================
# HYPER-DETAILED SHADERS & LASER MATERIALS
# ==========================================
def create_shader(name, base_color=(0.1, 0.1, 0.1, 1.0), metallic=0.0, roughness=0.3,
                  emission_color=(0,0,0,1), emission_strength=0.0, transmission=0.0,
                  subsurface=0.0, ior=1.45):
    mat = bpy.data.materials.new(name=name)
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if not bsdf:
        return mat
    
    if 'Base Color' in bsdf.inputs:
        bsdf.inputs['Base Color'].default_value = base_color
    if 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = metallic
    if 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = roughness
    if 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = emission_color
    if 'Emission Strength' in bsdf.inputs:
        bsdf.inputs['Emission Strength'].default_value = emission_strength
    if 'Transmission Weight' in bsdf.inputs:
        bsdf.inputs['Transmission Weight'].default_value = transmission
    if 'Subsurface Weight' in bsdf.inputs:
        bsdf.inputs['Subsurface Weight'].default_value = subsurface
    if 'IOR' in bsdf.inputs:
        bsdf.inputs['IOR'].default_value = ior
        
    return mat

def create_all_materials():
    mats = {}
    # 1. Vibrant Metallic Ruby Crimson Red (Flagship boAt Red)
    mats['crimson_red'] = create_shader(
        'CrimsonRedMetallic',
        base_color=(0.88, 0.02, 0.06, 1.0),
        metallic=0.95,
        roughness=0.10
    )
    # 2. Velvet Carbon Matte Black
    mats['carbon_matte'] = create_shader(
        'CarbonMatteBlack',
        base_color=(0.018, 0.020, 0.024, 1.0),
        metallic=0.22,
        roughness=0.26
    )
    # 3. Smoked Crystal Acrylic (See-through lid & driver window)
    mats['smoked_crystal'] = create_shader(
        'SmokedCrystalAcrylic',
        base_color=(0.06, 0.07, 0.10, 1.0),
        metallic=0.05,
        roughness=0.05,
        transmission=0.88,
        ior=1.52
    )
    # 4. Internal Pure Copper Voice Coil (Luminous Amber Copper)
    mats['copper_coil'] = create_shader(
        'CopperVoiceCoil',
        base_color=(0.99, 0.44, 0.16, 1.0),
        metallic=1.0,
        roughness=0.12,
        emission_color=(1.0, 0.35, 0.08, 1.0),
        emission_strength=4.0
    )
    # 5. Neodymium Magnet Core (Mirror Silver Alloy)
    mats['magnet_core'] = create_shader(
        'NeodymiumMagnet',
        base_color=(0.82, 0.84, 0.88, 1.0),
        metallic=0.98,
        roughness=0.14
    )
    # 6. Graphene Acoustic Diaphragm Dome
    mats['diaphragm'] = create_shader(
        'GrapheneDiaphragm',
        base_color=(0.08, 0.09, 0.12, 1.0),
        metallic=0.85,
        roughness=0.18
    )
    # 7. Micro Circuit PCB
    mats['pcb_board'] = create_shader(
        'MicroCircuitPCB',
        base_color=(0.01, 0.05, 0.03, 1.0),
        metallic=0.6,
        roughness=0.22
    )
    # 8. 24K Mirror Gold (Bevels, Logo Badge, Contact Pins)
    mats['gold_mirror'] = create_shader(
        'MirrorGold24K',
        base_color=(1.0, 0.82, 0.22, 1.0),
        metallic=1.0,
        roughness=0.04
    )
    # 9. Gunmetal Titanium Hardware
    mats['titanium_gunmetal'] = create_shader(
        'TitaniumGunmetal',
        base_color=(0.32, 0.34, 0.38, 1.0),
        metallic=0.96,
        roughness=0.18
    )
    # 10. Translucent Ruby Silicone Ear Tip
    mats['silicone_ruby'] = create_shader(
        'SiliconeRuby',
        base_color=(0.45, 0.02, 0.07, 1.0),
        metallic=0.0,
        roughness=0.28,
        subsurface=0.55,
        transmission=0.50
    )
    # 11. Electric Neon Cyan Pulse LED
    mats['led_cyan'] = create_shader(
        'NeonCyanLED',
        base_color=(0.0, 0.95, 1.0, 1.0),
        emission_color=(0.0, 0.95, 1.0, 1.0),
        emission_strength=60.0
    )
    # 12. Neon Magenta Pulse LED
    mats['led_magenta'] = create_shader(
        'NeonMagentaLED',
        base_color=(1.0, 0.05, 0.85, 1.0),
        emission_color=(1.0, 0.05, 0.85, 1.0),
        emission_strength=55.0
    )
    # 13. Cyber Laser Scanning Beam
    mats['laser_grid'] = create_shader(
        'CyberLaserBeam',
        base_color=(0.0, 1.0, 0.85, 1.0),
        emission_color=(0.0, 1.0, 0.85, 1.0),
        emission_strength=90.0,
        transmission=0.7
    )
    # 14. Ground Impact Sonic Shockwave Ring
    mats['ground_shockwave'] = create_shader(
        'GroundImpactWave',
        base_color=(1.0, 0.15, 0.35, 1.0),
        emission_color=(1.0, 0.15, 0.35, 1.0),
        emission_strength=75.0,
        transmission=0.5
    )
    # 15. Sub-Bass Pulse Ring (Cyan)
    mats['air_shockwave_cyan'] = create_shader(
        'AirSonicPulseCyan',
        base_color=(0.0, 0.95, 1.0, 1.0),
        emission_color=(0.0, 0.95, 1.0, 1.0),
        emission_strength=80.0,
        transmission=0.6
    )
    # 16. Punch-Bass Pulse Ring (Magenta)
    mats['air_shockwave_magenta'] = create_shader(
        'AirSonicPulseMagenta',
        base_color=(1.0, 0.08, 0.75, 1.0),
        emission_color=(1.0, 0.08, 0.75, 1.0),
        emission_strength=80.0,
        transmission=0.6
    )
    # 17. Dark Obsidian Mirror Pedestal
    mats['studio_pedestal'] = create_shader(
        'ObsidianMirrorPedestal',
        base_color=(0.012, 0.015, 0.022, 1.0),
        metallic=0.82,
        roughness=0.08
    )
    # 18. Acoustic Mesh
    mats['acoustic_mesh'] = create_shader(
        'AcousticMesh',
        base_color=(0.18, 0.18, 0.20, 1.0),
        metallic=0.96,
        roughness=0.22
    )
    return mats

# ==========================================
# 3D HARDWARE MODELING (MULTI-LAYER EXPLODABLE)
# ==========================================
def build_earbud(name_prefix, mats, is_right=True):
    root = bpy.data.objects.new(f"{name_prefix}_Root", None)
    root.empty_display_type = 'ARROWS'
    root.empty_display_size = 0.50
    bpy.context.collection.objects.link(root)
    
    mirror_x = 1.0 if is_right else -1.0
    
    # Dedicated layer pivots for mid-air exploded anatomy view
    pivots = {}
    layer_names = ['tip', 'mesh', 'nozzle', 'diaphragm', 'coil', 'magnet', 'pcb', 'rear']
    for lname in layer_names:
        p = bpy.data.objects.new(f"{name_prefix}_Piv_{lname}", None)
        p.empty_display_type = 'PLAIN_AXES'
        p.empty_display_size = 0.15
        bpy.context.collection.objects.link(p)
        parent_to(p, root)
        pivots[lname] = p

    # Acoustic axis angle
    acoustic_rot = (math.radians(35), math.radians(-32 * mirror_x), math.radians(15))

    # 1. Rear Acoustic Shell (Parented to pivots['rear'])
    bpy.ops.mesh.primitive_uv_sphere_add(segments=36, ring_count=28, radius=0.40, location=(0, 0, 0))
    rear = bpy.context.active_object
    rear.name = f"{name_prefix}_RearPod"
    rear.scale = (0.92, 1.12, 0.88)
    rear.rotation_euler = (math.radians(-10), math.radians(15 * mirror_x), 0)
    apply_smooth(rear)
    rear.data.materials.append(mats['crimson_red'])
    parent_to(rear, pivots['rear'])
    
    # 2. Transparent Crystal Viewport Ring (Fixed to root)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.36, depth=0.12, vertices=36, location=(0.10 * mirror_x, 0.12, -0.02))
    window = bpy.context.active_object
    window.name = f"{name_prefix}_CrystalWindow"
    window.rotation_euler = acoustic_rot
    apply_smooth(window)
    window.data.materials.append(mats['smoked_crystal'])
    parent_to(window, root)
    
    # 3. 10mm Dynamic Bass Driver: Neodymium Ring Magnet (pivots['magnet'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.08, vertices=32, location=(0.12 * mirror_x, 0.14, -0.02))
    magnet = bpy.context.active_object
    magnet.name = f"{name_prefix}_DriverMagnet"
    magnet.rotation_euler = acoustic_rot
    apply_smooth(magnet)
    magnet.data.materials.append(mats['magnet_core'])
    parent_to(magnet, pivots['magnet'])
    
    # 4. Pure Copper Voice Coil Winding Ring (pivots['coil'])
    bpy.ops.mesh.primitive_torus_add(major_radius=0.18, minor_radius=0.045, major_segments=36, minor_segments=18,
                                     location=(0.14 * mirror_x, 0.16, -0.02))
    coil = bpy.context.active_object
    coil.name = f"{name_prefix}_CopperCoil"
    coil.rotation_euler = acoustic_rot
    apply_smooth(coil)
    coil.data.materials.append(mats['copper_coil'])
    parent_to(coil, pivots['coil'])
    
    # 5. Graphene Acoustic Diaphragm Dome (pivots['diaphragm'])
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.22, location=(0.18 * mirror_x, 0.19, -0.025))
    dome = bpy.context.active_object
    dome.name = f"{name_prefix}_DiaphragmDome"
    dome.scale = (1.0, 1.0, 0.32)
    dome.rotation_euler = acoustic_rot
    apply_smooth(dome)
    dome.data.materials.append(mats['diaphragm'])
    parent_to(dome, pivots['diaphragm'])

    # 6. Micro Circuit PCB (pivots['pcb'])
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.04 * mirror_x, -0.08, -0.22))
    pcb = bpy.context.active_object
    pcb.name = f"{name_prefix}_PCB"
    pcb.scale = (0.24, 0.12, 0.45)
    apply_smooth(pcb)
    pcb.data.materials.append(mats['pcb_board'])
    parent_to(pcb, pivots['pcb'])
    
    # 7. Titanium Front Nozzle Shell (pivots['nozzle'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.20, depth=0.28, vertices=32, location=(0.25 * mirror_x, 0.25, -0.03))
    nozzle = bpy.context.active_object
    nozzle.name = f"{name_prefix}_Nozzle"
    nozzle.rotation_euler = acoustic_rot
    apply_smooth(nozzle)
    nozzle.data.materials.append(mats['crimson_red'])
    parent_to(nozzle, pivots['nozzle'])
    
    # 8. Acoustic Gold Mesh & Bevel Ring (pivots['mesh'])
    bpy.ops.mesh.primitive_cylinder_add(radius=0.19, depth=0.03, vertices=32, location=(0.33 * mirror_x, 0.35, -0.10))
    grille = bpy.context.active_object
    grille.name = f"{name_prefix}_Grille"
    grille.rotation_euler = acoustic_rot
    apply_smooth(grille)
    grille.data.materials.append(mats['acoustic_mesh'])
    parent_to(grille, pivots['mesh'])
    
    bpy.ops.mesh.primitive_torus_add(major_radius=0.19, minor_radius=0.02, major_segments=32, minor_segments=12,
                                     location=(0.33 * mirror_x, 0.35, -0.10))
    gold_rim = bpy.context.active_object
    gold_rim.name = f"{name_prefix}_GoldRim"
    gold_rim.rotation_euler = acoustic_rot
    apply_smooth(gold_rim)
    gold_rim.data.materials.append(mats['gold_mirror'])
    parent_to(gold_rim, pivots['mesh'])
    
    # 9. Multi-Tier Ribbed Translucent Ruby Silicone Tip (pivots['tip'])
    bpy.ops.mesh.primitive_cone_add(radius1=0.34, radius2=0.20, depth=0.28, vertices=36, location=(0.36 * mirror_x, 0.39, -0.12))
    tip = bpy.context.active_object
    tip.name = f"{name_prefix}_SiliconeTip"
    tip.rotation_euler = acoustic_rot
    apply_smooth(tip)
    tip.data.materials.append(mats['silicone_ruby'])
    parent_to(tip, pivots['tip'])
    
    # 10. Velvet Carbon Stem (Fixed to root)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=1.35, vertices=32, location=(-0.13 * mirror_x, -0.19, -0.68))
    stem = bpy.context.active_object
    stem.name = f"{name_prefix}_Stem"
    stem.scale = (0.85, 1.08, 1.0)
    stem.rotation_euler = (math.radians(10), math.radians(-5 * mirror_x), math.radians(-8 * mirror_x))
    apply_smooth(stem)
    stem.data.materials.append(mats['carbon_matte'])
    parent_to(stem, root)
    
    # 11. 24K Gold Capacitive Touch Sensor
    bpy.ops.mesh.primitive_cylinder_add(radius=0.145, depth=0.15, vertices=32, location=(-0.14 * mirror_x, -0.27, -0.40))
    touch = bpy.context.active_object
    touch.name = f"{name_prefix}_TouchZone"
    touch.scale = (0.9, 0.35, 1.6)
    touch.rotation_euler = stem.rotation_euler
    apply_smooth(touch)
    touch.data.materials.append(mats['gold_mirror'])
    parent_to(touch, root)
    
    # 12. Neon Cyan LED Indicator
    bpy.ops.mesh.primitive_cylinder_add(radius=0.048, depth=0.20, vertices=24, location=(-0.145 * mirror_x, -0.305, -0.32))
    led = bpy.context.active_object
    led.name = f"{name_prefix}_LED"
    led.scale = (0.7, 0.25, 1.0)
    led.rotation_euler = stem.rotation_euler
    apply_smooth(led)
    led.data.materials.append(mats['led_cyan'])
    parent_to(led, root)
    
    # 13. Laser-Etched 24K Gold boAt Logo Badge on Stem
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.145 * mirror_x, -0.30, -0.72))
    badge = bpy.context.active_object
    badge.name = f"{name_prefix}_LogoBadge"
    badge.scale = (0.13, 0.02, 0.30)
    badge.rotation_euler = stem.rotation_euler
    apply_smooth(badge)
    badge.data.materials.append(mats['gold_mirror'])
    parent_to(badge, root)
    
    # 14. Golden Pogo Pins on Stem Base
    for p_i, p_off in enumerate([-0.045, 0.045]):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.035, depth=0.08, vertices=16, location=(-0.038 * mirror_x + p_off, -0.11, -1.30))
        pin = bpy.context.active_object
        pin.name = f"{name_prefix}_Pin_{p_i}"
        pin.data.materials.append(mats['gold_mirror'])
        parent_to(pin, root)
        
    return root, pivots

def build_charging_case(mats):
    case_root = bpy.data.objects.new("boAt_Case_Root", None)
    case_root.empty_display_type = 'ARROWS'
    case_root.empty_display_size = 0.65
    bpy.context.collection.objects.link(case_root)
    
    # 1. Lower Carbon Body
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.44))
    case_body = bpy.context.active_object
    case_body.name = "Case_LowerBody"
    case_body.scale = (2.3, 1.5, 0.85)
    mod_b = case_body.modifiers.new("Bevel", 'BEVEL')
    mod_b.width = 0.36
    mod_b.segments = 8
    apply_smooth(case_body)
    case_body.data.materials.append(mats['carbon_matte'])
    parent_to(case_body, case_root)
    
    # Crimson Racing Lip
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.0))
    rim = bpy.context.active_object
    rim.name = "Case_CrimsonRim"
    rim.scale = (2.32, 1.52, 0.07)
    mod_r = rim.modifiers.new("Bevel", 'BEVEL')
    mod_r.width = 0.08
    mod_r.segments = 4
    apply_smooth(rim)
    rim.data.materials.append(mats['crimson_red'])
    parent_to(rim, case_root)
    
    # Piano Black Docks
    for side, x_pos in [("L", -0.55), ("R", 0.55)]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.32, depth=0.42, vertices=32, location=(x_pos, 0.05, -0.16))
        well = bpy.context.active_object
        well.name = f"Dock_Well_{side}"
        well.data.materials.append(mats['carbon_matte'])
        parent_to(well, case_root)
        
        for p_i, p_off in enumerate([-0.045, 0.045]):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.032, depth=0.08, vertices=16, location=(x_pos + p_off, 0.05, -0.32))
            pin = bpy.context.active_object
            pin.data.materials.append(mats['gold_mirror'])
            parent_to(pin, case_root)

    # 5-Segment Dynamic Battery Equalizer HUD
    for i in range(5):
        x_led = -0.36 + (i * 0.18)
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_led, -0.76, -0.38))
        bar = bpy.context.active_object
        bar.name = f"HUD_Bar_{i+1}"
        bar.scale = (0.06, 0.02, 0.14)
        apply_smooth(bar)
        bar.data.materials.append(mats['led_cyan'] if i < 3 else mats['led_magenta'])
        parent_to(bar, case_root)

    # 2. Titanium Hinge Assembly
    lid_hinge = bpy.data.objects.new("Case_Hinge_Assembly", None)
    lid_hinge.location = (0, 0.74, 0.05)
    bpy.context.collection.objects.link(lid_hinge)
    parent_to(lid_hinge, case_root)
    
    bpy.ops.mesh.primitive_cylinder_add(radius=0.09, depth=1.6, vertices=32, location=(0, 0, 0))
    barrel = bpy.context.active_object
    barrel.name = "Hinge_Barrel"
    barrel.rotation_euler = (0, math.radians(90), 0)
    apply_smooth(barrel)
    barrel.data.materials.append(mats['titanium_gunmetal'])
    parent_to(barrel, lid_hinge)
    
    # 3. Translucent Smoked Crystal Lid
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.38))
    lid = bpy.context.active_object
    lid.name = "Case_CrystalLid"
    lid.scale = (2.3, 1.5, 0.74)
    mod_l = lid.modifiers.new("Bevel", 'BEVEL')
    mod_l.width = 0.36
    mod_l.segments = 8
    apply_smooth(lid)
    lid.data.materials.append(mats['smoked_crystal'])
    parent_to(lid, lid_hinge)
    
    # 24K Gold boAt Logo on Front Shell
    bpy.ops.object.text_add(location=(-0.40, -0.77, -0.22))
    case_logo = bpy.context.active_object
    case_logo.name = "Case_boAt_Logo"
    case_logo.data.body = "boAt"
    case_logo.data.size = 0.26
    case_logo.data.extrude = 0.015
    case_logo.data.bevel_depth = 0.003
    case_logo.rotation_euler = (math.radians(90), 0, 0)
    case_logo.data.materials.append(mats['gold_mirror'])
    parent_to(case_logo, case_root)
    
    return case_root, lid_hinge

def build_fx_elements(mats):
    # 1. Ground Impact Shockwave Ring
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.03, major_segments=64, minor_segments=16, location=(0, 0, -1.0))
    ground_wave = bpy.context.active_object
    ground_wave.name = "FX_GroundShockwave"
    apply_smooth(ground_wave)
    ground_wave.data.materials.append(mats['ground_shockwave'])
    
    # 2. Mid-Air Sonic Sub-Bass Pulse Ring (Cyan)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.025, major_segments=64, minor_segments=16, location=(0, -0.6, 1.2))
    air_wave_cyan = bpy.context.active_object
    air_wave_cyan.name = "FX_AirSonicWave_Cyan"
    air_wave_cyan.rotation_euler = (math.radians(90), 0, 0)
    apply_smooth(air_wave_cyan)
    air_wave_cyan.data.materials.append(mats['air_shockwave_cyan'])
    
    # 3. Mid-Air Sonic Punch Pulse Ring (Magenta)
    bpy.ops.mesh.primitive_torus_add(major_radius=0.1, minor_radius=0.025, major_segments=64, minor_segments=16, location=(0, -0.6, 1.2))
    air_wave_magenta = bpy.context.active_object
    air_wave_magenta.name = "FX_AirSonicWave_Magenta"
    air_wave_magenta.rotation_euler = (math.radians(90), 0, 0)
    apply_smooth(air_wave_magenta)
    air_wave_magenta.data.materials.append(mats['air_shockwave_magenta'])
    
    # 4. Cyber Laser Scanning Plane
    bpy.ops.mesh.primitive_plane_add(size=6.0, location=(0, -0.6, 1.2))
    laser = bpy.context.active_object
    laser.name = "FX_CyberLaserScan"
    laser.scale = (1.0, 0.008, 1.0)
    apply_smooth(laser)
    laser.data.materials.append(mats['laser_grid'])
    
    return ground_wave, air_wave_cyan, air_wave_magenta, laser

def build_studio_stage(mats):
    # Obsidian Pedestal
    bpy.ops.mesh.primitive_cylinder_add(radius=5.2, depth=0.25, vertices=64, location=(0, 0, -1.0))
    stage = bpy.context.active_object
    stage.name = "Studio_ObsidianPedestal"
    mod = stage.modifiers.new("Bevel", 'BEVEL')
    mod.width = 0.06
    mod.segments = 4
    apply_smooth(stage)
    stage.data.materials.append(mats['studio_pedestal'])
    
    # Neon Accent Rim
    bpy.ops.mesh.primitive_torus_add(major_radius=5.2, minor_radius=0.02, major_segments=64, minor_segments=12, location=(0, 0, -0.88))
    rim = bpy.context.active_object
    rim.name = "Pedestal_NeonRim"
    apply_smooth(rim)
    rim.data.materials.append(mats['led_cyan'])
    
    # Studio Floor
    bpy.ops.mesh.primitive_plane_add(size=50.0, location=(0, 0, -1.14))
    floor = bpy.context.active_object
    floor.name = "Studio_Floor"
    apply_smooth(floor)
    floor.data.materials.append(mats['studio_pedestal'])

# ==========================================
# CINEMATIC LIGHTING & CAMERA
# ==========================================
def setup_lighting():
    # Key Amber Light
    key_data = bpy.data.lights.new(name="Golden_Key_Light", type='AREA')
    key_data.energy = 2400.0
    key_data.size = 5.0
    key_data.size_y = 3.5
    key_data.color = (1.0, 0.88, 0.68)
    key_obj = bpy.data.objects.new("Golden_Key_Light", key_data)
    key_obj.location = (4.0, -4.5, 4.5)
    key_obj.rotation_euler = (math.radians(45), math.radians(10), math.radians(35))
    bpy.context.collection.objects.link(key_obj)
    
    # Rim Magenta Light
    rim_data = bpy.data.lights.new(name="Magenta_Rim_Light", type='AREA')
    rim_data.energy = 2800.0
    rim_data.size = 5.5
    rim_data.size_y = 3.0
    rim_data.color = (0.98, 0.10, 0.85)
    rim_obj = bpy.data.objects.new("Magenta_Rim_Light", rim_data)
    rim_obj.location = (-4.8, 4.0, 4.2)
    rim_obj.rotation_euler = (math.radians(-38), math.radians(-12), math.radians(-130))
    bpy.context.collection.objects.link(rim_obj)
    
    # Cyan Fill Spot
    fill_data = bpy.data.lights.new(name="Cyan_Fill_Spot", type='SPOT')
    fill_data.energy = 1800.0
    fill_data.spot_size = math.radians(50)
    fill_data.spot_blend = 0.4
    fill_data.color = (0.0, 0.95, 1.0)
    fill_obj = bpy.data.objects.new("Cyan_Fill_Spot", fill_data)
    fill_obj.location = (-3.2, -4.0, 3.5)
    fill_obj.rotation_euler = (math.radians(50), math.radians(-20), math.radians(-25))
    bpy.context.collection.objects.link(fill_obj)
    
    # Top Rim
    top_data = bpy.data.lights.new(name="Top_Rim_Light", type='AREA')
    top_data.energy = 1400.0
    top_data.size = 4.0
    top_data.color = (0.9, 0.95, 1.0)
    top_obj = bpy.data.objects.new("Top_Rim_Light", top_data)
    top_obj.location = (0, 0, 6.0)
    top_obj.rotation_euler = (0, 0, 0)
    bpy.context.collection.objects.link(top_obj)

def setup_camera():
    cam_data = bpy.data.cameras.new(name="Commercial_Director_Cam")
    cam_data.lens = 52.0
    cam_data.sensor_width = 36.0
    cam_data.clip_start = 0.05
    cam_data.clip_end = 100.0
    
    cam_obj = bpy.data.objects.new("Commercial_Director_Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    
    # Cinematic Tracking Target Empty
    cam_target = bpy.data.objects.new("Camera_LookTarget", None)
    cam_target.empty_display_type = 'SPHERE'
    cam_target.empty_display_size = 0.25
    bpy.context.collection.objects.link(cam_target)
    
    # Add Track To constraint
    track_con = cam_obj.constraints.new(type='TRACK_TO')
    track_con.target = cam_target
    track_con.track_axis = 'TRACK_NEGATIVE_Z'
    track_con.up_axis = 'UP_Y'
    
    return cam_obj, cam_target

# ==========================================
# 60 FPS HYPER-PHYSICS ANIMATION (360 FRAMES = 6.0 SECONDS)
# ==========================================
def animate_scene(case_root, lid_hinge, earbud_left, pivs_l, earbud_right, pivs_r,
                  ground_wave, air_wave_cyan, air_wave_magenta, laser, camera, cam_target):
    
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 360
    scene.render.fps = 60

    # -------------------------------------------------------------
    # PHASE 1: CASE DROP, KINETIC IMPACT SLAM & ELASTIC BOUNCE (Frames 1 - 45)
    # -------------------------------------------------------------
    # Gravitational fall from Z = 4.5m
    case_root.location = (0, 0, 4.5)
    case_root.rotation_euler = (math.radians(-14), math.radians(8), math.radians(-6))
    case_root.keyframe_insert(data_path="location", frame=1)
    case_root.keyframe_insert(data_path="rotation_euler", frame=1)
    
    # Slam onto pedestal at Frame 22 (High velocity impact!)
    case_root.location = (0, 0, -0.44)
    case_root.rotation_euler = (0, 0, 0)
    case_root.keyframe_insert(data_path="location", frame=22)
    case_root.keyframe_insert(data_path="rotation_euler", frame=22)
    
    # Elastic Rebound 1 (Frame 26): Bounces up 12cm with torque
    case_root.location = (0, 0, -0.32)
    case_root.rotation_euler = (math.radians(2.5), math.radians(-1.5), math.radians(1.0))
    case_root.keyframe_insert(data_path="location", frame=26)
    case_root.keyframe_insert(data_path="rotation_euler", frame=26)
    
    # Rebound Impact 2 (Frame 30)
    case_root.location = (0, 0, -0.44)
    case_root.rotation_euler = (0, 0, 0)
    case_root.keyframe_insert(data_path="location", frame=30)
    case_root.keyframe_insert(data_path="rotation_euler", frame=30)
    
    # Micro-settle (Frame 35)
    case_root.location = (0, 0, -0.42)
    case_root.keyframe_insert(data_path="location", frame=35)
    case_root.location = (0, 0, -0.44)
    case_root.keyframe_insert(data_path="location", frame=40)
    case_root.keyframe_insert(data_path="location", frame=360)

    # Ground Shockwave expands violently upon impact slam (Frames 22 - 50)
    ground_wave.scale = (0.01, 0.01, 0.01)
    ground_wave.keyframe_insert(data_path="scale", frame=1)
    ground_wave.keyframe_insert(data_path="scale", frame=21)
    ground_wave.scale = (6.5, 6.5, 0.8)
    ground_wave.keyframe_insert(data_path="scale", frame=46)
    ground_wave.scale = (0.01, 0.01, 0.01)
    ground_wave.keyframe_insert(data_path="scale", frame=50)

    # -------------------------------------------------------------
    # PHASE 2: PNEUMATIC SPRING LID BURST & HIGH-TORQUE EJECTION (Frames 30 - 85)
    # -------------------------------------------------------------
    # Lid snaps open with pneumatic damper rebound
    lid_hinge.rotation_euler = (0, 0, 0)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=1)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=32)
    
    # High-tension spring snaps lid back to -136° at Frame 54
    lid_hinge.rotation_euler = (math.radians(-136), 0, 0)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=54)
    
    # Mechanical hinge rebound bounce at Frame 64
    lid_hinge.rotation_euler = (math.radians(-120), 0, 0)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=64)
    
    # Settles wide open at Frame 75
    lid_hinge.rotation_euler = (math.radians(-130), 0, 0)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=75)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=310)
    
    # Smooth close for seamless loop (Frame 360)
    lid_hinge.rotation_euler = (0, 0, 0)
    lid_hinge.keyframe_insert(data_path="rotation_euler", frame=360)

    # --- EARBUDS ROCKET OUT OF DOCK WITH ANGULAR MOMENTUM ---
    dock_l = (-0.55, 0.05, 0.28)
    dock_r = (0.55, 0.05, 0.28)
    rot_dock_l = (math.radians(16), math.radians(-8), math.radians(10))
    rot_dock_r = (math.radians(16), math.radians(8), math.radians(-10))
    
    earbud_left.location = dock_l
    earbud_left.rotation_euler = rot_dock_l
    earbud_left.keyframe_insert(data_path="location", frame=1)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=1)
    earbud_left.keyframe_insert(data_path="location", frame=42)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=42)
    
    earbud_right.location = dock_r
    earbud_right.rotation_euler = rot_dock_r
    earbud_right.keyframe_insert(data_path="location", frame=1)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=1)
    earbud_right.keyframe_insert(data_path="location", frame=44)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=44)
    
    # Rocket upward into Zero-G Apex (Frame 85) with multi-axis tumble
    earbud_left.location = (-1.20, -0.40, 1.40)
    earbud_left.rotation_euler = (math.radians(45), math.radians(-240), math.radians(-110))
    earbud_left.keyframe_insert(data_path="location", frame=85)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=85)
    
    earbud_right.location = (1.20, -0.40, 1.40)
    earbud_right.rotation_euler = (math.radians(45), math.radians(240), math.radians(110))
    earbud_right.keyframe_insert(data_path="location", frame=85)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=85)

    # -------------------------------------------------------------
    # PHASE 3: BULLET-TIME MULTI-LAYER EXPLODED ANATOMY (Frames 90 - 145)
    # -------------------------------------------------------------
    # Cyber Laser Scanner Plane sweeps down from top to bottom
    laser.location = (0, -0.40, 2.6)
    laser.scale = (4.0, 0.008, 0.01)
    laser.keyframe_insert(data_path="location", frame=1)
    laser.keyframe_insert(data_path="scale", frame=1)
    laser.keyframe_insert(data_path="location", frame=90)
    laser.keyframe_insert(data_path="scale", frame=90)
    
    laser.location = (0, -0.40, 0.35)
    laser.scale = (4.0, 0.008, 0.01)
    laser.keyframe_insert(data_path="location", frame=135)
    laser.keyframe_insert(data_path="scale", frame=135)
    
    laser.scale = (0.01, 0.01, 0.01)
    laser.keyframe_insert(data_path="scale", frame=138)

    # Multi-Layer Exploded Anatomy: All components expand outward along acoustic vector!
    def animate_exploded_pivots(pivots, mirror):
        # Frame 1 and Frame 92: Zero offset (solid earbud)
        for p in pivots.values():
            p.location = (0, 0, 0)
            p.rotation_euler = (0, 0, 0)
            p.keyframe_insert(data_path="location", frame=1)
            p.keyframe_insert(data_path="rotation_euler", frame=1)
            p.keyframe_insert(data_path="location", frame=92)
            p.keyframe_insert(data_path="rotation_euler", frame=92)
        
        # Frame 120: Peak Exploded Deconstruction!
        pivots['tip'].location = (0.52 * mirror, 0.48, -0.16)
        pivots['tip'].keyframe_insert(data_path="location", frame=120)
        
        pivots['mesh'].location = (0.38 * mirror, 0.36, -0.12)
        pivots['mesh'].keyframe_insert(data_path="location", frame=120)
        
        pivots['nozzle'].location = (0.26 * mirror, 0.24, -0.08)
        pivots['nozzle'].keyframe_insert(data_path="location", frame=120)
        
        pivots['diaphragm'].location = (0.16 * mirror, 0.14, -0.04)
        pivots['diaphragm'].keyframe_insert(data_path="location", frame=120)
        
        # Pure Copper Voice Coil (Hovers & spins 720 degrees on its axis in zero-G!)
        pivots['coil'].location = (0.07 * mirror, 0.06, -0.01)
        pivots['coil'].rotation_euler = (0, 0, math.radians(720))
        pivots['coil'].keyframe_insert(data_path="location", frame=120)
        pivots['coil'].keyframe_insert(data_path="rotation_euler", frame=120)
        
        pivots['magnet'].location = (-0.02 * mirror, -0.02, 0.0)
        pivots['magnet'].keyframe_insert(data_path="location", frame=120)
        
        pivots['pcb'].location = (-0.18 * mirror, -0.14, -0.26)
        pivots['pcb'].keyframe_insert(data_path="location", frame=120)
        
        pivots['rear'].location = (-0.22 * mirror, -0.18, 0.12)
        pivots['rear'].keyframe_insert(data_path="location", frame=120)

        # Frame 142: High-speed electromagnetic SNAP back together!
        for p in pivots.values():
            p.location = (0, 0, 0)
            p.rotation_euler = (0, 0, 0)
            p.keyframe_insert(data_path="location", frame=142)
            p.keyframe_insert(data_path="rotation_euler", frame=142)

    animate_exploded_pivots(pivs_l, mirror=-1.0)
    animate_exploded_pivots(pivs_r, mirror=1.0)

    # -------------------------------------------------------------
    # PHASE 4: DUAL ACOUSTIC SHOCKWAVES & DOUBLE-HELIX DOGFIGHT (Frames 145 - 235)
    # -------------------------------------------------------------
    # Earbuds face each other in center at Frame 148
    earbud_left.location = (-0.68, -0.55, 1.25)
    earbud_left.rotation_euler = (0, math.radians(90), 0)
    earbud_left.keyframe_insert(data_path="location", frame=148)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=148)
    
    earbud_right.location = (0.68, -0.55, 1.25)
    earbud_right.rotation_euler = (0, math.radians(-90), 0)
    earbud_right.keyframe_insert(data_path="location", frame=148)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=148)

    # Dual Concentric Soundwave Shockwaves (Cyan Sub-Bass & Magenta Punch)
    air_wave_cyan.scale = (0.01, 0.01, 0.01)
    air_wave_cyan.keyframe_insert(data_path="scale", frame=1)
    air_wave_cyan.keyframe_insert(data_path="scale", frame=148)
    air_wave_cyan.scale = (9.5, 9.5, 9.5)
    air_wave_cyan.keyframe_insert(data_path="scale", frame=176)
    air_wave_cyan.scale = (0.01, 0.01, 0.01)
    air_wave_cyan.keyframe_insert(data_path="scale", frame=179)
    
    air_wave_magenta.scale = (0.01, 0.01, 0.01)
    air_wave_magenta.keyframe_insert(data_path="scale", frame=1)
    air_wave_magenta.keyframe_insert(data_path="scale", frame=158)
    air_wave_magenta.scale = (8.0, 8.0, 8.0)
    air_wave_magenta.keyframe_insert(data_path="scale", frame=186)
    air_wave_magenta.scale = (0.01, 0.01, 0.01)
    air_wave_magenta.keyframe_insert(data_path="scale", frame=189)

    # --- DOUBLE-HELIX DOGFIGHT KINETIC CORKSCREW (Frames 155 - 235) ---
    earbud_left.location = (0.50, -0.95, 1.55)
    earbud_left.rotation_euler = (math.radians(50), math.radians(310), math.radians(-70))
    earbud_left.keyframe_insert(data_path="location", frame=185)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=185)
    
    earbud_left.location = (0.95, -0.40, 0.95)
    earbud_left.rotation_euler = (math.radians(20), math.radians(450), math.radians(40))
    earbud_left.keyframe_insert(data_path="location", frame=210)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=210)
    
    earbud_right.location = (-0.50, -0.30, 0.85)
    earbud_right.rotation_euler = (math.radians(-50), math.radians(-310), math.radians(70))
    earbud_right.keyframe_insert(data_path="location", frame=185)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=185)
    
    earbud_right.location = (-0.95, -0.40, 1.45)
    earbud_right.rotation_euler = (math.radians(-20), math.radians(-450), math.radians(-40))
    earbud_right.keyframe_insert(data_path="location", frame=210)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=210)

    # -------------------------------------------------------------
    # PHASE 5: GRAND HERO PRESENTATION (PERFECT CENTER DUO) (Frames 240 - 360)
    # -------------------------------------------------------------
    # Brake hard with aerodynamic tilt into Grand Hero Climax (Frame 245)
    # Positioned symmetrically at X = -0.78 and +0.78, Z = 0.88, angled 3/4 profile facing camera!
    earbud_left.location = (-0.78, -0.45, 0.88)
    earbud_left.rotation_euler = (math.radians(12), math.radians(-15), math.radians(-55))
    earbud_left.keyframe_insert(data_path="location", frame=245)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=245)
    
    earbud_right.location = (0.78, -0.45, 0.88)
    earbud_right.rotation_euler = (math.radians(12), math.radians(15), math.radians(55))
    earbud_right.keyframe_insert(data_path="location", frame=245)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=245)

    # Subtle anti-gravity hovering bob (Frame 285)
    earbud_left.location = (-0.76, -0.42, 0.92)
    earbud_left.rotation_euler = (math.radians(10), math.radians(-12), math.radians(-52))
    earbud_left.keyframe_insert(data_path="location", frame=285)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=285)
    
    earbud_right.location = (0.76, -0.42, 0.92)
    earbud_right.rotation_euler = (math.radians(10), math.radians(12), math.radians(52))
    earbud_right.keyframe_insert(data_path="location", frame=285)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=285)

    # Return to dock for seamless infinite loop (Frame 360)
    earbud_left.location = dock_l
    earbud_left.rotation_euler = rot_dock_l
    earbud_left.keyframe_insert(data_path="location", frame=360)
    earbud_left.keyframe_insert(data_path="rotation_euler", frame=360)
    
    earbud_right.location = dock_r
    earbud_right.rotation_euler = rot_dock_r
    earbud_right.keyframe_insert(data_path="location", frame=360)
    earbud_right.keyframe_insert(data_path="rotation_euler", frame=360)

    # -------------------------------------------------------------
    # CINEMATIC DIRECTOR CAMERA TRACKING WITH LOOK TARGET
    # -------------------------------------------------------------
    # 1. Look Target animation
    # Frame 1: Case center
    cam_target.location = (0, 0, 0)
    cam_target.keyframe_insert(data_path="location", frame=1)
    
    # Frame 22: Impact slam
    cam_target.location = (0, 0, -0.44)
    cam_target.keyframe_insert(data_path="location", frame=22)
    
    # Frame 45: Launching earbuds
    cam_target.location = (0, 0, 0.2)
    cam_target.keyframe_insert(data_path="location", frame=45)
    
    # Frame 85: Zero-G apex
    cam_target.location = (0, -0.4, 1.4)
    cam_target.keyframe_insert(data_path="location", frame=85)
    
    # Frame 120: Exploded Tech Reveal Center (Locked onto Left Earbud Exploded Assembly!)
    cam_target.location = (-1.20, -0.20, 1.30)
    cam_target.keyframe_insert(data_path="location", frame=120)
    
    # Frame 160: Sonic shockwaves center
    cam_target.location = (0, -0.5, 1.25)
    cam_target.keyframe_insert(data_path="location", frame=160)
    
    # Frame 245: Duo Hero Climax Center (Perfect center of both earbuds and open case)
    cam_target.location = (0, -0.35, 0.45)
    cam_target.keyframe_insert(data_path="location", frame=245)
    
    # Frame 360: Return to start
    cam_target.location = (0, 0, 0)
    cam_target.keyframe_insert(data_path="location", frame=360)

    # 2. Camera Location animation
    # Frame 1: High wide overview
    camera.location = (0, -6.8, 3.2)
    camera.keyframe_insert(data_path="location", frame=1)
    
    # Frame 22: Impact Cam-Shake Recoil! (Handheld shockwave jerk)
    camera.location = (0.10, -5.6, 1.4)
    camera.keyframe_insert(data_path="location", frame=22)
    
    # Frame 26: Cam-Shake Rebound
    camera.location = (-0.08, -5.8, 1.65)
    camera.keyframe_insert(data_path="location", frame=26)
    
    # Frame 85: Low-Angle Rocket Sweep
    camera.location = (0.8, -4.8, 1.4)
    camera.keyframe_insert(data_path="location", frame=85)
    
    # Frame 120: Macro Exploded View Framing
    camera.location = (-1.20, -4.6, 1.40)
    camera.keyframe_insert(data_path="location", frame=120)
    
    # Frame 160: Rapid Whip-Pan for Sonic Shockwaves
    camera.location = (0, -5.4, 1.8)
    camera.keyframe_insert(data_path="location", frame=160)
    
    # Frame 245: Perfect Hero Lock (Frames both earbuds and open case cleanly!)
    camera.location = (0, -4.6, 0.90)
    camera.keyframe_insert(data_path="location", frame=245)
    
    # Frame 360: Return to wide start for seamless loop
    camera.location = (0, -6.8, 3.2)
    camera.keyframe_insert(data_path="location", frame=360)

    # Bezier interpolation across all curves
    def set_bezier(obj):
        if not obj.animation_data or not obj.animation_data.action:
            return
        act = obj.animation_data.action
        fcurves = []
        if hasattr(act, "fcurves"):
            fcurves = list(act.fcurves)
        elif hasattr(act, "layers"):
            for layer in act.layers:
                for strip in getattr(layer, "strips", []):
                    for cb in getattr(strip, "channelbags", []):
                        for fc in getattr(cb, "fcurves", []):
                            fcurves.append(fc)
        for fc in fcurves:
            for kp in getattr(fc, "keyframe_points", []):
                kp.interpolation = 'BEZIER'

    all_objs = [case_root, lid_hinge, earbud_left, earbud_right,
                ground_wave, air_wave_cyan, air_wave_magenta, laser, camera, cam_target]
    for p in list(pivs_l.values()) + list(pivs_r.values()):
        all_objs.append(p)
    for obj in all_objs:
        set_bezier(obj)

# ==========================================
# RENDER CONFIGURATION & MAIN
# ==========================================
def configure_render():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.fps = 60
    
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 16
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = True
            scene.eevee.motion_blur_shutter = 0.5
    
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("StudioWorld")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.010, 0.012, 0.018, 1.0)
        bg_node.inputs['Strength'].default_value = 0.85

def embed_auto_play_script():
    auto_script = bpy.data.texts.new("auto_play.py")
    auto_script.write("""import bpy

def on_load():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        space.region_3d.view_perspective = 'CAMERA'
    try:
        if not bpy.context.screen.is_animation_playing:
            bpy.ops.screen.animation_play()
    except Exception:
        pass
    return None

bpy.app.timers.register(on_load, first_interval=0.5)
""")
    auto_script.use_module = True

def main():
    print(">>> Initializing 60 FPS Hyper-Physics boAt Commercial (360 Frames)...", flush=True)
    clean_scene()
    
    script_dir = "C:/Users/makwana dhruv suresh/OneDrive/Desktop/3D"
    renders_dir = os.path.join(script_dir, "renders")
    os.makedirs(renders_dir, exist_ok=True)
    
    # 1. Shaders
    mats = create_all_materials()
    
    # 2. Hardware Models & Multi-Layer Pivots
    case_root, lid_hinge = build_charging_case(mats)
    earbud_left, pivs_l = build_earbud("boAt_Earbud_L", mats, is_right=False)
    earbud_right, pivs_r = build_earbud("boAt_Earbud_R", mats, is_right=True)
    ground_wave, air_wave_cyan, air_wave_magenta, laser = build_fx_elements(mats)
    build_studio_stage(mats)
    
    # 3. Cinematic Lighting & Camera with Target Tracking
    setup_lighting()
    camera, cam_target = setup_camera()
    
    # 4. 60 FPS Hyper-Physics Animation Choreography
    animate_scene(case_root, lid_hinge, earbud_left, pivs_l, earbud_right, pivs_r,
                  ground_wave, air_wave_cyan, air_wave_magenta, laser, camera, cam_target)
    
    # 5. Configure Render Engine
    configure_render()
    embed_auto_play_script()
    
    # 6. Save Master Blender File
    blend_path = os.path.join(script_dir, "boat_earbuds.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f">>> Successfully saved 60 FPS Master Scene: {blend_path}", flush=True)
    
    # 7. Render Hero Still (Frame 245: Grand Hero Climax Duo)
    bpy.context.scene.frame_set(245)
    still_path = os.path.join(renders_dir, "boat_earbuds_hero.png")
    bpy.context.scene.render.filepath = still_path
    bpy.context.scene.render.image_settings.media_type = 'IMAGE'
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    print(f">>> Rendering High-Resolution Hero Still to: {still_path}", flush=True)
    bpy.ops.render.render(write_still=True)
    print(">>> Hero Still Render Complete!", flush=True)

if __name__ == "__main__":
    main()
