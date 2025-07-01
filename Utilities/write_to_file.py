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