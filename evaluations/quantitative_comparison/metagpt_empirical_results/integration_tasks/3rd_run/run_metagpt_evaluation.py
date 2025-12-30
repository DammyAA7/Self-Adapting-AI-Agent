#!/usr/bin/env python3
"""
Run MetaGPT on SelfEvolve tasks
- Uses FileAnalyzer from SelfEvolve framework for context extraction
- Reads problem definitions from problem.json files
- Gives context in user prompt (same approach as AgentCoder/AutoGen)
"""
import json
import subprocess
import sys
import logging
import re
from pathlib import Path
from datetime import datetime

# Add SelfEvolve framework
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework')
from file_analyzer.analyzer import SimpleAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('metagpt_evaluation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Dataset path
DATASET_PATH = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'

# 8 Non-compositional tasks
NON_COMPOSITIONAL_TASKS = [
    # Integration tasks (4)
    'patient_risk_analyzer',
    'salary_analyzer',
    'student_gpa_calculator',
    'inventory_replenishment',
    # Data Processing tasks (4)
    'book_recommender',
    'friend_suggester',
    'movielens_dataset',
    'performance_tracker',
]


def load_problem(task_name):
    """Load problem.json for a task"""
    problem_file = Path(DATASET_PATH) / task_name / 'problem.json'

    if not problem_file.exists():
        logger.error(f"problem.json not found: {problem_file}")
        return None

    with open(problem_file, 'r') as f:
        return json.load(f)


def extract_context(task_name):
    """Extract context using SelfEvolve's FileAnalyzer"""
    task_path = Path(DATASET_PATH) / task_name

    if not task_path.exists():
        logger.error(f"Task folder not found: {task_path}")
        return ""

    try:
        logger.info(f"Extracting context for: {task_name}")
        analyzer = SimpleAnalyzer(str(task_path))
        analyzer.read_all_files()

        # Build context string (same format as AgentCoder)
        context = f"FOLDER STRUCTURE:\n"
        context += f"Root: {task_name}/\n"

        for filepath in sorted(analyzer.all_files_content.keys()):
            context += f"  - {filepath}\n"
        context += "\n"

        # Add file contents (exclude problem.json)
        for filepath, file_data in analyzer.all_files_content.items():
            if 'problem.json' in filepath:
                continue

            file_type = file_data.get('type', 'unknown')
            if file_type in ['python', 'csv', 'json'] and 'content' in file_data:
                context += f"\n{'='*70}\n"
                context += f"FILE: {filepath}\n"
                context += f"{'='*70}\n"
                context += f"{file_data['content']}\n"

        logger.info(f"Context extracted: {len(context)} chars")
        return context

    except Exception as e:
        logger.error(f"Error extracting context: {e}")
        return ""


def run_metagpt(task_name, prompt, context):
    """Run MetaGPT CLI with context in user prompt"""

    logger.info(f"\n{'='*70}")
    logger.info(f"TASK: {task_name}")
    logger.info(f"{'='*70}")

    # Build full prompt (context + task)
    if context:
        full_prompt = f"""AVAILABLE CODEBASE/DATA:
{context}

TASK:
{prompt}

IMPORTANT: Generate ONLY the requested Python function. Do not create a full project.
The function must work with the existing codebase shown above.
Output the code inside ```python``` blocks.
"""
    else:
        full_prompt = f"""TASK:
{prompt}

Generate the Python function. Output the code inside ```python``` blocks.
"""

    # Save prompt for reference
    prompt_dir = Path('metagpt_prompts')
    prompt_dir.mkdir(exist_ok=True)
    (prompt_dir / f'{task_name}_prompt.txt').write_text(full_prompt)
    logger.info(f"Prompt saved: {len(full_prompt)} chars")

    # Run MetaGPT CLI
    try:
        logger.info("Running MetaGPT CLI...")

        result = subprocess.run(
            ['metagpt', full_prompt],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes max
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT'
        )

        logger.info(f"MetaGPT completed (exit code: {result.returncode})")

        # Save raw output
        output_dir = Path('metagpt_outputs')
        output_dir.mkdir(exist_ok=True)
        (output_dir / f'{task_name}_stdout.txt').write_text(result.stdout)
        (output_dir / f'{task_name}_stderr.txt').write_text(result.stderr)

        # Extract code from output
        code = extract_code(result.stdout)

        if code:
            logger.info(f"Code extracted: {len(code)} chars")
            (output_dir / f'{task_name}_code.py').write_text(code)
        else:
            logger.warning("No code extracted from MetaGPT output")

        return {
            'task': task_name,
            'status': 'COMPLETED',
            'code': code,
            'stdout': result.stdout
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout on {task_name}")
        return {'task': task_name, 'status': 'TIMEOUT', 'code': None}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {'task': task_name, 'status': 'ERROR', 'code': None, 'error': str(e)}


def extract_code(stdout):
    """Extract Python code from MetaGPT output"""
    if not stdout:
        return None

    def decode_escaped(code):
        """Convert escaped newlines/tabs to actual characters"""
        if '\\n' in code:
            code = code.replace('\\n', '\n')
        if '\\t' in code:
            code = code.replace('\\t', '\t')
        if '\\"' in code:
            code = code.replace('\\"', '"')
        return code.strip()

    # Method 1: ```python blocks - get one that contains 'def '
    pattern = r'```python\s*(.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        # Prefer clean code without escaped newlines
        for match in matches:
            if 'def ' in match and '\\n' not in match:
                return match.strip()
        # Fallback: decode escaped newlines
        for match in matches:
            if 'def ' in match or '\\ndef ' in match:
                return decode_escaped(match)

    # Method 2: Look for escaped code in JSON content field
    # Pattern: "content": "...```python\nimport...\n```..."
    pattern = r'"content":\s*"([^"]*```python\\n.*?\\n```[^"]*)"'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        for match in matches:
            # Extract just the code part
            code_match = re.search(r'```python\\n(.*?)\\n```', match, re.DOTALL)
            if code_match:
                return decode_escaped(code_match.group(1))

    # Method 3: ``` blocks with def (non-python tagged)
    pattern = r'```\s*(def\s+\w+.*?)\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    if matches:
        for match in matches:
            if '\\n' not in match:
                return match.strip()
            else:
                return decode_escaped(match)

    # Method 4: Look for function definition directly in text
    pattern = r'(def\s+\w+\s*\([^)]*\)[^:]*:[\s\S]*?)(?=\ndef\s|\n\n\n|\Z)'
    matches = re.findall(pattern, stdout)
    if matches:
        for match in matches:
            if '\\n' not in match:
                return match.strip()

    return None


def test_code(task_name, code, test_code):
    """Test generated code against ground-truth test from problem.json"""

    if not code:
        logger.warning(f"No code to test for {task_name}")
        return {'task': task_name, 'passed': False, 'status': 'NO_CODE'}

    if not test_code:
        logger.warning(f"No test_code in problem.json for {task_name}")
        return {'task': task_name, 'passed': False, 'status': 'NO_TEST'}

    # Create test file with ABSOLUTE path
    test_dir = Path('/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT/metagpt_tests')
    test_dir.mkdir(exist_ok=True)
    test_file = test_dir / f'{task_name}_test.py'

    # Combine generated code with ground-truth test
    # Add sys.path so imports like "from dataset.xxx" work
    full_test = f"""# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
{code}

# Ground-truth test from problem.json
{test_code}
"""
    test_file.write_text(full_test)

    # Run test
    try:
        logger.info(f"Testing {task_name}...")
        logger.info(f"Test file: {test_file}")

        result = subprocess.run(
            [sys.executable, str(test_file.absolute())],
            capture_output=True,
            text=True,
            timeout=60,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent'
        )

        passed = result.returncode == 0
        logger.info(f"Test: {'PASS' if passed else 'FAIL'}")

        if not passed:
            logger.error(f"Error: {result.stderr[:500]}")
            # Save error for analysis
            error_file = test_dir / f'{task_name}_error.txt'
            error_file.write_text(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")

        return {
            'task': task_name,
            'passed': passed,
            'status': 'PASS' if passed else 'FAIL',
            'error': result.stderr if not passed else None
        }

    except subprocess.TimeoutExpired:
        return {'task': task_name, 'passed': False, 'status': 'TIMEOUT'}
    except Exception as e:
        return {'task': task_name, 'passed': False, 'status': 'ERROR', 'error': str(e)}


def main():
    """Run MetaGPT on 8 non-compositional tasks"""

    logger.info("="*70)
    logger.info("METAGPT EVALUATION ON SELFEVOLVE DATASET")
    logger.info("8 Non-Compositional Tasks")
    logger.info("Context: FileAnalyzer from SelfEvolve framework")
    logger.info("Problems: problem.json from dataset/")
    logger.info(f"Started: {datetime.now()}")
    logger.info("="*70)

    # Create directories
    Path('metagpt_prompts').mkdir(exist_ok=True)
    Path('metagpt_outputs').mkdir(exist_ok=True)
    Path('metagpt_tests').mkdir(exist_ok=True)

    results = []
    passed = 0
    failed = 0

    for task_name in NON_COMPOSITIONAL_TASKS:
        logger.info(f"\n>>> Processing: {task_name}")

        # Load problem.json
        problem = load_problem(task_name)
        if not problem:
            results.append({
                'task': task_name,
                'status': 'NO_PROBLEM_JSON',
                'passed': False
            })
            failed += 1
            continue

        prompt = problem.get('prompt', '')
        test_code_str = problem.get('test_code', '')

        # Extract context using FileAnalyzer
        context = extract_context(task_name)

        # Run MetaGPT
        run_result = run_metagpt(task_name, prompt, context)

        # Test generated code
        test_result = test_code(task_name, run_result.get('code'), test_code_str)

        # Record results
        final_result = {
            'task': task_name,
            'problem_name': problem.get('problem_name', task_name),
            'metagpt_status': run_result['status'],
            'test_status': test_result['status'],
            'passed': test_result.get('passed', False),
            'code_generated': run_result.get('code') is not None,
            'context_size': len(context)
        }
        results.append(final_result)

        if test_result.get('passed'):
            passed += 1
        else:
            failed += 1

        # Save incremental results
        with open('metagpt_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Progress: {passed}/{len(results)} passed ({100*passed/len(results):.1f}%)")

    # Final summary
    logger.info("\n" + "="*70)
    logger.info("FINAL RESULTS")
    logger.info("="*70)

    print("\n" + "="*70)
    print("METAGPT EVALUATION SUMMARY")
    print("="*70)
    print(f"{'Task':<30} {'Context':<10} {'MetaGPT':<12} {'Test':<10}")
    print("-"*70)
    for r in results:
        ctx = f"{r.get('context_size', 0)//1000}k" if r.get('context_size') else '-'
        status = 'PASS' if r['passed'] else 'FAIL'
        print(f"{r['task']:<30} {ctx:<10} {r.get('metagpt_status', '-'):<12} {status:<10}")
    print("-"*70)
    print(f"TOTAL: {passed}/{len(results)} = {100*passed/len(results):.1f}%")
    print("="*70)

    logger.info(f"Passed: {passed}, Failed: {failed}")
    logger.info(f"Pass Rate: {passed}/{len(results)} = {100*passed/len(results):.1f}%")
    logger.info(f"Completed: {datetime.now()}")


if __name__ == "__main__":
    main()
