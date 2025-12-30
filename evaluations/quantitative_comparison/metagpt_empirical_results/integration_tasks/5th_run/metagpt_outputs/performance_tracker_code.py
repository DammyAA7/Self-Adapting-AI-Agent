import csv
from typing import Optional, Dict, Any, Union

def performance_report(employee_id: Optional[str] = None, report_type: str = 'summary') -> Union[Dict[str, Any], Dict[str, Dict[str, Union[float, int]]]]:
    """
    Generate a performance report from performance_reviews.csv.
    Parameters:
        employee_id (str, optional): Employee ID to filter by. If None and report_type is 'department', returns department summary.
        report_type (str): 'summary', 'detailed', or 'department'.
    Returns:
        dict: Report as specified in the requirements.
    """
    import os
    csv_path = os.path.join(os.path.dirname(__file__), 'performance_reviews.csv')
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    if report_type == 'department' and employee_id is None:
        # Group by department
        from collections import defaultdict
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
    match = None
    for row in rows:
        if row['employee_id'] == employee_id:
            match = row
            break
    if not match:
        return {}

    if report_type == 'summary':
        return {
            'employee_id': match['employee_id'],
            'overall_rating': float(match['overall_rating']),
            'goals_status': match['goals_status']
        }
    elif report_type == 'detailed':
        # Convert types as in CSV: overall_rating and scores to float/int, count remains int, rest as string
        detailed = {}
        for k, v in match.items():
            if k == 'overall_rating':
                try:
                    detailed[k] = float(v)
                except ValueError:
                    detailed[k] = v
            elif k.endswith('_score'):
                try:
                    detailed[k] = int(v)
                except ValueError:
                    detailed[k] = v
            else:
                detailed[k] = v
        return detailed
    else:
        raise ValueError("Invalid report_type. Choose from 'summary', 'detailed', or 'department'.")