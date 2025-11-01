import sys
import os
# Add framework directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add project root to Python path (for dataset/ and other top-level imports)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
import unit_test.functions as uf

@pytest.fixture(autouse=True)
def clear_cache():
    uf.computation_cache.clear()
    yield
    uf.computation_cache.clear()

def test_computation_cache_exists_and_is_dict():
    assert hasattr(uf, 'computation_cache'), "computation_cache should be defined in unit_test.functions"
    assert isinstance(uf.computation_cache, dict), "computation_cache should be a dict"

def test_matrix_multiplication_normal():
    a = [[1, 2, 3],
         [4, 5, 6]]
    b = [[7, 8],
         [9, 10],
         [11, 12]]
    expected = [[58, 64], [139, 154]]
    result = uf.matrix_operations(a, b)
    assert result == expected
    # After one call, cache should have one entry
    assert len(uf.computation_cache) == 1

def test_matrix_multiplication_single_element():
    a = [[5]]
    b = [[-3]]
    expected = [[-15]]
    result = uf.matrix_operations(a, b)
    assert result == expected
    assert len(uf.computation_cache) == 1

def test_matrix_multiplication_cache_hit():
    a1 = [[2, 0], [0, 2]]
    b1 = [[1, 1], [1, 1]]
    r1 = uf.matrix_operations(a1, b1)
    # create new objects with same content
    a2 = [[2, 0], [0, 2]]
    b2 = [[1, 1], [1, 1]]
    r2 = uf.matrix_operations(a2, b2)
    # Should return same object from cache
    assert r1 is r2
    # Cache still has only one entry
    assert len(uf.computation_cache) == 1

def test_matrix_multiplication_different_matrices_cache_miss():
    a = [[1, 0], [0, 1]]
    b = [[1, 2], [3, 4]]
    c = [[2, 3], [4, 5]]
    # First call with (a, b)
    _ = uf.matrix_operations(a, b)
    # Second call with (a, c)
    _ = uf.matrix_operations(a, c)
    assert len(uf.computation_cache) == 2

@pytest.mark.parametrize("a, b", [
    # mismatched dimensions: 2x3 times 2x2
    ([[1, 2, 3], [4, 5, 6]], [[1, 2], [3, 4]]),
    # inner dimension mismatch
    ([[1, 2]], [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
])
def test_matrix_multiplication_invalid_dimension(a, b):
    result = uf.matrix_operations(a, b)
    assert result is None
    assert len(uf.computation_cache) == 0

@pytest.mark.parametrize("a, b", [
    (None, [[1]]),
    ([[1]], None),
    ("not a matrix", [[1]]),
    ([[1]], "not a matrix"),
    ([1, 2, 3], [[1], [2], [3]]),
])
def test_matrix_multiplication_invalid_input_types(a, b):
    result = uf.matrix_operations(a, b)
    assert result is None
    assert len(uf.computation_cache) == 0

def test_matrix_multiplication_empty_matrices():
    # define empty matrices
    a = []
    b = []
    result = uf.matrix_operations(a, b)
    assert result is None
    assert len(uf.computation_cache) == 0

if __name__ == "__main__":
    pytest.main([__file__])