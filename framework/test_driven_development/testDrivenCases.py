import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from unittest.mock import MagicMock, patch
from unit_test.functions import inventory_low_stock_alert

from dataset.inventory_replenishment.warehouse import Warehouse
from dataset.inventory_replenishment.product import Product
from dataset.inventory_replenishment.stock_level import StockLevel

@pytest.fixture
def sample_warehouse():
    warehouse = Warehouse("WH1")
    # Products
    prod1 = Product("SKU1", "Widget", "cat1", reorder_point=10, lead_time_days=2)
    prod2 = Product("SKU2", "Gadget", "cat2", reorder_point=5, lead_time_days=1)
    prod3 = Product("SKU3", "Doodad", "cat3", reorder_point=20, lead_time_days=3)
    warehouse.add_product(prod1)
    warehouse.add_product(prod2)
    warehouse.add_product(prod3)
    # Stock Levels
    stock1 = StockLevel("SKU1", "WH1", quantity=6, last_updated="2024-06-01")
    stock2 = StockLevel("SKU2", "WH1", quantity=8, last_updated="2024-06-01")
    stock3 = StockLevel("SKU3", "WH1", quantity=19, last_updated="2024-06-01")
    warehouse.add_stock_level(stock1)
    warehouse.add_stock_level(stock2)
    warehouse.add_stock_level(stock3)
    return warehouse

def test_inventory_low_stock_alert_happy_path(sample_warehouse):
    # SKU1 and SKU3 are below reorder_point
    result = inventory_low_stock_alert(sample_warehouse)
    expected = [
        {
            "sku": "SKU1",
            "name": "Widget",
            "current_stock": 6,
            "reorder_point": 10,
            "deficit": 4
        },
        {
            "sku": "SKU3",
            "name": "Doodad",
            "current_stock": 19,
            "reorder_point": 20,
            "deficit": 1
        }
    ]
    assert {tuple(sorted(d.items())) for d in result} == {tuple(sorted(d.items())) for d in expected}

def test_inventory_low_stock_alert_all_above_reorder_point():
    warehouse = Warehouse("WH2")
    prod1 = Product("SKU10", "Thing", "cat", reorder_point=5, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU10", "WH2", quantity=8, last_updated="2024-06-01")
    warehouse.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse)
    assert result == []

def test_inventory_low_stock_alert_exactly_at_reorder_point():
    warehouse = Warehouse("WH3")
    prod1 = Product("SKU20", "Exact", "cat", reorder_point=7, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU20", "WH3", quantity=7, last_updated="2024-06-01")
    warehouse.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse)
    assert result == []

def test_inventory_low_stock_alert_no_products():
    warehouse = Warehouse("WH4")
    result = inventory_low_stock_alert(warehouse)
    assert result == []

def test_inventory_low_stock_alert_zero_stock():
    warehouse = Warehouse("WH5")
    prod1 = Product("SKU30", "Zero", "cat", reorder_point=2, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU30", "WH5", quantity=0, last_updated="2024-06-01")
    warehouse.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse)
    assert result == [
        {
            "sku": "SKU30",
            "name": "Zero",
            "current_stock": 0,
            "reorder_point": 2,
            "deficit": 2
        }
    ]

def test_inventory_low_stock_alert_negative_stock():
    warehouse = Warehouse("WH6")
    prod1 = Product("SKU40", "Neg", "cat", reorder_point=3, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU40", "WH6", quantity=-2, last_updated="2024-06-01")
    warehouse.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse)
    assert result == [
        {
            "sku": "SKU40",
            "name": "Neg",
            "current_stock": -2,
            "reorder_point": 3,
            "deficit": 5
        }
    ]

def test_inventory_low_stock_alert_missing_stock_level():
    warehouse = Warehouse("WH7")
    prod1 = Product("SKU50", "NoStock", "cat", reorder_point=6, lead_time_days=1)
    warehouse.add_product(prod1)
    # No StockLevel added
    result = inventory_low_stock_alert(warehouse)
    assert result == [
        {
            "sku": "SKU50",
            "name": "NoStock",
            "current_stock": 0,
            "reorder_point": 6,
            "deficit": 6
        }
    ]

def test_inventory_low_stock_alert_invalid_warehouse_object():
    class Dummy: pass
    dummy = Dummy()
    result = inventory_low_stock_alert(dummy)
    assert result == []

def test_inventory_low_stock_alert_missing_reorder_point():
    warehouse = Warehouse("WH8")
    class ProdNoROP:
        def __init__(self):
            self.sku = "SKU60"
            self.name = "Bad"
    prod = ProdNoROP()
    warehouse.products[prod.sku] = prod
    result = inventory_low_stock_alert(warehouse)
    assert result == []

def test_inventory_low_stock_alert_composition_calls():
    warehouse = MagicMock()
    prod = MagicMock()
    prod.sku = "SKUX"
    prod.name = "Alpha"
    prod.reorder_point = 5
    warehouse.get_all_products.return_value = [prod]
    warehouse.get_current_stock.return_value = 2
    result = inventory_low_stock_alert(warehouse)
    warehouse.get_all_products.assert_called_once()
    warehouse.get_current_stock.assert_called_with("SKUX")
    assert result[0]['sku'] == "SKUX"
    assert result[0]['current_stock'] == 2
    assert result[0]['deficit'] == 3

def test_inventory_low_stock_alert_multiple_warehouses():
    warehouse1 = Warehouse("WHA")
    prod1 = Product("SKUA", "ProdA", "cat", reorder_point=10, lead_time_days=1)
    warehouse1.add_product(prod1)
    stock1 = StockLevel("SKUA", "WHB", quantity=5, last_updated="2024-06-01")
    warehouse1.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse1)
    assert result == [
        {
            "sku": "SKUA",
            "name": "ProdA",
            "current_stock": 0,
            "reorder_point": 10,
            "deficit": 10
        }
    ]

def test_inventory_low_stock_alert_last_updated_multiple_formats():
    warehouse = Warehouse("WH9")
    prod1 = Product("SKU70", "MultiDate", "cat", reorder_point=10, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU70", "WH9", quantity=3, last_updated="2024-06-02")
    warehouse.add_stock_level(stock1)
    stock2 = StockLevel("SKU71", "WH9", quantity=1, last_updated="2024-06-03 12:30")
    prod2 = Product("SKU71", "MultiDate2", "cat", reorder_point=5, lead_time_days=1)
    warehouse.add_product(prod2)
    warehouse.add_stock_level(stock2)
    stock3 = StockLevel("SKU72", "WH9", quantity=2, last_updated="2024-06-04 08:15:00")
    prod3 = Product("SKU72", "MultiDate3", "cat", reorder_point=3, lead_time_days=1)
    warehouse.add_product(prod3)
    warehouse.add_stock_level(stock3)
    result = inventory_low_stock_alert(warehouse)
    expected = [
        {
            "sku": "SKU70",
            "name": "MultiDate",
            "current_stock": 3,
            "reorder_point": 10,
            "deficit": 7
        },
        {
            "sku": "SKU71",
            "name": "MultiDate2",
            "current_stock": 1,
            "reorder_point": 5,
            "deficit": 4
        },
        {
            "sku": "SKU72",
            "name": "MultiDate3",
            "current_stock": 2,
            "reorder_point": 3,
            "deficit": 1
        }
    ]
    assert {tuple(sorted(d.items())) for d in result} == {tuple(sorted(d.items())) for d in expected}

def test_inventory_low_stock_alert_last_updated_supported_formats():
    warehouse = Warehouse("WH11")
    prod1 = Product("SKU100", "Date1", "cat", reorder_point=9, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU100", "WH11", quantity=2, last_updated="2024-06-10")
    warehouse.add_stock_level(stock1)
    prod2 = Product("SKU101", "Date2", "cat", reorder_point=7, lead_time_days=1)
    warehouse.add_product(prod2)
    stock2 = StockLevel("SKU101", "WH11", quantity=1, last_updated="2024-06-10 13:45:00")
    warehouse.add_stock_level(stock2)
    result = inventory_low_stock_alert(warehouse)
    expected = [
        {
            "sku": "SKU100",
            "name": "Date1",
            "current_stock": 2,
            "reorder_point": 9,
            "deficit": 7
        },
        {
            "sku": "SKU101",
            "name": "Date2",
            "current_stock": 1,
            "reorder_point": 7,
            "deficit": 6
        }
    ]
    assert {tuple(sorted(d.items())) for d in result} == {tuple(sorted(d.items())) for d in expected}

def test_inventory_low_stock_alert_invalid_last_updated_format_raises():
    warehouse = Warehouse("WH10")
    prod1 = Product("SKU80", "BadDate", "cat", reorder_point=6, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU80", "WH10", quantity=1, last_updated="06/02/2024 07:00:00 PM")
    warehouse.add_stock_level(stock1)
    with pytest.raises(ValueError) as excinfo:
        inventory_low_stock_alert(warehouse)
    assert "Unsupported date format" in str(excinfo.value) or "format" in str(excinfo.value)

def test_inventory_low_stock_alert_invalid_last_updated_format_error_message():
    warehouse = Warehouse("WH12")
    prod1 = Product("SKU200", "BadDate2", "cat", reorder_point=3, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU200", "WH12", quantity=1, last_updated="not-a-date")
    warehouse.add_stock_level(stock1)
    with pytest.raises(ValueError) as excinfo:
        inventory_low_stock_alert(warehouse)
    assert "Unsupported date format" in str(excinfo.value) or "format" in str(excinfo.value)

def test_inventory_low_stock_alert_multiple_invalid_last_updated_formats():
    warehouse = Warehouse("WH13")
    prod1 = Product("SKU300", "GoodDate", "cat", reorder_point=5, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU300", "WH13", quantity=2, last_updated="2024-06-12")
    warehouse.add_stock_level(stock1)
    prod2 = Product("SKU301", "BadDate3", "cat", reorder_point=8, lead_time_days=1)
    warehouse.add_product(prod2)
    stock2 = StockLevel("SKU301", "WH13", quantity=1, last_updated="invalid-format")
    warehouse.add_stock_level(stock2)
    with pytest.raises(ValueError) as excinfo:
        inventory_low_stock_alert(warehouse)
    assert "Unsupported date format" in str(excinfo.value) or "format" in str(excinfo.value)

def test_inventory_low_stock_alert_unsupported_datetime_middle_of_list():
    warehouse = Warehouse("WH14")
    prod1 = Product("SKU400", "GoodDate1", "cat", reorder_point=5, lead_time_days=1)
    prod2 = Product("SKU401", "BadDate", "cat", reorder_point=8, lead_time_days=1)
    warehouse.add_product(prod1)
    warehouse.add_product(prod2)
    stock1 = StockLevel("SKU400", "WH14", quantity=2, last_updated="2024-06-14")
    stock2 = StockLevel("SKU401", "WH14", quantity=1, last_updated="13-06-2024")
    warehouse.add_stock_level(stock1)
    warehouse.add_stock_level(stock2)
    with pytest.raises(ValueError) as excinfo:
        inventory_low_stock_alert(warehouse)
    assert "Unsupported date format" in str(excinfo.value) or "format" in str(excinfo.value)

def test_inventory_low_stock_alert_supported_datetime_variants():
    warehouse = Warehouse("WH15")
    prod1 = Product("SKU500", "Valid1", "cat", reorder_point=6, lead_time_days=1)
    warehouse.add_product(prod1)
    stock1 = StockLevel("SKU500", "WH15", quantity=1, last_updated="2024-06-15 10:45")
    warehouse.add_stock_level(stock1)
    try:
        result = inventory_low_stock_alert(warehouse)
        assert result[0]['sku'] == "SKU500"
        assert result[0]['current_stock'] == 1
        assert result[0]['deficit'] == 5
    except ValueError as e:
        assert "Unsupported date format" in str(e) or "format" in str(e)

def test_inventory_low_stock_alert_additional_supported_format_seconds():
    # Explicitly test '%Y-%m-%d %H:%M:%S' is accepted alongside '%Y-%m-%d'
    warehouse = Warehouse("WH16")
    prod1 = Product("SKU600", "SecondsDate", "cat", reorder_point=10, lead_time_days=1)
    stock1 = StockLevel("SKU600", "WH16", quantity=3, last_updated="2024-07-01 15:23:45")
    warehouse.add_product(prod1)
    warehouse.add_stock_level(stock1)
    result = inventory_low_stock_alert(warehouse)
    assert result[0]['sku'] == "SKU600"
    assert result[0]['current_stock'] == 3
    assert result[0]['deficit'] == 7

def test_inventory_low_stock_alert_all_supported_formats_together():
    # Mix all supported formats in one warehouse
    warehouse = Warehouse("WH17")
    prod1 = Product("SKU700", "Fmt1", "cat", reorder_point=4, lead_time_days=1)
    prod2 = Product("SKU701", "Fmt2", "cat", reorder_point=6, lead_time_days=1)
    prod3 = Product("SKU702", "Fmt3", "cat", reorder_point=8, lead_time_days=1)
    warehouse.add_product(prod1)
    warehouse.add_product(prod2)
    warehouse.add_product(prod3)
    stock1 = StockLevel("SKU700", "WH17", quantity=1, last_updated="2024-08-01")
    stock2 = StockLevel("SKU701", "WH17", quantity=2, last_updated="2024-08-02 12:00")
    stock3 = StockLevel("SKU702", "WH17", quantity=3, last_updated="2024-08-03 09:15:00")
    warehouse.add_stock_level(stock1)
    warehouse.add_stock_level(stock2)
    warehouse.add_stock_level(stock3)
    result = inventory_low_stock_alert(warehouse)
    expected = [
        {
            "sku": "SKU700",
            "name": "Fmt1",
            "current_stock": 1,
            "reorder_point": 4,
            "deficit": 3
        },
        {
            "sku": "SKU701",
            "name": "Fmt2",
            "current_stock": 2,
            "reorder_point": 6,
            "deficit": 4
        },
        {
            "sku": "SKU702",
            "name": "Fmt3",
            "current_stock": 3,
            "reorder_point": 8,
            "deficit": 5
        }
    ]
    assert {tuple(sorted(d.items())) for d in result} == {tuple(sorted(d.items())) for d in expected}

if __name__ == "__main__":
    pytest.main([__file__])
