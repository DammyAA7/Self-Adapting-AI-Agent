#!/usr/bin/env python3
"""
HumanEval Function Validator
Validates generated functions against HumanEval test cases using direct import
"""
import sys
import os
import importlib
import traceback
from typing import Tuple, Optional, Dict
import tempfile
import contextlib
from io import StringIO


class HumanEvalValidator:
    """Validate functions against HumanEval test cases"""
    
    def __init__(self, functions_path: str = None):
        """
        Initialize validator
        
        Args:
            functions_path: Path to the functions.py file (default: auto-detect)
        """
        if functions_path is None:
            # Auto-detect functions.py path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            functions_path = os.path.join(parent_dir, 'functions.py')
        
        self.functions_path = functions_path
        self.functions_module = None
        
        print(f"🔧 HumanEval Validator initialized")
        print(f"📁 Functions path: {self.functions_path}")
    
    def load_functions_module(self) -> bool:
        """
        Load the functions.py module dynamically
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Ensure the path exists
            if not os.path.exists(self.functions_path):
                print(f"❌ Functions file not found: {self.functions_path}")
                return False
            
            # Get the directory and module name
            functions_dir = os.path.dirname(self.functions_path)
            
            # Add to path if not already there
            if functions_dir not in sys.path:
                sys.path.insert(0, functions_dir)
            
            # Import or reload the functions module
            if self.functions_module is None:
                import functions as functions_module
                self.functions_module = functions_module
            else:
                # Reload to get latest functions
                importlib.reload(self.functions_module)
            
            print(f"✅ Functions module loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading functions module: {e}")
            traceback.print_exc()
            return False
    
    def get_function(self, entry_point: str):
        """
        Get a function from the functions module
        
        Args:
            entry_point: Name of the function to retrieve
            
        Returns:
            Function object or None if not found
        """
        if not self.functions_module:
            if not self.load_functions_module():
                return None
        
        try:
            # Reload module to ensure we have the latest functions
            importlib.reload(self.functions_module)
            
            if hasattr(self.functions_module, entry_point):
                function = getattr(self.functions_module, entry_point)
                print(f"✅ Found function: {entry_point}")
                return function
            else:
                print(f"❌ Function '{entry_point}' not found in functions module")
                available_functions = [name for name in dir(self.functions_module) 
                                     if callable(getattr(self.functions_module, name)) 
                                     and not name.startswith('_')]
                print(f"📋 Available functions: {available_functions}")
                return None
                
        except Exception as e:
            print(f"❌ Error retrieving function '{entry_point}': {e}")
            return None
    
    def validate_function(self, entry_point: str, test_code: str, verbose: bool = False) -> Tuple[bool, str]:
        """
        Validate a function against HumanEval test cases
        
        Args:
            entry_point: Name of the function to test
            test_code: HumanEval test code to execute
            verbose: Print detailed output
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        try:
            # Get the function
            candidate_function = self.get_function(entry_point)
            if candidate_function is None:
                return False, f"Function '{entry_point}' not found"
            
            # Prepare test execution environment
            test_namespace = {
                'candidate': candidate_function,
                '__builtins__': __builtins__
            }
            
            # Capture output if verbose
            if verbose:
                output_capture = StringIO()
                with contextlib.redirect_stdout(output_capture):
                    with contextlib.redirect_stderr(output_capture):
                        # Execute the test code
                        exec(test_code, test_namespace)
                captured_output = output_capture.getvalue()
                if captured_output:
                    print(f"📄 Test output: {captured_output}")
            else:
                # Execute the test code without capturing output
                exec(test_code, test_namespace)
            
            # If we get here, all tests passed
            print(f"✅ All HumanEval tests passed for {entry_point}")
            return True, "All tests passed"
            
        except AssertionError as e:
            error_msg = f"Test assertion failed: {str(e)}"
            if verbose:
                print(f"❌ {error_msg}")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Test execution error: {str(e)}"
            if verbose:
                print(f"❌ {error_msg}")
                traceback.print_exc()
            return False, error_msg
    
    def validate_with_timeout(self, entry_point: str, test_code: str, timeout: int = 30, verbose: bool = False) -> Tuple[bool, str]:
        """
        Validate function with timeout protection
        
        Args:
            entry_point: Name of the function to test
            test_code: HumanEval test code
            timeout: Timeout in seconds
            verbose: Print detailed output
            
        Returns:
            Tuple[bool, str]: (success, error_message)
        """
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError(f"Test execution timed out after {timeout}s")
        
        try:
            # Set timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)
            
            # Run validation
            result = self.validate_function(entry_point, test_code, verbose)
            
            # Clear timeout
            signal.alarm(0)
            
            return result
            
        except TimeoutError as e:
            signal.alarm(0)  # Clear timeout
            error_msg = str(e)
            if verbose:
                print(f"⏱️ {error_msg}")
            return False, error_msg
        
        except Exception as e:
            signal.alarm(0)  # Clear timeout
            error_msg = f"Unexpected error: {str(e)}"
            if verbose:
                print(f"❌ {error_msg}")
            return False, error_msg
    
    def run_test_check(self, entry_point: str, test_code: str) -> Dict:
        """
        Run comprehensive test check and return detailed results
        
        Args:
            entry_point: Function name to test
            test_code: HumanEval test code
            
        Returns:
            Dict with test results and metadata
        """
        start_time = os.times().elapsed
        
        # Run validation
        success, error_msg = self.validate_with_timeout(entry_point, test_code, verbose=True)
        
        end_time = os.times().elapsed
        execution_time = end_time - start_time
        
        return {
            'entry_point': entry_point,
            'success': success,
            'error_message': error_msg if not success else None,
            'execution_time': execution_time,
            'test_code_length': len(test_code)
        }


def main():
    """Test the HumanEval validator"""
    print("🧪 Testing HumanEval Validator...")
    
    # Initialize validator
    validator = HumanEvalValidator()
    
    # Load extractor to get test case
    from humaneval_extractor import HumanEvalExtractor
    extractor = HumanEvalExtractor()
    
    if not extractor.problems:
        print("❌ No HumanEval problems loaded")
        return 1
    
    # Test with is_equal_to_sum_even (should exist in functions.py)
    test_task_id = "HumanEval/138"
    entry_point = "is_equal_to_sum_even"
    
    print(f"\n🎯 Testing function: {entry_point}")
    
    # Get test cases
    test_code = extractor.get_test_cases(test_task_id)
    if not test_code:
        print(f"❌ No test cases found for {test_task_id}")
        return 1
    
    print(f"📋 Test code length: {len(test_code)} characters")
    
    # Run comprehensive test
    results = validator.run_test_check(entry_point, test_code)
    
    print(f"\n📊 Test Results:")
    print(f"  Function: {results['entry_point']}")
    print(f"  Success: {'✅' if results['success'] else '❌'}")
    print(f"  Execution Time: {results['execution_time']:.3f}s")
    
    if not results['success']:
        print(f"  Error: {results['error_message']}")
        return 1
    
    print(f"\n🎉 HumanEval Validator working correctly!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)