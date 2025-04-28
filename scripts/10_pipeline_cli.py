# Pipeline CLI
# 10_pipeline_cli.py
"""
Pipeline CLI
Command-line tool to manually trigger SVG to Video generation.
"""

import argparse
import sys
from pathlib import Path
from svg_to_video_pipeline import orchestrate_pipeline

def main():
    parser = argparse.ArgumentParser(description="SVG to Video Pipeline CLI")
    parser.add_argument("concept", type=str, help="Concept text to generate SVG and animation")
    parser.add_argument("--output", type=str, default="outputs/generated_video.mp4", help="Output video path (default: outputs/generated_video.mp4)")
    
    args = parser.parse_args()

    # Ensure output directory exists
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"🚀 Starting pipeline for concept: \"{args.concept}\"")
    orchestrate_pipeline(args.concept, str(output_path))
    print(f"✅ Done! Video available at: {output_path}")

if __name__ == "__main__":
    main()
