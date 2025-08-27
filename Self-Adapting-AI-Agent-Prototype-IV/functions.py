

import csv

def delete_todo(todo_id, path=None):
    """
    Deletes a todo item from the todo.csv file by its ID.
    Returns True if deletion was successful, False otherwise.
    """
    file_path = path if path else "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/todo.csv"
    # Validate todo_id
    if not isinstance(todo_id, int):
        return False
    if todo_id <= 0:
        return False
    try:
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            fieldnames = reader.fieldnames
    except Exception:
        return False
    found = False
    filtered_rows = []
    for row in rows:
        try:
            current_id = int(row.get('id', ''))
        except (ValueError, TypeError):
            continue
        if current_id == todo_id:
            found = True
        else:
            filtered_rows.append(row)
    if not found:
        return False
    try:
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in filtered_rows:
                writer.writerow(row)
    except Exception:
        return False
    return True


if __name__ == "__main__":
    pass
