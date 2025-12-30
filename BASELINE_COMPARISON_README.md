# Baseline Framework Quantitative Evaluation Methodology

Empirical evaluation of SelfEvolve against three state-of-the-art multi-agent code generation frameworks: AgentCoder, AutoGen, and MetaGPT.

**Evaluation Scope:** 11 codebase integration tasks (4 integration, 3 compositional, 4 data processing)
**Runs Per Framework:** 5 independent runs per task
**Total Experimental Results:** 165 verified runs

**Repository Structure:**
- `baselines/` - Baseline framework implementations (AgentCoder, AutoGen, MetaGPT)
- `evaluations/` - All evaluation results
  - `ablation_study/` - TDD pipeline ablation (with_tdd, without_tdd)
  - `quantitative_comparison/` - Baseline comparison results

**Research Principle:** All frameworks received identical context, task specifications, ground-truth test cases, and LLM backend to ensure fair comparison.

---

## EVALUATION OVERVIEW

### Task Categories

**Integration Tasks (4):** Salary Analyzer, Patient Risk Analyzer, Student GPA Calculator, Inventory Alert
- Codebase size: 577-783 LOC, 7-20 interconnected classes
- Requires: Navigation of existing multi-file codebases, proper import resolution, integration with existing class hierarchies

**Compositional Tasks (3):** Matrix Eigenvalue, Portfolio Risk, IoT Sensor Pipeline
- Session 1: Generate foundational function (30-50 LOC)
- Session 2: Generate function that builds upon Session 1 function (cross-session composition)
- Tests: Cross-session code reuse and compositional capability

**Data Processing Tasks (4):** Movie API, Book Recommender, Performance Tracker, Friend Suggester
- External datasets: 50-100 records
- Requires: Data file access, filtering, aggregation, recommendation generation

### Fair Comparison Protocol

All frameworks evaluated under identical conditions:

1. **Identical Codebase Context:** Complete source files (all .py files, data files, configurations) provided to each framework
2. **Identical Problem Specifications:** Same task descriptions and requirements
3. **Identical Ground-Truth Tests:** Same validation criteria for all frameworks
4. **Identical LLM Backend:** GPT-4.1 via Azure OpenAI for all frameworks
5. **Context Size:** 23,056 to 54,443 characters per task (same for all)

**Critical fairness measure for compositional tasks:** Baseline frameworks lack cross-session persistence (documented limitation). To ensure fair comparison, we manually extracted Session 1 generated code and explicitly provided it as Session 2 context—giving baselines an advantage they normally lack.

---

## AGENTCODER EVALUATION

### Configuration for Codebase Integration

AgentCoder was designed for HumanEval/MBPP (isolated function generation). To evaluate it on codebase integration tasks, we configured it to receive the same codebase context SelfEvolve receives.

**Files Modified:**
- `src/programmer_humaneval.py` (code generation)
- `src/test_designer_humaneval.py` (test generation)
- `src/test_executor_humaneval.py` (execution and variant selection)

**Key Modification - Context Injection:**

In `fetch_completion()` function (all three src files):

    # Extract codebase context from dataset
    codebase_context = data_entry.get("codebase_context", "")

    # Build prompt with context (if available)
    if codebase_context:
        # Integration/data tasks receive complete codebase
        prompt_with_context = f"""
        AVAILABLE CODEBASE/DATA:
        {codebase_context}

        TASK:
        {prompt}
        """
    else:
        # Compositional Session 1 tasks (no context)
        prompt_with_context = prompt

**What this achieves:** AgentCoder receives complete codebase files in the prompt—identical information to what SelfEvolve automatically analyzes. The difference: SelfEvolve extracts this automatically via codebase analysis; AgentCoder receives it pre-formatted in the prompt.

**Dataset Format:**

Tasks converted to HumanEval JSONL format for AgentCoder compatibility:

    {
      "task_id": "SelfEvolve/2",
      "prompt": "def patient_risk_score():\\n    '''...'''\\n    pass\\n",
      "entry_point": "patient_risk_score",
      "test": "",
      "test_code": "# Ground truth test specification",
      "codebase_context": "# Complete codebase files",
      "completion_list": [],
      "test_case_list": [],
      "completion": ""  # Best selected variant (set by test_executor)
    }

**Dataset Files:**
- `dataset/non_compositional_tasks.jsonl` - 8 integration + data processing tasks
- `dataset/compositional_session1.jsonl` - 3 compositional Session 1 tasks
- `dataset/compositional_session2.jsonl` - 3 compositional Session 2 tasks (with Session 1 code in context)

**Dataset Switching:** In each src file, comment/uncomment dataset path to select task set.

### Execution Protocol (5 Runs Per Task Set)

For each of 5 independent runs:

**1. Configure Dataset:**

    # In src/programmer_humaneval.py, test_designer_humaneval.py, test_executor_humaneval.py
    # Select dataset:
    with open("./dataset/non_compositional_tasks.jsonl", "r") as f:  # For integration/data
    # OR
    with open("./dataset/compositional_session1.jsonl", "r") as f:  # For comp S1
    # OR
    with open("./dataset/compositional_session2.jsonl", "r") as f:  # For comp S2

**2. Execute AgentCoder Pipeline:**

    cd AgentCoder
    python src/programmer_humaneval.py      # Generates 5 code variants per task
    python src/test_designer_humaneval.py   # Generates 5 test variants per task
    python src/test_executor_humaneval.py   # Tests combinations, selects best (5 iterations)

**Pipeline Output:**
- `dataset/gpt-4.1_python_noncomp.json` (or `_comp_s1.json`, `_comp_s2.json`)
- Contains: `completion_list` (5 variants), `test_case_list` (5 test suites), `completion` (best selected variant)

**3. Validate Against Ground Truth:**

    python test_agentcoder_final.py         # For integration/data tasks
    python test_compositional_final.py      # For compositional tasks

**Validation Script Behavior:**
- Loads task from output JSON
- Extracts `completion` field (AgentCoder's selected best variant)
- Executes against ground-truth test specification
- Records: PASS/FAIL status, error messages if failed

**4. Repeat 5 Times:**
Entire pipeline repeated 5 times per task set (integration, compositional S1, compositional S2) to account for LLM stochasticity.

### Compositional Task Handling

**Session 1:** Standard execution (no context)

**Session 2:**
1. Manually extract AgentCoder's selected `completion` from Session 1 output
2. Add to `compositional_session2.jsonl` dataset in `codebase_context` field
3. Run pipeline with Session 2 dataset
4. AgentCoder receives Session 1 code as if it had cross-session persistence

This manual injection gives AgentCoder the advantage it lacks (no built-in persistence mechanism).

### Results Structure

    evaluations/quantitative_comparison/agentcoder_empirical_results/
    ├── integration_tasks/
    │   ├── 1st_run/
    │   │   ├── dataset_created/                    # Created datasets
    │   │   ├── default_saved_logs/                 # AgentCoder default outputs (gpt-4.1_*.json)
    │   │   ├── ground_truth_test_results/          # Validation results (8 task .json files)
    │   │   └── terminal_logs/                      # Execution logs
    │   ├── 2nd_run/
    │   ├── 3rd_run/
    │   ├── 4th_run/
    │   └── 5th_run/
    └── compositional_tasks/
        ├── 1st_run/
        │   ├── dataset_created/                    # Session 1 & 2 datasets
        │   ├── default_saved_logs/                 # AgentCoder outputs (gpt-4.1_python_comp_s*.json)
        │   ├── ground_truth_test_results/          # compositional_evaluation.log, compositional_results.json
        │   └── terminal_logs/                      # Bash logs
        ├── 2nd_run/
        ├── 3rd_run/
        ├── 4th_run/
        └── 5th_run/

**Key Files:**
- `ground_truth_test_results/compositional_results.json`: PASS/FAIL for 3 compositional tasks
- `default_saved_logs/gpt-4.1_python_noncomp.json`: AgentCoder raw outputs
- AgentCoder uses 5 iterations per task (fixed budget)

**Performance:** 0/55 (0.0%) - Complete failure across all tasks and all runs
- Root cause: Import resolution failures (ModuleNotFoundError, ImportError)
- Designed for isolated functions (HumanEval 11.5 LOC avg), not codebase integration (577-783 LOC)

---

## AUTOGEN EVALUATION

### Configuration for Codebase Integration

AutoGen provides agbench benchmarking infrastructure. We created SelfEvolve benchmark following agbench format with codebase context integration.

**Task Structure:**

Each task defined via JSONL entry pointing to task directory:

    {
      "id": "patient_risk_analyzer",
      "template": "Tasks/patient_risk_analyzer"
    }

**Task Directory Contains:**
- `scenario.py` - Task specification (modified with context injection)
- `prompt.txt` - Function signature and docstring
- `context.txt` - Complete codebase files (SAME as SelfEvolve receives)
- `custom_code_executor.py` - Execution environment
- Ground-truth test specifications

**Context Injection in scenario.py:**

    # Load codebase context if available
    context = ""
    if os.path.exists("context.txt"):
        with open("context.txt", "rt") as fh:
            context = fh.read()

    # Build task message
    if context:
        task = f"""AVAILABLE CODEBASE/DATA:
        {context}

        Complete the following function:
        {prompt}
        """
    else:
        task = f"""Complete the following function:
        {prompt}
        """

**Fairness Measure - Ground Truth in Loop:**

AutoGen's HumanEval evaluation includes ground-truth tests in the execution loop. We maintained this protocol for fairness—ground-truth tests available to AutoGen's code executor during generation, matching its designed testing environment.

### Execution Protocol (5 Runs Per Task Set)

For each of 5 independent runs:

**Integration/Data Tasks (8 tasks):**

    cd AutoGen/python/packages/agbench/benchmarks/SelfEvolve
    agbench run Tasks/selfevolve_noncomp.jsonl --native

**Configuration:**
- `max_turns=12` conversation rounds
- Native execution (no Docker)
- Each task attempted once per run

**agbench Output (in SelfEvolve/Results/):**
- `Results/selfevolve_noncomp/SelfEvolve_[task_id]/0/console_log.txt` - Full conversation
- `Results/selfevolve_noncomp/SelfEvolve_[task_id]/0/` - Task execution artifacts

**After each run, results copied to:**

    evaluations/quantitative_comparison/autogen_empirical_results/integration_tasks/[run]/SelfEvolve/

**Validation:**

    agbench tabulate Results/selfevolve_noncomp

**Output:** `autogen_tabulate_pass.log` with pass/fail status for each task

**Compositional Tasks (3 tasks, 2 sessions):**

**Session 1:**

    agbench run Tasks/compositional_session1.jsonl --native

**Session 2 (with Session 1 context):**
1. Manually extract generated code from Session 1 results
2. Write extracted code to `context.txt` in each Session 2 task directory
3. Run Session 2:

       agbench run Tasks/compositional_session2.jsonl --native

4. AutoGen receives Session 1 code in task message (as if it had persistence)

**Repeat 5 times** for each session.

### Results Structure

    evaluations/quantitative_comparison/autogen_empirical_results/
    ├── integration_tasks/
    │   ├── 1st_run/
    │   │   └── SelfEvolve/
    │   │       ├── autogen_tabulate_pass.log (KEY FILE - PASS/FAIL results)
    │   │       ├── Results/ (agbench execution results)
    │   │       ├── Tasks/ (task definitions)
    │   │       ├── Scripts/
    │   │       ├── Templates/
    │   │       ├── config.yaml
    │   │       ├── ENV.yaml
    │   │       └── test_autogen_results.py
    │   ├── 2nd_run/
    │   ├── 3rd_run/
    │   ├── 4th_run/
    │   └── 5th_run/
    └── compositional_tasks/
        ├── 1st_run/
        │   ├── 1st_run/ (Session 1)
        │   │   └── SelfEvolve/
        │   │       ├── autogen_tabulate_pass.log
        │   │       └── Results/compositional_session1/SelfEvolve_[5,6,7]_S1/0/
        │   └── 2nd_run/ (Session 2)
        │       └── SelfEvolve/
        │           ├── autogen_tabulate_pass.log (KEY FILE - compositional results)
        │           ├── Results/compositional_session2/SelfEvolve_[5,6,7]_S2/0/
        │           └── Results/compositional_session1/ (Session 1 for reference)
        ├── 2nd_run/
        ├── 3rd_run/
        ├── 4th_run/
        └── 5th_run/

**Key Files:**
- `autogen_tabulate_pass.log`: Task ID, pass/fail status (True/False), turn count
- AutoGen uses max_turns=12 (variable conversation rounds)

**Performance:** 17/55 (30.9%)
- Integration: 0/20 (0%) - No success on codebase integration
- Compositional: 11/15 (73.3%) - Strong performance when Session 1 code simple and explicit
- Data Processing: 6/20 (30%) - Variable success on data manipulation

---

## METAGPT EVALUATION

### Configuration for Codebase Integration

MetaGPT generates complete software projects from requirements. We configured it to generate functions for existing codebases by providing codebase context in prompts.

**Evaluation Scripts Created:**
- `run_metagpt_evaluation.py` - Integration and data processing tasks
- `run_metagpt_compositional_session1.py` - Compositional Session 1
- `run_metagpt_compositional_session2.py` - Compositional Session 2

**Prompt Construction with Context:**

    # Load task and codebase
    prompt = load_task_prompt(task_name)
    codebase_context = load_codebase_context(task_name)

    # Build MetaGPT prompt
    full_prompt = f"""
    CODEBASE CONTEXT:
    {codebase_context}

    TASK:
    {prompt}

    Generate the Python function.
    """

    # Execute MetaGPT CLI
    result = subprocess.run(
        ['metagpt', full_prompt],
        capture_output=True,
        text=True,
        timeout=600
    )

**Code Extraction:**

MetaGPT outputs code with escaped characters (JSON format). Extraction includes decoding:

    def decode_escaped(code):
        code = code.replace('\\n', '\n')   # Newlines
        code = code.replace('\\t', '\t')   # Tabs
        code = code.replace('\\"', '"')    # Quotes
        return code.strip()

    # Extract from MetaGPT output
    pattern = r'```python\\s*(.*?)\\s*```'
    matches = re.findall(pattern, stdout, re.DOTALL)
    code = decode_escaped(max(matches, key=len)) if matches else None

### Execution Protocol (5 Runs Per Task Set)

For each of 5 independent runs:

**Integration/Data Tasks (8 tasks):**

    cd MetaGPT
    python run_metagpt_evaluation.py

**Process:**
- Iterates through 8 tasks
- For each task: loads codebase context, builds prompt, executes MetaGPT CLI
- Timeout: 600 seconds per task
- Single-shot generation (1 attempt per task)

**Output:**
- `metagpt_outputs/[task]_code.py` - Extracted code
- `metagpt_outputs/[task]_stdout.txt` - Full MetaGPT output
- `metagpt_results.json` - Structured results with pass/fail

**Validation:**
- Ground-truth tests executed against generated code
- Results saved to `metagpt_results.json`

**Compositional Tasks (3 tasks, 2 sessions):**

**Session 1:**

    python run_metagpt_compositional_session1.py

Generates Session 1 functions, saves to `metagpt_comp_s1_outputs/`

**Session 2:**
1. Load Session 1 code: `session1_code = load_from_s1_outputs(task)`
2. Inject into Session 2 prompt:

       full_prompt = f"""
       PREVIOUS CODE FROM SESSION 1:
       {session1_code}

       TASK FOR SESSION 2:
       {session2_prompt}
       """

3. Execute:

       python run_metagpt_compositional_session2.py

4. MetaGPT receives Session 1 code (as if it had cross-session persistence)

**Repeat 5 times** for each task set.

### Results Structure

    evaluations/quantitative_comparison/metagpt_empirical_results/
    ├── integration_tasks/
    │   ├── 1st_run/
    │   │   ├── metagpt_results.json (KEY FILE - PASS/FAIL status)
    │   │   ├── metagpt_outputs/ (8 tasks: *_code.py, *_stdout.txt)
    │   │   ├── metagpt_prompts/ (prompts used)
    │   │   ├── metagpt_tests/ (ground truth tests)
    │   │   ├── metagpt_evaluation.log
    │   │   └── run_metagpt_evaluation.py
    │   ├── 2nd_run/
    │   ├── 3rd_run/
    │   ├── 4th_run/
    │   └── 5th_run/
    └── compositional_tasks/
        ├── 1st_run/
        │   ├── 1st_run/ (Session 1)
        │   │   ├── metagpt_comp_s1_results.json (KEY FILE - Session 1 results)
        │   │   ├── metagpt_comp_s1_outputs/ (3 tasks: *_s1_code.py, *_s1_stdout.txt)
        │   │   ├── metagpt_comp_s1_prompts/
        │   │   ├── metagpt_compositional_s1.log
        │   │   └── run_metagpt_compositional_session1.py
        │   └── 2nd_run/ (Session 2)
        │       ├── metagpt_comp_s2_results.json (KEY FILE - Session 2 results)
        │       ├── metagpt_comp_s2_outputs/ (3 tasks: *_s2_code.py, *_s2_stdout.txt)
        │       ├── metagpt_comp_s2_prompts/
        │       ├── metagpt_comp_s2_tests/
        │       ├── metagpt_compositional_s2.log
        │       └── run_metagpt_compositional_session2.py
        ├── 2nd_run/
        ├── 3rd_run/
        ├── 4th_run/
        └── 5th_run/

**Key Files:**
- `metagpt_results.json`: Pass/fail status for 8 integration/data tasks
- `metagpt_comp_s2_results.json`: Pass/fail status for 3 compositional tasks
- Iteration count: 1 (single-shot generation per task)

**Performance:** 15/55 (27.3%)
- Integration: 10/20 (50%) - Moderate success (file list generation helps)
- Compositional: 5/15 (33.3%) - Struggles with cross-session composition
- Data Processing: 0/20 (0%) - Cannot access data files correctly

---

## STATISTICAL ANALYSIS

### Bonferroni-Corrected Wilcoxon Signed-Rank Tests

**Methodology:** Same pairing approach as RQ2 TDD ablation study.

**Pairing Structure:**

For each of 11 problems:
1. Compute success proportion for SelfEvolve: successes / 5 runs
2. Compute success proportion for baseline: successes / 5 runs
3. Create pair: (SelfEvolve proportion, baseline proportion)

Example:
- Salary Analyzer: SelfEvolve 4/5 (0.80), AgentCoder 0/5 (0.00) → Pair: (0.80, 0.00)
- Patient Risk: SelfEvolve 5/5 (1.00), AgentCoder 0/5 (0.00) → Pair: (1.00, 0.00)
- ... (11 pairs total)

**Statistical Test:**
- Wilcoxon signed-rank test on 11 problem-level pairs (N=11, not N=55 runs)
- Two-tailed test (conservative)
- Three comparisons: SelfEvolve vs AgentCoder, vs AutoGen, vs MetaGPT
- Bonferroni correction: α = 0.05 / 3 = 0.0167

**Execution:**

    cd framework/evaluation
    python wilcoxon_bonferroni_baseline_comparison.py

**Output Files:**
- `wilcoxon_bonferroni_results.json` - Full statistical results with effect sizes
- `bonferroni_overall_results.json` - Simplified results table

**Results:**
- SelfEvolve vs AgentCoder: W=0, p=0.000977, p_adj=0.003 ✓ Significant
- SelfEvolve vs AutoGen: W=0, p=0.003906, p_adj=0.012 ✓ Significant
- SelfEvolve vs MetaGPT: W=0, p=0.001953, p_adj=0.006 ✓ Significant

All comparisons statistically significant at Bonferroni-corrected α=0.0167.

---

## EMPIRICAL RESULTS SUMMARY

### Framework Performance

| Framework | Integration | Compositional | Data Processing | Overall |
|-----------|-------------|---------------|-----------------|---------|
| **SelfEvolve** | 18/20 (90.0%) | 14/15 (93.3%) | 19/20 (95.0%) | **51/55 (92.7%)** |
| AutoGen | 0/20 (0.0%) | 11/15 (73.3%) | 6/20 (30.0%) | 17/55 (30.9%) |
| MetaGPT | 10/20 (50.0%) | 5/15 (33.3%) | 0/20 (0.0%) | 15/55 (27.3%) |
| AgentCoder | 0/20 (0.0%) | 0/15 (0.0%) | 0/20 (0.0%) | 0/55 (0.0%) |

**Statistical Significance (Wilcoxon + Bonferroni):**
- vs AgentCoder: p_adj = 0.003
- vs AutoGen: p_adj = 0.012
- vs MetaGPT: p_adj = 0.006

All comparisons significant at α=0.0167 (Bonferroni-corrected threshold).

### Failure Analysis

**AgentCoder (0/55):**
- Documented design: "provides code snippets to human developer" (Huang et al.)
- Optimized for: HumanEval (11.5 LOC avg), MBPP (6.8 LOC avg)
- Our tasks: 577-783 LOC codebases
- Failure mode: Cannot resolve imports despite codebase in prompt

**AutoGen (17/55):**
- Documented design: Generic "infrastructure" for diverse applications
- Success: Compositional tasks with simple Session 1 code
- Failure: Complex codebase integration (no specialized mechanisms)

**MetaGPT (15/55):**
- Documented limitation: "Each software project executed independently" (Hong et al. Appendix A.1)
- Success: Integration tasks (file list generation helps)
- Failure: Cross-file dependencies (documented in Appendix C.2)

### Detailed Results Documentation

**All 165 individual results verified and documented in:**

    all_quantitative_results.txt

This file contains:
- Run-by-run results for each framework on each task
- Pass/fail status for all 55 runs per framework
- Summary statistics per framework
- Verification that results align with documented framework limitations

**Statistical Analysis Results:**

    framework/evaluation/wilcoxon_bonferroni_results.json
    framework/evaluation/bonferroni_overall_results.json

---

## RESEARCH INTEGRITY

**Fair Comparison Measures:**
- ✓ Identical context provided to all frameworks (23k-54k characters per task)
- ✓ Same LLM backend (GPT-4.1) for all frameworks
- ✓ Identical ground-truth validation criteria
- ✓ Baselines given advantage: Manual Session 1 injection (no persistence required)
- ✓ AutoGen tested under designed protocol: Ground truth in loop (HumanEval-style)

**Statistical Rigor:**
- ✓ Problem-level pairing (N=11 pairs, not N=55 runs)
- ✓ Bonferroni correction for multiple comparisons (α=0.0167)
- ✓ Conservative two-tailed tests
- ✓ All 165 results individually verified

**Alignment with Documented Limitations:**
- ✓ AgentCoder failures: Matches HumanEval/MBPP design scope
- ✓ AutoGen partial success: Matches generic framework design
- ✓ MetaGPT failures: Matches documented limitations (independent projects, cross-file dependencies)

**Transparency:**
- ✓ All source code modifications documented
- ✓ All datasets provided in replication package
- ✓ Complete results preserved for verification
- ✓ Statistical analysis scripts included

---

## CONTACT

For replication questions or additional details:
- See comprehensive appendix in paper submission
- All source code and datasets included in replication package
- Statistical analysis scripts available in `framework/evaluation/`

**Last Updated:** December 29, 2025
**Verification Status:** All 165 experimental results individually verified ✓
