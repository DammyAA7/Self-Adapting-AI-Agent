"""
Simple file analyzer for reading and providing full project context to LLM.
For research purposes - gives LLM complete visibility without filtering.
Enhanced with Tree-sitter for two-phase context management.
"""

import os
import json
import ast
from typing import Dict, Any, List

# Tree-sitter imports for robust code parsing
try:
    from tree_sitter import Language, Parser
    import tree_sitter_python as tspython
    TREE_SITTER_AVAILABLE = True
except ImportError:
    TREE_SITTER_AVAILABLE = False
    print("Warning: tree-sitter not available. Install with: pip install tree-sitter tree-sitter-python")

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
        self.folder_structure = None  # Store folder structure explicitly
        self.ignore_dirs = {'.git', '__pycache__', '.venv', 'venv', 'env',
                           'node_modules', '.pytest_cache', '.idea', '.vscode'}
        self.max_file_size = 100000  # 100KB max per file to avoid huge files

        # Initialize Tree-sitter parser for robust code analysis
        if TREE_SITTER_AVAILABLE:
            try:
                # Try newer tree-sitter API (v0.21+)
                self.ts_language = Language(tspython.language())
                self.ts_parser = Parser(self.ts_language)
            except TypeError:
                # Fallback to older API (v0.20)
                self.ts_parser = Parser()
                self.ts_language = Language(tspython.language())
                self.ts_parser.language = self.ts_language  # Property, not method
        else:
            self.ts_parser = None
            self.ts_language = None
        
    def _capture_folder_structure(self):
        """STEP 1: Capture folder structure FIRST (before reading files)"""
        directories = set()
        files = []

        for root, dirs, filenames in os.walk(self.project_path):
            # Remove ignored directories
            dirs[:] = [d for d in dirs if d not in self.ignore_dirs and not d.startswith('.')]

            rel_root = os.path.relpath(root, self.project_path)
            if rel_root != '.':
                directories.add(rel_root)

            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), self.project_path)
                file_type = 'python' if filename.endswith('.py') else \
                           'csv' if filename.endswith('.csv') else \
                           'json' if filename.endswith('.json') else 'other'

                files.append({
                    'path': rel_path,
                    'name': filename,
                    'type': file_type,
                    'is_init': filename == '__init__.py'
                })

        self.folder_structure = {
            'directories': sorted(list(directories)),
            'files': files,
            'root': os.path.basename(self.project_path)
        }

    def read_all_files(self) -> Dict[str, Any]:
        """
        Read all relevant files in the project without filtering.
        STEP 1: Capture folder structure FIRST (mandatory)
        STEP 2: Then read file contents
        """
        # STEP 1: ALWAYS capture folder structure first
        self._capture_folder_structure()
        print(f"✓ Folder structure captured: {len(self.folder_structure.get('files', []))} files, {len(self.folder_structure.get('directories', []))} directories")

        # STEP 2: Read file contents
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

                            # Use Tree-sitter for parsing (returns functions + parsed tree)
                            functions, parsed_tree = self._extract_functions_with_treesitter(content)

                            self.all_files_content[relative_path] = {
                                'type': 'python',
                                'content': content,  # FULL CONTENT
                                'line_count': len(content.splitlines()),
                                'functions': functions,  # From Tree-sitter
                                'classes': self._extract_classes(content),  # Still use AST for classes
                                'tree': parsed_tree  # Store Tree-sitter tree for Phase 2
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
    
    def _extract_functions_with_treesitter(self, python_code: str) -> tuple:
        """Extract function metadata using Tree-sitter with class context detection"""
        functions = []
        tree = None

        if not self.ts_parser:
            # Fallback to AST if tree-sitter not available
            return self._extract_functions(python_code), None

        try:
            # Parse with Tree-sitter
            tree = self.ts_parser.parse(bytes(python_code, 'utf-8'))

            # First: Extract class methods with Tree-sitter query
            class_query = self.ts_language.query("""
                (class_definition
                  name: (identifier) @class_name
                  body: (block
                    (decorated_definition
                      (decorator)* @decorators
                      definition: (function_definition
                        name: (identifier) @method_name
                        parameters: (parameters) @params
                      ) @method
                    )
                    (function_definition
                      name: (identifier) @method_name
                      parameters: (parameters) @params
                    ) @method
                  )
                ) @class
            """)

            class_methods = {}  # Map method_name -> class_name
            class_captures = class_query.captures(tree.root_node)

            for node, tag in class_captures:
                if tag == 'class_name':
                    current_class = node.text.decode('utf-8')
                elif tag == 'method':
                    method_name_node = node.child_by_field_name('name')
                    if method_name_node:
                        method_name = method_name_node.text.decode('utf-8')
                        class_methods[method_name] = current_class

            # Second: Extract all functions (standalone + methods)
            func_query = self.ts_language.query("""
                (function_definition
                  name: (identifier) @func_name
                  parameters: (parameters) @params
                ) @function
            """)

            func_captures = func_query.captures(tree.root_node)
            processed = set()

            for node, tag in func_captures:
                if tag == 'function':
                    name_node = node.child_by_field_name('name')
                    if not name_node:
                        continue

                    func_name = name_node.text.decode('utf-8')

                    # Avoid duplicates
                    if func_name in processed:
                        continue
                    processed.add(func_name)

                    # Get parameters
                    params_node = node.child_by_field_name('parameters')
                    args = self._parse_params_treesitter(params_node) if params_node else []

                    # Get docstring
                    docstring = self._extract_docstring_treesitter(node)

                    # Check if decorators exist (for @staticmethod, @classmethod detection)
                    parent = node.parent
                    is_static = False
                    is_classmethod = False
                    if parent and parent.type == 'decorated_definition':
                        for child in parent.children:
                            if child.type == 'decorator':
                                decorator_text = child.text.decode('utf-8')
                                if 'staticmethod' in decorator_text:
                                    is_static = True
                                elif 'classmethod' in decorator_text:
                                    is_classmethod = True

                    # Determine if this is a class method
                    class_name = class_methods.get(func_name)

                    functions.append({
                        'name': func_name,
                        'args': args,
                        'docstring': docstring,
                        'start_line': node.start_point[0] + 1,
                        'end_line': node.end_point[0] + 1,
                        'start_byte': node.start_byte,
                        'end_byte': node.end_byte,
                        'is_method': class_name is not None,
                        'class_name': class_name,
                        'is_static': is_static,
                        'is_classmethod': is_classmethod
                    })

        except Exception as e:
            # Fallback to AST on tree-sitter failure
            print(f"Tree-sitter parsing failed, using AST fallback: {e}")
            return self._extract_functions(python_code), None

        return functions, tree

    def _parse_params_treesitter(self, params_node) -> list:
        """Extract parameter names from Tree-sitter parameters node"""
        params = []
        if not params_node:
            return params

        for child in params_node.named_children:
            if child.type == 'identifier':
                params.append(child.text.decode('utf-8'))
            elif child.type in ['typed_parameter', 'default_parameter', 'typed_default_parameter']:
                # Get the name field
                name_node = child.child_by_field_name('name')
                if name_node:
                    params.append(name_node.text.decode('utf-8'))

        return params

    def _extract_docstring_treesitter(self, func_node) -> str:
        """Extract docstring from function using Tree-sitter"""
        body_node = func_node.child_by_field_name('body')
        if not body_node or len(body_node.named_children) == 0:
            return None

        first_stmt = body_node.named_children[0]
        if first_stmt.type == 'expression_statement':
            if len(first_stmt.named_children) > 0:
                expr = first_stmt.named_children[0]
                if expr.type == 'string':
                    docstring = expr.text.decode('utf-8')
                    # Remove triple quotes
                    return docstring.strip('"""').strip("'''").strip()

        return None

    def _extract_functions(self, python_code: str) -> list:
        """Extract function names and signatures from Python code using AST (fallback)"""
        functions = []
        try:
            tree = ast.parse(python_code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append({
                        'name': node.name,
                        'args': args,
                        'docstring': ast.get_docstring(node),
                        'start_line': node.lineno,
                        'end_line': node.end_lineno
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
    
    def _generate_folder_tree(self) -> str:
        """Generate a tree structure view from captured folder structure"""
        if not self.folder_structure:
            return "Folder structure not available\n"

        tree_lines = ["PROJECT FOLDER STRUCTURE:", "=" * 60]
        tree_lines.append(f"{self.folder_structure['root']}/")

        files_list = sorted(self.folder_structure['files'], key=lambda x: x['path'])
        dirs_shown = set()

        for file_info in files_list:
            parts = file_info['path'].split(os.sep)

            # Show directory headers
            if len(parts) > 1:
                dir_path = os.sep.join(parts[:-1])
                if dir_path not in dirs_shown:
                    dirs_shown.add(dir_path)
                    indent = "│   " * (len(parts) - 2)
                    tree_lines.append(f"{indent}├── [DIR]  {parts[-2]}/")

            # Marker based on type
            if file_info['is_init']:
                marker = '[INIT]'
            elif file_info['type'] == 'python':
                marker = '[PY]  '
            elif file_info['type'] == 'csv':
                marker = '[CSV] '
            elif file_info['type'] == 'json':
                marker = '[JSON]'
            else:
                marker = '[FILE]'

            # Indentation based on depth
            indent = "│   " * (len(parts) - 1) if len(parts) > 1 else ""
            tree_lines.append(f"{indent}├── {marker} {file_info['name']}")

        tree_lines.append("=" * 60)
        tree_lines.append("\n[INIT] = __init__.py (usually just imports - LLM should SKIP selecting these)")
        tree_lines.append("[PY]   = Python module files (select these for functions)")
        tree_lines.append("[CSV]  = Data files")
        tree_lines.append("[JSON] = Config files\n")
        return '\n'.join(tree_lines)

    def format_context_for_llm_phase1(self) -> str:
        """
        Phase 1: Format ONLY function signatures and metadata (lightweight).
        LLM uses this to semantically select which functions it needs full code for.
        """
        summary = self.get_project_summary()

        context = f"""PROJECT ANALYSIS - PHASE 1 (Metadata Only)
========================
Project Path: {summary['project_path']}
Total Files: {summary['total_files']}
Total Functions: {summary['total_functions']}
Total Classes: {summary['total_classes']}

{self._generate_folder_tree()}

AVAILABLE FUNCTIONS (Signatures + Docstrings Only):
"""

        # Add function signatures from all Python files
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'python' and 'functions' in file_data:
                if file_data['functions']:
                    context += f"\n{'='*60}\nFILE: {filepath}\n{'='*60}\n"

                    for func in file_data['functions']:
                        args_str = ', '.join(func['args'])

                        # Show if it's a class method
                        if func.get('is_method') and func.get('class_name'):
                            if func.get('is_static'):
                                context += f"\nStatic Method: {func['class_name']}.{func['name']}({args_str})\n"
                                context += f"  Usage: {func['class_name']}.{func['name']}(...)  # Call on class\n"
                            elif func.get('is_classmethod'):
                                context += f"\nClass Method: {func['class_name']}.{func['name']}({args_str})\n"
                                context += f"  Usage: {func['class_name']}.{func['name']}(...)  # Call on class\n"
                            else:
                                context += f"\nInstance Method: {func['class_name']}.{func['name']}({args_str})\n"
                                context += f"  Usage: instance.{func['name']}(...)  # Call on instance\n"
                        else:
                            context += f"\nStandalone Function: {func['name']}({args_str})\n"

                        if func.get('start_line') and func.get('end_line'):
                            context += f"  Location: Lines {func['start_line']}-{func['end_line']}\n"
                        if func.get('docstring'):
                            doc = func['docstring'][:100] + "..." if len(func.get('docstring', '')) > 100 else func.get('docstring', '')
                            context += f"  Description: {doc}\n"

        # Add class summaries (metadata only)
        context += "\n" + "="*60 + "\nCLASSES:\n" + "="*60 + "\n"
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'python' and 'classes' in file_data:
                if file_data['classes']:
                    for cls in file_data['classes']:
                        methods_str = ', '.join(cls.get('methods', []))
                        context += f"\n{filepath}: Class {cls['name']}\n  Methods: {methods_str}\n"

        # Add data file summaries (structure only, not content)
        context += "\n" + "="*60 + "\nDATA FILES:\n" + "="*60 + "\n"
        for filepath, file_data in self.all_files_content.items():
            if file_data.get('type') == 'csv':
                full_path = os.path.join(self.project_path, filepath)
                context += f"\nCSV: {filepath}\n"
                context += f"  Full Path: {full_path}\n"
                context += f"  Headers: {file_data.get('headers', 'Unknown')}\n"
                context += f"  Rows: {file_data.get('line_count', 0) - 1}\n"
            elif file_data.get('type') == 'json':
                full_path = os.path.join(self.project_path, filepath)
                context += f"\nJSON: {filepath}\n"
                context += f"  Full Path: {full_path}\n"
                context += f"  Structure: {file_data.get('structure', 'Unknown')}\n"

        # Add CRITICAL import instructions (MUST be included for correct imports)
        path_parts = self.project_path.split(os.sep)
        analyzed_dir_name = os.path.basename(self.project_path)

        # Find if 'dataset' or 'datasets' in path
        for i, part in enumerate(path_parts):
            if part in ['dataset', 'datasets']:
                analyzed_dir_name = '.'.join(path_parts[i:])
                break

        context += f"""

{'='*60}
CRITICAL IMPORT INSTRUCTIONS:
{'='*60}

For CLASSES (to access instance/class/static methods):
```python
from {analyzed_dir_name}.hospital import Hospital
from {analyzed_dir_name}.patient import Patient
```

For STATIC METHODS (shown as "Static Method: ClassName.method_name"):
```python
from {analyzed_dir_name}.salary_analyzer_class import SalaryAnalyzer
# Then call: SalaryAnalyzer.calculate_average_salary(data)
```

For STANDALONE FUNCTIONS:
```python
from {analyzed_dir_name}.utilities import helper_function
```

WRONG PATTERNS (Do NOT use):
❌ from hospital import Hospital  # Missing module path!
❌ from dataset.XYZ import Hospital  # Don't use placeholders!
❌ from salary_analyzer_class import calculate_average_salary  # It's a class method, not standalone!

The function being tested comes from:
```python
from unit_test.functions import your_function_name
```
"""

        return context

    def extract_selected_functions(self, selections: List[Dict[str, str]]) -> str:
        """
        Phase 2: Extract FULL implementations of selected functions using Tree-sitter.
        This is where Tree-sitter's precision extraction is used.
        """
        if not selections:
            return ""

        context = "\n" + "="*60 + "\n"
        context += "PHASE 2: SELECTED FUNCTION IMPLEMENTATIONS\n"
        context += "(Full code for functions selected by LLM)\n"
        context += "="*60 + "\n\n"

        for selection in selections:
            filepath = selection.get('filepath')
            func_name = selection.get('function_name')

            if not filepath or not func_name:
                continue

            # Try exact match first
            file_data = self.all_files_content.get(filepath)

            # If not found, try matching by basename (LLM might include dataset prefix)
            if not file_data:
                basename = os.path.basename(filepath)
                for key in self.all_files_content.keys():
                    if os.path.basename(key) == basename or key.endswith(filepath):
                        file_data = self.all_files_content[key]
                        filepath = key  # Use actual dict key
                        print(f"  → Matched '{selection.get('filepath')}' to '{key}'")
                        break

            if not file_data or file_data.get('type') != 'python':
                print(f"⚠ Warning: Could not find file '{filepath}' for function '{func_name}'")
                continue

            # Try Tree-sitter extraction first (most precise)
            extracted_code = None
            if file_data.get('tree') and self.ts_parser:
                extracted_code = self._extract_function_with_treesitter(
                    file_data['tree'], file_data['content'], func_name
                )

            # Fallback to line-based extraction
            if not extracted_code:
                extracted_code = self._extract_function_by_lines(
                    file_data['content'], func_name, file_data.get('functions', [])
                )

            if extracted_code:
                context += f"\n{'─'*60}\n"
                context += f"FILE: {filepath}\n"
                context += f"FUNCTION: {func_name}()\n"
                if 'reasoning' in selection:
                    context += f"WHY SELECTED: {selection['reasoning']}\n"
                context += f"{'─'*60}\n"
                context += extracted_code + "\n\n"

        return context

    def _extract_function_with_treesitter(self, tree, content: str, function_name: str) -> str:
        """Extract function code using Tree-sitter tree (Phase 2 - precise extraction)"""
        try:
            query = self.ts_language.query("""
                (function_definition
                  name: (identifier) @func_name
                ) @function
            """)

            captures = query.captures(tree.root_node)
            for node, tag in captures:
                if tag == 'function':
                    name_node = node.child_by_field_name('name')
                    if name_node and name_node.text.decode('utf-8') == function_name:
                        # Extract using Tree-sitter byte offsets (most precise)
                        return content[node.start_byte:node.end_byte]

        except Exception as e:
            print(f"Tree-sitter extraction failed for {function_name}: {e}")

        return None

    def _extract_function_by_lines(self, content: str, function_name: str, functions: list) -> str:
        """Fallback: Extract function by line numbers (if tree-sitter fails)"""
        for func in functions:
            if func['name'] == function_name:
                lines = content.splitlines()
                start = func.get('start_line', 1) - 1
                end = func.get('end_line', len(lines))
                return '\n'.join(lines[start:end])
        return None

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

CORRECT IMPORT PATTERN:
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unit_test.functions import *  # The function being tested comes from here
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
        print(context)

        return context