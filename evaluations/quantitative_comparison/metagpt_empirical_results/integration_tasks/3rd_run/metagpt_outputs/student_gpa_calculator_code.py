def calculate_simple_gpa(university, student_id):
    """
    Calculate the simple GPA for a student.

    Args:
        university: University object
        student_id: str, ID of the student

    Returns:
        float: GPA (0.0 - 4.0)
    """
    enrollments = university.get_student_enrollments(student_id)
    total_points = 0.0
    total_credits = 0

    for enrollment in enrollments:
        course = university.get_course(enrollment.course_code)
        if course:
            grade_points = enrollment.get_grade_points()
            credits = course.credits
            total_points += grade_points * credits
            total_credits += credits

    if total_credits == 0:
        return 0.0

    return total_points / total_credits