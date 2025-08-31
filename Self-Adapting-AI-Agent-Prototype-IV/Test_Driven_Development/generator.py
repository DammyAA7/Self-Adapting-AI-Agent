"""
This script generates a prompt for creating unit tests for a function.
"""
from Utilities.write_to_file import write_to_file, clear_file
import sys
import os

python_dir = sys.executable
folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/" 

# Don't read at module level - read inside function
# with open('Test_Driven_Development/prompt.txt', 'r') as f:
#     prompt = f.read()

# with open('functions.py', 'r') as f:
#     functions_code = f.read()

# with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
#     test_driven_code = f.read()

def generateTestDrivenCases(client, requirements, reinforced_requirement=None, project_context=None):

    with open('Test_Driven_Development/prompt.txt', 'r') as f:
        prompt = f.read()
    
    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
    except FileNotFoundError:
        functions_code = "# No functions available yet"
    
    # Read test_driven_code inside the function
    try:
        with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
            test_driven_code = f.read()
    except:
        test_driven_code = ""
    
    # Convert to OpenAI format
    user_content = f'''You are given these verified safe functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}

'''

    # Add project context if available
    if project_context:
        user_content += f'''PROJECT KNOWLEDGE:
================
{project_context}

You have full visibility of the project above. When generating test cases:
- Test with actual data structures from the project (CSV columns, JSON keys, etc.)
- Follow testing patterns you see in the project
- Create tests that verify integration with existing code
- Use realistic test data based on what you see in the project files

'''

    user_content += f'''Requirements: {requirements}

Test driven code already generated: {test_driven_code if test_driven_code else "Not available"}

If you are given a reinforced requirement, you must use it to fix the already generated test cases. Keep all the tests but make the adjustments where necessary or add new test case that satisfy the requirement and return the new modified script.

{"Reinforced requirement: " + reinforced_requirement if reinforced_requirement else ""}'''

    generator_messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content}
    ]

    # Using Azure OpenAI
    generator_response = client.chat.completions.create(
        model="o4-mini",  # Azure deployment name
        max_completion_tokens=10000,
        # temperature=0.7,
        messages=generator_messages
    )
    # Don't clear and append - just write the complete content
    test_cases = generator_response.choices[0].message.content
    # Write complete content, not append
    with open(folder_dir + 'Test_Driven_Development/testDrivenCases.py', 'w') as f:
        f.write(test_cases)
     
    return test_cases