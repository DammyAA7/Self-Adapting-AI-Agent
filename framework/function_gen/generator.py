'''
Function that generates Python code based on a prompt using OpenAI's API.
'''

# Read the new prompt from file
with open('function_gen/function.txt', 'r') as f:
    generator_prompt = f.read()

#Read available functions from file
with open('functions.py', 'r') as f:
    functions_code = f.read()

def generate_function_code(client, test_driven_code, project_context=None):
    # Build user content with optional project context
    user_content = f'''CRITICAL: READ THIS FIRST - Existing Functions You MUST Use:
====================================================================
The following functions already exist in functions.py. Before writing ANY code, analyze if ANY of these functions can be reused.
If they relate to your task, YOU MUST import and use them - reimplementing existing functionality is FORBIDDEN.

functions.py content:
{functions_code}

COMPOSITION REQUIREMENT: If the above contains ANY function related to this task (matrix operations, calculations, validations, data processing, etc.), you MUST:
1. Import that function: `from functions import existing_function_name`
2. Call it in your implementation
3. Only add NEW logic not covered by existing functions

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
EXTERNAL PROJECT CODEBASE (DEPENDENCIES - USE BUT DO NOT MODIFY)
{'='*70}

⚠️  CRITICAL BOUNDARY:
The code below is from the EXISTING external codebase.
These are DEPENDENCIES you can call/use, not code to modify.

YOUR SCOPE:
✅ GENERATE: The NEW function specified in requirements
❌ DON'T MODIFY: External classes (Warehouse, Product, StockLevel, etc.)
✅ IMPORT AND CALL: External classes and their methods
❌ DON'T REIMPLEMENT: Functionality that exists in external classes

EXTERNAL CODEBASE:
{project_context}

{'='*70}

CRITICAL REQUIREMENTS - You MUST follow these rules:
1. **USE EXACT FILE PATHS**: When you see file paths in context above, use complete absolute paths in your code, NOT relative paths.

2. **NO NEW FILES**: Work with existing files shown in context. Do not create new files unless explicitly requested.

3. **REUSE EXISTING DATA**: All data files (CSV, JSON, text, etc.) shown above contain real project data - use their exact paths.

4. **FOLLOW PROJECT PATTERNS**: Match the coding style, imports, and patterns from external code.

5. **RESPECT EXTERNAL CLASS CONSTRAINTS**: When calling external classes, follow their exact parameter requirements (formats, types, etc.).

EXAMPLES:
- If context shows "CSV FILE: /home/user/project/data.csv" → Use: DATA_PATH = "/home/user/project/data.csv"
- If StockLevel.__init__ expects datetime "%Y-%m-%d %H:%M:%S" → Use: "2024-06-01 00:00:00"
- NOT: DATA_PATH = "data.csv" or datetime = "2024-06-01" (WRONG formats)

'''

    user_content += f'Generate a Python function based on the following Test driven code: {test_driven_code}'

    # Convert messages for OpenAI format
    generator_messages = [
        {"role": "system", "content": generator_prompt},
        {"role": "user", "content": user_content}
    ]

    # Using Azure OpenAI
    # Note: Azure uses deployment names, not model names
    generator_response = client.chat.completions.create(
        model="gpt-4.1",  # Azure deployment name
        max_tokens=5000,
        temperature=0.7,
        messages=generator_messages
    )
    
    function = generator_response.choices[0].message.content
    formattedFunction = f"\n\n{function}\n"
    return formattedFunction