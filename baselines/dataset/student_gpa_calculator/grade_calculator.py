"""
Grade Calculator Module
Handles weighted grades, curves, and final grade calculations
"""

from typing import Dict, List, Optional, Tuple


class GradeCalculator:
    """Calculate and manage student grades with various weighting and curving methods"""

    def __init__(self):
        """Initialize the grade calculator with default configurations"""
        self.standard_scale = {
            'A': (90, 100),
            'B': (80, 89),
            'C': (70, 79),
            'D': (60, 69),
            'F': (0, 59)
        }
        self.plus_minus_threshold = 3

    def calculate_weighted_grade(self, components: Dict[str, Tuple[float, float]]) -> float:
        """
        Calculate weighted grade from multiple components

        Args:
            components: Dict mapping component name to (score, weight) tuples
                       Example: {'midterm': (85.0, 0.30), 'final': (92.0, 0.40)}

        Returns:
            Weighted average grade as a float
        """
        if not components:
            return 0.0

        total_weight = sum(weight for _, weight in components.values())
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(score * weight for score, weight in components.values())
        return weighted_sum / total_weight

    def apply_curve(self, score: float, curve_type: str = 'linear',
                   curve_amount: float = 5.0) -> float:
        """
        Apply grade curve to a score

        Args:
            score: Original score
            curve_type: Type of curve ('linear', 'sqrt', 'percentile')
            curve_amount: Amount to curve (meaning depends on curve_type)

        Returns:
            Curved score
        """
        if curve_type == 'linear':
            curved = min(100.0, score + curve_amount)
        elif curve_type == 'sqrt':
            curved = min(100.0, 10 * (score ** 0.5))
        elif curve_type == 'percentile':
            # Simple percentile boost
            curved = min(100.0, score * (1 + curve_amount / 100))
        else:
            curved = score

        return round(curved, 2)

    def calculate_final_grade(self, numeric_score: float,
                            use_plus_minus: bool = True) -> str:
        """
        Convert numeric score to letter grade

        Args:
            numeric_score: Numeric grade (0-100)
            use_plus_minus: Whether to use +/- modifiers

        Returns:
            Letter grade (e.g., 'A', 'B+', 'C-')
        """
        # Determine base letter grade
        letter = 'F'
        for grade, (low, high) in self.standard_scale.items():
            if low <= numeric_score <= high:
                letter = grade
                break

        if not use_plus_minus or letter in ['F', 'A']:
            # Special handling for A+ if score is perfect
            if letter == 'A' and numeric_score >= 97:
                return 'A+'
            return letter

        # Add plus/minus modifiers
        for grade, (low, high) in self.standard_scale.items():
            if low <= numeric_score <= high:
                range_size = high - low + 1
                position_in_range = numeric_score - low

                if position_in_range >= range_size - self.plus_minus_threshold:
                    return f"{grade}+"
                elif position_in_range < self.plus_minus_threshold:
                    return f"{grade}-"
                else:
                    return grade

        return letter
