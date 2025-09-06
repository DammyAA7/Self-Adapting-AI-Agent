from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


from typing import List, Dict, Any

def salary_analyzer() -> float:
    """
    Compute the average salary of all employees in the database.

    Returns:
        The average salary as a float. Returns 0.0 if there are no employees.
    """
    # Import here to avoid circular references if this file is re-imported elsewhere
    from employee_database import EmployeeDB, SalaryAnalyzer

    # Instantiate the in-memory employee database
    db = EmployeeDB()

    # Retrieve all employee records
    employees: List[Dict[str, Any]] = db.get_all_employees()

    # Use the existing SalaryAnalyzer to compute the average
    return SalaryAnalyzer.calculate_average_salary(employees)
