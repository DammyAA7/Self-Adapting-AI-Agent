'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

# Read the new prompt from file
with open('Function_Gen/function.txt', 'r') as f:
    generator_prompt = f.read()

def generate_function_code(client, function_requirement):
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": function_requirement}
    ]

    generator_response = client.chat.completions.create(
            model="o4-mini-2025-04-16",
            messages=generator_messages
        )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction