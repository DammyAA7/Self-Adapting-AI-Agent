"""
Dual Pass@k Evaluator for Self-Adapting AI Agent Prototype IV
Implements both standard Pass@k (multiple runs) and iteration efficiency (within runs)
"""
import subprocess
import json
import os
import sys
import time
import hashlib
import re
import math
from typing import Dict, List, Tuple, Optional
from datetime import datetime

# HumanEval integration imports
try:
    from humaneval_extractor import HumanEvalExtractor
    from humaneval_validator import HumanEvalValidator
    from humaneval_problem_mapping import TARGET_PROBLEM_MAPPING, get_humaneval_task_id, get_entry_point
    HUMANEVAL_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ HumanEval modules not available: {e}")
    HUMANEVAL_AVAILABLE = False

class DualPassKEvaluator:
    def __init__(self, verbose=False, timeout=1200, use_humaneval=False):
        self.verbose = verbose
        self.timeout = timeout  # 20 minutes default
        self.use_humaneval = use_humaneval and HUMANEVAL_AVAILABLE
        
        # Initialize HumanEval components if requested
        self.humaneval_extractor = None
        self.humaneval_validator = None
        
        if self.use_humaneval:
            try:
                self.humaneval_extractor = HumanEvalExtractor()
                self.humaneval_validator = HumanEvalValidator()
                print(f"✅ HumanEval evaluation enabled - authentic comparison mode")
            except Exception as e:
                print(f"❌ Failed to initialize HumanEval: {e}")
                self.use_humaneval = False
        
        self.results = {
            'problems': {},
            'standard_pass_k': {},
            'iteration_efficiency': {},
            'timestamp': datetime.now().isoformat(),
            'total_api_calls': 0,
            'humaneval_mode': self.use_humaneval
        }
        
        # Get paths
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.main_script = os.path.join(self.project_root, "Core", "main.py")
        
    def evaluate_problem_dual_metrics(self, problem_name: str, problem_request: str, num_runs: int = 10):
        """
        Evaluate a single problem with both Pass@k approaches
        """
        problem_id = hashlib.md5(problem_request.encode()).hexdigest()[:8]
        # Override with HumanEval prompt if enabled
        original_request = problem_request
        humaneval_task_id = None
        humaneval_entry_point = None
        
        if self.use_humaneval and problem_name in TARGET_PROBLEM_MAPPING:
            humaneval_task_id = get_humaneval_task_id(problem_name)
            humaneval_entry_point = get_entry_point(humaneval_task_id)
            
            # Get authentic HumanEval prompt
            authentic_prompt = self.humaneval_extractor.format_request_for_system(
                humaneval_task_id, "exact_prompt"
            )
            
            if authentic_prompt:
                problem_request = authentic_prompt
                if self.verbose:
                    print(f"📋 Using authentic HumanEval prompt for {humaneval_task_id}")
        
        print(f"\\n{'='*60}")
        print(f"📊 Evaluating: {problem_name}")
        if self.use_humaneval and humaneval_task_id:
            print(f"🎯 HumanEval Task: {humaneval_task_id} ({humaneval_entry_point})")
        print(f"📝 Request: {problem_request[:80]}...")
        print(f"🔄 Running {num_runs} independent attempts")
        print(f"{'='*60}")
        
        runs_data = []
        
        for run_num in range(num_runs):
            print(f"\\n🎲 Run {run_num + 1}/{num_runs}:")
            
            # Run complete system
            tdd_success, iterations_used, log_data = self.run_system_once(problem_request)
            
            # Initialize run data
            run_data = {
                'run': run_num + 1,
                'success': tdd_success,  # Keep original field for compatibility
                'tdd_success': tdd_success,
                'iterations': iterations_used,
                'log_snippet': log_data[-500:] if log_data else "",
                'humaneval_pass': None,
                'final_success': tdd_success  # Default to TDD result
            }
            
            # HumanEval validation if enabled and TDD succeeded
            if self.use_humaneval and tdd_success and humaneval_entry_point:
                print(f"  🧪 Validating with HumanEval tests...", end='', flush=True)
                
                # Get test cases
                test_code = self.humaneval_extractor.get_test_cases(humaneval_task_id)
                
                if test_code:
                    # Validate function against HumanEval tests
                    humaneval_success, error_msg = self.humaneval_validator.validate_function(
                        humaneval_entry_point, test_code, verbose=True
                    )
                    
                    run_data['humaneval_pass'] = humaneval_success
                    run_data['final_success'] = humaneval_success  # Override with HumanEval result
                    
                    if humaneval_success:
                        print(f" ✅")
                    else:
                        print(f" ❌ ({error_msg[:50]}...)")
                else:
                    print(f" ⚠️ No tests")
            
            runs_data.append(run_data)
            
            # Display final result
            if self.use_humaneval and humaneval_entry_point:
                tdd_status = "✅" if run_data['tdd_success'] else "❌"
                he_status = "✅" if run_data['humaneval_pass'] else ("❌" if run_data['humaneval_pass'] is False else "⚠️")
                final_status = "✅" if run_data['final_success'] else "❌"
                print(f"  TDD {tdd_status} | HumanEval {he_status} | Final {final_status} (iter {iterations_used})")
            else:
                if run_data['final_success']:
                    print(f"  ✅ Success at iteration {iterations_used}")
                else:
                    print(f"  ❌ Failed after {iterations_used} iterations")
            
            # Small delay to avoid overwhelming the system
            time.sleep(1)
        
        # Calculate both metrics
        standard_metrics = self.calculate_standard_pass_k(runs_data)
        efficiency_metrics = self.calculate_iteration_efficiency(runs_data)
        
        # Store results
        self.results['problems'][problem_name] = {
            'id': problem_id,
            'request': problem_request,
            'runs': runs_data,
            'standard_pass_k': standard_metrics,
            'iteration_efficiency': efficiency_metrics
        }
        
        # Display results for this problem
        self.display_problem_results(problem_name, standard_metrics, efficiency_metrics)
        
        return standard_metrics, efficiency_metrics
    
    def run_system_once(self, problem_request: str) -> Tuple[bool, int, str]:
        """
        Run your complete system once and extract results
        Returns: (success, iterations_used, log_output)
        """
        cmd = [
            sys.executable, self.main_script,
            '--clean-all',
            '--request', problem_request
        ]
        
        # Add debug flag in verbose mode
        if self.verbose:
            cmd.append('--debug')
        
        print(f"  🚀 Running system (timeout: {self.timeout//60}min)...", end='', flush=True)
        
        try:
            # Enhanced timeout handling with partial output capture
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.project_root
            )
            
            try:
                stdout, stderr = process.communicate(timeout=self.timeout)
                returncode = process.returncode
                
                # Count as API call
                self.results['total_api_calls'] += 1
                
                # Parse success/failure
                success = self.parse_success(stdout, stderr)
                iterations = self.parse_iterations(stdout)
                
                print(f" Done ({returncode})")
                
                # Show output in verbose mode
                if self.verbose:
                    print(f"\\n{'='*50} SYSTEM OUTPUT {'='*50}")
                    if stdout:
                        print("STDOUT:")
                        print(stdout)
                    if stderr:
                        print("\\nSTDERR:")
                        print(stderr)
                    print(f"{'='*110}")
                
                return success, iterations, stdout
                
            except subprocess.TimeoutExpired:
                print(f" TIMEOUT after {self.timeout//60} minutes")
                
                # Kill process and get partial output
                process.kill()
                stdout, stderr = process.communicate()
                
                # Show partial output for debugging
                if stdout:
                    print(f"\\n⚠️ PARTIAL STDOUT (last 1000 chars):\\n{stdout[-1000:]}")
                if stderr:
                    print(f"\\n⚠️ STDERR:\\n{stderr}")
                    
                return False, 6, f"Timeout after {self.timeout}s. Partial output: {stdout[-500:] if stdout else 'No output'}"
                
        except Exception as e:
            print(f" Error: {e}")
            return False, 0, str(e)
    
    def parse_success(self, stdout: str, stderr: str) -> bool:
        """Parse output to determine if function generation succeeded"""
        success_indicators = [
            "FUNCTION GENERATION SUCCESSFUL",
            "Adjudication Result: True", 
            "Function was just generated",
            "Added 'unknown_function' to safe functions",
            "Added '",
            "' to safe functions"
        ]
        
        for indicator in success_indicators:
            if indicator in stdout:
                return True
        
        return False
    
    def parse_iterations(self, stdout: str) -> int:
        """Parse how many iterations were used"""
        # Look for iteration patterns
        iteration_matches = re.findall(r'=== ITERATION (\\d+) ===', stdout)
        if iteration_matches:
            return int(iteration_matches[-1])
        
        # Look for max iterations reached
        if "Maximum iterations" in stdout:
            max_match = re.search(r'Maximum iterations \\((\\d+)\\)', stdout)
            if max_match:
                return int(max_match.group(1))
            return 6  # Default max
        
        # If successful but no iteration count, assume 1
        if self.parse_success(stdout, ""):
            return 1
            
        return 0
    
    def pass_at_k(self, n: int, c: int, k: int) -> float:
        """
        Calculate exact Pass@k using research-standard unbiased estimator
        
        Args:
            n: total samples generated
            c: number of correct samples
            k: k in Pass@k
            
        Returns:
            Probability that at least one of k samples is correct
        """
        if n - c < k:
            return 1.0
        return 1.0 - (math.comb(n - c, k) / math.comb(n, k))
    
    def calculate_standard_pass_k(self, runs_data: List[Dict]) -> Dict:
        """
        Calculate standard Pass@k from multiple independent runs using both methods:
        - Exact: Research-standard unbiased estimator (primary)
        - Empirical: Direct observation (for comparison)
        """
        total_runs = len(runs_data)
        if total_runs == 0:
            return {}
        
        # Count successful runs (use final_success for HumanEval compatibility)
        successful_runs = [r for r in runs_data if r.get('final_success', r['success'])]
        success_count = len(successful_runs)
        
        # Also count TDD success for comparison
        tdd_successful_runs = [r for r in runs_data if r['success']]
        tdd_success_count = len(tdd_successful_runs)
        
        # Find first success position (using final_success)
        first_success_run = None
        for i, run in enumerate(runs_data):
            if run.get('final_success', run['success']):
                first_success_run = i + 1
                break
        
        # Calculate exact Pass@k using research-standard formula (only for valid k values)
        n, c = total_runs, success_count
        exact_pass_1 = self.pass_at_k(n, c, 1) if n >= 1 else None
        exact_pass_5 = self.pass_at_k(n, c, 5) if n >= 5 else None
        exact_pass_10 = self.pass_at_k(n, c, 10) if n >= 10 else None
        
        # Calculate empirical Pass@k (only for valid k values)
        empirical_pass_1 = (1 if runs_data[0].get('final_success', runs_data[0]['success']) else 0) if n >= 1 else None
        empirical_pass_5 = (1 if any(r.get('final_success', r['success']) for r in runs_data[:5]) else 0) if n >= 5 else None
        empirical_pass_10 = (1 if any(r.get('final_success', r['success']) for r in runs_data[:10]) else 0) if n >= 10 else None
        
        results = {
            # Primary metrics (research-standard exact)
            'pass@1': exact_pass_1,
            'pass@5': exact_pass_5,
            'pass@10': exact_pass_10,
            # Secondary metrics (empirical for comparison)
            'pass@1_empirical': empirical_pass_1,
            'pass@5_empirical': empirical_pass_5,
            'pass@10_empirical': empirical_pass_10,
            # Breakdown metrics for analysis
            'tdd_success_count': tdd_success_count,
            'final_success_count': success_count,
            # Additional metadata
            'success_rate': (success_count / total_runs) * 100,
            'first_success_at_run': first_success_run,
            'total_successful': success_count,
            'total_runs': total_runs
        }
        
        return results
    
    def calculate_iteration_efficiency(self, runs_data: List[Dict]) -> Dict:
        """
        Calculate iteration efficiency metrics from successful runs
        """
        successful_runs = [r for r in runs_data if r.get('final_success', r['success'])]
        
        if not successful_runs:
            return {
                'avg_iterations': 0,
                'success_within_1': 0,
                'success_within_3': 0,  
                'success_within_6': 0,
                'iteration_distribution': {}
            }
        
        iterations_list = [r['iterations'] for r in successful_runs]
        total_successful = len(successful_runs)
        
        # Calculate distribution
        distribution = {}
        for i in range(1, 7):
            count = sum(1 for it in iterations_list if it == i)
            distribution[f'iteration_{i}'] = count
        
        # Calculate percentages within successful runs
        within_1 = sum(1 for it in iterations_list if it <= 1) / total_successful * 100
        within_3 = sum(1 for it in iterations_list if it <= 3) / total_successful * 100
        within_6 = sum(1 for it in iterations_list if it <= 6) / total_successful * 100
        
        return {
            'avg_iterations': sum(iterations_list) / total_successful,
            'min_iterations': min(iterations_list),
            'max_iterations': max(iterations_list),
            'success_within_1': within_1,
            'success_within_3': within_3,
            'success_within_6': within_6,
            'iteration_distribution': distribution,
            'total_successful_runs': total_successful
        }
    
    def display_problem_results(self, problem_name: str, standard: Dict, efficiency: Dict):
        """Display results for a single problem"""
        print(f"\\n{'='*60}")
        print(f"📈 Results for: {problem_name}")
        print(f"{'='*60}")
        
        # Show dual validation results if HumanEval enabled
        if hasattr(self, 'use_humaneval') and self.use_humaneval:
            tdd_count = standard.get('tdd_success_count', 0)
            final_count = standard.get('final_success_count', 0)
            total = standard.get('total_runs', 1)
            
            print(f"\\n🔍 Validation Results:")
            print(f"  TDD Generation: {tdd_count}/{total} ({tdd_count/total*100:.1f}%)")
            print(f"  Final Success: {final_count}/{total} ({final_count/total*100:.1f}%)")
        
        if standard:
            print("\\n🎯 Research-Standard Pass@k (Exact Formula):")
            if standard.get('pass@1') is not None:
                print(f"  Pass@1:  {standard.get('pass@1')*100:.1f}%")
            if standard.get('pass@5') is not None:
                print(f"  Pass@5:  {standard.get('pass@5')*100:.1f}%")
            else:
                print(f"  Pass@5:  N/A (need ≥5 runs, have {standard.get('total_runs', 0)})")
            if standard.get('pass@10') is not None:
                print(f"  Pass@10: {standard.get('pass@10')*100:.1f}%")
            else:
                print(f"  Pass@10: N/A (need ≥10 runs, have {standard.get('total_runs', 0)})")
            print(f"  Success rate: {standard.get('success_rate', 0):.1f}%")
            
            # Show empirical comparison
            print("\\n📊 Empirical Pass@k (Direct Observation):")
            if standard.get('pass@1_empirical') is not None:
                print(f"  Pass@1:  {standard.get('pass@1_empirical')*100:.0f}%")
            if standard.get('pass@5_empirical') is not None:
                print(f"  Pass@5:  {standard.get('pass@5_empirical')*100:.0f}%")
            else:
                print(f"  Pass@5:  N/A (need ≥5 runs)")
            if standard.get('pass@10_empirical') is not None:
                print(f"  Pass@10: {standard.get('pass@10_empirical')*100:.0f}%")
            else:
                print(f"  Pass@10: N/A (need ≥10 runs)")
            
            if standard.get('first_success_at_run'):
                print(f"  First success: Run {standard['first_success_at_run']}")
        
        if efficiency and efficiency.get('total_successful_runs', 0) > 0:
            print("\\n⚡ TDD Iteration Efficiency (Within Successful Runs):")
            print(f"  Average iterations: {efficiency['avg_iterations']:.2f}")
            print(f"  Success on 1st iteration: {efficiency['success_within_1']:.1f}%")
            print(f"  Success within 3 iterations: {efficiency['success_within_3']:.1f}%")
            print(f"  Success within 6 iterations: {efficiency['success_within_6']:.1f}%")
    
    def run_benchmark_suite(self, problems: Dict[str, str], runs_per_problem: int = 10):
        """
        Run complete benchmark suite with both metrics
        """
        print(f"\\n{'='*70}")
        print("🚀 DUAL PASS@K EVALUATION SUITE")
        print(f"{'='*70}")
        print(f"📋 Problems: {len(problems)}")
        print(f"🔄 Runs per problem: {runs_per_problem}")
        print(f"📊 Metrics: Standard Pass@k + TDD Efficiency")
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        start_time = time.time()
        
        for i, (problem_name, problem_request) in enumerate(problems.items(), 1):
            print(f"\\n[{i}/{len(problems)}] Processing {problem_name}...")
            self.evaluate_problem_dual_metrics(problem_name, problem_request, runs_per_problem)
            self.save_intermediate_results()
        
        # Display final summary
        total_time = time.time() - start_time
        self.display_final_summary(total_time)
        self.save_final_results()
        
        return self.results
    
    def display_final_summary(self, total_time: float):
        """Display comprehensive summary with both metrics"""
        print(f"\\n{'='*70}")
        print("📊 FINAL DUAL PASS@K EVALUATION SUMMARY")
        print(f"{'='*70}")
        
        if not self.results['problems']:
            print("❌ No problems evaluated")
            return
        
        # Aggregate standard Pass@k across all problems
        all_problems = list(self.results['problems'].values())
        
        # Exact Pass@k averages (research-standard) - filter out None values
        exact_pass_1_scores = [p['standard_pass_k']['pass@1'] for p in all_problems 
                              if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@1') is not None]
        exact_pass_5_scores = [p['standard_pass_k']['pass@5'] for p in all_problems 
                              if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@5') is not None]
        exact_pass_10_scores = [p['standard_pass_k']['pass@10'] for p in all_problems 
                               if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@10') is not None]
        
        avg_exact_pass_1 = sum(exact_pass_1_scores) / len(exact_pass_1_scores) * 100 if exact_pass_1_scores else None
        avg_exact_pass_5 = sum(exact_pass_5_scores) / len(exact_pass_5_scores) * 100 if exact_pass_5_scores else None
        avg_exact_pass_10 = sum(exact_pass_10_scores) / len(exact_pass_10_scores) * 100 if exact_pass_10_scores else None
        
        # Empirical Pass@k averages (for comparison) - filter out None values
        empirical_pass_1_scores = [p['standard_pass_k']['pass@1_empirical'] for p in all_problems 
                                  if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@1_empirical') is not None]
        empirical_pass_5_scores = [p['standard_pass_k']['pass@5_empirical'] for p in all_problems 
                                  if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@5_empirical') is not None]
        empirical_pass_10_scores = [p['standard_pass_k']['pass@10_empirical'] for p in all_problems 
                                   if 'standard_pass_k' in p and p['standard_pass_k'].get('pass@10_empirical') is not None]
        
        avg_empirical_pass_1 = sum(empirical_pass_1_scores) / len(empirical_pass_1_scores) * 100 if empirical_pass_1_scores else None
        avg_empirical_pass_5 = sum(empirical_pass_5_scores) / len(empirical_pass_5_scores) * 100 if empirical_pass_5_scores else None
        avg_empirical_pass_10 = sum(empirical_pass_10_scores) / len(empirical_pass_10_scores) * 100 if empirical_pass_10_scores else None
        
        print("\\n🎯 RESEARCH-STANDARD PASS@K (Exact Formula - Primary Results):")
        if avg_exact_pass_1 is not None:
            print(f"  Pass@1:  {avg_exact_pass_1:.1f}% (unbiased probability estimator)")
        if avg_exact_pass_5 is not None:
            print(f"  Pass@5:  {avg_exact_pass_5:.1f}% (research-comparable)")
        else:
            print(f"  Pass@5:  N/A (need ≥5 runs per problem)")
        if avg_exact_pass_10 is not None:
            print(f"  Pass@10: {avg_exact_pass_10:.1f}% (GPT-4/Codex standard)")
        else:
            print(f"  Pass@10: N/A (need ≥10 runs per problem)")
        
        print("\\n📊 EMPIRICAL PASS@K (Direct Observation - For Comparison):")
        if avg_empirical_pass_1 is not None:
            print(f"  Pass@1:  {avg_empirical_pass_1:.0f}% (first run success)")
        if avg_empirical_pass_5 is not None:
            print(f"  Pass@5:  {avg_empirical_pass_5:.0f}% (any success in first 5)")
        else:
            print(f"  Pass@5:  N/A (need ≥5 runs per problem)")
        if avg_empirical_pass_10 is not None:
            print(f"  Pass@10: {avg_empirical_pass_10:.0f}% (any success in first 10)")
        else:
            print(f"  Pass@10: N/A (need ≥10 runs per problem)")
        
        # Iteration efficiency averages (only from successful runs)
        problems_with_success = [p for p in all_problems if p.get('iteration_efficiency', {}).get('total_successful_runs', 0) > 0]
        
        if problems_with_success:
            avg_iterations = sum(p['iteration_efficiency']['avg_iterations'] for p in problems_with_success) / len(problems_with_success)
            avg_within_1 = sum(p['iteration_efficiency']['success_within_1'] for p in problems_with_success) / len(problems_with_success)
            avg_within_3 = sum(p['iteration_efficiency']['success_within_3'] for p in problems_with_success) / len(problems_with_success)
            avg_within_6 = sum(p['iteration_efficiency']['success_within_6'] for p in problems_with_success) / len(problems_with_success)
            
            print("\\n⚡ TDD ITERATION EFFICIENCY (Your Innovation):")
            print(f"  Average iterations to success: {avg_iterations:.2f}")
            print("  Within single run with TDD guidance:")
            print(f"    - {avg_within_1:.1f}% solve on first iteration")
            print(f"    - {avg_within_3:.1f}% solve within 3 iterations")
            print(f"    - {avg_within_6:.1f}% solve within 6 iterations")
        
        # Statistics
        total_problems = len(all_problems)
        problems_solved = len(problems_with_success)
        
        print(f"\\n{'='*70}")
        print("📊 EVALUATION STATISTICS:")
        print(f"{'='*70}")
        print(f"Total problems evaluated: {total_problems}")
        print(f"Problems solved (at least once): {problems_solved}")
        print(f"Overall solve rate: {(problems_solved/total_problems*100):.1f}%")
        print(f"Total API calls made: {self.results['total_api_calls']}")
        print(f"Total evaluation time: {total_time/60:.1f} minutes")
        
        # Comparison with benchmarks
        print(f"\\n{'='*70}")
        print("📝 COMPARISON WITH PUBLISHED RESULTS (Research-Standard Pass@k):")
        print(f"{'='*70}")
        print("Standard Benchmarks (HumanEval):")
        print("  GPT-4:        Pass@1=67.0%, Pass@10=86.4%")
        print("  GPT-3.5:      Pass@1=48.1%, Pass@10=69.9%")
        print("  Codex:        Pass@1=28.8%, Pass@10=46.8%")
        # Display Your System results with None handling
        if avg_exact_pass_1 is not None:
            if avg_exact_pass_10 is not None:
                print(f"\\nYour System:  Pass@1={avg_exact_pass_1:.1f}%, Pass@10={avg_exact_pass_10:.1f}% (Exact Formula)")
            else:
                print(f"\\nYour System:  Pass@1={avg_exact_pass_1:.1f}%, Pass@10=N/A (need ≥10 runs)")
        
        if problems_with_success:
            print(f"              (with avg {avg_iterations:.1f} iterations per success)")
        
        # Efficiency advantage calculation
        if avg_exact_pass_10 is not None and avg_exact_pass_10 > 0 and problems_with_success:
            print(f"\\n✨ EFFICIENCY ADVANTAGE:")
            print(f"  Standard approach needs 10 independent samples for {avg_exact_pass_10:.1f}%")
            print(f"  Your system needs {avg_iterations:.1f} iterations average for same success")
            print(f"  API efficiency: {(10/avg_iterations):.1f}x fewer calls per success")
        
        print(f"{'='*70}")
    
    def save_intermediate_results(self):
        """Save intermediate results during evaluation"""
        filename = 'pass_k_intermediate.json'
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def save_final_results(self):
        """Save final results with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'pass_k_dual_results_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
            
        print(f"\\n💾 Complete results saved to: {filename}")
        return filename