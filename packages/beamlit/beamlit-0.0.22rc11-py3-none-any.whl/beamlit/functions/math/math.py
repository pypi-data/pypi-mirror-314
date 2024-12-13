import math as math_operation
import operator


def math(query: str):
    """A function for performing mathematical calculations.."""
    safe_dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "pow": math_operation.pow,
        "sqrt": math_operation.sqrt,
        "sin": math_operation.sin,
        "cos": math_operation.cos,
        "tan": math_operation.tan,
        "pi": math_operation.pi,
        "e": math_operation.e,
    }

    # Add basic arithmetic operators
    safe_dict.update(
        {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv,
            "**": operator.pow,
            "%": operator.mod,
        }
    )

    try:
        # Replace 'x' with '*'
        query = query.replace("x", "*")

        # Evaluate the expression in a restricted environment
        return eval(query, {"__builtins__": {}}, safe_dict)
    except Exception as e:
        raise ValueError(f"Invalid expression: {str(e)}")
