#!/usr/bin/env python3
"""
Convert ground-truth tests to check(candidate) format for AutoGen
Wraps tests so AutoGen's custom_code_executor can use them
"""
import json
from pathlib import Path


def convert_test_to_check_format(test_code, entry_point):
    """
    Convert direct test to check(candidate) format

    Original:
        score = patient_risk_score(hospital, 'P001')

    Converted:
        def check(candidate):
            score = candidate(hospital, 'P001')
    """
    # Replace function calls with candidate()
    # Pattern: function_name( → candidate(
    converted = test_code.replace(f"{entry_point}(", "candidate(")

    # Wrap in check function
    wrapped = f"""def check(candidate):
{chr(10).join('    ' + line for line in converted.split(chr(10)))}
"""

    return wrapped


def main():
    """Convert all tests to check(candidate) format"""

    base_path = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    tasks = [
        'patient_risk_analyzer',
        'student_gpa_calculator',
        'inventory_replenishment',
        'movielens_dataset',
        'book_recommender',
        'performance_tracker',
        'friend_suggester',
        'salary_analyzer'
    ]

    print("Converting tests to check(candidate) format...")
    print("="*70)

    converted_tests = {}

    for task_name in tasks:
        # Load problem
        with open(f'{base_path}/{task_name}/problem.json') as f:
            problem = json.load(f)

        original_test = problem['test_code']
        entry_point = problem['entry_point']

        # Convert to check(candidate) format
        converted = convert_test_to_check_format(original_test, entry_point)

        converted_tests[task_name] = {
            'entry_point': entry_point,
            'converted_test': converted
        }

        print(f"\n{task_name}:")
        print(f"  Entry point: {entry_point}")
        print(f"  Original: {len(original_test)} chars")
        print(f"  Converted: {len(converted)} chars")
        print(f"  Preview:")
        print(converted[:200])

    # Save converted tests
    output = Path('converted_tests.json')
    with open(output, 'w') as f:
        json.dump(converted_tests, f, indent=2)

    print("\n" + "="*70)
    print(f"Saved: {output}")
    print("\nNow update create_jsonl.py to use converted tests")


if __name__ == "__main__":
    main()
