from Unit_Test.generator import generateTestCases
from Utilities.write_to_file import write_to_file, clear_file
import subprocess


def generate_execute_unit_tests(client, function_requirement, python_path, folder_path):
    """
    Executes unit tests for the given function requirement using the OpenAI client.
    
    Args:
        client: An instance of the Anthropic client.
        function_requirement: A string describing the function requirement for which to generate unit tests.
        
    Returns:
        The generated unit test code as a string.
    """

    unit_test_code = generateTestCases(client, function_requirement)
    write_to_file('python_function', folder_path + 'Unit_Test/unitTest.py', unit_test_code)

    cmd = [python_path, folder_path + "Unit_Test/unitTest.py"]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    
    clear_file('Unit_Test/unitTest.py')
    clear_file('Unit_Test/functions.py')

    return result.stderr

    
