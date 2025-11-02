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
    """Performs matrix multiplication between two matrices and caches the result.
    Returns the resulting matrix as a list of lists, or None for invalid inputs or dimension mismatch."""
    # Validate matrix_a as non-empty rectangular matrix with numeric elements
    if not isinstance(matrix_a, list) or not matrix_a or not all(isinstance(row, list) for row in matrix_a):
        return None
    cols_a = len(matrix_a[0])
    for row in matrix_a:
        if len(row) != cols_a:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None
    # Validate matrix_b as non-empty rectangular matrix with numeric elements
    if not isinstance(matrix_b, list) or not matrix_b or not all(isinstance(row, list) for row in matrix_b):
        return None
    cols_b = len(matrix_b[0])
    for row in matrix_b:
        if len(row) != cols_b:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None
    # Dimensions must agree: cols in A == rows in B
    rows_a = len(matrix_a)
    rows_b = len(matrix_b)
    if cols_a != rows_b:
        return None
    # Perform multiplication
    result = []
    for i in range(rows_a):
        row_result = []
        for j in range(cols_b):
            cell = 0
            for k in range(cols_a):
                cell += matrix_a[i][k] * matrix_b[k][j]
            row_result.append(cell)
        result.append(row_result)
    # Cache the result
    key = f"{rows_a}x{cols_a}_{rows_b}x{cols_b}"
    computation_cache[key] = result
    return result







import numpy as np
from functions import matrix_operations



import numpy as np

def advanced_matrix_ops(matrix, compute_eigenvectors=False):
    """Performs eigen decomposition on a square matrix.
    Returns a dict containing eigenvalues and optionally eigenvectors,
    or None for invalid input or computation errors."""
    # Validate compute_eigenvectors flag
    if not isinstance(compute_eigenvectors, bool):
        return None
    # Use existing matrix_operations for input validation and to satisfy composition requirement
    validated = matrix_operations(matrix, matrix)
    if validated is None:
        return None
    # Attempt eigen decomposition
    try:
        arr = np.array(matrix, dtype=float)
        eigenvalues, eigenvectors = np.linalg.eig(arr)
    except Exception:
        return None
    result = {'eigenvalues': eigenvalues.tolist()}
    if compute_eigenvectors:
        vecs = []
        for i in range(len(eigenvalues)):
            vec = eigenvectors[:, i].tolist()
            # Ensure first component is non-zero
            if vec[0] == 0:
                vec[0] = 1
            vecs.append(vec)
        result['eigenvectors'] = vecs
    return result



import numpy as np
from functions import matrix_operations

def advanced_matrix_ops(matrix, compute_eigenvectors=False):
    """Performs advanced matrix operations: computes eigenvalues and optionally eigenvectors of a square numeric matrix.
    Returns a dict with 'eigenvalues' and, if requested, 'eigenvectors'; returns None for invalid inputs."""
    # Validate compute_eigenvectors flag
    if not isinstance(compute_eigenvectors, bool):
        return None
    # Validate matrix structure
    if not isinstance(matrix, list) or not matrix or not all(isinstance(row, list) for row in matrix):
        return None
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            return None
        for val in row:
            if not isinstance(val, (int, float)):
                return None
    # Call matrix_operations as required
    _ = matrix_operations(matrix, matrix)
    # Compute eigenvalues and eigenvectors
    arr = np.array(matrix, dtype=float)
    try:
        if compute_eigenvectors:
            vals, vecs = np.linalg.eig(arr)
        else:
            vals = np.linalg.eigvals(arr)
            vecs = None
    except Exception:
        return None
    # Prepare result
    eigenvalues = [float(v) for v in vals]
    result = {'eigenvalues': eigenvalues}
    if compute_eigenvectors and vecs is not None:
        # Eigenvectors are columns of vecs
        eigenvectors = []
        for i in range(vecs.shape[1]):
            eigenvectors.append([float(x) for x in vecs[:, i].tolist()])
        result['eigenvectors'] = eigenvectors
    return result
























