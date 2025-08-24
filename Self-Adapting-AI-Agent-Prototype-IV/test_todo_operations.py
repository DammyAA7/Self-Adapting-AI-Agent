"""
Test ToDo operations matching thesis evaluation
"""
import csv
import os
import json
import time
import subprocess
import sys
from pathlib import Path
from datetime import datetime

class TodoTester:
    def __init__(self):
        self.results = []
        self.test_csv = 'test_todo.csv'
        self.log_file = "todo_test_results.json"
        
    def setup_test_csv(self):
        """Create test CSV with sample data"""
        with open(self.test_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'todo', 'status', 'priority', 'created_at', 'completed_at'])
            writer.writerow(['1', 'Sample task 1', 'pending', 'medium', '2024-01-01 10:00:00', ''])
            writer.writerow(['2', 'Sample task 2', 'pending', 'high', '2024-01-02 11:00:00', ''])
            writer.writerow(['3', 'Sample task 3', 'completed', 'low', '2024-01-03 12:00:00', '2024-01-04 13:00:00'])
            writer.writerow(['4', 'Sample task 4', 'in_progress', 'medium', '2024-01-04 14:00:00', ''])
            writer.writerow(['5', 'Sample task 5', 'pending', 'high', '2024-01-05 15:00:00', ''])
        print(f"✓ Created test CSV with 5 sample todos")
    
    def check_function_exists(self, function_name):
        """Check if function exists in tools.json"""
        tools_path = Path("Tool_Descriptor_Gen/tools.json")
        if not tools_path.exists():
            return False
        
        try:
            with open(tools_path, 'r') as f:
                tools = json.load(f)
                for tool in tools:
                    if tool.get('function', {}).get('name') == function_name:
                        return True
        except:
            pass
        return False
    
    def modify_main_for_test(self, user_input):
        """Temporarily modify main.py to use test input"""
        main_path = Path("Core/main.py")
        
        # Read the current main.py
        with open(main_path, 'r') as f:
            content = f.read()
        
        # Find and replace the user input line
        # Look for the current input line
        import re
        pattern = r'        \{"role": "user", "content": ".*"\}  # .*,'
        new_line = f'        {{"role": "user", "content": "{user_input}"}}  # Test input,'
        
        # Store original for restoration
        match = re.search(pattern, content)
        original_line = match.group(0) if match else '        {"role": "user", "content": "delete todo 5"}  # Example user input,'
        
        # Replace with test input
        modified_content = re.sub(pattern, new_line, content)
        
        # Write back the modified content
        with open(main_path, 'w') as f:
            f.write(modified_content)
        
        return original_line
    
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
        """Parse function_generation.log for metrics"""
        log_path = Path("function_generation.log")
        stats_path = Path("function_generation_stats.json")
        
        iterations = 0
        success = False
        generated_new = False
        duration = 0
        
        if log_path.exists():
            with open(log_path, 'r') as f:
                content = f.read()
            
            # Count iterations
            import re
            iterations = len(re.findall(r'=== ITERATION \d+ ===', content))
            
            # Check for success
            success = "Function successfully generated" in content
            
            # Check if new function was generated
            generated_new = "STARTING FUNCTION GENERATION" in content
        
        # Also check stats file for more details
        if stats_path.exists():
            try:
                with open(stats_path, 'r') as f:
                    stats = json.load(f)
                    # Get latest session info if available
            except:
                pass
        
        return iterations, success, generated_new, duration
    
    def run_test(self, user_input, expected_function, should_exist=None):
        """Run a single test and log results"""
        print(f"\n{'='*50}")
        print(f"Testing: {user_input}")
        print(f"Expected function: {expected_function}")
        
        # Check if function already exists
        exists_before = self.check_function_exists(expected_function)
        print(f"Function exists before test: {exists_before}")
        
        if should_exist is not None:
            print(f"Should exist: {should_exist}")
        print(f"{'='*50}")
        
        start_time = time.time()
        
        # Clear previous logs
        log_path = Path("function_generation.log")
        if log_path.exists():
            os.remove(log_path)
        
        # Modify main.py with test input
        original_line = self.modify_main_for_test(user_input)
        
        result = {
            'test': expected_function,
            'user_input': user_input,
            'start_time': datetime.now().isoformat(),
            'existed_before': exists_before,
            'iterations': 0,
            'success': False,
            'generated_new': False,
            'duration': 0,
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
            
            # Wait for completion
            stdout, stderr = process.communicate(timeout=300)  # 5 minute timeout
            
            # Parse results
            iterations, success, generated_new, log_duration = self.parse_logs_for_metrics()
            
            # Calculate actual duration
            duration = time.time() - start_time
            
            # Check if function exists after
            exists_after = self.check_function_exists(expected_function)
            
            result.update({
                'iterations': iterations,
                'success': success or exists_after,  # Success if function now exists
                'generated_new': generated_new,
                'exists_after': exists_after,
                'duration': duration,
                'stdout': stdout[:500] if stdout else None,
                'stderr': stderr[:500] if stderr else None
            })
            
            if generated_new:
                print(f"✓ Generated new function - Iterations: {iterations}")
            elif exists_before:
                print(f"✓ Used existing function")
            else:
                print(f"✓ Test completed - Success: {success}")
            
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
    
    def test_existing_functions(self):
        """Test functions that already exist (should not trigger generation)"""
        print("\n" + "="*60)
        print("TESTING EXISTING FUNCTIONS")
        print("="*60)
        
        tests = [
            ("add todo 'Buy groceries'", "add_todo", True),
            ("delete todo 3", "delete_todo", True)
        ]
        
        for user_input, func_name, should_exist in tests:
            self.run_test(user_input, func_name, should_exist)
            time.sleep(3)
    
    def test_new_generation(self):
        """Test generation of missing functions"""
        print("\n" + "="*60)
        print("TESTING NEW FUNCTION GENERATION")
        print("="*60)
        
        tests = [
            ("update todo 2 to completed", "update_todo"),
            ("list all pending todos", "list_todos"),
            ("mark todo 4 as done", "mark_todo_done"),
            ("get todo details for id 3", "get_todo")
        ]
        
        for user_input, expected_func in tests:
            self.run_test(user_input, expected_func, False)
            time.sleep(5)
    
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
        print("TODO TEST SUMMARY")
        print(f"{'='*60}")
        
        total = len(self.results)
        successful = sum(1 for r in self.results if r['success'])
        generated_new = sum(1 for r in self.results if r['generated_new'])
        used_existing = sum(1 for r in self.results if r['existed_before'] and not r['generated_new'])
        
        print(f"Total tests: {total}")
        print(f"Successful: {successful} ({successful/total*100:.1f}%)")
        print(f"Generated new functions: {generated_new}")
        print(f"Used existing functions: {used_existing}")
        
        # Calculate averages for generated functions
        generated_results = [r for r in self.results if r['generated_new']]
        if generated_results:
            avg_iterations = sum(r['iterations'] for r in generated_results) / len(generated_results)
            avg_duration = sum(r['duration'] for r in generated_results) / len(generated_results)
            
            print(f"\nFor newly generated functions:")
            print(f"  Average iterations: {avg_iterations:.2f}")
            print(f"  Average duration: {avg_duration:.2f} seconds")

if __name__ == "__main__":
    # First check environment
    from test_setup import setup_test_environment
    
    if not setup_test_environment():
        print("Please fix environment issues before running tests")
        sys.exit(1)
    
    # Run tests
    tester = TodoTester()
    
    # Setup test data
    tester.setup_test_csv()
    
    print("\n" + "="*60)
    print("RUNNING TODO OPERATION TESTS")
    print("="*60)
    
    # Test existing functions (should be fast, no generation)
    tester.test_existing_functions()
    
    # Test new function generation (will trigger TDD flow)
    tester.test_new_generation()
    
    # Print summary
    tester.print_summary()
    
    print("\nResults saved to: todo_test_results.json")