"""
JSON Processor Class
Handles JSON configuration and data files
"""
import json
from typing import Dict, Any, List, Optional
from pathlib import Path


class JSONProcessor:
    """Handles JSON configuration and data files"""

    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = {}

    def load_config(self) -> bool:
        """Load JSON configuration"""
        try:
            with open(self.config_path, 'r') as file:
                self.config = json.load(file)
                return True
        except Exception as e:
            print(f"Error loading JSON config: {e}")
            return False

    def get_database_settings(self) -> Optional[Dict[str, Any]]:
        """Extract database configuration"""
        return self.config.get('database', None)

    def get_api_endpoints(self) -> List[str]:
        """Get list of API endpoints from config"""
        return self.config.get('api', {}).get('endpoints', [])
