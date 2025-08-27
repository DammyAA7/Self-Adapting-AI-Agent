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

def delete_todo(todo_id, path=None):
    """
    Deletes a todo item by its ID from the todo.csv file.
    """
    if not isinstance(todo_id, int):
        raise TypeError("todo_id must be an integer")
    file_path = path if path else "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-III-Azure/todo.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: {file_path}")
    deleted = False
    rows = []
    try:
        with open(file_path, mode='r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get('id') == str(todo_id):
                    deleted = True
                    continue
                rows.append(row)
    except PermissionError:
        raise
    if not deleted:
        return False
    try:
        with open(file_path, mode='w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except PermissionError:
        raise
    return True

if __name__ == "__main__":
    pass
