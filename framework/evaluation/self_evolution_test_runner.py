"""
Self-Evolution Test Suite Runner
Executes test cases for the 11 self-evolution problems and logs results
"""
import sys
import os
# Add framework directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add parent directory (project root) to path so we can import from dataset/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import json
import logging
from datetime import datetime
import argparse


def setup_logging():
    """Setup logging to function_generation.log"""
    log_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'function_generation.log'
    )

    # Create logger
    logger = logging.getLogger('self_evolution_tests')
    logger.setLevel(logging.INFO)

    # Create file handler - APPEND mode preserves existing logs
    handler = logging.FileHandler(log_file, mode='a')  # 'a' = append, NOT overwrite
    handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


def load_test_suite():
    """Load test suite from individual problem.json files in dataset directories"""
    dataset_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'dataset'
    )

    test_suite = []

    # List all directories in dataset (excluding __pycache__)
    for dir_name in sorted(os.listdir(dataset_path)):
        dir_path = os.path.join(dataset_path, dir_name)

        # Skip non-directories and __pycache__
        if not os.path.isdir(dir_path) or dir_name == '__pycache__':
            continue

        # Check for problem.json file
        problem_file = os.path.join(dir_path, 'problem.json')
        if os.path.exists(problem_file):
            with open(problem_file, 'r') as f:
                problem_data = json.load(f)

                # Standardize the data structure for compatibility
                test_case = {
                    'id': problem_data['id'],
                    'problem_name': problem_data['problem_name'],
                    'test_code': problem_data['test_code'],
                    'task_id': problem_data.get('task_id', f"SelfEvolution/{problem_data['id']}"),
                    'domain': problem_data.get('domain', 'unknown'),
                    'directory': dir_name
                }

                # Add prompt information (handle both single and multi-session)
                if 'prompt' in problem_data:
                    test_case['prompt'] = problem_data['prompt']
                    test_case['entry_point'] = problem_data.get('entry_point', '')
                elif 'session_1' in problem_data:
                    # For multi-session problems, we might need special handling
                    test_case['is_multi_session'] = True
                    test_case['session_1'] = problem_data['session_1']
                    if 'session_2' in problem_data:
                        test_case['session_2'] = problem_data['session_2']

                # Add context files information
                test_case['context_files'] = problem_data.get('context_files', [])

                test_suite.append(test_case)

    # Sort by ID to maintain consistent order
    test_suite.sort(key=lambda x: x['id'])

    return test_suite


def run_test(test_id, logger):
    """
    Run a specific test by ID

    Args:
        test_id: ID of the test to run (1-11)
        logger: Logger instance for logging results

    Returns:
        (passed: bool, problem_name: str, error_msg: str)
    """
    # Load test suite
    test_suite = load_test_suite()

    # Find test by ID
    test_case = None
    for test in test_suite:
        if test['id'] == test_id:
            test_case = test
            break

    if not test_case:
        logger.error(f"Test ID {test_id} not found in test suite")
        return False, f"Unknown (ID {test_id})", "Test not found in suite"

    problem_name = test_case['problem_name']
    test_code = test_case['test_code']

    logger.info(f"Running test for: {problem_name} (ID {test_id})")
    print(f"\n{'='*60}")
    print(f"Running Test ID {test_id}: {problem_name}")
    print(f"{'='*60}\n")

    # Add dataset path to sys.path for imports to work
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    dataset_path = os.path.join(project_root, 'dataset')
    if dataset_path not in sys.path:
        sys.path.insert(0, dataset_path)
        logger.info(f"Added dataset path to sys.path: {dataset_path}")

    # Import functions module dynamically
    try:
        import importlib.util
        import functions as funcs_module

        # Reload to get latest changes
        importlib.reload(funcs_module)
        logger.info(f"Successfully imported functions from functions.py")
    except Exception as e:
        error_msg = f"Failed to import functions: {str(e)}"
        logger.error(error_msg)
        logger.info(f"===== TEST FAILED ===== ({problem_name})")
        return False, problem_name, error_msg

    # Execute the test code
    try:
        # Create a namespace for test execution
        test_namespace = {
            '__name__': '__main__',
            '__file__': __file__,
        }

        # Add all functions from functions.py to namespace
        for attr_name in dir(funcs_module):
            if not attr_name.startswith('_'):
                test_namespace[attr_name] = getattr(funcs_module, attr_name)

        # Execute the test code
        exec(test_code, test_namespace)

        # If we got here without exception, test passed
        logger.info(f"All assertions passed for {problem_name}")
        logger.info(f"===== TEST PASSED ===== ({problem_name})")
        print(f"\n✅ TEST PASSED: {problem_name}")
        return True, problem_name, None

    except AssertionError as e:
        error_msg = f"Assertion failed: {str(e)}"
        logger.error(f"Test assertion failed for {problem_name}: {error_msg}")
        logger.info(f"===== TEST FAILED ===== ({problem_name})")
        print(f"\n❌ TEST FAILED: {problem_name}")
        print(f"   Reason: {error_msg}")
        return False, problem_name, error_msg

    except Exception as e:
        error_msg = f"Execution error: {str(e)}"
        logger.error(f"Test execution error for {problem_name}: {error_msg}")
        logger.info(f"===== TEST FAILED ===== ({problem_name})")
        print(f"\n❌ TEST FAILED: {problem_name}")
        print(f"   Error: {error_msg}")
        return False, problem_name, error_msg


def run_all_tests(logger):
    """Run all tests in the suite"""
    test_suite = load_test_suite()

    results = []
    passed_count = 0
    failed_count = 0

    logger.info("="*60)
    logger.info("Starting Self-Evolution Test Suite Execution")
    logger.info(f"Total tests: {len(test_suite)}")
    logger.info("="*60)

    print(f"\n{'='*60}")
    print(f"Self-Evolution Test Suite - Running All Tests")
    print(f"Total tests: {len(test_suite)}")
    print(f"{'='*60}\n")

    for test in test_suite:
        test_id = test['id']
        passed, problem_name, error_msg = run_test(test_id, logger)

        results.append({
            'id': test_id,
            'problem_name': problem_name,
            'passed': passed,
            'error': error_msg
        })

        if passed:
            passed_count += 1
        else:
            failed_count += 1

    # Log summary
    pass_rate = (passed_count / len(test_suite)) * 100 if test_suite else 0

    logger.info("="*60)
    logger.info("Self-Evolution Test Suite Results")
    logger.info(f"Total tests: {len(test_suite)}")
    logger.info(f"Passed: {passed_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info(f"Pass Rate: {pass_rate:.1f}%")
    logger.info("="*60)

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {len(test_suite)}")
    print(f"Passed: {passed_count} ✅")
    print(f"Failed: {failed_count} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")
    print(f"{'='*60}\n")

    # Show details of failed tests
    if failed_count > 0:
        print("Failed Tests:")
        for result in results:
            if not result['passed']:
                print(f"  - ID {result['id']}: {result['problem_name']}")
                if result['error']:
                    print(f"    {result['error'][:100]}")
        print()

    return results


def main():
    parser = argparse.ArgumentParser(description='Run self-evolution test suite')
    parser.add_argument('--id', type=int, help='Run specific test by ID (1-11)')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    parser.add_argument('--list', action='store_true', help='List all available tests')

    args = parser.parse_args()

    # Setup logging
    logger = setup_logging()

    # List tests
    if args.list:
        test_suite = load_test_suite()
        print(f"\nAvailable Self-Evolution Tests:")
        print(f"{'='*80}")
        print(f"{'ID':<4} {'Problem Name':<35} {'Domain':<20} {'Directory':<20}")
        print(f"{'-'*4} {'-'*35} {'-'*20} {'-'*20}")
        for test in test_suite:
            print(f"{test['id']:<4} {test['problem_name'][:35]:<35} {test.get('domain', 'unknown')[:20]:<20} {test.get('directory', 'N/A')[:20]:<20}")
        print(f"{'='*80}")
        print(f"\nTotal: {len(test_suite)} tests\n")
        return

    # Run specific test
    if args.id:
        test_suite = load_test_suite()
        valid_ids = [t['id'] for t in test_suite]
        if args.id not in valid_ids:
            print(f"Error: Test ID must be one of: {sorted(valid_ids)}")
            sys.exit(1)

        passed, problem_name, error_msg = run_test(args.id, logger)

        if passed:
            print(f"\n✅ Test {args.id} ({problem_name}) PASSED")
            sys.exit(0)
        else:
            print(f"\n❌ Test {args.id} ({problem_name}) FAILED")
            if error_msg:
                print(f"Error: {error_msg}")
            sys.exit(1)

    # Run all tests
    elif args.all:
        results = run_all_tests(logger)

        # Exit with code 0 if all passed, 1 if any failed
        all_passed = all(r['passed'] for r in results)
        sys.exit(0 if all_passed else 1)

    # No arguments - show usage
    else:
        print("\nSelf-Evolution Test Runner")
        print("="*60)
        print("\nUsage:")
        print("  python evaluation/self_evolution_test_runner.py --list")
        print("  python evaluation/self_evolution_test_runner.py --id <1-11>")
        print("  python evaluation/self_evolution_test_runner.py --all")
        print("\nExamples:")
        print("  python evaluation/self_evolution_test_runner.py --list          # List all tests")
        print("  python evaluation/self_evolution_test_runner.py --id 2          # Run Patient Risk test")
        print("  python evaluation/self_evolution_test_runner.py --all           # Run all 11 tests")
        print()


if __name__ == "__main__":
    main()
