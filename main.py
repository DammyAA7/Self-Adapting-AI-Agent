import subprocess

python_dir = '/usr/local/bin/python3'

directory = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

# Function to call functions.py using subprocess
def call_function(func_name, arg1, arg2):
    cmd = [python_dir, directory + "functions.py", func_name, f"{arg1},{arg2}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr.strip()}"

if __name__ == "__main__":
    output = call_function("addition", 10, 25)
    print(f"Result from functions.py: {output}")
