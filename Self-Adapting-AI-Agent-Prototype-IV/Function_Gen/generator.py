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
    # Convert messages for OpenAI format
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": f'These are the functions already being used. You\'re given this as reference to help you generate a new function. Function.py : {functions_code}\n\nGenerate a Python function based on the following Test driven code: {test_driven_code}'}
    ]

    # Using Azure OpenAI
    # Note: Azure uses deployment names, not model names
    generator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        max_tokens=5000,
        messages=generator_messages,
        temperature=0.7
    )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction