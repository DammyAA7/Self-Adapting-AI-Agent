from salary_analyzer_class import SalaryAnalyzer
from typing import List, Dict, Any

def salary_analyzer(employees: List[Dict[str, Any]]) -> float:
    """
    Calculates the average salary from employee data.
    Args:
        employees: List of employee records (each a dict with a 'salary' key)
    Returns:
        float: The average salary value
    """
    return SalaryAnalyzer.calculate_average_salary(employees)