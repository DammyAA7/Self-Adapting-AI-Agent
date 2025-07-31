import logging
import json
import os
from datetime import datetime
class FunctionGenerationLogger:
    def __init__(self, log_file='function_generation.log', json_log_file='function_generation_stats.json'):
        self.log_file = log_file
        self.json_log_file = json_log_file
        self.setup_logging()
        self.current_session = {
            'session_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
            'start_time': datetime.now().isoformat(),
            'functions': []
        }
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                #logging.StreamHandler()  # Also log to console
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def start_function_generation(self, function_requirement, user_input):
        """Log the start of a new function generation process"""
        function_data = {
            'function_requirement': function_requirement,
            'user_input': user_input,
            'start_time': datetime.now().isoformat(),
            'iterations': 0,
            'successful': False,
            'final_function_name': None,
            'execution_metrics': [],
            'adjudication_attempts': []
        }
        
        self.current_function = function_data
        self.current_session['functions'].append(function_data)
        
        self.logger.info(f"=== STARTING FUNCTION GENERATION ===")
        self.logger.info(f"User Input: {user_input}")
        self.logger.info(f"Function Requirement: {function_requirement}")
        
    def log_iteration(self, iteration_num, unit_test_result, adjudication_result):
        """Log details of each iteration"""
        self.current_function['iterations'] = iteration_num
        
        adjudication_data = {
            'iteration': iteration_num,
            'judgement': adjudication_result.judgement,
            'requirement_suggestion': adjudication_result.code_requirement_suggestion,
            'unit_requirement_suggestion': adjudication_result.unit_requirement_suggestion,
            'timestamp': datetime.now().isoformat()
        }
        
        self.current_function['adjudication_attempts'].append(adjudication_data)
        
        self.logger.info(f"--- ITERATION {iteration_num} ---")
        self.logger.info(f"Unit Test Result: {unit_test_result}")
        self.logger.info(f"Adjudication Passed: {adjudication_result.judgement}")
        if not adjudication_result.judgement:
            self.logger.info(f"Requirement Suggestion: {adjudication_result.code_requirement_suggestion}")
            self.logger.info(f"Unit Requirement Suggestion: {adjudication_result.unit_requirement_suggestion}")
            
    def log_function_success(self, function_name, execution_metrics=None):
        """Log successful function generation and execution"""
        self.current_function['successful'] = True
        self.current_function['final_function_name'] = function_name
        self.current_function['end_time'] = datetime.now().isoformat()
        
        if execution_metrics:
            self.current_function['execution_metrics'].append({
                'function_name': function_name,
                'execution_time': execution_metrics.get('execution_time'),
                'memory_peak': execution_metrics.get('memory_peak'),
                'timestamp': datetime.now().isoformat()
            })
        
        self.logger.info(f"=== FUNCTION GENERATION SUCCESSFUL ===")
        self.logger.info(f"Function Name: {function_name}")
        self.logger.info(f"Total Iterations: {self.current_function['iterations']}")
        if execution_metrics:
            self.logger.info(f"Execution Time: {execution_metrics.get('execution_time', 'N/A')} seconds")
            self.logger.info(f"Memory Peak: {execution_metrics.get('memory_peak', 'N/A')} bytes")
            
    def log_existing_function_call(self, function_name, function_args, execution_metrics):
        """Log when an existing function is called successfully"""
        self.logger.info(f"=== EXISTING FUNCTION CALLED ===")
        self.logger.info(f"Function: {function_name}")
        self.logger.info(f"Arguments: {function_args}")
        self.logger.info(f"Execution Time: {execution_metrics.get('execution_time', 'N/A')} seconds")
        self.logger.info(f"Memory Peak: {execution_metrics.get('memory_peak', 'N/A')} bytes")
        
    def save_session_stats(self):
        """Save session statistics to JSON file"""
        self.current_session['end_time'] = datetime.now().isoformat()
        
        # Load existing stats or create new
        stats = []
        if os.path.exists(self.json_log_file):
            try:
                with open(self.json_log_file, 'r') as f:
                    stats = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                stats = []
        
        stats.append(self.current_session)
        
        with open(self.json_log_file, 'w') as f:
            json.dump(stats, f, indent=2)
            
    def get_generation_summary(self):
        """Get a summary of the current session"""
        total_functions = len(self.current_session['functions'])
        successful_functions = sum(1 for f in self.current_session['functions'] if f['successful'])
        total_iterations = sum(f['iterations'] for f in self.current_session['functions'])
        
        summary = {
            'total_functions_attempted': total_functions,
            'successful_functions': successful_functions,
            'total_iterations': total_iterations,
            'average_iterations_per_function': total_iterations / max(total_functions, 1)
        }
        
        self.logger.info(f"=== SESSION SUMMARY ===")
        self.logger.info(f"Functions Attempted: {summary['total_functions_attempted']}")
        self.logger.info(f"Successful Functions: {summary['successful_functions']}")
        self.logger.info(f"Total Iterations: {summary['total_iterations']}")
        self.logger.info(f"Average Iterations per Function: {summary['average_iterations_per_function']:.2f}")
        
        return summary
    
    def log_max_iterations_reached(self, max_iterations):
        """Log when the maximum iterations limit is reached"""
        self.logger.warning(f"=== MAX ITERATIONS REACHED ===")
        self.logger.warning(f"Maximum iterations ({max_iterations}) reached without successful function generation.")
