'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

def generate_function_code(client, function_requirement, reinforced_requirement=None, functions_code_param=None):
    # Read files inside the function to avoid import-time errors
    with open('Function_Gen/function.txt', 'r') as f:
        generator_prompt = f.read()
    
    # Read available functions from file with error handling
    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
        if not functions_code.strip():
            functions_code = "# No functions available yet"
    except (FileNotFoundError, IOError):
        functions_code = "# No functions available yet"
    
    # Convert messages for OpenAI format - matching Prototype-III structure
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": f'These are the functions already being used. You\'re given this as reference to help you generate a new function. Function.py : {functions_code}'},
        {"role": "user", "content": f"Generate a Python function based on the following requirement:{function_requirement}"},
        {"role": "user", "content": "If you are given a reinforced requirement, you must also use it when generating the function."},
        {"role": "user", "content": f"Reinforced requirement: {reinforced_requirement}" if reinforced_requirement else ""},
        {"role": "user", "content": "If you are given a function code, you must use it to fix the already generated function. Keep all the code but make the adjustments where necessary and return the new modified code."},
        {"role": "user", "content": f"Function code: {functions_code_param}" if functions_code_param else "Not available"}
    ]

    # Using Azure OpenAI
    # Note: Azure uses deployment names, not model names
    generator_response = client.chat.completions.create(
        model="o4-mini",  # Azure deployment name
        max_completion_tokens=5000,
        messages=generator_messages
        # temperature=0.7  # o4-mini only supports default temperature (1)
    )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction