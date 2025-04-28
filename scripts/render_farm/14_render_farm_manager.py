# Render Farm Manager
# 14_render_farm_manager.py
"""
Render Farm Manager
Manages and distributes rendering tasks to available workers via Redis.
"""

import redis
import time
import json

class RenderFarmManager:
    """Distributes rendering tasks to workers."""

    def __init__(self, host="localhost", port=6379, task_channel="render_tasks", result_channel="render_results"):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)
        self.task_channel = task_channel
        self.result_channel = result_channel

    def dispatch_task(self, blend_file_path, output_video_path):
        """Send a new rendering task to the farm."""
        task = {
            "blend_file_path": blend_file_path,
            "output_video_path": output_video_path
        }
        self.redis.publish(self.task_channel, json.dumps(task))
        print(f"🚀 Dispatched rendering task: {task}")

    def listen_for_results(self):
        """Listen for results from workers."""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(self.result_channel)
        print(f"👂 Listening for render results on channel: {self.result_channel}")

        for message in pubsub.listen():
            if message["type"] == "message":
                result = message["data"]
                print(f"✅ Received Render Result: {result}")

if __name__ == "__main__":
    manager = RenderFarmManager()

    # Example usage: dispatch task and listen
    manager.dispatch_task("temp/generated.blend", "outputs/final_video.mp4")
    manager.listen_for_results()
