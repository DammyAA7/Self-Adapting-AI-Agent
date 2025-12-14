"""
Prerequisite Checker Module
Validates course prerequisites and enrollment eligibility
"""

from typing import List, Dict, Set, Optional


class PrerequisiteChecker:
    """Check course prerequisites and validate student enrollment eligibility"""

    def __init__(self):
        """Initialize prerequisite checker with course dependency rules"""
        self.prerequisites: Dict[str, List[str]] = {}
        self.corequisites: Dict[str, List[str]] = {}

    def add_prerequisite(self, course_code: str, prerequisite_codes: List[str]) -> None:
        """
        Add prerequisite requirements for a course

        Args:
            course_code: Course requiring prerequisites
            prerequisite_codes: List of required prerequisite course codes
        """
        self.prerequisites[course_code] = prerequisite_codes

    def add_corequisite(self, course_code: str, corequisite_codes: List[str]) -> None:
        """
        Add corequisite requirements for a course

        Args:
            course_code: Course requiring corequisites
            corequisite_codes: List of courses that must be taken concurrently
        """
        self.corequisites[course_code] = corequisite_codes

    def check_prerequisites(self, course_code: str,
                          completed_courses: Set[str]) -> Dict[str, any]:
        """
        Check if student has completed prerequisites for a course

        Args:
            course_code: Course to check
            completed_courses: Set of course codes student has completed

        Returns:
            Dict with 'eligible' bool and 'missing' list of missing prerequisites
        """
        required = self.prerequisites.get(course_code, [])
        missing = [req for req in required if req not in completed_courses]

        return {
            'eligible': len(missing) == 0,
            'missing': missing,
            'required': required
        }

    def get_available_courses(self, all_courses: List[str],
                            completed_courses: Set[str],
                            enrolled_courses: Set[str] = None) -> List[Dict]:
        """
        Get list of courses student is eligible to take

        Args:
            all_courses: All available course codes
            completed_courses: Courses student has completed
            enrolled_courses: Courses student is currently enrolled in

        Returns:
            List of dicts with course info and eligibility status
        """
        if enrolled_courses is None:
            enrolled_courses = set()

        available = []
        for course in all_courses:
            if course in completed_courses or course in enrolled_courses:
                continue

            prereq_check = self.check_prerequisites(course, completed_courses)
            coreq_check = self._check_corequisites(course, enrolled_courses)

            if prereq_check['eligible'] and coreq_check['eligible']:
                available.append({
                    'course_code': course,
                    'status': 'available',
                    'notes': None
                })
            else:
                available.append({
                    'course_code': course,
                    'status': 'unavailable',
                    'notes': f"Missing: {prereq_check['missing'] + coreq_check['missing']}"
                })

        return available

    def _check_corequisites(self, course_code: str,
                          enrolled_courses: Set[str]) -> Dict[str, any]:
        """Check if corequisite courses are being taken concurrently"""
        required = self.corequisites.get(course_code, [])
        missing = [req for req in required if req not in enrolled_courses]

        return {
            'eligible': len(missing) == 0,
            'missing': missing
        }

    def validate_enrollment(self, course_code: str,
                          completed_courses: Set[str],
                          current_enrollment: Set[str]) -> Dict[str, any]:
        """
        Comprehensive validation for course enrollment

        Args:
            course_code: Course to validate
            completed_courses: Completed courses
            current_enrollment: Currently enrolled courses

        Returns:
            Dict with validation result and detailed messages
        """
        if course_code in completed_courses:
            return {
                'valid': False,
                'reason': 'Course already completed',
                'can_override': False
            }

        prereq = self.check_prerequisites(course_code, completed_courses)
        if not prereq['eligible']:
            return {
                'valid': False,
                'reason': f"Missing prerequisites: {', '.join(prereq['missing'])}",
                'can_override': True
            }

        coreq = self._check_corequisites(course_code, current_enrollment)
        if not coreq['eligible']:
            return {
                'valid': False,
                'reason': f"Missing corequisites: {', '.join(coreq['missing'])}",
                'can_override': False
            }

        return {
            'valid': True,
            'reason': 'All requirements met',
            'can_override': False
        }
