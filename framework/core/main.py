import os
import sys
# Add parent directory to path so imports work correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openai import OpenAI, AzureOpenAI
# import anthropic  # Not needed - using OpenAI only
import json
from function_gen.generator import generate_function_code
from test_driven_development.generator import generateTestDrivenCases
from utilities.write_to_file import write_to_file, clear_file, replace_function_in_file
from adjudicator.adjudicator import adjudicate
from intermediate_adjudicator.adjudicator import intermidiate_adjudicate
from tool_descriptor_gen.toolGenerator import generate_tool_definitions
from prompt_gen.promptGenerator import generateFunctionDescriptor
from unit_test.unitTestHandler import generate_execute_unit_tests
from utilities.execute_function import execute_function
from dotenv import load_dotenv
from utilities.Logger import FunctionGenerationLogger
from file_analyzer.analyzer import SimpleAnalyzer
from utilities.cleanup import reset_for_new_run, full_cleanup, reset_for_context_mode
import argparse

# Import terminal context if available
try:
    from terminal_context.context_manager import get_context_manager
    TERMINAL_CONTEXT_AVAILABLE = True
except ImportError:
    TERMINAL_CONTEXT_AVAILABLE = False
    print("Terminal Context not available - functions won't persist between generations")


python_dir = sys.executable
folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/" 

def get_user_input():
    """Get user request dynamically from various sources"""
    parser = argparse.ArgumentParser(description='Self-Evolving Framework with Project Analysis')
    parser.add_argument('--request', type=str, help='Direct request string')
    parser.add_argument('--file', type=str, help='Path to file containing request')
    parser.add_argument('--analyze', type=str, help='Path to project to analyze')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--clean', action='store_true', help='Clean test files before running')
    parser.add_argument('--clean-all', action='store_true', help='Clean all files including generated functions')
    parser.add_argument('--no-clean', action='store_true', help='Skip automatic cleanup of test files before running')
    parser.add_argument('--context-memory', action='store_true', help='Enable context memory mode - restore previous sessions and preserve function context')
    parser.add_argument('--session', type=str, help='Direct path to specific session file to load (requires --context-memory)')
    parser.add_argument('--auto-load', action='store_true', help='Automatically load the most recent context session without prompting (requires --context-memory)')
    parser.add_argument('--debug', action='store_true', help='Enable debug output for troubleshooting')

    args = parser.parse_args()

    # Validate auto-load requires context-memory
    if args.auto_load and not args.context_memory:
        print("❌ Error: --auto-load requires --context-memory to be enabled")
        parser.print_help()
        sys.exit(1)

    # Handle cleanup options first
    if args.clean_all:
        full_cleanup(verbose=True)
        if not args.request and not args.file and not args.interactive:
            print("Cleanup complete. Specify a request to generate a function.")
            return None, None, args
    elif args.clean:
        reset_for_new_run(clear_generated=False, verbose=True)
        if not args.request and not args.file and not args.interactive:
            print("Cleanup complete. Specify a request to generate a function.")
            return None, None, args

    # Interactive mode (default if no arguments)
    if args.interactive or (not args.request and not args.file):
        print("\n" + "="*60)
        print("Self-Evolving Framework - Interactive Mode")
        print("="*60)
        analyze_path = input("Project path to analyze (press Enter to skip): ").strip()
        request = input("What would you like me to help with? > ").strip()
        return request, analyze_path if analyze_path else None, args

    # File mode
    elif args.file:
        with open(args.file, 'r') as f:
            request = f.read().strip()
        return request, args.analyze, args

    # Direct request mode
    elif args.request:
        return args.request, args.analyze, args

    return None, None, args

def select_context_session(context_manager, auto_session=None, auto_load=False):
    """
    Interactive session selection for context memory mode.

    Args:
        context_manager: ContextManager instance
        auto_session: Direct path to session file (optional)
        auto_load: If True, automatically load the most recent session without prompting

    Returns:
        (loaded_successfully, session_file_path) tuple
    """
    import json
    from datetime import datetime
    import os
    
    if auto_session:
        # Direct session file provided via --session argument
        print(f"📂 Loading specified session: {auto_session}")
        if not os.path.exists(auto_session):
            print(f"❌ Session file not found: {auto_session}")
            return False, None
        success = context_manager.load_session(auto_session)
        if success:
            print("✅ Session loaded successfully!")
        return success, auto_session
    
    # List available sessions
    session_dir = os.path.join("..", "outputs", "sessions", "context_sessions")
    if not os.path.exists(session_dir):
        print("📁 No context sessions directory found. Starting fresh.")
        return False, None
    
    sessions = []
    for filename in os.listdir(session_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(session_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    sessions.append({
                        'filename': filename,
                        'filepath': filepath,
                        'created': data['session_data'].get('created_at', 'Unknown'),
                        'functions': list(data['session_data'].get('functions', {}).keys()),
                        'saved_at': data.get('saved_at', 'Unknown')
                    })
            except Exception as e:
                print(f"⚠ Warning: Could not read session {filename}: {e}")
                continue
    
    if not sessions:
        print("📁 No valid session files found. Starting fresh.")
        return False, None
    
    # Sort by saved_at timestamp (most recent first)
    sessions.sort(key=lambda x: x['saved_at'], reverse=True)

    # Auto-load most recent session if requested
    if auto_load and sessions:
        selected_file = sessions[0]['filepath']
        print("\n" + "="*60)
        print("Auto-Loading Most Recent Context Session")
        print("="*60)
        print(f"🎯 Loading: {sessions[0]['filename']}")

        # Load the session
        success = context_manager.load_session(selected_file)

        if success:
            print("✅ Session loaded successfully!")
            functions = context_manager.list_available_functions()
            if functions:
                print(f"📋 Available functions: {', '.join(functions)}")
            else:
                print("📋 No functions found in session")
        else:
            print("❌ Failed to load session")

        return success, selected_file

    print("\n" + "="*60)
    print("Context Memory Mode - Session Selection")
    print("="*60)
    print("\n📂 Available Context Sessions:")
    
    for idx, session in enumerate(sessions[:10], 1):
        # Parse timestamp for display
        try:
            timestamp = datetime.fromisoformat(session['saved_at'].replace('Z', '+00:00'))
            date_str = timestamp.strftime("%b %d, %H:%M")
        except:
            date_str = 'Unknown date'
        
        func_count = len(session['functions'])
        func_names = ', '.join(session['functions'][:3])
        if len(session['functions']) > 3:
            func_names += f", +{len(session['functions'])-3} more"
        
        print(f"{idx}. {session['filename']} ({date_str})")
        print(f"   Functions ({func_count}): {func_names if func_names else 'None'}")
        print()
    
    # Get user selection
    print("Options:")
    print(f"  - Enter 1-{len(sessions[:10])} to select a session")
    print("  - Enter full path to custom session file")
    print("  - Enter 'new' to start fresh with context memory")
    print("  - Press Enter to use most recent session")
    
    selection = input("\nYour choice: > ").strip()
    
    # Process selection
    selected_file = None
    if not selection and sessions:
        # Use most recent
        selected_file = sessions[0]['filepath']
        print(f"🎯 Using most recent session: {sessions[0]['filename']}")
    elif selection.lower() == 'new':
        print("🆕 Starting fresh session with context memory enabled")
        return False, None
    elif selection.isdigit() and 1 <= int(selection) <= len(sessions[:10]):
        selected_file = sessions[int(selection)-1]['filepath']
        print(f"🎯 Selected: {sessions[int(selection)-1]['filename']}")
    elif os.path.exists(selection):
        selected_file = selection
        print(f"🎯 Loading custom path: {selection}")
    else:
        print(f"❌ Invalid selection: {selection}")
        print("Starting fresh session...")
        return False, None
    
    # Load selected session
    print(f"\n📂 Loading session: {selected_file}")
    success = context_manager.load_session(selected_file)
    
    if success:
        print("✅ Session loaded successfully!")
        functions = context_manager.list_available_functions()
        if functions:
            print(f"📋 Available functions: {', '.join(functions)}")
        else:
            print("📋 No functions found in session")
    else:
        print("❌ Failed to load session")
    
    return success, selected_file

def setup_variables(user_request=None, project_context=""):
    with open('tool_descriptor_gen/tools.json', 'r') as f:
        tool_list = json.load(f)
    # Define the tools that the LLM can use
    tools = tool_list

    # Read the base prompt from file
    with open('core/prompt.txt', 'r') as f:
        system_prompt = f.read()

    # Add project context to system prompt if available
    if project_context:
        system_prompt = f"""{system_prompt}

PROJECT CONTEXT:
================
{project_context}

IMPORTANT: You have full visibility of the project above. Use this knowledge to:
- Reuse existing functions when appropriate
- Follow the same coding patterns and style
- Work with the actual data structures present in the project
- Generate code that integrates well with the existing codebase
"""

    # Use dynamic user request or fallback to default
    if not user_request:
        user_request = "Create a function that can calculate factorial expressions. And answer me what is 2!+2! (Print me answer)"

    #Define prompt for the LLM and input messages
    input_messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request}
    ]
    return tools, input_messages

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    
    # Initialize logger
    logger = FunctionGenerationLogger()
    
    # Initialize terminal context if available
    context_manager = None
    if TERMINAL_CONTEXT_AVAILABLE:
        context_manager = get_context_manager()
        print("Terminal Context initialized - functions will persist across generations")
    
    # Get user input, analyze path, and command-line args
    user_request, analyze_path, cmd_args = get_user_input()
    if not user_request:
        print("No request provided. Exiting.")
        sys.exit(0)
    
    # Handle context memory mode
    context_memory_mode = False
    loaded = False  # Track whether functions were loaded from session
    if hasattr(cmd_args, 'context_memory') and cmd_args.context_memory:
        context_memory_mode = True
        if not TERMINAL_CONTEXT_AVAILABLE:
            print("❌ Context memory mode requires Terminal Context module, but it's not available.")
            sys.exit(1)
        
        print("\n" + "="*60)
        print("Context Memory Mode Activated")
        print("="*60)
        
        # Load previous session
        auto_session = cmd_args.session if hasattr(cmd_args, 'session') and cmd_args.session else None
        auto_load = hasattr(cmd_args, 'auto_load') and cmd_args.auto_load
        loaded, session_path = select_context_session(context_manager, auto_session, auto_load)
        
        if loaded:
            # Re-populate unit_test/functions.py from loaded context
            print("\n🔄 Restoring function definitions to unit_test/functions.py...")
            
            # Debug: Check if session data is accessible
            if hasattr(context_manager, 'session_data') and context_manager.session_data:
                print(f"🔍 Debug: context_manager.session_data keys: {list(context_manager.session_data.keys())}")
                if 'functions' in context_manager.session_data:
                    print(f"🔍 Debug: functions key contains: {list(context_manager.session_data['functions'].keys())}")
                else:
                    print("⚠ Warning: No 'functions' key in session_data")
            else:
                print("⚠ Warning: context_manager.session_data is empty or not accessible")
            
            # Read enum content first
            with open('unit_test/enumUtility.txt', 'r') as f:
                enum_utility = f.read()

            # Clear and start with enums in BOTH files for synchronization
            clear_file('unit_test/functions.py')
            clear_file('functions.py')
            write_to_file('python_function', 'unit_test/functions.py', enum_utility)
            # Also write to root functions.py (without enums, just comment and cache)
            write_to_file('python', 'functions.py', "# Dynamically generated functions will be added here\n\ncomputation_cache = {}\n")

            # Add each function from the loaded session to BOTH files
            restored_count = 0
            for func_name, func_data in context_manager.session_data['functions'].items():
                if 'code' in func_data:
                    # Add newline for proper separation and ensure clean code
                    clean_code = func_data['code'].strip()
                    # Write to BOTH files to maintain synchronization
                    write_to_file('python_function', 'unit_test/functions.py', "\n" + clean_code + "\n")
                    write_to_file('python', 'functions.py', "\n" + clean_code + "\n")
                    print(f"  ✓ Restored function: {func_name}")
                    restored_count += 1
                else:
                    print(f"  ⚠ Skipped function '{func_name}' (incomplete data)")

            print(f"📋 Restored {restored_count} function(s) to unit_test/functions.py")

            # Verify functions were actually restored
            try:
                with open('unit_test/functions.py', 'r') as f:
                    content = f.read()

                missing_functions = []
                for func_name in context_manager.session_data['functions'].keys():
                    if 'code' in context_manager.session_data['functions'][func_name]:
                        if f"def {func_name}" not in content:
                            missing_functions.append(func_name)

                if missing_functions:
                    print(f"⚠ Warning: Functions not found in functions.py: {missing_functions}")
                else:
                    print("✅ All session functions verified in functions.py")
                    
            except Exception as e:
                print(f"⚠ Warning: Could not verify function restoration: {e}")
            
            print("✅ Function definitions restored!")
        else:
            print("🆕 Starting fresh session with context memory enabled")
        
        print("="*60 + "\n")
    
    # Note: Cleanup is already handled in get_user_input() if flags are set
    # No need to repeat it here

    # Analyze project if path provided
    project_context = ""
    if analyze_path:
        print(f"\nAnalyzing project at: {analyze_path}")
        print("This may take a moment...\n")

        analyzer = SimpleAnalyzer(analyze_path)
        analyzer.read_all_files()
        summary = analyzer.get_project_summary()

        print(f"Analysis complete!")
        print(f"Found {summary['total_files']} files:")
        print(f"  - Python: {summary['python_files']} files ({summary['total_functions']} functions, {summary['total_classes']} classes)")
        print(f"  - CSV: {summary['csv_files']} files")
        print(f"  - JSON: {summary['json_files']} files")
        print(f"  - Text/Config: {summary['text_files']} files")
        print(f"  - Total lines: {summary['total_lines']}")
        print(f"\nProceeding with your request...\n")

        # Get formatted context for LLM
        project_context = analyzer.format_context_for_llm()

    restart = True
    MAX_ITERATIONS = 6  # Maximum number of iterations before terminating
    
    # Azure OpenAI Configuration
    # Get credentials from environment variables
    azure_api_key = os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_API_KEY")
    azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or os.environ.get("AZURE_API_BASE")
    azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or os.environ.get("AZURE_API_VERSION")
    
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
    just_generated = False  # Track if we just generated a function

    try:
        while(restart):
            # If we just generated a function, skip generation check and go to execution
            if just_generated:
                just_generated = False
                print("Function was just generated, proceeding to execution...")
            
            tools, input_messages = setup_variables(user_request, project_context)
            user_input = user_request  # Use the dynamic user input
            
            # Debug logging for Pass@k evaluation
            if cmd_args.debug:
                print(f"DEBUG: Number of tools loaded: {len(tools)}")
                if tools:
                    tool_names = [t.get('function', {}).get('name', 'unknown') for t in tools]
                    print(f"DEBUG: Available tools: {tool_names}")
                else:
                    print("DEBUG: No tools loaded - this explains the failure!")
                    
                # Also show tools.json file content
                try:
                    with open('tool_descriptor_gen/tools.json', 'r') as f:
                        content = f.read()
                    print(f"DEBUG: tools.json content: {content[:200]}...")
                except Exception as e:
                    print(f"DEBUG: Error reading tools.json: {e}")
            
            # If we analyzed a project, remind the model to use project file paths when relevant
            if analyze_path and project_context:
                # Enhance the user message to include file path reminder
                enhanced_request = f"{user_request}\n\nNote: If this operation involves files, use the actual file paths from the analyzed project context."
                # Update the last user message (which contains the user request)
                if input_messages and input_messages[-1]["role"] == "user":
                    input_messages[-1]["content"] = enhanced_request
            
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
                print(function_args)
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
                # If the model did not call any tools, check if existing functions can handle this first
                function_requirement = response.choices[0].message.content
                logger.log_model_response_without_tools(function_requirement)
                
                # Two-phase approach: Check if existing functions can handle the request
                if tools:  # Only check if we have existing tools
                    check_message = "Before generating a new function, check: Do any of your existing tools match this request? If yes, call the appropriate function with reasonable example parameters. If no exact match exists, proceed with generating a new function."
                    
                    # If we analyzed a project, add file path reminder for existing function calls too
                    if analyze_path and project_context:
                        check_message += "\n\nNote: If calling functions that work with files, use the actual file paths from the analyzed project context."
                    
                    check_messages = input_messages + [
                        {"role": "assistant", "content": function_requirement},
                        {"role": "user", "content": check_message}
                    ]
                    
                    check_response = openai_client.chat.completions.create(
                        model=azure_deployment_name,
                        messages=check_messages,
                        tools=tools,
                        tool_choice="auto"
                    )
                    
                    # If the check response wants to use an existing tool, handle it
                    if check_response.choices[0].message.tool_calls:
                        print("Found existing function that can handle this request!")
                        tool_call = check_response.choices[0].message.tool_calls[0]
                        function_name = tool_call.function.name
                        function_args = json.loads(tool_call.function.arguments)
                        print(f"Using existing function: {function_name} with arguments: {function_args}")
                        
                        results, safetyType = execute_function(function_name, function_args, tools)
                        output = results['result']
                        
                        # Log existing function call
                        logger.log_existing_function_call(function_name, function_args, results)
                        
                        messages_with_result = input_messages + [
                            check_response.choices[0].message,
                            {"role": "tool", "content": str(output), "tool_call_id": tool_call.id}
                        ]
                        
                        final_response = openai_client.chat.completions.create(
                            model=azure_deployment_name,
                            messages=messages_with_result,
                            tools=tools
                        )
                        print("Final response:", final_response.choices[0].message.content)
                        restart = False
                        continue  # Skip function generation entirely
                
                adjudicator = False
                
                # Clean test files before starting generation (unless disabled)
                if not hasattr(cmd_args, 'no_clean') or not cmd_args.no_clean:
                    if context_memory_mode and loaded:
                        print("Context mode: Skipping cleanup (functions just restored)")
                    elif context_memory_mode:
                        print("Context mode: Cleaning test files only (preserving functions)...")
                        reset_for_context_mode(verbose=False)
                    else:
                        print("Cleaning test files for fresh generation...")
                        reset_for_new_run(clear_generated=False, verbose=False)
                else:
                    print("Skipping automatic cleanup (--no-clean specified)")

                while not adjudicator:
                    # Start logging for this function generation
                    if iteration_count == 0:  # First iteration
                        logger.start_function_generation(function_requirement, user_input)
                    
                    
                    iteration_count += 1
                    print(f"=== ITERATION {iteration_count} ===")
                    # Check if maximum iterations reached
                    if iteration_count > MAX_ITERATIONS:
                        clear_file('unit_test/unitTest.py')
                        print(f"Maximum iterations ({MAX_ITERATIONS}) reached. Terminating function generation.")
                        logger.log_max_iterations_reached(MAX_ITERATIONS)
                        restart = False
                        break
                
                    # If function code is not available or reinforced requirement is provided 
                    if not function_code or reinforced_requirement:
                        # Generate the function code using the generator module
                        print("Generating function code...")
                        test_driven_code = generateTestDrivenCases(openai_client, function_requirement, reinforced_requirement, project_context)
                        function_code = generate_function_code(openai_client, test_driven_code, project_context)
                        #Generate tool definitions
                        tools_code = generate_tool_definitions(openai_client, function_code)

                        #Generate the function descriptor
                        prompt_function_descriptor = generateFunctionDescriptor(openai_client, function_code, tools_code)
                        # clear_file('Unit_Test/functions.py')

                    # Handle functions.py based on context mode
                    if not context_memory_mode:
                        # Normal mode: clear and rewrite functions.py to avoid duplicates
                        clear_file('unit_test/functions.py')
                        # Generate unit tests using the generator module
                        with open('unit_test/enumUtility.txt', 'r') as f:
                            enum_utility = f.read()
                        write_to_file('python_function', 'unit_test/functions.py', enum_utility + "\n" + function_code)
                    else:
                        # Context mode: replace/add function while preserving existing ones
                        # Extract function name for replacement
                        import re
                        # Improved regex pattern to handle complex function names
                        func_match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', function_code)
                        
                        # Debug information for function name extraction
                        if not func_match:
                            first_lines = '\n'.join(function_code.split('\n')[:3])
                            print(f"🔍 Debug: Could not extract function name from:\n{first_lines}")
                            all_defs = re.findall(r'def\s+[^(]+\(', function_code)
                            print(f"🔍 All 'def' patterns found: {all_defs}")
                        if func_match:
                            current_func_name = func_match.group(1)
                            # Replace in BOTH files to maintain synchronization
                            replaced_unit = replace_function_in_file('unit_test/functions.py', current_func_name, function_code)
                            replaced_root = replace_function_in_file('functions.py', current_func_name, function_code)

                            if replaced_unit or replaced_root:
                                print(f"Context mode: Replaced function '{current_func_name}' in both files (iteration {iteration_count})")
                            else:
                                # If not replaced, append to both files
                                write_to_file('python_function', 'unit_test/functions.py', "\n" + function_code)
                                write_to_file('python', 'functions.py', "\n" + function_code)
                                print(f"Context mode: Added new function '{current_func_name}' to both files")
                        else:
                            # Fallback if function name extraction fails
                            print("Context mode: Appending function to both files (could not extract name)")
                            write_to_file('python_function', 'unit_test/functions.py', "\n" + function_code)
                            write_to_file('python', 'functions.py', "\n" + function_code)

                    if not unit_test_reinforced_requirement or reinforced_requirement: 
                        #Check test driven code
                        tdd_adjudication_result = intermidiate_adjudicate(openai_client)
                        logger.log_tdd_adjudication(iteration_count, tdd_adjudication_result, reinforced_requirement)

                        if not tdd_adjudication_result.judgement:
                            print("Test Driven Development adjudication failed. Reinforcing requirement...")
                            old_requirement = reinforced_requirement
                            reinforced_requirement = tdd_adjudication_result.requirement_suggestion
                            logger.log_reinforcement('tdd', old_requirement, reinforced_requirement, iteration_count)
                            continue

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
                        clear_file(folder_dir + 'test_driven_development/testDrivenCases.py')
                        clear_file('unit_test/unitTest.py')
                        write_to_file('python', 'functions.py', function_code)
                        write_to_file('json', 'tool_descriptor_gen/tools.json', tools_code)
                        write_to_file('txt', 'core/prompt.txt', prompt_function_descriptor)
                        
                        # Add function to terminal context if available
                        if context_manager and function_code:
                            try:
                                # Extract function name from tools_code for context tracking
                                tools_data = json.loads(tools_code) if isinstance(tools_code, str) else tools_code
                                if isinstance(tools_data, dict):
                                    func_name = tools_data['function']['name']
                                elif isinstance(tools_data, list) and len(tools_data) > 0:
                                    func_name = tools_data[0]['function']['name']
                                else:
                                    func_name = "unknown_function"
                                
                                # Add the function to the persistent context
                                context_manager.add_generated_function(func_name, function_code, {
                                    'requirement': function_requirement,
                                    'iterations': iteration_count
                                })
                                print(f"Function '{func_name}' added to persistent context")
                            except Exception as e:
                                print(f"Warning: Could not add function to context: {e}")
                        
                        # Extract function name from tools_code for logging
                        try:
                            # Parse the JSON
                            tools_data = json.loads(tools_code) if isinstance(tools_code, str) else tools_code

                            # Handle both single object and array formats
                            if isinstance(tools_data, dict):
                                # Single object format: {"type": "function", "function": {...}}
                                function_name = tools_data['function']['name']
                            elif isinstance(tools_data, list) and len(tools_data) > 0:
                                # Array format: [{"type": "function", "function": {...}}]
                                function_name = tools_data[0]['function']['name']
                            else:
                                function_name = "unknown_function"

                        except (json.JSONDecodeError, KeyError, IndexError) as e:
                            print(f"Warning: Could not extract function name from tools_code: {e}")
                            function_name = "unknown_function"
                        
                        # Log successful function generation
                        logger.log_function_success(function_name)
                        # Set flag to indicate we just generated a function
                        just_generated = True
                        iteration_count = 0  # Reset for next function
                        # Don't set restart = False here - need to loop back to execute the function!
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
        # clear_file(folder_dir + 'Test_Driven_Development/testDrivenCases.py')
        # clear_file('Unit_Test/unitTest.py')
        # clear_file('Unit_Test/functions.py')
        
        # Save terminal context session if available
        if context_manager:
            try:
                session_file = context_manager.save_session()
                print(f"Terminal context saved: {session_file}")
                
                # Print summary of available functions
                functions = context_manager.list_available_functions()
                if functions:
                    print(f"\nFunctions available in persistent context:")
                    for func in functions:
                        print(f"  - {func}")
            except Exception as e:
                print(f"Warning: Could not save terminal context: {e}")
        
        # Save session statistics and show summary
        logger.save_session_stats()
        logger.get_generation_summary()
        print("Logging complete. Check function_generation.log and function_generation_stats.json for details.")