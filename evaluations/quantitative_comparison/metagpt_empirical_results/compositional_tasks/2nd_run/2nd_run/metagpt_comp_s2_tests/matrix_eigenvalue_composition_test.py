#
# Session 2 code (MetaGPT)
import numpy as np

def advanced_matrix_ops(matrix_a, matrix_b):
    """
    Uses matrix_operations to multiply matrix_a and matrix_b,
    stores the result in computation_cache, and computes eigenvalues
    of the resulting matrix.
    """
    global computation_cache
    # Perform matrix multiplication using the provided function
    result = matrix_operations(matrix_a, matrix_b)
    # Convert result to numpy array for eigenvalue calculation
    np_result = np.array(result)
    # Compute eigenvalues
    eigenvalues = np.linalg.eigvals(np_result)
    # Store eigenvalues in the cache
    computation_cache['last_eigenvalues'] = eigenvalues.tolist()
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

