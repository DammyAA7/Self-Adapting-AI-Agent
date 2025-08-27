from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def calculate_factorial(n):
    """
    Calculates the factorial of a non-negative integer n.
    Raises ValueError for negative n and TypeError for non-integer n.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def calculate_factorial_expression(expr):
    """
    Calculates the sum of factorials in a factorial expression string like "2!+3!".
    """
    if not isinstance(expr, str):
        raise TypeError("Expression must be a string")
    expr_stripped = expr.strip()
    if not expr_stripped:
        raise ValueError("Expression cannot be empty")
    total = 0
    terms = expr.split("+")
    for term in terms:
        term_stripped = term.strip()
        if not term_stripped:
            raise ValueError("Invalid term in expression")
        if term_stripped.count("!") != 1 or not term_stripped.endswith("!"):
            raise ValueError(f"Invalid term format: {term_stripped}")
        operand_str = term_stripped[:-1]
        if operand_str.startswith("-") and operand_str[1:].isdigit():
            raise ValueError("Negative operand in factorial expression")
        if not operand_str.isdigit():
            raise TypeError("Operand must be an integer")
        n = int(operand_str)
        total += calculate_factorial(n)
    return total
