#
# Session 2 code (MetaGPT)
import math

def calculate_stock_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    volatility = math.sqrt(variance) * 100
    return volatility

def portfolio_risk_assessment(portfolio):
    """
    portfolio: dict, keys are stock names, values are dicts with 'prices' (list of floats) and 'allocation' (float)
    Returns: float, total portfolio risk as weighted sum of volatilities
    """
    total_risk = 0.0
    for stock, data in portfolio.items():
        prices = data.get('prices', [])
        allocation = data.get('allocation', 0.0)
        volatility = calculate_stock_volatility(prices)
        weighted_volatility = volatility * allocation
        total_risk += weighted_volatility
    return total_risk

# Ground-truth test

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

