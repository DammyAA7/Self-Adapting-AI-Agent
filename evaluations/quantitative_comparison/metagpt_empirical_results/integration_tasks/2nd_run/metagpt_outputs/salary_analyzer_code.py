def salary_analyzer(employee_data):
    """
    Calculates the average salary from employee data.

    Args:
        employee_data (list of dict): List of employee records, each containing a 'salary' key.

    Returns:
        float: The average salary value.
    """
    from salary_analyzer_class import SalaryAnalyzer
    return SalaryAnalyzer.calculate_average_salary(employee_data)