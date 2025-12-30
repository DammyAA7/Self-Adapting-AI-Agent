import csv
from collections import defaultdict

def performance_report(employee_id=None, report_type='summary'):
    """
    Reads performance_reviews.csv and returns performance report based on parameters.

    Parameters:
        employee_id (str, optional): Employee ID to filter. If None and report_type='department', returns department summary.
        report_type (str): 'summary', 'detailed', or 'department'. Default is 'summary'.

    Returns:
        dict: Report as specified in requirements.
    """
    filename = 'performance_reviews.csv'
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Convert types for relevant columns
    for row in rows:
        row['overall_rating'] = float(row['overall_rating'])
        row['technical_score'] = int(row['technical_score'])
        row['communication_score'] = int(row['communication_score'])
        row['teamwork_score'] = int(row['teamwork_score'])
        row['leadership_score'] = int(row['leadership_score'])

    if report_type == 'department' and employee_id is None:
        dept_data = defaultdict(lambda: {'total_rating': 0.0, 'count': 0})
        for row in rows:
            dept = row['department']
            dept_data[dept]['total_rating'] += row['overall_rating']
            dept_data[dept]['count'] += 1
        result = {}
        for dept, data in dept_data.items():
            result[dept] = {
                'avg_rating': data['total_rating'] / data['count'] if data['count'] else 0.0,
                'count': data['count']
            }
        return result

    # Find the row for the given employee_id
    match = next((row for row in rows if row['employee_id'] == employee_id), None)
    if not match:
        return None

    if report_type == 'summary':
        return {
            'employee_id': match['employee_id'],
            'overall_rating': match['overall_rating'],
            'goals_status': match['goals_status']
        }
    elif report_type == 'detailed':
        # Return all columns, preserving types
        return dict(match)
    else:
        raise ValueError("Invalid report_type. Must be 'summary', 'detailed', or 'department'.")