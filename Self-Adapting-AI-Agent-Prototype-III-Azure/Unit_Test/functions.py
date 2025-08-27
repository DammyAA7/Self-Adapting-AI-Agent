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

def add_multiple_rows(table_identifier, column_values, times, path=None):
    """
    Appends the specified column values as new rows to the given CSV table a specified number of times.
    """
    if not isinstance(table_identifier, str):
        raise TypeError("table_identifier must be a string")
    if not isinstance(column_values, dict):
        raise TypeError("column_values must be a dict")
    if not isinstance(times, int):
        raise TypeError("times must be an integer")
    if times < 1:
        return False
    if path and not isinstance(path, str):
        raise TypeError("path must be a string")
    file_path = table_identifier
    if path:
        file_path = path
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Table file not found: {file_path}")
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            if fieldnames is None:
                raise ValueError(f"No columns found in table: {file_path}")
    except PermissionError:
        raise
    rows_to_add = []
    for _ in range(times):
        row = {}
        for col in fieldnames:
            if col in column_values:
                row[col] = column_values[col]
            else:
                row[col] = ''
        rows_to_add.append(row)
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(rows_to_add)
    except PermissionError:
        raise
    return True

if __name__ == "__main__":
    pass
