import math
from typing import Dict, List, Any

def calculate_stock_volatility(prices: List[float]) -> float:
    """
    Calculate the volatility of a stock given its price history.

    Args:
        prices (List[float]): List of historical prices.

    Returns:
        float: Volatility as a percentage (0.0 if not enough data).
    """
    if len(prices) < 2:
        return 0.0
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
    mean_return = sum(returns) / len(returns)
    variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
    volatility = math.sqrt(variance) * 100
    return volatility

def portfolio_risk_assessment(portfolio: Dict[str, Dict[str, Any]]) -> float:
    """
    Assess the total portfolio risk as the weighted sum of individual stock volatilities.

    Args:
        portfolio (Dict[str, Dict[str, Any]]): 
            Dictionary where keys are stock names and values are dicts with:
                - 'prices': List[float], historical prices for the stock
                - 'allocation': float, allocation weight for the stock

    Returns:
        float: Total portfolio risk as the weighted sum of volatilities.
    """
    total_risk = 0.0
    for stock, data in portfolio.items():
        prices = data.get('prices', [])
        allocation = data.get('allocation', 0.0)
        volatility = calculate_stock_volatility(prices)
        weighted_volatility = volatility * allocation
        total_risk += weighted_volatility
    return total_risk