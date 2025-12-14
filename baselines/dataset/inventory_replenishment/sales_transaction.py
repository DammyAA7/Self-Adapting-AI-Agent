"""
Sales transaction records for inventory management
"""
from datetime import datetime


class SalesTransaction:
    """Sales record"""
    def __init__(self, transaction_id: str, sku: str, quantity_sold: int,
                 date: str, warehouse_id: str):
        self.transaction_id = transaction_id
        self.sku = sku
        self.quantity_sold = quantity_sold
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.warehouse_id = warehouse_id

    def __repr__(self):
        return f"Sale({self.sku}, qty={self.quantity_sold}, {self.date.date()})"
