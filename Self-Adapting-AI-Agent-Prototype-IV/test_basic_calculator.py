"""
Test basic calculator functionality matching thesis evaluation
"""
import subprocess
import json
import time
import os
import sys
from pathlib import Path
from datetime import datetime

class CalculatorTester:
    def __init__(self):
        self.results = []
        self.log_file = "calculator_test_results.json"
        
    def modify_main_for_test(self, user_input):
        """Temporarily modify main.py to use test input"""
        main_path = Path("Core/main.py")
        
        # Read the current main.py
        with open(main_path, 'r') as f:
            content = f.read()
        
        # Find and replace the user input line
        old_line = '        {"role": "user", "content": "delete todo 5"}  # Example user input,'
        new_line = f'        {{"role": "user", "content": "{user_input}"}}  # Test input,'
        
        modified_content = content.replace(old_line, new_line)
        
        # Write back the modified content
        with open(main_path, 'w') as f:
            f.write(modified_content)
        
        return old_line
        
    def restore_main(self, original_line):
        """Restore main.py to original state"""
        main_path = Path("Core/main.py")
        
        with open(main_path, 'r') as f:
            content = f.read()
        
        # Find the test input line pattern
        import re
        pattern = r'        \{"role": "user", "content": ".*"\}  # Test input,'
        
        # Replace with original
        modified_content = re.sub(pattern, original_line, content)
        
        with open(main_path, 'w') as f:
            f.write(modified_content)
    
    def parse_logs_for_metrics(self):
        """Parse function_generation.log for iteration count and success"""
        log_path = Path("../success_run/function_generation.log")
        if not log_path.exists():
            return 0, False, 0
        
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Count iterations
        import re
        iterations = len(re.findall(r'=== ITERATION \d+ ===', content))
        
        # Check for success
        success = "Function successfully generated" in content
        
        # Get duration if available
        duration_match = re.search(r'Total time: ([\d.]+)', content)
        duration = float(duration_match.group(1)) if duration_match else 0
        
        return iterations, success, duration
    
    def check_function_promotion(self, function_name):
        """Check if function was promoted to safe"""
        safe_functions_path = Path("Utilities/safeFunctions.json")
        if not safe_functions_path.exists():
            return False
        
        try:
            with open(safe_functions_path, 'r') as f:
                data = json.load(f)
                return function_name in data.get('safe', [])
        except:
            return False
    
    def run_test(self, user_input, expected_function):
        """Run a single test and log results"""
        print(f"\n{'='*50}")
        print(f"Testing: {user_input}")
        print(f"Expected function: {expected_function}")
        print(f"{'='*50}")
        
        start_time = time.time()
        
        # Clear previous logs
        log_path = Path("../success_run/function_generation.log")
        if log_path.exists():
            os.remove(log_path)
        
        # Modify main.py with test input
        original_line = self.modify_main_for_test(user_input)
        
        result = {
            'test': expected_function,
            'user_input': user_input,
            'start_time': datetime.now().isoformat(),
            'iterations': 0,
            'success': False,
            'duration': 0,
            'promoted': False,
            'error': None
        }
        
        try:
            # Run the system
            print("Running system...")
            process = subprocess.Popen(
                [sys.executable, 'Core/main.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for completion (with timeout)
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
            
            # Parse results from logs
            iterations, success, log_duration = self.parse_logs_for_metrics()
            
            # Calculate actual duration
            duration = time.time() - start_time
            
            # Check if function was promoted
            promoted = self.check_function_promotion(expected_function)
            
            result.update({
                'iterations': iterations,
                'success': success,
                'duration': duration if duration > 0 else log_duration,
                'promoted': promoted,
                'stdout': stdout[:500] if stdout else None,  # First 500 chars
                'stderr': stderr[:500] if stderr else None
            })
            
            print(f"✓ Test completed - Iterations: {iterations}, Success: {success}")
            
        except subprocess.TimeoutExpired:
            result['error'] = "Timeout after 5 minutes"
            print("✗ Test timeout")
        except Exception as e:
            result['error'] = str(e)
            print(f"✗ Test error: {e}")
        finally:
            # Restore main.py
            self.restore_main(original_line)
        
        self.results.append(result)
        self.save_results()
        
        return result
    
    def run_all_tests(self, repetitions=1):
        """Run all calculator tests from thesis"""
        tests = [
            ("add 5 and 3", "add"),
            ("subtract 7 from 10", "subtract"),
            ("multiply 4 by 6", "multiply"),
            ("divide 20 by 4", "divide"),
            ("calculate square root of 16", "sqrt")
        ]
        
        for i in range(repetitions):
            print(f"\n{'#'*60}")
            print(f"# REPETITION {i+1} of {repetitions}")
            print(f"{'#'*60}")
            
            for user_input, func_name in tests:
                self.run_test(user_input, func_name)
                time.sleep(5)  # Delay between tests
    
    def save_results(self):
        """Save results to JSON file"""
        with open(self.log_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def print_summary(self):
        """Print summary of test results"""
        if not self.results:
            print("No test results available")
            return
        
        print(f"\n{'='*60}")
        print("CALCULATOR TEST SUMMARY")
        print(f"{'='*60}")
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        
        print(f"Total tests: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Failed: {total - successful}")
        
        # Calculate averages for successful tests
        successful_results = [r for r in self.results if r['success']]
        if successful_results:
            avg_iterations = sum(r['iterations'] for r in successful_results) / len(successful_results)
            avg_duration = sum(r['duration'] for r in successful_results) / len(successful_results)
            
            print(f"\nFor successful tests:")
            print(f"  Average iterations: {avg_iterations:.2f}")
            print(f"  Average duration: {avg_duration:.2f} seconds")
            
            # Group by function
            by_function = {}
            for r in self.results:
                func = r['test']
                if func not in by_function:
                    by_function[func] = []
                by_function[func].append(r)
            
            print("\nBy function:")
            for func, results in by_function.items():
                success_rate = sum(1 for r in results if r['success']) / len(results) * 100
                avg_iter = sum(r['iterations'] for r in results if r['success']) / max(1, sum(1 for r in results if r['success']))
                print(f"  {func}: {success_rate:.0f}% success, {avg_iter:.1f} avg iterations")

if __name__ == "__main__":
    # First check environment
    from test_setup import setup_test_environment
    
    if not setup_test_environment():
        print("Please fix environment issues before running tests")
        sys.exit(1)
    
    # Run tests
    tester = CalculatorTester()
    
    # Run each test once for debugging
    print("\n" + "="*60)
    print("RUNNING CALCULATOR TESTS")
    print("="*60)
    
    tester.run_all_tests(repetitions=1)
    tester.print_summary()
    
    print("\nResults saved to: calculator_test_results.json")