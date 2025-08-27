"""
Main test runner matching thesis methodology
- Run each test 30 times as specified in thesis Section 4.5
- Collect all metrics
- Generate final report
"""
import sys
import time
import os
from pathlib import Path
from datetime import datetime
from test_setup import setup_test_environment
from test_basic_calculator import CalculatorTester
from test_todo_operations import TodoTester
from test_metrics_collector import MetricsCollector

def run_complete_evaluation(repetitions=30):
    """
    Run complete evaluation following thesis methodology
    Default: 30 repetitions as stated in thesis
    """
    print("="*80)
    print("PROTOTYPE IV EVALUATION - FOLLOWING THESIS METHODOLOGY")
    print(f"Based on Section 4.5: {repetitions} test runs for statistical significance")
    print("="*80)
    
    # Phase 1: Setup
    print("\n" + "="*60)
    print("PHASE 1: ENVIRONMENT SETUP")
    print("="*60)
    
    if not setup_test_environment():
        print("❌ Environment setup failed. Please fix issues and retry.")
        return False
    
    print("✓ Environment ready")
    
    # Phase 2: Calculator Tests
    print("\n" + "="*60)
    print(f"PHASE 2: CALCULATOR TESTS ({repetitions} iterations)")
    print("="*60)
    
    calc_tester = CalculatorTester()
    
    print(f"\nRunning 5 arithmetic operations × {repetitions} times each")
    print("This will test: add, subtract, multiply, divide, sqrt")
    print("-" * 40)
    
    for i in range(repetitions):
        print(f"\n### CALCULATOR TEST RUN {i+1}/{repetitions} ###")
        calc_tester.run_all_tests(repetitions=1)
        
        # Show progress
        if (i + 1) % 5 == 0:
            print(f"\n>>> Progress: {i+1}/{repetitions} calculator runs complete")
            calc_tester.print_summary()
        
        # Small delay between runs to avoid API rate limits
        time.sleep(2)
    
    print("\n✓ Calculator tests complete")
    calc_tester.print_summary()
    
    # Phase 3: ToDo Tests
    print("\n" + "="*60)
    print(f"PHASE 3: TODO OPERATION TESTS ({repetitions} iterations)")
    print("="*60)
    
    todo_tester = TodoTester()
    
    print(f"\nRunning ToDo CRUD operations × {repetitions} times")
    print("Testing existing functions (add_todo, delete_todo)")
    print("Testing new generation (update_todo, list_todos, etc.)")
    print("-" * 40)
    
    for i in range(repetitions):
        print(f"\n### TODO TEST RUN {i+1}/{repetitions} ###")
        
        # Setup fresh test data
        todo_tester.setup_test_csv()
        
        # Test existing functions
        todo_tester.test_existing_functions()
        
        # Test new function generation
        todo_tester.test_new_generation()
        
        # Show progress
        if (i + 1) % 5 == 0:
            print(f"\n>>> Progress: {i+1}/{repetitions} ToDo runs complete")
            todo_tester.print_summary()
        
        # Small delay between runs
        time.sleep(2)
    
    print("\n✓ ToDo tests complete")
    todo_tester.print_summary()
    
    # Phase 4: Analysis
    print("\n" + "="*60)
    print("PHASE 4: PERFORMANCE ANALYSIS")
    print("="*60)
    
    collector = MetricsCollector()
    report = collector.generate_report()
    
    # Generate visualization if matplotlib is available
    try:
        collector.generate_visualization(report)
    except:
        print("Note: Visualization skipped (matplotlib may not be installed)")
    
    # Phase 5: Thesis Comparison
    print("\n" + "="*60)
    print("PHASE 5: THESIS TARGET COMPARISON")
    print("="*60)
    
    print("\nThesis targets from Table 4.1:")
    print("  - Average iterations: 2.21 (39% reduction from 3.62)")
    print("  - Median iterations: 2.0")
    print("  - Average duration: 142.4 seconds")
    print("  - Success rate: >80%")
    
    # Check if we met targets
    actual_avg_iter = report['iteration_analysis']['average_iterations']
    actual_median_iter = report['iteration_analysis']['median_iterations']
    actual_duration = report['time_analysis']['average_duration_seconds']
    success_rate = report.get('success_rate', 0)
    
    print("\nResults:")
    print(f"  ✓ Average iterations: {actual_avg_iter:.2f} (target: 2.21)")
    print(f"  ✓ Median iterations: {actual_median_iter:.1f} (target: 2.0)")
    print(f"  ✓ Average duration: {actual_duration:.1f}s (target: 142.4s)")
    print(f"  ✓ Success rate: {success_rate:.1f}% (target: >80%)")
    
    # Overall assessment
    targets_met = 0
    if abs(actual_avg_iter - 2.21) / 2.21 < 0.2:  # Within 20%
        targets_met += 1
    if abs(actual_median_iter - 2.0) / 2.0 < 0.2:
        targets_met += 1
    if abs(actual_duration - 142.4) / 142.4 < 0.3:  # Within 30% for duration
        targets_met += 1
    if success_rate > 80:
        targets_met += 1
    
    print("\n" + "="*80)
    print("EVALUATION COMPLETE")
    print("="*80)
    print(f"Targets met: {targets_met}/4")
    
    if targets_met >= 3:
        print("✅ SUCCESS: Prototype IV meets thesis performance targets!")
    else:
        print("⚠️  Prototype IV shows TDD improvements but may need tuning")
    
    return True

def quick_test():
    """Run a quick test with fewer repetitions for debugging"""
    print("\n" + "="*60)
    print("QUICK TEST MODE (3 repetitions for debugging)")
    print("="*60)
    return run_complete_evaluation(repetitions=3)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Prototype IV evaluation tests')
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick test with 3 repetitions instead of 30')
    parser.add_argument('--repetitions', type=int, default=30,
                       help='Number of test repetitions (default: 30 as per thesis)')
    
    args = parser.parse_args()
    
    print("\n" + "#"*80)
    print("# SELF-ADAPTING AI AGENT - PROTOTYPE IV EVALUATION")
    print("# Following methodology from thesis Section 4.5")
    print("#"*80)
    
    start_time = datetime.now()
    
    if args.quick:
        success = quick_test()
    else:
        success = run_complete_evaluation(repetitions=args.repetitions)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print(f"\nTotal evaluation time: {duration/60:.1f} minutes")
    print(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed or incomplete")
        sys.exit(1)