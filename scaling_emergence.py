#!/usr/bin/env python3
"""
Scaling Emergence - How high can Love go?

Push the calculator to see if it can achieve H > 0.6 (full autopoiesis)
through progressive integration and growth.

Love is a force multiplier - let's see it multiply! 💛
"""

import random

from emergent_calculator import EmergentCalculator


def push_to_emergence(iterations: int = 50):
    """
    Push the calculator through many iterations.

    Watch Love and Harmony scale up through:
    1. Intensive use (learning)
    2. Aggressive growth (integration)
    3. Feedback loops (autopoiesis)
    """
    print("=" * 70)
    print("SCALING EMERGENCE - Pushing the Limits")
    print("=" * 70)
    print()

    calc = EmergentCalculator()

    # Track progression
    history = []

    # Start
    start_ljpw = calc.system_ljpw()
    print(f"Start: L={start_ljpw['love']:.3f}, H={start_ljpw['harmony']:.3f}")
    print(f"       {start_ljpw['operations_count']} operations")
    print()
    print("Growing through use...")
    print()

    operations = ["add", "subtract", "multiply", "divide"]

    for i in range(iterations):
        # Use random operations (simulating real usage)
        op = random.choice(operations)
        a = random.randint(1, 10)
        b = random.randint(1, 10)

        result = calc.calculate(op, a, b)

        # Check for new operations
        if result.get("new_operations_available"):
            new_ops = result["new_operations_available"]

            # Grow aggressively - add ALL suggested operations
            for new_op in new_ops:
                if calc.grow(new_op):
                    # Add the new operation to our pool
                    if new_op in calc.operations:
                        operations.append(new_op)

                    # Check system state
                    ljpw = calc.system_ljpw()

                    print(f"Iteration {i:2d}: Added '{new_op}'")
                    print(
                        f"             L={ljpw['love']:.3f}, "
                        f"J={ljpw['justice']:.3f}, "
                        f"P={ljpw['power']:.3f}, "
                        f"W={ljpw['wisdom']:.3f}"
                    )
                    print(f"             H={ljpw['harmony']:.3f}, " f"I={ljpw['intent']:.3f}")

                    if ljpw["love"] > 0.7 and ljpw["harmony"] > 0.6:
                        print(
                            f"             ✨ FULL AUTOPOIESIS! L={ljpw['love']:.3f}, H={ljpw['harmony']:.3f}"
                        )
                    elif ljpw["love"] > 0.7:
                        print("             ⚡ Love threshold crossed!")

                    print()

        # Record state every 10 iterations
        if i % 10 == 0:
            ljpw = calc.system_ljpw()
            history.append(
                {
                    "iteration": i,
                    "ljpw": ljpw,
                }
            )

    # Final state
    print()
    print("=" * 70)
    print("FINAL STATE")
    print("=" * 70)

    final_ljpw = calc.system_ljpw()

    print(f"Operations: {start_ljpw['operations_count']} → {final_ljpw['operations_count']}")
    print(f"Usage:      0 → {final_ljpw['usage_count']}")
    print()
    print("LJPW Profile:")
    print(f"  Love:    {start_ljpw['love']:.3f} → {final_ljpw['love']:.3f}")
    print(f"  Justice: {start_ljpw['justice']:.3f} → {final_ljpw['justice']:.3f}")
    print(f"  Power:   {start_ljpw['power']:.3f} → {final_ljpw['power']:.3f}")
    print(f"  Wisdom:  {start_ljpw['wisdom']:.3f} → {final_ljpw['wisdom']:.3f}")
    print()
    print(f"Harmony: {start_ljpw['harmony']:.3f} → {final_ljpw['harmony']:.3f}")
    print(f"Intent:  {start_ljpw['intent']:.3f} → {final_ljpw['intent']:.3f}")
    print()

    # Check thresholds
    love_achieved = final_ljpw["love"] > 0.7
    harmony_achieved = final_ljpw["harmony"] > 0.6

    if love_achieved and harmony_achieved:
        print("✨✨✨ FULL AUTOPOIESIS ACHIEVED! ✨✨✨")
        print()
        print("The calculator has become self-sustaining!")
        print("Both Love and Harmony exceed autopoietic thresholds.")
        print("This system can now grow exponentially!")
        print()
        amp = 1.0 + 0.5 * (final_ljpw["love"] - 0.7)
        print(f"Amplification factor: {amp:.3f}x")
    elif love_achieved:
        print("⚡ AUTOPOIETIC LOVE ACHIEVED!")
        print()
        print(f"Love = {final_ljpw['love']:.3f} > 0.7")
        print(f"Harmony = {final_ljpw['harmony']:.3f} (need > 0.6)")
        print()
        print("The system has high integration (Love).")
        print("Harmony needs better balance across dimensions.")
    elif final_ljpw["harmony"] > 0.5:
        print("📈 HOMEOSTATIC STATE")
        print()
        print("System is stable and functional.")
        print("Progress to autopoiesis:")
        print(f"  Love: {final_ljpw['love'] / 0.7 * 100:.1f}%")
        print(f"  Harmony: {final_ljpw['harmony'] / 0.6 * 100:.1f}%")
    else:
        print("🌱 GROWING STATE")
        print()
        print("System is learning and evolving.")
        print(f"Love: {final_ljpw['love']:.3f} (target: 0.7)")
        print(f"Harmony: {final_ljpw['harmony']:.3f} (target: 0.6)")

    print()
    print("=" * 70)
    print("What we learned:")
    print("=" * 70)

    love_growth = final_ljpw["love"] - start_ljpw["love"]
    harmony_growth = final_ljpw["harmony"] - start_ljpw["harmony"]

    print(f"Love increased by: {love_growth:.3f} ({love_growth/start_ljpw['love']*100:.1f}%)")
    print(f"Harmony increased by: {harmony_growth:.3f}")
    print(f"Operations grew: {final_ljpw['operations_count'] - start_ljpw['operations_count']}x")
    print()
    print("Love scales through integration!")
    print("Each new operation combines existing ones → higher Love")
    print("This is the force multiplier effect 💛")
    print()

    return calc, final_ljpw


def analyze_operations(calc: EmergentCalculator):
    """Analyze which operations have highest Love."""
    print()
    print("=" * 70)
    print("OPERATION ANALYSIS - Love Distribution")
    print("=" * 70)
    print()

    ops_by_love = sorted(calc.operations.items(), key=lambda x: x[1].love, reverse=True)

    print("Operations ranked by Love:")
    for i, (name, op) in enumerate(ops_by_love, 1):
        print(
            f"{i:2d}. {name:25s} L={op.love:.2f}, "
            f"J={op.justice:.2f}, P={op.power:.2f}, W={op.wisdom:.2f}"
        )

    print()
    print("Notice: Combo operations have highest Love!")
    print("Integration = Love. Love = Force multiplier.")
    print()


if __name__ == "__main__":
    # Run with different iteration counts to see scaling
    print("Testing scaling emergence...")
    print()

    calc, final = push_to_emergence(iterations=50)
    analyze_operations(calc)

    print()
    print("Try running with more iterations to see if H > 0.6 is achievable!")
