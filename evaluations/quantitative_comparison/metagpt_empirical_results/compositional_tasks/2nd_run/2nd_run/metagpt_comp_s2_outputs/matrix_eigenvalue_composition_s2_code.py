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