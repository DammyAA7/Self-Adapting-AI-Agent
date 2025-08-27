

def calculate_factorial(n):
    """
    Calculates the factorial of a non-negative integer.
    Raises TypeError if the input is not an integer.
    Raises ValueError if the input is negative.
    Returns the factorial value.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    pass
