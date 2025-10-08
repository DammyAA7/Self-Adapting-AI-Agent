#!/usr/bin/env python3
"""
CodeEval-Pro (HumanEval Pro) Evaluator
Evaluates generated functions against HumanEval Pro test cases
"""

import sys
import os
import json
import traceback
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple
import ast
import re

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all functions from Unit_Test/functions.py
try:
    from Unit_Test.functions import *
except ImportError as e:
    print(f"Warning: Could not import from Unit_Test.functions: {e}")
    print("Some functions may not be available for testing")

class CodeEvalProEvaluator:
    """Evaluator for HumanEval Pro benchmark problems"""

    def __init__(self, dataset_path: str = None):
        """Initialize evaluator with path to HumanEval Pro dataset"""
        if dataset_path is None:
            # Default path to HumanEval Pro dataset
            dataset_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/CodeEval-Pro-main/dataset/humaneval_pro.json"

        self.dataset_path = dataset_path
        self.problems = self._load_dataset()
        self.log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(self.log_dir, exist_ok=True)

    def _load_dataset(self) -> Dict:
        """Load HumanEval Pro dataset from JSON file"""
        try:
            with open(self.dataset_path, 'r') as f:
                data = json.load(f)
            # Convert list to dict indexed by ID for easy access
            return {problem['id']: problem for problem in data}
        except FileNotFoundError:
            print(f"Error: Dataset not found at {self.dataset_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.dataset_path}")
            return {}

    def get_problem(self, problem_id: int) -> Dict:
        """Get a specific problem by ID"""
        if problem_id not in self.problems:
            raise ValueError(f"Problem ID {problem_id} not found in dataset")
        return self.problems[problem_id]

    def extract_test_code(self, problem: Dict) -> str:
        """Extract and prepare test code from problem definition"""
        # HumanEval Pro has different test formats
        if 'test_code' in problem:
            return problem['test_code']
        elif 'test' in problem:
            return problem['test']
        elif 'test_list' in problem:
            # Some problems have test_list instead of test
            return '\n'.join(problem['test_list'])
        elif 'unit_tests' in problem:
            return problem['unit_tests']
        else:
            return ""

    def prepare_test_environment(self) -> Dict:
        """Prepare the environment with available functions"""
        # Get all defined functions from current scope
        env = {}

        # Add all imported functions from Unit_Test.functions
        for name, obj in globals().items():
            if callable(obj) and not name.startswith('_'):
                env[name] = obj

        # Also try to import from functions.py in main directory
        try:
            functions_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'functions.py'
            )
            if os.path.exists(functions_path):
                with open(functions_path, 'r') as f:
                    exec(f.read(), env)
        except Exception as e:
            print(f"Warning: Could not load functions.py: {e}")

        return env

    def run_tests(self, problem_id: int, verbose: bool = True) -> Tuple[bool, Dict]:
        """
        Run tests for a specific problem ID
        Returns: (success, results_dict)
        """
        results = {
            'problem_id': problem_id,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'tests_passed': 0,
            'tests_failed': 0,
            'errors': [],
            'details': []
        }

        try:
            # Get problem
            problem = self.get_problem(problem_id)
            results['problem_name'] = problem.get('name', f'Problem_{problem_id}')
            results['task_id'] = problem.get('task_id', f'HumanEval/{problem_id}')

            if verbose:
                print(f"\n{'='*60}")
                print(f"Testing Problem ID {problem_id}: {results['problem_name']}")
                print(f"Task: {results['task_id']}")
                print(f"{'='*60}")

            # Get test code
            test_code = self.extract_test_code(problem)
            if not test_code:
                results['errors'].append("No test code found for this problem")
                return False, results

            # Prepare environment
            env = self.prepare_test_environment()

            # Add test utilities
            env['__test_results__'] = []

            # For now, we won't track individual assertions
            # Just run the tests and see if they pass or fail overall

            # Execute test code
            try:
                # First, check if we have the required function
                # Extract function name from test code (common patterns)
                func_names = re.findall(r'def test_(\w+)|(\w+)\(', test_code)
                required_funcs = set()
                for match in func_names:
                    if match[0]:
                        required_funcs.add(match[0])
                    elif match[1] and match[1] not in ['assert', 'print', 'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple', 'type', 'isinstance', 'range', 'enumerate']:
                        required_funcs.add(match[1])

                # Check if required functions exist
                missing_funcs = []
                builtin_funcs = dir(__builtins__)  # Get list of builtin function names
                for func_name in required_funcs:
                    if func_name not in env and func_name not in builtin_funcs:
                        missing_funcs.append(func_name)

                if missing_funcs:
                    results['errors'].append(f"Missing required functions: {', '.join(missing_funcs)}")
                    if verbose:
                        print(f"❌ Missing functions: {', '.join(missing_funcs)}")
                    return False, results

                # Execute the test code
                exec(test_code, env)

                # If we get here without exception, all tests passed
                results['tests_passed'] = 1
                results['details'].append("✓ All tests passed")
                results['success'] = True

                if verbose:
                    if results['success']:
                        print(f"✅ All tests passed! ({results['tests_passed']} tests)")
                    else:
                        print(f"❌ Some tests failed: {results['tests_failed']} failed, {results['tests_passed']} passed")

            except AssertionError as e:
                results['tests_failed'] += 1
                error_msg = f"Assertion failed: {str(e)}"
                results['errors'].append(error_msg)
                results['details'].append(f"✗ {error_msg}")
                if verbose:
                    print(f"❌ {error_msg}")

            except Exception as e:
                error_msg = f"Test execution error: {str(e)}\n{traceback.format_exc()}"
                results['errors'].append(error_msg)
                if verbose:
                    print(f"❌ Error during test execution:")
                    print(traceback.format_exc())

        except Exception as e:
            error_msg = f"Evaluation error: {str(e)}"
            results['errors'].append(error_msg)
            if verbose:
                print(f"❌ {error_msg}")

        return results['success'], results

    def save_log(self, results: Dict, log_file: str = None) -> str:
        """Save evaluation results to a log file"""
        if log_file is None:
            # Generate log filename based on problem ID and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            problem_id = results.get('problem_id', 'unknown')
            log_file = os.path.join(self.log_dir, f"eval_problem_{problem_id}_{timestamp}.log")

        # Format log content
        log_content = []
        log_content.append("="*60)
        log_content.append(f"CodeEval-Pro Evaluation Log")
        log_content.append(f"Timestamp: {results.get('timestamp', 'N/A')}")
        log_content.append("="*60)
        log_content.append(f"Problem ID: {results.get('problem_id', 'N/A')}")
        log_content.append(f"Problem Name: {results.get('problem_name', 'N/A')}")
        log_content.append(f"Task ID: {results.get('task_id', 'N/A')}")
        log_content.append("-"*40)
        log_content.append(f"Result: {'SUCCESS ✅' if results.get('success') else 'FAILURE ❌'}")
        log_content.append(f"Tests Passed: {results.get('tests_passed', 0)}")
        log_content.append(f"Tests Failed: {results.get('tests_failed', 0)}")
        log_content.append("-"*40)

        if results.get('details'):
            log_content.append("Test Details:")
            for detail in results['details']:
                log_content.append(f"  {detail}")

        if results.get('errors'):
            log_content.append("-"*40)
            log_content.append("Errors:")
            for error in results['errors']:
                log_content.append(f"  {error}")

        log_content.append("="*60)

        # Write to file
        with open(log_file, 'w') as f:
            f.write('\n'.join(log_content))

        print(f"\n📝 Log saved to: {log_file}")
        return log_file

    def evaluate_multiple(self, problem_ids: List[int], save_logs: bool = True) -> Dict:
        """Evaluate multiple problems and return summary"""
        summary = {
            'total': len(problem_ids),
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'results': []
        }

        print(f"\nEvaluating {len(problem_ids)} problems...")
        print("="*60)

        for problem_id in problem_ids:
            success, results = self.run_tests(problem_id, verbose=True)

            if save_logs:
                self.save_log(results)

            summary['results'].append(results)
            if success:
                summary['passed'] += 1
            elif results['errors']:
                summary['errors'] += 1
            else:
                summary['failed'] += 1

        # Print summary
        print("\n" + "="*60)
        print("EVALUATION SUMMARY")
        print("="*60)
        print(f"Total Problems: {summary['total']}")
        print(f"✅ Passed: {summary['passed']} ({summary['passed']/summary['total']*100:.1f}%)")
        print(f"❌ Failed: {summary['failed']} ({summary['failed']/summary['total']*100:.1f}%)")
        print(f"⚠️  Errors: {summary['errors']} ({summary['errors']/summary['total']*100:.1f}%)")
        print("="*60)

        return summary


def main():
    """Command-line interface for the evaluator"""
    parser = argparse.ArgumentParser(description='Evaluate functions against HumanEval Pro test cases')
    parser.add_argument('problem_ids', nargs='+', type=int,
                       help='Problem ID(s) to evaluate (e.g., 3 6 8 10 11)')
    parser.add_argument('--dataset', type=str, default=None,
                       help='Path to HumanEval Pro dataset JSON')
    parser.add_argument('--no-log', action='store_true',
                       help='Do not save log files')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimal output')

    args = parser.parse_args()

    # Create evaluator
    evaluator = CodeEvalProEvaluator(dataset_path=args.dataset)

    # Check if dataset loaded
    if not evaluator.problems:
        print("Error: Could not load dataset. Please check the path.")
        sys.exit(1)

    # Evaluate problems
    if len(args.problem_ids) == 1:
        # Single problem
        problem_id = args.problem_ids[0]
        success, results = evaluator.run_tests(problem_id, verbose=not args.quiet)

        if not args.no_log:
            log_file = evaluator.save_log(results)
            print(f"\nLog file: {log_file}")

        # Exit with appropriate code
        sys.exit(0 if success else 1)
    else:
        # Multiple problems
        summary = evaluator.evaluate_multiple(args.problem_ids, save_logs=not args.no_log)

        # Exit with code based on results
        sys.exit(0 if summary['passed'] == summary['total'] else 1)


if __name__ == "__main__":
    main()