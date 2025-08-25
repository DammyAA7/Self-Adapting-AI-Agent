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

def calculate_expression(expr, path=None):
    """
    Safely evaluates a simple arithmetic expression in string form.
    Returns the result if valid, otherwise returns False for invalid/malformed input.
    Supports +, -, *, /, %, **, parentheses, floats, scientific notation.
    """
    # Check input type
    if not isinstance(expr, str):
        return False
    expr = expr.strip()
    if not expr:
        return False

    # Acceptable characters: digits, operators, dot, e, E, parentheses, spaces, tabs, newlines, unary +/-
    allowed_re = re.compile(r'^[\d\s\+\-\*\/\%\(\)\.eE]+$')
    # Remove tabs/newlines for further checks and eval
    expr_clean = expr.replace('\t', '').replace('\n', '').replace(' ', '')
    if not expr_clean:
        return False
    # Check for any illegal characters
    if not allowed_re.fullmatch(expr.replace('\t', '').replace('\n', '')):
        return False

    # Disallow malformed float: two or more consecutive dots in a number (e.g., 2..5)
    if re.search(r'\d*\.\.\d*', expr_clean):
        return False

    # Disallow empty parenthesis
    if re.search(r'\(\s*\)', expr):
        return False

    # Parenthesis matching check
    def paren_balanced(s):
        cnt = 0
        for c in s:
            if c == '(':
                cnt += 1
            elif c == ')':
                cnt -= 1
                if cnt < 0:
                    return False
        return cnt == 0
    if not paren_balanced(expr):
        return False

    # Disallow unmatched right parenthesis at edge
    if expr.count('(') != expr.count(')'):
        return False

    # Remove all white spaces for operator/parenthesis checks
    ex = expr.replace(' ', '').replace('\n','').replace('\t','')
    if not ex or all(c in '+-*/%()' for c in ex):
        return False

    # Disallow trailing operator (except closing parenthesis)
    if re.match(r'.*[\+\-\*\/\%\*]$', ex) and not ex.endswith(')'):
        return False
    # Disallow leading operator sequence except unary +/-
    if re.match(r'^[\*\/%]{1,2}', ex):
        return False

    # Disallow operator sequence at end (e.g., 2+2**, 2+2//)
    if re.search(r'[\+\-\*\/\%]{2,}$', ex):
        if not ex.endswith('**'):
            return False
        # Only allow ** if not at end
        if ex.endswith('**'):
            # Only allow if followed by a digit (should not be at end)
            if len(ex) < 3 or not ex[-3].isdigit():
                return False

    # Disallow malformed operator sequences:
    # e.g., 2***2, ** at start, or any sequence of three or more non-digit, non-parenthesis, non-space
    # Allow '**' for exponentiation, allow '//' for integer division (even if not tested)
    # Disallow three or more of the same or different operator (e.g., '***', '///', '+++' etc.)
    tokens = re.findall(r'(\*\*\*+|\/\/\/+|[\+\-\*\/\%]{3,}|[\/\*]{3,})', ex)
    if tokens:
        return False
    # Disallow '***' except in valid exponentiation (e.g., '2***2' is invalid, but '2**2' is valid)
    if re.search(r'\*{3,}', ex):
        return False
    if re.search(r'\/{3,}', ex):
        return False
    # Disallow repeated % operator
    if re.search(r'%{2,}', ex):
        return False

    # Disallow empty parenthesis
    if re.search(r'\(\)', ex):
        return False

    # Disallow unmatched right parenthesis
    if ex.count('(') < ex.count(')'):
        return False

    # Disallow unmatched left parenthesis
    if ex.count('(') > ex.count(')'):
        return False

    # Disallow trailing ** or // (e.g., "2+2**")
    if re.search(r'(\*\*|//)$', ex):
        return False

    # Disallow expression like "2++--**//"
    if re.fullmatch(r'[\+\-\*\/\%]+', ex):
        return False

    # Disallow parenthesis with nothing inside (already checked above)

    # Disallow malformed float with multiple dots (already checked above)

    # Try to evaluate, catch exceptions
    try:
        # Only allow safe builtins
        # Remove spaces/tabs/newlines for eval
        safe_expr = expr.replace('\t','').replace('\n','')
        # Safely evaluate the expression
        result = eval(safe_expr, {"__builtins__": None}, {})
        # If result is not int or float, reject
        if not isinstance(result, (int, float)):
            return False
        return result
    except (ZeroDivisionError, SyntaxError, NameError, TypeError, ValueError):
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