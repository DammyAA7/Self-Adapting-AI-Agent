"""
Course Class
University course information and metadata
"""


class Course:
    """University course information"""
    def __init__(self, code: str, name: str, credits: int, difficulty: int):
        self.code = code
        self.name = name
        self.credits = credits
        self.difficulty = difficulty  # 100-400 level (100=intro, 400=advanced)

    def is_advanced(self) -> bool:
        """Check if course is advanced level (300+)"""
        return self.difficulty >= 300

    def __repr__(self):
        return f"Course({self.code}, {self.name}, {self.credits}cr, L{self.difficulty})"
