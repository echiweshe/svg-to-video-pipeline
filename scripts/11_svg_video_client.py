# SVG Video Client
# 11_svg_video_client.py
"""
SVG Video Client
Submits generation requests to the SVG-to-Video Service via Redis.
"""

import sys
from redis_bus import RedisBus

def main():
    if len(sys.argv) < 3:
        print("Usage: python 11_svg_video_client.py <concept_text> <output_filename.mp4>")
        sys.exit(1)

    concept_text = sys.argv[1]
    output_filename = sys.argv[2]

    # Connect to Redis
    bus = RedisBus()

    # Format the message
    message = f"{concept_text}|||{output_filename}"

    # Publish the message
    bus.publish(message)
    print(f"🚀 Published task: {message}")

if __name__ == "__main__":
    main()
