#!/usr/bin/env python3
"""
MetaGPT Compositional Tasks - SESSION 2
- Uses Session 1 generated code as context
- Runs session_2 prompt from problem.json
- Tests against ground-truth test_code
"""
import json
import subprocess
import sys
import logging
import re
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metagpt_compositional_s2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DATASET_PATH = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
S1_OUTPUT_PATH = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT/metagpt_comp_s1_outputs'

COMPOSITIONAL_TASKS = [
    'matrix_eigenvalue_composition',
    'portfolio_risk_calculator',
    'iot_sensor_pipeline',
]


def load_problem(task_name):
    problem_file = Path(DATASET_PATH) / task_name / 'problem.json'
    if not problem_file.exists():
        return None
    with open(problem_file, 'r') as f:
        return json.load(f)


def load_session1_code(task_name):
    """Load code generated in Session 1"""
    code_file = Path(S1_OUTPUT_PATH) / f'{task_name}_s1_code.py'
    if not code_file.exists():
        logger.error(f"Session 1 code not found: {code_file}")
        return None
    return code_file.read_text()


def extract_code(stdout):
    if not stdout:
        return None

    def decode_escaped(code):
        """Decode escaped characters from JSON/string representation"""
        if '\\n' in code:
            code = code.replace('\\n', '\n')
        if '\\t' in code:
            code = code.replace('\\t', '\t')
        if '\\"' in code:
            code = code.replace('\\"', '"')
        return code.strip()

    # Method 1: ```python blocks
    pattern = r'```python\s*(.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        longest = max(matches, key=len)
        # Check if it has escaped chars (from JSON output)
        if '\\n' in longest:
            return decode_escaped(longest)
        return longest.strip()

    # Method 2: ``` blocks starting with import/def/from
    pattern = r'```\s*\n((?:import|def|from).*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        longest = max(matches, key=len)
        if '\\n' in longest:
            return decode_escaped(longest)
        return longest.strip()

    # Method 3: Any ``` block with code indicators
    pattern = r'```\s*\n(.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        code_blocks = [m for m in matches if 'def ' in m or 'import ' in m]
        if code_blocks:
            longest = max(code_blocks, key=len)
            if '\\n' in longest:
                return decode_escaped(longest)
            return longest.strip()

    return None


def get_workspace_files_before():
    """Get list of .py files in workspace before running"""
    workspace = Path('/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT/workspace')
    if workspace.exists():
        return set(workspace.glob('**/*.py'))
    return set()


def get_new_workspace_code(before_files):
    """Get code from newly created workspace files"""
    workspace = Path('/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT/workspace')
    if not workspace.exists():
        return None

    current_files = set(workspace.glob('**/*.py'))
    new_files = current_files - before_files

    if new_files:
        # Get the newest file
        newest = max(new_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"Found new workspace file: {newest}")
        return newest.read_text()
    return None


def run_metagpt_session2(task_name, prompt, session1_code):
    """Run Session 2: Session 1 code as context"""
    logger.info(f"\n{'='*70}")
    logger.info(f"SESSION 2: {task_name}")
    logger.info(f"{'='*70}")
    logger.info(f"Session 1 code: {len(session1_code)} chars")

    # Track workspace files before running
    before_files = get_workspace_files_before()

    full_prompt = f"""
python
{session1_code}


TASK:
{prompt}


Generate the Python function. Output the code inside ```python``` blocks.
"""


    prompt_dir = Path('metagpt_comp_s2_prompts')
    prompt_dir.mkdir(exist_ok=True)
    (prompt_dir / f'{task_name}_s2_prompt.txt').write_text(full_prompt)

    try:
        logger.info("Running MetaGPT CLI (Session 2, with S1 context)...")
        result = subprocess.run(
            ['metagpt', full_prompt],
            capture_output=True,
            text=True,
            timeout=600,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT'
        )

        logger.info(f"MetaGPT completed (exit code: {result.returncode})")

        output_dir = Path('metagpt_comp_s2_outputs')
        output_dir.mkdir(exist_ok=True)
        (output_dir / f'{task_name}_s2_stdout.txt').write_text(result.stdout)

        code = extract_code(result.stdout)
        if not code:
            # Fallback: check workspace for new files
            code = get_new_workspace_code(before_files)

        if code:
            logger.info(f"Code extracted: {len(code)} chars")
            (output_dir / f'{task_name}_s2_code.py').write_text(code)
        else:
            logger.warning("No code extracted from stdout or workspace")

        return {'task': task_name, 'status': 'COMPLETED', 'code': code}

    except subprocess.TimeoutExpired:
        return {'task': task_name, 'status': 'TIMEOUT', 'code': None}
    except Exception as e:
        return {'task': task_name, 'status': 'ERROR', 'code': None, 'error': str(e)}


def test_code(task_name, session1_code, session2_code, test_code_str):
    """Test combined Session 1 + Session 2 code against ground-truth"""

    if not session2_code:
        return {'task': task_name, 'passed': False, 'status': 'NO_CODE'}

    if not test_code_str:
        return {'task': task_name, 'passed': False, 'status': 'NO_TEST'}

    test_dir = Path('/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT/metagpt_comp_s2_tests')
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / f'{task_name}_test.py'

    ## Session 2 code (testing of composition) + ground-truth test
    full_test = f"""#
# Session 2 code (MetaGPT)
{session2_code}

# Ground-truth test
{test_code_str}
"""
    test_file.write_text(full_test)

    try:
        logger.info(f"Testing {task_name}...")
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent'
        )

        passed = result.returncode == 0
        logger.info(f"Test: {'PASS' if passed else 'FAIL'}")

        if not passed:
            logger.error(f"Error: {result.stderr[:500]}")
            (test_dir / f'{task_name}_error.txt').write_text(result.stderr)

        return {'task': task_name, 'passed': passed, 'status': 'PASS' if passed else 'FAIL'}

    except subprocess.TimeoutExpired:
        return {'task': task_name, 'passed': False, 'status': 'TIMEOUT'}
    except Exception as e:
        return {'task': task_name, 'passed': False, 'status': 'ERROR', 'error': str(e)}


def main():
    logger.info("="*70)
    logger.info("METAGPT COMPOSITIONAL - SESSION 2")
    logger.info("3 Compositional Tasks (S1 code as context, with testing)")
    logger.info(f"Started: {datetime.now()}")
    logger.info("="*70)

    Path('metagpt_comp_s2_prompts').mkdir(exist_ok=True)
    Path('metagpt_comp_s2_outputs').mkdir(exist_ok=True)
    Path('metagpt_comp_s2_tests').mkdir(exist_ok=True)

    results = []
    passed = 0
    failed = 0

    for task_name in COMPOSITIONAL_TASKS:
        problem = load_problem(task_name)
        if not problem or 'session_2' not in problem:
            logger.error(f"No session_2 in {task_name}")
            results.append({'task': task_name, 'status': 'NO_SESSION_2', 'passed': False})
            failed += 1
            continue

        # Load Session 1 code
        s1_code = load_session1_code(task_name)
        if not s1_code:
            results.append({'task': task_name, 'status': 'NO_S1_CODE', 'passed': False})
            failed += 1
            continue

        # Run Session 2
        prompt = problem['session_2'].get('prompt', '')
        run_result = run_metagpt_session2(task_name, prompt, s1_code)

        # Test combined code
        test_code_str = problem.get('test_code', '')
        test_result = test_code(task_name, s1_code, run_result.get('code'), test_code_str)

        final_result = {
            'task': task_name,
            'metagpt_status': run_result['status'],
            'test_status': test_result['status'],
            'passed': test_result.get('passed', False)
        }
        results.append(final_result)

        if test_result.get('passed'):
            passed += 1
        else:
            failed += 1

        with open('metagpt_comp_s2_results.json', 'w') as f:
            json.dump(results, f, indent=2)

    print("\n" + "="*70)
    print("SESSION 2 SUMMARY (Compositional)")
    print("="*70)
    print(f"{'Task':<35} {'MetaGPT':<12} {'Test':<10}")
    print("-"*70)
    for r in results:
        status = 'PASS' if r.get('passed') else 'FAIL'
        print(f"{r['task']:<35} {r.get('metagpt_status', '-'):<12} {status:<10}")
    print("-"*70)
    print(f"TOTAL: {passed}/{len(results)} = {100*passed/len(results):.1f}%")
    print("="*70)
    logger.info(f"Completed: {datetime.now()}")


if __name__ == "__main__":
    main()
