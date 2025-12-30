def inventory_low_stock_alert(warehouse):
    """
    For each product in the warehouse, check if current stock is below reorder point.
    If so, add to result list with sku, name, current_stock, reorder_point, and deficit.
    Returns a list of such dicts.
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