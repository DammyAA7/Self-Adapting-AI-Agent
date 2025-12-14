"""
Patient Class
Patient information and medical history management
"""

from typing import List
from .condition import Condition


class Patient:
    """Patient information and medical history"""
    def __init__(self, id: str, name: str, age: int, blood_type: str):
        self.id = id
        self.name = name
        self.age = age
        self.blood_type = blood_type
        self.conditions: List[Condition] = []

    def add_condition(self, condition: Condition):
        """Add a medical condition to patient record"""
        self.conditions.append(condition)

    def get_total_conditions(self) -> int:
        """Get count of all conditions"""
        return len(self.conditions)

    def get_average_severity(self) -> float:
        """Calculate average severity of all conditions"""
        if not self.conditions:
            return 0.0
        return sum(c.severity for c in self.conditions) / len(self.conditions)

    def __repr__(self):
        return f"Patient({self.id}, {self.name}, age={self.age})"
