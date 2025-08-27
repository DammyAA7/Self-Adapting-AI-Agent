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

def delete_column(column_name, path=None):
    """
    Deletes a specified column from the todo.csv file, updating the file schema accordingly.
    """
    if not isinstance(column_name, str):
        raise TypeError("column_name must be a string")
    file_path = path if path is not None else "todo.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        if not fieldnames or column_name not in fieldnames:
            return False
        new_fieldnames = [fn for fn in fieldnames if fn != column_name]
        rows = list(reader)
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=new_fieldnames)
            writer.writeheader()
            for row in rows:
                row.pop(column_name, None)
                writer.writerow(row)
    except PermissionError:
        raise PermissionError(f"Permission denied when writing to file: {file_path}")
    return True

if __name__ == "__main__":
    pass
