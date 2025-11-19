"""
This script generates a prompt for creating unit tests for a function.
"""

def generateTestCases(client, requirements, reinforced_requirement=None, project_context=None):
    # Read files inside the function to avoid import-time errors
    with open('unit_test/prompt.txt', 'r') as f:
        generator_prompt = f.read()
    
    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
    except FileNotFoundError:
        functions_code = "# No functions available yet"
    
    try:
        with open('unit_test/unitTest.py', 'r') as f:
            unit_test_code = f.read()
    except FileNotFoundError:
        unit_test_code = ""
    
    try:
        with open('test_driven_development/testDrivenCases.py', 'r') as f:
            test_driven_code = f.read()
    except FileNotFoundError:
        test_driven_code = "# No test driven cases available"
    # Convert to OpenAI format
    user_content = f'''You are given these verified helper functions as reference to assist with test data creation and setup. Available functions from functions.py: {functions_code}

'''

    # Add project context if available
    if project_context:
        user_content += f'''PROJECT KNOWLEDGE:
================
{project_context}

You have full visibility of the project above. When generating unit tests:
- Test with actual data structures from the project (CSV columns, JSON keys, etc.)
- Follow unit testing patterns you see in the project
- Create tests that verify integration with existing code
- Use realistic test data based on what you see in the project files

'''

    user_content += f'''Requirements: {requirements}

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
        model="gpt-4.1",  # Azure deployment name
        max_tokens=5000,
        temperature=0.7,
        messages=generator_messages
    )

    # AUTO-FIX: Fix common syntax errors before returning
    unit_test_code = generator_response.choices[0].message.content
    unit_test_code = fix_common_syntax_errors(unit_test_code)

    return unit_test_code

def fix_common_syntax_errors(code: str) -> str:
    """Fix common syntax errors in generated test code"""
    lines = code.split('\n')
    fixed_lines = []

    for line in lines:
        # Fix unclosed parenthesis in sys.path.insert with nested dirname()
        if 'sys.path.insert' in line and line.count('(') > line.count(')'):
            # Count missing closing parens
            missing = line.count('(') - line.count(')')
            line = line.rstrip() + (')' * missing)
            print(f"  ✓ Auto-fixed unclosed parenthesis in sys.path line")

        fixed_lines.append(line)

    return '\n'.join(fixed_lines)