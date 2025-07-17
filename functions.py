import argparse
import csv
import os
from datetime import datetime


def add_todo(todo_text):
    """Add a new todo item to the todo.csv file"""
    # Create the CSV file if it doesn't exist
    file_exists = os.path.exists('todo.csv')
    
    with open('todo.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'todo', 'created_at', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Get the next ID by reading existing entries
        todo_id = 1
        if file_exists:
            with open('todo.csv', 'r', encoding='utf-8') as read_file:
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
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'pending'
        })
    
    print(f"Todo added successfully with ID: {todo_id}")
    return todo_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a todo item to todo.csv")
    parser.add_argument("function_name", type=str, help="Function to run (use 'add_todo')")
    parser.add_argument("todo_text", type=str, help="The todo item text to add")

    args = parser.parse_args()
    func_name = args.function_name
    todo_text = args.todo_text

    try:
        # Only allow the add_todo function
        if func_name == "add_todo":
            result = add_todo(todo_text)
        else:
            print(f"Error: Unknown function '{func_name}'. Only 'add_todo' is supported.")
    except Exception as e:
        print(f"Error: {e}")