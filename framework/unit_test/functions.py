from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


from dataset.inventory_replenishment.warehouse import Warehouse

def inventory_low_stock_alert(warehouse):
    """
    Returns a list of dictionaries for products in the warehouse that are below their reorder point.
    Each dict contains: 'sku', 'name', 'current_stock', 'reorder_point', 'deficit'.
    Handles missing stock level, zero or negative stock, and skips products without reorder_point.
    Returns [] for invalid warehouse objects.
    Raises ValueError if any StockLevel.last_updated is in an unsupported date format.
    """
    import datetime

    # Supported date formats for StockLevel.last_updated
    supported_formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S"
    ]

    # Validate warehouse object: must have get_all_products and get_current_stock
    if not hasattr(warehouse, "get_all_products") or not hasattr(warehouse, "get_current_stock"):
        return []

    result = []
    try:
        products = warehouse.get_all_products()
    except Exception:
        return []

    for prod in products:
        # Defensive: skip if prod has no reorder_point or name or sku
        if not hasattr(prod, "reorder_point") or not hasattr(prod, "sku") or not hasattr(prod, "name"):
            continue

        sku = prod.sku
        name = prod.name
        reorder_point = getattr(prod, "reorder_point", None)
        if reorder_point is None:
            continue

        # Get current stock using warehouse.get_current_stock(sku)
        try:
            current_stock = warehouse.get_current_stock(sku)
        except Exception:
            current_stock = 0

        # Find all stock_levels for this SKU in the warehouse (if attribute exists)
        stock_levels = getattr(warehouse, "stock_levels", [])
        for stock in stock_levels:
            if getattr(stock, "sku", None) == sku and getattr(stock, "warehouse_id", None) == getattr(warehouse, "warehouse_id", None):
                last_updated = getattr(stock, "last_updated", None)
                if last_updated is not None:
                    # Validate date format
                    for fmt in supported_formats:
                        try:
                            datetime.datetime.strptime(last_updated, fmt)
                            break
                        except Exception:
                            continue
                    else:
                        raise ValueError(f"Unsupported date format for last_updated: {last_updated}")
                # Only check the first matching stock_level for this SKU+warehouse_id
                break

        # If current_stock < reorder_point, add alert
        if current_stock < reorder_point:
            result.append({
                "sku": sku,
                "name": name,
                "current_stock": current_stock,
                "reorder_point": reorder_point,
                "deficit": reorder_point - current_stock
            })

    return result

