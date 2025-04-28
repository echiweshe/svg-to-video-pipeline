# 15_render_farm_worker.py
"""
Render Farm Worker
Listens for rendering tasks and processes them.
"""

import redis
import json
import subprocess
import time
import os

class RenderFarmWorker:
    """Listens for rendering tasks and renders the Blender file."""

    def __init__(self, host="localhost", port=6379, task_channel="render_tasks", result_channel="render_results"):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.task_channel = task_channel
        self.result_channel = result_channel

    def render_blend_file(self, blend_file_path, output_video_path):
        """Invoke Blender to render a .blend file into a video."""
        blender_executable = "blender"  # Assumes blender is in PATH
        command = [
            blender_executable,
            "-b", blend_file_path,
            "-o", output_video_path,
            "-F", "FFMPEG",
            "-a"
        ]
        print(f"🎬 Starting render: {blend_file_path} -> {output_video_path}")
        subprocess.run(command, check=True)
        print(f"✅ Render completed: {output_video_path}")

    def listen_for_tasks(self):
        """Subscribe to tasks and process them."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.task_channel)
        print(f"👂 Listening for render tasks on channel: {self.task_channel}")

        for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    task = json.loads(message["data"])
                    blend_file = task["blend_file_path"]
                    output_video = task["output_video_path"]
                    self.render_blend_file(blend_file, output_video)
                    self.redis.publish(self.result_channel, f"✅ Successfully rendered {output_video}")
                except Exception as e:
                    self.redis.publish(self.result_channel, f"❌ Error: {str(e)}")

if __name__ == "__main__":
    worker = RenderFarmWorker()
    worker.listen_for_tasks()
