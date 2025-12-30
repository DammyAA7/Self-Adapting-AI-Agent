from salary_analyzer.salary_analyzer_class import SalaryAnalyzer

def salary_analyzer(employees):
    """
    Calculates the average salary from a list of employee records.
    Args:
        employees (list of dict): List of employee data, each with a 'salary' key.
    Returns:
        float: The average salary value.
    """
    return SalaryAnalyzer.calculate_average_salary(employees)