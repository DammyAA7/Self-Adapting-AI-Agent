#!/usr/bin/env python3
"""
Create JSONL file for agbench (proper format)
Each entry specifies template substitutions
"""
import json
import sys
from pathlib import Path

# Add framework
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework')
from file_analyzer.analyzer import SimpleAnalyzer


def get_context(task_name):
    """Get context (SAME as AgentCoder)"""
    base_path = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    context_path = f'{base_path}/{task_name}'

    if not Path(context_path).exists():
        return ""

    analyzer = SimpleAnalyzer(context_path)
    analyzer.read_all_files()

    context = ""
    for filepath, file_data in analyzer.all_files_content.items():
        if 'problem.json' in filepath:
            continue
        if file_data.get('type') in ['python', 'csv', 'json'] and 'content' in file_data:
            context += f"\nFILE: {filepath}\n{'='*70}\n"
            context += file_data['content'] + "\n"

    return context


def main():
    """Create JSONL file for agbench"""

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

    base_path = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    jsonl_records = []

    print("Creating agbench JSONL file...")
    print("="*70)

    for task_name in tasks:
        # Load problem
        with open(f'{base_path}/{task_name}/problem.json') as f:
            problem = json.load(f)

        # Get context
        context = get_context(task_name)

        # Convert test to check(candidate) format
        entry_point = problem['entry_point']
        test_code = problem['test_code']

        # Replace function_name( with candidate(
        converted_test = test_code.replace(f"{entry_point}(", "candidate(")

        # Wrap in check function
        wrapped_test = f"""def check(candidate):
{chr(10).join('    ' + line for line in converted_test.split(chr(10)))}
"""

        # Create agbench record (with converted test for AutoGen's validation)
        record = {
            "id": f"SelfEvolve_{problem['id']}",
            "template": "../Templates/AgentChat",
            "substitutions": {
                "prompt.txt": {"__PROMPT__": problem['prompt']},
                "test.txt": {"__TEST__": wrapped_test},
                "context.txt": {"__CONTEXT__": context if context else ""},
                "custom_code_executor.py": {"__ENTRY_POINT__": entry_point}  # Function name
            }
        }

        jsonl_records.append(record)
        print(f"Added: {task_name}")
        print(f"  ID: {record['id']}")
        print(f"  Context: {len(context)} chars")

    # Save JSONL
    output = Path('../Tasks/selfevolve_noncomp.jsonl')
    with open(output, 'w') as f:
        for record in jsonl_records:
            f.write(json.dumps(record) + '\n')

    print("\n" + "="*70)
    print(f"Created: {output}")
    print(f"Tasks: {len(jsonl_records)}")
    print("\nRun: agbench run Tasks/selfevolve_noncomp.jsonl")


if __name__ == "__main__":
    main()
