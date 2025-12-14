"""
University Class
Main university system managing students, courses, and enrollments
"""

from typing import Dict, List, Optional
from .student import Student
from .course import Course
from .enrollment import Enrollment
from .department import Department


class University:
    """Main university system managing students, courses, and enrollments"""
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self.enrollments: List[Enrollment] = []
        self.departments: Dict[str, Department] = {}

    def add_student(self, student: Student):
        """Register a new student"""
        self.students[student.id] = student

    def add_course(self, course: Course):
        """Add a course to catalog"""
        self.courses[course.code] = course

    def add_enrollment(self, enrollment: Enrollment):
        """Record a course enrollment"""
        self.enrollments.append(enrollment)

    def add_department(self, department: Department):
        """Add an academic department"""
        self.departments[department.code] = department

    def get_student(self, student_id: str) -> Optional[Student]:
        """Retrieve student by ID"""
        return self.students.get(student_id)

    def get_course(self, course_code: str) -> Optional[Course]:
        """Retrieve course by code"""
        return self.courses.get(course_code)

    def get_student_enrollments(self, student_id: str) -> List[Enrollment]:
        """Get all enrollments for a student"""
        return [e for e in self.enrollments if e.student_id == student_id]

    def get_completed_credits(self, student_id: str) -> int:
        """Calculate total credits completed (grade D or better)"""
        enrollments = self.get_student_enrollments(student_id)
        total = 0
        for e in enrollments:
            if e.grade != 'F':
                course = self.get_course(e.course_code)
                if course:
                    total += course.credits
        return total

    def get_all_students(self) -> List[Student]:
        """Get all registered students"""
        return list(self.students.values())

    def __repr__(self):
        return f"University({len(self.students)} students, {len(self.courses)} courses, {len(self.enrollments)} enrollments)"


# Sample data for testing
def create_sample_university():
    """Create sample university with test data"""
    university = University()

    # Add departments
    cs_dept = Department("CS", "Computer Science")
    math_dept = Department("MATH", "Mathematics")
    university.add_department(cs_dept)
    university.add_department(math_dept)

    # Add courses
    university.add_course(Course("CS101", "Intro to Programming", 3, 100))
    university.add_course(Course("CS201", "Data Structures", 4, 200))
    university.add_course(Course("CS301", "Algorithms", 4, 300))
    university.add_course(Course("CS401", "Machine Learning", 4, 400))
    university.add_course(Course("MATH150", "Calculus I", 4, 100))
    university.add_course(Course("MATH250", "Linear Algebra", 3, 200))
    university.add_course(Course("MATH350", "Probability", 3, 300))

    # Student 1: Good performance, mixed difficulty
    s1 = Student("S001", "Alice Chen", "Computer Science", 2022)
    university.add_student(s1)
    university.add_enrollment(Enrollment("S001", "CS101", "Fall 2022", "A"))
    university.add_enrollment(Enrollment("S001", "MATH150", "Fall 2022", "A-"))
    university.add_enrollment(Enrollment("S001", "CS201", "Spring 2023", "B+"))
    university.add_enrollment(Enrollment("S001", "MATH250", "Spring 2023", "A"))
    university.add_enrollment(Enrollment("S001", "CS301", "Fall 2023", "B"))
    university.add_enrollment(Enrollment("S001", "CS401", "Spring 2024", "A-"))

    # Student 2: Average performance
    s2 = Student("S002", "Bob Williams", "Computer Science", 2023)
    university.add_student(s2)
    university.add_enrollment(Enrollment("S002", "CS101", "Fall 2023", "B"))
    university.add_enrollment(Enrollment("S002", "MATH150", "Fall 2023", "C+"))
    university.add_enrollment(Enrollment("S002", "CS201", "Spring 2024", "B-"))
    university.add_enrollment(Enrollment("S002", "MATH250", "Spring 2024", "C"))

    # Student 3: Struggling, some failures
    s3 = Student("S003", "Carol Martinez", "Mathematics", 2022)
    university.add_student(s3)
    university.add_enrollment(Enrollment("S003", "MATH150", "Fall 2022", "C"))
    university.add_enrollment(Enrollment("S003", "MATH250", "Spring 2023", "D"))
    university.add_enrollment(Enrollment("S003", "CS101", "Fall 2023", "B-"))
    university.add_enrollment(Enrollment("S003", "MATH350", "Spring 2024", "F"))

    return university


if __name__ == "__main__":
    university = create_sample_university()
    print(university)
    print(f"\nStudents: {[s.name for s in university.get_all_students()]}")
    print(f"\nS001 enrollments: {university.get_student_enrollments('S001')}")
    print(f"S001 completed credits: {university.get_completed_credits('S001')}")

    # Test course retrieval
    cs401 = university.get_course("CS401")
    print(f"\nCS401 details: {cs401}")
    print(f"CS401 is advanced: {cs401.is_advanced()}")
