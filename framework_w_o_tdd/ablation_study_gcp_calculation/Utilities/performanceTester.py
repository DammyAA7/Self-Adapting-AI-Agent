import time
import psutil
import tracemalloc
from typing import Callable

def performance_function(func, *args, **kwargs):

    # Initialize result dictionary
    test_result = {
        'result': None,
        'execution_time': 0.0,
        'memory_peak': 0,
        'memory_current': 0,
        'success': False,
        'error': None,
        'function_name': getattr(func, '__name__', str(func))
    }
    
    # Get initial memory state
    process = psutil.Process()
    initial_memory = process.memory_info().rss
    
    # Start memory tracing for peak memory usage
    tracemalloc.start()
    
    try:
        # Record start time
        start_time = time.perf_counter()
        
        # Execute the function
        result = func(*args, **kwargs)
        
        # Record end time
        end_time = time.perf_counter()
        
        # Calculate execution time
        execution_time = end_time - start_time
        
        # Get peak memory usage during execution
        current_memory, peak_memory = tracemalloc.get_traced_memory()
        
        # Get final memory state
        final_memory = process.memory_info().rss
        memory_delta = final_memory - initial_memory
        
        # Update result dictionary
        test_result.update({
            'result': result,
            'execution_time': execution_time,
            'memory_peak': peak_memory,
            'memory_current': memory_delta,
            'success': True
        })
        
    except Exception as e:
        # Handle any errors during execution
        end_time = time.perf_counter()
        execution_time = end_time - start_time if 'start_time' in locals() else 0.0
        
        try:
            current_memory, peak_memory = tracemalloc.get_traced_memory()
        except:
            peak_memory = 0
            
        final_memory = process.memory_info().rss
        memory_delta = final_memory - initial_memory
        
        test_result.update({
            'result': None,
            'execution_time': execution_time,
            'memory_peak': peak_memory,
            'memory_current': memory_delta,
            'success': False,
            'error': str(e)
        })
        
    finally:
        # Stop memory tracing
        tracemalloc.stop()
    
    return test_result

def performance_subprocess_call(function_name, args, python_dir, folder_dir):
    """Profile your subprocess-based call_function"""
    import subprocess
    
    def subprocess_wrapper():
        # Create a Python script that imports and executes the function
        script = f"""
import sys
sys.path.insert(0, '{folder_dir}')
try:
    from functions import {function_name}
except ImportError:
    from Unit_Test.functions import {function_name}

# Parse the arguments
args_str = '{args}'
if args_str:
    # Convert string args to appropriate types
    args_list = []
    for arg in args_str.split(','):
        arg = arg.strip()
        # Try to convert to int if possible
        try:
            args_list.append(int(arg))
        except ValueError:
            # Keep as string if not a number
            args_list.append(arg)
    result = {function_name}(*args_list)
else:
    result = {function_name}()

print(result if result is not None else 'Success')
"""
        cmd = [python_dir, "-c", script]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd=folder_dir)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            raise RuntimeError(f"Subprocess error: {result.stderr.strip()}")
    
    return performance_function(subprocess_wrapper)

def performance_execute(function_name, *args):
    import importlib

    
    def execute_wrapper():
        # First try to import from root functions.py
        try:
            import functions as functions
            importlib.reload(functions)
            if hasattr(functions, function_name):
                func = getattr(functions, function_name)
                return func(*args)
        except (ImportError, AttributeError):
            pass
        
        # If not found in root, try Unit_Test/functions.py
        try:
            from Unit_Test import functions as unit_functions
            importlib.reload(unit_functions)
            if hasattr(unit_functions, function_name):
                func = getattr(unit_functions, function_name)
                return func(*args)
        except (ImportError, AttributeError):
            pass
        
        raise ValueError(f"Function '{function_name}' not found in either functions.py or Unit_Test/functions.py")
    
    return performance_function(execute_wrapper)