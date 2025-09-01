# Dynamically generated functions will be added here



import csv
from datetime import datetime

def add_todo(file_path, todo, priority, status="pending", created_at=None):
    """Adds a new todo item to the specified CSV file.
    Returns True if the todo was added successfully, False otherwise."""
    valid_priorities = {'low', 'medium', 'high', 'critical'}
    if not file_path or not isinstance(file_path, str):
        return False
    if not todo or not isinstance(todo, str):
        return False
    if priority not in valid_priorities:
        return False
    try:
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception:
        return False
    if rows:
        try:
            max_id = max(int(r['id']) for r in rows if r.get('id'))
        except Exception:
            max_id = 0
        next_id = max_id + 1
    else:
        next_id = 1
    created_at_str = created_at if created_at else datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fieldnames = ['id', 'todo', 'status', 'priority', 'created_at', 'completed_at']
    row = {
        'id': str(next_id),
        'todo': todo,
        'status': status,
        'priority': priority,
        'created_at': created_at_str,
        'completed_at': ''
    }
    try:
        with open(file_path, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(row)
    except Exception:
        return False
    return True


if __name__ == "__main__":
    pass

if __name__ == "__main__":
    pass
