"""
Feature Engineer Class
Feature engineering operations for machine learning
"""
from typing import List


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
