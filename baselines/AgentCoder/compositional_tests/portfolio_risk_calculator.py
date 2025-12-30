
def portfolio_risk_assessment(portfolio: dict) -> float:
    '''
    Takes a dict where keys are stock names and values have 'prices' list and 'allocation' float.
    For each stock, call calculate_stock_volatility(prices), multiply by allocation,
    sum all weighted volatilities. Returns: float representing total portfolio risk as weighted sum.
    Example:
    portfolio = {
        'AAPL': {'prices': [100, 101, 102], 'allocation': 0.6},
        'GOOG': {'prices': [200, 202, 201], 'allocation': 0.4},
    }
    '''
    import math

    # Chain-of-Thought:
    # 1. For each stock in the portfolio:
    #    a. Extract 'prices' and 'allocation'
    #    b. Call calculate_stock_volatility(prices)
    #    c. Multiply volatility by allocation
    # 2. Sum all weighted volatilities
    # 3. Return the total

    total_risk = 0.0
    for stock, info in portfolio.items():
        prices = info.get('prices', [])
        allocation = info.get('allocation', 0.0)
        # Defensive: skip if allocation <= 0 or prices invalid
        if allocation <= 0 or not isinstance(prices, list):
            continue
        volatility = calculate_stock_volatility(prices)
        total_risk += volatility * allocation

    return total_risk



# Test Session 1 function: calculate_stock_volatility
prices1 = [100.0, 102.0, 98.0, 101.0, 99.0]
vol1 = calculate_stock_volatility(prices1)
assert isinstance(vol1, float)
assert vol1 >= 0  # Volatility cannot be negative
assert vol1 < 100  # Reasonable volatility range

# Test edge cases
assert calculate_stock_volatility([]) == 0.0
assert calculate_stock_volatility([100.0]) == 0.0

# Test Session 2 function: portfolio_risk_assessment
portfolio = {
    'AAPL': {'prices': [150.0, 152.0, 148.0, 155.0], 'allocation': 0.6},
    'GOOGL': {'prices': [2800.0, 2820.0, 2790.0, 2850.0], 'allocation': 0.4}
}
portfolio_risk = portfolio_risk_assessment(portfolio)
assert isinstance(portfolio_risk, float)
assert portfolio_risk >= 0
assert portfolio_risk < 100

print('Portfolio Risk Calculator tests passed')

