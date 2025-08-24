from Unit_Test.generator import generateTestCases
from Utilities.write_to_file import write_to_file, clear_file
import subprocess
import sys
import os

python_path = sys.executable  # Use current Python interpreter
folder_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/"

def generate_execute_unit_tests(client, function_requirement, unit_test_reinforced_requirement=None):
    """
    Executes unit tests for the given function requirement using the OpenAI client.
    
    Args:
        client: An instance of the OpenAI client.
        function_requirement: A string describing the function requirement for which to generate unit tests.
        unit_test_reinforced_requirement: Optional reinforced requirements for test generation.
        
    Returns:
        The test execution results as a string.
    """

    with open('Unit_Test/unitTest.py', 'r') as f:
        file_unit_test_code = f.read()

    if not file_unit_test_code or unit_test_reinforced_requirement:
        print("Generating unit test cases...")
        unit_test_code = generateTestCases(client, function_requirement, unit_test_reinforced_requirement)
        clear_file('Unit_Test/unitTest.py')
        write_to_file('python_function', folder_path + 'Unit_Test/unitTest.py', unit_test_code)

    print("Running Unit Tests...")
    
    # Use pytest to run the tests
    cmd = [python_path, "-m", "pytest", folder_path + "Unit_Test/unitTest.py", "-v", "--tb=short"]
    
    # Set working directory for proper imports
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=folder_path)
    
    # Return both stdout and stderr for complete output
    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += "\nERRORS:\n" + result.stderr
    
    # If no output at all, return a message
    if not output.strip():
        output = "No output from test execution"
    
    return output
