import subprocess
import os
from openai import OpenAI
import json
from generator import generate_function_code
from write_to_file import write_to_file
from toolGenerator import generate_tool_definitions
from promptGenerator import generateFunctionDescriptor

os.environ["OPENAI_API_KEY"] = "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"

# Define directory paths
python_dir = '/usr/local/bin/python3'
folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

def setup_variables():
    with open('tools.json', 'r') as f:
        tool_list = json.load(f)
    # Define the tools that the LLM can use
    tools = tool_list

    # Read the new prompt from file
    with open('prompts/prompt.txt', 'r') as f:
        system_prompt = f.read()

    #Define prompt for the LLM and input messages
    input_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "multiply 5 by 5"}
    ]

    return tools, input_messages

# Function to call functions.py using subprocess
def call_function(func_name, arg1, arg2):
    cmd = [python_dir, folder_dir + "functions.py", func_name, f"{arg1},{arg2}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return f"Error: {result.stderr.strip()}"

if __name__ == "__main__":
    restart = True
    while(restart):
        tools, input_messages = setup_variables()
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
            print(f"Model called tool: {function_name} with arguments: {function_args}")
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
            restart = False
        else:
            # If the model did not call any tools, generate a function code
            function_requirement = response.choices[0].message.content
            
            # Generate the function code using the generator module
            print("Generating function code...")
            function_code = generate_function_code(client, function_requirement)
            print("Function code generated successfully.")
            
            # Append the generated function code to functions.py
            print('Writing function code to functions.py...')
            write_to_file('python', 'functions.py', function_code)
            print("Function code appended successfully.")

            #Generate tool definitions
            print("Generating tool definitions...")
            tools_code = generate_tool_definitions(client, function_code)
            print("Tool definitions generated successfully.")
            # Write tool definition
            print("Writing to tools.json")
            write_to_file('json', 'tools.json', tools_code)
            print("Successfully written to file")

            # Generate the function descriptor
            print("Generating function descriptor...")
            prompt_function_descriptor = generateFunctionDescriptor(client, function_code, tools_code)
            write_to_file('txt', 'prompts/prompt.txt', prompt_function_descriptor)
            print("Function descriptor generated and written to prompts/prompt.txt")
            
            print("Restarting the process...")
