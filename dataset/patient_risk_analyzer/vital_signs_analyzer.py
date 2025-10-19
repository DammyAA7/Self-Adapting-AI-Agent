"""
Vital Signs Analyzer
Analyzes trends and patterns in patient vital signs
"""
from typing import List, Dict, Tuple
from datetime import datetime, timedelta


class VitalSignsTrends:
    """Analyzes vital signs trends over time"""

    @staticmethod
    def calculate_bp_trend(readings: List[Tuple[int, int, str]]) -> str:
        """
        Calculate blood pressure trend
        Args: List of (systolic, diastolic, date) tuples
        Returns: 'increasing', 'decreasing', or 'stable'
        """
        if len(readings) < 3:
            return 'insufficient_data'

        systolic_values = [r[0] for r in readings]

        # Check if trending up or down
        increases = sum(1 for i in range(1, len(systolic_values))
                       if systolic_values[i] > systolic_values[i-1])

        if increases > len(systolic_values) * 0.6:
            return 'increasing'
        elif increases < len(systolic_values) * 0.4:
            return 'decreasing'
        return 'stable'

    @staticmethod
    def detect_anomalies(values: List[float], threshold_std: float = 2.0) -> List[int]:
        """Detect anomalous readings using standard deviation"""
        if len(values) < 3:
            return []

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std = variance ** 0.5

        anomalies = []
        for i, val in enumerate(values):
            if abs(val - mean) > threshold_std * std:
                anomalies.append(i)
        return anomalies


class HeartRateMonitor:
    """Monitors heart rate patterns"""

    NORMAL_RANGE = (60, 100)
    BRADYCARDIA_THRESHOLD = 60
    TACHYCARDIA_THRESHOLD = 100

    @staticmethod
    def classify_heart_rate(bpm: int) -> str:
        """Classify heart rate as normal, bradycardia, or tachycardia"""
        if bpm < HeartRateMonitor.BRADYCARDIA_THRESHOLD:
            return 'bradycardia'
        elif bpm > HeartRateMonitor.TACHYCARDIA_THRESHOLD:
            return 'tachycardia'
        return 'normal'

    @staticmethod
    def calculate_avg_heart_rate(readings: List[int]) -> float:
        """Calculate average heart rate from readings"""
        if not readings:
            return 0.0
        return sum(readings) / len(readings)

    @staticmethod
    def check_variability(readings: List[int]) -> Dict[str, float]:
        """Calculate heart rate variability metrics"""
        if len(readings) < 2:
            return {'variability': 0.0, 'range': 0}

        diff_sum = sum(abs(readings[i] - readings[i-1]) for i in range(1, len(readings)))
        avg_variability = diff_sum / (len(readings) - 1)

        return {
            'variability': avg_variability,
            'range': max(readings) - min(readings),
            'min': min(readings),
            'max': max(readings)
        }
