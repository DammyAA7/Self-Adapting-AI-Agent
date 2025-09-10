#!/usr/bin/env python3
"""
HumanEval Dataset Extractor
Loads problems directly from HumanEval.jsonl for authentic evaluation
"""
import json
import os
import re
from typing import Dict, Optional


class HumanEvalExtractor:
    """Extract and process problems from HumanEval.jsonl dataset"""
    
    def __init__(self, jsonl_path: str = None):
        """Initialize with path to HumanEval.jsonl file"""
        if jsonl_path is None:
            # Default path to TiCoder's HumanEval dataset
            jsonl_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/TiCoder-main/datasets/human-eval/HumanEval.jsonl"
        
        self.jsonl_path = jsonl_path
        self.problems = {}
        
        if os.path.exists(jsonl_path):
            self.problems = self.load_all_problems()
            print(f"✅ Loaded {len(self.problems)} HumanEval problems from {jsonl_path}")
        else:
            print(f"❌ HumanEval dataset not found at: {jsonl_path}")
    
    def load_all_problems(self) -> Dict:
        """Load all HumanEval problems from JSONL file"""
        problems = {}
        
        try:
            with open(self.jsonl_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            task_id = data.get('task_id')
                            if task_id:
                                problems[task_id] = data
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Warning: Invalid JSON on line {line_num}: {e}")
                            continue
        except Exception as e:
            print(f"❌ Error reading HumanEval dataset: {e}")
            
        return problems
    
    def get_problem(self, task_id: str) -> Optional[Dict]:
        """Get complete problem data for a task ID"""
        return self.problems.get(task_id)
    
    def get_problem_prompt(self, task_id: str) -> Optional[str]:
        """Get the exact prompt for a problem"""
        problem = self.problems.get(task_id)
        return problem.get('prompt') if problem else None
    
    def get_entry_point(self, task_id: str) -> Optional[str]:
        """Get the function name to implement"""
        problem = self.problems.get(task_id)
        return problem.get('entry_point') if problem else None
    
    def get_test_cases(self, task_id: str) -> Optional[str]:
        """Get the test cases for a problem"""
        problem = self.problems.get(task_id)
        return problem.get('test') if problem else None
    
    def get_canonical_solution(self, task_id: str) -> Optional[str]:
        """Get the canonical solution (reference implementation)"""
        problem = self.problems.get(task_id)
        return problem.get('canonical_solution') if problem else None
    
    def extract_docstring(self, prompt: str) -> str:
        """Extract docstring description from the prompt"""
        # Look for docstring between triple quotes
        docstring_match = re.search(r'"""(.*?)"""', prompt, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            # Clean up the docstring - remove extra whitespace and newlines
            lines = [line.strip() for line in docstring.split('\n') if line.strip()]
            return ' '.join(lines)
        
        # Fallback: try to extract from comments
        lines = prompt.split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                return line.strip().lstrip('#').strip()
        
        return "Implement the function as specified"
    
    def format_request_for_system(self, task_id: str, format_type: str = "complete_function") -> Optional[str]:
        """
        Convert HumanEval prompt to your system's request format
        
        Args:
            task_id: HumanEval task ID (e.g., "HumanEval/138")
            format_type: How to format the request
                - "complete_function": Give exact prompt to complete
                - "create_function": Extract description and ask to create
                - "exact_prompt": Use the exact prompt as-is
        """
        problem = self.problems.get(task_id)
        if not problem:
            return None
        
        prompt = problem['prompt']
        entry_point = problem['entry_point']
        
        if format_type == "exact_prompt":
            # Return the exact prompt as provided by HumanEval
            return prompt
        
        elif format_type == "complete_function":
            # Ask system to complete the function (most authentic)
            return f"Complete this Python function:\n\n{prompt}"
        
        elif format_type == "create_function":
            # Extract description and ask to create function (your system's style)
            description = self.extract_docstring(prompt)
            return f"Create a function named {entry_point} that {description.lower()}"
        
        else:
            # Default to complete_function
            return f"Complete this Python function:\n\n{prompt}"
    
    def get_all_task_ids(self) -> list:
        """Get all available task IDs"""
        return list(self.problems.keys())
    
    def get_problem_count(self) -> int:
        """Get total number of problems loaded"""
        return len(self.problems)
    
    def validate_task_id(self, task_id: str) -> bool:
        """Check if a task ID exists in the dataset"""
        return task_id in self.problems
    
    def get_problem_info(self, task_id: str) -> Dict:
        """Get summary information about a problem"""
        problem = self.problems.get(task_id)
        if not problem:
            return {}
        
        return {
            'task_id': task_id,
            'entry_point': problem.get('entry_point'),
            'description': self.extract_docstring(problem.get('prompt', '')),
            'has_tests': bool(problem.get('test')),
            'has_solution': bool(problem.get('canonical_solution'))
        }


def main():
    """Test the HumanEval extractor"""
    print("🔍 Testing HumanEval Extractor...")
    
    # Initialize extractor
    extractor = HumanEvalExtractor()
    
    if not extractor.problems:
        print("❌ No problems loaded. Exiting.")
        return 1
    
    # Test with a known problem
    test_task_id = "HumanEval/138"
    
    print(f"\n📋 Testing with {test_task_id}:")
    
    # Get problem info
    info = extractor.get_problem_info(test_task_id)
    print(f"  Entry point: {info.get('entry_point')}")
    print(f"  Description: {info.get('description')}")
    
    # Test different request formats
    print(f"\n🔧 Request Formats:")
    
    complete_format = extractor.format_request_for_system(test_task_id, "complete_function")
    print(f"Complete function format:\n{complete_format[:100]}...")
    
    create_format = extractor.format_request_for_system(test_task_id, "create_function")
    print(f"Create function format: {create_format}")
    
    # Test test cases
    test_cases = extractor.get_test_cases(test_task_id)
    if test_cases:
        print(f"\n🧪 Test cases available: {len(test_cases)} characters")
    
    print(f"\n✅ HumanEval Extractor working correctly!")
    print(f"📊 Total problems available: {extractor.get_problem_count()}")
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)