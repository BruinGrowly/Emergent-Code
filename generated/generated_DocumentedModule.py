"""
DocumentedModule - A generated calculator module

This module provides: SecureCalculator, SimpleCalculator, CalculatorValidator
"""


class SecureCalculator:
    """Calculator with validated operations and logging."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        """Validated addition with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a, b):
        """Validated subtraction with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result


class SimpleCalculator:
    """Basic calculator with direct operations."""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


class CalculatorValidator:
    """Validation utilities for calculator operations."""

    @staticmethod
    def validate_numeric(value):
        """Ensure value is numeric."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected numeric, got {type(value).__name__}")
        return True

    @staticmethod
    def validate_non_zero(value):
        """Ensure value is not zero."""
        if value == 0:
            raise ValueError("Value cannot be zero")
        return True


# Usage Examples
def example_usage():
    """Demonstrate module usage."""
    calc = SecureCalculator()
    result = calc.add(5, 3)
    print(f"Result: {result}")
