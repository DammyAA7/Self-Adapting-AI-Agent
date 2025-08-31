from Unit_Test.generator import generateTestCases
from Utilities.write_to_file import write_to_file, clear_file
import subprocess
import sys
import os

python_path = sys.executable  # Use current Python interpreter
folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

def generate_execute_unit_tests(client, function_requirement, unit_test_reinforced_requirement=None, project_context=None):
    """
    Executes unit tests for the given function requirement using the OpenAI client.
    
    Args:
        client: An instance of the OpenAI client.
        function_requirement: A string describing the function requirement for which to generate unit tests.
        unit_test_reinforced_requirement: Optional reinforced requirements for test generation.
        project_context: Optional project context for context-aware test generation.

    Returns:
        The test execution results as a string.
    """

    with open('Unit_Test/unitTest.py', 'r') as f:
        file_unit_test_code = f.read()

    if not file_unit_test_code or unit_test_reinforced_requirement:
        print("Generating unit test cases...")
        unit_test_code = generateTestCases(client, function_requirement, unit_test_reinforced_requirement, project_context)
        clear_file('Unit_Test/unitTest.py')
        write_to_file('python_function', folder_path + 'Unit_Test/unitTest.py', unit_test_code)
        
        # Log the generated unit test content
        print(f"Generated {len(unit_test_code)} characters of unit test code")
        print("Unit test file written to: Unit_Test/unitTest.py")
        
        # Verify file was written
        with open('Unit_Test/unitTest.py', 'r') as f:
            written_content = f.read()
        print(f"Verified: unitTest.py now contains {len(written_content)} characters")
        
        # Show first 500 chars of the test
        if written_content:
            print("\n=== First 500 chars of generated unit tests ===")
            print(written_content[:500])
            print("=== End of preview ===\n")
    else:
        print(f"Using existing unit tests ({len(file_unit_test_code)} characters)")

    print("Running Unit Tests...")
    
    # Check if unitTest.py exists and has content before running
    test_file_path = folder_path + "Unit_Test/unitTest.py"
    if os.path.exists(test_file_path):
        with open(test_file_path, 'r') as f:
            test_content = f.read()
        print(f"Running pytest on unitTest.py ({len(test_content)} characters)")
    else:
        print("WARNING: unitTest.py does not exist!")
    
    # Use pytest to run the tests
    cmd = [python_path, "-m", "pytest", test_file_path, "-v", "--tb=short"]
    print(f"Executing command: {' '.join(cmd)}")
    
    # Set working directory for proper imports
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=folder_path)
    
    print(f"Pytest exit code: {result.returncode}")
    
    # Return both stdout and stderr for complete output
    output = ""
    if result.stdout:
        output += result.stdout
        print(f"Pytest stdout length: {len(result.stdout)} characters")
    if result.stderr:
        output += "\nERRORS:\n" + result.stderr
        print(f"Pytest stderr length: {len(result.stderr)} characters")
    
    # If no output at all, return a message
    if not output.strip():
        output = "No output from test execution"
        print("WARNING: No output from pytest execution")
    
    return output
