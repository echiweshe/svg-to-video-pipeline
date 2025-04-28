# Pipeline Config Manager
# 09_pipeline_config.py
"""
Pipeline Config Manager
Loads pipeline configuration from a JSON file.
"""

import json
from pathlib import Path

class PipelineConfig:
    """Loads configuration for the SVG-to-Video pipeline."""
    
    def __init__(self, config_path=None):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.config_path = config_path or (self.base_dir / "config" / "config.json")
        self.config = {}
        
        self.load()

    def load(self):
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        print(f"✅ Loaded config from {self.config_path}")

    def get(self, key, default=None):
        """Retrieve a configuration value."""
        return self.config.get(key, default)

    def reload(self):
        """Reload the configuration."""
        self.load()

if __name__ == "__main__":
    config = PipelineConfig()
    print(config.config)
