
from pydantic import BaseModel

# Read the new prompt from file
with open('Impact_Analysis/prompt.txt', 'r') as f:
    prompt = f.read()
# Read the function code from file
with open('functions.py', 'r') as f:
    function_code = f.read()
    
class OutputStructure(BaseModel):
    judgement: bool
    func_name: str
    function_edit: str

def analyze(client, fucntion_requirement):
    """
    Analyzes the function code against the requirements and available code.
    """
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"List of all available functions: {function_code}"},
        {"role": "user", "content": fucntion_requirement}
    ]

    response = client.responses.parse(
        model="o3-2025-04-16",
        input=messages, 
        text_format=OutputStructure
    )

    return response.output_parsed