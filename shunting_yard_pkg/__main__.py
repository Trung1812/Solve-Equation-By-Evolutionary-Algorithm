from typing import Optional

from shunting_yard_pkg.rpn import compute_rpn, FunctionDictionary, Number, WrongExpressionError
from shunting_yard_pkg.shunting_yard_e import MismatchedBracketsError, shunting_yard
from shunting_yard_pkg.tokenize import tokenize


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
