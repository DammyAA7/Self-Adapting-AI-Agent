#!/usr/bin/env python3
"""
Run Dual Pass@k Evaluation
Command-line interface for Pass@k evaluation with both metrics
"""
import sys
import os
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.pass_k_dual_evaluator import DualPassKEvaluator
from evaluation.benchmark_problems import get_all_problems, get_quick_problems

def main():
    parser = argparse.ArgumentParser(
        description="Run Dual Pass@k Evaluation on Self-Evolving Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick test with 2 problems, 5 runs each
  python evaluation/run_dual_pass_k.py --quick --runs 5
  
  # Full evaluation with all problems, 10 runs each  
  python evaluation/run_dual_pass_k.py --runs 10
  
  # Custom evaluation with specific number of problems
  python evaluation/run_dual_pass_k.py --problems 3 --runs 8
        """
    )
    
    parser.add_argument('--runs', type=int, default=10,
                       help='Number of independent runs per problem (default: 10)')
    parser.add_argument('--quick', action='store_true',
                       help='Quick test with subset of problems')
    parser.add_argument('--problems', type=int,
                       help='Limit to first N problems from full set')
    parser.add_argument('--problem', type=str,
                       help='Run specific problem by name (e.g., "is_equal_to_sum_even_HE_138")')
    parser.add_argument('--list-problems', action='store_true',
                       help='List all available problems and exit')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output during evaluation')
    parser.add_argument('--use-humaneval', action='store_true',
                       help='Enable HumanEval validation for authentic TiCoder comparison')
    
    args = parser.parse_args()
    
    # Handle list problems option
    if args.list_problems:
        all_problems = get_all_problems()
        print("📋 Available HumanEval Problems:")
        print("=" * 50)
        for i, (name, description) in enumerate(all_problems.items(), 1):
            print(f"{i:2}. {name}")
            print(f"    {description[:80]}...")
            print()
        return 0
    
    # Select problems
    if args.problem:
        # Run specific problem
        all_problems = get_all_problems()
        if args.problem not in all_problems:
            print(f"❌ Problem '{args.problem}' not found!")
            print("🔍 Available problems:")
            for name in all_problems.keys():
                print(f"  - {name}")
            return 1
        problems = {args.problem: all_problems[args.problem]}
        print(f"🎯 Single problem evaluation: {args.problem}")
    elif args.quick:
        problems = get_quick_problems()
        print("🏃 Quick evaluation mode selected")
    else:
        all_problems = get_all_problems()
        if args.problems:
            # Take first N problems
            items = list(all_problems.items())[:args.problems]
            problems = dict(items)
            print(f"📋 Evaluating first {len(problems)} problems")
        else:
            problems = all_problems
            print("📋 Full evaluation mode selected")
    
    print(f"🎯 Problems to evaluate: {list(problems.keys())}")
    print(f"🔄 Runs per problem: {args.runs}")
    print(f"📊 Total system runs: {len(problems) * args.runs}")
    if args.use_humaneval:
        print(f"🧪 Evaluation mode: HumanEval-validated (authentic TiCoder comparison)")
    else:
        print(f"🧪 Evaluation mode: TDD-only")
    print(f"⏱️ Estimated time: {(len(problems) * args.runs * 2 / 60):.1f} minutes")
    
    # Confirm before starting
    if len(problems) * args.runs > 20:
        response = input("\\n⚠️  This will make many API calls. Continue? (y/N): ")
        if response.lower() != 'y':
            print("Evaluation cancelled.")
            return
    
    # Initialize evaluator
    evaluator = DualPassKEvaluator(verbose=args.verbose, use_humaneval=args.use_humaneval)
    
    try:
        # Run evaluation
        results = evaluator.run_benchmark_suite(problems, args.runs)
        
        print("\\n🎉 Evaluation completed successfully!")
        print(f"📄 Check the generated JSON file for detailed results")
        
        return 0
        
    except KeyboardInterrupt:
        print("\\n\\n⏹️ Evaluation interrupted by user")
        evaluator.save_intermediate_results()
        print("💾 Intermediate results saved")
        return 1
        
    except Exception as e:
        print(f"\\n❌ Error during evaluation: {e}")
        evaluator.save_intermediate_results()
        print("💾 Intermediate results saved")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)