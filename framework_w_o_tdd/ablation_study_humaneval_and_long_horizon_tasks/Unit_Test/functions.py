from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
computation_cache = None

def matrix_operations(matrix_a, matrix_b):
    """Performs matrix multiplication of two matrices(matrix_a m×n, matrix_b n×p),
    stores the resulting matrix in the global variable computation_cache, and returns it."""
    # Validate that both inputs are 2D lists
    if not isinstance(matrix_a, list) or not isinstance(matrix_b, list):
        raise TypeError("Both matrix_a and matrix_b must be lists.")
    if not matrix_a or not matrix_b:
        raise ValueError("Input matrices cannot be empty.")
    if any(not isinstance(row, list) for row in matrix_a):
        raise TypeError("matrix_a must be a two-dimensional list.")
    if any(not isinstance(row, list) for row in matrix_b):
        raise TypeError("matrix_b must be a two-dimensional list.")
    # Validate consistent row lengths
    num_cols_a = len(matrix_a[0])
    if any(len(row) != num_cols_a for row in matrix_a):
        raise ValueError("All rows in matrix_a must have the same length.")
    num_cols_b = len(matrix_b[0])
    if any(len(row) != num_cols_b for row in matrix_b):
        raise ValueError("All rows in matrix_b must have the same length.")
    # Check dimensions for multiplication
    num_rows_a = len(matrix_a)
    num_rows_b = len(matrix_b)
    if num_cols_a != num_rows_b:
        raise ValueError("Incompatible dimensions for matrix multiplication.")
    # Perform multiplication
    result = [[0 for _ in range(num_cols_b)] for _ in range(num_rows_a)]
    for i in range(num_rows_a):
        for j in range(num_cols_b):
            total = 0
            for k in range(num_cols_a):
                a_val = matrix_a[i][k]
                b_val = matrix_b[k][j]
                if not isinstance(a_val, (int, float)) or not isinstance(b_val, (int, float)):
                    raise TypeError("Matrix elements must be numeric.")
                total += a_val * b_val
            result[i][j] = total
    # Store in global cache
    global computation_cache
    computation_cache = result
    return result
