"""
Employee Database Class
Simple employee database operations
"""
from typing import List, Dict, Any, Optional


# Sample employee database - this would normally come from a real database
EMPLOYEE_DATA = [
    {"id": 1, "name": "John Smith", "email": "john.smith@company.com", "age": 35, "role": "admin", "department": "IT", "salary": 75000},
    {"id": 2, "name": "Sarah Johnson", "email": "sarah.j@company.com", "age": 28, "role": "developer", "department": "Engineering", "salary": 65000},
    {"id": 3, "name": "Mike Brown", "email": "mike.brown@company.com", "age": 42, "role": "manager", "department": "Sales", "salary": 80000},
    {"id": 4, "name": "Lisa Davis", "email": "lisa.davis@company.com", "age": 31, "role": "developer", "department": "Engineering", "salary": 70000},
    {"id": 5, "name": "Tom Wilson", "email": "tom.w@company.com", "age": 45, "role": "admin", "department": "IT", "salary": 78000},
    {"id": 6, "name": "Emma Garcia", "email": "emma.g@company.com", "age": 26, "role": "analyst", "department": "Marketing", "salary": 55000},
    {"id": 7, "name": "David Lee", "email": "david.lee@company.com", "age": 38, "role": "manager", "department": "HR", "salary": 72000},
    {"id": 8, "name": "Anna Taylor", "email": "anna.t@company.com", "age": 33, "role": "developer", "department": "Engineering", "salary": 68000},
    {"id": 9, "name": "James Miller", "email": "james.m@company.com", "age": 29, "role": "analyst", "department": "Finance", "salary": 58000},
    {"id": 10, "name": "Mary Johnson", "email": "mary.j@company.com", "age": 41, "role": "admin", "department": "IT", "salary": 76000}
]


class EmployeeDB:
    """Simple employee database operations"""

    def __init__(self, data: List[Dict[str, Any]] = None):
        self.employees = data or EMPLOYEE_DATA.copy()

    def get_all_employees(self) -> List[Dict[str, Any]]:
        """Get all employees"""
        return self.employees.copy()

    def get_employee_by_id(self, emp_id: int) -> Optional[Dict[str, Any]]:
        """Get employee by ID"""
        for emp in self.employees:
            if emp['id'] == emp_id:
                return emp.copy()
        return None

    def filter_by_department(self, department: str) -> List[Dict[str, Any]]:
        """Get all employees in a department"""
        return [emp for emp in self.employees if emp['department'] == department]

    def filter_by_role(self, role: str) -> List[Dict[str, Any]]:
        """Get all employees with specific role"""
        return [emp for emp in self.employees if emp['role'] == role]

    def get_employees_over_age(self, min_age: int) -> List[Dict[str, Any]]:
        """Get employees above specified age"""
        return [emp for emp in self.employees if emp['age'] > min_age]

    def get_employees_by_salary_range(self, min_salary: int, max_salary: int) -> List[Dict[str, Any]]:
        """Get employees within salary range"""
        return [emp for emp in self.employees
                if min_salary <= emp['salary'] <= max_salary]

    def get_department_list(self) -> List[str]:
        """Get unique list of departments"""
        departments = set(emp['department'] for emp in self.employees)
        return sorted(list(departments))

    def get_role_list(self) -> List[str]:
        """Get unique list of roles"""
        roles = set(emp['role'] for emp in self.employees)
        return sorted(list(roles))

    def count_employees(self) -> int:
        """Get total employee count"""
        return len(self.employees)

    def count_by_department(self) -> Dict[str, int]:
        """Count employees by department"""
        counts = {}
        for emp in self.employees:
            dept = emp['department']
            counts[dept] = counts.get(dept, 0) + 1
        return counts

    def count_by_role(self) -> Dict[str, int]:
        """Count employees by role"""
        counts = {}
        for emp in self.employees:
            role = emp['role']
            counts[role] = counts.get(role, 0) + 1
        return counts
