
def inventory_low_stock_alert(warehouse):
    '''
    Create a function called inventory_low_stock_alert that takes a Warehouse object. For each product from warehouse.get_all_products(), get current stock using warehouse.get_current_stock(product.sku). If current stock is below product.reorder_point, add to result list with dict containing: sku, name, current_stock, reorder_point, and deficit (reorder_point minus current_stock). Return the list.
    '''
    result = []
    for product in warehouse.get_all_products():
        current_stock = warehouse.get_current_stock(product.sku)
        if current_stock < product.reorder_point:
            deficit = product.reorder_point - current_stock
            result.append({
                'sku': product.sku,
                'name': product.name,
                'current_stock': current_stock,
                'reorder_point': product.reorder_point,
                'deficit': deficit
            })
    return result



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
