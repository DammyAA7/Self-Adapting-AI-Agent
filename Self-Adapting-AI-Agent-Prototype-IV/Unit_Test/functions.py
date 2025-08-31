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
import datetime

def add_todo(todo, priority, status=None, created_at=None, completed_at=None, file_path=None):
    """Add a new todo entry to the CSV file at file_path.
    Returns True if the entry was added successfully, False otherwise."""
    # Validate todo description
    if not isinstance(todo, str) or not todo.strip():
        return False
    # Validate priority
    valid_priorities = {"low", "medium", "high", "critical"}
    if not isinstance(priority, str) or priority not in valid_priorities:
        return False
    # Determine status
    if status is not None:
        if not isinstance(status, str):
            return False
        entry_status = status
    else:
        entry_status = "pending"
    # Validate file path
    if not isinstance(file_path, str) or not os.path.exists(file_path):
        return False
    # Read existing entries to determine next ID
    try:
        with open(file_path, newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception:
        return False
    max_id = 0
    for row in rows[1:]:
        try:
            curr_id = int(row[0])
            if curr_id > max_id:
                max_id = curr_id
        except Exception:
            continue
    new_id = max_id + 1
    # Determine created_at
    if created_at is not None:
        if not isinstance(created_at, str) or not created_at.strip():
            return False
        entry_created = created_at
    else:
        entry_created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Determine completed_at
    if completed_at is not None:
        if not isinstance(completed_at, str):
            return False
        entry_completed = completed_at
    else:
        entry_completed = ""
    # Append new row
    try:
        with open(file_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([str(new_id), todo, entry_status, priority, entry_created, entry_completed])
    except Exception:
        return False
    return True
