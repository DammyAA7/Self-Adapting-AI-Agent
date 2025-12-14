
import csv
from collections import defaultdict
from typing import Optional, Dict, Any, List

def performance_report(employee_id: Optional[str]=None, report_type: str='summary') -> Optional[Dict[str, Any]]:
    '''
    Reads 'performance_reviews.csv' and returns performance info.
    See docstring above for modes and results.
    '''
    # Map column names to types for type-correct conversion
    float_cols = {'technical_score', 'communication_score', 'teamwork_score', 'leadership_score', 'overall_rating'}
    int_cols = set()  # (none explicitly, but could extend)
    
    def parse_row(row):
        # Helper to apply types in detailed mode
        return { 
            k: float(row[k]) if k in float_cols else row[k]
            for k in row
        }

    # Read the data into a list of dicts
    with open('performance_reviews.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if employee_id is not None:
        # Find matching row
        for row in rows:
            if row['employee_id'] == employee_id:
                if report_type == 'summary':
                    return {
                        'employee_id': row['employee_id'],
                        'overall_rating': float(row['overall_rating']),
                        'goals_status': row['goals_status']
                    }
                elif report_type == 'detailed':
                    # Return all columns, with number types preserved as appropriate
                    detailed = {}
                    for k, v in row.items():
                        if k in float_cols:
                            detailed[k] = float(v)
                        else:
                            detailed[k] = v
                    return detailed
        # Not found
        return None

    elif employee_id is None and report_type == 'department':
        # Group by department
        dept_stats = defaultdict(lambda: {'ratings': [], 'count': 0})
        for row in rows:
            dept = row['department']
            try:
                rating = float(row['overall_rating'])
            except Exception:
                continue  # Skip bad data
            dept_stats[dept]['ratings'].append(rating)
            dept_stats[dept]['count'] += 1

        # Build output
        result = {}
        for dept, stat in dept_stats.items():
            ratings = stat['ratings']
            count = stat['count']
            avg = sum(ratings) / count if count else 0.0
            result[dept] = {'avg_rating': avg, 'count': count}
        return result

    else:
        # Unknown mode, return None or raise error
        return None



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
