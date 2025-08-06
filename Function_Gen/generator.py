'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

# Read the new prompt from file
with open('Function_Gen/function.txt', 'r') as f:
    generator_prompt = f.read()

#Read available functions from file
with open('functions.py', 'r') as f:
    functions_code = f.read()

def generate_function_code(client, test_driven_code):
    generator_messages = [
        {"role": "assistant", "content": generator_prompt},
        {"role": "user", "content": f'These are the functions already being used. You\'re given this as reference to help you generate a new function. Function.py : {functions_code}'},
        {"role": "user", "content": f"Generate a Python function based on the following Test driven code: {test_driven_code}"}
    ]

    generator_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        messages=generator_messages,
    )
    
    function = generator_response.content[0].text
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction