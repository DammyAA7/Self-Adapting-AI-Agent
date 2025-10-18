# SelfEvolve: An Agentic Architecture for Runtime Code Generation

## Paper Abstract
Traditional self-adaptive systems automatically reconfigure existing components in response to changing requirements, but provide limited support for the generation of novel functionalities. The software generation capabilities of large language models (LLMs) open the possibility to create entirely new modules at runtime, enabling a form of self-evolution beyond traditional self-adaptation. We present SelfEvolve, an orchestrated pipeline architecture enabling runtime self-evolution through iterative code generation based on automatic test-driven development. Evaluation demonstrates 92.7% average Pass@1 (51/55) across 11 diverse self-evolution problems spanning integration, compositional, and data processing tasks.

## Repository Structure

```
Self-Adapting-AI-Agent/
├── framework/                       # Main implementation of SelfEvolve
│   ├── core/                       # Entry point and orchestration (main.py)
│   ├── adjudicator/               # Final adjudication component
│   ├── intermediate_adjudicator/  # TDD validation component
│   ├── function_gen/              # Function synthesis component
│   ├── test_driven_development/   # TDD test generation
│   ├── unit_test/                 # Unit test generation
│   ├── terminal_context/          # Session persistence for compositional tasks
│   ├── file_analyzer/             # Codebase analysis for integration tasks
│   └── evaluation/                # Evaluation runner and metrics
│
├── dataset/                        # 11 self-evolution problems
│   ├── Integration Tasks (4 problems)
│   ├── Compositional Tasks (3 problems)
│   └── Data Processing Tasks (4 problems)
│
└── evaluations/                    # Experimental results and logs
```

## Installation

```bash
# Clone repository
git clone [repository-url]
cd Self-Adapting-AI-Agent

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: AZURE_OPENAI_API_KEY=your_key_here
```

## Dataset Overview

The evaluation dataset comprises 11 problems across three task categories as described in the paper (Table 1):

### Task Categories

| Category | Problems | Characteristics |
|----------|----------|-----------------|
| **Integration** | 4 | Multi-file codebases (577-783 LOC, 7-20 classes) requiring analysis and interfacing with existing class hierarchies |
| **Compositional** | 3 | Cross-session tasks where Session 2 functions build upon Session 1 capabilities |
| **Data Processing** | 4 | External dataset manipulation (50-100 records) with filtering, aggregation, and recommendation operations |

### Problem Details

| ID | Problem Name | Domain | Task Type | Size |
|----|-------------|--------|-----------|------|
| 1 | Salary Analyzer | HR Analytics | Integration | 616 LOC, 12 classes |
| 2 | Patient Risk Analyzer | Healthcare | Integration | 752 LOC, 20 classes |
| 3 | Student GPA Calculator | Education | Integration | 783 LOC, 10 classes |
| 4 | Inventory Low Stock Alert | E-Commerce | Integration | 577 LOC, 7 classes |
| 5 | Matrix Eigenvalue | Linear Algebra | Compositional | 40-50 LOC |
| 6 | Portfolio Risk | Finance | Compositional | 30-40 LOC |
| 7 | IoT Sensor Pipeline | IoT Systems | Compositional | 40-50 LOC |
| 8 | Movie API | Media Systems | Data Processing | 100 records |
| 9 | Book Recommender | Content Rec. | Data Processing | 100 records |
| 10 | Performance Tracker | HR Analytics | Data Processing | 50 records |
| 11 | Friend Suggester | Social Network | Data Processing | 100 users |

## Reproducing Paper Results

### Integration and Data Processing Tasks (IDs: 1-4, 8-11)

Each problem contains a `problem.json` file with the specific prompt to use:

```bash
cd framework

# General format for Integration and Data Processing tasks:
python core/main.py --analyze ../dataset/[problem_directory] \
  --request "[prompt from dataset/[problem_directory]/problem.json]"

# Example for Problem ID 4 (Inventory Low Stock Alert):
# 1. Read the prompt from dataset/inventory_replenishment/problem.json
# 2. Run the framework:
python core/main.py --analyze ../dataset/inventory_replenishment \
  --request "[use prompt field from problem.json]"

# 3. Verify result:
python evaluation/self_evolution_test_runner.py --id 4
```

### Compositional Tasks (IDs: 5-7)

These require two sessions to demonstrate cross-session composition. Each problem's `problem.json` contains both `session_1` and `session_2` prompts:

```bash
cd framework

# Example for Problem ID 7 (IoT Sensor Pipeline):

# Step 1: Read prompts from dataset/iot_sensor_pipeline/problem.json
# - session_1.prompt: Create parse_sensor_reading function
# - session_2.prompt: Create aggregate_temperature function using parse_sensor_reading

# Step 2: Session 1 - Create base function
python core/main.py --clean-all \
  --request "Create a function called parse_sensor_reading that takes a string like 'T:25.5|H:60|TS:1234567890'. Split by '|' to get parts. For each part, split by ':' to get key and value. Return dict with 'temperature', 'humidity', 'timestamp' keys. If a value cannot be converted to float/int, set to None. Handle T as float, H as float, TS as int."

# Step 3: Session 2 - Build upon previous function
python core/main.py --context-memory
# When prompted to select a session, choose the one with parse_sensor_reading
# Then enter the session_2 prompt:
# "Load previous session and create aggregate_temperature function. Takes a list of raw sensor strings. Use parse_sensor_reading to parse each one. Collect all temperature values that are not None. Return average of all temperatures rounded to 2 decimals. Return 0.0 if no valid temperatures."

# Step 4: Verify result
python evaluation/self_evolution_test_runner.py --id 7
```

### Running Individual Problems

To run any specific problem from the evaluation suite:

```bash
cd framework

# List all available problems
python evaluation/self_evolution_test_runner.py --list

# Run specific problem by ID (1-11)
python evaluation/self_evolution_test_runner.py --id [1-11]
```

## Key Components (Architecture Section 2.1)

| Component | File | Description |
|-----------|------|-------------|
| **Chat & Tool Dispatcher** | `framework/core/main.py` | Entry point, determines if existing tools suffice |
| **Test-Driven Code Generator** | `framework/test_driven_development/generator.py` | Generates TDD test cases |
| **Function Generator** | `framework/function_gen/generator.py` | Synthesizes function code |
| **Intermediate Adjudicator** | `framework/intermediate_adjudicator/adjudicator.py` | Validates against TDD tests |
| **Unit Test Generator** | `framework/unit_test/generator.py` | Generates comprehensive test suite |
| **Final Adjudicator** | `framework/adjudicator/adjudicator.py` | Final validation |
| **Terminal Context** | `framework/terminal_context/context_manager.py` | Maintains cross-session state |

## Experimental Configuration

- **Model**: GPT-4.1 (selected for OpenAI function-calling protocol support)
- **Iterations**: Maximum n=6 per problem
- **Runs**: 5 independent runs per problem
- **Metrics**: Pass@1 (binary success), Average Iterations (convergence efficiency)
- **Statistical Analysis**: Wilcoxon signed-rank test (p<0.001, r=0.98)

## Output Files

Each run generates two output files:
- `function_generation.log` - Detailed execution logs including iterations, adjudication results, and error messages
- `function_generation_stats.json` - Performance metrics including timing, iteration counts, and success/failure status

## Problem Specification Format

Each problem in the `dataset/` directory contains:
- `problem.json` - Problem specification including ID, prompt(s), test code, and domain
- Supporting Python files for integration tasks (e.g., class definitions, data structures)
- CSV/JSON data files for data processing tasks

For compositional tasks, `problem.json` contains `session_1` and `session_2` objects with separate prompts for each session.

## Paper Reproducibility

This repository accompanies the paper submission. The implementation demonstrates:

1. **Runtime self-evolution** through autonomous code generation during execution
2. **Test-driven development** reducing iterations by 2.1x (2.2 vs 4.7)
3. **Dual adjudication** achieving 92.7% success rate across diverse tasks
4. **Cross-session composition** enabling incremental capability building

All experimental results reported in the paper can be reproduced using the commands provided above. Each problem can be executed independently, and the evaluation runner verifies correctness against predefined test specifications.
