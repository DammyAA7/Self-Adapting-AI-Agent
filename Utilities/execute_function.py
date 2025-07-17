from Utilities.performanceTester import performance_subprocess_call, performance_execute
import json

def is_safe_function(function_name):
    """Check if function is safe to run via module import"""
    try:
        with open('Utilities/safeFunctions.json', 'r') as f:
            safe_list = json.load(f)
        return function_name in safe_list['safe']
    except:
        # If file doesn't exist or error, default to unsafe
        return False
    
def add_safe_function(name):
    """Add function to safe list"""
    safe_factions_path = 'Utilities/safeFunctions.json'
    try:
        with open(safe_factions_path, 'r') as f:
            data = json.load(f)
    except:
        data = {"safe": []}
    
    if name not in data['safe']:
        data['safe'].append(name)
        with open(safe_factions_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Added '{name}' to safe functions")
    else:
        print(f"'{name}' is already safe")


def execute_function(function_name, args, function_definitions):

    python_dir = '/usr/local/bin/python3'
    folder_dir = "/Users/oluwadamilola/Developer/Self Adapting AI Agent/" 
    """Execute function using safe method (import) or unsafe method (subprocess)"""
    is_safe = is_safe_function(function_name)
    
    if is_safe:
        print(f"Executing {function_name} via MODULE IMPORT (safe)")
        func_def = None
        for func in function_definitions:
            if func["function"]["name"] == function_name:
                func_def = func["function"]
                break
        
        if not func_def:
            raise ValueError(f"Function definition not found for {function_name}")
        
        # Convert args based on parameter types
        arg_list = []
        properties = func_def["parameters"]["properties"]
        
        # For functions with a single parameter
        if len(properties) == 1:
            param_name = list(properties.keys())[0]
            param_type = properties[param_name]["type"]
            
            if param_type == "string":
                # String parameter - use args as-is (no comma splitting)
                arg_list = [args]
            elif param_type == "number":
                # Single number parameter
                arg_list = [float(args.strip())]
            elif param_type == "array":
                # Array parameter - split by comma and convert based on items type
                items_type = properties[param_name]["items"]["type"]
                if items_type == "number":
                    arg_list = [float(x.strip()) for x in args.split(',') if x.strip()]
                elif items_type == "string":
                    arg_list = [x.strip() for x in args.split(',') if x.strip()]
        
        # For functions with multiple parameters
        else:
            # For now, assume comma-separated values
            if ',' in args:
                # Multiple arguments - split and convert
                raw_args = [x.strip() for x in args.split(',') if x.strip()]
                
                # Check each parameter type in order
                param_names = list(properties.keys())
                for i, param_name in enumerate(param_names):
                    param_type = properties[param_name]["type"]
                    
                    if param_type == "number" and i < len(raw_args):
                        arg_list.append(float(raw_args[i]))
                    elif param_type == "array" and i < len(raw_args):
                        # Remaining args go to the array parameter
                        remaining_args = raw_args[i:]
                        items_type = properties[param_name]["items"]["type"]
                        if items_type == "number":
                            arg_list.append([float(x) for x in remaining_args])
                        elif items_type == "string":
                            arg_list.append(remaining_args)
                        break
            else:
                # Single argument
                first_param = list(properties.keys())[0]
                param_type = properties[first_param]["type"]
                
                if param_type == "string":
                    arg_list = [args]
                elif param_type == "number":
                    arg_list = [float(args.strip())]
        
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

