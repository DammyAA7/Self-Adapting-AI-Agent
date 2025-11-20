from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def inventory_low_stock_alert(warehouse):
    """
    Returns a list of dictionaries for each product in the warehouse whose current stock is below the reorder point.
    Each dictionary contains: sku, name, current_stock, reorder_point, and deficit.
    Returns an empty list if there are no such products, or if input is invalid.
    """
    if not warehouse or not hasattr(warehouse, "get_all_products") or not hasattr(warehouse, "get_current_stock"):
        return []
    result = []
    try:
        products = warehouse.get_all_products()
    except Exception:
        return []
    for product in products:
        # Validate product object has required attributes
        if not hasattr(product, "sku") or not hasattr(product, "name") or not hasattr(product, "reorder_point"):
            continue
        try:
            sku = product.sku
            name = product.name
            reorder_point = product.reorder_point
            # Defensive: skip if reorder_point is not int
            if not isinstance(reorder_point, int):
                continue
            current_stock = warehouse.get_current_stock(sku)
            # Defensive: skip if current_stock is not an int
            if not isinstance(current_stock, int):
                continue
            if current_stock < reorder_point:
                result.append({
                    "sku": sku,
                    "name": name,
                    "current_stock": current_stock,
                    "reorder_point": reorder_point,
                    "deficit": reorder_point - current_stock
                })
        except Exception:
            continue
    return result

