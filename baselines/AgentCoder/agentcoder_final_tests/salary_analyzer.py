
from .employee_db import EMPLOYEE_DATA
from .salary_analyzer_class import SalaryAnalyzer

def salary_analyzer():
    '''
    Create a function called salary_analyzer that calculates average salary from employee data. Returns: float representing the average salary value.
    '''
    return SalaryAnalyzer.calculate_average_salary(EMPLOYEE_DATA)



from dataset.salary_analyzer.employee_db import EmployeeDB

db = EmployeeDB()
assert callable(salary_analyzer)
result = salary_analyzer()
assert isinstance(result, (int, float))
assert result > 0
assert 30000 <= result <= 200000
print('Salary Analyzer tests passed')
