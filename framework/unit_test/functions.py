from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def matrix_operations(A, B):
    '''Performs matrix multiplication of two matrices A and B and caches the result.'''
    # Validate input types
    if not isinstance(A, list) or not isinstance(B, list):
        return None
    # Validate non-empty matrices
    if len(A) == 0 or len(B) == 0:
        return None
    # Validate rows of A
    if any(not isinstance(row, list) for row in A):
        return None
    # Validate rows of B
    if any(not isinstance(row, list) for row in B):
        return None
    # Validate consistent row lengths and numeric entries for A
    n_cols_A = len(A[0])
    if n_cols_A == 0:
        return None
    for row in A:
        if len(row) != n_cols_A:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None
    # Validate consistent row lengths and numeric entries for B
    n_cols_B = len(B[0])
    if n_cols_B == 0:
        return None
    for row in B:
        if len(row) != n_cols_B:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None
    # Validate multiplication dimensions
    if n_cols_A != len(B):
        return None
    # Build cache key
    key = str(tuple(map(tuple, A))) + '_' + str(tuple(map(tuple, B)))
    # Return cached result if available
    if key in computation_cache:
        return computation_cache[key]
    # Compute multiplication
    result = []
    for i in range(len(A)):
        row_res = []
        for j in range(n_cols_B):
            sum_cell = 0
            for k in range(n_cols_A):
                sum_cell += A[i][k] * B[k][j]
            row_res.append(sum_cell)
        result.append(row_res)
    # Cache and return
    computation_cache[key] = result
    return result
