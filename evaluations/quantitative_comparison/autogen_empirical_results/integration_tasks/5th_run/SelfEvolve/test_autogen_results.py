#!/usr/bin/env python3
"""
Phase 2: External Validation of AutoGen Results
Extract generated code and test against ground-truth (same as AgentCoder)
"""
import json
import re
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
        logging.FileHandler('autogen_evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def extract_code_from_console_log(console_log_path):
    """
    Extract final generated code from AutoGen's console log
    Looks for last code block in coder's messages
    """
    with open(console_log_path) as f:
        log = f.read()

    # Find all code blocks from coder
    # Pattern: ```python ... ```
    code_blocks = re.findall(r'```python\n(.*?)\n```', log, re.DOTALL)

    if not code_blocks:
        logger.warning("No code blocks found in console log")
        return None

    # Return the last (most recent) code block
    final_code = code_blocks[-1].strip()
    logger.info(f"Extracted final code: {len(final_code)} chars")

    return final_code


def test_generated_code(task_id, generated_code, ground_truth_test):
    """Test AutoGen's generated code against ground-truth"""

    if not generated_code:
        return {'task': task_id, 'status': 'NO_CODE'}

    # Create test file (generated code + ground-truth)
    test_file = Path(f'validation_tests/{task_id}.py')
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text(generated_code + '\n\n' + ground_truth_test)

    # Run test
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent'
        )

        if result.returncode == 0:
            logger.info(f"PASS: {task_id}")
            return {
                'task': task_id,
                'status': 'PASS',
                'code_length': len(generated_code)
            }
        else:
            logger.warning(f"FAIL: {task_id}")
            return {
                'task': task_id,
                'status': 'FAIL',
                'error': result.stderr[:300],
                'code_length': len(generated_code)
            }

    except Exception as e:
        logger.error(f"ERROR: {task_id} - {e}")
        return {'task': task_id, 'status': 'ERROR', 'error': str(e)}


def main():
    """Validate all AutoGen results against ground-truth"""

    logger.info("="*70)
    logger.info("AUTOGEN EXTERNAL VALIDATION (Phase 2)")
    logger.info("Testing generated code against ground-truth (fair comparison)")
    logger.info("="*70)

    # Load JSONL to get ground-truth tests
    jsonl_path = 'Tasks/selfevolve_noncomp.jsonl'
    with open(jsonl_path) as f:
        tasks_data = [json.loads(line) for line in f]

    results = []

    # For each task in Results
    results_dir = Path('Results/selfevolve_noncomp')
    if not results_dir.exists():
        logger.error("No results found. Run agbench first.")
        return

    for task_data in tasks_data:
        task_id = task_data['id']
        logger.info(f"\n--- Validating: {task_id} ---")

        # Find result folder
        task_result_dir = results_dir / task_id / '0'
        if not task_result_dir.exists():
            logger.warning(f"Results not found for {task_id}")
            continue

        # Extract code from console log
        console_log = task_result_dir / 'console_log.txt'
        generated_code = extract_code_from_console_log(console_log)

        # Get ground-truth test
        ground_truth = task_data.get('_ground_truth_test', '')

        # Test
        result = test_generated_code(task_id, generated_code, ground_truth)
        results.append(result)

    # Summary
    logger.info("\n" + "="*70)
    logger.info("AUTOGEN EVALUATION SUMMARY")
    logger.info("="*70)

    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    logger.info(f"\nTotal: {total}")
    logger.info(f"PASS: {passed} ({passed/total*100:.1f}%)")
    logger.info(f"FAIL: {failed} ({failed/total*100:.1f}%)")

    logger.info(f"\nAutoGen Pass@1: {passed}/{total} = {passed/total*100:.1f}%")
    logger.info(f"AgentCoder Pass@1: 0/8 = 0.0%")
    logger.info(f"SelfEvolve Pass@1: 92.7%")

    # Save results
    with open('autogen_validation_results.json', 'w') as f:
        json.dump({
            'evaluation_date': datetime.now().isoformat(),
            'framework': 'AutoGen',
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': passed/total*100,
            'results': results
        }, f, indent=2)

    logger.info(f"\nResults: autogen_validation_results.json")


if __name__ == "__main__":
    main()
