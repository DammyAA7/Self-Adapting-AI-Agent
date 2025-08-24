import argparse
import csv
import os
import datetime
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

def add_todo(todo_text, path=None):
  """Add a new todo item to the todo.csv file"""
  file_path = path if path else globals().get('file_path', 'todo.csv')
  
  # Create the CSV file if it doesn't exist
  file_exists = os.path.exists(file_path)
  
  with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'todo', 'status', 'priority', 'created_at', 'completed_at']
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
      'status': Status.PENDING.value,
      'priority': Priority.MEDIUM.value,
      'created_at': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
      'completed_at': ''
    })
  
  print(f"Todo added successfully with ID: {todo_id}")
  return todo_id




import csv
import os

def delete_todo(todo_id, path=None):
    """
    Delete a todo item from the CSV file by its ID.
    Returns True if successful, False otherwise.
    """
    file_path = path if path else globals().get('file_path', 'todo.csv')
    
    # Handle None input
    if todo_id is None:
        return False
    
    # Try to convert todo_id to integer
    try:
        if isinstance(todo_id, str):
            if todo_id.strip() == "":
                return False
            # Handle string float conversion
            todo_id = int(float(todo_id))
        elif isinstance(todo_id, float):
            todo_id = int(todo_id)
        elif not isinstance(todo_id, int):
            return False
    except (ValueError, TypeError):
        return False
    
    # Handle negative or zero IDs
    if todo_id <= 0:
        return False
    
    # Check if file exists
    if not os.path.exists(file_path):
        return False
    
    try:
        # Read all todos
        todos = []
        found = False
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            
            # Check if required fieldnames exist
            if not fieldnames or 'id' not in fieldnames:
                return False
            
            for row in reader:
                try:
                    row_id = int(row['id'])
                    if row_id == todo_id:
                        found = True
                        # Skip this row (delete it)
                        continue
                    else:
                        todos.append(row)
                except (ValueError, KeyError):
                    # Keep malformed rows
                    todos.append(row)
        
        if not found:
            return False
        
        # Write back the remaining todos
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if fieldnames:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(todos)
        
        return True
        
    except (IOError, csv.Error):
        return False




import re

def calculate_expression(expr):
    """
    Safely evaluates a simple mathematical expression given as a string.
    Supports +, -, *, /, parentheses, and decimal numbers.
    Returns the numeric result or False for invalid input.
    """
    # Validate input type
    if not isinstance(expr, str):
        return False
    if expr is None:
        return False
    expr = expr.strip()
    if expr == '':
        return False

    # Only allow valid characters: digits, operators, whitespace, decimal point, parentheses
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\) \t\r\n]+", expr):
        return False

    # Disallow consecutive operators (except for unary minus)
    # (We allow things like '2+-2' and '-4+7', so we can't just block all consecutive operators)
    # We'll rely on eval with restricted globals/locals, and catch exceptions

    try:
        # Evaluate the expression safely
        result = eval(expr, {'__builtins__': None}, {})
    except (SyntaxError, NameError, TypeError, ZeroDivisionError):
        return False

    return result


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