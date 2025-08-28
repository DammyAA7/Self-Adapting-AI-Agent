

import re
import math

def evaluate_factorial_expression(expression):
    """
    Evaluates expressions containing factorials and arithmetic operators.
    Returns the result or False for invalid expressions.
    """
    if not isinstance(expression, str):
        return False
    expr = expression.strip()
    if not expr:
        return False
    # Validate characters
    for ch in expr:
        if ch not in "0123456789+-*/! ":
            return False
    if "!!" in expr:
        return False
    # Replace factorials
    try:
        expr_replaced = re.sub(r'(\d+)!', lambda m: str(math.factorial(int(m.group(1)))), expr)
    except Exception:
        return False
    # Evaluate expression
    try:
        result = eval(expr_replaced)
    except ZeroDivisionError:
        return False
    except Exception:
        return False
    return result

