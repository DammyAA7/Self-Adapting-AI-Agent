import os
from openai import OpenAI
import json
from Function_Gen.generator import generate_function_code
from Utilities.write_to_file import write_to_file
from Adjudicator.adjudicator import adjudicate
from Tool_Gen.toolGenerator import generate_tool_definitions
from Prompt_Gen.promptGenerator import generateFunctionDescriptor
from Utilities.performanceTester import performance_subprocess_call, performance_execute

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
        {"role": "user", "content": "what is 5 multiplied by 3.5?"}
    ]
    return tools, input_messages
    
def extract_numbers_from_args(function_args):
    """
    Extracts all numbers from function arguments, regardless of structure.
    
    Args:
        function_args (dict): The function arguments dictionary
        
    Returns:
        list: A flat list of all numbers found in the arguments
    """
    numbers = ""
    
    def extract_from_value(value):
        nonlocal numbers
        if isinstance(value, (int, float)):
            numbers += str(value) + ","
        elif isinstance(value, list):
            for item in value:
                extract_from_value(item)
        elif isinstance(value, dict):
            for v in value.values():
                extract_from_value(v)
    
    for arg_value in function_args.values():
        extract_from_value(arg_value)
    
    # Remove trailing comma if it exists
    if numbers and numbers.endswith(","):
        numbers = numbers[:-1]
    
    return numbers

def is_safe_function(function_name):
    """Check if function is safe to run via module import"""
    try:
        with open('safeFunctions.json', 'r') as f:
            safe_list = json.load(f)
        return function_name in safe_list['safe']
    except:
        # If file doesn't exist or error, default to unsafe
        return False

def add_safe_function(name):
    """Add function to safe list"""
    try:
        with open('safeFunctions.json', 'r') as f:
            data = json.load(f)
    except:
        data = {"safe": []}
    
    if name not in data['safe']:
        data['safe'].append(name)
        with open('safeFunctions.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Added '{name}' to safe functions")
    else:
        print(f"'{name}' is already safe")


def execute_function(function_name, args):
    """Execute function using safe method (import) or unsafe method (subprocess)"""
    is_safe = is_safe_function(function_name)
    
    if is_safe:
        print(f"Executing {function_name} via MODULE IMPORT (safe)")
        # Convert args string to actual arguments
        arg_list = [float(x.strip()) for x in args.split(',') if x.strip()]
        results = performance_execute(function_name, *arg_list)
        return results, "safe"
    else:
        print(f"Executing {function_name} via SUBPROCESS (unsafe)")
        results = performance_subprocess_call(function_name, args, python_dir, folder_dir)
        
        # If subprocess execution was successful, promote to safe
        if results.get('result') is not None and 'Error:' not in str(results.get('result', '')):
            print(f"Function {function_name} executed successfully via subprocess - promoting to safe")
            add_safe_function(function_name)
            return results, "promoted_to_safe"
        else:
            return results, "unsafe"


if __name__ == "__main__":
    restart = True
    while(restart):
        tools, input_messages = setup_variables()
        # Assign OpenAI API key 
        api_key = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
        model="gpt-4o",
        messages=input_messages,
        tools=tools,
        tool_choice="auto"
        )
        #check if model wants to use tools
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            args = extract_numbers_from_args(function_args)
            print(f"Model called tool: {function_name} with arguments: {function_args}")
            
            results, safetyType = execute_function(function_name, args)
            output = results['result']
            print(f"Output from {function_name}: {output}")
            print(f"Time: {results['execution_time']:.6f} seconds")
            print(f"Memory peak: {results['memory_peak']} bytes")
            
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
        elif response.choices[0].message.content:
            # If the model did not call any tools, generate a function code
            function_requirement = response.choices[0].message.content
            
            # Generate the function code using the generator module
            print("Generating function code...")
            function_code = generate_function_code(client, function_requirement)

            #Generate tool definitions
            tools_code = generate_tool_definitions(client, function_code)
            
            #Generate the function descriptor
            prompt_function_descriptor = generateFunctionDescriptor(client, function_code, tools_code)

            adjudication_result = adjudicate(client, input_messages[1]['content'], function_requirement, function_code, tools_code, prompt_function_descriptor)

            print("Adjudication Result:", adjudication_result)

            #Code for adjudicator here
            if adjudication_result.lower() == "true":
                write_to_file('python', 'functions.py', function_code)
                write_to_file('json', 'tools.json', tools_code)
                write_to_file('txt', 'prompts/prompt.txt', prompt_function_descriptor)
            
            print("Restarting the process...")
