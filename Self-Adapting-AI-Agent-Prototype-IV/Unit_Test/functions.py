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

def list_help_todos(file_path):
    """List todos containing 'help' case-insensitive from a CSV file.
    Reads the CSV at file_path and prints each row where the 'todo' field includes
    'help' (case-insensitive). Returns True if any such todos are printed,
    False otherwise. Returns False if the file cannot be found.
    """
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            found = False
            for row in reader:
                if len(row) > 1 and 'help' in row[1].lower():
                    print(','.join(row))
                    found = True
            return True if found else False
    except FileNotFoundError:
        return False
