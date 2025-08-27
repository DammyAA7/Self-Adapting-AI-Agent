from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def calculate_gcd(numbers):
    """
    Calculates the greatest common divisor (GCD) of a list of integers.
    Returns the GCD as an integer, or False for invalid input as required by test cases.
    """
    if not isinstance(numbers, list) or not numbers or any(isinstance(n, list) for n in numbers):
        return False
    if any(not isinstance(n, int) for n in numbers):
        return False
    if len(numbers) == 0:
        return False
    # Handle single value
    if len(numbers) == 1:
        return abs(numbers[0])
    def gcd(a, b):
        a, b = abs(a), abs(b)
        while b != 0:
            a, b = b, a % b
        return a
    result = abs(numbers[0])
    for n in numbers[1:]:
        result = gcd(result, n)
    return result

