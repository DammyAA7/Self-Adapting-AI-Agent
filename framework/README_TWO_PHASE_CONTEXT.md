# Two-Phase Context Management with Tree-sitter

## Overview

The SelfEvolve framework now implements **two-phase context management** to prevent context overflow when analyzing large codebases. Instead of dumping entire files (27,000+ tokens), the system intelligently extracts only relevant functions.

**Token Reduction:** 87% (27,000 → 3,500 tokens average)

---

## How It Works

### The Problem (Before)

```
User: "Calculate patient risk score"
↓
System reads patient_risk_analyzer project (12 files, 752 LOC)
↓
Dumps ALL 752 lines + CSV data into context
↓
27,000 tokens sent to LLM for EVERY generation step
↓
Context overflow, expensive, slow
```

### The Solution (After)

```
User: "Calculate patient risk score"
↓
PHASE 1: Extract Metadata Only
  - Parse all files with Tree-sitter
  - Get function signatures, docstrings, line numbers
  - Show folder structure
  - Result: ~2,500 tokens (metadata only)
↓
PHASE 1.5: LLM Semantic Selection
  - LLM analyzes task: "calculate patient risk score"
  - LLM selects relevant functions using semantic understanding
  - Example: Selects get_patient, calculate_risk, validate_vitals
  - Returns: JSON with filepath, function_name, reasoning
↓
PHASE 2: Extract Selected Functions Only
  - Tree-sitter extracts FULL code for selected functions only
  - Uses byte offsets for precise extraction
  - Result: ~1,000 tokens (5 functions instead of 60)
↓
TOTAL: ~3,500 tokens (87% reduction)
```

---

## Key Features

### 1. Tree-sitter Parsing

**What:** Robust code parser used by VSCode, GitHub

**Why:**
- More robust than Python's AST (handles syntax errors)
- Provides byte-level precision
- Query language for targeted extraction
- Multi-language support (Python, Java, C++, etc.)

**Where Used:**
- Parsing files to extract function metadata
- Detecting class methods vs standalone functions
- Extracting selected functions by byte range

**Fallback:** If tree-sitter not installed, falls back to AST

---

### 2. Semantic Function Selection

**What:** LLM analyzes task and selects relevant functions

**Example:**

```
Task: "Calculate eigenvalues"

LLM sees metadata:
  matrix_multiply(a, b)
    Description: "Multiplies two matrices"

  parse_csv(filepath)
    Description: "Loads CSV data"

LLM thinks:
  "Eigenvalue calculation needs matrix operations.
   matrix_multiply is relevant (semantic understanding!)
   parse_csv is not relevant to eigenvalues."

LLM selects:
  [{"filepath": "matrix_utils.py", "function_name": "matrix_multiply",
    "reasoning": "Eigenvalue algorithm requires matrix multiplication"}]
```

**Key:** Uses semantic understanding, NOT keyword matching. Even though "eigenvalue" keyword doesn't appear in "matrix_multiply", LLM understands the relationship.

---

### 3. Class Method Detection

**What:** Distinguishes between standalone functions and class methods

**Example:**

```
Code:
class SalaryAnalyzer:
    @staticmethod
    def calculate_average_salary(employees):
        return sum(e['salary'] for e in employees) / len(employees)

Phase 1 Shows:
Static Method: SalaryAnalyzer.calculate_average_salary(employees)
  Usage: SalaryAnalyzer.calculate_average_salary(...)  # Call on class
  Description: Calculate average salary for list of employees

NOT:
Function: calculate_average_salary(employees)  ← Wrong! It's a class method!
```

**Import Instructions:**
```python
# Correct
from dataset.salary_analyzer.salary_analyzer_class import SalaryAnalyzer
result = SalaryAnalyzer.calculate_average_salary(data)

# Wrong (old behavior)
from salary_analyzer_class import calculate_average_salary  # ModuleNotFoundError!
```

---

### 4. Folder Structure Awareness

**What:** Shows project organization to LLM

**Example:**

```
PROJECT FOLDER STRUCTURE:
============================================================
patient_risk_analyzer/
├── [INIT] __init__.py          ← Marked to skip
├── [PY]   hospital.py
├── [PY]   patient.py
├── [DIR]  utils/
│   ├── [PY]   validator.py
│   └── [PY]   formatter.py
├── [CSV]  patient_data.csv
└── [JSON] config.json
============================================================

[INIT] = __init__.py (usually just imports - rarely need selection)
[PY]   = Python modules (select these for functions)
```

**Benefits:**
- LLM sees organization (core vs utils vs models)
- `__init__.py` clearly marked (LLM learns to skip)
- Shows data files separately
- Helps LLM prioritize selections

---

### 5. Automatic Syntax Fixing

**What:** Auto-fixes unclosed parentheses in generated code

**Problem:**
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Missing closing parenthesis! ────────────────────────────────────────────────────^
```

**Solution:**
```python
# Auto-fix detects and adds missing parenthesis
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Fixed! ──────────────────────────────────────────────────────────────────────────────────^

Output: ✓ Auto-fixed unclosed parenthesis in sys.path line
```

---

## Installation

### Required Dependency

```bash
pip install tree-sitter tree-sitter-python
```

**If not installed:** System prints warning but continues with AST fallback (reduced robustness but functional)

---

## Usage

### Basic Usage

```bash
python core/main.py --analyze /path/to/project --request "Create function that does X"
```

### Example

```bash
python core/main.py --analyze dataset/patient_risk_analyzer \
  --request "Calculate patient risk score based on age, conditions, and vitals"
```

### Output You'll See

```
✓ Folder structure captured: 13 files, 0 directories
✓ Analysis complete!

PHASE 1: Extracting function metadata...
✓ Phase 1 complete: ~2,766 tokens (metadata only)

DEBUG: PHASE 1 CONTEXT
[Shows function signatures, docstrings, folder structure]

PHASE 1.5: LLM analyzing and selecting relevant functions...

✓ LLM SEMANTIC SELECTION: Selected 5 relevant functions
============================================================
  • get_patient from hospital.py
    → Reason: Required to retrieve Patient object by patient_id
  • get_recent_records from hospital.py
    → Reason: Needed to fetch recent medical records
  ...

DEBUG: LLM SELECTION RESULT
[Shows JSON with selected functions]

PHASE 2: Extracting full code for 5 selected functions...
✓ Phase 2 complete: ~756 tokens (selected implementations)

DEBUG: PHASE 2 EXTRACTED CODE
[Shows actual function implementations]

TOTAL CONTEXT SIZE: ~3,523 tokens
============================================================
```

---

## How LLM Selection Works

### Semantic Understanding (Not Keywords)

**Example 1: Matrix Operations**

```
User Request: "Calculate eigenvalues"
Keyword Search: "eigenvalue" → Nothing found ❌

LLM Semantic Search:
  Sees: matrix_multiply(a, b) - "Multiplies two matrices"
  Thinks: "Eigenvalues need matrix operations"
  Selects: matrix_multiply ✅
```

**Example 2: Patient Risk**

```
User Request: "Calculate patient risk score"

LLM sees 60 functions, selects only 5:
  ✅ get_patient - "Retrieves patient by ID"
  ✅ get_total_conditions - "Counts patient conditions"
  ✅ get_average_severity - "Average condition severity"
  ✅ has_abnormal_vitals - "Checks for abnormal vitals"
  ✅ get_recent_records - "Gets recent medical records"

  ❌ Skips:
     - calculate_insurance_cost (not relevant to risk)
     - schedule_appointment (not relevant to risk)
     - 50+ other irrelevant functions
```

**Key:** GPT-4 understands semantic relationships from its training, bridging the gap between user intent and codebase function names.

---

## Architecture

### File Structure

```
framework/
├── file_analyzer/
│   └── analyzer.py          ← Two-phase context management
├── core/
│   └── main.py             ← LLM function selector
├── test_driven_development/
│   ├── generator.py        ← Auto-fix syntax
│   └── prompt.txt          ← Scope clarification
└── unit_test/
    └── generator.py         ← Auto-fix syntax
```

### Flow Diagram

```
┌──────────────────────┐
│ analyzer.py          │
│ read_all_files()     │
└──────────────────────┘
          │
          ├─ Step 1: _capture_folder_structure()
          │           Captures folder tree FIRST
          │
          ├─ Step 2: _extract_functions_with_treesitter()
          │           Parses with Tree-sitter
          │           Detects class methods vs functions
          │           Stores parsed trees
          │
          └─ Step 3: format_context_for_llm_phase1()
                      Returns metadata only (~2,500 tokens)

          ↓

┌──────────────────────┐
│ main.py              │
│ select_relevant_*()  │
└──────────────────────┘
          │
          └─ LLM Call: "Which functions do you need?"
              Returns: [{"filepath": "...", "function_name": "..."}]

          ↓

┌──────────────────────┐
│ analyzer.py          │
│ extract_selected_*() │
└──────────────────────┘
          │
          ├─ For each selection:
          │    - Get stored tree
          │    - Query for function by name
          │    - Extract using byte offsets
          │
          └─ Returns: Full implementations (~1,000 tokens)
```

---

## Configuration

### Token Reduction Settings

**File:** `framework/file_analyzer/analyzer.py`

```python
self.max_file_size = 100000  # 100KB max (line 35)
# Files larger than this are skipped in old approach
# With two-phase, can now handle by selecting specific functions

# Phase 1 docstring limit (line 485)
doc = func['docstring'][:100] + "..."  # Truncate long docstrings
```

### Selection Limit

**File:** `framework/core/main.py`

```python
# Line 263
"Select UP TO 10 most relevant functions"
# Prevents Phase 2 from extracting too many functions
```

### Temperature Settings

```python
# Function selection (main.py line 278)
temperature=0.3  # Low temperature for consistent selection

# TDD generation (test_driven_development/generator.py line 92)
temperature=0.7  # Higher for diverse test cases

# Function generation (function_gen/generator.py line 65)
temperature=0.7  # Higher for creative implementations
```

---

## Performance Metrics

### Context Size Comparison

| Project | Files | LOC | Before (Full Dump) | After (Two-Phase) | Reduction |
|---------|-------|-----|-------------------|-------------------|-----------|
| Patient Risk | 12 | 752 | 27,000 tokens | 3,500 tokens | 87% |
| Student GPA | 10 | 783 | 28,000 tokens | 3,800 tokens | 86% |
| Inventory | 8 | 577 | 22,000 tokens | 3,200 tokens | 85% |

### LLM Calls Per Generation

| Phase | Before | After |
|-------|--------|-------|
| TDD Test Gen | 27k tokens | 3.5k tokens |
| Function Gen | 27k tokens | 3.5k tokens |
| Unit Test Gen | 27k tokens | 3.5k tokens |
| **Selection** | - | 2.5k tokens (new) |
| **TOTAL** | 81k tokens | 13k tokens |

**Savings:** 84% reduction in total token usage

---

## Debug Output

### Enable Debug View

Debug output is automatically enabled. You'll see:

```
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
DEBUG: PHASE 1 CONTEXT (What LLM sees for selection)
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
[First 2000 characters of Phase 1 metadata]
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

✓ LLM SEMANTIC SELECTION: Selected 5 relevant functions
  • get_patient from hospital.py
    → Reason: Required to retrieve Patient object
  ...

▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
DEBUG: PHASE 2 EXTRACTED CODE
▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
[Full implementations of selected functions]
▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲
```

**What to check:**
1. Phase 1: Are function signatures complete?
2. Selection: Did LLM select the right functions?
3. Phase 2: Was full code actually extracted?
4. Final: Is combined context reasonable size?

---

## Technical Details

### Phase 1: Metadata Extraction

**File:** `framework/file_analyzer/analyzer.py`

**Method:** `format_context_for_llm_phase1()` (line 465)

**Output Format:**
```
PROJECT ANALYSIS - PHASE 1 (Metadata Only)
Total Functions: 60

PROJECT FOLDER STRUCTURE:
[Tree view with [INIT], [PY], [CSV] markers]

AVAILABLE FUNCTIONS:
============================================================
FILE: warehouse.py
============================================================

Static Method: Warehouse.get_all_products()
  Location: Lines 45-50
  Description: Get all products in catalog

Instance Method: Warehouse.get_current_stock(sku)
  Location: Lines 52-65
  Description: Get current stock quantity for product

CRITICAL IMPORT INSTRUCTIONS:
[Shows correct import patterns for classes vs functions]
```

---

### Phase 1.5: LLM Selection

**File:** `framework/core/main.py`

**Method:** `select_relevant_functions()` (line 240)

**Input:**
```
TASK: {user_request}
AVAILABLE FUNCTIONS: {phase1_metadata}

Consider:
- Direct dependencies
- Indirect dependencies
- Semantic relationships
```

**Output:**
```json
{
  "functions": [
    {
      "filepath": "warehouse.py",
      "function_name": "get_all_products",
      "reasoning": "Needed to iterate over all products"
    },
    ...
  ]
}
```

**Parameters:**
- Temperature: 0.3 (consistent selections)
- Limit: 10 functions max
- Response format: JSON object

---

### Phase 2: Targeted Extraction

**File:** `framework/file_analyzer/analyzer.py`

**Method:** `extract_selected_functions()` (line 497)

**Process:**
1. For each selected function:
   - Get filepath from selection
   - Match filepath to dictionary key (handles full vs relative paths)
   - Get stored tree from Phase 1 (no re-parsing!)
   - Query tree for specific function by name
   - Extract using byte offsets: `content[start_byte:end_byte]`
2. Build context string with all extracted code
3. Include "WHY SELECTED" reasoning for transparency

**Output:**
```
PHASE 2: SELECTED FUNCTION IMPLEMENTATIONS
============================================================

────────────────────────────────────────────────────────────
FILE: warehouse.py
FUNCTION: get_all_products()
WHY SELECTED: Needed to iterate over all products
────────────────────────────────────────────────────────────
def get_all_products(self) -> List[Product]:
    """Get all products in catalog"""
    return list(self.products.values())
```

---

## Troubleshooting

### Issue 1: "tree-sitter not available"

**Symptom:**
```
Warning: tree-sitter not available. Install with: pip install tree-sitter tree-sitter-python
```

**Solution:**
```bash
pip install tree-sitter tree-sitter-python
```

**Alternative:** System works with AST fallback (less robust but functional)

---

### Issue 2: Phase 2 Empty (52 tokens instead of ~800)

**Symptom:**
```
✓ Phase 2 complete: ~52 tokens
[Phase 2 section is empty or minimal]
```

**Cause:** Filepath mismatch between LLM selection and dictionary keys

**Fix Applied:** Lines 442-453 in analyzer.py now match by basename

**Verify:**
Look for: `→ Matched 'dataset/path/file.py' to 'file.py'`

---

### Issue 3: Wrong Functions Selected

**Symptom:** LLM selects irrelevant functions

**Debug:**
```
Check DEBUG: LLM SELECTION RESULT
Read "reasoning" field - why did LLM select each function?
```

**Possible Causes:**
- Phase 1 metadata unclear (improve docstrings in codebase)
- Task description vague (be more specific in request)
- Selection limit too low (increase from 10 if needed)

---

### Issue 4: Tests for Existing Classes Generated

**Symptom:**
```
def test_StockLevel_init_datetime():  ← Testing existing class!
def test_inventory_low_stock_alert():  ← Correct
```

**Cause:** TDD generator testing existing classes instead of just new function

**Fix Applied:** prompt.txt lines 32-36 (scope clarification)

**If persists:** This is a prompt adherence issue with GPT-4.1, not a context management issue

---

## Comparison: Two-Phase vs Full Dump

### Full Dump (Old Approach)

**Advantages:**
- Simple implementation
- No LLM selection call needed
- Guaranteed complete context

**Disadvantages:**
- Context overflow (27,000+ tokens)
- Expensive ($$ tokens)
- Slow (large prompts)
- Includes irrelevant code

### Two-Phase (New Approach)

**Advantages:**
- 87% token reduction
- Scales to large codebases
- Semantic selection (only relevant code)
- Shows folder structure
- Detects class methods correctly

**Disadvantages:**
- One extra LLM call (selection)
- Slightly more complex
- Requires tree-sitter (or AST fallback)

**Verdict:** Two-phase is better for projects >500 LOC

---

## Files Modified

| File | Purpose | Lines Added |
|------|---------|-------------|
| `file_analyzer/analyzer.py` | Tree-sitter integration, two-phase formatting | ~180 |
| `core/main.py` | LLM selector, two-phase pipeline | ~60 |
| `test_driven_development/generator.py` | Auto-fix syntax | ~25 |
| `unit_test/generator.py` | Auto-fix syntax | ~25 |
| `test_driven_development/prompt.txt` | Scope clarification | ~5 |

**Total:** ~295 lines added, ~35 lines modified

---

## Future Enhancements

1. **Caching:** Cache Phase 1 metadata between runs
2. **Incremental:** Only re-parse changed files
3. **Multi-language:** Add Java, C++, JavaScript grammars
4. **Dependency Graph:** Auto-include transitive dependencies
5. **Learning:** Track which functions are often selected together

---

## References

- **Kaggle SWE-Bench 1st Place:** Context retrieval for test generation
- **Kaggle SWE-Bench 4th Place:** Tree-sitter for code contextualization
- **Tree-sitter:** https://tree-sitter.github.io/tree-sitter/
- **SWE-agent (Yang et al.):** 100-line sliding window context management

---

## Change Log

See `CHANGELOG.md` for detailed before/after comparisons and rationale for each change.

---

## Quick Reference

### Key Commands

```bash
# Basic usage
python core/main.py --analyze /path/to/project --request "your request"

# Clean before running
python core/main.py --clean-all --analyze /path/to/project --request "..."

# With context memory
python core/main.py --context-memory --analyze /path/to/project --request "..."
```

### Key Indicators

**Success:**
```
✓ Folder structure captured: X files
✓ Phase 1 complete: ~2,500 tokens
✓ LLM selected N functions
✓ Phase 2 complete: ~800 tokens
TOTAL: ~3,500 tokens
```

**Failure:**
```
⚠ Warning: Could not find file 'X' for function 'Y'  ← Filepath mismatch
✓ Phase 2 complete: ~52 tokens  ← Extraction failed
```

### Where Tree-sitter is Used

1. **Parsing (Phase 1):** `analyzer.py:153` - `ts_parser.parse()`
2. **Querying (Phase 1):** `analyzer.py:167` - Tree-sitter query language
3. **Metadata (Phase 1):** `analyzer.py:166-257` - Extract functions with class context
4. **Extraction (Phase 2):** `analyzer.py:542` - `content[start_byte:end_byte]`

---

## Support

**Issues?** Check:
1. `function_generation.log` for detailed logs
2. Debug output sections (▼ markers)
3. `CHANGELOG.md` for what changed
4. This README for troubleshooting

**Common Fix:** Most issues are resolved by ensuring tree-sitter is installed and Phase 2 filepath matching is working.
