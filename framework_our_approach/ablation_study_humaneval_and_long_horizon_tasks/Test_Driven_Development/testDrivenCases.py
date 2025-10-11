import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from Unit_Test.functions import salary_analyzer
from test_context_extended.employee_database import EmployeeDB

def test_salary_analyzer_default_data():
    # Using default EmployeeDB data, expected average salary
    result = salary_analyzer()
    assert isinstance(result, float)
    assert pytest.approx(70300.0, rel=1e-6) == result

def test_salary_analyzer_return_type():
    result = salary_analyzer()
    assert isinstance(result, float)

def test_salary_analyzer_with_custom_data(monkeypatch):
    # Define custom employee salaries for testing
    custom_employees = [
        {"salary": 100.0},
        {"salary": 300.0},
        {"salary": 500.0}
    ]
    # Patch the get_all_employees method on the EmployeeDB class
    monkeypatch.setattr(EmployeeDB, "get_all_employees", lambda self: custom_employees)
    result = salary_analyzer()
    expected = (100.0 + 300.0 + 500.0) / 3
    assert result == pytest.approx(expected, rel=1e-6)

def test_salary_analyzer_empty_dataset(monkeypatch):
    # Patch get_all_employees to return an empty list
    monkeypatch.setattr(EmployeeDB, "get_all_employees", lambda self: [])
    result = salary_analyzer()
    assert result == 0.0

if __name__ == "__main__":
    pytest.main([__file__])