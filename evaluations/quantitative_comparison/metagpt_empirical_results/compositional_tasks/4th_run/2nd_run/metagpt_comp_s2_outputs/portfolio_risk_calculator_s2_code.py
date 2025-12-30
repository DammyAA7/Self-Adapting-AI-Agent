def calculate_stock_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    volatility = (variance ** 0.5) * 100
    return volatility

def portfolio_risk_assessment(portfolio):
    """
    portfolio: dict, keys are stock names, values are dicts with 'prices' (list of floats) and 'allocation' (float)
    Returns: float, total portfolio risk as weighted sum of volatilities
    """
    total_risk = 0.0
    for stock, info in portfolio.items():
        prices = info.get('prices', [])
        allocation = info.get('allocation', 0.0)
        volatility = calculate_stock_volatility(prices)
        total_risk += volatility * allocation
    return total_risk