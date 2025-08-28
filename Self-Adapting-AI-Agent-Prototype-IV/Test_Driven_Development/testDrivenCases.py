import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from Unit_Test.functions import *
from functions import *

def test_evaluate_factorial_expression_simple_addition():
    result = evaluate_factorial_expression("2!+3!")
    assert result == 8  # 2 + 6

def test_evaluate_factorial_expression_single_factorial():
    result = evaluate_factorial_expression("5!")
    assert result == 120

def test_evaluate_factorial_expression_multiplication_and_subtraction():
    result = evaluate_factorial_expression("4!*2-3!")
    assert result == 42  # 24*2 - 6

def test_evaluate_factorial_expression_division():
    result = evaluate_factorial_expression("6!/720")
    assert result == 1  # 720/720

def test_evaluate_factorial_expression_zero_factorial_and_addition():
    result = evaluate_factorial_expression("0!+1!")
    assert result == 2  # 1 + 1

def test_evaluate_factorial_expression_complex_expression():
    result = evaluate_factorial_expression("3!+4!*2/8-5!")
    # 3! = 6, 4!*2 = 48, 48/8 = 6, 6+6 = 12, 12-120 = -108
    assert result == -108

def test_evaluate_factorial_expression_with_spaces():
    result = evaluate_factorial_expression(" 2! + 3! ")
    assert result == 8

def test_evaluate_factorial_expression_large_factorial():
    # 20! = 2432902008176640000
    result = evaluate_factorial_expression("20!")
    assert result == 2432902008176640000

def test_evaluate_factorial_expression_division_by_zero_handling():
    result = evaluate_factorial_expression("3!/0")
    assert result == False  # Should handle division by zero gracefully

def test_evaluate_factorial_expression_invalid_double_factorial():
    result = evaluate_factorial_expression("3!!")
    assert result == False  # Double factorial not supported

def test_evaluate_factorial_expression_invalid_chars():
    result = evaluate_factorial_expression("abc")
    assert result == False

def test_evaluate_factorial_expression_malformed_expression():
    result = evaluate_factorial_expression("!2")
    assert result == False

def test_evaluate_factorial_expression_empty_string():
    result = evaluate_factorial_expression("")
    assert result == False

def test_evaluate_factorial_expression_whitespace_only():
    result = evaluate_factorial_expression("    ")
    assert result == False

def test_evaluate_factorial_expression_wrong_type_input():
    result = evaluate_factorial_expression(None)
    assert result == False

def test_evaluate_factorial_expression_invalid_parentheses():
    result = evaluate_factorial_expression("(3!+2!)")
    assert result == False  # Parentheses not allowed

def test_evaluate_factorial_expression_invalid_operator_sequence():
    result = evaluate_factorial_expression("2!+*3!")
    assert result == False  # Invalid operator sequence

def test_evaluate_factorial_expression_fractional_factorial():
    result = evaluate_factorial_expression("3.5!")
    assert result == False  # Fractional factorial not supported

def test_evaluate_factorial_expression_trailing_operator():
    result = evaluate_factorial_expression("5!+")
    assert result == False  # Trailing operator invalid

def test_evaluate_factorial_expression_leading_plus_operator():
    result = evaluate_factorial_expression("+3!")
    assert result == 6  # +6 yields 6

def test_evaluate_factorial_expression_leading_minus_operator():
    result = evaluate_factorial_expression("-3!")
    assert result == -6  # -6 yields -6

def test_evaluate_factorial_expression_only_operator():
    result = evaluate_factorial_expression("+")
    assert result == False  # Single operator invalid

def test_evaluate_factorial_expression_multiple_factorials_sum():
    result = evaluate_factorial_expression("2!+3!+4!")
    assert result == 32  # 2 + 6 + 24

def test_evaluate_factorial_expression_multiplication_no_spaces():
    result = evaluate_factorial_expression("2!*3!")
    assert result == 12  # 2 * 6

def test_evaluate_factorial_expression_non_integer_division():
    result = evaluate_factorial_expression("3!/4")
    assert result == 1.5  # 6/4 yields 1.5


if __name__ == "__main__":
    pytest.main([__file__])