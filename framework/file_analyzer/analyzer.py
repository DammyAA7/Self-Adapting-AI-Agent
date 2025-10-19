"""
Simple file analyzer for reading and providing full project context to LLM.
For research purposes - gives LLM complete visibility without filtering.
"""

import os
import json
import ast
from typing import Dict, Any

class SimpleAnalyzer:
    """Reads all project files and provides full content to LLM"""
    
    def __init__(self, project_path: str):
        """
        Initialize analyzer with project path.
        
        Args:
            project_path: Path to the project to analyze
        """
        self.project_path = os.path.abspath(project_path) if project_path else os.getcwd()
        self.all_files_content = {}
        self.ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'env', 
                           'node_modules', '.pytest_cache', '.idea', '.vscode'}
        self.max_file_size = 100000  # 100KB max per file to avoid huge files
        
    def read_all_files(self) -> Dict[str, Any]:
        """
        Read all relevant files in the project without filtering.
        Returns everything for the LLM to process.
        """
        for root, dirs, files in os.walk(self.project_path):
            # Remove ignored directories from traversal
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith('.')]
            
            for file in files:
                filepath = os.path.join(root, file)
                relative_path = os.path.relpath(filepath, self.project_path)
                
                # Skip if file is too large
                try:
                    if os.path.getsize(filepath) > self.max_file_size:
                        self.all_files_content[relative_path] = {
                            'type': 'skipped',
                            'reason': f'File too large ({os.path.getsize(filepath)} bytes)'
                        }
                        continue
                except:
                    continue
                
                # Read Python files - COMPLETE CONTENT
                if file.endswith('.py'):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.all_files_content[relative_path] = {
                                'type': 'python',
                                'content': content,  # FULL CONTENT
                                'line_count': len(content.splitlines()),
                                'functions': self._extract_functions(content),
                                'classes': self._extract_classes(content)
                            }
                    except Exception as e:
                        self.all_files_content[relative_path] = {
                            'type': 'python',
                            'error': f"Could not read: {str(e)}"
                        }
                        
                # Read CSV files - COMPLETE CONTENT
                elif file.endswith('.csv'):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            lines = content.splitlines()
                            self.all_files_content[relative_path] = {
                                'type': 'csv',
                                'content': content,  # FULL CONTENT - ALL LINES
                                'line_count': len(lines),
                                'headers': lines[0] if lines else ''
                            }
                    except Exception as e:
                        self.all_files_content[relative_path] = {
                            'type': 'csv',
                            'error': f"Could not read: {str(e)}"
                        }
                        
                # Read JSON files - COMPLETE CONTENT
                elif file.endswith('.json'):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Try to parse to check if valid
                            json_data = json.loads(content)
                            self.all_files_content[relative_path] = {
                                'type': 'json',
                                'content': content,  # FULL CONTENT
                                'structure': self._get_json_structure(json_data)
                            }
                    except Exception as e:
                        self.all_files_content[relative_path] = {
                            'type': 'json',
                            'error': f"Could not read or parse: {str(e)}"
                        }
                        
                # Read text/config files - COMPLETE CONTENT
                elif file.endswith(('.txt', '.md', '.yml', '.yaml', '.ini', '.conf')):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            self.all_files_content[relative_path] = {
                                'type': 'text',
                                'content': content,  # FULL CONTENT
                                'line_count': len(content.splitlines())
                            }
                    except Exception as e:
                        self.all_files_content[relative_path] = {
                            'type': 'text',
                            'error': f"Could not read: {str(e)}"
                        }
        
        return self.all_files_content
    
    def _extract_functions(self, python_code: str) -> list:
        """Extract function names and signatures from Python code"""
        functions = []
        try:
            tree = ast.parse(python_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        'name': node.name,
                        'args': args,
                        'docstring': ast.get_docstring(node)
                    })
        except:
            pass
        return functions
    
    def _extract_classes(self, python_code: str) -> list:
        """Extract class names from Python code"""
        classes = []
        try:
            tree = ast.parse(python_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    classes.append({
                        'name': node.name,
                        'methods': methods
                    })
        except:
            pass
        return classes
    
    def _get_json_structure(self, json_data: Any) -> str:
        """Get a simple representation of JSON structure"""
        if isinstance(json_data, dict):
            return f"Object with keys: {list(json_data.keys())}"
        elif isinstance(json_data, list):
            if json_data and isinstance(json_data[0], dict):
                return f"Array of {len(json_data)} objects with keys: {list(json_data[0].keys())}"
            else:
                return f"Array with {len(json_data)} items"
        else:
            return str(type(json_data).__name__)
    
    def get_project_summary(self) -> Dict[str, Any]:
        """Get a summary of the analyzed project"""
        summary = {
            'project_path': self.project_path,
            'total_files': len(self.all_files_content),
            'python_files': 0,
            'csv_files': 0,
            'json_files': 0,
            'text_files': 0,
            'total_functions': 0,
            'total_classes': 0,
            'total_lines': 0,
            'file_list': list(self.all_files_content.keys())
        }
        
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'python':
                summary['python_files'] += 1
                summary['total_lines'] += file_data.get('line_count', 0)
                if 'functions' in file_data:
                    summary['total_functions'] += len(file_data['functions'])
                if 'classes' in file_data:
                    summary['total_classes'] += len(file_data['classes'])
            elif file_data.get('type') == 'csv':
                summary['csv_files'] += 1
                summary['total_lines'] += file_data.get('line_count', 0)
            elif file_data.get('type') == 'json':
                summary['json_files'] += 1
            elif file_data.get('type') == 'text':
                summary['text_files'] += 1
                summary['total_lines'] += file_data.get('line_count', 0)
        
        return summary
    
    def format_context_for_llm(self) -> str:
        """
        Format all file contents into a single context string for the LLM.
        No filtering - give LLM everything to work with.
        """
        summary = self.get_project_summary()
        
        context = f"""PROJECT ANALYSIS COMPLETE
========================
Project Path: {summary['project_path']}
Total Files Analyzed: {summary['total_files']}
Total Lines of Code/Data: {summary['total_lines']}
- Python files: {summary['python_files']} (Functions: {summary['total_functions']}, Classes: {summary['total_classes']})
- CSV files: {summary['csv_files']}
- JSON files: {summary['json_files']}
- Text/Config files: {summary['text_files']}

FILE STRUCTURE:
{chr(10).join('- ' + f for f in summary['file_list'])}

FILE PATHS AVAILABLE IN PROJECT:
================================
"""
        
        # Add full paths for each file type
        for filepath, file_data in self.all_files_content.items():
            full_path = os.path.join(self.project_path, filepath)
            file_type = file_data.get('type', 'unknown')
            if file_type == 'csv':
                context += f"CSV FILE: {full_path}\n"
            elif file_type == 'json':
                context += f"JSON FILE: {full_path}\n"
            elif file_type == 'python':
                context += f"PYTHON FILE: {full_path}\n"
            elif file_type == 'text':
                context += f"TEXT/CONFIG FILE: {full_path}\n"
        

        # Extract analyzed directory name for import instructions
        # Check if this is inside a 'dataset' or 'datasets' directory
        path_parts = self.project_path.split(os.sep)

        # Find if 'dataset' or 'datasets' is in the path
        import_path_components = []
        found_dataset = False
        for i, part in enumerate(path_parts):
            if part in ['dataset', 'datasets']:
                # Include dataset and everything after it
                import_path_components = path_parts[i:]
                found_dataset = True
                break

        if found_dataset:
            # Use full path from dataset onwards (e.g., dataset.patient_risk_analyzer)
            analyzed_dir_name = '.'.join(import_path_components)
        else:
            # Fallback to just basename if not in dataset directory
            analyzed_dir_name = os.path.basename(self.project_path)

        # Add import instructions
        context += f"""
CRITICAL IMPORT INSTRUCTIONS FOR TDD TESTS:
==========================================
When generating test cases that need classes/data from this analyzed project:

1. ALWAYS import classes and helper functions from the analyzed codebase using the FULL module path
2. NEVER import the function being tested from the codebase (it doesn't exist there yet!)
3. Import the function being tested from unit_test.functions
4. Never cause syntax errors:  File "framework/test_driven_development/testDrivenCases.py", line 4
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                       ^
SyntaxError: '(' was never closed


CORRECT IMPORT PATTERN (IMPORTANT: Use this exact Pattern to avoid problems. Always sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))) <-- IN HERE GIVE 5TH BRACKET IN LAST):
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
"""

        # Add specific import examples based on actual Python files found
        python_files = [f for f, d in self.all_files_content.items() if d.get('type') == 'python']
        if python_files:
            context += "\n# Import classes/data from analyzed codebase:\n"
            for py_file in python_files[:3]:  # Show first 3 as examples
                module_name = os.path.splitext(os.path.basename(py_file))[0]
                file_data = self.all_files_content[py_file]
                if file_data.get('classes'):
                    class_names = ', '.join([c['name'] for c in file_data['classes'][:5]])
                    context += f"from {analyzed_dir_name}.{module_name} import {class_names}\n"
                if file_data.get('functions'):
                    # Only show helper functions (like create_sample_xxx)
                    helper_funcs = [f['name'] for f in file_data['functions'] if 'create' in f['name'] or 'sample' in f['name']]
                    if helper_funcs:
                        context += f"from {analyzed_dir_name}.{module_name} import {', '.join(helper_funcs[:3])}\n"

        context += """```
        
IMPORTANT: If any file path is needed, always use the FULL ABSOLUTE paths shown in "FULL PATH" sections above.

Example: (CRITICAL: Always use absolute paths from the FILE PATHS section above):
WRONG: file_path = Path(__file__).parent / "data.csv"
RIGHT: file_path = "/absolute/path/to/dataset/patient_risk_analyzer/data.csv"  # Use actual FULL PATH shown above

IMPORTANT: Replace the class/function names above with the ACTUAL names you need from the files shown below.
Do NOT hardcode 'XYZ' or use placeholder names - use the real class names from the analyzed files!

WRONG: from dataset.XYZ import XYZ  # ❌ Don't use placeholders!
RIGHT: from dataset.patient_risk_analyzer.patient_records import Hospital, Patient  # ✅ Use actual names!

COMPLETE FILE CONTENTS BELOW:
==============================
"""
        
        # Add all Python files with FULL content
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'python' and 'content' in file_data:
                full_path = os.path.join(self.project_path, filepath)
                context += f"\n{'='*60}\nFILE: {filepath} (Python - {file_data.get('line_count', 0)} lines)\nFULL PATH: {full_path}\n{'='*60}\n"
                
                # Add function summary if available
                if file_data.get('functions'):
                    context += "Functions in this file:\n"
                    for func in file_data['functions']:
                        context += f"  - {func['name']}({', '.join(func['args'])})\n"
                    context += "\n"
                
                # Add the COMPLETE content
                context += file_data['content']
                context += "\n\n"
        
        # Add CSV files with FULL content
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'csv' and 'content' in file_data:
                full_path = os.path.join(self.project_path, filepath)
                context += f"\n{'='*60}\nFILE: {filepath} (CSV - {file_data.get('line_count', 0)} lines)\nFULL PATH: {full_path}\n{'='*60}\n"
                context += f"Headers: {file_data.get('headers', 'Unknown')}\n\n"
                context += "COMPLETE CSV CONTENT:\n"
                context += file_data['content']  # ALL LINES
                context += "\n\n"
        
        # Add JSON files with FULL content
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'json' and 'content' in file_data:
                full_path = os.path.join(self.project_path, filepath)
                context += f"\n{'='*60}\nFILE: {filepath} (JSON)\nFULL PATH: {full_path}\n{'='*60}\n"
                context += f"Structure: {file_data.get('structure', 'Unknown')}\n\n"
                context += "COMPLETE JSON CONTENT:\n"
                context += file_data['content']  # FULL JSON
                context += "\n\n"
        
        # Add text/config files with FULL content
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'text' and 'content' in file_data:
                full_path = os.path.join(self.project_path, filepath)
                context += f"\n{'='*60}\nFILE: {filepath} (Text/Config - {file_data.get('line_count', 0)} lines)\nFULL PATH: {full_path}\n{'='*60}\n"
                context += file_data['content']  # FULL CONTENT
                context += "\n\n"
        
        # Report skipped files
        skipped = [f for f, d in self.all_files_content.items() if d.get('type') == 'skipped']
        if skipped:
            context += f"\nSKIPPED FILES (too large):\n"
            for filepath in skipped:
                context += f"- {filepath}: {self.all_files_content[filepath].get('reason', 'Unknown reason')}\n"

        return context