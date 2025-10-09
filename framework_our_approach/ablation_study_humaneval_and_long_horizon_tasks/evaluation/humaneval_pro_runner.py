#!/usr/bin/env python3
"""
HumanEval Pro Runner
Automatically runs all HumanEval Pro problems through the SelfEvolve framework
"""

import os
import sys
import json
import subprocess
import time
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import re
import logging

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class HumanEvalProRunner:
    """Runner for executing HumanEval Pro problems through the framework"""

    def __init__(self, dataset_path: str = None, framework_path: str = None):
        """Initialize the runner with paths"""
        if dataset_path is None:
            dataset_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/CodeEval-Pro-main/dataset/humaneval_pro.json"

        if framework_path is None:
            framework_path = "/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent/framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks"

        self.dataset_path = dataset_path
        self.framework_path = framework_path
        self.problems = self._load_dataset()
        self.results = {}
        self.log_dir = os.path.join(self.framework_path, "codeeval_run_logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # Setup main logger
        self.setup_main_logger()

    def setup_main_logger(self):
        """Setup main logger for batch runs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"batch_run_{timestamp}.log")

        # Create logger
        self.logger = logging.getLogger('HumanEvalProRunner')
        self.logger.setLevel(logging.DEBUG)

        # Clear existing handlers
        self.logger.handlers = []

        # File handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler (optional, for important messages)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info("="*80)
        self.logger.info("HumanEval Pro Runner - Batch Execution Log")
        self.logger.info(f"Timestamp: {timestamp}")
        self.logger.info("="*80)

    def _load_dataset(self) -> Dict:
        """Load HumanEval Pro dataset"""
        try:
            with open(self.dataset_path, 'r') as f:
                data = json.load(f)
            return {problem['id']: problem for problem in data}
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return {}

    def formulate_request(self, problem: Dict, is_composed: bool = False) -> Optional[str]:
        """
        Formulate a request string for the problem based on the user's pattern
        Returns None if required function names cannot be extracted
        """
        if is_composed:
            # For composed problems (using the base function)
            test_code = problem.get('test_code', '')
            new_problem = problem.get('new_problem', '')
            raw_problem = problem.get('raw_problem', '')

            # Extract the composed function name from test_code
            # Look for function calls in assertions like: assert function_name(...)
            func_matches = re.findall(r'assert\s+(\w+)\s*\(', test_code)
            if not func_matches:
                return None  # Skip if no composed function name found

            # Get the most common function name (should be the composed function)
            func_name = max(set(func_matches), key=func_matches.count)

            # Extract the base function name from raw_problem
            base_func_match = re.search(r'def\s+(\w+)\s*\(', raw_problem)
            if not base_func_match:
                return None  # Skip if no base function name found

            base_func_name = base_func_match.group(1)

            # Format request similar to user's example
            request = f"Create a function named {func_name} that uses existing {base_func_name} function to follow this instruction: {new_problem}"

        else:
            # For base/raw problems
            raw_problem = problem.get('raw_problem', '')

            # Extract function name from raw_problem
            func_match = re.search(r'def\s+(\w+)\s*\(', raw_problem)
            if not func_match:
                return None  # Skip if no function name found

            func_name = func_match.group(1)

            # Format request similar to user's example
            # The raw_problem already contains the complete function signature and docstring
            request = f"Create a function named {func_name} that {raw_problem}"

        return request

    def save_problem_log(self, problem_id: int, phase: str, result: Dict) -> str:
        """
        Save detailed log file for a single problem execution

        Args:
            problem_id: Problem ID
            phase: 'base' or 'composed'
            result: Result dictionary with execution details

        Returns:
            Path to saved log file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = os.path.join(self.log_dir, f"problem_{problem_id}_{phase}_{timestamp}.log")

        with open(log_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"HumanEval Pro - Problem {problem_id} ({phase.upper()})\n")
            f.write(f"Timestamp: {result.get('timestamp', 'N/A')}\n")
            f.write("="*80 + "\n\n")

            # Result summary
            f.write("RESULT SUMMARY\n")
            f.write("-"*40 + "\n")
            f.write(f"Success: {result.get('success', False)}\n")
            f.write(f"Skipped: {result.get('skipped', False)}\n")
            f.write(f"Iterations: {result.get('iterations', 0)}\n")
            f.write(f"Time Taken: {result.get('time_taken', 0):.2f}s\n")
            if result.get('error'):
                f.write(f"Error: {result['error']}\n")
            if result.get('generated_function'):
                f.write(f"Generated Function: {result['generated_function']}\n")
            f.write("\n")

            # Request sent to framework
            if result.get('request'):
                f.write("REQUEST SENT TO FRAMEWORK\n")
                f.write("-"*40 + "\n")
                f.write(result['request'])
                f.write("\n\n")

            # Full output from framework
            if result.get('output'):
                f.write("FRAMEWORK OUTPUT\n")
                f.write("-"*40 + "\n")
                f.write(result['output'])
                f.write("\n\n")

            # Additional debug info
            f.write("DEBUG INFORMATION\n")
            f.write("-"*40 + "\n")
            f.write(f"Problem ID: {problem_id}\n")
            f.write(f"Phase: {phase}\n")
            f.write(f"Framework Path: {self.framework_path}\n")
            f.write("\n")

            f.write("="*80 + "\n")

        return log_filename

    def run_cleanup(self) -> bool:
        """Run cleanup command"""
        try:
            cmd = [sys.executable, "Core/main.py", "--clean-all"]
            result = subprocess.run(
                cmd,
                cwd=self.framework_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if hasattr(self, 'logger'):
                self.logger.debug(f"Cleanup command executed, return code: {result.returncode}")
            return result.returncode == 0
        except Exception as e:
            if hasattr(self, 'logger'):
                self.logger.error(f"Cleanup failed: {e}")
            print(f"Cleanup failed: {e}")
            return False

    def find_most_recent_session(self) -> Optional[str]:
        """Find the most recent session file in context_sessions directory"""
        session_dir = os.path.join(self.framework_path, "context_sessions")
        if not os.path.exists(session_dir):
            return None

        # Get all session files
        session_files = []
        for filename in os.listdir(session_dir):
            if filename.endswith('.json') and filename.startswith('session_'):
                filepath = os.path.join(session_dir, filename)
                mtime = os.path.getmtime(filepath)
                session_files.append((filepath, mtime))

        if not session_files:
            return None

        # Sort by modification time (most recent first)
        session_files.sort(key=lambda x: x[1], reverse=True)
        return session_files[0][0]

    def run_single_problem(self, problem_id: int, use_context: bool = False) -> Dict:
        """
        Run a single problem through the framework
        """
        problem = self.problems.get(problem_id)
        if not problem:
            return {"success": False, "error": f"Problem {problem_id} not found", "skipped": True}

        result = {
            "problem_id": problem_id,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "iterations": 0,
            "time_taken": 0,
            "error": None,
            "generated_function": None,
            "skipped": False
        }

        start_time = time.time()

        try:
            # Formulate the request
            request = self.formulate_request(problem, is_composed=use_context)

            if request is None:
                # Skip this problem if we can't extract function names
                result["skipped"] = True
                result["error"] = "Could not extract required function names"
                result["time_taken"] = time.time() - start_time
                return result

            # Build command based on context
            if use_context:
                # Find most recent session file to avoid interactive prompt
                session_file = self.find_most_recent_session()
                if session_file:
                    self.logger.debug(f"Using session file: {session_file}")
                    cmd = [sys.executable, "Core/main.py", "--context-memory", "--session", session_file, "--request", request]
                else:
                    self.logger.warning("No session file found, running without context")
                    cmd = [sys.executable, "Core/main.py", "--request", request]
            else:
                cmd = [sys.executable, "Core/main.py", "--request", request]

            # Save request for debugging
            result["request"] = request

            # Run the command
            # Timeout increased to 20 minutes for complex problems
            # Some problems can take 10+ minutes due to multiple iterations
            process_result = subprocess.run(
                cmd,
                cwd=self.framework_path,
                capture_output=True,
                text=True,
                timeout=1200  # 20 minutes timeout
            )

            # Parse output for success indicators
            output = process_result.stdout
            result["output"] = output

            # Check for success patterns
            if "Adjudication Result: True" in output:
                result["success"] = True

            # Extract iteration count
            iteration_matches = re.findall(r'=== ITERATION (\d+) ===', output)
            if iteration_matches:
                result["iterations"] = max(int(i) for i in iteration_matches)

            # Extract generated function if available
            if "Function '.+' added to persistent context" in output:
                func_match = re.search(r"Function '(\w+)' added to persistent context", output)
                if func_match:
                    result["generated_function"] = func_match.group(1)

        except subprocess.TimeoutExpired:
            result["error"] = "Timeout after 20 minutes"
        except Exception as e:
            result["error"] = str(e)

        result["time_taken"] = time.time() - start_time
        return result

    def run_problem_pair(self, problem_id: int) -> Tuple[Dict, Dict]:
        """
        Run both the base problem and composed problem for a HumanEval Pro pair
        """
        self.logger.info("="*60)
        self.logger.info(f"Problem {problem_id}: Starting execution")
        self.logger.info("="*60)

        print(f"\n{'='*60}")
        print(f"Running Problem {problem_id}")
        print(f"{'='*60}")

        # Step 1: Clean everything
        print("🧹 Cleaning workspace...")
        self.logger.info("Step 1: Cleaning workspace")

        cleanup_success = self.run_cleanup()  # Always runs

        if not cleanup_success:
            print("❌ Cleanup failed")
            self.logger.error("Cleanup failed")
        else:
            self.logger.info("Cleanup completed successfully")

        # Step 2: Run base problem (raw_problem)
        print(f"\n📝 Generating base function for Problem {problem_id}...")
        self.logger.info(f"Step 2: Generating base function for Problem {problem_id}")
        base_result = self.run_single_problem(problem_id, use_context=False)

        # Save base problem log
        base_log_file = self.save_problem_log(problem_id, 'base', base_result)
        self.logger.info(f"Base log saved to: {base_log_file}")

        if base_result.get("skipped"):
            print(f"⚠️  Base function skipped: {base_result.get('error', 'Could not extract function name')}")
            self.logger.warning(f"Base function skipped: {base_result.get('error')}")
        elif base_result["success"]:
            print(f"✅ Base function generated in {base_result['iterations']} iterations ({base_result['time_taken']:.1f}s)")
            self.logger.info(f"Base function generated successfully in {base_result['iterations']} iterations")
        else:
            print(f"❌ Base function generation failed: {base_result.get('error', 'Unknown error')}")
            self.logger.error(f"Base function generation failed: {base_result.get('error')}")

        # Step 3: Clean workspace again before composed function
        # This ensures --context-memory starts clean and properly restores from session
        if not base_result.get("skipped"):
            print(f"\n🧹 Cleaning workspace before composed function...")
            self.logger.info("Step 3: Cleaning workspace before composed function")

            cleanup_success = self.run_cleanup()  # Always runs

            if not cleanup_success:
                print("❌ Cleanup failed")
                self.logger.error("Cleanup before composed failed")
            else:
                self.logger.info("Cleanup before composed completed successfully")

            # Step 4: Run composed problem (new_problem) with context
            print(f"\n📝 Generating composed function for Problem {problem_id}...")
            self.logger.info(f"Step 4: Generating composed function for Problem {problem_id}")
            composed_result = self.run_single_problem(problem_id, use_context=True)

            # Save composed problem log
            composed_log_file = self.save_problem_log(problem_id, 'composed', composed_result)
            self.logger.info(f"Composed log saved to: {composed_log_file}")

            if composed_result.get("skipped"):
                print(f"⚠️  Composed function skipped: {composed_result.get('error', 'Could not extract function name')}")
                self.logger.warning(f"Composed function skipped: {composed_result.get('error')}")
            elif composed_result["success"]:
                print(f"✅ Composed function generated in {composed_result['iterations']} iterations ({composed_result['time_taken']:.1f}s)")
                self.logger.info(f"Composed function generated successfully in {composed_result['iterations']} iterations")
            else:
                print(f"❌ Composed function generation failed: {composed_result.get('error', 'Unknown error')}")
                self.logger.error(f"Composed function generation failed: {composed_result.get('error')}")
        else:
            # Skip composed if base was skipped
            composed_result = {
                "problem_id": problem_id,
                "skipped": True,
                "error": "Skipped because base function was skipped",
                "success": False
            }
            self.logger.info("Steps 3-4: Skipped composed function (base was skipped)")

        self.logger.info(f"Problem {problem_id}: Execution completed")
        return base_result, composed_result

    def evaluate_problem(self, problem_id: int) -> Dict:
        """
        Run the evaluator on a problem
        """
        try:
            from codeeval_pro_evaluator import CodeEvalProEvaluator
            evaluator = CodeEvalProEvaluator(self.dataset_path)
            success, results = evaluator.run_tests(problem_id, verbose=False)
            return results
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_batch(self, problem_ids: List[int], evaluate: bool = True) -> Dict:
        """
        Run a batch of problems
        """
        batch_results = {
            "timestamp": datetime.now().isoformat(),
            "total_problems": len(problem_ids),
            "successful_base": 0,
            "successful_composed": 0,
            "evaluated_success": 0,
            "skipped_base": 0,
            "skipped_composed": 0,
            "skipped_problems": [],
            "results": []
        }

        print(f"\n{'='*80}")
        print(f"HumanEval Pro Batch Runner - {len(problem_ids)} problems")
        print(f"{'='*80}")

        for i, problem_id in enumerate(problem_ids, 1):
            print(f"\n[{i}/{len(problem_ids)}] Problem {problem_id}")

            # Run both base and composed
            base_result, composed_result = self.run_problem_pair(problem_id)

            # Step 5: Evaluate if requested
            eval_result = None
            if evaluate:
                print(f"\n🔍 Evaluating Problem {problem_id}...")
                self.logger.info(f"Step 5: Evaluating Problem {problem_id}")
                eval_result = self.evaluate_problem(problem_id)
                if eval_result.get("success"):
                    print(f"✅ Evaluation passed!")
                    self.logger.info(f"Problem {problem_id} evaluation: PASSED")
                    batch_results["evaluated_success"] += 1
                else:
                    print(f"❌ Evaluation failed")
                    self.logger.warning(f"Problem {problem_id} evaluation: FAILED")

            # Store results
            problem_results = {
                "problem_id": problem_id,
                "base": base_result,
                "composed": composed_result,
                "evaluation": eval_result
            }
            batch_results["results"].append(problem_results)

            # Update counters
            if base_result.get("skipped"):
                batch_results["skipped_base"] += 1
                if problem_id not in batch_results["skipped_problems"]:
                    batch_results["skipped_problems"].append(problem_id)
            elif base_result["success"]:
                batch_results["successful_base"] += 1

            if composed_result.get("skipped"):
                batch_results["skipped_composed"] += 1
            elif composed_result["success"]:
                batch_results["successful_composed"] += 1

            # Save intermediate results
            self.save_results(batch_results)

        return batch_results

    def save_results(self, results: Dict, filename: str = None) -> str:
        """
        Save results to JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.log_dir, f"run_results_{timestamp}.json")

        # Remove large output fields for cleaner logs
        clean_results = json.loads(json.dumps(results))  # Deep copy
        for result in clean_results.get("results", []):
            if "base" in result and "output" in result["base"]:
                result["base"]["output"] = f"[Output truncated - {len(result['base']['output'])} chars]"
            if "composed" in result and "output" in result["composed"]:
                result["composed"]["output"] = f"[Output truncated - {len(result['composed']['output'])} chars]"

        with open(filename, 'w') as f:
            json.dump(clean_results, f, indent=2)

        return filename

    def print_summary(self, results: Dict):
        """
        Print a summary of results
        """
        self.logger.info("\n" + "="*80)
        self.logger.info("FINAL SUMMARY")
        self.logger.info("="*80)

        print(f"\n{'='*80}")
        print("EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"Total Problems: {results['total_problems']}")
        print(f"✅ Successful Base Functions: {results['successful_base']} ({results['successful_base']/results['total_problems']*100:.1f}%)")
        print(f"✅ Successful Composed Functions: {results['successful_composed']} ({results['successful_composed']/results['total_problems']*100:.1f}%)")

        if results.get('skipped_base', 0) > 0 or results.get('skipped_composed', 0) > 0:
            print(f"⚠️  Skipped Base Functions: {results.get('skipped_base', 0)} ({results.get('skipped_base', 0)/results['total_problems']*100:.1f}%)")
            print(f"⚠️  Skipped Composed Functions: {results.get('skipped_composed', 0)} ({results.get('skipped_composed', 0)/results['total_problems']*100:.1f}%)")

        if results.get('evaluated_success') is not None:
            print(f"✅ Evaluation Passed: {results['evaluated_success']} ({results['evaluated_success']/results['total_problems']*100:.1f}%)")

        # Problem-specific summary
        print(f"\n{'Problem':<10} {'Base':<10} {'Composed':<10} {'Evaluated':<10}")
        print("-" * 40)
        for result in results['results']:
            problem_id = result['problem_id']

            # Base status
            if result['base'].get('skipped'):
                base_status = "⚠"
            elif result['base']['success']:
                base_status = "✓"
            else:
                base_status = "✗"

            # Composed status
            if result['composed'].get('skipped'):
                composed_status = "⚠"
            elif result['composed']['success']:
                composed_status = "✓"
            else:
                composed_status = "✗"

            # Evaluation status
            eval_status = "✓" if result.get('evaluation', {}).get('success') else "✗" if result.get('evaluation') else "-"

            print(f"{problem_id:<10} {base_status:<10} {composed_status:<10} {eval_status:<10}")

        # List skipped problems
        if results.get('skipped_problems'):
            print(f"\n⚠️  Skipped Problems (could not extract function names):")
            print(f"   {', '.join(map(str, results['skipped_problems']))}")
            self.logger.warning(f"Skipped Problems: {', '.join(map(str, results['skipped_problems']))}")

        # Log summary statistics
        self.logger.info(f"Total Problems: {results['total_problems']}")
        self.logger.info(f"Successful Base: {results['successful_base']} ({results['successful_base']/results['total_problems']*100:.1f}%)")
        self.logger.info(f"Successful Composed: {results['successful_composed']} ({results['successful_composed']/results['total_problems']*100:.1f}%)")

        results_file = self.save_results(results)
        print(f"\n📁 JSON Results saved to: {results_file}")
        print(f"📁 Batch Log saved to: {self.logger.handlers[0].baseFilename if self.logger.handlers else 'N/A'}")
        print(f"📁 Individual problem logs saved to: {self.log_dir}/problem_*_*.log")

        self.logger.info(f"Results saved to: {results_file}")
        self.logger.info("="*80)
        self.logger.info("Batch execution completed")
        self.logger.info("="*80)

        print(f"{'='*80}")


def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(description='Run HumanEval Pro problems through SelfEvolve framework')
    parser.add_argument('problems', nargs='*', type=int,
                       help='Problem IDs to run (leave empty for all)')
    parser.add_argument('--dataset', type=str, default=None,
                       help='Path to HumanEval Pro dataset')
    parser.add_argument('--framework', type=str, default=None,
                       help='Path to framework directory')
    parser.add_argument('--no-eval', action='store_true',
                       help='Skip evaluation after generation')
    parser.add_argument('--limit', type=int, default=None,
                       help='Limit number of problems to run')
    parser.add_argument('--start', type=int, default=0,
                       help='Start from problem ID')

    args = parser.parse_args()

    # Create runner
    runner = HumanEvalProRunner(
        dataset_path=args.dataset,
        framework_path=args.framework
    )

    # Determine which problems to run
    if args.problems:
        problem_ids = args.problems
    else:
        # Get all problem IDs
        problem_ids = sorted(list(runner.problems.keys()))

        # Apply start and limit
        if args.start:
            problem_ids = [p for p in problem_ids if p >= args.start]
        if args.limit:
            problem_ids = problem_ids[:args.limit]

    if not problem_ids:
        print("No problems to run")
        return

    print(f"Will run {len(problem_ids)} problems: {problem_ids}")

    # Run batch
    results = runner.run_batch(problem_ids, evaluate=not args.no_eval)

    # Print summary
    runner.print_summary(results)


if __name__ == "__main__":
    main()