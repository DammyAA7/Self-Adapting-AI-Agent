import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import functions
from functions import calculate_factorial_expression, calculate_factorial

def test_calculate_factorial_expression_single_term():
    assert calculate_factorial_expression("5!") == 120

def test_calculate_factorial_expression_multiple_terms():
    assert calculate_factorial_expression("2!+3!") == 8

def test_calculate_factorial_expression_zero_term():
    assert calculate_factorial_expression("0!") == 1

def test_calculate_factorial_expression_zero_and_nonzero_terms():
    assert calculate_factorial_expression("0!+4!+1!") == 26

def test_calculate_factorial_expression_repeated_terms():
    assert calculate_factorial_expression("4!+4!+4!") == 72

def test_calculate_factorial_expression_large_input():
    assert calculate_factorial_expression("10!") == 3628800

def test_calculate_factorial_expression_multiple_large_terms():
    assert calculate_factorial_expression("6!+7!") == 5760

def test_calculate_factorial_expression_whitespace_handling():
    assert calculate_factorial_expression(" 3! + 2! + 1! ") == 9

def test_calculate_factorial_expression_negative_operand():
    with pytest.raises(ValueError):
        calculate_factorial_expression("-1!+2!")

def test_calculate_factorial_expression_non_integer_operand():
    with pytest.raises(TypeError):
        calculate_factorial_expression("2.5!+3!")
    with pytest.raises(TypeError):
        calculate_factorial_expression("a!+3!")

def test_calculate_factorial_expression_invalid_format():
    with pytest.raises(ValueError):
        calculate_factorial_expression("2!!+3!")
    with pytest.raises(ValueError):
        calculate_factorial_expression("5+3!")

def test_calculate_factorial_expression_empty_string():
    with pytest.raises(ValueError):
        calculate_factorial_expression("")

def test_calculate_factorial_expression_only_plus():
    with pytest.raises(ValueError):
        calculate_factorial_expression("++")

def test_calculate_factorial_expression_integration_with_calculate_factorial():
    terms = ["1!", "3!", "5!"]
    expr = "+".join(terms)
    expected = sum(calculate_factorial(int(term[:-1])) for term in terms)
    assert calculate_factorial_expression(expr) == expected

def test_calculate_factorial_expression_uses_calculate_factorial(monkeypatch):
    calls = []
    def fake_factorial(n):
        calls.append(n)
        return n * 2
    monkeypatch.setattr(functions, 'calculate_factorial', fake_factorial)
    result = calculate_factorial_expression("1!+2!+3!")
    assert calls == [1, 2, 3]
    assert result == sum([n * 2 for n in [1, 2, 3]])

if __name__ == "__main__":
    pytest.main([__file__])