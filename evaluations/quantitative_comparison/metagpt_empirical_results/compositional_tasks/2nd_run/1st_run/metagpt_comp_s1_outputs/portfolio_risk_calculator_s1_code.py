import math

def calculate_stock_volatility(prices):
    if len(prices) < 2:
        return 0.0
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    mean = sum(returns) / len(returns)
    variance = sum((r - mean) ** 2 for r in returns) / len(returns)
    return math.sqrt(variance) * 100