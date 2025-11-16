"""
Agent Configuration
Centralized configuration for all agents in the system.
"""

import os
from typing import Dict, Any


class AgentConfig:
    """Configuration settings for agents."""
    
    # Model Configuration
    DEFAULT_MODEL = "gemini-2.0-flash-exp"
    ALTERNATIVE_MODELS = [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-2.0-flash-exp"
    ]
    
    # Temperature Settings (controls randomness)
    TEMPERATURE_SEARCH = 0.4  # Balanced for search
    TEMPERATURE_SUMMARIZE = 0.3  # Lower for factual summaries
    TEMPERATURE_FACT_CHECK = 0.2  # Lowest for accuracy
    TEMPERATURE_WRITE = 0.5  # Higher for creative writing
    
    # Research Depth Settings
    QUICK_RESEARCH_SOURCES = 3
    MEDIUM_RESEARCH_SOURCES = 5
    DEEP_RESEARCH_SOURCES = 10
    
    # Memory Settings
    MEMORY_STORAGE_PATH = os.getenv("MEMORY_STORAGE_PATH", "memory_bank.json")
    MAX_HISTORY_ITEMS = 100
    
    # Output Settings
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "outputs")
    REPORT_FORMAT = "txt"  # or "md", "pdf"
    
    # Session Settings
    SESSION_TIMEOUT_MINUTES = 30
    AUTO_SAVE = True
    
    # API Settings
    API_RETRY_ATTEMPTS = 3
    API_TIMEOUT_SECONDS = 30
    
    @classmethod
    def get_model(cls) -> str:
        """Get the model name from environment or default."""
        return os.getenv("MODEL_NAME", cls.DEFAULT_MODEL)
    
    @classmethod
    def get_config_dict(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary."""
        return {
            "model": cls.get_model(),
            "temperatures": {
                "search": cls.TEMPERATURE_SEARCH,
                "summarize": cls.TEMPERATURE_SUMMARIZE,
                "fact_check": cls.TEMPERATURE_FACT_CHECK,
                "write": cls.TEMPERATURE_WRITE
            },
            "research_depth": {
                "quick": cls.QUICK_RESEARCH_SOURCES,
                "medium": cls.MEDIUM_RESEARCH_SOURCES,
                "deep": cls.DEEP_RESEARCH_SOURCES
            },
            "memory": {
                "storage_path": cls.MEMORY_STORAGE_PATH,
                "max_history": cls.MAX_HISTORY_ITEMS
            },
            "output": {
                "directory": cls.OUTPUT_DIR,
                "format": cls.REPORT_FORMAT
            }
        }
    
    @classmethod
    def print_config(cls):
        """Print current configuration."""
        print("\n🔧 Agent Configuration")
        print("=" * 60)
        config = cls.get_config_dict()
        for key, value in config.items():
            print(f"{key.upper()}:")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}: {sub_value}")
            else:
                print(f"  {value}")
        print("=" * 60 + "\n")


# Export configuration
__all__ = ["AgentConfig"]
