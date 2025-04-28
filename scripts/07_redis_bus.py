# Redis Message Bus
# 07_redis_bus.py
"""
Redis Message Bus
Simple publish/subscribe wrapper for asynchronous communication between components.
"""

import redis
import threading
import time

class RedisBus:
    """Simple Redis Pub/Sub message bus."""

    def __init__(self, host="localhost", port=6379, db=0, channel="svg_to_video"):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.channel = channel
        self._listening = False

    def publish(self, message):
        """Publish a message to the channel."""
        self.redis.publish(self.channel, message)
        print(f"✅ Published message: {message}")

    def subscribe(self, callback):
        """Subscribe to the channel and run a callback on new messages."""
        def listener():
            self.pubsub.subscribe(self.channel)
            print(f"👂 Subscribed to channel: {self.channel}")
            for message in self.pubsub.listen():
                if message["type"] == "message":
                    callback(message["data"])

        self._listening = True
        thread = threading.Thread(target=listener, daemon=True)
        thread.start()

    def stop(self):
        """Stop listening to messages."""
        if self._listening:
            self.pubsub.unsubscribe(self.channel)
            self._listening = False
            print("🛑 Unsubscribed and stopped listening.")

# Example usage if running standalone
if __name__ == "__main__":
    def handle_message(msg):
        print(f"Received: {msg}")

    bus = RedisBus()
    bus.subscribe(handle_message)

    time.sleep(1)
    bus.publish("Hello World from RedisBus!")
    time.sleep(5)
    bus.stop()
