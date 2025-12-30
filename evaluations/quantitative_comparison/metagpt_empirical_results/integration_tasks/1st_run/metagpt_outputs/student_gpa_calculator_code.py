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