"""
Transcript Generator Module
Generates official academic transcripts with GPA and honors
"""

from typing import List, Dict, Optional
from datetime import datetime


class TranscriptGenerator:
    """Generate official academic transcripts for students"""

    def __init__(self, institution_name: str = "University"):
        """Initialize transcript generator with institution information"""
        self.institution_name = institution_name
        self.honors_thresholds = {
            'Summa Cum Laude': 3.9,
            'Magna Cum Laude': 3.7,
            'Cum Laude': 3.5
        }

    def generate_official_transcript(self, student_data: Dict,
                                    courses: List[Dict]) -> str:
        """
        Generate a formatted official transcript

        Args:
            student_data: Dict with student info (name, id, major, etc.)
            courses: List of course dicts with semester, course, grade, credits

        Returns:
            Formatted transcript as string
        """
        header = self._create_header(student_data)
        course_section = self._format_courses(courses)
        gpa_section = self._calculate_gpa_summary(courses)
        honors = self.calculate_honors(gpa_section['cumulative_gpa'])

        transcript = f"{header}\n\n{course_section}\n\n{gpa_section['summary']}"
        if honors:
            transcript += f"\n\nHonors: {honors}"

        transcript += f"\n\nOfficial Transcript Generated: {datetime.now().strftime('%Y-%m-%d')}"
        return transcript

    def _create_header(self, student_data: Dict) -> str:
        """Create transcript header with student information"""
        return f"""
{'=' * 60}
{self.institution_name.upper()}
OFFICIAL ACADEMIC TRANSCRIPT
{'=' * 60}

Student Name: {student_data.get('name', 'N/A')}
Student ID: {student_data.get('id', 'N/A')}
Major: {student_data.get('major', 'Undeclared')}
Date of Birth: {student_data.get('dob', 'N/A')}
"""

    def _format_courses(self, courses: List[Dict]) -> str:
        """Format course listing by semester"""
        if not courses:
            return "No courses completed."

        formatted = "ACADEMIC RECORD\n" + "-" * 60
        current_semester = None

        for course in sorted(courses, key=lambda x: x.get('semester', '')):
            semester = course.get('semester', 'Unknown')
            if semester != current_semester:
                formatted += f"\n\n{semester}:"
                current_semester = semester

            formatted += (f"\n  {course.get('code', 'N/A'):12} "
                        f"{course.get('name', 'Unknown Course'):30} "
                        f"{course.get('credits', 0):3} cr  "
                        f"Grade: {course.get('grade', 'N/A')}")

        return formatted

    def calculate_honors(self, gpa: float) -> Optional[str]:
        """
        Determine honors designation based on GPA

        Args:
            gpa: Cumulative GPA

        Returns:
            Honors designation or None
        """
        for honor, threshold in self.honors_thresholds.items():
            if gpa >= threshold:
                return honor
        return None

    def _calculate_gpa_summary(self, courses: List[Dict]) -> Dict:
        """Calculate GPA statistics for transcript"""
        grade_points = {'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                       'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0.0}

        total_points = 0.0
        total_credits = 0

        for course in courses:
            grade = course.get('grade', 'F')
            credits = course.get('credits', 0)
            points = grade_points.get(grade, 0.0)

            total_points += points * credits
            total_credits += credits

        cumulative_gpa = total_points / total_credits if total_credits > 0 else 0.0

        summary = f"""
GPA SUMMARY
{'-' * 60}
Total Credits Attempted: {total_credits}
Total Grade Points: {total_points:.2f}
Cumulative GPA: {cumulative_gpa:.3f}
"""
        return {'cumulative_gpa': cumulative_gpa, 'summary': summary,
                'total_credits': total_credits}
