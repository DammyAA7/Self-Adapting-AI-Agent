computation_cache = {}

def matrix_operations(matrix_a, matrix_b):
    """
    Performs basic matrix multiplication between matrix_a and matrix_b.
    Stores the result in the global variable computation_cache.
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