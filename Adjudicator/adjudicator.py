"""

"""

# Read the new prompt from file
with open('prompts/adjudicator.txt', 'r') as f:
    adjudicator_prompt = f.read()
    


def adjudicate(client, user_prompt, function_requirments, function_code, tool_descriptor, prompt_descriptor):
    """
    Adjudicates the function code against the requirements and descriptors.
    
    Args:
        client: The OpenAI client instance.
        user_prompt (str): The original user prompt.
        function_requirments (str): The requirements for the function.
        function_code (str): The generated function code.
        tool_descriptor (str): The description of the tool.
        prompt_descriptor (str): The description of the prompt.
        
    Returns:
        str: The adjudication result.
    """
    adjudicator_messages = [
        {"role": "system", "content": adjudicator_prompt},
        {"role": "user", "content": f"User Prompt: {user_prompt}\n\nFunction Requirements: {function_requirments}\n\nFunction Code:\n{function_code}\n\nTool Descriptor: {tool_descriptor}\n\nPrompt Descriptor: {prompt_descriptor}"}
    ]

    adjudicator_response = client.chat.completions.create(
        model="gpt-4o",
        messages=adjudicator_messages,
        max_tokens=5,  # Limit tokens to force concise response
        temperature=0  # Make response deterministic
    )

    return adjudicator_response.choices[0].message.content