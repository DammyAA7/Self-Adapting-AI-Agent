#!/usr/bin/env python3
"""
Create task instances for SelfEvolve benchmark
Mirrors HumanEval's structure
"""
import json
import sys
from pathlib import Path

# Add framework path (absolute to avoid relative path issues)
framework_path = '/framework'
sys.path.insert(0, framework_path)
from file_analyzer.analyzer import SimpleAnalyzer


def get_context_for_task(task_name):
    """Extract SAME context AgentCoder received"""
    base_path = '/dataset'

    context_map = {
        'patient_risk_analyzer': f'{base_path}/patient_risk_analyzer',
        'student_gpa_calculator': f'{base_path}/student_gpa_calculator',
        'inventory_replenishment': f'{base_path}/inventory_replenishment',
        'salary_analyzer': f'{base_path}/salary_analyzer',
        'movielens_dataset': f'{base_path}/movielens_dataset',
        'book_recommender': f'{base_path}/book_recommender',
        'performance_tracker': f'{base_path}/performance_tracker',
        'friend_suggester': f'{base_path}/friend_suggester',
    }

    context_path = context_map.get(task_name)
    if not context_path:
        return ""

    if not Path(context_path).exists():
        print(f"Warning: Context path not found: {context_path}")
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


def create_task_instance(task_name, task_id, prompt, test_code):
    """
    Create task instance folder with prompt.txt, context.txt, test.txt
    Follows agbench structure
    """
    # Create task folder
    task_folder = Path(f"../Tasks/{task_name}")
    task_folder.mkdir(parents=True, exist_ok=True)

    print(f"\nCreating task: {task_name}")

    # 1. Create prompt.txt
    prompt_file = task_folder / "prompt.txt"
    prompt_file.write_text(prompt)
    print(f"  - prompt.txt: {len(prompt)} chars")

    # 2. Create context.txt (SAME as AgentCoder received)
    context = get_context_for_task(task_name)
    if context:
        context_file = task_folder / "context.txt"
        context_file.write_text(context)
        print(f"  - context.txt: {len(context)} chars")
    else:
        print(f"  - No context (standalone task)")

    # 3. Create test.txt (ground-truth)
    test_file = task_folder / "test.txt"
    test_file.write_text(test_code)
    print(f"  - test.txt: {len(test_code)} chars")

    # 4. Copy template files to task folder
    template_dir = Path("../Templates/AgentChat")
    for file in ['scenario.py', 'custom_code_executor.py', 'reasoning_model_context.py', 'requirements.txt']:
        src = template_dir / file
        if src.exists():
            dst = task_folder / file
            dst.write_text(src.read_text())

    # 5. Copy config.yaml
    config_src = Path("../config.yaml")
    if config_src.exists():
        (task_folder / "config.yaml").write_text(config_src.read_text())

    print(f"  - Template files copied")


def main():
    """Generate all task instances"""
    print("="*70)
    print("CREATING SELFEVOLVE TASKS FOR AUTOGEN")
    print("="*70)

    # Load non-compositional tasks (8 tasks)
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

    base_path = '/dataset'

    for task_name in tasks:
        # Load problem definition (absolute path)
        problem_file = Path(f"{base_path}/{task_name}/problem.json")

        with open(problem_file) as f:
            problem = json.load(f)

        prompt = problem['prompt']
        test_code = problem['test_code']
        task_id = problem['id']

        create_task_instance(task_name, task_id, prompt, test_code)

    print("\n" + "="*70)
    print(f"Created {len(tasks)} task instances in ../Tasks/")
    print("\nNext: Run AutoGen evaluation")
    print("  cd ../Tasks")
    print("  agbench run <task_folder>")
    print("="*70)


if __name__ == "__main__":
    main()
