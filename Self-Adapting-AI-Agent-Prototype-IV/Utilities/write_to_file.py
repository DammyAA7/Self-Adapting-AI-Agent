'''
Function that writes to a file
Could be txt, json or python file
'''

def write_to_file(type, file_path, content):
    if type == 'txt':
        # Implementation for writing to a text file
        with open(file_path, 'r') as f:
            lines = f.readlines()
        main_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('----'):
                main_index = i
                break
        if main_index != -1:
            # Insert the new prompt descriptor before the main block
            lines.insert(main_index, content + '\n\n')
            
            with open(file_path, 'w') as f:
                f.writelines(lines)
        
    elif type == 'json':
        import json as json_module
        
        # Read existing content
        with open(file_path, 'r') as f:
            existing_content = f.read().strip()
        
        # Handle different cases
        if not existing_content or existing_content == '[]':
            # Empty file or empty array - create new array with the content
            if content.strip().startswith('['):
                # Content is already an array
                with open(file_path, 'w') as f:
                    f.write(content + '\n')
            else:
                # Content is a single object, wrap it in an array
                with open(file_path, 'w') as f:
                    f.write('[\n' + content + '\n]\n')
        else:
            # File has existing array content - append to it
            try:
                # Parse existing JSON array
                existing_data = json_module.loads(existing_content)
                
                # Parse new content
                if content.strip().startswith('['):
                    new_data = json_module.loads(content)
                    if isinstance(new_data, list):
                        # Handle duplicate prevention for tools.json
                        if file_path.endswith('tools.json'):
                            for item in new_data:
                                if not any(existing_item.get('function', {}).get('name') == item.get('function', {}).get('name') 
                                         for existing_item in existing_data):
                                    existing_data.append(item)
                        else:
                            existing_data.extend(new_data)
                    else:
                        existing_data.append(new_data)
                else:
                    # Try to parse as JSON object
                    try:
                        new_obj = json_module.loads(content)
                        # Handle duplicate prevention for tools.json
                        if file_path.endswith('tools.json'):
                            if not any(existing_item.get('function', {}).get('name') == new_obj.get('function', {}).get('name') 
                                     for existing_item in existing_data):
                                existing_data.append(new_obj)
                        else:
                            existing_data.append(new_obj)
                    except:
                        # If not valid JSON, treat as raw text (shouldn't happen)
                        pass
                
                # Write back as formatted JSON
                with open(file_path, 'w') as f:
                    json_module.dump(existing_data, f, indent=4)
                    f.write('\n')
                    
            except json_module.JSONDecodeError:
                # Fallback to old behavior if JSON parsing fails
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                last_index = len(lines) - 1
                lines.insert(last_index, "," + content + '\n')
                with open(file_path, 'w') as f:
                    f.writelines(lines)
    elif type == 'python':
        with open(file_path, 'r') as f:
            lines = f.readlines()
        main_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('if __name__ == "__main__":'):
                main_index = i
                break

        if main_index != -1:
            # Insert the new function before the main block
            lines.insert(main_index, content + '\n\n')
            
            with open(file_path, 'w') as f:
                f.writelines(lines)
        else:
            # If no main block exists or file is empty, append the content with a main block
            with open(file_path, 'w') as f:
                f.write(content + '\n\nif __name__ == "__main__":\n    pass\n')
    elif type == 'python_function':
        with open(file_path, 'a') as f:
            f.write(content)

def clear_file(file_path):
    """
    Clears the content of the specified file.
    
    Args:
        file_path (str): The path to the file to be cleared.
    """
    with open(file_path, 'w') as f:
        f.write('')  # Write an empty string to clear the file