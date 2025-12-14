# Add project root to path for imports
import sys
sys.path.insert(0, '/home/aifahim/PycharmProjects/Self-Adapting-AI-Agent')

# Generated code by MetaGPT
def calculate_simple_gpa(university, student_id):
    """
    Calculate the simple GPA for a student given a University object and student_id.
    For each enrollment, multiply grade points by course credits, sum all points and credits,
    and return total_points / total_credits as GPA (0.0-4.0).
    """
    enrollments = university.get_student_enrollments(student_id)
    total_points = 0.0
    total_credits = 0
    for enrollment in enrollments:
        course = university.get_course(enrollment.course_code)
        if course:
            points = enrollment.get_grade_points() * course.credits
            total_points += points
            total_credits += course.credits
    return total_points / total_credits if total_credits > 0 else 0.0

# Ground-truth test from problem.json

from dataset.student_gpa_calculator.university import University, create_sample_university

university = create_sample_university()

# Test S001 - Good student: A(3cr), A-(4cr), B+(4cr), A(3cr), B(4cr), A-(4cr)
# GPA = (4.0*3 + 3.7*4 + 3.3*4 + 4.0*3 + 3.0*4 + 3.7*4) / (3+4+4+3+4+4) = 78.8/22 = 3.58
gpa_s001 = calculate_simple_gpa(university, 'S001')
assert isinstance(gpa_s001, float)
assert 3.5 <= gpa_s001 <= 3.7

# Test S002 - Average student: B(3cr), C+(4cr), B-(4cr), C(3cr)
# GPA = (3.0*3 + 2.3*4 + 2.7*4 + 2.0*3) / (3+4+4+3) = 35.0/14 = 2.5
gpa_s002 = calculate_simple_gpa(university, 'S002')
assert isinstance(gpa_s002, float)
assert 2.4 <= gpa_s002 <= 2.6

# Test S003 - Struggling: C(4cr), D(3cr), B-(3cr), F(3cr)
# GPA = (2.0*4 + 1.0*3 + 2.7*3 + 0.0*3) / (4+3+3+3) = 19.1/13 = 1.47
gpa_s003 = calculate_simple_gpa(university, 'S003')
assert isinstance(gpa_s003, float)
assert 1.4 <= gpa_s003 <= 1.6

print('Student GPA Calculator tests passed')

