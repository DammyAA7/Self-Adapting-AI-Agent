"""
This script generates a prompt for creating unit tests for a function.
"""
from Utilities.write_to_file import write_to_file, clear_file

python_dir = '/usr/bin/python3'
folder_dir = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/" 

# Read the updated prompt from file
with open('Test_Driven_Development/prompt.txt', 'r') as f:
    prompt = f.read()

with open('functions.py', 'r') as f:
    functions_code = f.read()

with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
    test_driven_code = f.read()

def generateTestDrivenCases(client, requirements, reinforced_requirement=None):
    # Convert to OpenAI format
    user_content = f'''You are given these verified safe functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}

Requirements: {requirements}

Test driven code already generated: {test_driven_code if test_driven_code else "Not available"}

If you are given a reinforced requirement, you must use it to fix the already generated test cases. Keep all the tests but make the adjustments where necessary or add new test case that satisfy the requirement and return the new modified script.

{"Reinforced requirement: " + reinforced_requirement if reinforced_requirement else ""}'''

    generator_messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_content}
    ]

    # Using Azure OpenAI
    generator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        max_tokens=10000,
        messages=generator_messages,
        temperature=0.7
    )
    clear_file(folder_dir + 'Test_Driven_Development/testDrivenCases.py')
    test_cases = generator_response.choices[0].message.content
    write_to_file('python_function', folder_dir + 'Test_Driven_Development/testDrivenCases.py', test_cases)
     
    return test_cases