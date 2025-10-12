"""
Stock level tracking for inventory management
"""
from datetime import datetime


class StockLevel:
    """Current inventory level"""
    def __init__(self, sku: str, warehouse_id: str, quantity: int, last_updated: str):
        self.sku = sku
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.last_updated = datetime.strptime(last_updated, "%Y-%m-%d %H:%M:%S")

    def is_low_stock(self, reorder_point: int) -> bool:
        """Check if stock is below reorder point"""
        return self.quantity < reorder_point

    def __repr__(self):
        return f"StockLevel({self.sku}, WH:{self.warehouse_id}, qty={self.quantity})"
