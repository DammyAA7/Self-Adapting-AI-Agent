#!/usr/bin/env python3
"""
Demo: Terminal Context with Generated Functions
Shows how generated functions persist in context for incremental building
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Terminal_Context.context_manager import ContextManager
from Utilities.performanceTester import performance_terminal_execute

def demo_incremental_function_generation():
    """
    Demonstrates how the terminal context allows generated functions
    to build on each other incrementally.
    """
    print("=" * 70)
    print("DEMO: Terminal Context for Incremental Function Generation")
    print("=" * 70)
    
    # Initialize context manager
    manager = ContextManager()
    print("\n1. Initialized Context Manager")
    
    # Simulate first generated function - basic calculation
    print("\n2. Generating first function: calculate_simple_interest")
    first_function = """
def calculate_simple_interest(principal, rate, time):
    '''
    Calculate simple interest.
    
    Args:
        principal: Initial amount
        rate: Interest rate (as decimal, e.g., 0.05 for 5%)
        time: Time period in years
    
    Returns:
        Simple interest amount
    '''
    return principal * rate * time
"""
    
    success = manager.add_generated_function("calculate_simple_interest", first_function, {
        'requirement': 'Calculate simple interest',
        'iterations': 1
    })
    print(f"   - Added: {success}")
    
    # Test the first function
    print("\n3. Testing first function:")
    result = manager.execute_in_context("""
result = calculate_simple_interest(1000, 0.05, 2)
print(f"Simple interest on $1000 at 5% for 2 years: ${result}")
""")
    print(f"   Output: {result['output']}")
    
    # Simulate second generated function - builds on the first
    print("\n4. Generating second function: calculate_compound_interest")
    second_function = """
def calculate_compound_interest(principal, rate, time, n=12):
    '''
    Calculate compound interest and compare with simple interest.
    Uses the previously defined calculate_simple_interest function!
    
    Args:
        principal: Initial amount
        rate: Annual interest rate (as decimal)
        time: Time period in years
        n: Compounding frequency per year (default monthly)
    
    Returns:
        Dictionary with compound interest, simple interest, and difference
    '''
    # Calculate compound interest
    compound_amount = principal * (1 + rate/n) ** (n * time)
    compound_interest = compound_amount - principal
    
    # Use the PREVIOUSLY GENERATED function!
    simple_interest = calculate_simple_interest(principal, rate, time)
    
    return {
        'compound': compound_interest,
        'simple': simple_interest,
        'difference': compound_interest - simple_interest,
        'total_amount': compound_amount
    }
"""
    
    success = manager.add_generated_function("calculate_compound_interest", second_function, {
        'requirement': 'Calculate compound interest using simple interest function',
        'iterations': 1
    })
    print(f"   - Added: {success}")
    
    # Test the second function (which uses the first)
    print("\n5. Testing second function (uses first function):")
    result = manager.execute_in_context("""
result = calculate_compound_interest(1000, 0.05, 2)
print(f"Compound interest: ${result['compound']:.2f}")
print(f"Simple interest: ${result['simple']:.2f}")
print(f"Difference: ${result['difference']:.2f}")
print(f"Total amount: ${result['total_amount']:.2f}")
""")
    print(f"   Output:\n{result['output']}")
    
    # Simulate third generated function - uses both previous functions
    print("\n6. Generating third function: calculate_investment_portfolio")
    third_function = """
def calculate_investment_portfolio(investments):
    '''
    Calculate returns for a portfolio of investments.
    Uses BOTH previously generated functions!
    
    Args:
        investments: List of investment dictionaries with keys:
                    - amount, rate, years, type ('simple' or 'compound')
    
    Returns:
        Portfolio summary with total returns
    '''
    total_returns = 0
    results = []
    
    for inv in investments:
        amount = inv['amount']
        rate = inv['rate']
        years = inv['years']
        inv_type = inv.get('type', 'compound')
        
        if inv_type == 'simple':
            # Use first generated function
            interest = calculate_simple_interest(amount, rate, years)
            total = amount + interest
        else:
            # Use second generated function
            result = calculate_compound_interest(amount, rate, years)
            interest = result['compound']
            total = result['total_amount']
        
        results.append({
            'type': inv_type,
            'principal': amount,
            'interest': interest,
            'total': total
        })
        total_returns += total
    
    return {
        'investments': results,
        'total_portfolio_value': total_returns,
        'total_interest_earned': total_returns - sum(inv['amount'] for inv in investments)
    }
"""
    
    success = manager.add_generated_function("calculate_investment_portfolio", third_function, {
        'requirement': 'Calculate portfolio using both previous functions',
        'iterations': 1
    })
    print(f"   - Added: {success}")
    
    # Test the third function (which uses both previous functions)
    print("\n7. Testing third function (uses both previous functions):")
    result = manager.execute_in_context("""
portfolio = [
    {'amount': 5000, 'rate': 0.04, 'years': 3, 'type': 'simple'},
    {'amount': 10000, 'rate': 0.05, 'years': 5, 'type': 'compound'},
    {'amount': 3000, 'rate': 0.03, 'years': 2, 'type': 'simple'}
]

result = calculate_investment_portfolio(portfolio)
print("Portfolio Analysis:")
print("-" * 40)
for i, inv in enumerate(result['investments'], 1):
    print(f"Investment {i} ({inv['type']}): ${inv['principal']:,.2f} -> ${inv['total']:,.2f}")
    print(f"  Interest earned: ${inv['interest']:,.2f}")
print("-" * 40)
print(f"Total portfolio value: ${result['total_portfolio_value']:,.2f}")
print(f"Total interest earned: ${result['total_interest_earned']:,.2f}")
""")
    print(f"\n{result['output']}")
    
    # Show all available functions
    print("\n8. All functions available in context:")
    functions = manager.list_available_functions()
    for func in functions:
        print(f"   - {func}")
    
    # Get session summary
    summary = manager.get_session_summary()
    print(f"\n9. Session Summary:")
    print(f"   - Functions defined: {summary['functions_defined']}")
    print(f"   - Total executions: {summary['executions']}")
    
    # Save the session
    session_file = manager.save_session("demo_session.json")
    print(f"\n10. Session saved to: {session_file}")
    
    # Performance test with terminal context
    print("\n11. Performance Test with Terminal Context:")
    perf_result = performance_terminal_execute(manager, """
# Performance test: Calculate for larger portfolio
large_portfolio = [{'amount': i*1000, 'rate': 0.04 + i*0.001, 'years': i, 'type': 'compound'} 
                   for i in range(1, 11)]
result = calculate_investment_portfolio(large_portfolio)
print(f"Large portfolio (10 investments): ${result['total_portfolio_value']:,.2f}")
""")
    print(f"   - Execution time: {perf_result['execution_time']:.3f} seconds")
    print(f"   - Memory peak: {perf_result['memory_peak'] / 1024:.1f} KB")
    print(f"   - Success: {perf_result['success']}")
    print(f"   - Context preserved: {perf_result['context_preserved']}")
    
    # Cleanup
    manager.terminate_all()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Each generated function remains available for the next!")
    print("This enables TRUE incremental development where complex systems")
    print("are built step-by-step, with each function building on previous ones.")
    print("=" * 70)

if __name__ == "__main__":
    demo_incremental_function_generation()