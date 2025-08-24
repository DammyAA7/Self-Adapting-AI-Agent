"""

"""

from Intermidiate_Adjudicator.execute_tdd import execute
from pydantic import BaseModel

# Read the new prompt from file
with open('Adjudicator/adjudicator.txt', 'r') as f:
    adjudicator_prompt = f.read()
    
class OutputStructure(BaseModel):
    judgement: bool
    requirement_suggestion: str

def intermidiate_adjudicate(client):
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
    test_driven_results = execute()
    
    adjudicator_messages = [
        {"role": "system", "content": adjudicator_prompt},
        {"role": "user", "content": test_driven_results},
        
    ]

    # Using OpenAI with structured output
    import json
    
    # Add structure instructions to the prompt
    structured_prompt = f"{adjudicator_prompt}\n\nYou must respond with a JSON object with exactly these fields:\n- judgement: boolean (true/false)\n- requirement_suggestion: string"
    
    adjudicator_messages[0]["content"] = structured_prompt
    
    adjudicator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        messages=adjudicator_messages,
        temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    # Parse the JSON response
    try:
        result = json.loads(adjudicator_response.choices[0].message.content)
        return OutputStructure(**result)
    except:
        # Fallback if JSON parsing fails
        return OutputStructure(
            judgement=False,
            requirement_suggestion="Failed to parse TDD adjudication response"
        )