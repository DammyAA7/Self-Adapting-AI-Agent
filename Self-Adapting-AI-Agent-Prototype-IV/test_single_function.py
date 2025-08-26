"""
Test a single function generation for debugging
Useful for testing specific inputs and monitoring the TDD flow
"""
import os
import sys
import time
import json
import subprocess
import re
from pathlib import Path
from datetime import datetime

def test_single_request(user_input, verbose=True):
    """
    Test a single user request and monitor the generation process
    
    Args:
        user_input: The user request to test
        verbose: If True, print detailed output
    
    Returns:
        Dictionary with test results
    """
    print("="*60)
    print(f"SINGLE FUNCTION TEST")
    print(f"Input: {user_input}")
    print("="*60)
    
    # First check environment
    from test_setup import setup_test_environment
    if not setup_test_environment():
        print("❌ Environment setup failed")
        return None
    
    # Clear previous logs
    log_files = ['function_generation.log', 'function_generation_stats.json']
    for log_file in log_files:
        if Path(log_file).exists():
            os.remove(log_file)
            print(f"Cleared: {log_file}")
    
    # Temporarily modify main.py
    main_path = Path("Core/main.py")
    
    # Read the current main.py
    with open(main_path, 'r') as f:
        original_content = f.read()
    
    # Find and replace the user input line
    pattern = r'        \{"role": "user", "content": ".*"\}  # .*,'
    new_line = f'        {{"role": "user", "content": "{user_input}"}}  # Test input,'
    
    modified_content = re.sub(pattern, new_line, original_content)
    
    # Write modified content
    with open(main_path, 'w') as f:
        f.write(modified_content)
    
    print(f"\n✓ Modified main.py with test input")
    
    # Run the system
    print("\nStarting system...")
    print("-" * 40)
    
    start_time = time.time()
    result = {
        'input': user_input,
        'start_time': datetime.now().isoformat(),
        'iterations': 0,
        'success': False,
        'duration': 0,
        'tdd_adjudications': [],
        'final_adjudications': [],
        'error': None
    }
    
    try:
        # Change to the correct directory before running
        original_dir = os.getcwd()
        os.chdir(Path(__file__).parent)
        
        # Run with real-time output capture
        process = subprocess.Popen(
            [sys.executable, 'Core/main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=Path(__file__).parent
        )
        
        # Monitor output in real-time if verbose
        if verbose:
            print("\n### SYSTEM OUTPUT ###")
            stdout_lines = []
            stderr_lines = []
            
            # Read output line by line
            while True:
                output = process.stdout.readline()
                if output:
                    print(f"  {output.strip()}")
                    stdout_lines.append(output)
                
                # Check if process has finished
                if process.poll() is not None:
                    break
            
            # Get any remaining output
            remaining_stdout, stderr = process.communicate()
            if remaining_stdout:
                stdout_lines.append(remaining_stdout)
            if stderr:
                stderr_lines.append(stderr)
                if verbose and stderr.strip():
                    print(f"\nSTDERR: {stderr}")
            
            stdout = ''.join(stdout_lines)
            stderr = ''.join(stderr_lines)
        else:
            # Just wait for completion
            stdout, stderr = process.communicate(timeout=300)
        
        result['duration'] = time.time() - start_time
        
        print("\n" + "-" * 40)
        print(f"✓ System execution complete ({result['duration']:.2f} seconds)")
        
    except subprocess.TimeoutExpired:
        process.kill()
        result['error'] = "Timeout after 5 minutes"
        print("✗ System timeout")
    except Exception as e:
        result['error'] = str(e)
        print(f"✗ Error: {e}")
    finally:
        # Restore original main.py
        with open(main_path, 'w') as f:
            f.write(original_content)
        print("✓ Restored main.py")
    
    # Parse logs for detailed metrics
    print("\n### LOG ANALYSIS ###")
    
    log_path = Path("../success_run/function_generation.log")
    if log_path.exists():
        with open(log_path, 'r') as f:
            log_content = f.read()
        
        # Count iterations
        iterations = re.findall(r'=== ITERATION (\d+) ===', log_content)
        result['iterations'] = len(iterations)
        print(f"Iterations: {result['iterations']}")
        
        # Check for success
        if "Function successfully generated" in log_content:
            result['success'] = True
            # Extract function name
            func_match = re.search(r'Function ([\w_]+) successfully generated', log_content)
            if func_match:
                result['function_name'] = func_match.group(1)
                print(f"✓ Function generated: {result['function_name']}")
        else:
            print("✗ Function generation failed")
        
        # Extract TDD adjudication results
        tdd_matches = re.findall(r'TDD Adjudication Passed: (True|False)', log_content)
        result['tdd_adjudications'] = [m == 'True' for m in tdd_matches]
        if result['tdd_adjudications']:
            print(f"TDD Adjudications: {result['tdd_adjudications']}")
            print(f"  - Passed: {sum(result['tdd_adjudications'])}")
            print(f"  - Failed: {len(result['tdd_adjudications']) - sum(result['tdd_adjudications'])}")
        
        # Extract final adjudication results
        final_matches = re.findall(r'Adjudication Passed: (True|False)', log_content)
        result['final_adjudications'] = [m == 'True' for m in final_matches]
        if result['final_adjudications']:
            print(f"Final Adjudications: {result['final_adjudications']}")
            print(f"  - Passed: {sum(result['final_adjudications'])}")
            print(f"  - Failed: {len(result['final_adjudications']) - sum(result['final_adjudications'])}")
        
        # Check if maximum iterations was reached
        if "Maximum iterations" in log_content:
            result['max_iterations_reached'] = True
            print("⚠️  Maximum iterations reached")
    else:
        print("⚠️  No log file generated")
    
    # Check generated files
    print("\n### GENERATED FILES ###")
    
    # Check if function was added to functions.py
    functions_path = Path("functions.py")
    if functions_path.exists():
        with open(functions_path, 'r') as f:
            functions_content = f.read()
        
        # Count function definitions
        func_defs = re.findall(r'^def (\w+)\(', functions_content, re.MULTILINE)
        print(f"Functions in functions.py: {len(func_defs)}")
        if func_defs:
            print(f"  Functions: {', '.join(func_defs[-5:])}")  # Show last 5
    
    # Check tools.json
    tools_path = Path("Tool_Descriptor_Gen/tools.json")
    if tools_path.exists():
        with open(tools_path, 'r') as f:
            tools = json.load(f)
        print(f"Tools registered: {len(tools)}")
        if tools:
            tool_names = [t.get('function', {}).get('name', 'unknown') for t in tools]
            print(f"  Tools: {', '.join(tool_names[-5:])}")  # Show last 5
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Input: {user_input}")
    print(f"Success: {'✓ Yes' if result['success'] else '✗ No'}")
    print(f"Iterations: {result['iterations']}")
    print(f"Duration: {result['duration']:.2f} seconds")
    
    if result['success'] and result['iterations'] > 0:
        print(f"Efficiency: {result['duration'] / result['iterations']:.2f} seconds/iteration")
    
    # Save result
    result_file = f"single_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\n✓ Results saved to: {result_file}")
    
    return result

def test_batch(test_cases, delay=5):
    """
    Test multiple cases in sequence
    
    Args:
        test_cases: List of user inputs to test
        delay: Seconds to wait between tests
    """
    results = []
    
    print("="*60)
    print(f"BATCH TEST: {len(test_cases)} cases")
    print("="*60)
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n\n{'#'*60}")
        print(f"# TEST CASE {i}/{len(test_cases)}")
        print(f"{'#'*60}")
        
        result = test_single_request(user_input, verbose=False)
        results.append(result)
        
        if i < len(test_cases):
            print(f"\nWaiting {delay} seconds before next test...")
            time.sleep(delay)
    
    # Print summary
    print("\n\n" + "="*60)
    print("BATCH TEST SUMMARY")
    print("="*60)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total tests: {total}")
    print(f"Successful: {successful} ({successful/total*100:.1f}%)")
    print(f"Failed: {total - successful}")
    
    if results:
        avg_iterations = sum(r['iterations'] for r in results) / len(results)
        avg_duration = sum(r['duration'] for r in results) / len(results)
        print(f"Average iterations: {avg_iterations:.2f}")
        print(f"Average duration: {avg_duration:.2f} seconds")
    
    # Save batch results
    batch_file = f"batch_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(batch_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ Batch results saved to: {batch_file}")
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test single function generation')
    parser.add_argument('input', nargs='?', default="multiply 5 by 3",
                       help='User input to test (default: "multiply 5 by 3")')
    parser.add_argument('--batch', action='store_true',
                       help='Run batch test with predefined cases')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress verbose output')
    
    args = parser.parse_args()
    
    if args.batch:
        # Predefined test cases for batch testing
        test_cases = [
            "add 10 and 20",
            "calculate factorial of 5",
            "find the maximum of 3, 7, 2, 9, 1",
            "convert celsius 25 to fahrenheit",
            "calculate area of circle with radius 5",
            "update todo 3 to completed",
            "list all pending todos",
            "find prime numbers up to 20"
        ]
        
        print("Running batch test with predefined cases...")
        test_batch(test_cases)
    else:
        # Single test
        print(f"Testing single input: {args.input}")
        test_single_request(args.input, verbose=not args.quiet)