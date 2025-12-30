#!/usr/bin/env python3
"""
Extract Session 1 generated code and create Session 2 JSONL
Session 2 will have Session 1 code as context (same as AgentCoder approach)
"""
import json
import re
from pathlib import Path


def extract_code_from_log(console_log_path):
    """Extract final code from console log"""
    with open(console_log_path) as f:
        log = f.read()

    # Find all code blocks
    code_blocks = re.findall(r'```python\n(.*?)\n```', log, re.DOTALL)

    if not code_blocks:
        return None

    # Return last code block (final generated code)
    return code_blocks[-1].strip()


def main():
    """Extract Session 1 code and create Session 2 JSONL"""

    print("="*70)
    print("EXTRACTING SESSION 1 CODE FOR SESSION 2")
    print("="*70)

    base_path = '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/dataset'

    # Session 1 results mapping
    session1_tasks = [
        {
            'result_id': 'SelfEvolve_5_S1',
            'task_name': 'matrix_eigenvalue_composition',
            'problem_id': 5,
            's1_entry': 'matrix_operations',
            's2_entry': 'advanced_matrix_ops',
        },
        {
            'result_id': 'SelfEvolve_6_S1',
            'task_name': 'portfolio_risk_calculator',
            'problem_id': 6,
            's1_entry': 'calculate_stock_volatility',
            's2_entry': 'portfolio_risk_assessment',
        },
        {
            'result_id': 'SelfEvolve_7_S1',
            'task_name': 'iot_sensor_pipeline',
            'problem_id': 7,
            's1_entry': 'parse_sensor_reading',
            's2_entry': 'aggregate_temperature',
        }
    ]

    session2_records = []

    for task in session1_tasks:
        print(f"\n{task['task_name']}:")

        # Extract Session 1 code
        console_log = Path(f"/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/AutoGen/python/packages/agbench/benchmarks/SelfEvolve/Results/compositional_session1/{task['result_id']}/0/console_log.txt")
        s1_code = extract_code_from_log(console_log)

        print(s1_code)

        if not s1_code:
            print(f"  ERROR: No code extracted from {console_log}")
            continue

        print(f"  Session 1 code extracted: {len(s1_code)} chars")
        print(f"  Function: {task['s1_entry']}")

        # Load Session 2 prompt from problem.json
        problem_file = Path(f"{base_path}/{task['task_name']}/problem.json")
        with open(problem_file) as f:
            problem = json.load(f)

        s2 = problem['session_2']
        s2_prompt = s2['prompt']

        # Convert Session 2 test to check(candidate) format
        test_code = problem['test_code']
        converted_test = test_code.replace(f"{task['s2_entry']}(", "candidate(")
        wrapped_test = f"""def check(candidate):
{chr(10).join('    ' + line for line in converted_test.split(chr(10)))}
"""

        # Create Session 2 record with Session 1 code as context
        record = {
            "id": f"SelfEvolve_{task['problem_id']}_S2",
            "template": "../Templates/AgentChat",
            "substitutions": {
                "prompt.txt": {"__PROMPT__": s2_prompt},
                "test.txt": {"__TEST__": wrapped_test},
                "context.txt": {"__CONTEXT__": s1_code},  # Session 1 code here!
                "custom_code_executor.py": {"__ENTRY_POINT__": task['s2_entry']}
            }
        }

        session2_records.append(record)
        print(f"  Session 2 created:")
        print(f"    Entry: {task['s2_entry']}")
        print(f"    Context: {len(s1_code)} chars (Session 1 code)")

    # Save Session 2 JSONL
    output = Path('/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/AutoGen/python/packages/agbench/benchmarks/SelfEvolve/Tasks/compositional_session2.jsonl')
    with open(output, 'w') as f:
        for record in session2_records:
            f.write(json.dumps(record) + '\n')

    print("\n" + "="*70)
    print(f"Created: {output}")
    print(f"Tasks: {len(session2_records)}")
    print("\nRun: agbench run Tasks/compositional_session2.jsonl --native")
    print("="*70)


if __name__ == "__main__":
    main()
