import subprocess
import os
from openai import OpenAI
import json

os.environ["OPENAI_API_KEY"] = "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"

# Define directory paths
python_dir = '/usr/local/bin/python3'
folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

with open('tools.json', 'r') as f:
    tool_list = json.load(f)
# Define the tools that the LLM can use
tools = tool_list

# Read the new prompt from file
with open('prompts/prompt.txt', 'r') as f:
    system_prompt = f.read()

# Read the new prompt from file
with open('prompts/generator/function.txt', 'r') as f:
    generator_prompt = f.read()

#Define prompt for the LLM and input messages
input_messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "50 remove from 9"}
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
        print(f"Result from functions.py: {output}")
    else:
        function_requirement = response.choices[0].message.content
        print(function_requirement)
        # Define the generator prompt for the LLM
        generator_messages = [
            {"role": "system", "content": generator_prompt},
            {"role": "user", "content": function_requirement}
        ]
        generator_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=generator_messages
        )
        function = generator_response.choices[0].message.content
        new_function = f"\n\n{function}\n"
        print("Generated function code:", new_function)
        with open('functions.py', 'a') as f:
            f.write(new_function)
        print("Function code appended to functions.py")

