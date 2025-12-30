# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
def salary_analyzer(employees):
    """
    Calculates the average salary from employee data.

    Args:
        employees (list of dict): List of employee records, each containing at least a 'salary' key.

    Returns:
        float: The average salary value.
    """
    from salary_analyzer.salary_analyzer_class import SalaryAnalyzer
    return SalaryAnalyzer.calculate_average_salary(employees)

# Ground-truth test from problem.json

from dataset.salary_analyzer.employee_db import EmployeeDB

db = EmployeeDB()
assert callable(salary_analyzer)
result = salary_analyzer()
assert isinstance(result, (int, float))
assert result > 0
assert 30000 <= result <= 200000
print('Salary Analyzer tests passed')

