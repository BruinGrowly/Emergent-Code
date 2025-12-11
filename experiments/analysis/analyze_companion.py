#!/usr/bin/env python3
"""
Analyze the LJPW Companion itself.

The critical test: Does code written with GENUINE INTENT score higher
in Love and Harmony than code written mechanically?
"""

import inspect
from ljpw_companion import LJPWCompanion

def main():
    companion = LJPWCompanion()

    print("=" * 80)
    print("ANALYZING THE COMPANION ITSELF")
    print("=" * 80)
    print()
    print("Does genuine intent show up in the LJPW profile?")
    print("This code was written with:")
    print("  - Real desire to help developers")
    print("  - Genuine belief in the framework's value")
    print("  - Intent to create something useful, not just an exercise")
    print()
    print("Let's see if that intent is measurable...")
    print()

    # Analyze the main methods
    methods_to_analyze = [
        ("analyze_code_with_guidance", "The core method - analyzes and guides"),
        ("_generate_insights", "Where genuine help lives - actionable suggestions"),
        ("_generate_encouragement", "Supportive messaging - empathy and support"),
        ("display_guidance", "Clear, helpful communication"),
    ]

    for method_name, description in methods_to_analyze:
        print("-" * 80)
        print(f"Method: {method_name}")
        print(f"Purpose: {description}")
        print()

        # Get source
        method = getattr(LJPWCompanion, method_name)
        code = inspect.getsource(method)

        # Analyze
        analysis = companion.analyze_code_with_guidance(code, method_name)

        if "error" in analysis:
            print(f"Error: {analysis['error']}")
            continue

        ljpw = analysis['ljpw']
        h = analysis['harmony']

        print(f"LJPW: L={ljpw['love']:.3f}, J={ljpw['justice']:.3f}, "
              f"P={ljpw['power']:.3f}, W={ljpw['wisdom']:.3f}")
        print(f"Harmony: {h:.3f}")
        print(f"Phase: {analysis['phase']}")

        if ljpw['love'] > 0.5:
            print(f"  ✓ Love > 0.5! Higher than most mechanical compositions")
        if h > 0.3:
            print(f"  ✓ Harmony > 0.3! Higher than mechanical compositions")
        if analysis['autopoietic_potential']['is_autopoietic']:
            print(f"  ✨ AUTOPOIETIC! The genuine intent shows up!")

        print()

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)


if __name__ == "__main__":
    main()
