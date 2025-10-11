"""
E-Commerce Inventory Management System
Retail domain codebase for self-evolution testing
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


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


class Warehouse:
    """Warehouse inventory management"""
    def __init__(self, warehouse_id: str = "WH01"):
        self.warehouse_id = warehouse_id
        self.products: Dict[str, Product] = {}
        self.stock_levels: List[StockLevel] = []
        self.sales_history: List[SalesTransaction] = []
        self.purchase_orders: List[PurchaseOrder] = []

    def add_product(self, product: Product):
        """Add product to catalog"""
        self.products[product.sku] = product

    def add_stock_level(self, stock: StockLevel):
        """Update stock level"""
        # Remove old stock level for same SKU/warehouse
        self.stock_levels = [s for s in self.stock_levels
                            if not (s.sku == stock.sku and s.warehouse_id == stock.warehouse_id)]
        self.stock_levels.append(stock)

    def add_sale(self, sale: SalesTransaction):
        """Record a sale"""
        self.sales_history.append(sale)

    def add_purchase_order(self, po: PurchaseOrder):
        """Create a purchase order"""
        self.purchase_orders.append(po)

    def get_product(self, sku: str) -> Optional[Product]:
        """Retrieve product by SKU"""
        return self.products.get(sku)

    def get_current_stock(self, sku: str, warehouse_id: str = None) -> int:
        """Get current stock quantity for a product"""
        wh_id = warehouse_id or self.warehouse_id
        for stock in self.stock_levels:
            if stock.sku == sku and stock.warehouse_id == wh_id:
                return stock.quantity
        return 0

    def get_sales_last_n_days(self, sku: str, days: int = 30) -> List[SalesTransaction]:
        """Get sales history for last N days"""
        cutoff = datetime.now() - timedelta(days=days)
        return [s for s in self.sales_history
                if s.sku == sku and s.date >= cutoff]

    def get_all_products(self) -> List[Product]:
        """Get all products in catalog"""
        return list(self.products.values())

    def get_low_stock_products(self) -> List[Tuple[Product, int]]:
        """Get products below reorder point"""
        low_stock = []
        for product in self.products.values():
            current = self.get_current_stock(product.sku)
            if current < product.reorder_point:
                low_stock.append((product, current))
        return low_stock

    def calculate_daily_sales_rate(self, sku: str, days: int = 30) -> float:
        """Calculate average daily sales for a product"""
        sales = self.get_sales_last_n_days(sku, days)
        if not sales:
            return 0.0
        total_sold = sum(s.quantity_sold for s in sales)
        return total_sold / days

    def __repr__(self):
        return f"Warehouse({self.warehouse_id}, {len(self.products)} products, {len(self.sales_history)} sales)"


# Sample data for testing
def create_sample_warehouse():
    """Create sample warehouse with test data"""
    warehouse = Warehouse("WH01")

    # Add products
    warehouse.add_product(Product("SKU001", "Laptop Dell XPS 15", "Electronics", 10, 7))
    warehouse.add_product(Product("SKU002", "iPhone 15 Pro", "Electronics", 15, 5))
    warehouse.add_product(Product("SKU003", "Office Chair", "Furniture", 5, 14))
    warehouse.add_product(Product("SKU004", "Wireless Mouse", "Accessories", 20, 3))
    warehouse.add_product(Product("SKU005", "USB-C Cable", "Accessories", 50, 2))
    warehouse.add_product(Product("SKU006", "Monitor 27inch", "Electronics", 8, 10))

    # Add current stock levels
    warehouse.add_stock_level(StockLevel("SKU001", "WH01", 8, "2025-10-09 10:00:00"))  # Below reorder
    warehouse.add_stock_level(StockLevel("SKU002", "WH01", 12, "2025-10-09 10:00:00"))  # Below reorder
    warehouse.add_stock_level(StockLevel("SKU003", "WH01", 15, "2025-10-09 10:00:00"))  # Above reorder
    warehouse.add_stock_level(StockLevel("SKU004", "WH01", 18, "2025-10-09 10:00:00"))  # Below reorder
    warehouse.add_stock_level(StockLevel("SKU005", "WH01", 45, "2025-10-09 10:00:00"))  # Below reorder
    warehouse.add_stock_level(StockLevel("SKU006", "WH01", 6, "2025-10-09 10:00:00"))  # Below reorder

    # Add sales history (last 30 days)
    base_date = datetime.now()
    for i in range(30):
        sale_date = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
        # SKU001: 1-2 per day
        warehouse.add_sale(SalesTransaction(f"TX{i*10+1}", "SKU001", 1 + (i % 2), sale_date, "WH01"))
        # SKU002: 2-3 per day (high velocity)
        warehouse.add_sale(SalesTransaction(f"TX{i*10+2}", "SKU002", 2 + (i % 2), sale_date, "WH01"))
        # SKU004: 3-5 per day (very high velocity)
        warehouse.add_sale(SalesTransaction(f"TX{i*10+3}", "SKU004", 3 + (i % 3), sale_date, "WH01"))
        # SKU005: 5-8 per day (extremely high velocity)
        warehouse.add_sale(SalesTransaction(f"TX{i*10+4}", "SKU005", 5 + (i % 4), sale_date, "WH01"))

    # SKU003 and SKU006: Low sales
    for i in range(0, 30, 5):
        sale_date = (base_date - timedelta(days=i)).strftime("%Y-%m-%d")
        warehouse.add_sale(SalesTransaction(f"TX{i*10+5}", "SKU003", 1, sale_date, "WH01"))
        warehouse.add_sale(SalesTransaction(f"TX{i*10+6}", "SKU006", 1, sale_date, "WH01"))

    return warehouse


if __name__ == "__main__":
    warehouse = create_sample_warehouse()
    print(warehouse)
    print(f"\nAll products: {[p.name for p in warehouse.get_all_products()]}")
    print(f"\nLow stock products:")
    for product, qty in warehouse.get_low_stock_products():
        print(f"  {product.sku}: {qty} (reorder at {product.reorder_point})")

    print(f"\nSKU002 daily sales rate (30 days): {warehouse.calculate_daily_sales_rate('SKU002', 30):.2f}")
    print(f"SKU005 daily sales rate (30 days): {warehouse.calculate_daily_sales_rate('SKU005', 30):.2f}")
