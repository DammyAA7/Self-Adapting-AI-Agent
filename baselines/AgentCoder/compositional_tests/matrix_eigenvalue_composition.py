
import numpy as np

def advanced_matrix_ops():
    '''
    Load the previous session and create a function called advanced_matrix_ops 
    that uses the existing matrix_operations function and computation_cache 
    to perform eigenvalue calculations.
    '''
    # Step 1: Call matrix_operations() to ensure cache has previous computation
    matrix_operations()
    
    # Step 2: Retrieve the result matrix
    global computation_cache
    result = computation_cache.get('result')
    
    if result is None:
        raise ValueError("No result found in computation_cache.")
    
    # Step 3: Convert to numpy array for eigenvalue calculation
    result_np = np.array(result)
    
    # Step 4: Check if the matrix is square (eigenvalues only for square matrices)
    if result_np.shape[0] != result_np.shape[1]:
        raise ValueError("Cannot compute eigenvalues: Resulting matrix is not square.")
    
    # Step 5: Compute eigenvalues
    eigenvalues = np.linalg.eigvals(result_np)
    
    # Step 6: Store eigenvalues in computation_cache
    computation_cache['eigenvalues'] = eigenvalues.tolist()  # Convert to list for JSON serializability if needed

    # (Optional) Print or return eigenvalues
    print("Eigenvalues of the result matrix:", eigenvalues)



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

