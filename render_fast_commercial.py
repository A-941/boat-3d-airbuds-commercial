import bpy
import os
import subprocess

def render_commercial():
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 360
    scene.render.fps = 60
    
    # Fast crisp 720p render for rapid commercial preview
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    
    if hasattr(scene, "eevee"):
        if hasattr(scene.eevee, "taa_render_samples"):
            scene.eevee.taa_render_samples = 4
        if hasattr(scene.eevee, "use_motion_blur"):
            scene.eevee.use_motion_blur = True
            scene.eevee.motion_blur_shutter = 0.5
            
    tmp_dir = "C:/tmp/boat_frames"
    os.makedirs(tmp_dir, exist_ok=True)
    
    scene.render.filepath = os.path.join(tmp_dir, "frame_")
    scene.render.image_settings.media_type = 'IMAGE'
    scene.render.image_settings.file_format = 'PNG'
    
    print(">>> Rendering 360 Frames at 60 FPS...", flush=True)
    bpy.ops.render.render(animation=True)
    print(">>> Frame sequence complete! Encoding MP4 with FFmpeg...", flush=True)
    
    mp4_out = "C:/Users/makwana dhruv suresh/OneDrive/Desktop/3D/renders/boat_earbuds_commercial.mp4"
    ffmpeg_exe = "C:/ffmpeg/bin/ffmpeg.exe"
    
    cmd = [
        ffmpeg_exe,
        "-y",
        "-framerate", "60",
        "-i", os.path.join(tmp_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "veryfast",
        mp4_out
    ]
    subprocess.run(cmd, check=True)
    print(f">>> Commercial video successfully saved: {mp4_out}", flush=True)

if __name__ == "__main__":
    render_commercial()
