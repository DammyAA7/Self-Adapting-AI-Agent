from Utilities.performanceTester import performance_subprocess_call, performance_execute
import json
import sys

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
            val += str(value) + ","
        elif isinstance(value, list):
            for item in value:
                extract_from_value(item)
        elif isinstance(value, str):
            val += value + ","
        elif isinstance(value, dict):
            for v in value.values():
                extract_from_value(v)
    
    for arg_value in function_args.values():
        extract_from_value(arg_value)
    
    # Remove trailing comma if it exists
    if val and val.endswith(","):
        val = val[:-1]
    
    return val



def execute_function(function_name, function_args, function_definitions):

    python_dir = sys.executable
    folder_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
    """Execute function using safe method (import) or unsafe method (subprocess)"""
    is_safe = is_safe_function(function_name)
    args = extract_from_args(function_args)
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
                stripped_arg = args.strip()
                # Check if the number is an integer or float
                if '.' in stripped_arg:
                    arg_list = [float(stripped_arg)]
                else:
                    try:
                        arg_list = [int(stripped_arg)]
                    except ValueError:
                        # Fallback to float if conversion fails
                        arg_list = [float(stripped_arg)]
            elif param_type == "array":
                # Array parameter - split by comma and convert based on items type
                items_type = properties[param_name]["items"]["type"]
                if items_type == "number":
                    # Process each number in the array, handling integers and floats differently
                    processed_args = []
                    for x in args.split(','):
                        if x.strip():
                            num_str = x.strip()
                            if '.' in num_str:
                                # It's a float
                                processed_args.append(float(num_str))
                            else:
                                try:
                                    # Try to convert to integer
                                    processed_args.append(int(num_str))
                                except ValueError:
                                    # Fallback to float if conversion fails
                                    processed_args.append(float(num_str))
                    arg_list = processed_args
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
                        num_str = raw_args[i]
                        if '.' in num_str:
                            # It's a float
                            arg_list.append(float(num_str))
                        else:
                            try:
                                # Try to convert to integer
                                arg_list.append(int(num_str))
                            except ValueError:
                                # Fallback to float if conversion fails
                                arg_list.append(float(num_str))
                    elif param_type == "array" and i < len(raw_args):
                        # Remaining args go to the array parameter
                        remaining_args = raw_args[i:]
                        items_type = properties[param_name]["items"]["type"]
                        if items_type == "number":
                            processed_args = []
                            for x in remaining_args:
                                if '.' in x:
                                    processed_args.append(float(x))
                                else:
                                    try:
                                        processed_args.append(int(x))
                                    except ValueError:
                                        processed_args.append(float(x))
                            arg_list.append(processed_args)
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
                    stripped_arg = args.strip()
                    # Check if the number is an integer or float
                    if '.' in stripped_arg:
                        arg_list = [float(stripped_arg)]
                    else:
                        try:
                            arg_list = [int(stripped_arg)]
                        except ValueError:
                            # Fallback to float if conversion fails
                            arg_list = [float(stripped_arg)]
        
        results = performance_execute(function_name, *arg_list)
        return results, "safe"
    else:
        print(f"Executing {function_name} via SUBPROCESS (unsafe)")
        results = performance_subprocess_call(function_name, args, python_dir, folder_dir)
        
        # If subprocess execution was successful, promote to safe
        if results.get('result') is not None and 'Error:' not in str(results.get('result', '')):
            add_safe_function(function_name)
            return results, "promoted_to_safe"
        else:
            return results, "unsafe"

