"""
Product catalog information for inventory management
"""


class Product:
    """Product catalog information"""
    def __init__(self, sku: str, name: str, category: str, reorder_point: int, lead_time_days: int):
        self.sku = sku
        self.name = name
        self.category = category
        self.reorder_point = reorder_point  # Minimum stock before reorder
        self.lead_time_days = lead_time_days  # Days to receive new stock

    def __repr__(self):
        return f"Product({self.sku}, {self.name}, reorder={self.reorder_point})"
