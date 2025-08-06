"""
This script generates a prompt for creating unit tests for a function.
"""

# Read the updated prompt from file
with open('Unit_Test/prompt.txt', 'r') as f:
    generator_prompt = f.read()

with open('functions.py', 'r') as f:
    functions_code = f.read()

with open('Unit_Test/unitTest.py', 'r') as f:
    unit_test_code = f.read()

with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
    test_driven_code = f.read()

def generateTestCases(client, requirements, reinforced_requirement=None):
    generator_messages = [
        {"role": "assistant", "content": generator_prompt},
        {"role": "user", "content": f'You are given these verified helper functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}'},
        {"role": "user", "content": requirements},
        {"role": "user", "content": f'These are the test driven code already generated: {test_driven_code}'},
        {"role": "user", "content": "If you are given a reinforced requirement, you must use it to fix the already generated test cases. Keep all the tests but make the adjustments where necessary and return the new modified script."},
        {"role": "user", "content": f"Reinforced requirement: {reinforced_requirement}" if reinforced_requirement else ""},
        {"role": "user", "content": f"Unit test code: {unit_test_code}" if unit_test_code else "Not available"}
    ]

    generator_response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=5000,
        messages=generator_messages,
    )
     
    return generator_response.content[0].text