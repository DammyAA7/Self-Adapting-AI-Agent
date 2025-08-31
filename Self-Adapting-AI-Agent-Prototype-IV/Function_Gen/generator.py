'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

# Read the new prompt from file
with open('Function_Gen/function.txt', 'r') as f:
    generator_prompt = f.read()

def generate_function_code(client, function_requirement, reinforced_requirement=None, project_context=None):
    # Read existing functions to avoid conflicts and enable reuse
    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
    except FileNotFoundError:
        functions_code = "# No existing functions"
    
    # Build user content with optional project context
    user_content = f'These are the functions already being used. You\'re given this as reference to help you generate a new function. Function.py : {functions_code}\n\n'

    # Add project context if available
    if project_context:
        user_content += f'''PROJECT KNOWLEDGE:
================
{project_context}

You have full visibility of the project above. When generating the function:
- Reuse existing functions from the project when appropriate
- Follow the same coding patterns and style you see in the project
- Use the actual data structures (CSV columns, JSON keys) present in the project
- Ensure compatibility with the existing codebase

'''

    user_content += f'Function Requirement: {function_requirement}\n\n'
    
    if reinforced_requirement:
        user_content += f'Reinforced Requirement (must be followed): {reinforced_requirement}\n\n'
    
    user_content += 'Generate a Python function that fulfills the above requirement.'

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