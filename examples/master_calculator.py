"""A calculator grown from a "golden standard" DNA blueprint, with guaranteed robustness."""

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

def add_robust(a, b):
    """
    This function safely adds two numbers. It includes checks to ensure
    the inputs are valid numbers, embodying Justice and correctness.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a + b



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



def divide_simple(a, b):
    """
    Pure Power: Raw execution. Forcefully divides.
    """
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
    parser.add_argument('a', type=float, help="The first number.")
    parser.add_argument('operation', type=str, choices=['add', 'subtract', 'multiply', 'divide'], help="The operation to perform.")
    parser.add_argument('b', type=float, help="The second number.")
    args = parser.parse_args()
    ops = {'add': add_robust, 'subtract': subtract_robust, 'multiply': multiply_robust, 'divide': divide_simple, }
    try:
        result = ops[args.operation](args.a, args.b)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
