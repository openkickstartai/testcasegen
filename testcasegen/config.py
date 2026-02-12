"""Configuration management for TestCaseGen."""

import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class Config:
    """Configuration settings for test generation."""
    
    framework: str = "pytest"
    output_dir: Path = Path("tests")
    verbose: bool = False
    max_test_cases: int = 10
    include_edge_cases: bool = True
    include_error_cases: bool = True
    custom_templates: Optional[Dict[str, str]] = None
    exclude_patterns: list = None
    
    def __post_init__(self):
        if self.exclude_patterns is None:
            self.exclude_patterns = ["__*", "test_*"]
        
        if isinstance(self.output_dir, str):
            self.output_dir = Path(self.output_dir)
    
    def load_from_file(self, config_path: str):
        """Load configuration from a JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        # Update configuration with loaded data
        for key, value in config_data.items():
            if hasattr(self, key):
                if key == "output_dir":
                    setattr(self, key, Path(value))
                else:
                    setattr(self, key, value)
    
    def save_to_file(self, config_path: str):
        """Save current configuration to a JSON file."""
        config_data = asdict(self)
        # Convert Path to string for JSON serialization
        config_data["output_dir"] = str(self.output_dir)
        
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
    
    def get_template_config(self) -> Dict[str, Any]:
        """Get template-specific configuration."""
        return {
            "framework": self.framework,
            "max_test_cases": self.max_test_cases,
            "include_edge_cases": self.include_edge_cases,
            "include_error_cases": self.include_error_cases,
            "custom_templates": self.custom_templates or {}
        }
    
    def should_exclude(self, filename: str) -> bool:
        """Check if a file should be excluded based on patterns."""
        import fnmatch
        
        for pattern in self.exclude_patterns:
            if fnmatch.fnmatch(filename, pattern):
                return True
        return False
    
    @classmethod
    def create_default_config(cls, output_path: str = "testcasegen.json"):
        """Create a default configuration file."""
        config = cls()
        config.save_to_file(output_path)
        return config