from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


import re

def validate_email_addresses(emails):
    """Validates a list of email addresses and returns a dict mapping each unique address to its validity."""
    if not isinstance(emails, list):
        raise TypeError("emails must be provided as a list")
    pattern = re.compile(r'^[A-Za-z0-9._+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$')
    result = {}
    for email in emails:
        if not isinstance(email, str):
            raise TypeError("all items in the email list must be strings")
        if email in result:
            continue
        result[email] = bool(pattern.match(email))
    return result
