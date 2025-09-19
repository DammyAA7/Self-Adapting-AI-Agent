#!/usr/bin/env python3
"""
HumanEval Problem Mapping Configuration
Maps your system's problem names to official HumanEval task IDs
"""

# Target problems for TiCoder comparison
TARGET_PROBLEM_MAPPING = {
    # Your problem name -> HumanEval task ID
    "is_equal_to_sum_even_HE_138": "HumanEval/138",
    "smallest_change_HE_73": "HumanEval/73", 
    "decimal_to_binary_HE_79": "HumanEval/79",
    "car_race_collision_HE_41": "HumanEval/41",
    "count_up_to_HE_96": "HumanEval/96",
    "split_words_HE_125": "HumanEval/125",
    "move_one_ball_HE_109": "HumanEval/109",
    "match_parens_HE_119": "HumanEval/119",
    "rounded_avg_HE_103": "HumanEval/103",
    "sort_array_HE_88": "HumanEval/88"
}

# Reverse mapping: HumanEval task ID -> Your problem name
HUMANEVAL_TO_PROBLEM_MAPPING = {v: k for k, v in TARGET_PROBLEM_MAPPING.items()}

# Entry point verification (for safety)
EXPECTED_ENTRY_POINTS = {
    "HumanEval/138": "is_equal_to_sum_even",
    "HumanEval/73": "smallest_change", 
    "HumanEval/79": "decimal_to_binary",
    "HumanEval/41": "car_race_collision",
    "HumanEval/96": "count_up_to",
    "HumanEval/125": "split_words",
    "HumanEval/109": "move_one_ball",
    "HumanEval/119": "match_parens",
    "HumanEval/103": "rounded_avg",
    "HumanEval/88": "sort_array"
}

def get_humaneval_task_id(problem_name: str) -> str:
    """Get HumanEval task ID for a problem name"""
    return TARGET_PROBLEM_MAPPING.get(problem_name)

def get_problem_name(task_id: str) -> str:
    """Get problem name for a HumanEval task ID"""
    return HUMANEVAL_TO_PROBLEM_MAPPING.get(task_id)

def get_entry_point(task_id: str) -> str:
    """Get expected entry point for a HumanEval task ID"""
    return EXPECTED_ENTRY_POINTS.get(task_id)

def validate_problem_mapping(extractor) -> bool:
    """
    Validate that all mapped problems exist in HumanEval dataset
    and have expected entry points
    """
    print("🔍 Validating problem mapping...")
    
    all_valid = True
    
    for problem_name, task_id in TARGET_PROBLEM_MAPPING.items():
        # Check if task exists
        if not extractor.validate_task_id(task_id):
            print(f"❌ {task_id} not found in dataset")
            all_valid = False
            continue
            
        # Check entry point
        actual_entry = extractor.get_entry_point(task_id)
        expected_entry = EXPECTED_ENTRY_POINTS.get(task_id)
        
        if actual_entry != expected_entry:
            print(f"❌ {task_id}: Expected entry point '{expected_entry}', got '{actual_entry}'")
            all_valid = False
        else:
            print(f"✅ {task_id} -> {actual_entry}")
    
    return all_valid

def get_all_target_problems():
    """Get list of all target problem names"""
    return list(TARGET_PROBLEM_MAPPING.keys())

def get_all_target_task_ids():
    """Get list of all target HumanEval task IDs"""
    return list(TARGET_PROBLEM_MAPPING.values())

def is_target_problem(problem_name: str) -> bool:
    """Check if a problem name is one of our target problems"""
    return problem_name in TARGET_PROBLEM_MAPPING

def is_target_task_id(task_id: str) -> bool:
    """Check if a task ID is one of our target problems"""
    return task_id in HUMANEVAL_TO_PROBLEM_MAPPING


def main():
    """Test the problem mapping"""
    print("🗺️  Testing HumanEval Problem Mapping...")
    
    # Load extractor to validate
    from humaneval_extractor import HumanEvalExtractor
    extractor = HumanEvalExtractor()
    
    if not extractor.problems:
        print("❌ Cannot validate - no problems loaded")
        return 1
    
    # Validate all mappings
    if validate_problem_mapping(extractor):
        print(f"\n✅ All {len(TARGET_PROBLEM_MAPPING)} problem mappings are valid!")
        
        # Show sample data
        print(f"\n📋 Sample Problem Data:")
        sample_problem = "is_equal_to_sum_even_HE_138"
        task_id = get_humaneval_task_id(sample_problem)
        entry_point = get_entry_point(task_id)
        
        print(f"  Problem: {sample_problem}")
        print(f"  Task ID: {task_id}")
        print(f"  Entry Point: {entry_point}")
        
        # Test request generation
        request = extractor.format_request_for_system(task_id, "complete_function")
        print(f"  Request: {request[:100]}...")
        
    else:
        print("❌ Some mappings are invalid!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)