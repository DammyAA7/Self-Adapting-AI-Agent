"""
Salary Analyzer Class
Salary analysis utilities
"""
from typing import List, Dict, Any


class SalaryAnalyzer:
    """Salary analysis utilities"""

    @staticmethod
    def calculate_average_salary(employees: List[Dict[str, Any]]) -> float:
        """Calculate average salary for list of employees"""
        if not employees:
            return 0.0
        total_salary = sum(emp['salary'] for emp in employees)
        return total_salary / len(employees)

    @staticmethod
    def find_salary_range(employees: List[Dict[str, Any]]) -> Dict[str, float]:
        """Find min and max salary in employee list"""
        if not employees:
            return {"min": 0.0, "max": 0.0}

        salaries = [emp['salary'] for emp in employees]
        return {
            "min": min(salaries),
            "max": max(salaries)
        }

    @staticmethod
    def get_salary_statistics(employees: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get comprehensive salary statistics"""
        if not employees:
            return {
                "count": 0,
                "average": 0.0,
                "min": 0.0,
                "max": 0.0,
                "total": 0.0
            }

        salaries = [emp['salary'] for emp in employees]
        return {
            "count": len(salaries),
            "average": sum(salaries) / len(salaries),
            "min": min(salaries),
            "max": max(salaries),
            "total": sum(salaries)
        }
