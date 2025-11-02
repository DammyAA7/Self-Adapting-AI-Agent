"""
Student GPA Calculator Package
Education domain codebase for self-evolution testing
"""

# Export all classes and functions for easy importing
from .course import *
from .enrollment import *
from .student import *
from .department import *
from .university import *
from .grade_calculator import *
from .transcript_generator import *
from .prerequisite_checker import *
from .scholarship_evaluator import *

# Explicit exports
__all__ = [
    'Course', 'Enrollment', 'Student', 'Department', 'University',
    'GradeCalculator', 'TranscriptGenerator', 'PrerequisiteChecker',
    'ScholarshipEvaluator', 'ScholarshipType', 'create_sample_university'
]
