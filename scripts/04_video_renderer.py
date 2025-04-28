# Video Renderer
# 04_video_renderer.py
"""
Video Renderer
Renders the animated Blender scene into a final video file.
"""

import bpy
import sys
import os

def setup_render_settings(output_path, resolution_x=1920, resolution_y=1080, fps=30):
    """Configure render settings for video output."""
    scene = bpy.context.scene
    scene.render.image_settings.file_format = 'FFMPEG'
    scene.render.ffmpeg.format = 'MPEG4'
    scene.render.ffmpeg.codec = 'H264'
    scene.render.ffmpeg.constant_rate_factor = 'HIGH'
    scene.render.ffmpeg.ffmpeg_preset = 'GOOD'
    scene.render.filepath = output_path
    
    scene.render.resolution_x = resolution_x
    scene.render.resolution_y = resolution_y
    scene.render.fps = fps

    print(f"✅ Render settings configured. Output: {output_path}")

def render_animation():
    """Render the animation to video."""
    bpy.ops.render.render(animation=True)
    print("✅ Rendering completed.")

def main(output_path, resolution_x=1920, resolution_y=1080, fps=30):
    if not output_path.lower().endswith(".mp4"):
        raise ValueError("Output path must end with .mp4")
    
    setup_render_settings(output_path, resolution_x, resolution_y, fps)
    render_animation()

if __name__ == "__main__":
    if "--" in sys.argv:
        idx = sys.argv.index("--")
        args = sys.argv[idx+1:]
        
        output_path = args[0] if len(args) > 0 else "outputs/output_video.mp4"
        resolution_x = int(args[1]) if len(args) > 1 else 1920
        resolution_y = int(args[2]) if len(args) > 2 else 1080
        fps = int(args[3]) if len(args) > 3 else 30
        
        main(output_path, resolution_x, resolution_y, fps)
    else:
        print("Usage: blender --background --python 04_video_renderer.py -- <output_path> [resolution_x resolution_y fps]")
