import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from unit_test.functions import *
import numpy as np
from unittest.mock import patch

@pytest.fixture
def example_matrix():
    # Simple symmetric matrix with known eigenvalues
    return [[1, 2], [2, 3]]

@pytest.fixture
def singular_matrix():
    # Singular matrix (determinant zero)
    return [[1, 2], [2, 4]]

@pytest.fixture
def non_square_matrix():
    # Non-square matrix for invalid input
    return [[1, 2, 3], [4, 5, 6]]

@pytest.fixture
def bad_matrix():
    # Not a matrix (invalid type)
    return [1, 2, 3]

def test_advanced_matrix_ops_eigenvalues_basic(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix  # dummy value just for composition
        result = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)
        assert isinstance(result, (list, np.ndarray))
        assert pytest.approx(sorted(result), abs=1e-3) == sorted(np.linalg.eigvals(np.array(example_matrix)))

def test_advanced_matrix_ops_eigenvectors_basic(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix  # dummy value just for composition
        result = advanced_matrix_ops(example_matrix, operation='eigenvectors')
        mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)
        assert isinstance(result, (list, np.ndarray))
        eigvecs = np.linalg.eig(np.array(example_matrix))[1]
        if isinstance(result, list):
            result = np.array(result)
        # For reinforced requirement, check shape and numerical correctness
        assert result.shape == eigvecs.T.shape or result.shape == eigvecs.shape
        # Compare at least one vector numerically
        assert np.allclose(sorted(np.abs(result[0])), sorted(np.abs(eigvecs.T[0])), rtol=1e-3, atol=1e-3)

def test_advanced_matrix_ops_inverse(example_matrix):
    # Should NOT call matrix_operations
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='inverse')
        mock_matrix_operations.assert_not_called()
        expected = np.linalg.inv(np.array(example_matrix))
        if isinstance(result, list):
            result = np.array(result)
        assert np.allclose(result, expected)

def test_advanced_matrix_ops_inverse_singular(singular_matrix):
    # Should NOT call matrix_operations
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(singular_matrix, operation='inverse')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_non_square_matrix(non_square_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(non_square_matrix, operation='eigenvalues')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_bad_matrix_type(bad_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(bad_matrix, operation='eigenvalues')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_invalid_operation(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='not_supported')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_empty_matrix():
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops([], operation='eigenvalues')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_composition_with_matrix_operations(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = [[0.5, -1], [-1, 0.5]]
        result = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        mock_matrix_operations.assert_any_call(example_matrix, example_matrix)
        assert isinstance(result, (list, np.ndarray))
        matrix_b = [[1,0],[0,1]]
        result_mult = advanced_matrix_ops(example_matrix, operation='multiply', matrix_b=matrix_b)
        assert mock_matrix_operations.call_args_list[0] == ((example_matrix, example_matrix),)
        assert mock_matrix_operations.call_args_list[1] == ((example_matrix, matrix_b),)
        assert result_mult == [[0.5, -1], [-1, 0.5]]
        assert mock_matrix_operations.call_count == 2

def test_advanced_matrix_ops_determinant_calls_matrix_operations(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix  # dummy value just for composition
        result = advanced_matrix_ops(example_matrix, operation='determinant')
        mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)
        expected = float(np.linalg.det(np.array(example_matrix)))
        assert pytest.approx(result, abs=1e-3) == expected

def test_advanced_matrix_ops_integration_matrix_operations_multiplication(example_matrix):
    matrix_b = [[2,0],[0,2]]
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = [[4, 4], [8, 8]]
        result = advanced_matrix_ops(example_matrix, operation='multiply', matrix_b=matrix_b)
        mock_matrix_operations.assert_called_once_with(example_matrix, matrix_b)
        assert result == [[4, 4], [8, 8]]

def test_advanced_matrix_ops_handles_duplicate_operation(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix
        result1 = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        result2 = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        assert mock_matrix_operations.call_count == 2
        assert np.allclose(sorted(result1), sorted(result2))
        assert mock_matrix_operations.call_args_list[0] == ((example_matrix, example_matrix),)
        assert mock_matrix_operations.call_args_list[1] == ((example_matrix, example_matrix),)

def test_advanced_matrix_ops_handles_large_matrix():
    matrix = np.random.rand(10,10)
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = matrix.tolist()
        result = advanced_matrix_ops(matrix.tolist(), operation='eigenvalues')
        expected = np.linalg.eigvals(matrix)
        mock_matrix_operations.assert_called_once_with(matrix.tolist(), matrix.tolist())
        assert len(result) == 10
        assert np.allclose(sorted(result), sorted(expected), rtol=1e-3, atol=1e-3)

def test_advanced_matrix_ops_matrix_operations_not_called_for_inverse(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='inverse')
        mock_matrix_operations.assert_not_called()
        expected = np.linalg.inv(np.array(example_matrix))
        if isinstance(result, list):
            result = np.array(result)
        assert np.allclose(result, expected)

def test_advanced_matrix_ops_matrix_operations_not_called_for_unsupported(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='not_supported')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_multiply_matrix_operations_called(example_matrix):
    matrix_b = [[5, 6], [7, 8]]
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = [[19, 22], [43, 50]]
        result = advanced_matrix_ops(example_matrix, operation='multiply', matrix_b=matrix_b)
        mock_matrix_operations.assert_called_once_with(example_matrix, matrix_b)
        assert result == [[19, 22], [43, 50]]

def test_advanced_matrix_ops_multiply_with_missing_matrix_b(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='multiply')
        mock_matrix_operations.assert_not_called()
        assert result is None or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_matrix_operations_called_for_all_relevant_ops(example_matrix):
    relevant_ops = ['eigenvalues', 'eigenvectors', 'determinant', 'multiply']
    matrix_b = [[3, 1], [2, 4]]
    for op in relevant_ops:
        with patch('functions.matrix_operations') as mock_matrix_operations:
            mock_matrix_operations.return_value = example_matrix
            if op == 'multiply':
                result = advanced_matrix_ops(example_matrix, operation=op, matrix_b=matrix_b)
                mock_matrix_operations.assert_called_once_with(example_matrix, matrix_b)
                assert result == example_matrix
                assert mock_matrix_operations.call_count == 1
            else:
                result = advanced_matrix_ops(example_matrix, operation=op)
                mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)
                assert result is not None
                assert mock_matrix_operations.call_count == 1

def test_advanced_matrix_ops_matrix_operations_not_called_for_inverse_and_unsupported(example_matrix):
    for op in ['inverse', 'not_a_real_op']:
        with patch('functions.matrix_operations') as mock_matrix_operations:
            result = advanced_matrix_ops(example_matrix, operation=op)
            mock_matrix_operations.assert_not_called()
            assert result is None or isinstance(result, list) or (isinstance(result, bool) and result is False)

def test_advanced_matrix_ops_matrix_operations_call_count_for_multiple_ops(example_matrix):
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix
        result1 = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        result2 = advanced_matrix_ops(example_matrix, operation='determinant')
        result3 = advanced_matrix_ops(example_matrix, operation='eigenvectors')
        assert mock_matrix_operations.call_count == 3
        expected_calls = [
            ((example_matrix, example_matrix),),
            ((example_matrix, example_matrix),),
            ((example_matrix, example_matrix),)
        ]
        assert mock_matrix_operations.call_args_list == expected_calls

def test_advanced_matrix_ops_matrix_operations_call_count_with_multiply_and_advanced(example_matrix):
    matrix_b = [[1, 0], [0, 1]]
    with patch('functions.matrix_operations') as mock_matrix_operations:
        mock_matrix_operations.return_value = example_matrix
        result1 = advanced_matrix_ops(example_matrix, operation='multiply', matrix_b=matrix_b)
        result2 = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        assert mock_matrix_operations.call_count == 2
        assert mock_matrix_operations.call_args_list[0] == ((example_matrix, matrix_b),)
        assert mock_matrix_operations.call_args_list[1] == ((example_matrix, example_matrix),)
        assert result1 == example_matrix
        assert result2 is not None

def test_advanced_matrix_ops_matrix_operations_side_effects(example_matrix):
    # Reinforced requirement: matrix_operations side effect should set global computation_cache
    import functions
    with patch('functions.matrix_operations', wraps=functions.matrix_operations) as mock_matrix_operations:
        # computation_cache should be set to the result of matrix_operations
        result = advanced_matrix_ops(example_matrix, operation='multiply', matrix_b=example_matrix)
        assert functions.computation_cache == result
        mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)

def test_advanced_matrix_ops_matrix_operations_side_effects_for_eigenvalues(example_matrix):
    import functions
    with patch('functions.matrix_operations', wraps=functions.matrix_operations) as mock_matrix_operations:
        result = advanced_matrix_ops(example_matrix, operation='eigenvalues')
        # computation_cache should be set to the result of matrix_operations
        assert functions.computation_cache == example_matrix
        mock_matrix_operations.assert_called_once_with(example_matrix, example_matrix)

if __name__ == "__main__":
    pytest.main([__file__])
