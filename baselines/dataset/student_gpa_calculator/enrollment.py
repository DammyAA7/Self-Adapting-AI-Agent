"""
Enrollment Class
Student course enrollment records with grade tracking
"""


class Enrollment:
    """Student course enrollment record"""
    def __init__(self, student_id: str, course_code: str, semester: str, grade: str):
        self.student_id = student_id
        self.course_code = course_code
        self.semester = semester
        self.grade = grade  # Letter grade: A, A-, B+, B, B-, C+, C, C-, D, F

    def get_grade_points(self) -> float:
        """Convert letter grade to GPA points"""
        grade_map = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D': 1.0, 'F': 0.0
        }
        return grade_map.get(self.grade, 0.0)

    def __repr__(self):
        return f"Enrollment({self.student_id}, {self.course_code}, {self.grade})"
