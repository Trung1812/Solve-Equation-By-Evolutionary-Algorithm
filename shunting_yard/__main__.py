from typing import Optional
import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from shunting_yard.rpn import compute_rpn, FunctionDictionary, Number, WrongExpressionError
from shunting_yard.shunting_yard import MismatchedBracketsError, shunting_yard
from shunting_yard.tokenize import tokenize


def compute(expression: str, case_sensitive: bool = True, additional_functions: Optional[FunctionDictionary] = None) -> Number:
    """Compute the value of a mathematical expression. Equivalent to compute_rpn(shunting_yard(expression), additional_functions).
    Check the docstring of these functions for more details.

    Args:
        string (str): string containing the mathematical expression to compute.
        case_sensitive (bool): indicates whether the expression should care about case.

    Returns:
        Number: Result.
    """
    return compute_rpn(shunting_yard(expression, case_sensitive), additional_functions)

# Define the equation you want to solve
eq = input("Enter the equation you want to solve: ")
print(shunting_yard(eq, variable='x'))
print(compute_rpn(shunting_yard(eq).replace('x', '1')))