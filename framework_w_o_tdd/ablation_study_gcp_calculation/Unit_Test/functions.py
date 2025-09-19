

def gcd(numbers):
    """
    Returns the greatest common divisor (GCD) of two or more integers in the input list.
    If a single integer is provided, returns its absolute value.
    Raises ValueError if the input is empty or contains non-integer values.
    """
    if not isinstance(numbers, (list, tuple)):
        raise ValueError("Input must be a list or tuple of integers.")
    if len(numbers) == 0:
        raise ValueError("At least one integer must be provided.")
    for n in numbers:
        if not isinstance(n, int):
            raise ValueError("All elements must be integers.")
    def _gcd(a, b):
        while b:
            a, b = b, a % b
        return abs(a)
    if len(numbers) == 1:
        return abs(numbers[0])
    result = numbers[0]
    for num in numbers[1:]:
        result = _gcd(result, num)
    return result

