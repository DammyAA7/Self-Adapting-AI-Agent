import os
import sys
# Add parent directory to path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import AzureOpenAI
import json
from Function_Gen.generator import generate_function_code
from Utilities.write_to_file import write_to_file, clear_file
from Adjudicator.adjudicator import adjudicate
from Tool_Descriptor_Gen.toolGenerator import generate_tool_definitions
from Prompt_Gen.promptGenerator import generateFunctionDescriptor
from Unit_Test.unitTestHandler import generate_execute_unit_tests
from Utilities.execute_function import execute_function
from dotenv import load_dotenv
from Utilities.Logger import FunctionGenerationLogger

python_path = sys.executable
folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"

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
        {"role": "user", "content": "Create me a new function that can calculate GCD/Greatest Common Divisor expressions. And answer me what is the GCD of 24 and 36 (Print me answer)"}  # Example user input
    ]
    return tools, input_messages

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    
    # Initialize logger
    logger = FunctionGenerationLogger()
    
    restart = True
    MAX_ITERATIONS = 5  # Maximum number of iterations before terminating
    
    # Azure OpenAI Configuration
    # Get credentials from environment variables
    azure_api_key = os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_API_KEY")
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_API_BASE") or "https://jenly-staging.cognitiveservices.azure.com"
    azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or os.environ.get("AZURE_API_VERSION") or "2024-12-01-preview"
    
    if not azure_api_key:
        raise ValueError("AZURE_OPENAI_API_KEY or AZURE_API_KEY environment variable is required. Please set it before running.")
    
    # You need to specify your deployment name - replace with your actual deployment
    # Common deployment names are: gpt-35-turbo, gpt-4, etc.
    azure_deployment_name = "gpt-4.1"  # CHANGE THIS to your actual deployment name
    
    # Create Azure OpenAI client
    openai_client = AzureOpenAI(
        api_key=azure_api_key,
        azure_endpoint=azure_endpoint,
        api_version=azure_api_version
    )
    
    # Use Azure OpenAI for both clients
    anthropic_client = openai_client  # Using Azure OpenAI for all operations
    
    function_code = None
    tools_code = None
    prompt_function_descriptor = None
    reinforced_requirement = ""
    unit_test_reinforced_requirement = ""
    iteration_count = 0

    try:
        while(restart):
            tools, input_messages = setup_variables()
            user_input = input_messages[-1]["content"]  # Get the user input
            
            response = openai_client.chat.completions.create(
                model=azure_deployment_name,  # Use Azure deployment name
                messages= input_messages + ([{"role": "user", "content": f"Reinforced requirment: {reinforced_requirement}"}] if reinforced_requirement else []),
                tools=tools,
                tool_choice="auto"
            )
            
            # Check if model wants to use tools
            if response.choices[0].message.tool_calls:
                tool_call = response.choices[0].message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                print(f"Model called tool: {function_name} with arguments: {function_args}")
                
                results, safetyType = execute_function(function_name, function_args, tools)
                output = results['result']
                
                # Log existing function call
                logger.log_existing_function_call(function_name, function_args, results)
                
                messages_with_result = input_messages + [
                    response.choices[0].message,
                    {"role": "tool", "content": str(output), "tool_call_id": tool_call.id}
                ]
                
                final_response = openai_client.chat.completions.create(
                    model=azure_deployment_name,
                    messages=messages_with_result,
                    tools=tools
                )
                print("Final response:", final_response.choices[0].message.content)
                restart = False
                
            elif response.choices[0].message.content:
                # If the model did not call any tools, generate a function code
                function_requirement = response.choices[0].message.content
                logger.log_model_response_without_tools(function_requirement)
                adjudicator = False

                while not adjudicator:
                    # Start logging for this function generation
                    if iteration_count == 0:  # First iteration
                        logger.start_function_generation(function_requirement, user_input)
                    
                    
                    iteration_count += 1
                    print(f"=== ITERATION {iteration_count} ===")
                    # Check if maximum iterations reached
                    if iteration_count > MAX_ITERATIONS:
                        clear_file('Unit_Test/unitTest.py')
                        print(f"Maximum iterations ({MAX_ITERATIONS}) reached. Terminating function generation.")
                        logger.log_max_iterations_reached(MAX_ITERATIONS)
                        restart = False
                        break
                
                    # If function code is not available or reinforced requirement is provided 
                    if not function_code or reinforced_requirement:
                        # Generate the function code using the generator module
                        print("Generating function code...")
                        function_code = generate_function_code(openai_client, function_requirement, reinforced_requirement)
                        #Generate tool definitions
                        tools_code = generate_tool_definitions(openai_client, function_code)

                        #Generate the function descriptor
                        prompt_function_descriptor = generateFunctionDescriptor(openai_client, function_code, tools_code)
                    
                    # Always clear and rewrite the functions.py file to avoid duplicates
                    clear_file('Unit_Test/functions.py')
                    write_to_file('python_function', 'Unit_Test/functions.py', function_code)

                    unit_test_result = generate_execute_unit_tests(openai_client, function_requirement, unit_test_reinforced_requirement)
                    # Don't clear functions.py here - we need it for the unit tests and adjudication!

                    adjudication_result = adjudicate(openai_client, unit_test_result)


                    print("Adjudication Result:", adjudication_result.judgement)

                    # Log this iteration
                    logger.log_iteration(iteration_count, unit_test_result, adjudication_result)
                    #Code for adjudicator here
                    if adjudication_result.judgement:
                        adjudicator = True
                        #clear files after successful adjudication
                        clear_file('Unit_Test/unitTest.py')
                        write_to_file('python', 'functions.py', function_code)
                        write_to_file('json', 'Tool_Descriptor_Gen/tools.json', tools_code)
                        write_to_file('txt', 'Core/prompt.txt', prompt_function_descriptor)
                        
                        # Extract function name from tools_code for logging
                        try:
                            tools_data = json.loads(tools_code) if isinstance(tools_code, str) else tools_code
                            function_name = tools_data[0]['function']['name'] if tools_data else "unknown_function"
                        except (json.JSONDecodeError, KeyError, IndexError):
                            function_name = "unknown_function"
                        
                        # Log successful function generation
                        logger.log_function_success(function_name)
                    else:
                        old_code_req = reinforced_requirement
                        old_unit_req = unit_test_reinforced_requirement
                        
                        reinforced_requirement = adjudication_result.code_requirement_suggestion
                        unit_test_reinforced_requirement = adjudication_result.unit_requirement_suggestion
                        
                        logger.log_reinforcement('code', old_code_req, reinforced_requirement, iteration_count)
                        logger.log_reinforcement('unit_test', old_unit_req, unit_test_reinforced_requirement, iteration_count)
    
                        print(f"Restarting the process... (Iteration {iteration_count})")
    except KeyboardInterrupt:
        logger.log_user_interruption()  # ADD THIS
        logger.logger.info("Process interrupted by user")
    except Exception as e:
        logger.log_unexpected_error(str(e))  # ADD THIS
        logger.logger.error(f"Unexpected error: {str(e)}")
    finally:
        # Only clear files if we want to clean up after completion
        # Comment these out for debugging to see generated files
        # clear_file('Unit_Test/unitTest.py')
        # clear_file('Unit_Test/functions.py')
        # Save session statistics and show summary
        logger.save_session_stats()
        logger.get_generation_summary()
        print("Logging complete. Check function_generation.log and function_generation_stats.json for details.")