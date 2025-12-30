# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import csv
from collections import defaultdict

def performance_report(employee_id=None, report_type='summary'):
    """
    Reads performance_reviews.csv and returns performance reports based on parameters.

    Parameters:
        employee_id (str, optional): Employee ID to filter by. If None and report_type='department', returns department summary.
        report_type (str): 'summary', 'detailed', or 'department'. Default is 'summary'.

    Returns:
        dict: Report as specified in requirements.
    """
    csv_path = 'performance_reviews.csv'
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    # Helper to convert types for detailed mode
    def convert_row_types(row):
        # Columns to convert to float
        float_cols = ['technical_score', 'communication_score', 'teamwork_score', 'leadership_score', 'overall_rating']
        int_cols = []
        converted = {}
        for k, v in row.items():
            if k in float_cols:
                converted[k] = float(v)
            elif k in int_cols:
                converted[k] = int(v)
            else:
                converted[k] = v
        return converted

    if report_type == 'department' and employee_id is None:
        # Group by department
        dept_data = defaultdict(list)
        for row in rows:
            dept = row['department']
            try:
                rating = float(row['overall_rating'])
            except Exception:
                continue
            dept_data[dept].append(rating)
        result = {}
        for dept, ratings in dept_data.items():
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
            else:
                avg_rating = 0.0
            result[dept] = {
                'avg_rating': avg_rating,
                'count': len(ratings)
            }
        return result

    # Find the row for the given employee_id
    row = next((r for r in rows if r['employee_id'] == employee_id), None)
    if not row:
        return None

    if report_type == 'summary':
        return {
            'employee_id': row['employee_id'],
            'overall_rating': float(row['overall_rating']),
            'goals_status': row['goals_status']
        }
    elif report_type == 'detailed':
        return convert_row_types(row)
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

