"""
Data Validator Class
Validates data structures and formats
"""
from typing import Dict, Any


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
