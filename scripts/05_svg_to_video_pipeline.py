# SVG to Video Pipeline Coordinator
# 05_svg_to_video_pipeline.py
"""
SVG to Video Pipeline
Orchestrates the full pipeline: generate SVG -> convert to 3D -> animate -> render video.
"""

import subprocess
import os
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_DIR = BASE_DIR / "outputs"

# Paths to individual scripts
SVG_GEN_SCRIPT = SCRIPTS_DIR / "01_langchain_svg_generator.py"
SVG_TO_3D_SCRIPT = SCRIPTS_DIR / "02_svg_to_3d_blender.py"
ANIMATION_SCRIPT = SCRIPTS_DIR / "03_scenex_animation.py"
RENDER_SCRIPT = SCRIPTS_DIR / "04_video_renderer.py"

def generate_svg(concept, svg_output_path):
    """Call SVG generation script (LangChain)"""
    # Placeholder: real call would involve LangChain API
    # Here we simulate creating a static SVG
    svg_content = f\"\"\"<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">
    <rect width="800" height="600" fill="lightblue" />
    <text x="400" y="300" font-size="30" text-anchor="middle" fill="black">{concept}</text>
    </svg>\"\"\"
    with open(svg_output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✅ SVG generated at: {svg_output_path}")

def run_blender_script(script_path, args):
    """Run a Blender Python script with arguments."""
    blender_path = "blender"  # Assumes 'blender' is in PATH
    command = [
        blender_path, "--background", "--python", str(script_path), "--"
    ] + args
    print(f"▶️ Running Blender script: {script_path.name} with args {args}")
    subprocess.run(command, check=True)

def orchestrate_pipeline(concept, output_video_path):
    """Run the full SVG-to-Video pipeline."""
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    svg_path = TEMP_DIR / "generated.svg"
    blend_path = TEMP_DIR / "generated.blend"
    
    # Step 1: Generate SVG
    generate_svg(concept, svg_path)

    # Step 2: Import SVG into Blender and create 3D mesh
    run_blender_script(SVG_TO_3D_SCRIPT, [str(svg_path), str(blend_path), "0.1"])

    # Step 3: Animate 3D objects
    run_blender_script(ANIMATION_SCRIPT, ["1", "120", "5.0"])

    # Step 4: Render to video
    run_blender_script(RENDER_SCRIPT, [str(output_video_path)])

    print(f"✅ Pipeline completed! Final video at: {output_video_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python 05_svg_to_video_pipeline.py <concept_text> <output_video_path>")
    else:
        concept_text = sys.argv[1]
        output_video_path = sys.argv[2]
        orchestrate_pipeline(concept_text, output_video_path)
