#!/usr/bin/env python3
"""
Emergent Calculator - Growing through use with love and attention

Intent: Make it genuinely useful
Attention: Design it carefully to enable emergence
Love: Integrate components so they amplify each other
"""

from typing import Dict, List, Any, Callable
from dataclasses import dataclass
import math


@dataclass
class Operation:
    """An operation the calculator can perform."""
    name: str
    func: Callable
    love: float      # How much it integrates
    justice: float   # How much it validates
    power: float     # How much it computes
    wisdom: float    # How much it learns


class EmergentCalculator:
    """
    A calculator that grows new operations through use.

    Designed with love and attention to enable emergence.
    """

    def __init__(self):
        # Start simple - basic operations
        self.operations = {
            "add": Operation("add", lambda a, b: a + b,
                           love=0.3, justice=0.0, power=0.5, wisdom=0.0),
            "subtract": Operation("subtract", lambda a, b: a - b,
                                love=0.3, justice=0.0, power=0.5, wisdom=0.0),
            "multiply": Operation("multiply", lambda a, b: a * b,
                                love=0.3, justice=0.0, power=0.5, wisdom=0.0),
            "divide": Operation("divide", self._safe_divide,
                              love=0.3, justice=0.5, power=0.5, wisdom=0.0),
        }

        # Track usage - this enables learning
        self.usage_history = []
        self.value_history = []

        # Track what operations work together (integration!)
        self.operation_pairs = {}

        # Track what values are common (pattern recognition!)
        self.common_values = {}

    def _safe_divide(self, a: float, b: float) -> float:
        """Divide with validation - shows Justice."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def calculate(self, operation: str, a: float, b: float) -> Dict[str, Any]:
        """
        Calculate with learning.

        Every calculation teaches the system about usage patterns.
        This is Love - connecting usage to growth.
        """
        # Validate inputs (Justice)
        if operation not in self.operations:
            return {
                "error": f"Unknown operation: {operation}",
                "suggestions": self._suggest_operations(operation)
            }

        # Execute (Power)
        try:
            op = self.operations[operation]
            result = op.func(a, b)
            success = True
            error = None
        except Exception as e:
            result = None
            success = False
            error = str(e)

        # Learn from usage (Wisdom)
        if success:
            self._learn_from_usage(operation, a, b, result)

        return {
            "result": result,
            "success": success,
            "error": error,
            "operation_ljpw": {
                "love": op.love,
                "justice": op.justice,
                "power": op.power,
                "wisdom": op.wisdom,
            },
            "new_operations_available": self._check_for_emergence()
        }

    def _learn_from_usage(self, operation: str, a: float, b: float, result: float):
        """Learn patterns from usage - this is Wisdom."""
        # Track this calculation
        self.usage_history.append({
            "operation": operation,
            "a": a,
            "b": b,
            "result": result,
        })

        # Track values used
        for val in [a, b, result]:
            self.common_values[val] = self.common_values.get(val, 0) + 1

        # Track operation pairs (what comes after what)
        if len(self.usage_history) > 1:
            prev_op = self.usage_history[-2]["operation"]
            pair = (prev_op, operation)
            self.operation_pairs[pair] = self.operation_pairs.get(pair, 0) + 1

    def _suggest_operations(self, attempted: str) -> List[str]:
        """Suggest similar operations - this is Love (helping the user)."""
        suggestions = []

        # Find operations with similar names
        for op_name in self.operations.keys():
            if attempted.lower() in op_name or op_name in attempted.lower():
                suggestions.append(op_name)

        return suggestions if suggestions else list(self.operations.keys())[:3]

    def _check_for_emergence(self) -> List[str]:
        """
        Check if conditions are right for new operations to emerge.

        This is where Love (integration) + Wisdom (patterns) create emergence!
        """
        new_ops = []

        # Pattern 1: Multiply used often → suggest power
        multiply_count = sum(1 for h in self.usage_history if h["operation"] == "multiply")
        if multiply_count >= 3 and "power" not in self.operations:
            new_ops.append("power")

        # Pattern 2: Divide used often → suggest modulo
        divide_count = sum(1 for h in self.usage_history if h["operation"] == "divide")
        if divide_count >= 3 and "modulo" not in self.operations:
            new_ops.append("modulo")

        # Pattern 3: Many calculations → suggest average
        if len(self.usage_history) >= 6 and "average" not in self.operations:
            new_ops.append("average")

        # Pattern 4: Same value used multiple times → suggest square
        repeated_values = [v for v, count in self.common_values.items() if count >= 3]
        if repeated_values and "square" not in self.operations:
            new_ops.append("square")

        # Pattern 5: Operations often paired → suggest combo operation
        if self.operation_pairs:
            most_common_pair = max(self.operation_pairs.items(), key=lambda x: x[1])
            if most_common_pair[1] >= 2:
                pair_name = f"{most_common_pair[0][0]}_then_{most_common_pair[0][1]}"
                if pair_name not in self.operations and len(new_ops) < 3:
                    new_ops.append(pair_name)

        return new_ops

    def grow(self, operation_name: str) -> bool:
        # Auto-healed: Input validation for grow
        if operation_name is not None and not isinstance(operation_name, str):
            raise TypeError(f'operation_name must be str, got {type(operation_name).__name__}')
        """
        Grow by adding a new operation.

        This is emergence - the system creating new capabilities!
        Returns True if growth happened.
        """
        if operation_name in self.operations:
            return False

        # Create new operations based on learned patterns
        # Each new operation has higher Love (more integration!)

        if operation_name == "power":
            self.operations["power"] = Operation(
                "power",
                lambda a, b: a ** b,
                love=0.5,      # Higher love - integrates multiply concept
                justice=0.3,   # Some validation
                power=0.7,     # More powerful
                wisdom=0.3     # Learned from usage
            )
            return True

        elif operation_name == "modulo":
            self.operations["modulo"] = Operation(
                "modulo",
                lambda a, b: a % b if b != 0 else 0,
                love=0.5,      # Integrates divide concept
                justice=0.4,   # Handles edge cases
                power=0.6,
                wisdom=0.3
            )
            return True

        elif operation_name == "average":
            self.operations["average"] = Operation(
                "average",
                lambda a, b: (a + b) / 2,
                love=0.7,      # HIGH LOVE - integrates add + divide!
                justice=0.3,
                power=0.5,
                wisdom=0.4     # Learned from many calculations
            )
            return True

        elif operation_name == "square":
            self.operations["square"] = Operation(
                "square",
                lambda a, b: a * a,  # b is ignored
                love=0.6,      # Integrates multiply concept
                justice=0.2,
                power=0.7,
                wisdom=0.5     # Learned from repeated values
            )
            return True

        # Combo operations - HIGH LOVE (integration of two operations!)
        elif "_then_" in operation_name:
            parts = operation_name.split("_then_")
            if len(parts) == 2 and all(p in self.operations for p in parts):
                first_op = self.operations[parts[0]]
                second_op = self.operations[parts[1]]

                def combo_func(a, b):
                    intermediate = first_op.func(a, b)
                    return second_op.func(intermediate, b)

                # Combo operations have VERY HIGH LOVE (integration!)
                self.operations[operation_name] = Operation(
                    operation_name,
                    combo_func,
                    love=0.8,      # VERY HIGH - integrates two operations!
                    justice=max(first_op.justice, second_op.justice),
                    power=(first_op.power + second_op.power) / 2,
                    wisdom=0.6     # Learned from usage patterns
                )
                return True

        return False

    def system_ljpw(self) -> Dict[str, float]:
        """
        Calculate LJPW for the entire calculator system.

        This is where we see emergence at scale!
        """
        if not self.operations:
            return {"love": 0, "justice": 0, "power": 0, "wisdom": 0, "harmony": 0}

        # Average across all operations
        avg_love = sum(op.love for op in self.operations.values()) / len(self.operations)
        avg_justice = sum(op.justice for op in self.operations.values()) / len(self.operations)
        avg_power = sum(op.power for op in self.operations.values()) / len(self.operations)
        avg_wisdom = sum(op.wisdom for op in self.operations.values()) / len(self.operations)

        # Integration bonus - more operations = more integration!
        integration_bonus = min(len(self.operations) / 10, 0.3)

        # Learning bonus - more history = more wisdom!
        learning_bonus = min(len(self.usage_history) / 20, 0.2)

        # Apply bonuses
        love = min(1.0, avg_love + integration_bonus)
        justice = avg_justice
        power = avg_power
        wisdom = min(1.0, avg_wisdom + learning_bonus)

        # Calculate harmony
        harmony = (love * justice * power * wisdom) ** 0.25 if all([love, justice, power, wisdom]) else 0

        return {
            "love": round(love, 3),
            "justice": round(justice, 3),
            "power": round(power, 3),
            "wisdom": round(wisdom, 3),
            "harmony": round(harmony, 3),
            "intent": round(love + wisdom, 3),
            "operations_count": len(self.operations),
            "usage_count": len(self.usage_history),
        }


def demonstrate_emergence():
    """Demonstrate the calculator growing through use."""
    print("=" * 70)
    print("EMERGENT CALCULATOR - Growth Through Use")
    print("=" * 70)
    print()

    calc = EmergentCalculator()

    print("Starting state:")
    ljpw = calc.system_ljpw()
    print(f"  Operations: {ljpw['operations_count']}")
    print(f"  LJPW: L={ljpw['love']:.3f}, J={ljpw['justice']:.3f}, "
          f"P={ljpw['power']:.3f}, W={ljpw['wisdom']:.3f}")
    print(f"  Harmony: {ljpw['harmony']:.3f}")
    print()

    # Use it - watch it learn
    print("Phase 1: Basic usage")
    print("-" * 70)

    results = [
        calc.calculate("add", 2, 3),
        calc.calculate("multiply", 4, 5),
        calc.calculate("multiply", 6, 7),
        calc.calculate("multiply", 8, 9),  # 3rd multiply triggers power
    ]

    ljpw = calc.system_ljpw()
    print(f"After 4 calculations:")
    print(f"  LJPW: L={ljpw['love']:.3f}, W={ljpw['wisdom']:.3f}, H={ljpw['harmony']:.3f}")
    print(f"  New operations suggested: {results[-1]['new_operations_available']}")
    print()

    # Grow!
    print("Phase 2: Growing new operations")
    print("-" * 70)

    for new_op in results[-1]['new_operations_available']:
        grew = calc.grow(new_op)
        print(f"  Added '{new_op}': {grew}")

    ljpw = calc.system_ljpw()
    print(f"\nAfter growth:")
    print(f"  Operations: {ljpw['operations_count']}")
    print(f"  LJPW: L={ljpw['love']:.3f}, J={ljpw['justice']:.3f}, "
          f"P={ljpw['power']:.3f}, W={ljpw['wisdom']:.3f}")
    print(f"  Harmony: {ljpw['harmony']:.3f}")
    print()

    # Keep using - trigger more emergence
    print("Phase 3: Continued use")
    print("-" * 70)

    more_results = [
        calc.calculate("divide", 10, 2),
        calc.calculate("divide", 20, 4),
        calc.calculate("divide", 30, 5),  # 3rd divide
        calc.calculate("add", 1, 1),
        calc.calculate("subtract", 5, 3),
        calc.calculate("power", 2, 3),  # Using new operation!
    ]

    ljpw = calc.system_ljpw()
    new_ops = more_results[-1].get('new_operations_available', [])
    print(f"After more use:")
    print(f"  Usage count: {ljpw['usage_count']}")
    print(f"  LJPW: L={ljpw['love']:.3f}, W={ljpw['wisdom']:.3f}, H={ljpw['harmony']:.3f}")
    print(f"  New operations available: {new_ops}")
    print()

    # Grow again!
    print("Phase 4: Second growth")
    print("-" * 70)

    for new_op in new_ops:
        grew = calc.grow(new_op)
        if grew:
            print(f"  Added '{new_op}'")
            # Show the LJPW of the new operation
            if new_op in calc.operations:
                op = calc.operations[new_op]
                print(f"    LJPW: L={op.love:.2f}, J={op.justice:.2f}, "
                      f"P={op.power:.2f}, W={op.wisdom:.2f}")

    ljpw = calc.system_ljpw()
    print(f"\nFinal state:")
    print(f"  Operations: {ljpw['operations_count']}")
    print(f"  LJPW: L={ljpw['love']:.3f}, J={ljpw['justice']:.3f}, "
          f"P={ljpw['power']:.3f}, W={ljpw['wisdom']:.3f}")
    print(f"  Harmony: {ljpw['harmony']:.3f}")
    print(f"  Intent: {ljpw['intent']:.3f}")
    print()

    if ljpw['love'] > 0.7:
        print("✨ LOVE > 0.7! Autopoietic Love threshold reached!")
    if ljpw['harmony'] > 0.6:
        print("✨ HARMONY > 0.6! System is AUTOPOIETIC!")

    if ljpw['love'] > 0.7 or ljpw['harmony'] > 0.5:
        print("\n🌟 EMERGENCE DETECTED!")
        print("The calculator has grown beyond its initial design.")
        print("Through use and learning, it developed new capabilities.")
        print("This is autopoiesis in action! 🌱")

    print()
    print("=" * 70)
    print(f"Growth: {4} → {ljpw['operations_count']} operations")
    print(f"Love increased as operations integrated")
    print(f"Wisdom increased through learning from {ljpw['usage_count']} uses")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_emergence()
