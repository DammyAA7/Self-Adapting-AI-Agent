import subprocess

python_path = '/usr/bin/python3'
folder_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/Self-Adapting-AI-Agent-Prototype-IV/"
def execute():
   
    print("Running Test driven code...")
    cmd_test = [python_path, folder_path + "Test_Driven_Development/testDrivenCases.py"]

    result = subprocess.run(cmd_test, capture_output=True, text=True, timeout=30)

    return result.stdout
    