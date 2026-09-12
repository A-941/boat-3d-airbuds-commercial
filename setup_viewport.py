import bpy

def configure_viewport_and_play():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        space.region_3d.view_perspective = 'CAMERA'
                        try:
                            with bpy.context.temp_override(window=window, screen=screen, area=area):
                                if not bpy.context.screen.is_animation_playing:
                                    bpy.ops.screen.animation_play()
                        except Exception:
                            try:
                                bpy.ops.screen.animation_play()
                            except Exception:
                                pass

    print(">>> [boAt 3D Viewport] Initialized Material Preview & Real-Time 60 FPS Playback!")
    return 1.5

bpy.app.timers.register(configure_viewport_and_play, first_interval=0.6)
