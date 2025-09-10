"""

"""

from pydantic import BaseModel

# Read the new prompt from file
with open('Adjudicator/adjudicator.txt', 'r') as f:
    adjudicator_prompt = f.read()
    
class OutputStructure(BaseModel):
    judgement: bool
    code_requirement_suggestion: str
    unit_requirement_suggestion: str

def adjudicate(client, test_case_results):
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
        {"role": "user", "content": test_case_results},
        
    ]

    # Using OpenAI with structured output
    import json
    
    # Add structure instructions to the prompt
    structured_prompt = f"""{adjudicator_prompt}

IMPORTANT: You MUST respond with ONLY a valid JSON object, no other text before or after. Use exactly these fields:
- judgement: boolean (true/false)
- code_requirement_suggestion: string
- unit_requirement_suggestion: string

Example format:
{{"judgement": true, "code_requirement_suggestion": "", "unit_requirement_suggestion": ""}}

ONLY output the JSON object, nothing else."""
    
    adjudicator_messages[0]["content"] = structured_prompt
    
    adjudicator_response = client.chat.completions.create(
        model="gpt-4-0613",
        messages=adjudicator_messages,
        temperature=0.3
        # response_format={"type": "json_object"}
    )
    
    # Parse the JSON response
    try:
        response_content = adjudicator_response.choices[0].message.content
        result = json.loads(response_content)
        return OutputStructure(**result)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in adjudicator: {e}")
        print(f"Response content: {adjudicator_response.choices[0].message.content}")
        return OutputStructure(
            judgement=False,
            code_requirement_suggestion="",
            unit_requirement_suggestion=""
        )
    except Exception as e:
        print(f"Unexpected error in adjudicator: {e}")
        return OutputStructure(
            judgement=False,
            code_requirement_suggestion="",
            unit_requirement_suggestion=""
        )