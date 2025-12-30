#!/usr/bin/env python3
"""
Create Session 1 and Session 2 JSONL for compositional tasks
Same approach as AgentCoder: Session 1 (blank context) → Session 2 (Session 1 code as context)
"""
import json
from pathlib import Path


def convert_test_to_check_format(test_code, entry_point):
    """Convert test to check(candidate) format"""
    converted = test_code.replace(f"{entry_point}(", "candidate(")
    wrapped = f"""def check(candidate):
{chr(10).join('    ' + line for line in converted.split(chr(10)))}
"""
    return wrapped


def create_session1_jsonl():
    """Create Session 1 JSONL (3 compositional tasks, NO context)"""

    base_path = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'
    comp_tasks = ['matrix_eigenvalue_composition', 'portfolio_risk_calculator', 'iot_sensor_pipeline']

    jsonl_records = []

    print("CREATING SESSION 1 COMPOSITIONAL JSONL")
    print("="*70)

    for task_name in comp_tasks:
        # Load problem
        with open(f'{base_path}/{task_name}/problem.json') as f:
            problem = json.load(f)

        # Get Session 1 info
        s1 = problem['session_1']

        # Convert Session 1 test (if exists, otherwise empty)
        # For Session 1, we might not have separate tests
        # Let AutoGen just generate and run code
        test_code = "def check(candidate): pass  # Session 1: basic generation, no validation yet"

        record = {
            "id": f"SelfEvolve_{problem['id']}_S1",
            "template": "../Templates/AgentChat",
            "substitutions": {
                "prompt.txt": {"__PROMPT__": s1['prompt']},
                "test.txt": {"__TEST__": test_code},
                "context.txt": {"__CONTEXT__": ""},  # BLANK for Session 1
                "custom_code_executor.py": {"__ENTRY_POINT__": s1['entry_point']}
            }
        }

        jsonl_records.append(record)
        print(f"\nSession 1: {task_name}")
        print(f"  Entry: {s1['entry_point']}")
        print(f"  Context: BLANK (starting fresh)")

    # Save Session 1 JSONL
    output = Path('../Tasks/compositional_session1.jsonl')
    with open(output, 'w') as f:
        for record in jsonl_records:
            f.write(json.dumps(record) + '\n')

    print("\n" + "="*70)
    print(f"Created: {output}")
    print(f"Tasks: {len(jsonl_records)}")
    print("\nRun: agbench run Tasks/compositional_session1.jsonl --native")
    print("Then extract Session 1 code for Session 2")


if __name__ == "__main__":
    create_session1_jsonl()
