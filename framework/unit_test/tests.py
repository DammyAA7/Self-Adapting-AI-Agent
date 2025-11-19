
import sys
import os
# Add framework directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add project root to Python path (for dataset/ and other top-level imports)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# import pytest
from functions import *

import json
import logging
from datetime import datetime
import argparse


def setup_logging():
    """Setup logging to function_generation.log"""
    log_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'function_generation.log'
    )

    # Create logger
    logger = logging.getLogger('self_evolution_tests')
    logger.setLevel(logging.INFO)

    # Create file handler - APPEND mode preserves existing logs
    handler = logging.FileHandler(log_file, mode='a')  # 'a' = append, NOT overwrite
    handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger
### START TESTS ###


from dataset.salary_analyzer.employee_db import EmployeeDB

db = EmployeeDB()
assert callable(salary_analyzer)
result = salary_analyzer()
assert isinstance(result, (int, float))
assert result > 0
assert 30000 <= result <= 200000
print('Salary Analyzer tests passed')


logger = setup_logging()
logger.info(f"Running test for: {"Salary Analyzer"} (ID {"1"})")
logger.info(f"Successfully imported functions from functions.py")
logger.info(f"All assertions passed for {"Salary Analyzer"}")
logger.info(f"===== TEST PASSED ===== ({"Salary Analyzer"})")
print("success")