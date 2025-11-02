"""
Purchase order management for inventory restocking
"""
from datetime import datetime


class PurchaseOrder:
    """Purchase order for restocking"""
    def __init__(self, order_id: str, sku: str, quantity: int, order_date: str):
        self.order_id = order_id
        self.sku = sku
        self.quantity = quantity
        self.order_date = datetime.strptime(order_date, "%Y-%m-%d")
        self.status = "pending"  # pending, shipped, received

    def __repr__(self):
        return f"PO({self.order_id}, {self.sku}, qty={self.quantity}, {self.status})"
