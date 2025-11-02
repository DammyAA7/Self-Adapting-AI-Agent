"""
Model Evaluator Class
Model evaluation metrics and utilities
"""
import math
from typing import List


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
