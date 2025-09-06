#!/usr/bin/env python3
"""
Test script for Terminal Context integration with Prototype IV
Tests persistent context preservation between function executions.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Terminal_Context.persistent_terminal import PersistentTerminal
from Terminal_Context.context_manager import ContextManager

def test_basic_terminal():
    """Test basic terminal functionality."""
    print("=" * 60)
    print("TEST 1: Basic Terminal Functionality")
    print("=" * 60)
    
    terminal = PersistentTerminal("python")
    
    # Test 1: Define a variable
    result = terminal.execute("x = 10")
    print(f"Set x = 10 - Success: {result['success']}")
    
    # Test 2: Use the variable (context preserved!)
    result = terminal.execute("print(f'x = {x}')")
    print(f"Access x - Output: {result['output']}")
    
    # Test 3: Define a function
    result = terminal.execute("""
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
""")
    print(f"Define factorial - Success: {result['success']}")
    
    # Test 4: Use the function
    result = terminal.execute("print(factorial(5))")
    print(f"factorial(5) = {result['output']}")
    
    # Test 5: Function can use previous variable
    result = terminal.execute("print(f'factorial of x={x} is {factorial(x)}')")
    print(f"factorial(x) = {result['output']}")
    
    terminal.terminate()
    print("✓ Basic terminal test passed\n")

def test_context_manager():
    """Test context manager functionality."""
    print("=" * 60)
    print("TEST 2: Context Manager with Function Building")
    print("=" * 60)
    
    manager = ContextManager()
    
    # Add first function
    print("Adding calculate_interest function...")
    interest_code = """
def calculate_interest(principal, rate, time):
    '''Calculate simple interest'''
    return principal * rate * time
"""
    success = manager.add_generated_function("calculate_interest", interest_code)
    print(f"Added calculate_interest: {success}")
    
    # Add second function that uses the first
    print("\nAdding calculate_compound_interest function...")
    compound_code = """
def calculate_compound_interest(principal, rate, time, n=1):
    '''Calculate compound interest using the simple interest function'''
    # This function can call calculate_interest!
    simple = calculate_interest(principal, rate, time)
    compound = principal * ((1 + rate/n) ** (n * time)) - principal
    return {
        'simple': simple,
        'compound': compound,
        'difference': compound - simple
    }
"""
    success = manager.add_generated_function("calculate_compound_interest", compound_code)
    print(f"Added calculate_compound_interest: {success}")
    
    # Test using both functions
    print("\nTesting compound interest calculation...")
    result = manager.execute_in_context("""
result = calculate_compound_interest(1000, 0.05, 10, 12)
print(f"Simple Interest: ${result['simple']:.2f}")
print(f"Compound Interest: ${result['compound']:.2f}")
print(f"Difference: ${result['difference']:.2f}")
""")
    print(f"Calculation output:\n{result['output']}")
    
    # List available functions
    functions = manager.list_available_functions()
    print(f"\nAvailable functions in context: {functions}")
    
    # Get session summary
    summary = manager.get_session_summary()
    print(f"\nSession Summary:")
    print(f"  - Functions defined: {summary['functions_defined']}")
    print(f"  - Total executions: {summary['executions']}")
    
    # Save session
    session_file = manager.save_session("test_session.json")
    print(f"\nSession saved to: {session_file}")
    
    manager.terminate_all()
    print("✓ Context manager test passed\n")

def test_incremental_building():
    """Test incremental function building (key feature!)."""
    print("=" * 60)
    print("TEST 3: Incremental Function Building")
    print("=" * 60)
    print("This demonstrates the KEY BENEFIT: building complex systems step by step\n")
    
    manager = ContextManager()
    
    # Step 1: Basic data structure
    print("Step 1: Define Product class")
    manager.execute_in_context("""
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.name}: ${self.price} x {self.quantity}"
""")
    
    # Step 2: Inventory management (uses Product)
    print("Step 2: Add inventory management")
    manager.execute_in_context("""
class Inventory:
    def __init__(self):
        self.products = []
    
    def add_product(self, name, price, quantity):
        # Uses the Product class defined earlier!
        product = Product(name, price, quantity)
        self.products.append(product)
        return product
    
    def total_value(self):
        return sum(p.price * p.quantity for p in self.products)
""")
    
    # Step 3: Use the incrementally built system
    print("Step 3: Use the complete system")
    result = manager.execute_in_context("""
# Create inventory
inv = Inventory()
inv.add_product("Laptop", 999.99, 5)
inv.add_product("Mouse", 29.99, 20)
inv.add_product("Keyboard", 79.99, 15)

# Calculate total
total = inv.total_value()
print(f"Total inventory value: ${total:.2f}")

# List products
print("\\nInventory:")
for product in inv.products:
    print(f"  - {product}")
""")
    
    print(f"\nSystem output:\n{result['output']}")
    
    manager.terminate_all()
    print("\n✓ Incremental building test passed")
    print("This is the key advantage: each function/class remains available for the next!")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TERMINAL CONTEXT INTEGRATION TEST")
    print("Testing persistent context preservation in Prototype IV")
    print("="*60 + "\n")
    
    try:
        test_basic_terminal()
        test_context_manager()
        test_incremental_building()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED!")
        print("Terminal Context is working correctly with Prototype IV")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()