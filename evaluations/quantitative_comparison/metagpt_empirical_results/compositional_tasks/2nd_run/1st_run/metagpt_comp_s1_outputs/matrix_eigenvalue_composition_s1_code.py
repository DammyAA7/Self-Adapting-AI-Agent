computation_cache = {}

def matrix_operations(matrix_a, matrix_b)

    global computation_cache
    # Check if multiplication is possible
    if len(matrix_a[0]) != len(matrix_b):
        raise ValueError("Number of columns in matrix_a must equal number of rows in matrix_b.")
    result = []
    for i in range(len(matrix_a)):
        row = []
        for j in range(len(matrix_b[0])):
            sum_product = 0
            for k in range(len(matrix_b)):
                sum_product += matrix_a[i][k] * matrix_b[k][j]
            row.append(sum_product)
        result.append(row)
    computation_cache['last_result'] = result
    return result