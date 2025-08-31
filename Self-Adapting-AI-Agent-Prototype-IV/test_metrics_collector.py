"""
Collect and analyze metrics matching thesis Table 4.1
"""
import json
import statistics
import re
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

class MetricsCollector:
    def __init__(self, log_file='function_generation.log', stats_file='function_generation_stats.json'):
        self.log_file = log_file
        self.stats_file = stats_file
        self.calculator_results_file = 'calculator_test_results.json'
        self.todo_results_file = 'todo_test_results.json'
        
    def parse_logs(self):
        """Parse logs to extract metrics"""
        metrics = {
            'iterations': [],
            'durations': [],
            'success_count': 0,
            'failure_count': 0,
            'tdd_passes': [],
            'functions_generated': [],
            'tdd_adjudication_failures': 0,
            'final_adjudication_failures': 0
        }
        
        log_path = Path(self.log_file)
        if not log_path.exists():
            print(f"Log file {self.log_file} not found")
            return metrics
        
        with open(log_path, 'r') as f:
            content = f.read()
        
        # Split by function generation sessions
        sessions = content.split('=== STARTING FUNCTION GENERATION ===')
        
        for session in sessions[1:]:  # Skip first empty split
            # Count iterations
            iterations = len(re.findall(r'=== ITERATION \d+ ===', session))
            if iterations > 0:
                metrics['iterations'].append(iterations)
            
            # Check for success
            if "Function successfully generated" in session:
                metrics['success_count'] += 1
                
                # Extract function name
                func_match = re.search(r'Function ([\w_]+) successfully generated', session)
                if func_match:
                    metrics['functions_generated'].append(func_match.group(1))
            elif "Maximum iterations" in session or iterations > 0:
                metrics['failure_count'] += 1
            
            # Count TDD adjudication failures
            tdd_failures = len(re.findall(r'TDD Adjudication Passed: False', session))
            metrics['tdd_adjudication_failures'] += tdd_failures
            
            # Count final adjudication failures
            final_failures = len(re.findall(r'Adjudication Passed: False', session))
            metrics['final_adjudication_failures'] += final_failures
            
            # Extract duration if available
            duration_match = re.search(r'Total duration: ([\d.]+)', session)
            if duration_match:
                metrics['durations'].append(float(duration_match.group(1)))
        
        return metrics
    
    def parse_test_results(self):
        """Parse test result JSON files"""
        combined_results = {
            'calculator': [],
            'todo': [],
            'all': []
        }
        
        # Parse calculator results
        calc_path = Path(self.calculator_results_file)
        if calc_path.exists():
            with open(calc_path, 'r') as f:
                combined_results['calculator'] = json.load(f)
                combined_results['all'].extend(combined_results['calculator'])
        
        # Parse todo results
        todo_path = Path(self.todo_results_file)
        if todo_path.exists():
            with open(todo_path, 'r') as f:
                combined_results['todo'] = json.load(f)
                combined_results['all'].extend(combined_results['todo'])
        
        return combined_results
    
    def calculate_statistics(self, data_list):
        """Calculate statistical measures"""
        if not data_list:
            return {
                'mean': 0,
                'median': 0,
                'std_dev': 0,
                'min': 0,
                'max': 0,
                'count': 0
            }
        
        return {
            'mean': statistics.mean(data_list),
            'median': statistics.median(data_list),
            'std_dev': statistics.stdev(data_list) if len(data_list) > 1 else 0,
            'min': min(data_list),
            'max': max(data_list),
            'count': len(data_list)
        }
    
    def generate_report(self):
        """Generate report matching thesis Table 4.1"""
        print("\n" + "="*80)
        print("PERFORMANCE ANALYSIS REPORT - PROTOTYPE IV")
        print("="*80)
        
        # Parse all data sources
        log_metrics = self.parse_logs()
        test_results = self.parse_test_results()
        
        # Separate successful and failed results
        all_results = test_results['all']
        successful_results = [r for r in all_results if r.get('success', False)]
        failed_results = [r for r in all_results if not r.get('success', False)]
        generated_results = [r for r in all_results if r.get('generated_new', False)]
        
        # Calculate iteration statistics
        all_iterations = [r['iterations'] for r in all_results if r.get('iterations', 0) > 0]
        success_iterations = [r['iterations'] for r in successful_results if r.get('iterations', 0) > 0]
        failed_iterations = [r['iterations'] for r in failed_results if r.get('iterations', 0) > 0]
        
        # Calculate duration statistics (in seconds)
        all_durations = [r['duration'] for r in all_results if r.get('duration', 0) > 0]
        success_durations = [r['duration'] for r in successful_results if r.get('duration', 0) > 0]
        failed_durations = [r['duration'] for r in failed_results if r.get('duration', 0) > 0]
        
        # Create report matching thesis Table 4.1 format
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(all_results),
            'successful_tests': len(successful_results),
            'failed_tests': len(failed_results),
            'success_rate': len(successful_results) / len(all_results) * 100 if all_results else 0,
            
            # Iteration Analysis (matching thesis)
            'iteration_analysis': {
                'average_iterations': statistics.mean(all_iterations) if all_iterations else 0,
                'median_iterations': statistics.median(all_iterations) if all_iterations else 0,
                'iteration_range': f"{min(all_iterations) if all_iterations else 0} - {max(all_iterations) if all_iterations else 0}",
                'standard_deviation': statistics.stdev(all_iterations) if len(all_iterations) > 1 else 0,
            },
            
            # Success vs Failure Patterns
            'success_failure_patterns': {
                'successful_functions_avg_iterations': statistics.mean(success_iterations) if success_iterations else 0,
                'failed_functions_avg_iterations': statistics.mean(failed_iterations) if failed_iterations else 0,
            },
            
            # Time Analysis
            'time_analysis': {
                'average_duration_seconds': statistics.mean(all_durations) if all_durations else 0,
                'average_duration_minutes': statistics.mean(all_durations) / 60 if all_durations else 0,
                'median_duration_seconds': statistics.median(all_durations) if all_durations else 0,
                'duration_range_seconds': f"{min(all_durations):.1f} - {max(all_durations):.1f}" if all_durations else "0 - 0",
                'standard_deviation_seconds': statistics.stdev(all_durations) if len(all_durations) > 1 else 0,
            },
            
            # Success vs Failure Time Patterns
            'time_patterns': {
                'successful_functions_avg_seconds': statistics.mean(success_durations) if success_durations else 0,
                'failed_functions_avg_seconds': statistics.mean(failed_durations) if failed_durations else 0,
            },
            
            # Key Performance Indicators
            'key_indicators': {
                'functions_with_timing_data': len([r for r in all_results if r.get('duration', 0) > 0]),
                'tdd_integration': 'Yes',
                'new_functions_generated': len(generated_results),
                'tdd_adjudication_failures': log_metrics['tdd_adjudication_failures'],
                'final_adjudication_failures': log_metrics['final_adjudication_failures']
            }
        }
        
        # Print formatted report
        print("\n### ITERATION ANALYSIS ###")
        print(f"Average Iterations: {report['iteration_analysis']['average_iterations']:.2f}")
        print(f"Median Iterations: {report['iteration_analysis']['median_iterations']:.1f}")
        print(f"Iteration Range: {report['iteration_analysis']['iteration_range']}")
        print(f"Standard Deviation: {report['iteration_analysis']['standard_deviation']:.2f}")
        
        print("\n### SUCCESS VS FAILURE PATTERNS ###")
        print(f"Successful Functions (avg iterations): {report['success_failure_patterns']['successful_functions_avg_iterations']:.2f}")
        print(f"Failed Functions (avg iterations): {report['success_failure_patterns']['failed_functions_avg_iterations']:.2f}")
        
        print("\n### TIME ANALYSIS ###")
        print(f"Average Duration (seconds): {report['time_analysis']['average_duration_seconds']:.1f}")
        print(f"Average Duration (minutes): {report['time_analysis']['average_duration_minutes']:.1f}")
        print(f"Median Duration (seconds): {report['time_analysis']['median_duration_seconds']:.1f}")
        print(f"Duration Range (seconds): {report['time_analysis']['duration_range_seconds']}")
        print(f"Standard Deviation (seconds): {report['time_analysis']['standard_deviation_seconds']:.1f}")
        
        print("\n### KEY PERFORMANCE INDICATORS ###")
        print(f"Functions with Timing Data: {report['key_indicators']['functions_with_timing_data']}")
        print(f"TDD Integration: {report['key_indicators']['tdd_integration']}")
        print(f"New Functions Generated: {report['key_indicators']['new_functions_generated']}")
        
        # Compare with thesis targets
        print("\n" + "="*80)
        print("COMPARISON WITH THESIS TARGETS (Table 4.1)")
        print("="*80)
        
        thesis_targets = {
            'Average Iterations': (2.21, report['iteration_analysis']['average_iterations']),
            'Median Iterations': (2.0, report['iteration_analysis']['median_iterations']),
            'Success Iterations': (1.75, report['success_failure_patterns']['successful_functions_avg_iterations']),
            'Failed Iterations': (2.56, report['success_failure_patterns']['failed_functions_avg_iterations']),
            'Average Duration (s)': (142.4, report['time_analysis']['average_duration_seconds']),
            'Success Duration (s)': (111.9, report['time_patterns']['successful_functions_avg_seconds'])
        }
        
        print(f"{'Metric':<25} {'Target':<12} {'Actual':<12} {'Difference':<15} {'Status'}")
        print("-" * 80)
        
        for metric, (target, actual) in thesis_targets.items():
            if target > 0:
                diff = ((actual - target) / target) * 100
                status = "✓ PASS" if abs(diff) <= 20 else "✗ FAIL"  # 20% tolerance
            else:
                diff = 0
                status = "N/A"
            
            print(f"{metric:<25} {target:<12.2f} {actual:<12.2f} {diff:+14.1f}% {status}")
        
        # Save report to file
        report_file = f"performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Full report saved to: {report_file}")
        
        return report
    
    def generate_visualization(self, report):
        """Generate visualization plots"""
        try:
            # Create figure with subplots
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('Prototype IV Performance Analysis', fontsize=16)
            
            # Plot 1: Iteration Distribution
            test_results = self.parse_test_results()
            iterations = [r['iterations'] for r in test_results['all'] if r.get('iterations', 0) > 0]
            if iterations:
                axes[0, 0].hist(iterations, bins=range(0, max(iterations) + 2), edgecolor='black')
                axes[0, 0].axvline(2.21, color='red', linestyle='--', label='Thesis Target (2.21)')
                axes[0, 0].set_xlabel('Iterations')
                axes[0, 0].set_ylabel('Frequency')
                axes[0, 0].set_title('Iteration Distribution')
                axes[0, 0].legend()
            
            # Plot 2: Success Rate by Function Type
            calc_success = sum(1 for r in test_results['calculator'] if r.get('success', False))
            calc_total = len(test_results['calculator'])
            todo_success = sum(1 for r in test_results['todo'] if r.get('success', False))
            todo_total = len(test_results['todo'])
            
            if calc_total > 0 or todo_total > 0:
                categories = ['Calculator', 'ToDo']
                success_rates = [
                    calc_success / calc_total * 100 if calc_total > 0 else 0,
                    todo_success / todo_total * 100 if todo_total > 0 else 0
                ]
                axes[0, 1].bar(categories, success_rates, color=['blue', 'green'])
                axes[0, 1].set_ylabel('Success Rate (%)')
                axes[0, 1].set_title('Success Rate by Function Type')
                axes[0, 1].set_ylim(0, 100)
            
            # Plot 3: Duration Distribution
            durations = [r['duration'] for r in test_results['all'] if r.get('duration', 0) > 0]
            if durations:
                axes[1, 0].hist(durations, bins=20, edgecolor='black')
                axes[1, 0].axvline(142.4, color='red', linestyle='--', label='Thesis Target (142.4s)')
                axes[1, 0].set_xlabel('Duration (seconds)')
                axes[1, 0].set_ylabel('Frequency')
                axes[1, 0].set_title('Duration Distribution')
                axes[1, 0].legend()
            
            # Plot 4: Iterations vs Duration
            if iterations and len(durations) == len(iterations):
                axes[1, 1].scatter(iterations, durations, alpha=0.5)
                axes[1, 1].set_xlabel('Iterations')
                axes[1, 1].set_ylabel('Duration (seconds)')
                axes[1, 1].set_title('Iterations vs Duration')
            
            plt.tight_layout()
            
            # Save figure
            plot_file = f"performance_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(plot_file)
            print(f"\n✓ Visualization saved to: {plot_file}")
            
            # Don't show plot in automated tests
            # plt.show()
            
        except Exception as e:
            print(f"Warning: Could not generate visualization: {e}")

if __name__ == "__main__":
    collector = MetricsCollector()
    
    print("="*80)
    print("METRICS COLLECTION AND ANALYSIS")
    print("="*80)
    
    # Generate report
    report = collector.generate_report()
    
    # Generate visualization
    collector.generate_visualization(report)
    
    print("\n✅ Analysis complete!")