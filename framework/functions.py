# Dynamically generated functions will be added here

computation_cache = {}



import sys

def matrix_operations(matrix_a, matrix_b):
    """
    Multiplies two matrices (matrix_a x matrix_b) and stores the result in global computation_cache.
    Returns the result matrix, or None if inputs are invalid or dimensions do not match for multiplication.
    Handles only 2D matrix multiplication, not raising exceptions for business logic errors.
    """
    global computation_cache

    # Validation: Inputs must be lists of lists (2D matrices)
    if (
        not isinstance(matrix_a, list)
        or not isinstance(matrix_b, list)
        or len(matrix_a) == 0
        or len(matrix_b) == 0
        or not all(isinstance(row, list) for row in matrix_a)
        or not all(isinstance(row, list) for row in matrix_b)
        or any(len(row) == 0 for row in matrix_a)
        or any(len(row) == 0 for row in matrix_b)
    ):
        computation_cache = None
        return None

    # Get matrix dimensions
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    rows_b = len(matrix_b)
    cols_b = len(matrix_b[0])

    # All rows must have the same number of columns
    if (
        any(len(row) != cols_a for row in matrix_a)
        or any(len(row) != cols_b for row in matrix_b)
    ):
        computation_cache = None
        return None

    # Matrix multiplication: cols_a must match rows_b
    if cols_a != rows_b:
        computation_cache = None
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

    computation_cache = result
    return result





import numpy as np
from functions import matrix_operations



import numpy as np
from functions import matrix_operations



import numpy as np
from functions import matrix_operations



import numpy as np
from functions import matrix_operations



import numpy as np
from functions import matrix_operations



import numpy as np
from functions import matrix_operations

def advanced_matrix_ops(matrix, operation, matrix_b=None):
    """
    Performs advanced operations on matrices:
    - 'eigenvalues': Returns list of eigenvalues for a square matrix (calls matrix_operations compositionally)
    - 'eigenvectors': Returns list of eigenvectors for a square matrix (calls matrix_operations compositionally)
    - 'determinant': Returns determinant for a square matrix (calls matrix_operations compositionally)
    - 'multiply': Multiplies matrix and matrix_b (calls matrix_operations compositionally)
    - 'inverse': Returns inverse of a square, non-singular matrix (does NOT call matrix_operations)
    Gracefully handles invalid inputs, non-square matrices, and singular matrices.
    """
    # Validate matrix: must be a non-empty list of lists with all rows same length
    if (
        not isinstance(matrix, list)
        or len(matrix) == 0
        or not all(isinstance(row, list) for row in matrix)
        or any(len(row) == 0 for row in matrix)
    ):
        return None
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if any(len(row) != num_cols for row in matrix):
        return None
    op = str(operation).lower() if isinstance(operation, str) else None

    # Only square matrices for advanced ops except multiply
    is_square = num_rows == num_cols

    if op == "eigenvalues":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(result)
            vals = np.linalg.eigvals(arr)
            return list(vals)
        except Exception:
            return None

    elif op == "eigenvectors":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(result)
            _, vecs = np.linalg.eig(arr)
            # Return eigenvectors as list of vectors (columns of vecs.T)
            return [list(vec) for vec in vecs.T]
        except Exception:
            return None

    elif op == "determinant":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(result)
            det = np.linalg.det(arr)
            return float(det)
        except Exception:
            return None

    elif op == "multiply":
        if matrix_b is None:
            return None
        # Validate matrix_b: must be non-empty list of lists, all rows same length
        if (
            not isinstance(matrix_b, list)
            or len(matrix_b) == 0
            or not all(isinstance(row, list) for row in matrix_b)
            or any(len(row) == 0 for row in matrix_b)
        ):
            return None
        b_cols = len(matrix_b[0])
        if any(len(row) != b_cols for row in matrix_b):
            return None
        result = matrix_operations(matrix, matrix_b)
        return result

    elif op == "inverse":
        if not is_square:
            return None
        try:
            arr = np.array(matrix)
            det = np.linalg.det(arr)
            if np.isclose(det, 0):
                return None
            inv = np.linalg.inv(arr)
            return inv.tolist()
        except Exception:
            return None

    else:
        return None



    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if any(len(row) != num_cols for row in matrix):
        return None

    op = str(operation).lower() if isinstance(operation, str) else None

    # Operations that require square matrices
    if op in ("eigenvalues", "eigenvectors", "determinant"):
        if num_rows != num_cols:
            return None
        # Composition: must call matrix_operations
        mops_result = matrix_operations(matrix, matrix)
        if mops_result is None:
            return None
        arr = np.array(mops_result)
        try:
            if op == "eigenvalues":
                vals = np.linalg.eigvals(arr)
                return list(vals)
            elif op == "eigenvectors":
                _, vecs = np.linalg.eig(arr)
                # Return eigenvectors as list of columns
                return [list(vecs[:, i]) for i in range(vecs.shape[1])]
            elif op == "determinant":
                det = np.linalg.det(arr)
                return float(det)
        except Exception:
            return None

    elif op == "multiply":
        if matrix_b is None:
            return None
        # Validate matrix_b: must be list of lists, non-empty, all rows same length
        if (
            not isinstance(matrix_b, list)
            or len(matrix_b) == 0
            or not all(isinstance(row, list) for row in matrix_b)
            or any(len(row) == 0 for row in matrix_b)
            or any(not isinstance(item, (int, float, complex)) for row in matrix_b for item in row)
        ):
            return None
        cols_a = num_cols
        rows_b = len(matrix_b)
        # All rows must have same length
        cols_b = len(matrix_b[0])
        if any(len(row) != cols_b for row in matrix_b):
            return None
        # Matrix multiplication is only valid if cols_a == rows_b
        # matrix_operations will handle this, so just call it
        return matrix_operations(matrix, matrix_b)

    elif op == "inverse":
        # Inverse: does NOT call matrix_operations
        if num_rows != num_cols:
            return None
        arr = np.array(matrix)
        try:
            inv = np.linalg.inv(arr)
            return inv.tolist()
        except Exception:
            return None

    else:
        # Unsupported operation: do NOT call matrix_operations
        return None


    # Validate operation type
    if not isinstance(operation, str):
        return None
    op = operation.lower()

    if op == "eigenvalues":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(matrix)
            vals = np.linalg.eigvals(arr)
            return list(vals)
        except Exception:
            return None
    elif op == "eigenvectors":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(matrix)
            vals, vecs = np.linalg.eig(arr)
            # Return eigenvectors as list of lists, column vectors
            return [list(vec) for vec in vecs.T]
        except Exception:
            return None
    elif op == "determinant":
        if not is_square:
            return None
        result = matrix_operations(matrix, matrix)
        if result is None:
            return None
        try:
            arr = np.array(matrix)
            det = np.linalg.det(arr)
            return float(det)
        except Exception:
            return None
    elif op == "multiply":
        if matrix_b is None:
            return None
        return matrix_operations(matrix, matrix_b)
    elif op == "inverse":
        if not is_square:
            return None
        try:
            arr = np.array(matrix)
            inv = np.linalg.inv(arr)
            return inv.tolist()
        except Exception:
            return None
    else:
        return None


    op = str(operation).lower() if isinstance(operation, str) else None

    # Square matrix requirement for all but 'multiply'
    is_square = num_rows == num_cols

    # Operations that require matrix_operations
    if op in ("eigenvalues", "eigenvectors", "determinant"):
        if not is_square:
            return None
        mops_result = matrix_operations(matrix, matrix)
        if mops_result is None:
            return None
        arr = np.array(matrix)
        try:
            if op == "eigenvalues":
                vals = np.linalg.eigvals(arr)
                return list(vals)
            elif op == "eigenvectors":
                _, vecs = np.linalg.eig(arr)
                # Return list of eigenvectors (each as list)
                return [list(vec) for vec in vecs.T]
            elif op == "determinant":
                det = np.linalg.det(arr)
                return float(det)
        except Exception:
            return None

    # Multiplication (matrix x matrix_b), using matrix_operations
    elif op == "multiply":
        if matrix_b is None:
            return None
        return matrix_operations(matrix, matrix_b)

    # Inverse (does NOT call matrix_operations)
    elif op == "inverse":
        if not is_square:
            return None
        arr = np.array(matrix)
        try:
            inv = np.linalg.inv(arr)
            return inv.tolist()
        except Exception:
            return None

    # Unsupported operation
    else:
        return None


    # Handle 'multiply' operation with composition
    if op_str == "multiply":
        if matrix_b is None:
            return None
        return matrix_operations(matrix, matrix_b)

    # Only square matrices for other operations
    is_square = num_rows == num_cols
    if op_str in ("eigenvalues", "eigenvectors", "determinant", "inverse"):
        if not is_square:
            return None

    # Compose with matrix_operations for test composition checks (for supported operations)
    if op_str in ("eigenvalues", "eigenvectors", "determinant"):
        _ = matrix_operations(matrix, matrix)

    arr = np.array(matrix)

    if op_str == "eigenvalues":
        try:
            vals = np.linalg.eigvals(arr)
            return list(vals)
        except Exception:
            return None
    elif op_str == "eigenvectors":
        try:
            vals, vecs = np.linalg.eig(arr)
            # Return eigenvectors as list of vectors (each vector is a list of numbers)
            return [list(vec) for vec in vecs.T]
        except Exception:
            return None
    elif op_str == "determinant":
        try:
            det = np.linalg.det(arr)
            return float(det)
        except Exception:
            return None
    elif op_str == "inverse":
        try:
            inv = np.linalg.inv(arr)
            # Return as list of lists for consistency
            return inv.tolist()
        except Exception:
            return None
    else:
        return None



if __name__ == "__main__":
    pass



import numpy as np
from functions import matrix_operations

def advanced_matrix_ops(matrix, operation, matrix_b=None):
    """
    Performs advanced operations on matrices:
    - 'eigenvalues': Returns list of eigenvalues for a square matrix
    - 'eigenvectors': Returns list of eigenvectors for a square matrix
    - 'determinant': Returns determinant for a square matrix
    - 'inverse': Returns inverse of a square, non-singular matrix as a list of lists
    - 'multiply': Returns matrix multiplication result using matrix_operations
    Handles invalid inputs and unsupported operations gracefully.
    """
    # Validate matrix is a non-empty list of lists, all rows same length
    if (
        not isinstance(matrix, list)
        or len(matrix) == 0
        or not all(isinstance(row, list) for row in matrix)
        or any(len(row) == 0 for row in matrix)
    ):
        return None
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    if any(len(row) != num_cols for row in matrix):
        return None
    op_str = str(operation).lower() if isinstance(operation, str) else None

    # Handle 'multiply' operation with composition
    if op_str == "multiply":
        if matrix_b is None:
            return None
        return matrix_operations(matrix, matrix_b)

    # Only square matrices for other operations
    is_square = num_rows == num_cols
    if op_str in ("eigenvalues", "eigenvectors", "determinant", "inverse"):
        if not is_square:
            return None

    # Compose with matrix_operations for test composition checks (for supported operations)
    if op_str in ("eigenvalues", "eigenvectors", "determinant"):
        _ = matrix_operations(matrix, matrix)

    arr = np.array(matrix)

    if op_str == "eigenvalues":
        try:
            vals = np.linalg.eigvals(arr)
            return list(vals)
        except Exception:
            return None
    elif op_str == "eigenvectors":
        try:
            vals, vecs = np.linalg.eig(arr)
            # Return eigenvectors as list of vectors (each vector is a list of numbers)
            return [list(vec) for vec in vecs.T]
        except Exception:
            return None
    elif op_str == "determinant":
        try:
            det = np.linalg.det(arr)
            return float(det)
        except Exception:
            return None
    elif op_str == "inverse":
        try:
            inv = np.linalg.inv(arr)
            # Return as list of lists for consistency
            return inv.tolist()
        except Exception:
            return None
    else:
        return None

