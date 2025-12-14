import numpy as np

# Global cache for computation results
computation_cache = {}

def matrix_operations(matrix_a, matrix_b):
    """
    Performs basic matrix multiplication between matrix_a and matrix_b.
    Stores the result in the global variable computation_cache.

    Args:
        matrix_a (list of list of float): The first matrix.
        matrix_b (list of list of float): The second matrix.

    Returns:
        list of list of float: The result of matrix multiplication.
    """
    global computation_cache
    # Check if matrices can be multiplied
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Number of columns in matrix_a must equal number of rows in matrix_b.")
    result = [[0 for _ in range(len(matrix_b[0]))] for _ in range(len(matrix_a))]
    for i in range(len(matrix_a)):
        for j in range(len(matrix_b[0])):
            for k in range(len(matrix_b)):
                result[i][j] += matrix_a[i][k] * matrix_b[k][j]
    computation_cache['last_result'] = result
    return result

def advanced_matrix_ops(matrix_a, matrix_b):
    """
    Uses matrix_operations to multiply matrix_a and matrix_b, then computes the eigenvalues
    of the resulting matrix. Stores both the multiplication result and eigenvalues in computation_cache.

    Args:
        matrix_a (list of list of float): The first matrix.
        matrix_b (list of list of float): The second matrix.

    Returns:
        dict: A dictionary with keys 'product' and 'eigenvalues'.
              'product' is the matrix multiplication result (list of lists),
              'eigenvalues' is a list of eigenvalues (complex or float).
    """
    # Perform matrix multiplication using the existing function
    product = matrix_operations(matrix_a, matrix_b)

    # Convert the result to a numpy array for eigenvalue calculation
    product_np = np.array(product, dtype=float)

    # Check if the product is a square matrix for eigenvalue calculation
    if product_np.shape[0] != product_np.shape[1]:
        raise ValueError("Eigenvalues can only be computed for square matrices. "
                         "The product matrix has shape {}.".format(product_np.shape))

    # Compute eigenvalues
    eigenvalues = np.linalg.eigvals(product_np)
    eigenvalues_list = eigenvalues.tolist()

    # Store in computation_cache
    computation_cache['eigenvalues'] = eigenvalues_list

    return {
        'product': product,
        'eigenvalues': eigenvalues_list
    }