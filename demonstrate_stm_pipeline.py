#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
Demonstrate the STM (Signal, Transform, Meaning) Pipeline

This script shows how raw signals (code) transform into semantic meaning (LJPW)
through the Python Code Harmonizer's STM pipeline.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from harmonizer_integration import PythonCodeHarmonizer


def demonstrate_stm_pipeline():
    """Demonstrate the complete STM transformation pipeline."""

    print("=" * 80)
    print("STM FRAMEWORK DEMONSTRATION")
    print("Signal → Transform → Meaning")
    print("=" * 80)
    print()
    print("This demonstration shows how raw code signals are transformed")
    print("into semantic meaning (LJPW coordinates) through multiple stages.")
    print("=" * 80)

    harmonizer = PythonCodeHarmonizer(quiet=True)

    # =========================================================================
    # STAGE 1: Single Signal → Meaning
    # =========================================================================
    print("\n" + "=" * 80)
    print("STAGE 1: SINGLE SIGNAL TRANSFORMATION")
    print("=" * 80)
    print("\nDemonstrates: How a single code signal transforms into LJPW meaning")
    print()

    code_signal = """
def validate_user_input(data):
    '''Validate user input with type checking'''
    if not isinstance(data, dict):
        raise TypeError("Invalid data type")
    return data
"""

    print("SIGNAL (Raw Code):")
    print(code_signal)
    print("\nTRANSFORM:")
    print("  1. Parse AST")
    print("  2. Extract intent from name: 'validate_user_input'")
    print("  3. Extract intent from docstring: 'Validate user input...'")
    print("  4. Extract execution from body: If statement, raise, return")
    print("  5. Map to semantic dimensions")
    print("  6. Calculate LJPW coordinates")
    print()

    result = harmonizer.analyze_file_content(code_signal)
    if result and "validate_user_input" in result:
        profile = result["validate_user_input"]["ice_result"]["ice_components"]["intent"].coordinates
        print("MEANING (LJPW Coordinates):")
        print(f"  L={profile.love:.3f}   (Love - connection, communication)")
        print(f"  J={profile.justice:.3f}   (Justice - validation, correctness)")
        print(f"  P={profile.power:.3f}   (Power - transformation, action)")
        print(f"  W={profile.wisdom:.3f}   (Wisdom - understanding, knowledge)")
        print()
        print("INTERPRETATION:")
        if profile.justice > 0.5:
            print("  → High Justice: Strong validation/checking focus")
        if profile.love > 0.3:
            print("  → Moderate Love: User-oriented error handling")
        if profile.wisdom > 0.3:
            print("  → Moderate Wisdom: Understanding data types")
        if profile.power > 0.3:
            print("  → Moderate Power: Error raising capability")

    # =========================================================================
    # STAGE 2: Multi-Signal Aggregation
    # =========================================================================
    print("\n" + "=" * 80)
    print("STAGE 2: MULTI-SIGNAL AGGREGATION")
    print("=" * 80)
    print("\nDemonstrates: How multiple signals aggregate into unified meaning")
    print()

    signals = {
        "Signal 1": """
def add_simple(a, b):
    '''Simple addition'''
    return a + b
""",
        "Signal 2": """
def validate_numeric(value):
    '''Validate numeric input'''
    if not isinstance(value, (int, float)):
        raise TypeError("Must be numeric")
""",
        "Signal 3": """
def log_operation(operation, a, b, result):
    '''Log arithmetic operation'''
    print(f"[LOG] {operation}({a}, {b}) = {result}")
""",
    }

    meanings = {}
    print("SIGNALS (Three Components):")
    for name, code in signals.items():
        result = harmonizer.analyze_file_content(code)
        if result:
            func_name = list(result.keys())[0]
            profile = result[func_name]["ice_result"]["ice_components"]["intent"].coordinates
            meanings[name] = profile
            print(f"\n{name}: {func_name}")
            print(f"  → L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    print("\n\nTRANSFORM (Aggregation):")
    print("  1. Analyze each signal individually")
    print("  2. Calculate centroid of LJPW coordinates")
    print("  3. Consider signal weights")
    print()

    if meanings:
        # Calculate aggregate
        avg_l = sum(p.love for p in meanings.values()) / len(meanings)
        avg_j = sum(p.justice for p in meanings.values()) / len(meanings)
        avg_p = sum(p.power for p in meanings.values()) / len(meanings)
        avg_w = sum(p.wisdom for p in meanings.values()) / len(meanings)

        print("MEANING (Aggregated LJPW):")
        print(f"  L={avg_l:.3f}   (Average Love)")
        print(f"  J={avg_j:.3f}   (Average Justice)")
        print(f"  P={avg_p:.3f}   (Average Power)")
        print(f"  W={avg_w:.3f}   (Average Wisdom)")

    # =========================================================================
    # STAGE 3: Intent-Modulated Transform
    # =========================================================================
    print("\n" + "=" * 80)
    print("STAGE 3: INTENT-MODULATED TRANSFORMATION")
    print("=" * 80)
    print("\nDemonstrates: How intent signal modulates the final meaning")
    print()

    # Composition with intent
    composed_signal = """
def secure_add(a, b):
    '''
    Securely add two numbers with validation and logging.
    Ensures type safety and tracks all operations.
    '''
    if not isinstance(a, (int, float)):
        raise TypeError("First argument must be numeric")
    if not isinstance(b, (int, float)):
        raise TypeError("Second argument must be numeric")
    result = a + b
    print(f"[LOG] secure_add({a}, {b}) = {result}")
    return result
"""

    print("SIGNAL (Composed Function):")
    print(composed_signal)
    print("\nTRANSFORM (Multi-Stage):")
    print("  1. Extract intent signal: 'secure_add'")
    print("     → Keywords: 'secure', 'add'")
    print("     → Intent LJPW: Justice (secure), Love (add)")
    print()
    print("  2. Extract component signals:")
    print("     → Validation logic (Justice)")
    print("     → Arithmetic operation (Love)")
    print("     → Logging behavior (Love)")
    print()
    print("  3. Aggregate component meanings")
    print("  4. Blend with intent meaning (40% intent, 40% components)")
    print("  5. Add structural bonuses (20%)")
    print()

    result = harmonizer.analyze_file_content(composed_signal)
    if result and "secure_add" in result:
        profile = result["secure_add"]["ice_result"]["ice_components"]["intent"].coordinates
        print("MEANING (Final LJPW):")
        print(f"  L={profile.love:.3f}   (Love from addition + logging)")
        print(f"  J={profile.justice:.3f}   (Justice from 'secure' + validation)")
        print(f"  P={profile.power:.3f}   (Power from error raising)")
        print(f"  W={profile.wisdom:.3f}   (Wisdom from 'secure' understanding)")
        print()
        print("EMERGENCE OBSERVED:")
        print("  → Intent 'secure' contributes Justice and Wisdom")
        print("  → Components contribute Love (add, log) and Justice (validate)")
        print("  → Result: Balanced profile across multiple dimensions")
        print("  → This demonstrates intent-modulated transformation!")

    # =========================================================================
    # STAGE 4: Signal Quality Analysis
    # =========================================================================
    print("\n" + "=" * 80)
    print("STAGE 4: SIGNAL QUALITY COMPARISON")
    print("=" * 80)
    print("\nDemonstrates: How signal quality affects meaning clarity")
    print()

    quality_tests = [
        ("Low Quality", """
def do_stuff(x, y):
    return x + y
"""),
        ("Medium Quality", """
def add_numbers(x, y):
    '''Add two numbers'''
    return x + y
"""),
        ("High Quality", """
def add_numbers_securely(x, y):
    '''
    Add two numbers with type validation and logging.
    Ensures inputs are numeric and tracks the operation.
    '''
    if not isinstance(x, (int, float)):
        raise TypeError("x must be numeric")
    if not isinstance(y, (int, float)):
        raise TypeError("y must be numeric")
    result = x + y
    print(f"[LOG] {x} + {y} = {result}")
    return result
"""),
    ]

    print("Signal Quality Impact on Meaning:\n")
    for quality, code in quality_tests:
        result = harmonizer.analyze_file_content(code)
        if result:
            func_name = list(result.keys())[0]
            profile = result[func_name]["ice_result"]["ice_components"]["intent"].coordinates

            # Calculate semantic richness
            richness = sum([profile.love, profile.justice, profile.power, profile.wisdom])
            dimensions_used = sum([1 for v in [profile.love, profile.justice, profile.power, profile.wisdom] if v > 0.1])

            print(f"{quality:15s} Signal: {func_name}")
            print(f"{'':15s} LJPW: L={profile.love:.2f}, J={profile.justice:.2f}, P={profile.power:.2f}, W={profile.wisdom:.2f}")
            print(f"{'':15s} Richness: {richness:.2f} | Dimensions: {dimensions_used}/4")
            print()

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n" + "=" * 80)
    print("STM PIPELINE SUMMARY")
    print("=" * 80)
    print()
    print("The STM Framework operates in stages:")
    print()
    print("1. SIGNAL CAPTURE")
    print("   → Extract raw information from code")
    print("   → Multiple channels: name, docstring, body, structure")
    print()
    print("2. SIGNAL PARSING")
    print("   → Tokenize and analyze each channel")
    print("   → Map to semantic dimensions (LJPW)")
    print()
    print("3. SIGNAL AGGREGATION")
    print("   → Combine multiple signals")
    print("   → Weight by importance (intent 40%, components 40%, structure 20%)")
    print()
    print("4. SIGNAL TRANSFORMATION")
    print("   → Apply coupling (dimension amplification)")
    print("   → Add structural bonuses")
    print("   → Normalize to [0,1] range")
    print()
    print("5. MEANING GENERATION")
    print("   → Output LJPW coordinates")
    print("   → Calculate quality metrics")
    print("   → Provide semantic interpretation")
    print()
    print("=" * 80)
    print()
    print("KEY INSIGHTS:")
    print()
    print("✓ Every code analysis is STM (Signal → Transform → Meaning)")
    print("✓ Intent signals carry 40% of semantic weight")
    print("✓ High-quality signals produce richer meanings")
    print("✓ Multiple signals aggregate into unified meaning")
    print("✓ Transforms can be calibrated and optimized")
    print()
    print("STM is the engine that powers LJPW semantic analysis! 🎯")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_stm_pipeline()
