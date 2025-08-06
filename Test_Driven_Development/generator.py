"""
This script generates a prompt for creating unit tests for a function.
"""
from Utilities.write_to_file import write_to_file, clear_file

python_dir = '/usr/local/bin/python3'
folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

# Read the updated prompt from file
with open('Test_Driven_Development/prompt.txt', 'r') as f:
    prompt = f.read()

with open('functions.py', 'r') as f:
    functions_code = f.read()

with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
    test_driven_code = f.read()

def generateTestDrivenCases(client, requirements, reinforced_requirement=None):
    generator_messages = [
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": f'You are given these verified safe functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}'},
        {"role": "user", "content": requirements},
        {"role": "user", "content": f'These are the test driven code already generated: {test_driven_code}' if test_driven_code else "Not available"},
        {"role": "user", "content": "If you are given a reinforced requirement, you must use it to fix the already generated test cases. Keep all the tests but make the adjustments where necessary or add new test case that statisfy the requirment and return the new modified script."},
        {"role": "user", "content": f"Reinforced requirement: {reinforced_requirement}" if reinforced_requirement else ""}
    ]

    generator_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10000,
        messages=generator_messages,
    )
    clear_file(folder_dir + 'Test_Driven_Development/testDrivenCases.py')
    test_cases = generator_response.content[0].text
    write_to_file('python_function', folder_dir + 'Test_Driven_Development/testDrivenCases.py', test_cases)
     
    return generator_response.content[0].text