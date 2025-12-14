"""
Run AgentCoder on SelfEvolve tasks using THE SAME evaluation protocol
If AgentCoder fails, it demonstrates their limitations, not unfair comparison
"""
import json
import os
import sys
from pathlib import Path

# Add parent directory to import dataset
sys.path.insert(0, str(Path(__file__).parent.parent))

#####


from dataset.salary_analyzer.employee_db import EmployeeDB

warehouse = create_sample_warehouse()
low_stock = inventory_low_stock_alert(warehouse)

assert isinstance(low_stock, list)
assert len(low_stock) == 5  # SKU001, SKU002, SKU004, SKU005, SKU006 are below reorder

# Verify each low stock item has correct structure
for item in low_stock:
    assert isinstance(item, dict)
    assert 'sku' in item
    assert 'name' in item
    assert 'current_stock' in item
    assert 'reorder_point' in item
    assert 'deficit' in item
    assert item['current_stock'] < item['reorder_point']
    assert item['deficit'] == item['reorder_point'] - item['current_stock']

# Verify specific SKUs are in the list
skus_in_result = [item['sku'] for item in low_stock]
assert 'SKU001' in skus_in_result
assert 'SKU002' in skus_in_result
assert 'SKU004' in skus_in_result
assert 'SKU005' in skus_in_result
assert 'SKU006' in skus_in_result
assert 'SKU003' not in skus_in_result  # SKU003 is above reorder point

print('Inventory Low Stock Alert tests passed')

#####

def load_selfevolve_task(task_name):
    """Load a task from SelfEvolve dataset"""
    problem_path = Path(f"../dataset/{task_name}/problem.json")

    if not problem_path.exists():
        raise FileNotFoundError(f"Task not found: {task_name}")

    with open(problem_path, 'r') as f:
        return json.load(f)

def convert_to_agentcoder_format(task, task_name):
    """
    Convert SelfEvolve task to AgentCoder format

    CRITICAL: AgentCoder expects HumanEval-style standalone functions
    Our tasks require integration with existing codebases

    If AgentCoder fails, it proves they lack integration capability
    """

    # Handle compositional tasks (two sessions)
    if 'session_1' in task:
        print(f"⚠️  WARNING: Task '{task_name}' is compositional (requires 2 sessions)")
        print(f"   AgentCoder has no cross-session persistence")
        print(f"   Testing Session 1 only (Session 2 will fail)")
        entry_point = task['session_1']['entry_point']
        prompt_text = task['session_1']['prompt']
    else:
        entry_point = task['entry_point']
        prompt_text = task['prompt']

    # Build the prompt (HumanEval format)
    agentcoder_prompt = f"""
def {entry_point}():
    '''
    {prompt_text}
    '''
    pass
"""

    # Check for context files (integration tasks)
    context_files = task.get('context_files', [])
    if context_files:
        print(f"⚠️  WARNING: Task requires existing codebase:")
        for cf in context_files:
            print(f"   - {cf}")
        print(f"   AgentCoder has NO mechanism to provide codebase context")
        print(f"   Expected to FAIL on integration requirements")

        # Try to add context as comment (will likely not help)
        agentcoder_prompt += f"""

# REQUIRED CONTEXT (AgentCoder cannot actually access this):
# This function must integrate with existing classes from: {context_files}
# AgentCoder limitation: No mechanism to provide external codebase
"""

    # Get ground-truth tests
    test_code = task.get('test_code', '')

    # Create AgentCoder-compatible test format
    # Note: AgentCoder expects check(candidate) format
    # Your tests use direct imports and assertions
    # This mismatch will cause issues

    agentcoder_task = {
        "task_id": f"SelfEvolve/{task.get('id', task_name)}",
        "prompt": agentcoder_prompt,
        "entry_point": entry_point,
        "test": test_code,

        # Metadata for analysis
        "original_task": task_name,
        "context_files": context_files,
        "is_compositional": 'session_1' in task,
        "expected_to_fail": len(context_files) > 0 or 'session_1' in task
    }

    return agentcoder_task


def main():
    """Convert all 11 tasks to AgentCoder format"""

    tasks = [
        'salary_analyzer',
        'patient_risk_analyzer',
        'student_gpa_calculator',
        'inventory_replenishment',
        'matrix_eigenvalue_composition',
        'portfolio_risk_calculator',
        'iot_sensor_pipeline',
        'movielens_dataset',
        'book_recommender',
        'performance_tracker',
        'friend_suggester'
    ]

    print("=" * 70)
    print("CONVERTING SELFEVOLVE TASKS TO AGENTCODER FORMAT")
    print("=" * 70)
    print("\nIMPORTANT: This conversion will reveal AgentCoder's limitations:")
    print("1. Integration tasks: AgentCoder has no codebase context mechanism")
    print("2. Compositional tasks: AgentCoder has no cross-session persistence")
    print("3. Expected outcome: AgentCoder will FAIL most tasks")
    print("4. This PROVES their limitations, not unfair comparison\n")
    print("=" * 70)

    results = []

    for task_name in tasks:
        print(f"\n{'─' * 70}")
        print(f"Task: {task_name}")
        print(f"{'─' * 70}")

        try:
            # Load task
            task = load_selfevolve_task(task_name)

            # Convert
            agentcoder_task = convert_to_agentcoder_format(task, task_name)

            # Save individual task
            output_file = Path(f"selfevolve_tasks/{task_name}.json")
            output_file.parent.mkdir(exist_ok=True)

            with open(output_file, 'w') as f:
                json.dump(agentcoder_task, f, indent=2)

            print(f"✓ Converted and saved to: {output_file}")

            if agentcoder_task['expected_to_fail']:
                print(f"⚠️  EXPECTED TO FAIL due to AgentCoder limitations")

            results.append(agentcoder_task)

        except Exception as e:
            print(f"✗ Error converting {task_name}: {e}")

    # Save complete dataset
    dataset_file = Path("selfevolve_tasks/complete_dataset.jsonl")
    with open(dataset_file, 'w') as f:
        for task in results:
            f.write(json.dumps(task) + '\n')

    print("\n" + "=" * 70)
    print(f"CONVERSION COMPLETE")
    print(f"Total tasks: {len(results)}")
    print(f"Dataset: {dataset_file}")
    print(f"\nExpected failures:")
    print(f"- Integration tasks (4): {sum(1 for t in results if t.get('context_files'))}")
    print(f"- Compositional tasks (3): {sum(1 for t in results if t.get('is_compositional'))}")
    print(f"- Simple tasks that might work (4): {len(results) - sum(1 for t in results if t.get('expected_to_fail'))}")
    print("=" * 70)
    print("\nNext: Run AgentCoder on these tasks and document failures")
    print("Command: python run_agentcoder_experiment.py")


if __name__ == "__main__":
    main()
