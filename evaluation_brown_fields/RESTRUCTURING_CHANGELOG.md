# Restructuring Changelog - HumanEval-Like Format

## Date: 2025-10-12

### Overview
Restructured the test_context dataset folders to follow a HumanEval-like format with standardized structure for each problem. This makes the dataset more consistent, maintainable, and easier to use for evaluation.

---

## Changes Made

### 1. Inventory Replenishment Module Refactoring

**Before:**
- Single monolithic file: `inventory_system.py` (189 lines)
- All classes (Product, StockLevel, SalesTransaction, PurchaseOrder, Warehouse) in one file
- No standardized problem metadata

**After:**
- Split into separate module files for better organization:
  - `product.py` - Product class (18 lines)
  - `stock_level.py` - StockLevel class (20 lines)
  - `sales_transaction.py` - SalesTransaction class (18 lines)
  - `purchase_order.py` - PurchaseOrder class (16 lines)
  - `warehouse.py` - Warehouse class and create_sample_warehouse function (155 lines)
  - `__init__.py` - Module exports and documentation
- Added `problem.json` with test_code embedded

**Why Changed:**
- **Modularity:** Each class now has its own file, following single-responsibility principle
- **Maintainability:** Easier to locate and modify specific components
- **Reusability:** Classes can be imported independently
- **Testability:** Isolated components are easier to unit test

---

### 2. Standardized Problem Structure for All Folders

**Before:**
- Each problem folder had inconsistent structure
- Test code was in separate `SELF_EVOLUTION_TEST_SUITE.json`
- No individual problem metadata files

**After:**
Each problem folder now contains:
- **Context files** (e.g., `employee_database.py`, `patient_records.py`)
- **`problem.json`** with standardized fields:
  - `id`: Unique problem identifier
  - `task_id`: HumanEval-style task ID (e.g., "SelfEvolution/4")
  - `problem_name`: Human-readable problem name
  - `prompt`: Detailed problem description
  - `entry_point`: Function name to implement
  - `context_files`: List of supporting code files
  - `dataset`: Dataset category ("self-evolution")
  - `domain`: Problem domain (e.g., "e-commerce", "healthcare")
  - `requires_context`: Boolean indicating if context is required
  - **`test_code`**: Complete test code embedded in JSON (NEW)

**Why Changed:**
- **Self-contained:** Each problem folder is now completely self-contained
- **HumanEval compatibility:** Follows HumanEval.jsonl structure pattern
- **Easier evaluation:** Test code is directly accessible from problem metadata
- **Better organization:** All problem information in one place

---

### 3. Problem Folders Updated

#### 3.1 Salary Analyzer (ID: 1)
- **Files:** employee_database.py, data_processor.py, ml_utils.py, web_crawler.py
- **Domain:** HR Analytics
- **Added:** problem.json with embedded test code

#### 3.2 Patient Risk Analyzer (ID: 2)
- **Files:** patient_records.py
- **Domain:** Healthcare
- **Added:** problem.json with embedded test code

#### 3.3 Student GPA Calculator (ID: 3)
- **Files:** enrollment_system.py
- **Domain:** Education
- **Added:** problem.json with embedded test code

#### 3.4 Inventory Low Stock Alert (ID: 4)
- **Files:** product.py, stock_level.py, sales_transaction.py, purchase_order.py, warehouse.py
- **Domain:** E-Commerce
- **Restructured:** Split inventory_system.py into 5 separate class files
- **Added:** problem.json with embedded test code

#### 3.5 Movie API Interface Evolution (ID: 8)
- **Files:** movie.csv
- **Domain:** Media Recommendation
- **Added:** problem.json with embedded test code

#### 3.6 Book Recommender (ID: 9)
- **Files:** books.csv
- **Domain:** Media Recommendation
- **Added:** problem.json with embedded test code

#### 3.7 Performance Tracker (ID: 10)
- **Files:** performance_reviews.csv
- **Domain:** HR Analytics
- **Added:** problem.json with embedded test code

#### 3.8 Friend Suggester (ID: 11)
- **Files:** social_graph.json
- **Domain:** Social Network
- **Added:** problem.json with embedded test code

---

## File Structure Comparison

### Before:
```
test_context/
├── inventory_replenishment/
│   ├── __init__.py
│   └── inventory_system.py (all classes)
├── salary_analyzer/
│   ├── __init__.py
│   └── employee_database.py
└── ...
```

### After:
```
test_context/
├── inventory_replenishment/
│   ├── __init__.py
│   ├── product.py
│   ├── stock_level.py
│   ├── sales_transaction.py
│   ├── purchase_order.py
│   ├── warehouse.py
│   └── problem.json (with test_code)
├── salary_analyzer/
│   ├── __init__.py
│   ├── employee_database.py
│   ├── data_processor.py
│   ├── ml_utils.py
│   ├── web_crawler.py
│   └── problem.json (with test_code)
└── ...
```

---

## Benefits of Restructuring

### 1. **Consistency**
- All problem folders follow the same structure
- Standardized metadata format across all problems
- Uniform test code embedding strategy

### 2. **HumanEval Compatibility**
- Follows the established pattern from HumanEval.jsonl
- Each problem is self-contained with task_id, prompt, entry_point, and test
- Can be easily converted to JSONL format if needed

### 3. **Improved Maintainability**
- Separated concerns (class files, test code, metadata)
- Easier to update individual components
- Clear documentation in each problem.json

### 4. **Better Testability**
- Test code is embedded in problem.json
- Easy to extract and execute tests programmatically
- Consistent test structure across all problems

### 5. **Enhanced Modularity**
- inventory_replenishment classes can be imported independently
- Each class has single responsibility
- Easier to extend or modify individual components

---

## Migration Guide

If you need to use these problems:

### Reading Problem Metadata:

```python
import json

with open('../dataset/inventory_replenishment/problem.json', 'r') as f:
  problem = json.load(f)

print(f"Task ID: {problem['task_id']}")
print(f"Entry Point: {problem['entry_point']}")
print(f"Test Code: {problem['test_code']}")
```

### Importing Context Classes:
```python
# Old way (still works):
from test_context_extended.inventory_system import Warehouse

# New way (recommended):
from test_context.inventory_replenishment import Warehouse, Product, StockLevel
```

### Running Tests:
```python
# Extract and execute test code
exec(problem['test_code'], globals())
```

---

## Breaking Changes

### None
- All imports remain backward compatible
- Old code using `test_context_extended` still works
- New modular structure is additive, not destructive

---

## Next Steps

1. ✅ Split inventory_system.py into class files
2. ✅ Create problem.json for all problem folders
3. ✅ Embed test_code in problem.json files
4. 🔲 Optional: Create unified problem loader utility
5. 🔲 Optional: Generate HumanEval.jsonl format from problem.json files

---

## Notes

- The original `SELF_EVOLUTION_TEST_SUITE.json` is preserved for reference
- All test assertions remain unchanged - only the structure has changed
- Context file paths in test_code use absolute paths where necessary for CSV/JSON files
- Each problem.json includes domain classification for better organization

---

**Generated by:** Claude Code (Sonnet 4.5)
**Date:** October 12, 2025
**Reviewer:** Please verify test compatibility before merging
