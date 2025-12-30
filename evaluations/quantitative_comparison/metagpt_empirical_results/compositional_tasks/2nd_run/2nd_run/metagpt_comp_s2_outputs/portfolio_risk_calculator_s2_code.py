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