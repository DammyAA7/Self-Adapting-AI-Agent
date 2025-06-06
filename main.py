import subprocess
import os
from openai import OpenAI
import json

os.environ["OPENAI_API_KEY"] = "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"

# Define directory paths
python_dir = '/usr/local/bin/python3'
folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

# Define tools for the LLM
tools = [
    {
        "type": "function",
        "function": {
            "name": "addition",
            "description": "Adds two numbers and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The first addend."},
                    "b": {"type": "number", "description": "The second addend."}
                },
                "required": ["a", "b"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "subtraction",
            "description": "Subtracts the second number from the first and returns the result.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "The minuend."},
                    "b": {"type": "number", "description": "The subtrahend."}
                },
                "required": ["a", "b"]
            }
        }
    }
]

#Define prompt for the LLM and input messages
input_messages = [
    {"role": "system", "content": "You are a calculator bot that can add or subtract numbers."},
    {"role": "user", "content": "What's 47 minus 21?"}
]

# Function to call functions.py using subprocess
def call_function(func_name, arg1, arg2):
    cmd = [python_dir, folder_dir + "functions.py", func_name, f"{arg1},{arg2}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr.strip()}"

if __name__ == "__main__":
    # Assign OpenAI API key 
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    messages=input_messages,
    tools=tools,
    tool_choice="auto"
)
#check if model wants to use tools
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        output = call_function(function_name, function_args['a'], function_args['b'])
        messages_with_result = input_messages + [
            response.choices[0].message,
            {"role": "tool", "content": str(output), "tool_call_id": tool_call.id}
        ]
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages_with_result,
            tools=tools
        )
        print("Final response:", final_response.choices[0].message.content)
    else:
        print(response.choices[0].message.content)
    
    print(f"Result from functions.py: {output}")
