
def portfolio_risk_assessment(portfolio: dict) -> float:
    '''
    Takes a dict where keys are stock names and values have 'prices' list and 'allocation' float.
    For each stock, calls calculate_stock_volatility(prices), multiplies by allocation, sums all weighted volatilities.
    Returns: float representing total portfolio risk as weighted sum.
    '''
    total_risk = 0.0
    for stock_data in portfolio.values():
        prices = stock_data.get('prices', [])
        allocation = stock_data.get('allocation', 0.0)
        volatility = calculate_stock_volatility(prices)
        weighted_volatility = volatility * allocation
        total_risk += weighted_volatility
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

