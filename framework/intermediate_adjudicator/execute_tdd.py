import subprocess
import sys
import os

# Use the current Python interpreter (which has pytest installed)
python_path = sys.executable
folder_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

def execute():
    print("Running Test driven code...")
    # Use pytest to run the tests and get proper output
    cmd_test = [python_path, "-m", "pytest", "test_driven_development/testDrivenCases.py", "-v", "--tb=short"]
    
    # Run with correct working directory so imports work
    result = subprocess.run(cmd_test, 
                          capture_output=True, 
                          text=True, 
                          timeout=30,
                          cwd=folder_path)  # Set working directory
    
    # Combine stdout and stderr for complete output
    output = ""
    if result.stdout:
        output += result.stdout
    if result.stderr:
        output += "\nSTDERR:\n" + result.stderr
    
    # If still empty, return a message
    if not output.strip():
        return "No output from test execution"
    
    return output
    