"""
Data Scaler Class
Handles data normalization and scaling
"""
import math
from typing import List


class DataScaler:
    """Handles data normalization and scaling"""

    def __init__(self):
        self.mean = None
        self.std = None
        self.min_val = None
        self.max_val = None

    def fit_standard_scaler(self, data: List[float]) -> None:
        """Fit standard scaler (z-score normalization)"""
        self.mean = sum(data) / len(data)
        variance = sum((x - self.mean) ** 2 for x in data) / len(data)
        self.std = math.sqrt(variance)

    def transform_standard(self, data: List[float]) -> List[float]:
        """Apply standard scaling transformation"""
        if self.mean is None or self.std is None:
            raise ValueError("Scaler not fitted. Call fit_standard_scaler first.")
        return [(x - self.mean) / self.std for x in data]

    def fit_minmax_scaler(self, data: List[float]) -> None:
        """Fit min-max scaler (0-1 normalization)"""
        self.min_val = min(data)
        self.max_val = max(data)

    def transform_minmax(self, data: List[float]) -> List[float]:
        """Apply min-max scaling transformation"""
        if self.min_val is None or self.max_val is None:
            raise ValueError("Scaler not fitted. Call fit_minmax_scaler first.")
        range_val = self.max_val - self.min_val
        if range_val == 0:
            return [0.0] * len(data)
        return [(x - self.min_val) / range_val for x in data]
