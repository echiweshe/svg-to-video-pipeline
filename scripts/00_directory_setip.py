import os
from pathlib import Path

# Define the base project path
BASE_PATH = r"C:\\ZB_Share\\Labs\\src\\CluadeMCP\\svg-to-video-pipeline"

# Define the structure with optional content
structure = {
    "docs/architecture/implementation_guides": {
        "00_index.md": "# Index\n",
        "01_project_overview.md": "# Project Overview\n",
        "02_svg_generation_component.md": "# SVG Generation Component\n",
        "03_svg_to_3d_conversion_component.md": "# SVG to 3D Conversion Component\n",
        "04_animation_system_component_part2.md": "# Animation System Component\n",
        "05_video_rendering_component.md": "# Video Rendering Component\n",
        "06_pipeline_orchestration_part2.md": "# Pipeline Orchestration\n",
        "07_infrastructure_integration_part2.md": "# Infrastructure Integration\n",
        "08_testing_and_deployment_guide_part3.md": "# Testing and Deployment Guide\n",
    },
    "docs/architecture": {
        "svg_to_video_implementation_plan.md": "# SVG to Video Implementation Plan\n",
        "svg_to_video_implementation_plan_combined_part2.md": "",
        "svg_to_video_implementation_plan_combined_part3.md": "",
        "svg_to_video_implementation_plan_part3.md": "",
        "svg_to_video_implementation_plan_part4.md": "",
        "svg_to_video_implementation_plan_part5.md": "",
        "technology_stack_strategy.md": "# Technology Stack Strategy\n",
    },
    "scripts": {
        "01_langchain_svg_generator.py": "# LangChain SVG Generator\n",
        "02_svg_to_3d_blender.py": "# SVG to 3D Blender Converter\n",
        "03_scenex_animation.py": "# SceneX Animation\n",
        "04_video_renderer.py": "# Video Renderer\n",
        "05_svg_to_video_pipeline.py": "# SVG to Video Pipeline Coordinator\n",
        "06_langchain_manager.py": "# LangChain Manager\n",
        "07_redis_bus.py": "# Redis Message Bus\n",
        "08_svg_video_service.py": "# SVG Video Service\n",
        "09_pipeline_config.py": "# Pipeline Config Manager\n",
        "10_pipeline_cli.py": "# Pipeline CLI\n",
        "11_svg_video_client.py": "# SVG Video Client\n",
        "12_service_launcher.py": "# Service Launcher\n",
        "13_example_client.py": "# Example Client\n",
    },
    "scripts/render_farm": {
        "14_render_farm_manager.py": "# Render Farm Manager\n",
        "15_render_farm_worker.py": "# Render Farm Worker\n",
    },
    "outputs": {},
    "temp": {},
    "config": {
        "config.json": "{\n  \"temp_dir\": \"temp\",\n  \"script_dir\": \"scripts\",\n  \"output_dir\": \"outputs\",\n  \"blender_path\": \"blender\",\n  \"default_provider\": \"claude\",\n  \"default_render_quality\": \"medium\",\n  \"cleanup_temp\": true,\n  \"log_level\": \"INFO\"\n}\n"
    },
}

def create_structure_with_content(base_path, structure):
    for folder, files in structure.items():
        folder_path = Path(base_path) / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"Created folder: {folder_path}")

        for file, content in files.items():
            file_path = folder_path / file
            if not file_path.exists():
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Created file: {file_path}")

if __name__ == "__main__":
    create_structure_with_content(BASE_PATH, structure)
    print("\n✅ Directory structure and files created and populated successfully.")
