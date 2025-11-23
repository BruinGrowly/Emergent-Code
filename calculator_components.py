"""
SPDX-License-Identifier: MIT
Calculator Components - The "Gene Pool"

This module provides a variety of component implementations for building a
calculator. Each component has a distinct semantic profile (LJPW) and is
designed to be analyzed and selected by an ICE-based growth engine.
"""

from typing import Union

Number = Union[int, float]


class CalculatorError(Exception):
    """Base exception for calculator operations."""

    pass


class DivisionByZeroError(CalculatorError):
    """Exception raised when attempting to divide by zero."""

    pass


class InvalidInputError(CalculatorError):
    """Exception raised when inputs are not numeric."""

    pass


# --- Functional Components: Arithmetic ---


def add_simple(a: Number, b: Number) -> Number:
    """Pure Power: A direct, unchecked operation."""
    return a + b


def add_robust(a: Number, b: Number) -> Number:
    """
    This function safely adds two numbers. It includes checks to ensure
    the inputs are valid numbers, embodying Justice and correctness.

    Raises:
        InvalidInputError: If inputs are not numeric
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise InvalidInputError("Both inputs must be numeric")
    return a + b


def subtract_simple(a: Number, b: Number) -> Number:
    """Pure Power: A direct, unchecked operation."""
    return a - b


def multiply_simple(a: Number, b: Number) -> Number:
    """Pure Power: A direct, unchecked operation."""
    return a * b


def divide_robust(a: Number, b: Number) -> Number:
    """
    This function safely divides two numbers. It validates the divisor
    to prevent a system crash from division by zero, embodying Justice.

    Raises:
        DivisionByZeroError: If attempting to divide by zero
    """
    if b == 0:
        raise DivisionByZeroError("Justice demands we cannot divide by zero.")
    return a / b


def subtract_robust(a: Number, b: Number) -> Number:
    """
    Safely subtracts two numbers, ensuring inputs are numeric.

    Raises:
        InvalidInputError: If inputs are not numeric
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise InvalidInputError("Both inputs must be numeric")
    return a - b


def multiply_robust(a: Number, b: Number) -> Number:
    """
    Safely multiplies two numbers, ensuring inputs are numeric.

    Raises:
        InvalidInputError: If inputs are not numeric
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise InvalidInputError("Both inputs must be numeric")
    return a * b


def divide_simple(a: Number, b: Number) -> Number:
    """Pure Power: Direct division, risks ZeroDivisionError."""
    return a / b


# --- Structural Components: Main Execution Logic ---


def main_parser_simple() -> None:
    """
    A very simple parser using sys.argv. It has high Power due to its
    directness but low Love (bad UX) and low Justice (no validation).
    """
    import sys

    # Expects format: python <script> <a> <op> <b>
    a = float(sys.argv[1])
    op_str = sys.argv[2]
    b = float(sys.argv[3])

    ops = {
        "add": add_simple,
        "subtract": subtract_simple,
        "multiply": multiply_simple,
        "divide": divide_robust,
    }

    result = ops[op_str](a, b)
    print(f"Result: {result}")


def main_parser_robust() -> None:
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

    # Note: This main block intelligently selects the most robust functions available
    ops = {
        "add": add_robust,
        "subtract": subtract_simple,
        "multiply": multiply_simple,
        "divide": divide_robust,
    }
    result = ops[args.operation](args.a, args.b)
    print(f"Result: {result}")


# ==============================================================================
# Atomic Components (Fractal Building Blocks)
# ==============================================================================


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


# ==============================================================================
#  SOURCE CODE DICTIONARY FOR LJPW ANALYSIS
# ==============================================================================

# We need the source code as strings for the harmonizer to analyze
SOURCES = {
    "functions": {
        "validate_numeric": '''
def validate_numeric(a, b):
    """
    Atomic Justice: Ensures inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
''',
        "log_operation": '''
def log_operation(func_name, a, b, result):
    """
    Atomic Love: Observes and records the operation.
    """
    print(f"[LOG] {func_name}({a}, {b}) = {result}")
''',
        "add_simple": """
def add_simple(a, b):
    # Pure Power: A direct, raw execution. Forcefully adds.
    return a + b
""",
        "add_robust": '''
def add_robust(a, b):
    """
    This function safely adds two numbers. It includes checks to ensure
    the inputs are valid numbers, embodying Justice and correctness.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a + b
''',
        "subtract_simple": """
def subtract_simple(a, b):
    # Pure Power: Raw execution. Forcefully subtracts.
    return a - b
""",
        "multiply_simple": """
def multiply_simple(a, b):
    # Pure Power: Raw execution. Forcefully multiplies.
    return a * b
""",
        "divide_robust": '''
def divide_robust(a, b):
    """
    This function safely divides two numbers. It validates the divisor
    to prevent a system crash from division by zero, embodying Justice.
    """
    if b == 0:
        raise ValueError("Error: Justice demands we cannot divide by zero.")
    return a / b
''',
        "subtract_robust": '''
def subtract_robust(a, b):
    """
    Safely subtracts two numbers, ensuring inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a - b
''',
        "multiply_robust": '''
def multiply_robust(a, b):
    """
    Safely multiplies two numbers, ensuring inputs are numeric.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numeric")
    return a * b
''',
        "divide_simple": '''
def divide_simple(a, b):
    """
    Pure Power: Raw execution. Forcefully divides.
    """
    return a / b
''',
    },
    "main_blocks": {
        "main_parser_simple": '''
def main_simple():
    """
    A very simple parser using sys.argv. It has high Power due to its
    directness but low Love (bad UX) and low Justice (no validation).
    """
    import sys
    a = float(sys.argv[1])
    op_str = sys.argv[2]
    b = float(sys.argv[3])
    ops = {'add': add_simple, 'subtract': subtract_simple, 'multiply': multiply_simple, 'divide': divide_robust}
    result = ops[op_str](a, b)
    print(f"Result: {result}")
''',
        "main_parser_robust": '''
def main_robust():
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
    ops = {'add': add_robust, 'subtract': subtract_simple, 'multiply': multiply_simple, 'divide': divide_robust}
    try:
        result = ops[args.operation](args.a, args.b)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
''',
    },
}
