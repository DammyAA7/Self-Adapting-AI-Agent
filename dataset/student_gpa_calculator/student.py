"""
Student Class
Student profile and information
"""


class Student:
    """Student profile information"""
    def __init__(self, id: str, name: str, major: str, admission_year: int):
        self.id = id
        self.name = name
        self.major = major
        self.admission_year = admission_year

    def __repr__(self):
        return f"Student({self.id}, {self.name}, {self.major})"
