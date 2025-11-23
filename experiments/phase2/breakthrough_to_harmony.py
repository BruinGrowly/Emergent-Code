#!/usr/bin/env python3
"""
Breakthrough to Harmony - Can we reach H > 0.6?

We have Love (0.778). Now we need Harmony through balance.
Add operations with high Justice and create mega-combinations.
"""

from emergent_calculator import EmergentCalculator, Operation


class BalancedCalculator(EmergentCalculator):
    """Extended calculator with balanced, validation-heavy operations."""

    def __init__(self):
        super().__init__()

        # Add balanced validation operations right away
        self._add_validation_operations()
        self._add_mega_combo_operations()

    def _add_validation_operations(self):
        """Add operations with HIGH Justice (validation)."""

        # Safe operations with lots of validation
        self.operations["safe_add"] = Operation(
            "safe_add",
            lambda a, b: a + b if self._validate_number(a) and self._validate_number(b) else 0,
            love=0.4,      # Some integration
            justice=0.8,   # HIGH validation!
            power=0.5,
            wisdom=0.4
        )

        self.operations["safe_multiply"] = Operation(
            "safe_multiply",
            lambda a, b: a * b if abs(a) < 1000 and abs(b) < 1000 else 0,
            love=0.4,
            justice=0.8,   # HIGH validation!
            power=0.6,
            wisdom=0.4
        )

        self.operations["validated_divide"] = Operation(
            "validated_divide",
            lambda a, b: a / b if b != 0 and abs(b) > 0.001 else 0,
            love=0.5,      # Integrates divide concept
            justice=0.9,   # VERY HIGH validation!
            power=0.5,
            wisdom=0.5
        )

    def _add_mega_combo_operations(self):
        """Add operations that integrate 3+ operations - MAXIMUM Love!"""

        # Mega combo: add → multiply → divide
        def compute_average_of_products(a, b):
            """Combines add, multiply, divide - 3 operations!"""
            product1 = a * a
            product2 = b * b
            total = product1 + product2
            return total / 2

        self.operations["average_of_squares"] = Operation(
            "average_of_squares",
            compute_average_of_products,
            love=0.9,      # MAXIMUM Love - integrates 3 operations!
            justice=0.5,
            power=0.7,
            wisdom=0.6
        )

        # Another mega combo with validation
        def safe_geometric_mean(a, b):
            """Combines multiply, power, validation - high integration + high justice!"""
            if a <= 0 or b <= 0:
                return 0
            product = a * b
            return product ** 0.5

        self.operations["geometric_mean"] = Operation(
            "geometric_mean",
            safe_geometric_mean,
            love=0.8,      # High Love - integrates multiple concepts
            justice=0.7,   # High Justice - validates inputs
            power=0.7,
            wisdom=0.6
        )

    def _validate_number(self, n):
        """Helper for validation."""
        return isinstance(n, (int, float)) and not (n != n) and abs(n) < 1e10


def push_to_harmony():
    """Push for H > 0.6 with balanced operations."""
    print("=" * 70)
    print("BREAKTHROUGH TO HARMONY - Pushing for H > 0.6")
    print("=" * 70)
    print()

    calc = BalancedCalculator()

    # Initial state with balanced operations
    ljpw = calc.system_ljpw()
    print("Starting with balanced operations:")
    print(f"  Operations: {ljpw['operations_count']}")
    print(f"  LJPW: L={ljpw['love']:.3f}, J={ljpw['justice']:.3f}, "
          f"P={ljpw['power']:.3f}, W={ljpw['wisdom']:.3f}")
    print(f"  Harmony: {ljpw['harmony']:.3f}")
    print(f"  Intent: {ljpw['intent']:.3f}")
    print()

    if ljpw['love'] > 0.7:
        print("✨ Love > 0.7!")
    if ljpw['harmony'] > 0.6:
        print("✨✨ HARMONY > 0.6! FULL AUTOPOIESIS!")
    elif ljpw['harmony'] > 0.5:
        print("✓ Harmony > 0.5 (homeostatic)")

    print()

    # Now use it to trigger more growth
    print("Using the calculator to trigger emergence...")
    print()

    # Use operations that will trigger new growth
    test_operations = [
        ("safe_add", 5, 3),
        ("safe_multiply", 4, 6),
        ("validated_divide", 10, 2),
        ("average_of_squares", 3, 4),
        ("geometric_mean", 9, 16),
        ("multiply", 2, 3),
        ("multiply", 4, 5),
        ("multiply", 6, 7),  # Trigger power
    ]

    for i, (op, a, b) in enumerate(test_operations):
        result = calc.calculate(op, a, b)

        if result.get('new_operations_available'):
            new_ops = result['new_operations_available']
            print(f"  Iteration {i}: Emerged {new_ops}")

            for new_op in new_ops:
                if calc.grow(new_op):
                    ljpw = calc.system_ljpw()
                    print(f"    Added '{new_op}': L={ljpw['love']:.3f}, H={ljpw['harmony']:.3f}")

    # Final state
    print()
    print("=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    final = calc.system_ljpw()
    print(f"Operations: {final['operations_count']}")
    print(f"Usage: {final['usage_count']}")
    print()
    print("LJPW Profile:")
    print(f"  Love:    {final['love']:.3f}")
    print(f"  Justice: {final['justice']:.3f}")
    print(f"  Power:   {final['power']:.3f}")
    print(f"  Wisdom:  {final['wisdom']:.3f}")
    print()
    print(f"Harmony: {final['harmony']:.3f}")
    print(f"Intent:  {final['intent']:.3f}")
    print()

    # Check thresholds
    if final['love'] > 0.7 and final['harmony'] > 0.6:
        print("✨✨✨ FULL AUTOPOIESIS ACHIEVED! ✨✨✨")
        print()
        print("Both thresholds exceeded:")
        print(f"  Love = {final['love']:.3f} > 0.7 ✓")
        print(f"  Harmony = {final['harmony']:.3f} > 0.6 ✓")
        print()
        amp = 1.0 + 0.5 * (final['love'] - 0.7)
        print(f"Amplification factor: {amp:.3f}x")
        print()
        print("This system is self-sustaining and exponentially growing!")
        print("Autopoiesis achieved through Love + Balance! 💛⚖️")
    elif final['love'] > 0.7:
        print("✨ AUTOPOIETIC LOVE ACHIEVED!")
        print()
        print(f"Love = {final['love']:.3f} > 0.7 ✓")
        print(f"Harmony = {final['harmony']:.3f}")
        gap = 0.6 - final['harmony']
        print(f"Need +{gap:.3f} more Harmony for full autopoiesis")
        print()
        print(f"Bottleneck: {min_dimension(final)}")
    else:
        print("Progress:")
        print(f"  Love: {final['love']/0.7*100:.1f}% to threshold")
        print(f"  Harmony: {final['harmony']/0.6*100:.1f}% to threshold")

    print()

    # Analyze which operations are most balanced
    print("=" * 70)
    print("MOST BALANCED OPERATIONS")
    print("=" * 70)

    ops_by_harmony = []
    for name, op in calc.operations.items():
        h = (op.love * op.justice * op.power * op.wisdom) ** 0.25 if all([op.love, op.justice, op.power, op.wisdom]) else 0
        ops_by_harmony.append((name, op, h))

    ops_by_harmony.sort(key=lambda x: x[2], reverse=True)

    print()
    for i, (name, op, h) in enumerate(ops_by_harmony[:10], 1):
        print(f"{i:2d}. {name:25s} H={h:.3f} "
              f"(L={op.love:.2f}, J={op.justice:.2f}, P={op.power:.2f}, W={op.wisdom:.2f})")

    print()
    print("Notice: Operations with ALL dimensions present have highest H!")
    print("Balance is key to Harmony. Love is key to growth.")
    print("Together: Autopoiesis! 🌟")


def min_dimension(ljpw):
    """Find which dimension is lowest."""
    dims = [
        ("Love", ljpw['love']),
        ("Justice", ljpw['justice']),
        ("Power", ljpw['power']),
        ("Wisdom", ljpw['wisdom']),
    ]
    min_dim = min(dims, key=lambda x: x[1])
    return f"{min_dim[0]} is lowest at {min_dim[1]:.3f}"


if __name__ == "__main__":
    push_to_harmony()
