"""
Demand Forecaster Module
Forecasts product demand using historical sales data
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta


class DemandForecaster:
    """Forecast product demand using various forecasting methods"""

    def __init__(self):
        """Initialize demand forecaster with default parameters"""
        self.seasonal_factors = {
            'spring': 1.0,
            'summer': 1.2,
            'fall': 1.1,
            'winter': 0.9
        }
        self.trend_weight = 0.3

    def forecast_demand(self, historical_data: List[Dict],
                       forecast_periods: int = 30,
                       method: str = 'moving_average') -> List[Dict]:
        """
        Forecast future demand based on historical data

        Args:
            historical_data: List of dicts with 'date' and 'quantity' sold
            forecast_periods: Number of periods to forecast
            method: Forecasting method ('moving_average', 'exponential', 'trend')

        Returns:
            List of forecasted demand dicts with date and predicted quantity
        """
        if not historical_data:
            return []

        if method == 'moving_average':
            return self._moving_average_forecast(historical_data, forecast_periods)
        elif method == 'exponential':
            return self._exponential_smoothing(historical_data, forecast_periods)
        elif method == 'trend':
            return self._trend_forecast(historical_data, forecast_periods)
        else:
            return self._moving_average_forecast(historical_data, forecast_periods)

    def _moving_average_forecast(self, data: List[Dict],
                                 periods: int, window: int = 7) -> List[Dict]:
        """Simple moving average forecast"""
        if len(data) < window:
            window = len(data)

        recent_values = [d['quantity'] for d in data[-window:]]
        average = sum(recent_values) / len(recent_values)

        last_date = datetime.fromisoformat(data[-1]['date']) if isinstance(data[-1]['date'], str) else data[-1]['date']

        forecasts = []
        for i in range(1, periods + 1):
            forecast_date = last_date + timedelta(days=i)
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_quantity': round(average, 2),
                'method': 'moving_average'
            })

        return forecasts

    def _exponential_smoothing(self, data: List[Dict],
                              periods: int, alpha: float = 0.3) -> List[Dict]:
        """Exponential smoothing forecast"""
        if not data:
            return []

        # Initialize with first value
        smoothed = data[0]['quantity']

        # Apply exponential smoothing to historical data
        for record in data[1:]:
            smoothed = alpha * record['quantity'] + (1 - alpha) * smoothed

        last_date = datetime.fromisoformat(data[-1]['date']) if isinstance(data[-1]['date'], str) else data[-1]['date']

        forecasts = []
        for i in range(1, periods + 1):
            forecast_date = last_date + timedelta(days=i)
            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_quantity': round(smoothed, 2),
                'method': 'exponential_smoothing'
            })

        return forecasts

    def _trend_forecast(self, data: List[Dict], periods: int) -> List[Dict]:
        """Linear trend-based forecast"""
        if len(data) < 2:
            return []

        trend = self.calculate_trend(data)
        base_value = data[-1]['quantity']
        last_date = datetime.fromisoformat(data[-1]['date']) if isinstance(data[-1]['date'], str) else data[-1]['date']

        forecasts = []
        for i in range(1, periods + 1):
            forecast_date = last_date + timedelta(days=i)
            predicted = base_value + (trend * i)
            predicted = max(0, predicted)  # Ensure non-negative

            forecasts.append({
                'date': forecast_date.isoformat(),
                'predicted_quantity': round(predicted, 2),
                'method': 'trend',
                'trend': trend
            })

        return forecasts

    def calculate_trend(self, historical_data: List[Dict]) -> float:
        """
        Calculate trend coefficient from historical data

        Args:
            historical_data: List of sales records

        Returns:
            Trend coefficient (daily change rate)
        """
        if len(historical_data) < 2:
            return 0.0

        quantities = [d['quantity'] for d in historical_data]
        n = len(quantities)

        # Simple linear regression
        x_mean = (n - 1) / 2
        y_mean = sum(quantities) / n

        numerator = sum((i - x_mean) * (quantities[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        trend = numerator / denominator
        return round(trend, 4)

    def seasonal_adjustment(self, base_demand: float,
                          season: str) -> float:
        """
        Apply seasonal adjustment to base demand

        Args:
            base_demand: Base forecasted demand
            season: Season name ('spring', 'summer', 'fall', 'winter')

        Returns:
            Seasonally adjusted demand
        """
        factor = self.seasonal_factors.get(season.lower(), 1.0)
        adjusted = base_demand * factor
        return round(adjusted, 2)
