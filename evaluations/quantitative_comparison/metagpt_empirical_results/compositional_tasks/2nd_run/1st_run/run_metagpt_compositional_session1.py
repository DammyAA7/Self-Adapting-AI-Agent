#!/usr/bin/env python3
"""
MetaGPT Compositional Tasks - SESSION 1
- Runs session_1 prompt from problem.json
- NO context given (starting fresh)
- NO ground-truth test (just generate and save code)
"""
import json
import subprocess
import sys
import logging
import re
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metagpt_compositional_s1.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

DATASET_PATH = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'

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


def extract_code(stdout):
    if not stdout:
        return None

    def decode_escaped(code):
        if '\\n' in code:
            code = code.replace('\\n', '\n')
        if '\\t' in code:
            code = code.replace('\\t', '\t')
        if '\\"' in code:
            code = code.replace('\\"', '"')
        return code.strip()

    pattern = r'```python\s*(.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        for match in matches:
            if 'def ' in match and '\\n' not in match:
                return match.strip()
        for match in matches:
            if 'def ' in match or '\\ndef ' in match:
                return decode_escaped(match)

    pattern = r'```\s*(def\s+\w+.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        return decode_escaped(matches[0]) if '\\n' in matches[0] else matches[0].strip()

    return None


def run_metagpt_session1(task_name, prompt):
    """Run Session 1: NO context"""
    logger.info(f"\n{'='*70}")
    logger.info(f"SESSION 1: {task_name}")
    logger.info(f"{'='*70}")

    full_prompt = f"""TASK:
{prompt}

Generate the Python function. Output the code inside ```python``` blocks.
"""

    prompt_dir = Path('metagpt_comp_s1_prompts')
    prompt_dir.mkdir(exist_ok=True)
    (prompt_dir / f'{task_name}_s1_prompt.txt').write_text(full_prompt)

    try:
        logger.info("Running MetaGPT CLI (Session 1, no context)...")
        result = subprocess.run(
            ['metagpt', full_prompt],
            capture_output=True,
            text=True,
            timeout=1200,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT'
        )

        logger.info(f"MetaGPT completed (exit code: {result.returncode})")

        output_dir = Path('metagpt_comp_s1_outputs')
        output_dir.mkdir(exist_ok=True)
        (output_dir / f'{task_name}_s1_stdout.txt').write_text(result.stdout)

        code = extract_code(result.stdout)
        if code:
            logger.info(f"Code extracted: {len(code)} chars")
            (output_dir / f'{task_name}_s1_code.py').write_text(code)
        else:
            logger.warning("No code extracted")

        return {'task': task_name, 'status': 'COMPLETED', 'code': code}

    except subprocess.TimeoutExpired:
        return {'task': task_name, 'status': 'TIMEOUT', 'code': None}
    except Exception as e:
        return {'task': task_name, 'status': 'ERROR', 'code': None, 'error': str(e)}


def main():
    logger.info("="*70)
    logger.info("METAGPT COMPOSITIONAL - SESSION 1")
    logger.info("3 Compositional Tasks (NO context, NO testing)")
    logger.info(f"Started: {datetime.now()}")
    logger.info("="*70)

    Path('metagpt_comp_s1_prompts').mkdir(exist_ok=True)
    Path('metagpt_comp_s1_outputs').mkdir(exist_ok=True)

    results = []

    for task_name in COMPOSITIONAL_TASKS:
        problem = load_problem(task_name)
        if not problem or 'session_1' not in problem:
            logger.error(f"No session_1 in {task_name}")
            results.append({'task': task_name, 'status': 'NO_SESSION_1', 'code': None})
            continue

        prompt = problem['session_1'].get('prompt', '')
        run_result = run_metagpt_session1(task_name, prompt)
        results.append(run_result)

        with open('metagpt_comp_s1_results.json', 'w') as f:
            json.dump(results, f, indent=2)

    print("\n" + "="*70)
    print("SESSION 1 SUMMARY (Code Generation Only)")
    print("="*70)
    for r in results:
        code_status = 'YES' if r.get('code') else 'NO'
        print(f"{r['task']:<35} {r['status']:<12} Code: {code_status}")
    print("="*70)
    logger.info(f"Completed: {datetime.now()}")


if __name__ == "__main__":
    main()
