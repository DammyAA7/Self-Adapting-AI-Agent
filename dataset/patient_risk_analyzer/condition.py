"""
Medical Condition Class
Represents a medical condition with severity tracking
"""

from datetime import datetime


class Condition:
    """Represents a medical condition"""
    def __init__(self, name: str, severity: int, diagnosed_date: str):
        self.name = name
        self.severity = severity  # 1-10 scale
        self.diagnosed_date = datetime.strptime(diagnosed_date, "%Y-%m-%d")

    def __repr__(self):
        return f"Condition({self.name}, severity={self.severity})"
