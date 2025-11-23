"""A calculator grown via Fractal Composition (LJPW)."""

import argparse
import sys

# --- Atomic Components (Fractal Building Blocks) ---


def validate_numeric(a, b):
    """
    Atomic Justice: Ensures inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")


def log_operation(func_name, a, b, result):
    """
    Atomic Love: Observes and records the operation.
    """
    print(f"[LOG] {func_name}({a}, {b}) = {result}")


# --- Component Gene Pool (Semantically Selected) ---


# Fractally Grown: secure_add
def secure_add(a, b):
    """
    Fractally composed function: secure_add
    Core: add_simple (Power)
    Guard: validate_numeric (Justice)
    Observer: log_operation (Love)
    """
    validate_numeric(a, b)
    result = a + b
    log_operation("secure_add", a, b, result)
    return result


def subtract_robust(a, b):
    """
    Safely subtracts two numbers, ensuring inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a - b


def multiply_robust(a, b):
    """
    Safely multiplies two numbers, ensuring inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a * b


def divide_robust(a, b):
    """
    This function safely divides two numbers. It validates the divisor
    to prevent a system crash from division by zero, embodying Justice.
    """
    if b == 0:
        raise ValueError("Error: Justice demands we cannot divide by zero.")
    return a / b


# --- Semantically Selected Main Block (guided by Master Gene Pool Archetypes) ---


def main():
    """
    A robust parser using argparse. It provides helpful user feedback,
    validation, and clear structure. It embodies high Wisdom (structure),
    high Justice (validation), and high Love (good UX).
    """
    import argparse

    parser = argparse.ArgumentParser(description="A robust command-line calculator.")
    parser.add_argument("a", type=float, help="The first number.")
    parser.add_argument(
        "operation",
        type=str,
        choices=["add", "subtract", "multiply", "divide"],
        help="The operation to perform.",
    )
    parser.add_argument("b", type=float, help="The second number.")
    args = parser.parse_args()
    ops = {
        "add": secure_add,
        "subtract": subtract_robust,
        "multiply": multiply_robust,
        "divide": divide_robust,
    }
    try:
        result = ops[args.operation](args.a, args.b)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
