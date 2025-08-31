"""
Persistent Terminal Module
Maintains context across multiple command executions by keeping subprocess alive.
Inspired by Open Interpreter's approach to context preservation.
"""

import subprocess
import queue
import threading
import time
import os
import sys
import platform
from typing import Optional, Dict, Any, List


class PersistentTerminal:
    """
    Maintains a persistent subprocess for continuous context.
    Unlike traditional subprocess.run(), this keeps the process alive
    between commands, preserving variables, functions, and state.
    """
    
    def __init__(self, shell_type: str = "python", timeout: float = 2.0):
        """
        Initialize a persistent terminal session.
        
        Args:
            shell_type: Type of shell ('python', 'bash', 'cmd', 'powershell')
            timeout: Default timeout for output collection in seconds
        """
        self.shell_type = shell_type
        self.timeout = timeout
        self.process = None
        self.output_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.is_alive = False
        self.context_variables = {}  # Track defined variables/functions
        self.execution_history = []  # Track command history
        
        # Start the persistent process
        self.start_process()
    
    def start_process(self):
        """Start a persistent subprocess based on shell type."""
        # Determine the command based on shell type and platform
        if self.shell_type == "python":
            # Use interactive mode to keep Python interpreter alive
            cmd = [sys.executable, "-i", "-u"]  # -u for unbuffered output
        elif self.shell_type == "bash":
            if platform.system() == "Windows":
                # Try WSL bash first, then Git bash
                cmd = ["wsl", "bash"]
            else:
                cmd = ["bash"]
        elif self.shell_type == "cmd":
            if platform.system() == "Windows":
                cmd = ["cmd.exe"]
            else:
                raise ValueError("CMD is only available on Windows")
        elif self.shell_type == "powershell":
            if platform.system() == "Windows":
                cmd = ["powershell.exe", "-NoExit", "-Command", "-"]
            else:
                cmd = ["pwsh", "-NoExit", "-Command", "-"]
        else:
            raise ValueError(f"Unsupported shell type: {self.shell_type}")
        
        # Create the subprocess with pipes for communication
        try:
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,  # Unbuffered
                universal_newlines=True,
                env=os.environ.copy()
            )
            
            # Start threads to read output and errors
            self.stdout_thread = threading.Thread(
                target=self._read_stream,
                args=(self.process.stdout, self.output_queue),
                daemon=True
            )
            self.stderr_thread = threading.Thread(
                target=self._read_stream,
                args=(self.process.stderr, self.error_queue),
                daemon=True
            )
            
            self.stdout_thread.start()
            self.stderr_thread.start()
            
            self.is_alive = True
            
            # Initialize based on shell type
            self._initialize_shell()
            
            print(f"Started persistent {self.shell_type} terminal (PID: {self.process.pid})")
            
        except Exception as e:
            print(f"Failed to start {self.shell_type} terminal: {e}")
            self.is_alive = False
            raise
    
    def _initialize_shell(self):
        """Initialize the shell with necessary settings."""
        if self.shell_type == "python":
            # Set up Python environment
            init_code = """
import sys
import os
__terminal_context__ = True
print("Python terminal initialized with context preservation")
"""
            self.execute(init_code, timeout=1)
        elif self.shell_type == "bash":
            # Set bash to not exit on error
            self.execute("set +e", timeout=0.5)
    
    def _read_stream(self, stream, target_queue):
        """Read from a stream and put lines into a queue."""
        try:
            for line in iter(stream.readline, ''):
                if line:
                    target_queue.put(line)
        except:
            pass  # Stream closed
    
    def execute(self, code: str, timeout: Optional[float] = None) -> Dict[str, Any]:
        """
        Execute code in the persistent session.
        
        Args:
            code: Code to execute
            timeout: Timeout for collecting output (uses default if None)
            
        Returns:
            Dictionary with 'output', 'error', 'success' keys
        """
        if not self.is_alive or not self.process:
            raise RuntimeError("Terminal process is not alive")
        
        if timeout is None:
            timeout = self.timeout
        
        # Clear queues before execution
        self._clear_queues()
        
        # Track execution
        self.execution_history.append(code)
        
        # Send code to the process
        try:
            # For Python, handle multi-line code blocks specially
            if self.shell_type == "python":
                marker = "__EXECUTION_COMPLETE__"
                
                # Check if this is a multi-line code block (function definition, class, etc.)
                is_multiline = any(keyword in code for keyword in ['def ', 'class ', 'for ', 'while ', 'with ', 'if ', 'try:', 'except'])
                
                if is_multiline and '\n' in code.strip():
                    # Wrap multi-line code in exec() to execute as a complete block
                    # Escape any existing triple quotes in the code
                    escaped_code = code.replace('"""', '\\"\\"\\"').replace("'''", "\\'\\'\\'")
                    exec_code = f'exec("""{escaped_code}""")\nprint("{marker}")\n'
                else:
                    # Single line or simple statement - execute directly
                    exec_code = code
                    if not exec_code.endswith('\n'):
                        exec_code += '\n'
                    exec_code += f"print('{marker}')\n"
                
                self.process.stdin.write(exec_code)
            else:
                # Non-Python shells - execute as before
                if not code.endswith('\n'):
                    code += '\n'
                self.process.stdin.write(code)
            
            self.process.stdin.flush()
            
            # Collect output
            output = self._collect_output(timeout, marker if self.shell_type == "python" else None)
            errors = self._collect_errors(0.1)  # Quick error check
            
            # Track defined variables/functions (for Python)
            if self.shell_type == "python" and "def " in code:
                # Extract function names
                import re
                functions = re.findall(r'def\s+(\w+)\s*\(', code)
                for func in functions:
                    self.context_variables[func] = 'function'
            
            return {
                'output': output,
                'error': errors,
                'success': len(errors) == 0 or errors.isspace(),
                'context_preserved': True
            }
            
        except Exception as e:
            return {
                'output': '',
                'error': str(e),
                'success': False,
                'context_preserved': False
            }
    
    def _collect_output(self, timeout: float, end_marker: Optional[str] = None) -> str:
        """Collect output from the output queue."""
        output_lines = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                line = self.output_queue.get_nowait()
                
                # Check for end marker
                if end_marker and end_marker in line:
                    # Remove the marker from output
                    line = line.replace(end_marker, '').strip()
                    if line:
                        output_lines.append(line)
                    break
                
                output_lines.append(line.rstrip())
                
            except queue.Empty:
                # If we have output and queue is empty, we're likely done
                if output_lines:
                    time.sleep(0.1)  # Brief wait to ensure no more output
                    if self.output_queue.empty():
                        break
                else:
                    time.sleep(0.01)  # Small sleep to prevent busy waiting
        
        return '\n'.join(output_lines)
    
    def _collect_errors(self, timeout: float) -> str:
        """Collect errors from the error queue."""
        error_lines = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                line = self.error_queue.get_nowait()
                error_lines.append(line.rstrip())
            except queue.Empty:
                break
        
        return '\n'.join(error_lines)
    
    def _clear_queues(self):
        """Clear output and error queues."""
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except:
                break
        
        while not self.error_queue.empty():
            try:
                self.error_queue.get_nowait()
            except:
                break
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get information about the current context."""
        return {
            'shell_type': self.shell_type,
            'is_alive': self.is_alive,
            'pid': self.process.pid if self.process else None,
            'defined_variables': list(self.context_variables.keys()),
            'execution_count': len(self.execution_history)
        }
    
    def list_functions(self) -> List[str]:
        """List all functions defined in the context."""
        if self.shell_type == "python":
            result = self.execute("print([name for name in dir() if callable(eval(name)) and not name.startswith('_')])", timeout=1)
            if result['success']:
                try:
                    # Parse the list from output
                    import ast
                    return ast.literal_eval(result['output'].strip())
                except:
                    pass
        return [k for k, v in self.context_variables.items() if v == 'function']
    
    def clear_context(self):
        """Clear the context by restarting the process."""
        self.terminate()
        self.context_variables.clear()
        self.execution_history.clear()
        self.start_process()
    
    def terminate(self):
        """Terminate the persistent process."""
        if self.process:
            try:
                self.process.stdin.close()
                self.process.stdout.close()
                self.process.stderr.close()
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                try:
                    self.process.kill()  # Force kill if terminate fails
                except:
                    pass
            
            self.process = None
            self.is_alive = False
            print(f"Terminated {self.shell_type} terminal")
    
    def __del__(self):
        """Cleanup on deletion."""
        self.terminate()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.terminate()


# Convenience function for quick testing
def test_persistent_terminal():
    """Test the persistent terminal with Python."""
    print("Testing Persistent Terminal...")
    
    with PersistentTerminal("python") as terminal:
        # Test 1: Define a function
        result = terminal.execute("def add(a, b): return a + b")
        print(f"Define function - Success: {result['success']}")
        
        # Test 2: Use the function (context preserved!)
        result = terminal.execute("result = add(5, 3)")
        print(f"Use function - Success: {result['success']}")
        
        # Test 3: Access the variable (context preserved!)
        result = terminal.execute("print(f'Result is: {result}')")
        print(f"Access variable - Output: {result['output']}")
        
        # Test 4: List functions
        functions = terminal.list_functions()
        print(f"Available functions: {functions}")
        
        # Test 5: Get context info
        info = terminal.get_context_info()
        print(f"Context info: {info}")


if __name__ == "__main__":
    test_persistent_terminal()