# Example Client
# 13_example_client.py
"""
Example Client
Demonstrates sending a job and listening for the result from the SVG Video Service.
"""

import time
from redis_bus import RedisBus

def handle_result(message):
    print(f"📩 Service Response: {message}")

def main():
    concept_text = "Water Cycle Diagram"
    output_filename = "water_cycle.mp4"

    bus = RedisBus()

    # Subscribe to listen for results
    bus.subscribe(handle_result)

    # Give a tiny delay to ensure subscription is active
    time.sleep(1)

    # Publish the task
    task_message = f"{concept_text}|||{output_filename}"
    bus.publish(task_message)
    print(f"🚀 Task sent: {task_message}")

    try:
        # Keep the client alive to receive results
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Stopping Example Client...")
        bus.stop()

if __name__ == "__main__":
    main()
