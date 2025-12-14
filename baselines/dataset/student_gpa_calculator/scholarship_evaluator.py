"""
Scholarship Evaluator Module
Evaluates scholarship eligibility and calculates award amounts
"""

from typing import List, Dict, Optional
from enum import Enum


class ScholarshipType(Enum):
    """Types of scholarships available"""
    MERIT = "merit"
    NEED_BASED = "need_based"
    ATHLETIC = "athletic"
    DEPARTMENTAL = "departmental"


class ScholarshipEvaluator:
    """Evaluate scholarship eligibility and calculate award amounts"""

    def __init__(self):
        """Initialize scholarship evaluator with default criteria"""
        self.scholarships = {
            'Presidential': {'type': ScholarshipType.MERIT, 'gpa_min': 3.9,
                           'amount': 25000, 'renewable': True},
            'Dean\'s': {'type': ScholarshipType.MERIT, 'gpa_min': 3.7,
                       'amount': 15000, 'renewable': True},
            'Academic Excellence': {'type': ScholarshipType.MERIT, 'gpa_min': 3.5,
                                  'amount': 10000, 'renewable': True},
            'Financial Need': {'type': ScholarshipType.NEED_BASED, 'gpa_min': 2.5,
                             'amount': 8000, 'renewable': True},
            'Department Honors': {'type': ScholarshipType.DEPARTMENTAL, 'gpa_min': 3.6,
                                'amount': 5000, 'renewable': False}
        }
        self.minimum_credits = 12

    def check_eligibility(self, student_data: Dict,
                         scholarship_name: str) -> Dict[str, any]:
        """
        Check if student is eligible for a specific scholarship

        Args:
            student_data: Dict with gpa, credits, financial_need, department, etc.
            scholarship_name: Name of scholarship to check

        Returns:
            Dict with eligibility status and details
        """
        if scholarship_name not in self.scholarships:
            return {'eligible': False, 'reason': 'Scholarship not found'}

        scholarship = self.scholarships[scholarship_name]
        gpa = student_data.get('gpa', 0.0)
        credits = student_data.get('credits', 0)

        # Check basic requirements
        if gpa < scholarship['gpa_min']:
            return {
                'eligible': False,
                'reason': f"GPA {gpa:.2f} below minimum {scholarship['gpa_min']}"
            }

        if credits < self.minimum_credits:
            return {
                'eligible': False,
                'reason': f"Credits {credits} below minimum {self.minimum_credits}"
            }

        # Check type-specific requirements
        if scholarship['type'] == ScholarshipType.NEED_BASED:
            if not student_data.get('financial_need', False):
                return {
                    'eligible': False,
                    'reason': 'No demonstrated financial need'
                }

        if scholarship['type'] == ScholarshipType.DEPARTMENTAL:
            if student_data.get('department') != scholarship_name.split()[0]:
                return {
                    'eligible': False,
                    'reason': 'Not in required department'
                }

        return {
            'eligible': True,
            'reason': 'All requirements met',
            'amount': scholarship['amount']
        }

    def calculate_award_amount(self, student_data: Dict,
                              scholarship_names: List[str]) -> Dict[str, any]:
        """
        Calculate total scholarship award amount

        Args:
            student_data: Student information
            scholarship_names: List of scholarships to consider

        Returns:
            Dict with total amount and breakdown
        """
        total = 0
        awards = []

        for name in scholarship_names:
            result = self.check_eligibility(student_data, name)
            if result['eligible']:
                amount = result['amount']
                total += amount
                awards.append({
                    'scholarship': name,
                    'amount': amount,
                    'renewable': self.scholarships[name]['renewable']
                })

        return {
            'total_amount': total,
            'awards': awards,
            'count': len(awards)
        }

    def rank_applicants(self, applicants: List[Dict],
                       scholarship_name: str) -> List[Dict]:
        """
        Rank scholarship applicants by eligibility and merit

        Args:
            applicants: List of applicant dicts with student data
            scholarship_name: Scholarship to rank for

        Returns:
            Sorted list of eligible applicants with ranking
        """
        eligible = []

        for applicant in applicants:
            result = self.check_eligibility(applicant, scholarship_name)
            if result['eligible']:
                eligible.append({
                    'student_id': applicant.get('student_id'),
                    'name': applicant.get('name'),
                    'gpa': applicant.get('gpa', 0.0),
                    'credits': applicant.get('credits', 0),
                    'score': self._calculate_merit_score(applicant)
                })

        # Sort by merit score (descending)
        ranked = sorted(eligible, key=lambda x: x['score'], reverse=True)

        # Add rank numbers
        for i, applicant in enumerate(ranked, 1):
            applicant['rank'] = i

        return ranked

    def _calculate_merit_score(self, student_data: Dict) -> float:
        """Calculate overall merit score for ranking"""
        gpa = student_data.get('gpa', 0.0)
        credits = student_data.get('credits', 0)
        leadership = student_data.get('leadership_hours', 0)
        community_service = student_data.get('community_service_hours', 0)

        # Weighted scoring formula
        score = (gpa * 40) + (min(credits / 150, 1.0) * 30) + \
                (min(leadership / 100, 1.0) * 15) + \
                (min(community_service / 100, 1.0) * 15)

        return round(score, 2)
