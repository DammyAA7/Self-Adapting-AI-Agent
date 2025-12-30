# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
def inventory_low_stock_alert(warehouse):
    """
    Returns a list of products with stock below their reorder point.

    Args:
        warehouse (Warehouse): The warehouse object.

    Returns:
        List[Dict]: List of dicts with sku, name, current_stock, reorder_point, and deficit.
    """
    low_stock_list = []
    for product in warehouse.get_all_products():
        current_stock = warehouse.get_current_stock(product.sku)
        if current_stock < product.reorder_point:
            low_stock_list.append({
                'sku': product.sku,
                'name': product.name,
                'current_stock': current_stock,
                'reorder_point': product.reorder_point,
                'deficit': product.reorder_point - current_stock
            })
    return low_stock_list

# Ground-truth test from problem.json

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

