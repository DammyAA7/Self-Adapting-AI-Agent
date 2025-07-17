import os
from openai import OpenAI
import json
from Function_Gen.generator import generate_function_code
from Utilities.write_to_file import write_to_file
from Adjudicator.adjudicator import adjudicate
from Tool_Descriptor_Gen.toolGenerator import generate_tool_definitions
from Prompt_Gen.promptGenerator import generateFunctionDescriptor
from Unit_Test.generator import generateTestCases
from Unit_Test.unitTestHandler import generate_execute_unit_tests
from Utilities.execute_function import execute_function
from dotenv import load_dotenv
import anthropic


python_dir = '/usr/local/bin/python3'
folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 

def setup_variables():
    with open('Tool_Descriptor_Gen/tools.json', 'r') as f:
        tool_list = json.load(f)
    # Define the tools that the LLM can use
    tools = tool_list

    # Read the new prompt from file
    with open('Core/prompt.txt', 'r') as f:
        system_prompt = f.read()

    #Define prompt for the LLM and input messages
    input_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "get new tires"}
    ]
    return tools, input_messages

def extract_from_args(function_args):
    """
    Extracts all numbers from function arguments, regardless of structure.
    
    Args:
        function_args (dict): The function arguments dictionary
        
    Returns:
        list: A flat list of all numbers found in the arguments
    """
    val = ""
    
    def extract_from_value(value):
        nonlocal val
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
    if val and val.endswith(","):
        val = val[:-1]
    
    return val

if __name__ == "__main__":
    load_dotenv()
    restart = True
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

    openai_client = OpenAI(api_key=openai_api_key)
    
    anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)


    while(restart):
        tools, input_messages = setup_variables()
        # Assign OpenAI API key 
        
        response = openai_client.chat.completions.create(
        model="o3-2025-04-16",
        messages=input_messages,
        tools=tools,
        tool_choice="auto"
        )
        #check if model wants to use tools
        reinforced_requirement  = ""
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            print(f"Model called tool: {function_name} with arguments: {function_args}")
            args = extract_from_args(function_args)
            print(f"Extracted args: {args}")
            
            results, safetyType = execute_function(function_name, function_args['todo_text'], tools)
            output = results['result']
            print(f"Output from {function_name}: {output}")
            print(f"Time: {results['execution_time']:.6f} seconds")
            print(f"Memory peak: {results['memory_peak']} bytes")
            
            messages_with_result = input_messages + [
                response.choices[0].message,
                {"role": "tool", "content": str(output), "tool_call_id": tool_call.id}
            ]
            
            final_response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages_with_result,
                tools=tools
            )
            print("Final response:", final_response.choices[0].message.content)
            restart = False
        """
        elif response.choices[0].message.content:
            # If the model did not call any tools, generate a function code
            function_requirement = response.choices[0].message.content
            print("FUNCTION REQUIREMENT:", function_requirement)    
            
            # Generate the function code using the generator module
            print("Generating function code...")
            function_code = generate_function_code(openai_client, reinforced_requirement + function_requirement)
            print("Function code", function_code)

            #Generate tool definitions
            tools_code = generate_tool_definitions(openai_client, function_code)
            
            #Generate the function descriptor
            prompt_function_descriptor = generateFunctionDescriptor(openai_client, function_code, tools_code)

            print("Running Unit Tests...")
            # Generate unit tests using the generator module
            write_to_file('python_function', 'Unit_Test/functions.py', function_code)

            unit_test_result = generate_execute_unit_tests(anthropic_client, function_requirement, python_dir, folder_dir)
            
            print("Results of Unit Tests:", unit_test_result)

            adjudication_result = adjudicate(openai_client, unit_test_result)

            print("Adjudication Result:", adjudication_result.judgement)
            print("Requirement Suggestion:", adjudication_result.requirement_suggestion)

            #Code for adjudicator here
            if adjudication_result.judgement:
                write_to_file('python', 'functions.py', function_code)
                write_to_file('json', 'Tool_Descriptor_Gen/tools.json', tools_code)
                write_to_file('txt', 'Core/prompt.txt', prompt_function_descriptor)
            else:
                reinforced_requirement = adjudication_result.requirement_suggestion
            print("Restarting the process...")
            """
