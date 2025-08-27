"""
This script generates a prompt for creating unit tests for a function.
"""

def generateTestCases(client, requirements, reinforced_requirement=None):
    # Read files inside the function to avoid import-time errors
    with open('Unit_Test/prompt.txt', 'r') as f:
        generator_prompt = f.read()
    
    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
    except FileNotFoundError:
        functions_code = "# No functions available yet"
    
    try:
        with open('Unit_Test/unitTest.py', 'r') as f:
            unit_test_code = f.read()
    except FileNotFoundError:
        unit_test_code = ""
    
    try:
        with open('Test_Driven_Development/testDrivenCases.py', 'r') as f:
            test_driven_code = f.read()
    except FileNotFoundError:
        test_driven_code = "# No test driven cases available"
    # Convert to OpenAI format
    user_content = f'''You are given these verified helper functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}

Requirements: {requirements}

These are the test driven code already generated: {test_driven_code}

If you are given a reinforced requirement, you must use it to fix the already generated test cases. Keep all the tests but make the adjustments where necessary and return the new modified script.

{"Reinforced requirement: " + reinforced_requirement if reinforced_requirement else ""}

Unit test code: {unit_test_code if unit_test_code else "Not available"}'''

    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": user_content}
    ]

    # Using Azure OpenAI
    generator_response = client.chat.completions.create(
        model="o4-mini",  # Azure deployment name
        max_completion_tokens=5000,
        # temperature=0.7,
        messages=generator_messages
    )
     
    return generator_response.choices[0].message.content