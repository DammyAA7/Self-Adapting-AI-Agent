'''
Function that generates tool definitions based on a prompt using OpenAI's API.
'''
def generate_tool_definitions(client, function):
    with open('Tool_Descriptor_Gen/tools.txt', 'r') as f:
        generator_prompt = f.read()
    
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": function}
    ]

    generator_response = client.chat.completions.create(
        model="o4-mini",  # Azure deployment name
        messages=generator_messages
    )

    tools_code = generator_response.choices[0].message.content
    # Return the raw JSON directly without adding indentation
    return tools_code