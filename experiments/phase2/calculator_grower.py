#!/usr/bin/env python3
"""
Calculator Grower - Helps the calculator learn and grow
"""

from simple_calculator import calculate


class CalculatorGrower:
    """Helps the calculator grow by learning from usage."""

    def __init__(self):
        self.usage_history = []
        self.new_operations = {}

    def use(self, operation: str, a: float, b: float) -> dict:
        """
        Use the calculator and track what's being used.
        Learn from patterns to suggest growth.
        """
        # Try to calculate
        try:
            result = calculate(operation, a, b)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)

        # Track usage
        self.usage_history.append({
            "operation": operation,
            "a": a,
            "b": b,
            "success": success,
        })

        # Learn from usage patterns
        self._learn_from_usage()

        return {
            "result": result,
            "success": success,
            "error": error,
            "suggestions": list(self.new_operations.keys()),
        }

    def _learn_from_usage(self):
        """Learn what new operations might be useful."""
        # Count operation usage
        op_counts = {}
        for use in self.usage_history:
            op = use["operation"]
            op_counts[op] = op_counts.get(op, 0) + 1

        # If multiply is used a lot, suggest power
        if op_counts.get("multiply", 0) > 2:
            if "power" not in self.new_operations:
                self.new_operations["power"] = self._make_power_operation()

        # If divide is used a lot, suggest modulo
        if op_counts.get("divide", 0) > 2:
            if "modulo" not in self.new_operations:
                self.new_operations["modulo"] = self._make_modulo_operation()

        # If we have lots of operations, suggest average
        if len(self.usage_history) > 5:
            if "average" not in self.new_operations:
                self.new_operations["average"] = self._make_average_operation()

    def _make_power_operation(self):
        """Create a new power operation."""
        def power(a: float, b: float) -> float:
            return a ** b
        return power

    def _make_modulo_operation(self):
        """Create a new modulo operation."""
        def modulo(a: float, b: float) -> float:
            return a % b
        return modulo

    def _make_average_operation(self):
        """Create a new average operation."""
        def average(a: float, b: float) -> float:
            return (a + b) / 2
        return average

    def grow(self):
        """
        Apply the learned operations to actually grow the calculator.
        Returns the code for the new operations.
        """
        if not self.new_operations:
            return "No new operations learned yet"

        code_additions = []
        for op_name, op_func in self.new_operations.items():
            code_additions.append(f"    elif operation == '{op_name}':")
            code_additions.append(f"        return {op_name}(a, b)")

        return "\n".join(code_additions)


if __name__ == "__main__":
    print("Calculator Grower - Proof of Concept")
    print("=" * 50)
    print()

    grower = CalculatorGrower()

    # Use the calculator - it learns from patterns
    print("Using multiply a bunch...")
    grower.use("multiply", 2, 3)
    grower.use("multiply", 4, 5)
    grower.use("multiply", 6, 7)

    print(f"Suggestions after multiply: {grower.new_operations.keys()}")
    print()

    print("Using divide a bunch...")
    grower.use("divide", 10, 2)
    grower.use("divide", 20, 4)
    grower.use("divide", 30, 5)

    print(f"Suggestions after divide: {grower.new_operations.keys()}")
    print()

    print("More operations to trigger average...")
    grower.use("add", 1, 2)
    grower.use("subtract", 5, 3)

    print(f"Final suggestions: {grower.new_operations.keys()}")
    print()

    # Show the growth
    print("Code to add to calculator:")
    print(grower.grow())
