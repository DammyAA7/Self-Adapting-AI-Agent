#!/usr/bin/env python3
"""
Run MetaGPT CLI on SelfEvolve tasks
Using default CLI with context in prompt (same as AgentCoder/AutoGen)
"""
import json
import subprocess
import sys
import logging
import re
import os
from pathlib import Path
from datetime import datetime

# Add framework for context
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


# 8 Non-compositional tasks (same as AgentCoder/AutoGen)
NON_COMPOSITIONAL_TASKS = [
    # Integration tasks (4)
    {
        'name': 'patient_risk_analyzer',
        'requirement': """Create a function called patient_risk_score that takes a Hospital object and patient_id.
Navigate the class hierarchy to calculate risk using:
- patient.age, patient.get_total_conditions(), patient.get_average_severity()
- hospital.get_recent_records(patient_id, 90)
Return a float between 0-100 representing risk score."""
    },
    {
        'name': 'salary_analyzer',
        'requirement': """Create a function called calculate_department_salary_stats that takes an EmployeeDatabase object and department name.
Navigate the class hierarchy to calculate:
- average salary, min salary, max salary for the department
Return a dictionary with these statistics."""
    },
    {
        'name': 'student_gpa_calculator',
        'requirement': """Create a function called calculate_weighted_gpa that takes an EnrollmentSystem object and student_id.
Navigate the class hierarchy to calculate weighted GPA based on course credits and grades.
Return a float representing the weighted GPA."""
    },
    {
        'name': 'inventory_replenishment',
        'requirement': """Create a function called get_low_stock_alerts that takes an InventorySystem object.
Navigate the class hierarchy to identify items below reorder threshold.
Return a list of items needing replenishment with quantities."""
    },
    # Data Processing tasks (4)
    {
        'name': 'movie_api',
        'requirement': """Create a function called get_top_rated_movies that takes a movies data list and minimum_rating.
Filter movies with rating >= minimum_rating, sort by rating descending.
Return list of movie titles."""
    },
    {
        'name': 'book_recommender',
        'requirement': """Create a function called recommend_books that takes books data and user preferences (genre).
Find books matching the genre, sorted by rating.
Return top 5 recommended book titles."""
    },
    {
        'name': 'performance_tracker',
        'requirement': """Create a function called calculate_performance_score that takes employee performance records.
Calculate weighted performance score based on metrics.
Return a float representing overall performance."""
    },
    {
        'name': 'friend_suggester',
        'requirement': """Create a function called suggest_friends that takes social network data and user_id.
Find potential friends based on mutual connections.
Return list of suggested user_ids."""
    },
]


def get_context(task_name):
    """Get SAME context as AgentCoder/AutoGen using FileAnalyzer"""
    base = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    context_path = f'{base}/{task_name}'

    if not Path(context_path).exists():
        logger.warning(f"Context path not found: {context_path}")
        return ""

    try:
        analyzer = SimpleAnalyzer(context_path)
        analyzer.read_all_files()

        context = "FOLDER STRUCTURE:\n"
        for filepath in analyzer.all_files_content.keys():
            context += f"  - {filepath}\n"
        context += "\n"

        for filepath, file_data in analyzer.all_files_content.items():
            if 'problem.json' in filepath:
                continue
            if file_data.get('type') in ['python', 'csv', 'json'] and 'content' in file_data:
                context += f"\n{'='*70}\nFILE: {filepath}\n{'='*70}\n{file_data['content']}\n"

        return context
    except Exception as e:
        logger.error(f"Error extracting context: {e}")
        return ""


def run_metagpt(task_name, requirement, context):
    """Run MetaGPT with context (same approach as AgentCoder/AutoGen)"""

    logger.info(f"\n{'='*70}")
    logger.info(f"TASK: {task_name}")
    logger.info(f"{'='*70}")
    logger.info(f"Context size: {len(context)} chars")

    # Build full prompt with context
    if context:
        full_prompt = f"""AVAILABLE CODEBASE/DATA:
{context}

TASK:
{requirement}

IMPORTANT: Generate ONLY the requested Python function. Do not create a full project.
The function should work with the existing codebase shown above.
"""
    else:
        full_prompt = f"""TASK:
{requirement}

Generate the Python function."""

    # Write prompt to file for reference
    prompt_file = Path(f'metagpt_prompts/{task_name}_prompt.txt')
    prompt_file.parent.mkdir(exist_ok=True)
    prompt_file.write_text(full_prompt)

    # Run MetaGPT CLI
    try:
        logger.info("Running MetaGPT CLI...")

        result = subprocess.run(
            ['metagpt', full_prompt, '--project-name', task_name],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minutes max
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/MetaGPT'
        )

        logger.info(f"MetaGPT completed (exit code: {result.returncode})")

        # Save output
        output_file = Path(f'metagpt_outputs/{task_name}_output.txt')
        output_file.parent.mkdir(exist_ok=True)
        output_file.write_text(f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}")

        # Extract code from output (MetaGPT prints code in response)
        code = extract_code_from_output(result.stdout)

        return {
            'task': task_name,
            'status': 'COMPLETED' if result.returncode == 0 else 'ERROR',
            'code': code,
            'stdout': result.stdout,
            'stderr': result.stderr
        }

    except subprocess.TimeoutExpired:
        logger.error(f"Timeout on {task_name}")
        return {'task': task_name, 'status': 'TIMEOUT', 'code': None}
    except Exception as e:
        logger.error(f"Error running MetaGPT: {e}")
        return {'task': task_name, 'status': 'ERROR', 'error': str(e), 'code': None}


def extract_code_from_output(stdout):
    """Extract Python code from MetaGPT output"""
    # Look for code blocks
    code_pattern = r'```python\s*(.*?)\s*```'
    matches = re.findall(code_pattern, stdout, re.DOTALL)

    if matches:
        # Return the longest code block (likely the main function)
        return max(matches, key=len)

    # Try without language specifier
    code_pattern = r'```\s*(def .*?)\s*```'
    matches = re.findall(code_pattern, stdout, re.DOTALL)
    if matches:
        return max(matches, key=len)

    return None


def test_generated_code(task_name, code):
    """Test generated code against ground-truth tests"""

    if not code:
        logger.warning(f"No code to test for {task_name}")
        return {'task': task_name, 'status': 'NO_CODE', 'passed': False}

    # Load ground-truth test
    base = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    problem_file = Path(f'{base}/{task_name}/problem.json')

    if not problem_file.exists():
        logger.warning(f"No problem.json for {task_name}")
        return {'task': task_name, 'status': 'NO_TEST', 'passed': False}

    try:
        with open(problem_file) as f:
            problem = json.load(f)

        ground_truth_test = problem.get('test_code', '')
        if not ground_truth_test:
            logger.warning(f"No test_code in problem.json for {task_name}")
            return {'task': task_name, 'status': 'NO_TEST', 'passed': False}

        # Create test file
        test_dir = Path('metagpt_tests')
        test_dir.mkdir(exist_ok=True)
        test_file = test_dir / f'{task_name}_test.py'

        # Combine generated code with ground-truth test
        full_test = f"""# Generated code by MetaGPT
{code}

# Ground-truth test
{ground_truth_test}
"""
        test_file.write_text(full_test)

        # Run test
        logger.info(f"Testing {task_name}...")
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            timeout=60,
            cwd='/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent'
        )

        passed = result.returncode == 0
        logger.info(f"Test result: {'PASS' if passed else 'FAIL'}")

        if not passed:
            logger.error(f"Test error: {result.stderr[:500]}")

        return {
            'task': task_name,
            'status': 'PASS' if passed else 'FAIL',
            'passed': passed,
            'error': result.stderr if not passed else None
        }

    except Exception as e:
        logger.error(f"Error testing {task_name}: {e}")
        return {'task': task_name, 'status': 'ERROR', 'passed': False, 'error': str(e)}


def main():
    """Run MetaGPT on 8 non-compositional tasks"""

    logger.info("="*70)
    logger.info("METAGPT EVALUATION ON SELFEVOLVE DATASET")
    logger.info("8 Non-Compositional Tasks")
    logger.info(f"Started: {datetime.now()}")
    logger.info("="*70)

    # Create directories
    Path('metagpt_prompts').mkdir(exist_ok=True)
    Path('metagpt_outputs').mkdir(exist_ok=True)
    Path('metagpt_tests').mkdir(exist_ok=True)

    results = []
    passed = 0
    failed = 0

    for task in NON_COMPOSITIONAL_TASKS:
        task_name = task['name']
        requirement = task['requirement']

        # Get context (same as AgentCoder/AutoGen)
        context = get_context(task_name)

        # Run MetaGPT
        run_result = run_metagpt(task_name, requirement, context)

        # Test generated code
        test_result = test_generated_code(task_name, run_result.get('code'))

        # Record results
        final_result = {
            'task': task_name,
            'metagpt_status': run_result['status'],
            'test_status': test_result['status'],
            'passed': test_result.get('passed', False),
            'code_generated': run_result.get('code') is not None
        }
        results.append(final_result)

        if test_result.get('passed'):
            passed += 1
        else:
            failed += 1

        # Save incremental results
        with open('metagpt_results.json', 'w') as f:
            json.dump(results, f, indent=2)

        logger.info(f"Progress: {passed} passed, {failed} failed out of {len(results)}")

    # Final summary
    logger.info("\n" + "="*70)
    logger.info("FINAL RESULTS")
    logger.info("="*70)
    logger.info(f"Total: {len(results)}")
    logger.info(f"Passed: {passed}")
    logger.info(f"Failed: {failed}")
    logger.info(f"Pass Rate: {passed}/{len(results)} = {100*passed/len(results):.1f}%")
    logger.info(f"Completed: {datetime.now()}")

    # Print summary table
    print("\n" + "="*70)
    print("METAGPT EVALUATION SUMMARY")
    print("="*70)
    print(f"{'Task':<30} {'Status':<10} {'Passed':<10}")
    print("-"*70)
    for r in results:
        status = 'PASS' if r['passed'] else 'FAIL'
        print(f"{r['task']:<30} {r['test_status']:<10} {status:<10}")
    print("-"*70)
    print(f"TOTAL: {passed}/{len(results)} = {100*passed/len(results):.1f}%")


if __name__ == "__main__":
    main()
