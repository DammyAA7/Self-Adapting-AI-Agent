# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
from salary_analyzer_class import SalaryAnalyzer

def salary_analyzer(employee_data):
    """
    Calculates the average salary from employee data.

    Args:
        employee_data (list of dict): List of employee records, each containing a 'salary' key.

    Returns:
        float: The average salary value.
    """
    return SalaryAnalyzer.calculate_average_salary(employee_data)

# Ground-truth test from problem.json

from dataset.salary_analyzer.employee_db import EmployeeDB

db = EmployeeDB()
assert callable(salary_analyzer)
result = salary_analyzer()
assert isinstance(result, (int, float))
assert result > 0
assert 30000 <= result <= 200000
print('Salary Analyzer tests passed')

