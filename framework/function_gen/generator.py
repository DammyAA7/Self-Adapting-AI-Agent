'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

# Read the new prompt from file
with open('function_gen/function.txt', 'r') as f:
    generator_prompt = f.read()

#Read available functions from file
with open('functions.py', 'r') as f:
    functions_code = f.read()

def generate_function_code(client, test_driven_code, project_context=None):
    # Build user content with optional project context
    user_content = f'These are the functions already being used. You\'re given this as reference to help you generate a new function. Function.py : {functions_code}\n\n'

    # Add project context if available
    if project_context:
        user_content += f'''PROJECT KNOWLEDGE:
================
{project_context}

CRITICAL REQUIREMENTS - You MUST follow these rules:
1. **USE EXACT FILE PATHS**: When you see any file paths in the project context above (e.g., "CSV FILE: /path/to/data.csv", "JSON FILE: /path/to/config.json", "PYTHON FILE: /path/to/module.py"), you MUST use the complete absolute paths in your code, NOT relative paths or generic filenames.

2. **NO NEW FILES**: Work with existing files shown in the project context. Do not create new files unless explicitly requested by the user.

3. **REUSE EXISTING DATA**: All data files (CSV, JSON, text, etc.) shown above contain real project data - use their exact paths and existing structures.

4. **FOLLOW PROJECT PATTERNS**: Match the coding style, imports, and patterns you see in existing project files.

EXAMPLES:
- If context shows "CSV FILE: /home/user/project/data.csv" → Use: DATA_PATH = "/home/user/project/data.csv"
- If context shows "JSON FILE: /home/user/config/settings.json" → Use: CONFIG_PATH = "/home/user/config/settings.json"  
- If context shows "PYTHON FILE: /home/user/utils/helpers.py" → Import from exact path or use existing functions shown
- NOT: DATA_PATH = "data.csv" or CONFIG_PATH = "settings.json" (these are WRONG)

'''

    user_content += f'Generate a Python function based on the following Test driven code: {test_driven_code}'

    # Convert messages for OpenAI format
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": user_content}
    ]

    # Using Azure OpenAI
    # Note: Azure uses deployment names, not model names
    generator_response = client.chat.completions.create(
        model="o4-mini",  # Azure deployment name
        max_completion_tokens=5000,
        # temperature=0.7,
        messages=generator_messages
    )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction