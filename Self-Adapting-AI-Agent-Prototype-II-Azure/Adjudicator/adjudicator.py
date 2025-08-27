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
    structured_prompt = f"{adjudicator_prompt}\n\nYou must respond with a JSON object with exactly these fields:\n- judgement: boolean (true/false)\n- code_requirement_suggestion: string\n- unit_requirement_suggestion: string"
    
    adjudicator_messages[0]["content"] = structured_prompt
    
    adjudicator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        messages=adjudicator_messages,
        temperature=0.3,  # o4-mini only supports default temperature (1)
        response_format={"type": "json_object"}
    )
    
    # Parse the JSON response
    try:
        response_content = adjudicator_response.choices[0].message.content
        print(f"DEBUG - Adjudicator raw response: {response_content[:500]}")  # Debug output
        result = json.loads(response_content)
        
        # Handle different field names that the AI might return
        if 'unit_test_requirement_suggestion' in result and 'unit_requirement_suggestion' not in result:
            result['unit_requirement_suggestion'] = result.pop('unit_test_requirement_suggestion')
        
        # Ensure all required fields exist with defaults if needed
        result.setdefault('judgement', False)
        result.setdefault('code_requirement_suggestion', '')
        result.setdefault('unit_requirement_suggestion', '')
        
        return OutputStructure(**result)
    except Exception as e:
        print(f"ERROR - Adjudication parsing failed: {e}")
        print(f"ERROR - Raw response was: {adjudicator_response.choices[0].message.content[:500]}")
        # Fallback if JSON parsing fails
        return OutputStructure(
            judgement=False,
            code_requirement_suggestion="Failed to parse adjudication response",
            unit_requirement_suggestion="Please retry with clearer requirements"
        )