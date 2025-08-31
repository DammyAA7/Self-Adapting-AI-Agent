from enum import Enum

class Status(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


import math

def solve_ode_runge_kutta(f, x0, y0, x_end, step):
    """
    Numerically solves a first-order ordinary differential equation dy/dx = f(x, y)
    over the interval [x0, x_end] using the classic 4th-order Runge–Kutta method.

    Parameters:
        f (callable): Function f(x, y) that returns dy/dx.
        x0 (float): Initial value of the independent variable x.
        y0 (float): Initial value of the dependent variable y at x = x0.
        x_end (float): Final value of x where the solution should stop.
        step (float): Integration step size (Δx).

    Returns:
        tuple: A pair (xs, ys) where xs is a list of x values from x0 to x_end (inclusive)
               and ys is the corresponding list of y values.
    """
    if not callable(f):
        raise TypeError("f must be a callable function of (x, y)")
    try:
        x0 = float(x0)
        y0 = float(y0)
        x_end = float(x_end)
        step = float(step)
    except (TypeError, ValueError):
        raise TypeError("x0, y0, x_end, and step must be numeric")
    if step <= 0:
        raise ValueError("step size must be positive")
    if x_end < x0:
        raise ValueError("x_end must be greater than or equal to x0")

    xs = [x0]
    ys = [y0]
    x = x0
    y = y0

    # Integrate until reaching x_end
    while x < x_end:
        h = step if x + step <= x_end else (x_end - x)
        k1 = f(x, y)
        k2 = f(x + h / 2.0, y + h * k1 / 2.0)
        k3 = f(x + h / 2.0, y + h * k2 / 2.0)
        k4 = f(x + h,         y + h * k3)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        x = x + h
        xs.append(x)
        ys.append(y)

    return xs, ys
