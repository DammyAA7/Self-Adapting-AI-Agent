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
        user_content += f'''
     
======================================
EXTREMELY IMPORANT IMPORT RULES, NEVER SKIP THIS ---   

IMPORTANT: Replace the class/function names above with the ACTUAL names you need from the files shown below.
Do NOT hardcode 'XYZ/ABC/IFG' or use placeholder names - use the real class names from the analyzed files!
ALWAYS IMPORT FROM EXTERNAL PROJECT CODEBASE LIKE THIS:

RIGHT: from dataset.ABC.XYZ import IFG  # ✅ FOLLOW THIS STRUCTURE (TAKE THIS AS EXAMPLE NOT HARDCODED)
RIGHT: from dataset.inventory_replenishment.warehouse import Warehouse # ✅ CORRECT EXAMPLE (TAKE THIS AS EXAMPLE, YOU CAN SEE FIRST IS dataset., then it is directory name, then the file)
WRONG: from dataset.XYZ import XYZ  # ❌ Don't use placeholders!
WRONG: from warehouse import Warehouse # ❌ Don't Import Directly!
WRONG: from product import Product # ❌ Don't Import Directly!
        
IMPORTANT: If any file path is needed, always use the FULL ABSOLUTE paths shown in "FULL PATH" sections above.

Example: (CRITICAL: Always use absolute paths from the FILE PATHS section above):
WRONG: file_path = Path(__file__).parent / "data.csv"
RIGHT: file_path = "/absolute/path/to/dataset/patient_risk_analyzer/data.csv"  # Use actual FULL PATH shown above

======================================
     
{'='*70}
EXTERNAL PROJECT CODEBASE (DEPENDENCIES - USE BUT DO NOT TEST)
{'='*70}

⚠️  CRITICAL BOUNDARY:
The code below is from the EXISTING external codebase.
These are DEPENDENCIES, not test subjects.

YOUR SCOPE:
✅ TEST: The NEW function being generated
❌ DON'T TEST: External classes below (Warehouse, Product, StockLevel, etc.)
✅ USE: External classes in test fixtures
❌ DON'T CREATE: Tests named test_StockLevel_*, test_Warehouse_*, etc.

IMPORTANT: When using external classes in fixtures, follow their exact parameter constraints (check type hints, docstrings, formats).

EXTERNAL CODEBASE:
{project_context}

{'='*70}
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

    # AUTO-FIX: Check for common syntax error (unclosed parenthesis in sys.path.insert)
    test_cases = fix_common_syntax_errors(test_cases)

    # Write complete content, not append
    with open(folder_dir + 'test_driven_development/testDrivenCases.py', 'w') as f:
        f.write(test_cases)

    return test_cases

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