
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


#### START TESTS HERE ####


from dataset.inventory_replenishment.warehouse import Warehouse, create_sample_warehouse

warehouse = create_sample_warehouse()
low_stock = inventory_low_stock_alert(warehouse)

assert isinstance(low_stock, list)
assert len(low_stock) == 5  # SKU001, SKU002, SKU004, SKU005, SKU006 are below reorder

# Verify each low stock item has correct structure
for item in low_stock:
    assert isinstance(item, dict)
    assert 'sku' in item
    assert 'name' in item
    assert 'current_stock' in item
    assert 'reorder_point' in item
    assert 'deficit' in item
    assert item['current_stock'] < item['reorder_point']
    assert item['deficit'] == item['reorder_point'] - item['current_stock']

# Verify specific SKUs are in the list
skus_in_result = [item['sku'] for item in low_stock]
assert 'SKU001' in skus_in_result
assert 'SKU002' in skus_in_result
assert 'SKU004' in skus_in_result
assert 'SKU005' in skus_in_result
assert 'SKU006' in skus_in_result
assert 'SKU003' not in skus_in_result  # SKU003 is above reorder point

print('Inventory Low Stock Alert tests passed')

logger = setup_logging()
logger.info(f"Running test for: {"Inventory Low Stock Alert"} (ID {"4"})")
logger.info(f"Successfully imported functions from functions.py")
logger.info(f"All assertions passed for {"Inventory Low Stock Alert"}")
logger.info(f"===== TEST PASSED ===== ({"Inventory Low Stock Alert"})")
print("success")