import sys
import os
# Add framework directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Add project root to Python path (for dataset/ and other top-level imports)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
import numpy as np
from unittest.mock import patch
from unit_test.functions import advanced_matrix_ops

def test_advanced_matrix_ops_returns_eigenvalues_only_with_valid_matrix():
    A = [[2, 1], [1, 2]]
    result = advanced_matrix_ops(A)
    assert isinstance(result, dict)
    assert 'eigenvalues' in result
    assert 'eigenvectors' not in result
    values = result['eigenvalues']
    rounded = sorted([round(v, 5) for v in values])
    assert rounded == sorted([round(3.0, 5), round(1.0, 5)])

def test_advanced_matrix_ops_returns_eigenvalues_and_eigenvectors_when_requested():
    A = [[2, 1], [1, 2]]
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    assert isinstance(result, dict)
    assert 'eigenvalues' in result
    assert 'eigenvectors' in result
    values = result['eigenvalues']
    vectors = result['eigenvectors']
    assert len(vectors) == len(values)
    for vec in vectors:
        assert vec[0] != 0

def test_invalid_compute_flag_returns_none():
    # Default flag is valid
    assert advanced_matrix_ops([[1]]) is not None
    # Invalid flag type
    assert advanced_matrix_ops([[1]], compute_eigenvectors='yes') is None

def test_non_square_matrix_returns_none():
    assert advanced_matrix_ops([[1, 2, 3], [4, 5, 6]]) is None

def test_matrix_with_non_numeric_entries_returns_none():
    assert advanced_matrix_ops([['a', 'b'], ['c', 'd']]) is None

def test_eig_exception_returns_none(monkeypatch):
    A = [[1, 2], [3, 4]]
    def fake_eig(arr):
        raise Exception("linalg.eig failure")
    def fake_eigvals(arr):
        raise Exception("linalg.eigvals failure")
    monkeypatch.setattr('unit_test.functions.np.linalg.eig', fake_eig)
    monkeypatch.setattr('unit_test.functions.np.linalg.eigvals', fake_eigvals)
    # Both default and compute_eigenvectors=True should return None on exception
    assert advanced_matrix_ops(A) is None
    assert advanced_matrix_ops(A, compute_eigenvectors=True) is None

def test_uses_matrix_operations(monkeypatch):
    A = [[1, 2], [3, 4]]
    call_count = {'count': 0}
    def fake_matops(a, b):
        call_count['count'] += 1
        return [[1, 0], [0, 1]]
    monkeypatch.setattr('unit_test.functions.matrix_operations', fake_matops)
    _ = advanced_matrix_ops(A)
    assert call_count['count'] == 1
    _ = advanced_matrix_ops(A, compute_eigenvectors=True)
    assert call_count['count'] == 2

def test_default_uses_eigvals(monkeypatch):
    A = [[1, 0], [0, 1]]
    call = {'count': 0}
    def fake_eigvals(arr):
        call['count'] += 1
        return np.array([2.0, 3.0])
    monkeypatch.setattr('unit_test.functions.np.linalg.eigvals', fake_eigvals)
    result = advanced_matrix_ops(A)
    assert call['count'] == 1
    assert sorted(result['eigenvalues']) == [2.0, 3.0]

def test_1x1_matrix_compute_eigenvectors():
    A = [[5]]
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    assert result['eigenvalues'] == [5.0]
    assert 'eigenvectors' in result
    vecs = result['eigenvectors']
    assert isinstance(vecs, list) and len(vecs) == 1
    assert vecs[0][0] != 0

def test_eigenvector_first_component_zero_flips_sign(monkeypatch):
    A = [[1, 0], [0, 1]]
    vals = np.array([1.0, 1.0])
    vecs = np.array([[0.0, 0.0], [1.0, 1.0]])  # columns with zero first component
    def fake_eig(arr):
        return vals, vecs
    monkeypatch.setattr('unit_test.functions.np.linalg.eig', fake_eig)
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    vectors = result['eigenvectors']
    for vec in vectors:
        assert abs(vec[0]) > 1e-6

def test_eigenvector_near_zero_first_component_adjusted(monkeypatch):
    A = [[1, 0], [0, 1]]
    vals = np.array([1.0, 2.0])
    # eigenvectors with near-zero first component
    vecs = np.array([[1e-9, 1e-10], [1.5, 2.5]])
    def fake_eig(arr):
        return vals, vecs
    monkeypatch.setattr('unit_test.functions.np.linalg.eig', fake_eig)
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    for vec in result['eigenvectors']:
        assert abs(vec[0]) > 1e-6

def test_eigenvector_just_above_threshold_not_adjusted(monkeypatch):
    A = [[1]]
    vals = np.array([1.0])
    vecs = np.array([[2e-6]])
    def fake_eig(arr):
        return vals, vecs
    monkeypatch.setattr('unit_test.functions.np.linalg.eig', fake_eig)
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    adjusted = result['eigenvectors'][0][0]
    assert abs(adjusted - 2e-6) < 1e-12

def test_eigenvector_at_threshold_adjusted(monkeypatch):
    A = [[1]]
    vals = np.array([1.0])
    vecs = np.array([[1e-6]])
    def fake_eig(arr):
        return vals, vecs
    monkeypatch.setattr('unit_test.functions.np.linalg.eig', fake_eig)
    result = advanced_matrix_ops(A, compute_eigenvectors=True)
    assert abs(result['eigenvectors'][0][0]) > 1e-6

if __name__ == "__main__":
    pytest.main([__file__])