# Self-Adapting AI Agent Framework
## "Self-evolving Systems: a Runtime Architecture for Autonomous Code Generation"

This repository contains the refactored and optimized implementation of our self-adapting AI agent framework for ICSE '26 paper submission.

---

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add your OpenAI/Azure API key
```

### 2. Install Package (Optional)

```bash
# Install as editable package
pip install -e .
```

---

## Repository Structure

```
Self-Adapting-AI-Agent/
├── framework/                     # Main framework implementation
│   ├── adjudicator/              # Final adjudication logic
│   ├── core/                     # Main entry point (main.py)
│   ├── evaluation/               # Benchmark evaluation scripts
│   ├── file_analyzer/            # Codebase analysis
│   ├── function_gen/             # Function generation
│   ├── intermediate_adjudicator/ # Test-driven validation
│   ├── prompt_gen/               # Prompt generation
│   ├── terminal_context/         # Session memory management
│   ├── test_driven_development/  # TDD code generator
│   ├── tool_descriptor_gen/      # Tool definition generator
│   ├── unit_test/                # Unit test generation
│   └── utilities/                # Helper functions
│
├── dataset/                      # Test datasets (11 problems)
│   ├── patient_risk_analyzer/   # Healthcare (752 LOC, 20 classes)
│   ├── student_gpa_calculator/  # Education (783 LOC, 10 classes)
│   ├── salary_analyzer/         # HR Analytics (616 LOC, 12 classes)
│   ├── inventory_replenishment/ # E-commerce (577 LOC, 7 classes)
│   ├── book_recommender/        # Media (CSV data)
│   ├── friend_suggester/        # Social network (JSON data)
│   ├── movielens_dataset/       # Movies (CSV data)
│   ├── performance_tracker/     # HR (CSV data)
│   ├── iot_sensor_pipeline/     # IoT (cross-session)
│   ├── matrix_eigenvalue_composition/  # Math (cross-session)
│   └── portfolio_risk_calculator/      # Finance (cross-session)
│
├── outputs/                      # Generated outputs (gitignored)
│   ├── logs/                     # Execution logs
│   ├── stats/                    # Performance statistics
│   ├── results/                  # Pass@k results
│   └── sessions/                 # Context sessions
│
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Package configuration
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── COMPREHENSIVE_DATASET_ANALYSIS.md  # Detailed dataset documentation
```

---

## Architecture Components

The framework implements a self-adapting AI agent with Test-Driven Development and dual adjudication:

| Component | File | Description |
|-----------|------|-------------|
| **Chat & Tool Dispatcher** | `framework/core/main.py` | Main entry point and orchestration |
| **Test-Driven Generator** | `framework/test_driven_development/generator.py` | TDD test generation |
| **Function Generator** | `framework/function_gen/generator.py` | Function code generation |
| **Intermediate Adjudicator** | `framework/intermediate_adjudicator/adjudicator.py` | TDD validation |
| **Unit Test Generator** | `framework/unit_test/generator.py` | Unit test generation |
| **Final Adjudicator** | `framework/adjudicator/adjudicator.py` | Final validation |
| **Terminal Context** | `framework/terminal_context/context_manager.py` | Session persistence |
| **File Analyzer** | `framework/file_analyzer/analyzer.py` | Codebase analysis |

---

## Dataset Overview

### 11 Problems Across 9 Domains

For detailed analysis, see [COMPREHENSIVE_DATASET_ANALYSIS.md](COMPREHENSIVE_DATASET_ANALYSIS.md)

| # | Dataset | Domain | LOC | Classes | Tokens | Type |
|---|---------|--------|-----|---------|--------|------|
| 1 | patient_risk_analyzer | Healthcare | 752 | 20 | 6,797 | Code-Heavy |
| 2 | student_gpa_calculator | Education | 783 | 10 | 7,120 | Code-Heavy |
| 3 | salary_analyzer | HR Analytics | 616 | 12 | 5,314 | Code-Heavy |
| 4 | inventory_replenishment | E-commerce | 577 | 7 | 5,862 | Code-Heavy |
| 5 | book_recommender | Media | 119 | 0 | 2,221 | Data-Only |
| 6 | friend_suggester | Social Network | 2,917 | 0 | 14,009 | Data-Only |
| 7 | movielens_dataset | Media | 119 | 0 | 1,650 | Data-Only |
| 8 | performance_tracker | HR Analytics | 69 | 0 | 1,922 | Data-Only |
| 9 | iot_sensor_pipeline | IoT | 23 | 0 | 492 | Cross-Session |
| 10 | matrix_eigenvalue_composition | Mathematics | 23 | 0 | 323 | Cross-Session |
| 11 | portfolio_risk_calculator | Finance | 23 | 0 | 498 | Cross-Session |

**Total:** 6,076 lines, 49 classes, 46,208 tokens (36% of o4-mini's 128K context)

---

## Running the Framework

### Basic Usage

```bash
cd framework

# Generate a function with codebase analysis
python core/main.py --clean-all --analyze ../dataset/patient_risk_analyzer --request "Create a function called patient_risk_score that calculates patient risk scores"

# Cross-session composition (load previous function)
python core/main.py --context-memory
```

### Example: Patient Risk Analyzer

```bash
cd framework

python core/main.py --clean-all --analyze ../dataset/patient_risk_analyzer --request "Create a function called patient_risk_score that takes a Hospital object and patient_id. Calculate risk score using formula: (patient.age / 100 * 30) + (patient.get_total_conditions() * 5 * 25/100) + (patient.get_average_severity() * 10 * 25/100) + (20 if recent records have abnormal vitals else 0). Use hospital.get_patient(patient_id) and hospital.get_recent_records(patient_id, 90). Returns: float between 0.0 and 100.0."
```

### Example: Student GPA Calculator

```bash
cd framework

python core/main.py --clean-all --analyze ../dataset/student_gpa_calculator --request "Create a function called calculate_simple_gpa that takes a University object and student_id. For each enrollment from university.get_student_enrollments(student_id), get the course using university.get_course(enrollment.course_code), multiply enrollment.get_grade_points() by course.credits, sum all points and credits, return total_points / total_credits as GPA (0.0-4.0)."
```

### Running All Tests

```bash
cd framework

# Run specific test by ID
python evaluation/self_evolution_test_runner.py --id 2

# List all available tests
python evaluation/self_evolution_test_runner.py --list

# Run all tests
python evaluation/self_evolution_test_runner.py --all
```

---

## Key Features

### 1. **Test-Driven Development Pipeline**
- Generates TDD tests before implementation
- Iterative refinement based on test feedback
- Reduces iteration count significantly

### 2. **Dual Adjudication**
- Intermediate adjudication validates TDD tests
- Final adjudication validates complete solution
- Ensures high-quality code generation

### 3. **Terminal Context (Cross-Session Memory)**
- Saves generated functions across sessions
- Enables function composition and reuse
- Supports incremental capability building

### 4. **Codebase Analysis**
- Automatically analyzes unknown codebases
- Discovers classes, methods, and APIs
- Generates correct import paths

### 5. **Smart Import Resolution**
- Detects dataset/ directory structure
- Generates proper import paths (e.g., `from dataset.patient_risk_analyzer import Hospital`)
- Handles nested package structures

---

## Output Files

All generated outputs are stored in `outputs/` directory:

```
outputs/
├── logs/
│   └── function_generation.log         # Detailed execution logs
├── stats/
│   └── function_generation_stats.json  # Performance metrics
├── results/
│   └── pass_k_dual_results_*.json     # Evaluation results
└── sessions/
    └── context_sessions/*.json         # Saved function contexts
```

---

## Framework Architecture

### Pipeline Flow

```
User Request
    ↓
File Analyzer (analyzes codebase)
    ↓
TDD Test Generator (generates test cases)
    ↓
Intermediate Adjudicator (validates TDD tests)
    ↓
Function Generator (generates implementation)
    ↓
Unit Test Generator (generates unit tests)
    ↓
Final Adjudicator (validates complete solution)
    ↓
Success or Iterate
```

### Key Design Decisions

**1. Snake_Case Convention:**
All framework directories use Python's snake_case convention for better code quality.

**2. Modular Datasets:**
Each dataset class is in its own file, exported via `__init__.py` with `__all__` for clean public API.

**3. Project Root in sys.path:**
Test files include project root in sys.path to enable `from dataset.*` imports.

**4. Pytest Configuration:**
Custom pytest config to discover framework test files (`testDrivenCases.py`, `unitTest.py`).

---

## Dataset Structure

All datasets follow clean Python package structure:

```python
# Each dataset has __init__.py with exports
from .model1 import *
from .model2 import *

__all__ = ['Class1', 'Class2', 'helper_function']
```

### Code-Heavy Datasets (4)

**patient_risk_analyzer/** - Healthcare system with 20 classes:
- Core: Patient, Condition, MedicalRecord, Hospital
- Helpers: Medication management, vital signs, appointments, insurance, lab results, diagnosis, treatment

**student_gpa_calculator/** - Education system with 10 classes:
- Core: Student, Course, Enrollment, Department, University
- Helpers: Grade calculator, transcript generator, prerequisites, scholarships

**salary_analyzer/** - HR analytics with 12 classes:
- Data processing, employee database, ML utilities, web crawler components

**inventory_replenishment/** - E-commerce with 7 classes:
- Warehouse management, stock tracking, demand forecasting, order optimization

### Data-Only Datasets (4)

- **book_recommender/** - 100 books (CSV)
- **friend_suggester/** - 100 users, social graph (JSON)
- **movielens_dataset/** - 100 movies (CSV)
- **performance_tracker/** - 50 employee reviews (CSV)

### Cross-Session Datasets (3)

- **iot_sensor_pipeline/** - String parsing → aggregation
- **matrix_eigenvalue_composition/** - Matrix ops → eigenvalues
- **portfolio_risk_calculator/** - Stock volatility → portfolio risk

---

## Important Files & Locations

### Generated Outputs
- **Logs:** `outputs/logs/function_generation.log`
- **Stats:** `outputs/stats/function_generation_stats.json`
- **Results:** `outputs/results/pass_k_dual_results_*.json`
- **Sessions:** `outputs/sessions/context_sessions/*.json`

### Framework Components
- **Main Entry:** `framework/core/main.py`
- **Evaluator:** `framework/evaluation/self_evolution_test_runner.py`
- **Test Suite:** `framework/SELF_EVOLUTION_TEST_SUITE.json`

### Documentation
- **Dataset Analysis:** `COMPREHENSIVE_DATASET_ANALYSIS.md` (1,263 lines)
- **Problem Definitions:** `dataset/*/problem.json` (11 files)

---

## Paper Results (Legacy Paths)

**Note:** The paper experiments used the old structure. For new experiments, use the refactored `framework/` directory.

### Legacy Structure (Paper Experiments)
```
framework_our_approach/
├── architecture_designed_for_ticoder_comparison/  # Table 1
└── ablation_study_gcp_calculation/                # Table 2
```

**For reproducing paper results, refer to the original paths in the paper. For new work, use the refactored structure.**

---

## Refactoring Improvements

This codebase has been comprehensively refactored for production quality:

### ✅ Completed Improvements

1. **Directory Structure**
   - Renamed to snake_case (PascalCase → snake_case)
   - Fixed typo: Intermidiate → Intermediate
   - Simplified paths: framework/ instead of framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/

2. **Code Organization**
   - 49 classes split into individual files
   - Each class in its own module
   - Clean `__init__.py` with `__all__` exports

3. **Import Paths**
   - Updated 70+ import statements
   - Fixed 17+ hardcoded file paths
   - Added dataset/ parent detection in file analyzer

4. **Test Infrastructure**
   - Updated TDD and Unit test prompts
   - Added project root to sys.path
   - Fixed pytest configuration for custom test files

5. **Documentation**
   - Created comprehensive dataset analysis
   - Updated README with new structure
   - Added .gitignore and pyproject.toml

6. **Outputs Organization**
   - Moved logs to outputs/logs/
   - Moved stats to outputs/stats/
   - Moved results to outputs/results/
   - Moved sessions to outputs/sessions/

### Dataset Improvements

**Lines of Code Distribution (500-800 target):**
- patient_risk_analyzer: 752 lines ✅
- student_gpa_calculator: 783 lines ✅
- salary_analyzer: 616 lines ✅
- inventory_replenishment: 577 lines ✅

**Token Usage:** 46,208 tokens total (36% of o4-mini's 128K context) ✅

---

## Usage Examples

### Single Function Generation

```bash
cd framework

# Example: Salary analyzer
python core/main.py --clean-all --analyze ../dataset/salary_analyzer --request "Create a function called salary_analyzer that calculates average salary from employee data"
```

### Cross-Session Composition

```bash
cd framework

# Session 1: Create base function
python core/main.py --clean-all --request "Create a function called parse_sensor_reading that takes a string like 'T:25.5|H:60|TS:1234567890' and returns a dict with temperature, humidity, and timestamp"

# Session 2: Build on previous function
python core/main.py --context-memory
# Select the previous session, then enter:
# "Create aggregate_temperature function that uses parse_sensor_reading to calculate average temperature from multiple readings"
```

### Running Evaluations

```bash
cd framework

# Run evaluation for specific problem
python evaluation/self_evolution_test_runner.py --id 2

# Run HumanEval benchmarks
python evaluation/run_dual_pass_k.py --problem "is_equal_to_sum_even_HE_138" --runs 1 --use-humaneval --verbose
```

---

## Command-Line Arguments

### Main Framework (`core/main.py`)

- `--clean-all` - Clear previous functions and tests
- `--analyze <path>` - Analyze codebase at path (e.g., `../dataset/patient_risk_analyzer`)
- `--request "<description>"` - Function generation request
- `--context-memory` - Enable cross-session composition mode

### Evaluation Runner (`evaluation/self_evolution_test_runner.py`)

- `--id <number>` - Run specific test (1-11)
- `--list` - List all available tests
- `--all` - Run all tests sequentially

---

## Key Improvements from Refactoring

### Before → After

| Aspect | Before | After |
|--------|--------|-------|
| Directory names | PascalCase | snake_case ✅ |
| Main path | framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/ | framework/ ✅ |
| Import example | from Adjudicator.adjudicator | from adjudicator.adjudicator ✅ |
| Dataset location | test_context/ (inside framework) | dataset/ (project root) ✅ |
| Dataset imports | from patient_risk_analyzer | from dataset.patient_risk_analyzer ✅ |
| Class organization | Monolithic files (154 lines) | One class per file (avg 62 lines) ✅ |
| Outputs | Scattered in framework/ | Organized in outputs/ ✅ |
| Documentation | Minimal | Comprehensive (1,263 line analysis) ✅ |

---

## Python Package Structure

### Installation

```bash
# Development installation
pip install -e .

# With optional dependencies
pip install -e ".[dev,analysis]"
```

### Dependencies

**Core:**
- openai>=1.0.0
- python-dotenv>=1.0.0
- pydantic>=2.0.0
- psutil>=5.9.0

**Development:**
- pytest>=7.0.0
- black>=23.0.0
- flake8>=6.0.0
- mypy>=1.0.0

**Analysis:**
- matplotlib>=3.7.0
- pandas>=2.0.0
- seaborn>=0.12.0

---

## Testing

### Framework Tests

```bash
# Run pytest on generated tests
python -m pytest framework/test_driven_development/testDrivenCases.py -v
python -m pytest framework/unit_test/unitTest.py -v
```

### Self-Evolution Tests

```bash
cd framework

# Test specific problem
python evaluation/self_evolution_test_runner.py --id 2

# Test all problems
for i in {1..11}; do
    python evaluation/self_evolution_test_runner.py --id $i
done
```

---

## Project Statistics

### Code Metrics

- **Total Python Files:** 48
- **Total Classes:** 49
- **Total Methods:** 195+
- **Total LOC (Python):** 2,685
- **Total Data Lines:** 3,152

### Token Usage (o4-mini context: 128K)

- **Code-Heavy Datasets:** 25,093 tokens (19.6%)
- **Data-Only Datasets:** 19,793 tokens (15.5%)
- **Cross-Session Datasets:** 1,313 tokens (1.0%)
- **Total:** 46,208 tokens (36.1%)
- **Available:** 81,792 tokens (63.9%)

### Domain Coverage

- Healthcare (1), Education (1), HR Analytics (2), E-commerce (1)
- Media (2), Social Networks (1), IoT (1), Mathematics (1), Finance (1)
- **Total: 9 professional domains**

---

## File Organization Best Practices

### Dataset Package Pattern

```python
# dataset/example/__init__.py
"""Package documentation"""

# Import all classes
from .model1 import *
from .model2 import *

# Explicit public API
__all__ = ['Class1', 'Class2', 'function1']
```

### Import Patterns

```python
# In framework code
from dataset.patient_risk_analyzer import Hospital, Patient

# In test code
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dataset.patient_risk_analyzer import Hospital
```

---

## Troubleshooting

### Common Issues

**Issue:** Import error `ModuleNotFoundError: No module named 'dataset'`
**Fix:** Ensure project root is in sys.path:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
```

**Issue:** pytest doesn't discover tests
**Fix:** Verify pyproject.toml has:
```toml
python_files = ["test_*.py", "testDrivenCases.py", "unitTest.py"]
```

**Issue:** Context sessions not found
**Fix:** Verify sessions directory exists: `outputs/sessions/context_sessions/`

---

## Contributing

### Code Style

- **Python:** Follow PEP 8 (snake_case for modules, PascalCase for classes)
- **Type Hints:** Use comprehensive type annotations
- **Docstrings:** Document all classes and public methods
- **Line Length:** 100 characters (configured in pyproject.toml)

### Adding New Datasets

1. Create directory in `dataset/`
2. Add Python classes (one class per file)
3. Create `__init__.py` with exports
4. Add `problem.json` with test specification
5. Update `COMPREHENSIVE_DATASET_ANALYSIS.md`

---

## License

MIT License (see LICENSE file)

---

## Citation

If you use this code, please cite our ICSE '26 paper:

```bibtex
@inproceedings{selfevolving2026,
  title={Self-evolving Systems: a Runtime Architecture for Autonomous Code Generation},
  author={Your Name},
  booktitle={ICSE},
  year={2026}
}
```

---

## Contact

For questions about the framework or reproduction:
- GitHub Issues: [Create an issue](https://github.com/yourusername/self-adapting-ai-agent/issues)
- Email: your.email@example.com

---

**Last Updated:** 2025-10-12
**Framework Version:** 0.1.0 (Refactored)
**Python:** 3.8+ compatible
