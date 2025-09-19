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
            'functions': [],
            'existing_function_calls': []
        }
        self.current_function = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                # Uncomment the line below to also log to console
                # logging.StreamHandler()
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
            'terminated_early': False,
            'termination_reason': None,
            'final_function_name': None,
            'adjudication_attempts': [],
            'reinforcement_history': []
        }
        
        self.current_function = function_data
        self.current_session['functions'].append(function_data)
        
        self.logger.info(f"=== STARTING FUNCTION GENERATION ===")
        self.logger.info(f"User Input: {user_input}")
        self.logger.info(f"Function Requirement: {function_requirement}")
        
    def log_iteration(self, iteration_num, unit_test_result, adjudication_result):
        """Log details of each iteration"""
        if self.current_function is None:
            self.logger.warning("No current function to log iteration for")
            return
            
        self.current_function['iterations'] = iteration_num
        
        adjudication_data = {
            'iteration': iteration_num,
            'judgement': adjudication_result.judgement,
            'code_requirement_suggestion': adjudication_result.code_requirement_suggestion,
            'unit_requirement_suggestion': adjudication_result.unit_requirement_suggestion,
            'timestamp': datetime.now().isoformat(),
            'unit_test_summary': self._summarize_unit_test_result(unit_test_result)
        }
        
        self.current_function['adjudication_attempts'].append(adjudication_data)
        
        self.logger.info(f"--- ITERATION {iteration_num} ---")
        self.logger.info(f"Unit Test Result Summary: {adjudication_data['unit_test_summary']}")
        self.logger.info(f"Adjudication Passed: {adjudication_result.judgement}")
        if not adjudication_result.judgement:
            self.logger.info(f"Code Requirement Suggestion: {adjudication_result.code_requirement_suggestion}")
            self.logger.info(f"Unit Requirement Suggestion: {adjudication_result.unit_requirement_suggestion}")
            
    def log_reinforcement(self, reinforcement_type, old_requirement, new_requirement, iteration_num):
        """Log requirement reinforcements"""
        if self.current_function is None:
            self.logger.warning("No current function to log reinforcement for")
            return
            
        reinforcement_data = {
            'type': reinforcement_type,  # 'code' or 'unit_test'
            'iteration': iteration_num,
            'old_requirement': old_requirement,
            'new_requirement': new_requirement,
            'timestamp': datetime.now().isoformat()
        }
        
        self.current_function['reinforcement_history'].append(reinforcement_data)
        
        self.logger.info(f"--- REQUIREMENT REINFORCEMENT ({reinforcement_type.upper()}) ---")
        self.logger.info(f"Iteration: {iteration_num}")
        self.logger.info(f"Previous Requirement: {old_requirement}")
        self.logger.info(f"New Requirement: {new_requirement}")
            
    def log_function_success(self, function_name):
        """Log successful function generation"""
        if self.current_function is None:
            self.logger.warning("No current function to log success for")
            return
            
        self.current_function['successful'] = True
        self.current_function['final_function_name'] = function_name
        self.current_function['end_time'] = datetime.now().isoformat()
        
        # Calculate total time
        start_time = datetime.fromisoformat(self.current_function['start_time'])
        end_time = datetime.fromisoformat(self.current_function['end_time'])
        total_duration = (end_time - start_time).total_seconds()
        self.current_function['total_duration_seconds'] = total_duration
        
        self.logger.info(f"=== FUNCTION GENERATION SUCCESSFUL ===")
        self.logger.info(f"Function Name: {function_name}")
        self.logger.info(f"Total Iterations: {self.current_function['iterations']}")
        self.logger.info(f"Total Duration: {total_duration:.2f} seconds")
        self.logger.info(f"Final Adjudication Attempts: {len(self.current_function['adjudication_attempts'])}")
        self.logger.info(f"Requirement Reinforcements: {len(self.current_function['reinforcement_history'])}")
            
    def log_existing_function_call(self, function_name, function_args, execution_result):
        """Log when an existing function is called successfully"""
        call_data = {
            'function_name': function_name,
            'function_args': function_args,
            'execution_time': execution_result.get('execution_time'),
            'memory_peak': execution_result.get('memory_peak'),
            'result': str(execution_result.get('result', ''))[:200],  # Truncate long results
            'timestamp': datetime.now().isoformat(),
            'successful': execution_result.get('success', True)
        }
        
        self.current_session['existing_function_calls'].append(call_data)
        
        self.logger.info(f"=== EXISTING FUNCTION CALLED ===")
        self.logger.info(f"Function: {function_name}")
        self.logger.info(f"Arguments: {function_args}")
        self.logger.info(f"Execution Time: {execution_result.get('execution_time', 'N/A')} seconds")
        self.logger.info(f"Memory Peak: {execution_result.get('memory_peak', 'N/A')} bytes")
        self.logger.info(f"Success: {execution_result.get('success', True)}")
        
    def log_max_iterations_reached(self, max_iterations):
        """Log when the maximum iterations limit is reached"""
        if self.current_function is None:
            self.logger.warning("No current function to log max iterations for")
            return
            
        self.current_function['terminated_early'] = True
        self.current_function['termination_reason'] = f"Maximum iterations ({max_iterations}) reached"
        self.current_function['end_time'] = datetime.now().isoformat()
        
        # Calculate total time
        start_time = datetime.fromisoformat(self.current_function['start_time'])
        end_time = datetime.fromisoformat(self.current_function['end_time'])
        total_duration = (end_time - start_time).total_seconds()
        self.current_function['total_duration_seconds'] = total_duration
        
        self.logger.warning(f"=== MAX ITERATIONS REACHED ===")
        self.logger.warning(f"Maximum iterations ({max_iterations}) reached without successful function generation.")
        self.logger.warning(f"Total Duration: {total_duration:.2f} seconds")
        self.logger.warning(f"Final Iteration Count: {self.current_function['iterations']}")
        
    def log_user_interruption(self):
        """Log when process is interrupted by user"""
        self.logger.info("=== PROCESS INTERRUPTED BY USER ===")
        if self.current_function and not self.current_function.get('end_time'):
            self.current_function['terminated_early'] = True
            self.current_function['termination_reason'] = "User interruption (Ctrl+C)"
            self.current_function['end_time'] = datetime.now().isoformat()
            
    def log_unexpected_error(self, error_message):
        """Log unexpected errors"""
        self.logger.error(f"=== UNEXPECTED ERROR ===")
        self.logger.error(f"Error: {error_message}")
        if self.current_function and not self.current_function.get('end_time'):
            self.current_function['terminated_early'] = True
            self.current_function['termination_reason'] = f"Unexpected error: {error_message}"
            self.current_function['end_time'] = datetime.now().isoformat()
            
    def log_model_response_without_tools(self, response_content):
        """Log when model responds without calling tools (triggers function generation)"""
        self.logger.info(f"=== MODEL RESPONSE WITHOUT TOOL CALLS ===")
        self.logger.info(f"Response Content: {response_content[:200]}{'...' if len(response_content) > 200 else ''}")
        self.logger.info("Initiating function generation process...")
        
    def _summarize_unit_test_result(self, unit_test_result):
        """Create a brief summary of unit test results"""
        if not unit_test_result:
            return "No unit test result"
        
        result_str = str(unit_test_result)
        # Extract key information
        if "PASSED" in result_str and "FAILED" in result_str:
            return "Mixed results (some passed, some failed)"
        elif "PASSED" in result_str:
            return "All tests passed"
        elif "FAILED" in result_str or "ERROR" in result_str:
            return "Tests failed"
        else:
            return "Unit tests executed"
            
    def save_session_stats(self):
        """Save session statistics to JSON file"""
        self.current_session['end_time'] = datetime.now().isoformat()
        
        # Calculate session duration
        start_time = datetime.fromisoformat(self.current_session['start_time'])
        end_time = datetime.fromisoformat(self.current_session['end_time'])
        session_duration = (end_time - start_time).total_seconds()
        self.current_session['session_duration_seconds'] = session_duration
        
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
        terminated_functions = sum(1 for f in self.current_session['functions'] if f.get('terminated_early', False))
        total_iterations = sum(f['iterations'] for f in self.current_session['functions'])
        existing_function_calls = len(self.current_session['existing_function_calls'])
        successful_existing_calls = sum(1 for call in self.current_session['existing_function_calls'] if call.get('successful', True))
        
        # Calculate total final adjudication attempts
        total_final_adjudications = sum(len(f.get('adjudication_attempts', [])) for f in self.current_session['functions'])
        total_reinforcements = sum(len(f.get('reinforcement_history', [])) for f in self.current_session['functions'])
        
        summary = {
            'session_duration_seconds': self.current_session.get('session_duration_seconds', 0),
            'total_functions_attempted': total_functions,
            'successful_functions': successful_functions,
            'terminated_functions': terminated_functions,
            'total_iterations': total_iterations,
            'existing_function_calls': existing_function_calls,
            'successful_existing_calls': successful_existing_calls,
            'total_final_adjudication_attempts': total_final_adjudications,
            'total_requirement_reinforcements': total_reinforcements,
            'average_iterations_per_function': total_iterations / max(total_functions, 1)
        }
        
        self.logger.info(f"=== SESSION SUMMARY ===")
        self.logger.info(f"Session Duration: {summary['session_duration_seconds']:.2f} seconds")
        self.logger.info(f"Functions Attempted: {summary['total_functions_attempted']}")
        self.logger.info(f"Successful Functions: {summary['successful_functions']}")
        self.logger.info(f"Terminated Early: {summary['terminated_functions']}")
        self.logger.info(f"Total Iterations: {summary['total_iterations']}")
        self.logger.info(f"Average Iterations per Function: {summary['average_iterations_per_function']:.2f}")
        self.logger.info(f"Existing Function Calls: {summary['existing_function_calls']} ({summary['successful_existing_calls']} successful)")
        self.logger.info(f"Final Adjudication Attempts: {summary['total_final_adjudication_attempts']}")
        self.logger.info(f"Requirement Reinforcements: {summary['total_requirement_reinforcements']}")
        
        return summary