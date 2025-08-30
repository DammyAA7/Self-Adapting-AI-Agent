from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


import csv
import os

def filter_todos_by_status_and_priority(status, priority, path=None):
    """
    Filters todos by status and priority from the todo CSV file.
    Returns a list of matching todo items as dictionaries, or False for invalid input or file errors.
    """
    file_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/todo.csv"
    if path:
        file_path = path
    if not isinstance(status, str) or not isinstance(priority, str):
        return False
    if not os.path.exists(file_path):
        return False
    try:
        with open(file_path, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            results = []
            for row in reader:
                if row.get('status') == status and row.get('priority') == priority:
                    results.append(row)
        return results
    except (FileNotFoundError, PermissionError):
        return False
    except Exception:
        return False
