# SVG Video Service
# 08_svg_video_service.py
"""
SVG Video Service
Listens for generation commands over Redis and runs the SVG to Video pipeline.
"""

import asyncio
from pathlib import Path
from redis_bus import RedisBus
from svg_to_video_pipeline import orchestrate_pipeline

class SVGVideoService:
    """Service to listen for generation requests and execute the full pipeline."""
    
    def __init__(self, redis_host="localhost", redis_port=6379, channel="svg_to_video"):
        self.bus = RedisBus(host=redis_host, port=redis_port, channel=channel)
        self.temp_dir = Path("temp")
        self.outputs_dir = Path("outputs")

    def handle_message(self, message):
        """Handle an incoming message from Redis."""
        print(f"🟰 Received task: {message}")

        try:
            # Expect message format: concept_text|||output_video_filename.mp4
            concept, output_filename = message.split("|||")
            output_path = self.outputs_dir / output_filename

            # Run the full pipeline
            orchestrate_pipeline(concept, str(output_path))

            # Publish success
            self.bus.publish(f"✅ Completed: {output_filename}")

        except Exception as e:
            error_message = f"❌ Error: {str(e)}"
            print(error_message)
            self.bus.publish(error_message)

    def run(self):
        """Start listening for commands."""
        print("🚀 SVG Video Service started. Listening for tasks...")
        self.bus.subscribe(self.handle_message)

        try:
            # Keep the main thread alive
            while True:
                asyncio.sleep(3600)
        except KeyboardInterrupt:
            print("🛑 Shutting down service...")
            self.bus.stop()

if __name__ == "__main__":
    service = SVGVideoService()
    service.run()
