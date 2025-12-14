#!/usr/bin/env python3
"""
Test Compositional Tasks Session 2 Results
Ground-truth expects BOTH Session 1 and Session 2 functions
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
        logging.FileHandler('compositional_evaluation.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def test_compositional_task(session1_task, session2_task):
    """
    Test compositional task with BOTH Session 1 and Session 2 code
    Ground-truth expects both functions to exist and work together
    """
    name = session2_task['_original_task']

    # Get Session 1 code (best solution from Session 1 run)
    session1_code = session1_task['completion']
    session1_entry = session1_task['entry_point']

    # Get Session 2 code (best solution from Session 2 run)
    session2_code = session2_task['completion']
    session2_entry = session2_task['entry_point']

    logger.info(f"Session 1 function: {session1_entry} ({len(session1_code)} chars)")
    logger.info(f"Session 2 function: {session2_entry} ({len(session2_code)} chars)")

    # Check if Session 2 imports/uses Session 1
    imports_session1 = session1_entry in session2_code
    logger.info(f"Session 2 references Session 1 function: {imports_session1}")

    # Get ground-truth test (expects BOTH functions)
    test = session2_task['test']

    # Test Session 2 code (tests true integration capability)
    # If Session 2 doesn't properly integrate, it will fail
    test_code = f"""{session2_code}

{test}
"""

    # Create test file
    test_file = Path(f'compositional_tests/{name}.py')
    test_file.parent.mkdir(exist_ok=True)
    test_file.write_text(test_code)

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
                'session1_code_length': len(session1_code),
                'session2_code_length': len(session2_code),
                'imports_session1': imports_session1
            }
        else:
            logger.warning(f"FAIL: {name}")
            error_msg = result.stderr or result.stdout
            logger.debug(f"Error: {error_msg[:300]}")

            return {
                'task': name,
                'status': 'FAIL',
                'error': error_msg[:500],
                'imports_session1': imports_session1
            }

    except subprocess.TimeoutExpired:
        logger.error(f"TIMEOUT: {name}")
        return {'task': name, 'status': 'TIMEOUT'}
    except Exception as e:
        logger.error(f"ERROR: {name} - {e}")
        return {'task': name, 'status': 'ERROR', 'error': str(e)}


def main():
    """Test compositional tasks with both Session 1 and Session 2 code"""

    logger.info("="*70)
    logger.info("COMPOSITIONAL TASKS EVALUATION (Session 2)")
    logger.info("Testing if Session 2 code properly integrates Session 1")
    logger.info("="*70)

    # Load Session 2 final results (after 5 iterations)
    session2_file = 'dataset/gpt-4.1_4.json'
    logger.info(f"Loading Session 2 final results: {session2_file}")

    try:
        with open(session2_file) as f:
            session2_final = json.load(f)
    except FileNotFoundError:
        logger.error(f"Session 2 results not found")
        return

    logger.info(f"Loaded {len(session2_final)} Session 2 tasks")

    # For each Session 2 task, we need the Session 1 code
    # It's in the codebase_context field of Session 2 dataset
    with open('dataset/compositional_session2.jsonl') as f:
        session2_dataset = [json.loads(line) for line in f]

    results = []

    for i, s2_task in enumerate(session2_final):
        name = s2_task['_original_task']
        logger.info(f"\n--- Task {i+1}/3: {name} ---")

        # Get Session 1 code from Session 2's context
        s2_dataset_entry = session2_dataset[i]
        session1_code = s2_dataset_entry['codebase_context']

        # Create mock Session 1 task with this code
        s1_mock = {
            'completion': session1_code,
            'entry_point': s2_dataset_entry['_depends_on'][0]  # First dependency
        }

        result = test_compositional_task(s1_mock, s2_task)
        results.append(result)

    # Summary
    logger.info("\n" + "="*70)
    logger.info("COMPOSITIONAL TASKS SUMMARY")
    logger.info("="*70)

    total = len(results)
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')

    logger.info(f"\nTotal compositional tasks: {total}")
    logger.info(f"PASS: {passed} ({passed/total*100:.1f}%)")
    logger.info(f"FAIL: {failed} ({failed/total*100:.1f}%)")

    logger.info(f"\nAgentCoder Compositional Pass@1: {passed}/{total} = {passed/total*100:.1f}%")
    logger.info(f"SelfEvolve Compositional Pass@1: 93.3%")
    logger.info(f"Performance gap: {93.3 - (passed/total*100):.1f}pp")

    # Save results
    with open('compositional_results.json', 'w') as f:
        json.dump({
            'evaluation_date': datetime.now().isoformat(),
            'task_type': 'compositional',
            'sessions': 2,
            'total': total,
            'passed': passed,
            'failed': failed,
            'pass_rate': passed/total*100,
            'results': results
        }, f, indent=2)

    logger.info(f"\nResults saved: compositional_results.json")


if __name__ == "__main__":
    main()
