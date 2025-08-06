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

    adjudicator_response = client.responses.parse(
        model="o4-mini-2025-04-16",
        input=adjudicator_messages, 
        text_format=OutputStructure
    )

    return adjudicator_response.output_parsed