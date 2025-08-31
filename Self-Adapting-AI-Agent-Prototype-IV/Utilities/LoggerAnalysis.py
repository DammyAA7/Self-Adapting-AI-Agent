import json
import os
from datetime import datetime
import statistics
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter
import seaborn as sns

class FunctionGenerationAnalyzer:
    def __init__(self, json_log_file='function_generation_stats.json'):
        self.json_log_file = json_log_file
        self.data = self.load_data()
        
    def load_data(self):
        """Load the function generation statistics from JSON file"""
        if not os.path.exists(self.json_log_file):
            print(f"Warning: Log file {self.json_log_file} not found.")
            return []
        
        try:
            with open(self.json_log_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading data: {e}")
            return []
    
    def extract_function_data(self):
        """Extract all function generation attempts from sessions"""
        functions = []
        for session in self.data:
            for func in session.get('functions', []):
                func['session_id'] = session['session_id']
                func['session_start'] = session['start_time']
                
                # Calculate duration if start_time and end_time are available
                if 'start_time' in func and 'end_time' in func:
                    try:
                        start = datetime.fromisoformat(func['start_time'])
                        end = datetime.fromisoformat(func['end_time'])
                        func['duration_seconds'] = (end - start).total_seconds()
                    except (ValueError, TypeError):
                        func['duration_seconds'] = None
                else:
                    func['duration_seconds'] = None
                
                functions.append(func)
        return functions
    
    def calculate_iteration_time_statistics(self):
        """Calculate statistics about iterations and time"""
        functions = self.extract_function_data()
        
        if not functions:
            return {
                'error': 'No function data available for analysis'
            }
        
        # Extract iterations and durations
        iterations = [f.get('iterations', 0) for f in functions]
        durations = [f.get('duration_seconds') for f in functions if f.get('duration_seconds') is not None]
        
        # Separate by success status
        successful_functions = [f for f in functions if f.get('successful', False)]
        failed_functions = [f for f in functions if not f.get('successful', False)]
        
        successful_iterations = [f.get('iterations', 0) for f in successful_functions]
        failed_iterations = [f.get('iterations', 0) for f in failed_functions]
        
        successful_durations = [f.get('duration_seconds') for f in successful_functions if f.get('duration_seconds') is not None]
        failed_durations = [f.get('duration_seconds') for f in failed_functions if f.get('duration_seconds') is not None]
        
        stats = {
            'total_functions': len(functions),
            'successful_functions': len(successful_functions),
            'failed_functions': len(failed_functions),
            'success_rate': len(successful_functions) / len(functions) * 100 if functions else 0,
            
            # Iteration statistics
            'avg_iterations_all': statistics.mean(iterations) if iterations else 0,
            'median_iterations_all': statistics.median(iterations) if iterations else 0,
            'min_iterations': min(iterations) if iterations else 0,
            'max_iterations': max(iterations) if iterations else 0,
            'avg_iterations_successful': statistics.mean(successful_iterations) if successful_iterations else 0,
            'avg_iterations_failed': statistics.mean(failed_iterations) if failed_iterations else 0,
            
            # Duration statistics
            'functions_with_duration': len(durations),
            'avg_duration_seconds': statistics.mean(durations) if durations else 0,
            'median_duration_seconds': statistics.median(durations) if durations else 0,
            'min_duration_seconds': min(durations) if durations else 0,
            'max_duration_seconds': max(durations) if durations else 0,
            'avg_duration_successful': statistics.mean(successful_durations) if successful_durations else 0,
            'avg_duration_failed': statistics.mean(failed_durations) if failed_durations else 0,
        }
        
        # Add standard deviations
        if len(iterations) > 1:
            stats['std_dev_iterations'] = statistics.stdev(iterations)
        if len(durations) > 1:
            stats['std_dev_duration'] = statistics.stdev(durations)
            
        return stats
    
    def generate_report(self, save_to_file=True):
        """Generate a focused analysis report on iterations and time"""
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("FUNCTION GENERATION ANALYSIS - ITERATIONS & TIME")
        report_lines.append("=" * 60)
        
        stats = self.calculate_iteration_time_statistics()
        
        if 'error' in stats:
            error_msg = f"Error: {stats['error']}"
            print(error_msg)
            return
        
        report_lines.append("\n📊 OVERALL STATISTICS")
        report_lines.append(f"   Total Functions: {stats['total_functions']}")
        report_lines.append(f"   Success Rate: {stats['success_rate']:.1f}%")
        
        report_lines.append("\n🔄 ITERATION ANALYSIS")
        report_lines.append(f"   Average Iterations: {stats['avg_iterations_all']:.2f}")
        report_lines.append(f"   Median Iterations: {stats['median_iterations_all']:.1f}")
        report_lines.append(f"   Range: {stats['min_iterations']} - {stats['max_iterations']} iterations")
        report_lines.append(f"   Successful Functions: {stats['avg_iterations_successful']:.2f} avg iterations")
        report_lines.append(f"   Failed Functions: {stats['avg_iterations_failed']:.2f} avg iterations")
        if 'std_dev_iterations' in stats:
            report_lines.append(f"   Standard Deviation: {stats['std_dev_iterations']:.2f}")
        
        report_lines.append("\n⏱️  TIME ANALYSIS")
        if stats['functions_with_duration'] > 0:
            report_lines.append(f"   Functions with timing data: {stats['functions_with_duration']}")
            report_lines.append(f"   Average Duration: {stats['avg_duration_seconds']:.1f} seconds ({stats['avg_duration_seconds']/60:.1f} minutes)")
            report_lines.append(f"   Median Duration: {stats['median_duration_seconds']:.1f} seconds")
            report_lines.append(f"   Range: {stats['min_duration_seconds']:.1f} - {stats['max_duration_seconds']:.1f} seconds")
            report_lines.append(f"   Successful Functions: {stats['avg_duration_successful']:.1f} seconds average")
            report_lines.append(f"   Failed Functions: {stats['avg_duration_failed']:.1f} seconds average")
            if 'std_dev_duration' in stats:
                report_lines.append(f"   Standard Deviation: {stats['std_dev_duration']:.1f} seconds")
        else:
            report_lines.append("   No timing data available in the dataset")
        
        report_lines.append("\n💡 KEY INSIGHTS")
        if stats['avg_iterations_successful'] < stats['avg_iterations_failed']:
            report_lines.append("   ✓ Successful functions require fewer iterations on average")
        else:
            report_lines.append("   ⚠ Failed functions actually require fewer iterations (may hit limits)")
            
        if stats['functions_with_duration'] > 0:
            if stats['avg_duration_successful'] < stats['avg_duration_failed']:
                report_lines.append("   ✓ Successful functions complete faster on average")
            else:
                report_lines.append("   ⚠ Failed functions complete faster (likely due to early termination)")
        
        # Print to console
        for line in report_lines:
            print(line)
        
        # Save to file if requested
        if save_to_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f'function_generation_report_{timestamp}.txt'
            
            with open(filename, 'w', encoding='utf-8') as f:
                for line in report_lines:
                    f.write(line + '\n')
            
            print(f"\n📁 Report saved to: {filename}")
            return filename
    
    def create_focused_visualizations(self):
        """Create exactly two charts: iterations distribution and time analysis"""
        functions = self.extract_function_data()
        if not functions:
            print("No data available for visualization")
            return
        
        # Set up the plot style
        plt.style.use('default')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Function Generation Analysis: Iterations & Time', fontsize=16, fontweight='bold')
        
        # Chart 1: Iterations Distribution
        iterations = [f.get('iterations', 0) for f in functions]
        successful_iter = [f.get('iterations', 0) for f in functions if f.get('successful', False)]
        failed_iter = [f.get('iterations', 0) for f in functions if not f.get('successful', False)]
        
        # Create histogram for iterations
        bins = range(1, max(iterations) + 2)
        
        # Calculate averages for legend
        avg_successful = statistics.mean(successful_iter) if successful_iter else 0
        avg_failed = statistics.mean(failed_iter) if failed_iter else 0
        
        # Create labels with averages
        successful_label = f'Successful (avg: {avg_successful:.1f})'
        failed_label = f'Failed (avg: {avg_failed:.1f})' if failed_iter else 'Failed (avg: N/A)'
        
        ax1.hist([successful_iter, failed_iter], bins=bins, alpha=0.7, 
                label=[successful_label, failed_label], color=['green', 'red'], edgecolor='black')
        
        ax1.set_title('Function Generation: Iterations Distribution', fontweight='bold')
        ax1.set_xlabel('Number of Iterations')
        ax1.set_ylabel('Number of Functions')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add overall statistics lines
        avg_iter = statistics.mean(iterations)
        median_iter = statistics.median(iterations)
        ax1.axvline(avg_iter, color='blue', linestyle='--', alpha=0.8, label=f'Overall Mean: {avg_iter:.1f}')
        ax1.axvline(median_iter, color='orange', linestyle='--', alpha=0.8, label=f'Overall Median: {median_iter:.1f}')
        ax1.legend()
        
        # Chart 2: Time Analysis
        durations = [f.get('duration_seconds') for f in functions if f.get('duration_seconds') is not None]
        
        if durations:
            successful_durations = [f.get('duration_seconds') for f in functions 
                                  if f.get('successful', False) and f.get('duration_seconds') is not None]
            failed_durations = [f.get('duration_seconds') for f in functions 
                              if not f.get('successful', False) and f.get('duration_seconds') is not None]
            
            # Convert to minutes for better readability
            durations_min = [d/60 for d in durations]
            successful_min = [d/60 for d in successful_durations] if successful_durations else []
            failed_min = [d/60 for d in failed_durations] if failed_durations else []
            
            # Create histogram for duration
            if successful_min and failed_min:
                ax2.hist([successful_min, failed_min], bins=15, alpha=0.7,
                        label=['Successful', 'Failed'], color=['green', 'red'], edgecolor='black')
            elif durations_min:
                ax2.hist(durations_min, bins=15, alpha=0.7, color='blue', edgecolor='black')
            
            ax2.set_title('Function Generation: Time Distribution', fontweight='bold')
            ax2.set_xlabel('Duration (minutes)')
            ax2.set_ylabel('Number of Functions')
            if successful_min and failed_min:
                ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            # Add statistics
            avg_duration = statistics.mean(durations_min)
            median_duration = statistics.median(durations_min)
            ax2.axvline(avg_duration, color='blue', linestyle='--', alpha=0.8, 
                       label=f'Mean: {avg_duration:.1f}min')
            ax2.axvline(median_duration, color='orange', linestyle='--', alpha=0.8, 
                       label=f'Median: {median_duration:.1f}min')
            ax2.legend()
            
        else:
            ax2.text(0.5, 0.5, 'No timing data available\nin the dataset', 
                    ha='center', va='center', transform=ax2.transAxes, 
                    fontsize=14, bbox=dict(boxstyle='round', facecolor='lightgray'))
            ax2.set_title('Function Generation: Time Distribution', fontweight='bold')
            ax2.set_xlabel('Duration (minutes)')
            ax2.set_ylabel('Number of Functions')
        
        plt.tight_layout()
        
        # Save the plot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f'function_generation_analysis_{timestamp}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Charts saved to: {filename}")
        
        # Show the plot
        plt.show()
        
        return filename

def main():
    """Main function to run the focused analysis"""
    analyzer = FunctionGenerationAnalyzer()
    
    # Generate focused report
    analyzer.generate_report()
    
    # Create the two focused visualizations
    try:
        analyzer.create_focused_visualizations()
    except ImportError:
        print("\n📊 Visualization skipped - matplotlib not installed")
        print("   Install with: pip install matplotlib pandas")
    except Exception as e:
        print(f"\n📊 Visualization error: {e}")

if __name__ == "__main__":
    main()