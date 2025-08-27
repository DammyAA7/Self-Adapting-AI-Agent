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
        model="o4-mini",  # Azure deployment name
        messages=adjudicator_messages,
        # temperature=0.3,
        response_format={"type": "json_object"}
    )
    
    # Parse the JSON response
    try:
        response_content = adjudicator_response.choices[0].message.content
        result = json.loads(response_content)
        
        # Handle different field names the AI might return
        if 'code_requirement_suggestion' in result and 'requirement_suggestion' not in result:
            result['requirement_suggestion'] = result.get('code_requirement_suggestion', '')
        elif 'unit_test_requirement_suggestion' in result and 'requirement_suggestion' not in result:
            result['requirement_suggestion'] = result.get('unit_test_requirement_suggestion', '')
        
        # Ensure required fields exist
        if 'requirement_suggestion' not in result:
            result['requirement_suggestion'] = ''
        
        # Check if all tests passed based on the test results
        if "passed" in test_driven_results.lower() and "failed" not in test_driven_results.lower():
            # If all tests passed, override to success
            return OutputStructure(
                judgement=True,
                requirement_suggestion=""
            )
        
        return OutputStructure(
            judgement=result.get('judgement', False),
            requirement_suggestion=result.get('requirement_suggestion', '')
        )
    except Exception as e:
        # If we can't parse JSON, check the test results directly
        if test_driven_results and "passed" in test_driven_results.lower():
            # Check if all tests passed
            if "failed" not in test_driven_results.lower() and "error" not in test_driven_results.lower():
                return OutputStructure(
                    judgement=True,
                    requirement_suggestion=""
                )
        
        # Fallback if JSON parsing fails
        print(f"Adjudication parsing error: {e}")
        return OutputStructure(
            judgement=False,
            requirement_suggestion="Failed to parse TDD adjudication response"
        )