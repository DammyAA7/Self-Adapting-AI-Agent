"""
Department Class
Academic department information
"""


class Department:
    """Academic department"""
    def __init__(self, code: str, name: str):
        self.code = code
        self.name = name
        self.faculty_count = 0

    def __repr__(self):
        return f"Department({self.code}, {self.name})"
