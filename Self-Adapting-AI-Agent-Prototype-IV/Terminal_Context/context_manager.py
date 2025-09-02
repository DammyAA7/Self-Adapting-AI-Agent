"""
Context Manager Module
Manages multiple terminal sessions and provides higher-level context operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from .persistent_terminal import PersistentTerminal


class ContextManager:
    """
    Manages terminal contexts for the Self-Adapting AI Agent.
    Provides session management, function tracking, and context persistence.
    """
    
    def __init__(self, session_dir: str = "context_sessions"):
        """
        Initialize the context manager.
        
        Args:
            session_dir: Directory to store session data
        """
        self.session_dir = session_dir
        self.terminals: Dict[str, PersistentTerminal] = {}
        self.active_terminal: Optional[PersistentTerminal] = None
        self.session_data = {
            'created_at': datetime.now().isoformat(),
            'functions': {},
            'variables': {},
            'execution_history': []
        }
        
        # Create session directory if it doesn't exist
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
    
    def create_terminal(self, name: str = "main", shell_type: str = "python") -> PersistentTerminal:
        """
        Create a new terminal session.
        
        Args:
            name: Name for the terminal session
            shell_type: Type of shell (python, bash, etc.)
            
        Returns:
            The created PersistentTerminal instance
        """
        if name in self.terminals:
            print(f"Terminal '{name}' already exists. Using existing terminal.")
            return self.terminals[name]
        
        terminal = PersistentTerminal(shell_type)
        self.terminals[name] = terminal
        
        # Set as active if it's the first terminal
        if self.active_terminal is None:
            self.active_terminal = terminal
        
        return terminal
    
    def get_terminal(self, name: str = "main") -> Optional[PersistentTerminal]:
        """Get a terminal by name."""
        return self.terminals.get(name)
    
    def get_active_terminal(self) -> Optional[PersistentTerminal]:
        """Get the currently active terminal."""
        if self.active_terminal is None and self.terminals:
            # Set the first terminal as active
            self.active_terminal = next(iter(self.terminals.values()))
        return self.active_terminal
    
    def set_active_terminal(self, name: str):
        """Set the active terminal by name."""
        if name in self.terminals:
            self.active_terminal = self.terminals[name]
            return True
        return False
    
    def execute_in_context(self, code: str, terminal_name: str = None) -> Dict[str, Any]:
        """
        Execute code in a terminal context.
        
        Args:
            code: Code to execute
            terminal_name: Name of terminal to use (uses active if None)
            
        Returns:
            Execution result dictionary
        """
        if terminal_name:
            terminal = self.get_terminal(terminal_name)
        else:
            terminal = self.get_active_terminal()
        
        if not terminal:
            # Create a default terminal if none exists
            terminal = self.create_terminal()
        
        # Execute the code
        result = terminal.execute(code)
        
        # Track execution
        self.session_data['execution_history'].append({
            'timestamp': datetime.now().isoformat(),
            'code': code,
            'success': result['success'],
            'terminal': terminal_name or "main"
        })
        
        # Track functions if defined
        if "def " in code and result['success']:
            self._track_functions(code)
        
        return result
    
    def _track_functions(self, code: str):
        """Track function definitions in the session."""
        import re
        # Extract function definitions
        function_pattern = r'def\s+(\w+)\s*\((.*?)\):'
        matches = re.findall(function_pattern, code)
        
        for func_name, params in matches:
            # Preserve existing function data if it has complete 'code' key
            # This protects loaded session data from being overwritten with snippets
            if (func_name in self.session_data['functions'] and 
                'code' in self.session_data['functions'][func_name]):
                continue  # Skip overwriting complete function data
                
            # Only track with snippet if no complete data exists
            self.session_data['functions'][func_name] = {
                'parameters': params,
                'defined_at': datetime.now().isoformat(),
                'code_snippet': code[:200]  # Store first 200 chars
            }
    
    def add_generated_function(self, function_name: str, function_code: str, 
                             function_info: Dict[str, Any] = None):
        """
        Add a generated function to the context.
        
        Args:
            function_name: Name of the function
            function_code: Complete function code
            function_info: Additional information about the function
        """
        # Validate function code before execution
        if not function_code.strip():
            print(f"Failed to add function '{function_name}': Empty function code")
            return False
        
        # Check if function_name appears in the code (basic validation)
        if f"def {function_name}" not in function_code:
            print(f"Warning: Function name '{function_name}' not found in function code")
        
        # Execute the function code in the active terminal
        result = self.execute_in_context(function_code)
        
        if result['success']:
            # Track the function
            self.session_data['functions'][function_name] = {
                'code': function_code,
                'info': function_info or {},
                'added_at': datetime.now().isoformat(),
                'execution_result': result
            }
            print(f"Function '{function_name}' added to persistent context")
            return True
        else:
            error_msg = result.get('error', 'Unknown error')
            print(f"Failed to add function '{function_name}': {error_msg}")
            # Print the function code for debugging if there's an error
            if error_msg and 'IndentationError' in error_msg:
                print("Function code that caused the error:")
                for i, line in enumerate(function_code.split('\n'), 1):
                    print(f"{i:3d}: {line}")
            return False
    
    def list_available_functions(self) -> List[str]:
        """List all functions available in the current context."""
        terminal = self.get_active_terminal()
        if terminal and terminal.shell_type == "python":
            # Get functions from the Python context
            return terminal.list_functions()
        else:
            # Return tracked functions
            return list(self.session_data['functions'].keys())
    
    def save_session(self, filename: str = None) -> str:
        """
        Save the current session to a file.
        
        Args:
            filename: Name of the file (auto-generated if None)
            
        Returns:
            Path to the saved session file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{timestamp}.json"
        
        filepath = os.path.join(self.session_dir, filename)
        
        # Prepare session data
        save_data = {
            'session_data': self.session_data,
            'terminals': {
                name: terminal.get_context_info() 
                for name, terminal in self.terminals.items()
            },
            'saved_at': datetime.now().isoformat()
        }
        
        # Save to file
        with open(filepath, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"Session saved to: {filepath}")
        return filepath
    
    def load_session(self, filepath: str) -> bool:
        """
        Load a session from a file.
        
        Args:
            filepath: Path to the session file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            # Restore session data
            self.session_data = save_data['session_data']
            
            # Recreate terminals and execute function definitions
            for func_name, func_data in self.session_data['functions'].items():
                if 'code' in func_data:
                    # Re-execute the function definition
                    self.execute_in_context(func_data['code'])
            
            print(f"Session loaded from: {filepath}")
            print(f"Restored {len(self.session_data['functions'])} functions")
            return True
            
        except Exception as e:
            print(f"Failed to load session: {e}")
            return False
    
    def clear_all_contexts(self):
        """Clear all terminal contexts."""
        for terminal in self.terminals.values():
            terminal.clear_context()
        
        # Reset session data
        self.session_data = {
            'created_at': datetime.now().isoformat(),
            'functions': {},
            'variables': {},
            'execution_history': []
        }
        print("All contexts cleared")
    
    def terminate_all(self):
        """Terminate all terminal sessions."""
        for name, terminal in self.terminals.items():
            terminal.terminate()
            print(f"Terminated terminal: {name}")
        
        self.terminals.clear()
        self.active_terminal = None
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get a summary of the current session."""
        return {
            'terminals': list(self.terminals.keys()),
            'active_terminal': next((k for k, v in self.terminals.items() 
                                    if v == self.active_terminal), None),
            'functions_defined': len(self.session_data['functions']),
            'function_names': list(self.session_data['functions'].keys()),
            'executions': len(self.session_data['execution_history']),
            'session_created': self.session_data['created_at']
        }
    
    def __del__(self):
        """Cleanup on deletion."""
        self.terminate_all()


# Singleton instance for global access
_global_context_manager = None

def get_context_manager() -> ContextManager:
    """Get the global context manager instance."""
    global _global_context_manager
    if _global_context_manager is None:
        _global_context_manager = ContextManager()
    return _global_context_manager


# Test the context manager
if __name__ == "__main__":
    print("Testing Context Manager...")
    
    manager = ContextManager()
    
    # Create a Python terminal
    terminal = manager.create_terminal("main", "python")
    
    # Add a function
    factorial_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
    manager.add_generated_function("factorial", factorial_code)
    
    # Use the function
    result = manager.execute_in_context("print(factorial(5))")
    print(f"Factorial(5) = {result['output']}")
    
    # Add another function that uses the first
    double_factorial_code = """
def double_factorial(n):
    return factorial(n) * 2
"""
    manager.add_generated_function("double_factorial", double_factorial_code)
    
    # Use the new function
    result = manager.execute_in_context("print(double_factorial(5))")
    print(f"Double Factorial(5) = {result['output']}")
    
    # List functions
    functions = manager.list_available_functions()
    print(f"Available functions: {functions}")
    
    # Get summary
    summary = manager.get_session_summary()
    print(f"Session summary: {json.dumps(summary, indent=2)}")
    
    # Save session
    session_file = manager.save_session()
    
    # Cleanup
    manager.terminate_all()