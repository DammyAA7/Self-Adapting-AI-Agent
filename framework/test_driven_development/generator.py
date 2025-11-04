"""
This script generates a prompt for creating unit tests for a function.
"""
from utilities.write_to_file import write_to_file, clear_file
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

    with open('test_driven_development/prompt.txt', 'r') as f:
        prompt = f.read()

    try:
        with open('functions.py', 'r') as f:
            functions_code = f.read()
    except FileNotFoundError:
        functions_code = "# No functions available yet"

    # Read test_driven_code inside the function
    try:
        with open('test_driven_development/testDrivenCases.py', 'r') as f:
            test_driven_code = f.read()
    except:
        test_driven_code = ""
    
    # Convert to OpenAI format
    user_content = f'''CRITICAL: You are given these existing functions from functions.py. If ANY of these functions relate to the task requirements, your tests MUST verify that the new function imports and uses them (not reimplements them).

Available functions from functions.py:
{functions_code}

COMPOSITION TESTING RULE: If the above functions.py contains ANY function that could be a building block for this task, you MUST:
1. Write tests that verify the new function imports those existing functions
2. Use unittest.mock.patch to verify existing functions are called
3. Ensure tests FAIL if existing functions are NOT used when they should be

'''

    # Add project context if available
    if project_context:
        user_content += f'''PROJECT KNOWLEDGE:
================
{project_context}

CRITICAL REQUIREMENTS - You MUST follow these rules when generating test cases:
1. **USE TEMPORARY FILES FOR TESTS**: Create temporary files for testing, never modify actual project files. Use pytest fixtures, tempfile module, or tmp_path for safe testing.

2. **REPLICATE REAL DATA STRUCTURES**: Your test data should match the exact structure (columns, keys, formats) of the actual project files shown above, but in temporary test files.

3. **TEST FILE PATH PARAMETERS**: Ensure your tests verify that functions can accept file paths as parameters and work with different locations.

4. **FOLLOW PROJECT PATTERNS**: Match testing patterns, fixtures, and assertions you see in existing test files.

EXAMPLES FOR SAFE TESTING:
- If context shows CSV with columns "id,todo,status,priority" → Create temp CSV with same structure
- If context shows JSON with keys "name", "config" → Create temp JSON with same keys  
- Use: @pytest.fixture, tmp_path, tempfile.NamedTemporaryFile(), etc.
- Test that functions work with various file paths, not just hardcoded ones

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
        model="gpt-4.1",  # Azure deployment name
        max_tokens=10000,
        temperature=0.7,
        messages=generator_messages
    )
    # Don't clear and append - just write the complete content
    test_cases = generator_response.choices[0].message.content
    # Write complete content, not append
    with open(folder_dir + 'test_driven_development/testDrivenCases.py', 'w') as f:
        f.write(test_cases)
     
    return test_cases