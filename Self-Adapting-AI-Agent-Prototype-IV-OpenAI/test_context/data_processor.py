"""
Data Processing Module
Handles CSV and JSON data operations with validation
"""
import csv
import json
from typing import List, Dict, Any, Optional
from pathlib import Path


class DataValidator:
    """Validates data structures and formats"""
    
    @staticmethod
    def validate_user_data(user_record: Dict[str, Any]) -> bool:
        """
        Validates user record has required fields
        Required: id, name, email, age, role
        """
        required_fields = ['id', 'name', 'email', 'age', 'role']
        return all(field in user_record for field in required_fields)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        return '@' in email and '.' in email.split('@')[-1]


class CSVProcessor:
    """Handles CSV file operations"""
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data: List[Dict[str, Any]] = []
    
    def load_data(self) -> bool:
        """Load CSV data into memory"""
        try:
            with open(self.file_path, 'r') as file:
                reader = csv.DictReader(file)
                self.data = list(reader)
                return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return False
    
    def filter_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Filter users by their role"""
        return [record for record in self.data if record.get('role') == role]
    
    def get_users_over_age(self, min_age: int) -> List[Dict[str, Any]]:
        """Get users above specified age"""
        return [record for record in self.data 
                if int(record.get('age', 0)) > min_age]


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


# Example usage patterns
if __name__ == "__main__":
    # Process user data
    csv_proc = CSVProcessor("/data/users.csv")
    if csv_proc.load_data():
        admins = csv_proc.filter_by_role("admin")
        seniors = csv_proc.get_users_over_age(50)
    
    # Load configuration
    json_proc = JSONProcessor("/config/app_config.json")
    if json_proc.load_config():
        db_settings = json_proc.get_database_settings()
        endpoints = json_proc.get_api_endpoints()