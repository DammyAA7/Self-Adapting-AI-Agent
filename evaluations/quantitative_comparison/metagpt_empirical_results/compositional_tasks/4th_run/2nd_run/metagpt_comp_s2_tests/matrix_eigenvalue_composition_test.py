#
# Session 2 code (MetaGPT)
import numpy as np

def advanced_matrix_ops():
    """
    Uses the existing computation_cache and matrix_operations to perform eigenvalue calculations.
    Assumes computation_cache['last_result'] contains the latest matrix multiplication result.
    Returns the eigenvalues of the last result matrix.
    """
    # Ensure the last result exists
    if 'last_result' not in computation_cache:
        raise ValueError("No previous matrix operation result found in computation_cache.")
    last_result = computation_cache['last_result']
    # Convert to numpy array for eigenvalue calculation
    matrix_np = np.array(last_result)
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvals(matrix_np)
    return eigenvalues

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

