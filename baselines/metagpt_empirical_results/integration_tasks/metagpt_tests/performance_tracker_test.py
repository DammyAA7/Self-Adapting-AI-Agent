# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
import csv
from collections import defaultdict
from typing import Optional, Dict, Any, Union

def performance_report(employee_id: Optional[str] = None, report_type: str = 'summary') -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    """
    Reads performance_reviews.csv and returns performance report based on parameters.
    Parameters:
        employee_id (optional str): Employee ID to filter. If None and report_type is 'department', returns department summary.
        report_type (str): 'summary', 'detailed', or 'department'. Default is 'summary'.
    Returns:
        - summary: dict with 'employee_id', 'overall_rating' (float), 'goals_status' (str)
        - detailed: dict with all CSV columns, preserving types
        - department: dict {department: {'avg_rating': float, 'count': int}}
    """
    csv_path = 'performance_reviews.csv'
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    if report_type == 'department' and employee_id is None:
        dept_data = defaultdict(list)
        for row in rows:
            dept = row['department']
            try:
                rating = float(row['overall_rating'])
            except ValueError:
                continue
            dept_data[dept].append(rating)
        result = {}
        for dept, ratings in dept_data.items():
            result[dept] = {
                'avg_rating': sum(ratings) / len(ratings) if ratings else 0.0,
                'count': len(ratings)
            }
        return result

    # Find the row for the given employee_id
    match_row = None
    for row in rows:
        if row['employee_id'] == employee_id:
            match_row = row
            break
    if not match_row:
        return {}

    if report_type == 'summary':
        return {
            'employee_id': match_row['employee_id'],
            'overall_rating': float(match_row['overall_rating']),
            'goals_status': match_row['goals_status']
        }
    elif report_type == 'detailed':
        # Convert numeric columns to correct types
        detailed = {}
        for k, v in match_row.items():
            if k == 'overall_rating':
                detailed[k] = float(v)
            elif k in ['technical_score', 'communication_score', 'teamwork_score', 'leadership_score']:
                try:
                    detailed[k] = int(v)
                except ValueError:
                    detailed[k] = v
            else:
                detailed[k] = v
        return detailed
    else:
        raise ValueError("Invalid report_type. Choose 'summary', 'detailed', or 'department'.")

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

