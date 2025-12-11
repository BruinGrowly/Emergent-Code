#!/usr/bin/env python3
"""
Simple Calculator - Just does math
"""

def calculate(operation: str, a: float, b: float) -> float:
    """Do basic math operations."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Can't divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")


if __name__ == "__main__":
    print("Simple Calculator")
    print(f"2 + 3 = {calculate('add', 2, 3)}")
    print(f"10 - 4 = {calculate('subtract', 10, 4)}")
    print(f"5 * 6 = {calculate('multiply', 5, 6)}")
    print(f"20 / 4 = {calculate('divide', 20, 4)}")
