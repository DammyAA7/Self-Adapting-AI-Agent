#!/usr/bin/env python3
"""
Aggregate Pass@k Results from Individual Problem Runs
Combines multiple JSON result files into final comprehensive Pass@k metrics
"""
import json
import glob
import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List

def load_results_from_files(pattern: str = "pass_k_dual_results_*.json") -> List[Dict]:
    """Load all Pass@k result files matching the pattern"""
    files = glob.glob(pattern)
    results = []
    
    print(f"🔍 Found {len(files)} result files:")
    for file in sorted(files):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                results.append({
                    'file': file,
                    'data': data,
                    'timestamp': data.get('timestamp', 'unknown')
                })
            print(f"  ✅ {file} - {len(data.get('problems', {}))} problems")
        except Exception as e:
            print(f"  ❌ {file} - Error: {e}")
    
    return results

def aggregate_standard_pass_k(all_results: List[Dict]) -> Dict:
    """Aggregate standard Pass@k metrics across all problems"""
    all_problems = {}
    
    # Collect all problems from all result files
    for result in all_results:
        problems = result['data'].get('problems', {})
        for problem_name, problem_data in problems.items():
            if problem_name not in all_problems:
                all_problems[problem_name] = problem_data
            else:
                print(f"⚠️  Duplicate problem found: {problem_name}")
    
    if not all_problems:
        return {}
    
    # Calculate aggregate metrics
    pass_1_scores = [p['standard_pass_k']['pass@1'] for p in all_problems.values() if 'standard_pass_k' in p]
    pass_5_scores = [p['standard_pass_k']['pass@5'] for p in all_problems.values() if 'standard_pass_k' in p]
    pass_10_scores = [p['standard_pass_k']['pass@10'] for p in all_problems.values() if 'standard_pass_k' in p]
    
    avg_exact_pass_1 = sum(pass_1_scores) / len(pass_1_scores) * 100 if pass_1_scores else 0
    avg_exact_pass_5 = sum(pass_5_scores) / len(pass_5_scores) * 100 if pass_5_scores else 0
    avg_exact_pass_10 = sum(pass_10_scores) / len(pass_10_scores) * 100 if pass_10_scores else 0
    
    # Also calculate empirical averages
    emp_pass_1_scores = [p['standard_pass_k']['pass@1_empirical'] for p in all_problems.values() if 'standard_pass_k' in p]
    emp_pass_5_scores = [p['standard_pass_k']['pass@5_empirical'] for p in all_problems.values() if 'standard_pass_k' in p]
    emp_pass_10_scores = [p['standard_pass_k']['pass@10_empirical'] for p in all_problems.values() if 'standard_pass_k' in p]
    
    avg_emp_pass_1 = sum(emp_pass_1_scores) / len(emp_pass_1_scores) * 100 if emp_pass_1_scores else 0
    avg_emp_pass_5 = sum(emp_pass_5_scores) / len(emp_pass_5_scores) * 100 if emp_pass_5_scores else 0
    avg_emp_pass_10 = sum(emp_pass_10_scores) / len(emp_pass_10_scores) * 100 if emp_pass_10_scores else 0
    
    return {
        'exact': {
            'pass@1': avg_exact_pass_1,
            'pass@5': avg_exact_pass_5,
            'pass@10': avg_exact_pass_10
        },
        'empirical': {
            'pass@1': avg_emp_pass_1,
            'pass@5': avg_emp_pass_5,
            'pass@10': avg_emp_pass_10
        },
        'total_problems': len(all_problems)
    }

def aggregate_efficiency_metrics(all_results: List[Dict]) -> Dict:
    """Aggregate TDD iteration efficiency metrics"""
    problems_with_success = []
    
    # Collect all successful problems
    for result in all_results:
        problems = result['data'].get('problems', {})
        for problem_name, problem_data in problems.items():
            if problem_data.get('iteration_efficiency', {}).get('total_successful_runs', 0) > 0:
                problems_with_success.append(problem_data['iteration_efficiency'])
    
    if not problems_with_success:
        return {}
    
    avg_iterations = sum(p['avg_iterations'] for p in problems_with_success) / len(problems_with_success)
    avg_within_1 = sum(p['success_within_1'] for p in problems_with_success) / len(problems_with_success)
    avg_within_3 = sum(p['success_within_3'] for p in problems_with_success) / len(problems_with_success)
    avg_within_6 = sum(p['success_within_6'] for p in problems_with_success) / len(problems_with_success)
    
    return {
        'avg_iterations': avg_iterations,
        'success_within_1': avg_within_1,
        'success_within_3': avg_within_3,
        'success_within_6': avg_within_6,
        'problems_with_success': len(problems_with_success)
    }

def calculate_total_stats(all_results: List[Dict]) -> Dict:
    """Calculate total statistics across all runs"""
    total_api_calls = sum(result['data'].get('total_api_calls', 0) for result in all_results)
    total_problems = sum(len(result['data'].get('problems', {})) for result in all_results)
    
    # Calculate solve rate
    solved_problems = 0
    for result in all_results:
        problems = result['data'].get('problems', {})
        for problem_data in problems.values():
            if problem_data.get('standard_pass_k', {}).get('total_successful', 0) > 0:
                solved_problems += 1
    
    solve_rate = (solved_problems / total_problems * 100) if total_problems > 0 else 0
    
    return {
        'total_problems': total_problems,
        'problems_solved': solved_problems,
        'solve_rate': solve_rate,
        'total_api_calls': total_api_calls
    }

def display_final_results(pass_k_metrics: Dict, efficiency_metrics: Dict, stats: Dict):
    """Display final aggregated results in research format"""
    print("\n" + "="*70)
    print("🎯 FINAL AGGREGATED PASS@K RESULTS")
    print("="*70)
    
    if pass_k_metrics:
        print("\n🎯 RESEARCH-STANDARD PASS@K (Exact Formula - Primary Results):")
        print(f"  Pass@1:  {pass_k_metrics['exact']['pass@1']:.1f}% (unbiased probability estimator)")
        print(f"  Pass@5:  {pass_k_metrics['exact']['pass@5']:.1f}% (research-comparable)")
        print(f"  Pass@10: {pass_k_metrics['exact']['pass@10']:.1f}% (GPT-4/Codex standard)")
        
        print("\n📊 EMPIRICAL PASS@K (Direct Observation - For Comparison):")
        print(f"  Pass@1:  {pass_k_metrics['empirical']['pass@1']:.0f}% (first run success)")
        print(f"  Pass@5:  {pass_k_metrics['empirical']['pass@5']:.0f}% (any success in first 5)")
        print(f"  Pass@10: {pass_k_metrics['empirical']['pass@10']:.0f}% (any success in first 10)")
    
    if efficiency_metrics:
        print("\n⚡ TDD ITERATION EFFICIENCY (Your Innovation):")
        print(f"  Average iterations to success: {efficiency_metrics['avg_iterations']:.2f}")
        print(f"  Within single run with TDD guidance:")
        print(f"    - {efficiency_metrics['success_within_1']:.1f}% solve on first iteration")
        print(f"    - {efficiency_metrics['success_within_3']:.1f}% solve within 3 iterations")
        print(f"    - {efficiency_metrics['success_within_6']:.1f}% solve within 6 iterations")
    
    print(f"\n{'='*70}")
    print("📊 EVALUATION STATISTICS:")
    print(f"{'='*70}")
    print(f"Total problems evaluated: {stats['total_problems']}")
    print(f"Problems solved (at least once): {stats['problems_solved']}")
    print(f"Overall solve rate: {stats['solve_rate']:.1f}%")
    print(f"Total API calls made: {stats['total_api_calls']}")
    
    if pass_k_metrics:
        print(f"\n{'='*70}")
        print("📝 COMPARISON WITH PUBLISHED RESULTS (Research-Standard Pass@k):")
        print(f"{'='*70}")
        print("Standard Benchmarks (HumanEval):")
        print("  GPT-4:        Pass@1=67.0%, Pass@10=86.4%")
        print("  GPT-3.5:      Pass@1=48.1%, Pass@10=69.9%")
        print("  Codex:        Pass@1=28.8%, Pass@10=46.8%")
        print(f"\nYour System:  Pass@1={pass_k_metrics['exact']['pass@1']:.1f}%, Pass@10={pass_k_metrics['exact']['pass@10']:.1f}% (Exact Formula)")
        
        if efficiency_metrics:
            print(f"              (with avg {efficiency_metrics['avg_iterations']:.1f} iterations per success)")
            
            # Calculate efficiency advantage
            if pass_k_metrics['exact']['pass@10'] > 0:
                print(f"\n✨ EFFICIENCY ADVANTAGE:")
                print(f"  Standard approach needs 10 independent samples for {pass_k_metrics['exact']['pass@10']:.1f}%")
                print(f"  Your system needs {efficiency_metrics['avg_iterations']:.1f} iterations average for same success")
                print(f"  API efficiency: {(10/efficiency_metrics['avg_iterations']):.1f}x fewer calls per success")
    
    print(f"{'='*70}")

def save_aggregated_results(pass_k_metrics: Dict, efficiency_metrics: Dict, stats: Dict, all_results: List[Dict]):
    """Save aggregated results to JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"aggregated_pass_k_results_{timestamp}.json"
    
    aggregated_data = {
        'timestamp': datetime.now().isoformat(),
        'source_files': [r['file'] for r in all_results],
        'standard_pass_k': pass_k_metrics,
        'iteration_efficiency': efficiency_metrics,
        'statistics': stats,
        'total_problems_evaluated': stats['total_problems'],
        'evaluation_type': 'aggregated_individual_runs'
    }
    
    with open(filename, 'w') as f:
        json.dump(aggregated_data, f, indent=2)
    
    print(f"\n💾 Aggregated results saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Aggregate Pass@k results from individual problem runs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Aggregate all result files in current directory
  python evaluation/aggregate_pass_k_results.py
  
  # Aggregate specific pattern of files
  python evaluation/aggregate_pass_k_results.py --pattern "pass_k_dual_results_20250904*.json"
  
  # Just show results without saving
  python evaluation/aggregate_pass_k_results.py --no-save
        """
    )
    
    parser.add_argument('--pattern', type=str, default="pass_k_dual_results_*.json",
                       help='File pattern to match result files (default: pass_k_dual_results_*.json)')
    parser.add_argument('--no-save', action='store_true',
                       help='Do not save aggregated results to file')
    
    args = parser.parse_args()
    
    # Load all result files
    results = load_results_from_files(args.pattern)
    
    if not results:
        print("❌ No result files found!")
        print(f"🔍 Looked for pattern: {args.pattern}")
        return 1
    
    print(f"\n📊 Aggregating results from {len(results)} files...")
    
    # Aggregate metrics
    pass_k_metrics = aggregate_standard_pass_k(results)
    efficiency_metrics = aggregate_efficiency_metrics(results)
    stats = calculate_total_stats(results)
    
    # Display results
    display_final_results(pass_k_metrics, efficiency_metrics, stats)
    
    # Save aggregated results
    if not args.no_save:
        save_aggregated_results(pass_k_metrics, efficiency_metrics, stats, results)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)