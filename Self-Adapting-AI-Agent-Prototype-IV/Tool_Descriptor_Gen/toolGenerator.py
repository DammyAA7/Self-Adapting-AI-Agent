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
        model="gpt-4.1",  # Azure deployment name
        messages=generator_messages
    )

    tools_code = generator_response.choices[0].message.content
    # Split the code by lines, add tab indentation to each line, and rejoin
    formatted_lines = ["    " + line for line in tools_code.strip().split("\n")]
    formatted_tools_code = "\n" + "\n".join(formatted_lines) + "\n"
    return formatted_tools_code