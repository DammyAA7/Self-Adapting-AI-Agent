"""
Machine Learning Utilities
Common ML operations and data preprocessing functions
"""
import numpy as np
from typing import List, Tuple, Dict, Any
import math


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


class FeatureEngineer:
    """Feature engineering operations"""
    
    @staticmethod
    def create_polynomial_features(data: List[float], degree: int = 2) -> List[List[float]]:
        """Create polynomial features up to specified degree"""
        features = []
        for x in data:
            feature_row = [x ** i for i in range(1, degree + 1)]
            features.append(feature_row)
        return features
    
    @staticmethod
    def create_interaction_features(data1: List[float], data2: List[float]) -> List[float]:
        """Create interaction features between two variables"""
        if len(data1) != len(data2):
            raise ValueError("Both datasets must have same length")
        return [x1 * x2 for x1, x2 in zip(data1, data2)]
    
    @staticmethod
    def binning(data: List[float], num_bins: int) -> List[int]:
        """Convert continuous data into discrete bins"""
        if num_bins <= 0:
            raise ValueError("Number of bins must be positive")
        
        min_val, max_val = min(data), max(data)
        bin_width = (max_val - min_val) / num_bins
        
        bins = []
        for x in data:
            bin_idx = min(int((x - min_val) / bin_width), num_bins - 1)
            bins.append(bin_idx)
        return bins


class ModelEvaluator:
    """Model evaluation metrics and utilities"""
    
    @staticmethod
    def calculate_mse(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate Mean Squared Error"""
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and true values must have same length")
        
        squared_errors = [(true - pred) ** 2 for true, pred in zip(y_true, y_pred)]
        return sum(squared_errors) / len(squared_errors)
    
    @staticmethod
    def calculate_rmse(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate Root Mean Squared Error"""
        mse = ModelEvaluator.calculate_mse(y_true, y_pred)
        return math.sqrt(mse)
    
    @staticmethod
    def calculate_mae(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate Mean Absolute Error"""
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and true values must have same length")
        
        absolute_errors = [abs(true - pred) for true, pred in zip(y_true, y_pred)]
        return sum(absolute_errors) / len(absolute_errors)
    
    @staticmethod
    def calculate_r_squared(y_true: List[float], y_pred: List[float]) -> float:
        """Calculate R-squared (coefficient of determination)"""
        if len(y_true) != len(y_pred):
            raise ValueError("Predictions and true values must have same length")
        
        y_mean = sum(y_true) / len(y_true)
        ss_tot = sum((y - y_mean) ** 2 for y in y_true)
        ss_res = sum((y_true[i] - y_pred[i]) ** 2 for i in range(len(y_true)))
        
        if ss_tot == 0:
            return 1.0 if ss_res == 0 else 0.0
        
        return 1 - (ss_res / ss_tot)


# Usage examples
if __name__ == "__main__":
    # Example data
    sample_data = [1.0, 2.5, 3.7, 4.2, 5.8, 6.1, 7.3, 8.9]
    predictions = [1.1, 2.3, 3.9, 4.0, 5.9, 6.2, 7.1, 8.8]
    
    # Scaling example
    scaler = DataScaler()
    scaler.fit_standard_scaler(sample_data)
    scaled_data = scaler.transform_standard(sample_data)
    
    # Feature engineering
    poly_features = FeatureEngineer.create_polynomial_features(sample_data, degree=3)
    bins = FeatureEngineer.binning(sample_data, num_bins=4)
    
    # Model evaluation
    mse = ModelEvaluator.calculate_mse(sample_data, predictions)
    rmse = ModelEvaluator.calculate_rmse(sample_data, predictions)
    r2 = ModelEvaluator.calculate_r_squared(sample_data, predictions)