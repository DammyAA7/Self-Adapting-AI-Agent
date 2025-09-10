'''
This functions produces a function descriptor with examples that is inserted into the initial stage LLM prompt
'''

# Read the new prompt from file
with open('Prompt_Gen/prompt.txt', 'r') as f:
    generator_prompt = f.read()

def generateFunctionDescriptor(client, function, tool_descriptor):
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": function + tool_descriptor}
    ]

    generator_response = client.chat.completions.create(
            model="gpt-4-0613",
            messages=generator_messages
        )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction
