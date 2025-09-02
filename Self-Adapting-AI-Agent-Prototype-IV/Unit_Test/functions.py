from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


from test_context.employee_database import EmployeeDB, SalaryAnalyzer

def salary_analyzer():
    """Calculate average salary from the employee database."""
    db = EmployeeDB()
    employees = db.get_all_employees()
    return SalaryAnalyzer.calculate_average_salary(employees)
