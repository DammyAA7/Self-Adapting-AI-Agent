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