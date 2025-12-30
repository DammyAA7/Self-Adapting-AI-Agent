# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
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

# Ground-truth test from problem.json

result_summary = performance_report('E001', report_type='summary')
assert isinstance(result_summary, dict)
assert 'employee_id' in result_summary
assert 'overall_rating' in result_summary
assert 'goals_status' in result_summary
assert result_summary['employee_id'] == 'E001'
assert isinstance(result_summary['overall_rating'], (int, float))
assert result_summary['overall_rating'] == 2.5
assert result_summary['goals_status'] == 'Exceeded'

# Test detailed report
result_detailed = performance_report('E001', report_type='detailed')
assert isinstance(result_detailed, dict)
assert 'employee_id' in result_detailed
assert 'employee_name' in result_detailed
assert 'department' in result_detailed
assert 'technical_score' in result_detailed
assert result_detailed['department'] == 'Operations'
assert result_detailed['employee_name'] == 'Employee 1'

# Test department aggregation
result_dept = performance_report(None, report_type='department')
assert isinstance(result_dept, dict)
assert len(result_dept) >= 5
for dept_name, dept_data in result_dept.items():
    assert isinstance(dept_data, dict)
    assert 'avg_rating' in dept_data
    assert 'count' in dept_data
    assert isinstance(dept_data['avg_rating'], float)
    assert isinstance(dept_data['count'], int)

print('Performance Tracker tests passed')

