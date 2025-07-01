import argparse

def addition(*args):
  """
  Returns the sum of all arguments.
  """
  return sum(args)

def subtraction(first, *rest):
  """
  Returns the result of subtracting all subsequent arguments from the first.
  """
  result = first
  for num in rest:
    result -= num
  return result





def multiplication(multiplicand, multiplier):
    """
    Returns the product of multiplicand and multiplier.
    """
    return multiplicand * multiplier


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a math function with two arguments")
    parser.add_argument("function_name", type=str, help="Name of the function to run (e.g., addition or subtraction)")
    parser.add_argument("args", type=str, help="Comma-separated arguments (e.g., 1,34)")

    args = parser.parse_args()
    func_name = args.function_name
    # Try to convert each argument to int first, if that fails use float
    arg_list = []
    for x in args.args.split(","):
      x = x.strip()
      try:
        arg_list.append(int(x))
      except ValueError:
        try:
          arg_list.append(float(x))
        except ValueError:
          raise ValueError(f"Cannot convert '{x}' to a number")

    try:
        # Dynamically call the function
        result = globals()[func_name](*arg_list)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


