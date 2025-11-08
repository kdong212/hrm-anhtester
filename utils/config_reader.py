import json
import os
from pathlib import Path

class ConfigReader:
    """Utility class to read configuration from JSON files"""
    
    @staticmethod
    def get_credentials():
        """Load credentials from JSON file"""
        try:
            config_path = Path(__file__).parent.parent / "config" / "credentials.json"
            with open(config_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Credentials file not found at {config_path}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON format in credentials file")
    
    @staticmethod
    def get_base_url():
        """Get base URL from config"""
        config = ConfigReader.get_credentials()
        return config.get("base_url", "")
