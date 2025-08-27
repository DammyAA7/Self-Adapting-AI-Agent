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
    Returns True if the todo was deleted, False if the ID was not found.
    Raises FileNotFoundError if the CSV file does not exist.
    Raises TypeError if the todo_id is not an int or float.
    """
    file_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-III-Azure/todo.csv" if path is None else path
    if not isinstance(todo_id, (int, float)):
        raise TypeError("todo_id must be an integer or float")
    if not os.path.exists(file_path):
        raise FileNotFoundError("The todo.csv file does not exist")
    updated_rows = []
    deleted = False
    with open(file_path, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        for row in reader:
            try:
                row_id = int(float(row.get("id", -1)))
            except (ValueError, TypeError):
                row_id = -1
            if row_id == int(todo_id):
                deleted = True
                continue
            updated_rows.append(row)
    if deleted:
        with open(file_path, mode="w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(updated_rows)
        return True
    return False

if __name__ == "__main__":
    pass

