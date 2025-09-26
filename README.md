# Code Repository for ICSE '26 Paper
## "Self-evolving Systems: a Runtime Architecture for Autonomous Code Generation"

This repository contains the implementation and experiments for our paper submission.

## Quick Start

1. **Setup Environment:**
```bash
pip install -r requirements.txt
# Add your OpenAI API key to .env file
cp .env.example .env
```

2. **Repository Structure:**
```
self-evolving-systems-icse-submission/
├── framework_our_approach/                          # Full framework (with TDD + Unit Testing)
│   ├── architecture_designed_for_ticoder_comparison/  # Table 1 experiments (TiCoder comparison)
│   ├── ablation_study_gcp_calculation/              # Table 2 GCD experiments
│   └── ablation_study_humaneval_and_long_horizon_tasks/  # Tables 3 & 4 experiments
│
├── framework_w_o_tdd/                              # Ablation variant (without TDD)
│   ├── ablation_study_gcp_calculation/              # Table 2 GCD experiments
│   └── ablation_study_humaneval_and_long_horizon_tasks/  # Tables 3 & 4 experiments
│
├── framework_w_o_unit_test_and_tdd/               # Ablation variant (without both)
│   └── ablation_study_gcp_calculation/              # Table 2 GCD experiments only
│
└── TiCoder-codebase/                              # Microsoft TiCoder baseline (from https://github.com/microsoft/TiCoder)
    ├── individual_problems/                         # Custom JSONL files for our 3 test problems
    │   ├── HumanEval_is_equal_to_sum_even.jsonl
    │   ├── HumanEval_smallest_change.jsonl
    │   └── HumanEval_car_race_collision.jsonl
    ├── src/
    │   └── results/                                # TiCoder output files
    │       ├── global_results..json                # Results for is_equal_to_sum_even
    │       ├── global_results. (1).json            # Results for smallest_change
    │       └── global_results. (2).json            # Results for car_race_collision
    └── RUN_LOGS.md                                 # Terminal execution logs for TiCoder runs
```

## Paper Results → Code Mapping

### Table 1: Comparison with TiCoder (Section 4.1)
**Paper Claims:** Our Framework: 77.8% success, TiCoder: 46.7% success

**Code Location:**
- Our Framework: `framework_our_approach/architecture_designed_for_ticoder_comparison/` (requires OpenAI API Key)
- TiCoder Baseline: `TiCoder-codebase/` (Microsoft's implementation)

**Problems Tested (with HumanEval IDs):**
- `is_equal_to_sum_even_HE_138` - Our: 100%, TiCoder: 40% (2/5 solutions passed)
- `smallest_change_HE_73` - Our: 33%, TiCoder: 80% (4/5 solutions passed)
- `car_race_collision_HE_41` - Our: 100%, TiCoder: 20% (1/5 solutions passed)

**To Reproduce Our Framework:**
```bash
cd framework_our_approach/architecture_designed_for_ticoder_comparison

# Run each problem individually
python evaluation/run_dual_pass_k.py --problem "is_equal_to_sum_even_HE_138" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "smallest_change_HE_73" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "car_race_collision_HE_41" --runs 1 --use-humaneval --verbose

# View results in pass_k_dual_results_*.json files
```

### Table 2: GCD Ablation Study (Section 4.2)
**Paper Claims:** 50% iteration reduction with full framework

**Code Locations:**
- Full Framework (2 iterations): `framework_our_approach/ablation_study_gcp_calculation/`
- Without TDD (3 iterations): `framework_w_o_tdd/ablation_study_gcp_calculation/`
- Without Both (4 iterations): `framework_w_o_unit_test_and_tdd/ablation_study_gcp_calculation/`

**To Reproduce:**
```bash
# Run each variant and observe iteration count
cd framework_our_approach/ablation_study_gcp_calculation
python Core/main.py  # Expected: 2 iterations

cd ../../framework_w_o_tdd/ablation_study_gcp_calculation
python Core/main.py  # Expected: 3 iterations

cd ../../framework_w_o_unit_test_and_tdd/ablation_study_gcp_calculation
python Core/main.py  # Expected: 4 iterations
```

### Table 3: TDD Impact on HumanEval (Section 4.2)
**Paper Claims:** With TDD: 100% Pass@1, Without TDD: 90% Pass@1

**Code Locations:**
- With TDD: `framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/`
- Without TDD: `framework_w_o_tdd/ablation_study_humaneval_and_long_horizon_tasks/`

**10 HumanEval Problems (with IDs):**
- `is_equal_to_sum_even_HE_138`
- `smallest_change_HE_73`
- `decimal_to_binary_HE_79`
- `car_race_collision_HE_41`
- `count_up_to_HE_96`
- `split_words_HE_125`
- `move_one_ball_HE_109` (fails without TDD)
- `match_parens_HE_119`
- `rounded_avg_HE_103`
- `sort_array_HE_88`

**To Reproduce:**
```bash
# With TDD - All 10 problems pass
cd framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks

# Run each problem
python evaluation/run_dual_pass_k.py --problem "is_equal_to_sum_even_HE_138" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "smallest_change_HE_73" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "decimal_to_binary_HE_79" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "car_race_collision_HE_41" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "count_up_to_HE_96" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "split_words_HE_125" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "move_one_ball_HE_109" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "match_parens_HE_119" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "rounded_avg_HE_103" --runs 1 --use-humaneval --verbose
python evaluation/run_dual_pass_k.py --problem "sort_array_HE_88" --runs 1 --use-humaneval --verbose

# Without TDD - 9 pass, move_one_ball fails
cd framework_w_o_tdd/ablation_study_humaneval_and_long_horizon_tasks
# Run same commands as above
```

**Results Files:** Look for `pass_k_dual_results_*.json` files

### Table 4: Long-Horizon Tasks (Section 4.3)
**Paper Claims:**
- Salary Analyzer: Success in 2 iterations with TDD (168s), Failed without TDD (179s)
- Matrix Eigenvalue: Success in 1 iteration with TDD (125s), Failed without TDD (169s)

**Code Locations:**
- With TDD: `framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks/` (Prototype-IV)
- Without TDD: `framework_w_o_tdd/ablation_study_humaneval_and_long_horizon_tasks/` (Prototype-III)

**Key Components:**
- `Terminal_Context/` - Persistent memory across sessions
- `test_context/` - 597-line codebase for Salary Analyzer task
- `context_sessions/*.json` - Saved function compositions

#### To Reproduce Salary Analyzer Task:

**Without TDD (Expected: Failure after 6 iterations, ~179s):**
```bash
cd framework_w_o_tdd/ablation_study_humaneval_and_long_horizon_tasks

python Core/main.py --clean-all --analyze test_context --request "Create a function called salary_analyzer that calculates average salary from employee data"
```

**With TDD (Expected: Success after 2 iterations, ~168s):**
```bash
cd framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks

python Core/main.py --clean-all --analyze test_context --request "Create a function called salary_analyzer that calculates average salary from employee data"
```

#### To Reproduce Matrix Eigenvalue Task:

**Step 1: Create matrix_operations function**
```bash
cd framework_our_approach/ablation_study_humaneval_and_long_horizon_tasks
python Core/main.py
# When prompted, enter:
# > Create a function 'matrix_operations' that performs basic matrix multiplication and stores results in a global variable 'computation_cache'.
```

**Step 2: Load context and create advanced_matrix_ops**
```bash
python Core/main.py --clean-all  # Clean system first
python Core/main.py --context-memory
# Select the session with matrix_operations (press 1 or 2 as appropriate)
# When prompted, enter:
# > Load the previous session and create a function 'advanced_matrix_ops' that uses the existing 'matrix_operations' function and 'computation_cache' to perform eigenvalue calculations.
```

**Expected Results:**
- With TDD (Prototype-IV): Success after 1 iteration (~125s)
- Without TDD (Prototype-III): Failure after 6 iterations (~169s)

## Architecture Components (Figure 1)

| Pipeline Component | Implementation File |
|-------------------|-------------------|
| Chat & Tool Dispatcher | `Core/main.py` |
| Test-Driven Code Generator | `Test_Driven_Development/generator.py` |
| Function Generator | `Function_Gen/generator.py` |
| Intermediate Adjudicator | `Intermidiate_Adjudicator/adjudicator.py` |
| Unit Test Generator | `Unit_Test/generator.py` |
| Final Adjudicator | `Adjudicator/adjudicator.py` |
| Terminal Context | `Terminal_Context/context_manager.py` |

## Key Differences Between Framework Variants

### Full Framework (`framework_our_approach/`)
- Contains: TDD + Unit Testing + Dual Adjudication
- Core/main.py: 227 lines
- Imports: Test_Driven_Development, Intermidiate_Adjudicator
- Features: Iterative refinement with diagnostic feedback

### Without TDD (`framework_w_o_tdd/`)
- Contains: Unit Testing only
- Core/main.py: 205 lines
- Removed: Test_Driven_Development imports
- Impact: Higher iteration count, lower Pass@1

### Without Both (`framework_w_o_unit_test_and_tdd/`)
- Contains: Basic generation only
- Core/main.py: 206 lines
- Removed: Feedback-Based Iteration loop, unit test components
- Impact: No refinement capability

## Verification Checklist for Reviewers

- [ ] **Table 1**: Run 3 HumanEval problems with TiCoder comparison architecture, verify 77.8% success rate
- [ ] **Table 2**: Run GCD across 3 variants, verify iteration reduction (4→3→2)
- [ ] **Table 3**: Run 10 HumanEval problems, verify Pass@1 (100% vs 90%)
- [ ] **Table 4**: Run long-horizon tasks with command-line arguments, verify TDD enables success

## Important Files

- **Results**: `pass_k_dual_results_*.json` - Pass@k metrics
- **Sessions**: `context_sessions/*.json` - Function memory
- **Problem Mapping**: `evaluation/humaneval_problem_mapping.py` - HumanEval ID mappings
- **Run Logs**: `function_generation.log` - Detailed logs after each run
- **Run Stats**: `function_generation_stats.json` - Performance metrics after each run

## Notes

- Table 1 experiments use GPT-4-0613 for both our framework and TiCoder (fair comparison)
- The `move_one_ball_HE_109` problem specifically demonstrates TDD importance (only failure without TDD)
- Long-horizon tasks require command-line arguments for Salary Analyzer
- The `--use-humaneval` flag enables authentic HumanEval validation for TiCoder comparison
- The `--analyze` flag provides the codebase path for integration tasks
- The `--request` flag specifies the function to generate

## TiCoder Baseline Reproduction

To reproduce the TiCoder baseline results from Table 1:

```bash
cd TiCoder-codebase/src

# Run each problem (requires GPT-4-0613 API key)
python3 main.py --data_file_path ../individual_problems/HumanEval_is_equal_to_sum_even.jsonl \
    --max_code_suggestions 5 --fix_num_tests 5 --model "gpt-4-0613" --query_oracle

python3 main.py --data_file_path ../individual_problems/HumanEval_smallest_change.jsonl \
    --max_code_suggestions 5 --fix_num_tests 5 --model "gpt-4-0613" --query_oracle

python3 main.py --data_file_path ../individual_problems/HumanEval_car_race_collision.jsonl \
    --max_code_suggestions 5 --fix_num_tests 5 --model "gpt-4-0613" --query_oracle
```

**TiCoder Results:**
- Results stored in `src/results/global_results*.json`
- Terminal execution logs in `TiCoder-codebase/RUN_LOGS.md`
- Expected outcomes:
  - is_equal_to_sum_even: 2/5 solutions pass (40%)
  - smallest_change: 4/5 solutions pass (80%)
  - car_race_collision: 1/5 solutions pass (20%)
  - Average: 46.7% success rate

---

For questions about reproduction, please refer to the paper or contact the authors.