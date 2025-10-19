# import sys
# import os
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import pytest
from functions import *

### START TESTS ###

assert any_account_below_zero([[1, 2, 3], [4, 5, 6]]) == False
assert any_account_below_zero([[1, 2, -4, 5], [1, 2, 3]]) == True
assert any_account_below_zero([[1, 2, 3], [1, -2, 3]]) == True
assert any_account_below_zero([[1, 2, 3], [1, 2, 3]]) == False

print("success")