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
    Marks a specified todo item as completed in the todo.csv file.
    Returns True on successful update, False if the todo is already completed.
    Raises ValueError if the todo ID does not exist.
    """
    if not isinstance(todo_id, int):
        raise ValueError("todo_id must be an integer")
    file_path = path if path else globals().get('file_path', 'todo.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Todo file not found: {file_path}")
    todos = []
    found = False
    updated = False
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('id') == str(todo_id):
                    found = True
                    if row.get('status') == 'completed':
                        return False
                    row['status'] = 'completed'
                    row['completed_at'] = datetime.datetime.now().isoformat()
                    updated = True
                todos.append(row)
    except Exception as e:
        raise IOError(f"Error reading todo file: {e}")
    if not found:
        raise ValueError(f"Todo with ID {todo_id} not found")
    if updated:
        fieldnames = ['id', 'text', 'status', 'created_at', 'completed_at']
        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(todos)
        except Exception as e:
            raise IOError(f"Error writing todo file: {e}")
        return True
    return False


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