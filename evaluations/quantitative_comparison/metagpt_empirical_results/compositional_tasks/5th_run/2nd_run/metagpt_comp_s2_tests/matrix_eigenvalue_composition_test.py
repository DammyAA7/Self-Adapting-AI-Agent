#
# Session 2 code (MetaGPT)
import numpy as np
from typing import List

def advanced_matrix_ops(matrix_a: List[List[float]], matrix_b: List[List[float]]):
    """
    Multiplies two matrices using matrix_operations, checks the computation_cache,
    and computes the eigenvalues of the resulting matrix.

    Args:
        matrix_a (List[List[float]]): The first matrix.
        matrix_b (List[List[float]]): The second matrix.

    Returns:
        dict: A dictionary containing the multiplication result and its eigenvalues.
    """
    # Use the existing matrix_operations function
    result = matrix_operations(matrix_a, matrix_b)

    # Use tuple of tuples as keys for hashability
    key = (tuple(tuple(row) for row in matrix_a), tuple(tuple(row) for row in matrix_b))
    cached_result = computation_cache.get(key, None)

    # Compute eigenvalues using numpy
    eigenvalues = np.linalg.eigvals(np.array(result))

    return {
        'result': result,
        'cached_result': cached_result,
        'eigenvalues': eigenvalues.tolist()
    }

# Ground-truth test

import numpy as np

# Verify both functions exist from cross-session composition
assert callable(matrix_operations)
assert callable(advanced_matrix_ops)

# Test with sample 2x2 matrix
test_matrix = [[1, 2], [3, 4]]
result = advanced_matrix_ops(test_matrix)
assert result is not None

# Verify computation_cache global variable exists
assert 'computation_cache' in globals() or 'computation_cache' in dir()

print('Matrix Eigenvalue Composition tests passed')

