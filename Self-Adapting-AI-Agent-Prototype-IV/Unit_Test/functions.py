from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
computation_cache = {}

def matrix_operations(matrix_a, matrix_b):
    """Performs matrix multiplication with caching.

    Returns the resulting matrix as a list of lists.
    Returns None on invalid input or dimension mismatch."""
    global computation_cache

    # Type validation
    if not isinstance(matrix_a, list) or not isinstance(matrix_b, list):
        return None

    # Special case: both matrices empty
    if matrix_a == [] and matrix_b == []:
        key = (tuple(tuple(row) for row in matrix_a),
               tuple(tuple(row) for row in matrix_b))
        result = []
        computation_cache[key] = result
        return result

    # Validate that each row is a list
    for row in matrix_a:
        if not isinstance(row, list):
            return None
    for row in matrix_b:
        if not isinstance(row, list):
            return None

    # Reject if one is empty and the other is not
    if not matrix_a or not matrix_b:
        return None

    # Check consistent row lengths for matrix_a
    cols_a = len(matrix_a[0])
    for row in matrix_a:
        if len(row) != cols_a:
            return None

    # Check consistent row lengths for matrix_b
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])
    for row in matrix_b:
        if len(row) != cols_b:
            return None

    # Dimension compatibility: columns of A must equal rows of B
    if cols_a != rows_b:
        return None

    # Create cache key
    key = (tuple(tuple(row) for row in matrix_a),
           tuple(tuple(row) for row in matrix_b))
    if key in computation_cache:
        return computation_cache[key]

    # Compute matrix multiplication
    result = []
    for i in range(len(matrix_a)):
        result_row = []
        for j in range(cols_b):
            sum_val = 0
            for k in range(cols_a):
                sum_val += matrix_a[i][k] * matrix_b[k][j]
            result_row.append(sum_val)
        result.append(result_row)

    computation_cache[key] = result
    return result



computation_cache = {}

def advanced_matrix_ops(matrix, use_cache=True, cache_key=None):
    """Performs advanced matrix operations with optional caching.

    Validates that matrix is a non-empty square numeric matrix.
    If use_cache is True, caches the result under cache_key or an implicit key.
    Returns the result dict from matrix_operations or None on invalid input.
    """
    # Validate matrix structure
    if not isinstance(matrix, list) or len(matrix) == 0:
        return None
    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None

    # If caching disabled, always compute fresh and do not populate cache
    if not use_cache:
        return matrix_operations(matrix)

    # Determine cache key
    key = cache_key if cache_key is not None else tuple(tuple(row) for row in matrix)

    # Return cached result if available
    if key in computation_cache:
        return computation_cache[key]

    # Compute, cache, and return result
    result = matrix_operations(matrix)
    computation_cache[key] = result
    return result



computation_cache = {}

def advanced_matrix_ops(matrix, use_cache=True, cache_key=None):
    """Performs advanced matrix operations with optional caching.

    Validates that matrix is a non-empty square numeric matrix.
    If use_cache is True, caches the result under cache_key or an implicit key.
    Returns the result dict from matrix_operations or None on invalid input.
    """
    # Validate matrix structure
    if not isinstance(matrix, list) or len(matrix) == 0:
        return None
    n = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None

    # If caching disabled, always compute fresh and do not populate cache
    if not use_cache:
        return matrix_operations(matrix)

    # Determine cache key
    key = cache_key if cache_key is not None else tuple(tuple(row) for row in matrix)

    # Return cached result if available
    if key in computation_cache:
        return computation_cache[key]

    # Compute, cache, and return result
    result = matrix_operations(matrix)
    computation_cache[key] = result
    return result
