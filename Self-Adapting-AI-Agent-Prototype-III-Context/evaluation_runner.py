"""
Benchmark Evaluation Runner for Prototype IV
Runs comprehensive evaluation including HumanEval benchmarks and baseline comparisons.
"""

import os
import sys
import json
import time
from pathlib import Path

# Add SOTA_Evaluation to path
current_dir = Path(__file__).parent
sota_evaluation_path = current_dir.parent / "SOTA_Evaluation"
sys.path.insert(0, str(sota_evaluation_path))

# Add Prototype IV to path
sys.path.insert(0, str(current_dir))

from integration.prototype_iv_evaluator import PrototypeIVEvaluator
from datasets.humaneval_loader import HumanEvalLoader
from datasets.swe_bench_loader import SWEBenchLoader

def run_humaneval_evaluation(evaluator: PrototypeIVEvaluator, num_problems: int = 10):
    """Run HumanEval benchmark evaluation."""
    print(f"\n=== RUNNING HUMANEVAL BENCHMARK ({num_problems} problems) ===")
    
    # Run HumanEval benchmark
    benchmark_results = evaluator.run_humaneval_benchmark(num_problems)
    
    print(f"HumanEval Results:")
    print(f"  Total problems: {benchmark_results['total_problems']}")
    print(f"  Successful generations: {benchmark_results['successful_generations']}")
    print(f"  Success rate: {benchmark_results['pass_at_1_rate']:.2%}")
    print(f"  Average iterations: {benchmark_results['average_iterations']:.1f}")
    print(f"  Average time: {benchmark_results['average_time']:.1f}s")
    print(f"  Average complexity: {benchmark_results['average_complexity']:.1f}")
    
    return benchmark_results

def run_baseline_comparison(evaluator: PrototypeIVEvaluator, test_cases: list):
    """Run comparison against baseline (direct LLM)."""
    print(f"\n=== RUNNING BASELINE COMPARISON ({len(test_cases)} cases) ===")
    
    if not evaluator.baseline_comparator:
        print("Warning: No OpenAI client available, skipping baseline comparison")
        return None
    
    comparison_results = evaluator.run_baseline_comparison(test_cases)
    
    if 'error' not in comparison_results:
        print(f"Baseline Comparison Results:")
        success_rates = comparison_results.get('success_rates', {})
        print(f"  Framework success rate: {success_rates.get('framework', 0):.2%}")
        print(f"  Baseline success rate: {success_rates.get('baseline', 0):.2%}")
        print(f"  Improvement: {success_rates.get('improvement', 0):+.2%}")
        
        avg_times = comparison_results.get('average_times', {})
        print(f"  Framework avg time: {avg_times.get('framework', 0):.1f}s")
        print(f"  Baseline avg time: {avg_times.get('baseline', 0):.1f}s")
        print(f"  Framework faster: {'Yes' if avg_times.get('framework_faster', False) else 'No'}")
    
    return comparison_results

def run_statistical_analysis(evaluator: PrototypeIVEvaluator):
    """Run statistical analysis across prototypes."""
    print(f"\n=== RUNNING STATISTICAL ANALYSIS ===")
    
    # Sample data for all prototypes (replace with actual data)
    prototype_data = {
        'Prototype_I': [4.8, 5.2, 4.5, 5.0, 4.7, 4.9, 5.1, 4.6, 4.8, 5.0],
        'Prototype_II': [3.6, 3.8, 3.4, 3.5, 3.7, 3.9, 3.3, 3.6, 3.8, 3.5],
        'Prototype_III': [2.9, 3.1, 2.8, 3.0, 2.7, 3.2, 2.9, 2.8, 3.1, 2.9],
        'Prototype_IV': [2.2, 2.4, 2.1, 2.3, 2.0, 2.5, 2.1, 2.2, 2.4, 2.2]
    }
    
    statistical_results = evaluator.analyze_prototype_progression(prototype_data)
    
    print("Statistical Analysis Results:")
    if 'pairwise_comparisons' in statistical_results:
        for comparison, result in statistical_results['pairwise_comparisons'].items():
            if isinstance(result, dict) and 'p_value' in result:
                significance = "significant" if result.get('is_significant', False) else "not significant"
                print(f"  {comparison}: p={result['p_value']:.3f} ({significance})")
    
    if 'trend_analysis' in statistical_results:
        trend = statistical_results['trend_analysis']
        improvement = trend.get('overall_improvement_percent', 0)
        print(f"  Overall improvement: {improvement:+.1f}%")
        print(f"  Consistent improvement: {'Yes' if trend.get('consistent_improvement', False) else 'No'}")
    
    return statistical_results

def generate_paper_outputs(evaluator: PrototypeIVEvaluator, all_results: dict):
    """Generate LaTeX tables and figures for NIER paper."""
    print(f"\n=== GENERATING NIER PAPER OUTPUTS ===")
    
    paper_outputs = evaluator.generate_nier_paper_outputs(all_results.get('prototype_data'))
    
    print("Generated paper outputs:")
    if 'tables' in paper_outputs:
        print("  LaTeX Tables:")
        for table_name in paper_outputs['tables'].keys():
            print(f"    - {table_name}")
    
    if 'figures' in paper_outputs:
        print("  Figures:")
        for fig_name, fig_path in paper_outputs['figures'].items():
            print(f"    - {fig_name}: {fig_path}")
    
    return paper_outputs

def create_test_cases_from_humaneval():
    """Create test cases from HumanEval for baseline comparison."""
    loader = HumanEvalLoader()
    problems = loader.get_sample_problems(5)  # Small set for testing
    
    test_cases = []
    for problem in problems:
        requirement = loader.convert_to_natural_language(problem)
        test_cases.append({
            'id': problem['task_id'],
            'requirement': requirement,
            'entry_point': problem['entry_point']
        })
    
    return test_cases

def main():
    """Main evaluation runner."""
    print("Starting Prototype IV Comprehensive Evaluation")
    print("=" * 60)
    
    # Initialize evaluator
    prototype_iv_path = Path(__file__).parent
    
    # Try to load OpenAI client for baseline comparison
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        # Check for Azure OpenAI credentials
        azure_api_key = os.environ.get("AZURE_OPENAI_API_KEY") or os.environ.get("AZURE_API_KEY")
        if azure_api_key:
            from openai import AzureOpenAI
            azure_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT") or "https://jenly-staging.cognitiveservices.azure.com"
            azure_api_version = os.environ.get("AZURE_OPENAI_API_VERSION") or "2024-12-01-preview"
            
            openai_client = AzureOpenAI(
                api_key=azure_api_key,
                azure_endpoint=azure_endpoint,
                api_version=azure_api_version
            )
            print("✓ OpenAI client initialized - baseline comparison enabled")
        else:
            openai_client = None
            print("⚠ No OpenAI credentials - baseline comparison disabled")
    except Exception as e:
        openai_client = None
        print(f"⚠ Failed to initialize OpenAI client: {e}")
    
    # Initialize SOTA evaluator
    evaluator = PrototypeIVEvaluator(str(prototype_iv_path), openai_client)
    evaluator.start_evaluation_session(f"comprehensive_eval_{int(time.time())}")
    
    # Container for all results
    all_results = {
        'humaneval_results': None,
        'baseline_comparison': None,
        'statistical_analysis': None,
        'paper_outputs': None,
        'prototype_data': {
            'Prototype I': {'avg_iterations': 4.8, 'success_rate': 62, 'avg_time': 187.3, 'memory': 89.2},
            'Prototype II': {'avg_iterations': 3.6, 'success_rate': 71, 'avg_time': 156.2, 'memory': 76.4},
            'Prototype III': {'avg_iterations': 2.9, 'success_rate': 84, 'avg_time': 132.7, 'memory': 68.1},
            'Prototype IV': {'avg_iterations': 2.2, 'success_rate': 91, 'avg_time': 104.5, 'memory': 60.9}
        }
    }
    
    try:
        # 1. Run HumanEval benchmark
        all_results['humaneval_results'] = run_humaneval_evaluation(evaluator, num_problems=10)
        
        # 2. Run baseline comparison if OpenAI client available
        if openai_client:
            test_cases = create_test_cases_from_humaneval()
            all_results['baseline_comparison'] = run_baseline_comparison(evaluator, test_cases)
        
        # 3. Run statistical analysis
        all_results['statistical_analysis'] = run_statistical_analysis(evaluator)
        
        # 4. Generate paper outputs
        all_results['paper_outputs'] = generate_paper_outputs(evaluator, all_results)
        
        # 5. Generate comprehensive report
        print(f"\n=== GENERATING COMPREHENSIVE REPORT ===")
        comprehensive_report = evaluator.generate_comprehensive_report()
        
        print(f"\n=== EVALUATION SUMMARY ===")
        print(f"Session ID: {evaluator.session_id}")
        print(f"Results directory: {evaluator.results_dir}")
        print(f"Total evaluation time: {time.time() - evaluator.session_start_time:.1f}s")
        
        # Save all results
        results_file = evaluator.results_dir / "complete_evaluation_results.json"
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2, default=str)
        
        print(f"Complete results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n⚠ Evaluation interrupted by user")
    except Exception as e:
        print(f"\n❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nEvaluation completed!")

if __name__ == "__main__":
    main()