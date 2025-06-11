import argparse

def addition(a, b):
  """
  Returns the sum of a and b.
  """
  return a + b


def subtraction(a, b):
  """
  Returns the result of subtracting b from a.
  """
  return a - b

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a math function with two arguments")
    parser.add_argument("function_name", type=str, help="Name of the function to run (e.g., addition or subtraction)")
    parser.add_argument("args", type=str, help="Comma-separated arguments (e.g., 1,34)")

    args = parser.parse_args()
    func_name = args.function_name
    arg_list = [int(x.strip()) for x in args.args.split(",")]

    try:
        # Dynamically call the function
        result = globals()[func_name](*arg_list)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
