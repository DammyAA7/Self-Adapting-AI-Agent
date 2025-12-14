#!/usr/bin/env python3
"""
Empirical Evaluation: AgentCoder Final Code vs Ground-Truth Tests
Tests AgentCoder's best selected solution after 5 iterations
"""
import json
import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agentcoder_evaluation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def test_agentcoder_solution(task):
    """
    Test AgentCoder's best solution against ground-truth
    Uses 'completion' field which contains the best solution AgentCoder selected
    """
    name = task['_original_task']

    # Get AgentCoder's BEST solution (they selected this from 5 variants)
    if 'completion' in task and task['completion']:
        code = task['completion']
        logger.info(f"Using AgentCoder's selected best solution for {name}")
    elif 'completion_list' in task and task['completion_list']:
        code = task['completion_list'][0]
        logger.warning(f"No 'completion' field for {name}, using first solution from completion_list")
    else:
        logger.error(f"No generated code found for {name}")
        return {'task': name, 'status': 'NO_CODE', 'error': 'No completion field'}

    logger.info(f"Code length: {len(code)} characters")

    # Check for imports (diagnostic)
    has_imports = 'from ' in code or 'import ' in code
    logger.info(f"Code has imports: {has_imports}")

    # Get ground-truth test
    test = task.get('test', task.get('test_code', ''))
    if not test:
        logger.error(f"No ground-truth test available for {name}")
        return {'task': name, 'status': 'NO_TEST', 'error': 'Missing test'}

    # Create test file
    test_file = Path(f'agentcoder_final_tests/{name}.py')
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text(code + '\n\n' + test)

    logger.info(f"Test file created: {test_file}")

    # Execute ground-truth test
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            logger.info(f"PASS: {name}")
            return {
                'task': name,
                'status': 'PASS',
                'code_length': len(code),
                'has_imports': has_imports
            }
        else:
            logger.warning(f"FAIL: {name}")
            error_msg = result.stderr or result.stdout
            logger.debug(f"Error output: {error_msg[:500]}")

            return {
                'task': name,
                'status': 'FAIL',
                'error': error_msg,
                'code_length': len(code),
                'has_imports': has_imports
            }

    except subprocess.TimeoutExpired:
        logger.error(f"TIMEOUT: {name} (exceeded 30 seconds)")
        return {'task': name, 'status': 'TIMEOUT'}
    except Exception as e:
        logger.error(f"ERROR: {name} - {type(e).__name__}: {e}")
        return {'task': name, 'status': 'ERROR', 'error': str(e)}


def main():
    """Execute evaluation on AgentCoder's final results"""

    logger.info("="*70)
    logger.info("AGENTCODER EMPIRICAL EVALUATION")
    logger.info("Testing best solutions after 5 iterations against ground-truth")
    logger.info("="*70)

    # Load AgentCoder's final results (iteration 4)
    results_file = '../gpt-4.1_4.json'
    logger.info(f"Loading final results from: {results_file}")

    try:
        with open(results_file) as f:
            agentcoder_final = json.load(f)
    except FileNotFoundError:
        logger.error(f"Results file not found: {results_file}")
        logger.error("Ensure test_executor_humaneval.py completed successfully")
        return

    logger.info(f"Loaded {len(agentcoder_final)} tasks")

    # Test each task
    results = []
    for i, task in enumerate(agentcoder_final, 1):
        logger.info(f"\n--- Task {i}/{len(agentcoder_final)}: {task['_original_task']} ---")
        result = test_agentcoder_solution(task)
        results.append(result)

    # Calculate metrics
    logger.info("\n" + "="*70)
    logger.info("EVALUATION SUMMARY")
    logger.info("="*70)

    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    errors = sum(1 for r in results if r['status'] in ['ERROR', 'NO_CODE', 'TIMEOUT'])

    logger.info(f"\nTotal tasks evaluated: {total}")
    logger.info(f"PASS: {passed} ({passed/total*100:.1f}%)")
    logger.info(f"FAIL: {failed} ({failed/total*100:.1f}%)")
    logger.info(f"ERROR/TIMEOUT: {errors} ({errors/total*100:.1f}%)")

    logger.info(f"\nAgentCoder Pass@1: {passed}/{total} = {passed/total*100:.1f}%")
    logger.info(f"SelfEvolve Pass@1: 92.7%")
    logger.info(f"Performance gap: {92.7 - (passed/total*100):.1f} percentage points")

    # Breakdown by category
    integration_tasks = ['patient_risk_analyzer', 'student_gpa_calculator',
                         'inventory_replenishment', 'salary_analyzer']
    data_tasks = ['movielens_dataset', 'book_recommender',
                  'performance_tracker', 'friend_suggester']

    integration_pass = sum(1 for r in results if r['task'] in integration_tasks and r['status'] == 'PASS')
    data_pass = sum(1 for r in results if r['task'] in data_tasks and r['status'] == 'PASS')

    logger.info(f"\nBreakdown by category:")
    logger.info(f"  Integration tasks: {integration_pass}/4 ({integration_pass/4*100:.1f}%)")
    logger.info(f"  Data processing tasks: {data_pass}/4 ({data_pass/4*100:.1f}%)")

    # Save detailed results
    output_file = 'agentcoder_empirical_results.json'
    with open(output_file, 'w') as f:
        json.dump({
            'evaluation_date': datetime.now().isoformat(),
            'agentcoder_version': 'arXiv:2312.13010',
            'model': 'gpt-4.1',
            'iterations': 5,
            'total_tasks': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'pass_rate': passed/total*100,
            'detailed_results': results
        }, f, indent=2)

    logger.info(f"\nDetailed results saved to: {output_file}")
    logger.info("Evaluation complete")


if __name__ == "__main__":
    main()

