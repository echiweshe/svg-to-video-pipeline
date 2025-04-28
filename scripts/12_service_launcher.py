# Service Launcher
# 12_service_launcher.py
"""
Service Launcher
Starts the SVG Video Service to listen for generation tasks via Redis.
"""

from svg_video_service import SVGVideoService

def main():
    print("🚀 Launching SVG Video Service...")
    service = SVGVideoService()
    service.run()

if __name__ == "__main__":
    main()
