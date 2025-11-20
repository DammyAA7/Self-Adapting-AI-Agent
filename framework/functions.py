# Dynamically generated functions will be added here



def inventory_low_stock_alert(warehouse):
    """
    Returns a list of dicts for products in the warehouse whose current stock is below their reorder point.
    Each dict contains: sku, name, current_stock, reorder_point, deficit.
    Handles edge cases as specified in tests.
    """
    # Validate input: must have get_all_products and get_current_stock
    if not hasattr(warehouse, 'get_all_products') or not hasattr(warehouse, 'get_current_stock'):
        return []
    products = warehouse.get_all_products()
    if not isinstance(products, list):
        return []
    alerts = []
    for product in products:
        sku = getattr(product, 'sku', None)
        name = getattr(product, 'name', None)
        reorder_point = getattr(product, 'reorder_point', None)
        if sku is None or reorder_point is None:
            continue
        current_stock = warehouse.get_current_stock(sku)
        # If current_stock is None, treat as 0 (per test: missing stock returns 0)
        if current_stock is None:
            current_stock = 0
        # If reorder_point == 0, only negative stock triggers alert
        if reorder_point == 0:
            if current_stock < 0:
                alerts.append({
                    'sku': sku,
                    'name': name,
                    'current_stock': current_stock,
                    'reorder_point': reorder_point,
                    'deficit': abs(current_stock)
                })
            continue
        # Normal alert if stock < reorder_point
        if current_stock < reorder_point:
            alerts.append({
                'sku': sku,
                'name': name,
                'current_stock': current_stock,
                'reorder_point': reorder_point,
                'deficit': reorder_point - current_stock
            })
    return alerts



if __name__ == "__main__":
    pass

if __name__ == "__main__":
    pass
