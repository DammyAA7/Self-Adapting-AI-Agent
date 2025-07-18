import argparse
import csv
import os
import datetime



def add_todo(todo_text, path=None):
  """Add a new todo item to the todo.csv file"""
  file_path = path if path else globals().get('file_path', 'todo.csv')
  
  # Create the CSV file if it doesn't exist
  file_exists = os.path.exists(file_path)
  
  with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'todo', 'status', 'created_at', 'completed_at']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header if file is new
    if not file_exists:
      writer.writeheader()
    
    # Get the next ID by reading existing entries
    todo_id = 1
    if file_exists:
      with open(file_path, 'r', encoding='utf-8') as read_file:
        reader = csv.DictReader(read_file)
        existing_ids = []
        for row in reader:
          try:
            existing_ids.append(int(row['id']))
          except (ValueError, KeyError):
            continue
        if existing_ids:
          todo_id = max(existing_ids) + 1
    
    # Write the new todo
    writer.writerow({
      'id': todo_id,
      'todo': todo_text,
      'status': 'pending',
      'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      'completed_at': ''
    })
  
  print(f"Todo added successfully with ID: {todo_id}")
  return todo_id




import csv
import datetime
import os

def complete_todo(todo_id, path=None):
    """
    Marks a specific todo item as completed by its ID.
    """
    file_path = path if path else globals().get('file_path', 'todo.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    todos = []
    updated_todo = None
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if not row.get('id') or not row.get('status'):
                continue
            try:
                current_id = int(row['id'])
            except ValueError:
                continue
            if current_id == todo_id:
                if row['status'] != 'completed':
                    row['status'] = 'completed'
                    row['completed_at'] = datetime.datetime.now().isoformat()
                updated_todo = {
                    'id': current_id,
                    'text': row.get('text', ''),
                    'status': row['status'],
                    'created_at': row.get('created_at', ''),
                    'completed_at': row.get('completed_at', '')
                }
            todos.append(row)
    if updated_todo is None:
        raise ValueError(f"Todo with ID {todo_id} not found.")
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todos)
    return updated_todo




import csv
import os

def delete_todo(todo_id, path=None):
    """
    Removes a specific todo item from the todo.csv file by its ID.
    Returns True if deletion was successful.
    Raises ValueError if ID not found or invalid, FileNotFoundError if file missing.
    """
    file_path = path if path else globals().get('file_path', 'todo.csv')
    if not isinstance(todo_id, int):
        raise ValueError("todo_id must be an integer")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No todo file found at {file_path}")
    todos = []
    deleted = False
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row_id = int(row.get('id', -1))
            except ValueError:
                row_id = None
            if row_id == todo_id:
                deleted = True
                continue
            todos.append(row)
    if not deleted:
        raise ValueError(f"Todo with ID {todo_id} not found")
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'text', 'status', 'created_at', 'completed_at']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(todos)
    return True




import csv
import os

def list_todos(path=None):
    """
    Returns all todo items from the todo.csv file.

    Parses the file robustly: IDs as strings, raises FileNotFoundError if missing,
    raises exception containing 'malformed' for invalid CSV structure,
    and ensures no None entries are returned.
    """
    file_path = path if path else globals().get('file_path', 'todo.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Todo file not found: {file_path}")
    todos = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required_fields = ['id', 'text', 'status', 'created_at', 'completed_at']
            if reader.fieldnames is None or any(field not in reader.fieldnames for field in required_fields):
                raise Exception("malformed CSV: missing required columns")
            for row in reader:
                if any(row.get(field) is None for field in required_fields):
                    raise Exception("malformed CSV: None entries in row")
                todo = {field: row[field] for field in required_fields}
                todos.append(todo)
    except csv.Error as e:
        raise Exception("malformed CSV: " + str(e))
    return todos


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run any available function dynamically")
    parser.add_argument("function_name", type=str, help="Name of the function to run")
    parser.add_argument("args", type=str, help="Comma-separated arguments")
    
    args = parser.parse_args()
    func_name = args.function_name
    
    try:
        # Parse comma-separated arguments
        arg_list = []
        for x in args.args.split(","):
            x = x.strip()
            # Try to convert to int first, then float, then keep as string
            try:
                arg_list.append(int(x))
            except ValueError:
                try:
                    arg_list.append(float(x))
                except ValueError:
                    arg_list.append(x)  # Keep as string if not a number
        
        # Dynamically call the function
        if func_name in globals() and callable(globals()[func_name]):
            result = globals()[func_name](*arg_list)
            print(result)
        else:
            print(f"Error: Function '{func_name}' not found or not callable")
    except Exception as e:
        print(f"Error: {e}")