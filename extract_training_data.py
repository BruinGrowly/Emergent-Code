#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
Extract Training Data from Harmonizer Analysis

This script analyzes various code examples with the Python Code Harmonizer
to extract real LJPW profiles for calibration training data.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from harmonizer_integration import PythonCodeHarmonizer


def analyze_code(code: str, name: str, harmonizer):
    """Analyze a code snippet and extract LJPW profile."""
    print(f"\nAnalyzing {name}...")
    try:
        result = harmonizer.analyze_file_content(code)
        if result and name in result:
            profile = result[name]["ice_result"]["ice_components"]["intent"].coordinates
            print(f"  ✓ L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")
            return profile
        else:
            print(f"  ✗ Analysis failed - no result for {name}")
            return None
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return None


def main():
    print("=" * 70)
    print("TRAINING DATA EXTRACTION FROM HARMONIZER")
    print("=" * 70)

    harmonizer = PythonCodeHarmonizer(quiet=True)

    # Level 1: Secure Functions
    print("\n" + "=" * 70)
    print("LEVEL 1: SECURE FUNCTIONS")
    print("=" * 70)

    secure_add = '''
def secure_add(a, b):
    """Fractally composed function: secure_add"""
    from calculator_components import add_simple, validate_numeric, log_operation
    validate_numeric(a)
    validate_numeric(b)
    result = add_simple(a, b)
    log_operation('secure_add', a, b, result)
    return result
'''

    secure_subtract = '''
def secure_subtract(a, b):
    """Fractally composed function: secure_subtract"""
    from calculator_components import subtract_simple, validate_numeric, log_operation
    validate_numeric(a)
    validate_numeric(b)
    result = subtract_simple(a, b)
    log_operation('secure_subtract', a, b, result)
    return result
'''

    secure_multiply = '''
def secure_multiply(a, b):
    """Fractally composed function: secure_multiply"""
    from calculator_components import multiply_simple, validate_numeric, log_operation
    validate_numeric(a)
    validate_numeric(b)
    result = multiply_simple(a, b)
    log_operation('secure_multiply', a, b, result)
    return result
'''

    secure_divide = '''
def secure_divide(a, b):
    """Fractally composed function: secure_divide"""
    from calculator_components import divide_simple, validate_numeric, log_operation
    validate_numeric(a)
    validate_numeric(b)
    result = divide_simple(a, b)
    log_operation('secure_divide', a, b, result)
    return result
'''

    profiles = {}
    profiles['secure_add'] = analyze_code(secure_add, 'secure_add', harmonizer)
    profiles['secure_subtract'] = analyze_code(secure_subtract, 'secure_subtract', harmonizer)
    profiles['secure_multiply'] = analyze_code(secure_multiply, 'secure_multiply', harmonizer)
    profiles['secure_divide'] = analyze_code(secure_divide, 'secure_divide', harmonizer)

    # Level 1: Simple Functions
    print("\n" + "=" * 70)
    print("LEVEL 1: SIMPLE FUNCTIONS (Primitive Wrapping)")
    print("=" * 70)

    simple_add = '''
def simple_add(a, b):
    """Simple addition wrapper"""
    from calculator_components import add_simple
    return add_simple(a, b)
'''

    simple_multiply = '''
def simple_multiply(a, b):
    """Simple multiplication wrapper"""
    from calculator_components import multiply_simple
    return multiply_simple(a, b)
'''

    profiles['simple_add'] = analyze_code(simple_add, 'simple_add', harmonizer)
    profiles['simple_multiply'] = analyze_code(simple_multiply, 'simple_multiply', harmonizer)

    # Level 2: Classes
    print("\n" + "=" * 70)
    print("LEVEL 2: CLASSES")
    print("=" * 70)

    simple_calculator = '''
class SimpleCalculator:
    """A simple calculator with basic operations"""
    def add(self, a, b):
        from calculator_components import add_simple
        return add_simple(a, b)

    def multiply(self, a, b):
        from calculator_components import multiply_simple
        return multiply_simple(a, b)
'''

    secure_calculator = '''
class SecureCalculator:
    """A secure calculator with validation and logging"""
    def add(self, a, b):
        from calculator_components import add_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = add_simple(a, b)
        log_operation('add', a, b, result)
        return result

    def subtract(self, a, b):
        from calculator_components import subtract_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = subtract_simple(a, b)
        log_operation('subtract', a, b, result)
        return result

    def multiply(self, a, b):
        from calculator_components import multiply_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = multiply_simple(a, b)
        log_operation('multiply', a, b, result)
        return result

    def divide(self, a, b):
        from calculator_components import divide_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = divide_simple(a, b)
        log_operation('divide', a, b, result)
        return result
'''

    stateful_calculator = '''
class StatefulCalculator:
    """Calculator that maintains state"""
    def __init__(self):
        self.history = []
        self.last_result = None

    def add(self, a, b):
        from calculator_components import add_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = add_simple(a, b)
        log_operation('add', a, b, result)
        self.last_result = result
        self.history.append(('add', a, b, result))
        return result

    def multiply(self, a, b):
        from calculator_components import multiply_simple, validate_numeric, log_operation
        validate_numeric(a)
        validate_numeric(b)
        result = multiply_simple(a, b)
        log_operation('multiply', a, b, result)
        self.last_result = result
        self.history.append(('multiply', a, b, result))
        return result

    def get_history(self):
        return self.history
'''

    profiles['SimpleCalculator'] = analyze_code(simple_calculator, 'SimpleCalculator', harmonizer)
    profiles['SecureCalculator'] = analyze_code(secure_calculator, 'SecureCalculator', harmonizer)
    profiles['StatefulCalculator'] = analyze_code(stateful_calculator, 'StatefulCalculator', harmonizer)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - EXTRACTED LJPW PROFILES")
    print("=" * 70)

    successful = 0
    failed = 0

    for name, profile in profiles.items():
        if profile:
            print(f"✓ {name:<25} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")
            successful += 1
        else:
            print(f"✗ {name:<25} FAILED")
            failed += 1

    print()
    print(f"Successfully extracted: {successful}/{len(profiles)} profiles")
    print(f"Failed: {failed}/{len(profiles)} profiles")

    if successful > 0:
        print("\nNext steps:")
        print("1. Add these profiles to calibrate_composition_rules.py")
        print("2. Update component profiles based on analysis")
        print("3. Re-run calibration with real data")

    return 0


if __name__ == "__main__":
    sys.exit(main())
