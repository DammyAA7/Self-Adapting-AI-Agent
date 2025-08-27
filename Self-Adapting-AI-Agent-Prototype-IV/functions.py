

import csv
import os

def delete_todo(todo_id, path=None):
    """
    Deletes a todo item with the given ID from the todo CSV file.
    Returns True if the item was deleted, False if not found, invalid, or on any error.
    """
    file_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/todo.csv"
    if path is not None:
        file_path = path

    # Validate todo_id: must be int and > 0
    try:
        if not isinstance(todo_id, int):
            todo_id = int(todo_id)
    except Exception:
        return False
    if todo_id <= 0:
        return False

    # If file doesn't exist, return False (do NOT raise)
    if not os.path.isfile(file_path):
        return False

    # Read, filter, and re-write
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))
            if not reader:
                return False
            fieldnames = reader[0].keys()
            initial_len = len(reader)
            filtered_rows = [row for row in reader if str(row.get('id', '')).strip() != str(todo_id)]
            if len(filtered_rows) == initial_len:
                return False  # id not found
        # Write back if at least one row was removed
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(filtered_rows)
        return True
    except Exception:
        return False



if __name__ == "__main__":
    pass
