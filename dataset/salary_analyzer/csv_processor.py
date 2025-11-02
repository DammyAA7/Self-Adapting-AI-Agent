"""
CSV Processor Class
Handles CSV file operations
"""
import csv
from typing import List, Dict, Any
from pathlib import Path


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
