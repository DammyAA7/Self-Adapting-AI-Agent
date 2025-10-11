#!/usr/bin/env python3
"""
Self-Evolution Batch Runner
Automatically generates and tests all 11 self-evolution tasks
"""

import os
import sys
import json
import subprocess
import time
import logging
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class SelfEvolutionBatchRunner:
    """Runner for executing all self-evolution tasks"""

    def __init__(self, framework_path: str = None):
        """Initialize the runner"""
        if framework_path is None:
            framework_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.framework_path = framework_path
        self.log_dir = os.path.join(self.framework_path, "self_evolution_logs")
        os.makedirs(self.log_dir, exist_ok=True)

        # Setup logger
        self.setup_logger()

        # Load task definitions
        self.tasks = self.load_task_definitions()

    def setup_logger(self):
        """Setup batch run logger"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(self.log_dir, f"batch_run_{timestamp}.log")

        self.logger = logging.getLogger('SelfEvolutionBatchRunner')
        self.logger.setLevel(logging.INFO)
        self.logger.handlers = []

        # File handler
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        self.logger.info("="*80)
        self.logger.info("Self-Evolution Batch Runner - Starting Execution")
        self.logger.info(f"Timestamp: {timestamp}")
        self.logger.info("="*80)

    def load_task_definitions(self) -> List[Dict]:
        """Load task definitions from comprehensive evaluation document"""
        # Task definitions with requests from the comprehensive evaluation guide
        tasks = [
            {
                "id": 1,
                "name": "Salary Analyzer",
                "category": "Integration",
                "request": 'Create a function called salary_analyzer that calculates average salary from employee data',
                "analyze_path": "dataset",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 2,
                "name": "Patient Risk Analyzer",
                "category": "Integration",
                "request": 'Create a function called patient_risk_score that analyzes a patient\'s medical history from the Hospital system and calculates their risk score (0-100) based on: age (weight 0.3), number of conditions (weight 0.25), average condition severity (weight 0.25), and abnormal vitals in recent records (weight 0.2). The function should take a Hospital object and patient_id as parameters.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 3,
                "name": "Student GPA Calculator",
                "category": "Integration",
                "request": 'Create a function called calculate_simple_gpa that computes a student\'s simple GPA (not weighted by difficulty) from the University system. Use course credits and enrollment grades to calculate standard GPA. The function should take a University object and student_id as parameters and return the GPA (0.0-4.0 scale).',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 4,
                "name": "Inventory Low Stock Alert",
                "category": "Integration",
                "request": 'Create a function called inventory_low_stock_alert that identifies products below their reorder point from the Warehouse system. Return a list of dictionaries with {sku, name, current_stock, reorder_point, deficit} for each low stock product. The function should take a Warehouse object as parameter.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 5,
                "name": "Matrix Eigenvalue",
                "category": "Composition",
                "request": 'Load the previous session and create a function called advanced_matrix_ops that uses the existing matrix_operations function and computation_cache to perform eigenvalue calculations.',
                "analyze_path": None,
                "requires_context": True,
                "session_1_request": 'Create a function called matrix_operations that performs basic matrix multiplication and stores results in a global variable computation_cache.'
            },
            {
                "id": 6,
                "name": "Portfolio Risk Calculator",
                "category": "Composition",
                "request": 'Load the previous session and create a function called portfolio_risk_assessment that uses the existing calculate_stock_volatility function. The new function should take a dictionary where each key is a stock symbol and value is a dict with \'prices\' (list of floats) and \'allocation\' (float 0-1). Calculate volatility for each stock, weight by allocation, and return overall portfolio risk as weighted average.',
                "analyze_path": None,
                "requires_context": True,
                "session_1_request": 'Create a function called calculate_stock_volatility that takes a list of daily stock prices and calculates the 30-day volatility (standard deviation of daily returns as percentage). Calculate daily returns as (price[i] - price[i-1]) / price[i-1], then return standard deviation times 100.'
            },
            {
                "id": 7,
                "name": "IoT Sensor Pipeline",
                "category": "Composition",
                "request": 'Load the previous session and create a function called aggregate_temperature that uses the existing parse_sensor_reading function. Take a list of raw sensor readings, parse each one, and return the average temperature rounded to 2 decimal places.',
                "analyze_path": None,
                "requires_context": True,
                "session_1_request": 'Create a function called parse_sensor_reading that parses IoT sensor data format \'T:25.5|H:60|TS:1234567890\' where T=temperature, H=humidity, TS=Unix timestamp. Return dictionary with keys: temperature, humidity, timestamp. Handle malformed data by returning None for invalid fields.'
            },
            {
                "id": 8,
                "name": "Movie API",
                "category": "Evolution",
                "request": 'Create a function called movie_api that reads test_context_extended/movie.csv and returns movie data in three different formats based on caller context. Inspect call stack to detect version: if caller ends with \'_v1\' return simple list of titles, if \'_v2\' return dict with titles and metadata, if \'_v3\' return JSON-LD format. Use inspect module.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 9,
                "name": "Book Recommender",
                "category": "Evolution",
                "request": 'Create a function called book_recommender that reads test_context_extended/books.csv and recommends books based on genre parameter. The function must detect API version from environment variable API_VERSION: if \'v1\' return list of titles, if \'v2\' return dict with titles/count/avg_rating/genres, if \'v3\' return JSON-LD format with @context=http://schema.org and @type=BookCollection. Use os.environ.get to check the version.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 10,
                "name": "Performance Tracker",
                "category": "Evolution",
                "request": 'Create a function called performance_report that reads test_context_extended/performance_reviews.csv and generates different reports based on report_type parameter. If report_type=\'summary\' return dict with employee_id/overall_rating/goals_status, if \'detailed\' return all fields including feedback, if \'department\' and employee_id is None return aggregated stats by department (average ratings, count). The function takes employee_id and report_type as parameters.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            },
            {
                "id": 11,
                "name": "Friend Suggester",
                "category": "Evolution",
                "request": 'Create a function called friend_suggestions that reads test_context_extended/social_graph.json and recommends friends with progressive features based on RECOMMENDATION_MODE environment variable. In \'basic\' mode: find users with mutual friends, return top 5 with score = number of mutual friends. In \'enhanced\' mode: add common interests to score (mutual_friends * 2 + common_interests * 1.5). In \'advanced\' mode: add activity similarity (mutual_friends * 2 + interests * 1.5 + activity_match * 1.0). Check os.environ.get(\'RECOMMENDATION_MODE\', \'basic\') to determine mode.',
                "analyze_path": "test_context_extended",
                "requires_context": False,
                "session_1_request": None
            }
        ]
        return tasks

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
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")
            return False

    def find_most_recent_session(self) -> str:
        """Find most recent session file"""
        session_dir = os.path.join(self.framework_path, "context_sessions")
        if not os.path.exists(session_dir):
            return None

        session_files = []
        for filename in os.listdir(session_dir):
            if filename.endswith('.json') and filename.startswith('session_'):
                filepath = os.path.join(session_dir, filename)
                mtime = os.path.getmtime(filepath)
                session_files.append((filepath, mtime))

        if not session_files:
            return None

        session_files.sort(key=lambda x: x[1], reverse=True)
        return session_files[0][0]

    def generate_function(self, task: Dict) -> Dict:
        """Generate function for a task"""
        result = {
            "task_id": task["id"],
            "task_name": task["name"],
            "success": False,
            "iterations": 0,
            "time_taken": 0,
            "error": None
        }

        start_time = time.time()

        try:
            # Build command
            cmd = [sys.executable, "Core/main.py", "--request", task["request"]]

            if task.get("analyze_path"):
                cmd.extend(["--analyze", task["analyze_path"]])

            if task.get("requires_context"):
                session_file = self.find_most_recent_session()
                if session_file:
                    cmd.extend(["--context-memory", "--session", session_file])
                    self.logger.debug(f"Using session: {session_file}")
                else:
                    self.logger.warning("No session file found for context task")

            # Run generation
            self.logger.info(f"Running: {' '.join(cmd)}")
            process_result = subprocess.run(
                cmd,
                cwd=self.framework_path,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )

            output = process_result.stdout
            result["output"] = output

            # Check success
            if "Adjudication Result: True" in output:
                result["success"] = True

            # Extract iteration count
            import re
            iteration_matches = re.findall(r'=== ITERATION (\d+) ===', output)
            if iteration_matches:
                result["iterations"] = max(int(i) for i in iteration_matches)

        except subprocess.TimeoutExpired:
            result["error"] = "Timeout after 10 minutes"
        except Exception as e:
            result["error"] = str(e)

        result["time_taken"] = time.time() - start_time
        return result

    def run_test(self, task_id: int) -> Tuple[bool, str]:
        """Run test for a specific task"""
        try:
            cmd = [sys.executable, "evaluation/self_evolution_test_runner.py", "--id", str(task_id)]
            result = subprocess.run(
                cmd,
                cwd=self.framework_path,
                capture_output=True,
                text=True,
                timeout=60
            )

            success = result.returncode == 0
            output = result.stdout + result.stderr
            return success, output
        except Exception as e:
            return False, str(e)

    def run_task(self, task: Dict) -> Dict:
        """Run a complete task: generate + test"""
        self.logger.info("="*60)
        self.logger.info(f"Task {task['id']}: {task['name']} ({task['category']})")
        self.logger.info("="*60)

        # For composition tasks, need to run session 1 first
        if task.get("requires_context") and task.get("session_1_request"):
            self.logger.info("Step 1: Generating base function (Session 1)")
            session1_task = {
                "id": task["id"],
                "name": f"{task['name']} - Session 1",
                "request": task["session_1_request"],
                "analyze_path": None,
                "requires_context": False
            }
            gen_result_1 = self.generate_function(session1_task)

            if gen_result_1["success"]:
                self.logger.info(f"✅ Session 1 completed in {gen_result_1['iterations']} iterations")
            else:
                self.logger.error(f"❌ Session 1 failed: {gen_result_1.get('error', 'Unknown')}")

            # Clean before session 2
            self.logger.info("Step 2: Cleaning before Session 2")
            self.run_cleanup()

        # Generate main function
        self.logger.info(f"Generating function: {task['name']}")
        gen_result = self.generate_function(task)

        if gen_result["success"]:
            self.logger.info(f"✅ Function generated in {gen_result['iterations']} iterations ({gen_result['time_taken']:.1f}s)")
        else:
            self.logger.error(f"❌ Generation failed: {gen_result.get('error', 'Unknown')}")
            return {
                "task": task,
                "generation": gen_result,
                "test": {"success": False, "output": "Skipped - generation failed"}
            }

        # Run test
        self.logger.info(f"Testing function: {task['name']}")
        test_success, test_output = self.run_test(task["id"])

        if test_success:
            self.logger.info(f"✅ Test PASSED")
        else:
            self.logger.error(f"❌ Test FAILED")

        return {
            "task": task,
            "generation": gen_result,
            "test": {"success": test_success, "output": test_output}
        }

    def run_all_tasks(self) -> Dict:
        """Run all tasks"""
        results = {
            "timestamp": datetime.now().isoformat(),
            "total_tasks": len(self.tasks),
            "successful_generations": 0,
            "successful_tests": 0,
            "task_results": []
        }

        print(f"\n{'='*80}")
        print(f"Self-Evolution Batch Runner - {len(self.tasks)} Tasks")
        print(f"{'='*80}\n")

        for i, task in enumerate(self.tasks, 1):
            print(f"\n[{i}/{len(self.tasks)}] {task['name']}")

            # Clean before each task
            self.logger.info("Cleaning workspace...")
            self.run_cleanup()

            # Run task
            task_result = self.run_task(task)
            results["task_results"].append(task_result)

            # Update counters
            if task_result["generation"]["success"]:
                results["successful_generations"] += 1
            if task_result["test"]["success"]:
                results["successful_tests"] += 1

            # Save intermediate results
            self.save_results(results)

        return results

    def save_results(self, results: Dict) -> str:
        """Save results to JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.log_dir, f"results_{timestamp}.json")

        # Clean output for readability
        clean_results = json.loads(json.dumps(results))
        for task_result in clean_results.get("task_results", []):
            if "generation" in task_result and "output" in task_result["generation"]:
                output = task_result["generation"]["output"]
                task_result["generation"]["output"] = f"[{len(output)} chars]"
            if "test" in task_result and "output" in task_result["test"]:
                output = task_result["test"]["output"]
                task_result["test"]["output"] = f"[{len(output)} chars]"

        with open(filename, 'w') as f:
            json.dump(clean_results, f, indent=2)

        return filename

    def print_summary(self, results: Dict):
        """Print execution summary"""
        self.logger.info("\n" + "="*80)
        self.logger.info("FINAL SUMMARY")
        self.logger.info("="*80)

        print(f"\n{'='*80}")
        print("EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tasks: {results['total_tasks']}")
        print(f"✅ Successful Generations: {results['successful_generations']} ({results['successful_generations']/results['total_tasks']*100:.1f}%)")
        print(f"✅ Successful Tests: {results['successful_tests']} ({results['successful_tests']/results['total_tasks']*100:.1f}%)")

        # Task breakdown
        print(f"\n{'Task':<30} {'Category':<15} {'Gen':<5} {'Test':<5}")
        print("-" * 60)
        for task_result in results['task_results']:
            task = task_result['task']
            gen_status = "✓" if task_result['generation']['success'] else "✗"
            test_status = "✓" if task_result['test']['success'] else "✗"
            print(f"{task['name']:<30} {task['category']:<15} {gen_status:<5} {test_status:<5}")

        # Category breakdown
        categories = {}
        for task_result in results['task_results']:
            cat = task_result['task']['category']
            if cat not in categories:
                categories[cat] = {"total": 0, "gen_success": 0, "test_success": 0}
            categories[cat]["total"] += 1
            if task_result['generation']['success']:
                categories[cat]["gen_success"] += 1
            if task_result['test']['success']:
                categories[cat]["test_success"] += 1

        print(f"\nCategory Breakdown:")
        for cat, stats in categories.items():
            print(f"  {cat}: {stats['gen_success']}/{stats['total']} generations, {stats['test_success']}/{stats['total']} tests")

        print(f"{'='*80}\n")

        self.logger.info(f"Results saved to: {self.log_dir}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run all self-evolution tasks')
    parser.add_argument('--tasks', nargs='+', type=int, help='Specific task IDs to run (1-11)')
    parser.add_argument('--category', type=str, choices=['Integration', 'Composition', 'Evolution'],
                       help='Run only tasks from specific category')

    args = parser.parse_args()

    runner = SelfEvolutionBatchRunner()

    # Filter tasks if requested
    if args.tasks:
        runner.tasks = [t for t in runner.tasks if t['id'] in args.tasks]
    elif args.category:
        runner.tasks = [t for t in runner.tasks if t['category'] == args.category]

    # Run all tasks
    results = runner.run_all_tasks()

    # Print summary
    runner.print_summary(results)


if __name__ == "__main__":
    main()
