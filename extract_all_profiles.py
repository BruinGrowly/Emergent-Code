#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
Comprehensive LJPW Profile Extraction

Extracts all available LJPW profiles from:
1. Generated files from experiments
2. Standalone function patterns
3. Class patterns
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from harmonizer_integration import PythonCodeHarmonizer


def analyze_code(code: str, name: str, harmonizer):
    """Analyze a code snippet and extract all LJPW profiles."""
    result = harmonizer.analyze_file_content(code)
    profiles = {}
    if result:
        for func_name, data in result.items():
            try:
                profile = data['ice_result']['ice_components']['intent'].coordinates
                profiles[func_name] = profile
            except (KeyError, AttributeError):
                pass
    return profiles


def main():
    print("=" * 80)
    print("COMPREHENSIVE LJPW PROFILE EXTRACTION")
    print("=" * 80)

    harmonizer = PythonCodeHarmonizer(quiet=True)
    all_profiles = {}

    # ========================================================================
    # SECTION 1: Standalone Secure Functions
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 1: STANDALONE SECURE FUNCTIONS (Level 1)")
    print("=" * 80)

    secure_add_standalone = '''
def secure_add(a, b):
    """
    Fractally composed function: secure_add
    Core: add_simple (Power)
    Guard: validate_numeric (Justice)
    Observer: log_operation (Love)
    """
    validate_numeric(a, b)
    result = a + b
    log_operation('secure_add', a, b, result)
    return result
'''

    profiles = analyze_code(secure_add_standalone, 'secure_add_standalone', harmonizer)
    for name, profile in profiles.items():
        key = f"secure_add_function"
        all_profiles[key] = profile
        print(f"✓ {key:<35} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    # ========================================================================
    # SECTION 2: Generated SecureCalculator Class
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 2: GENERATED FILES - SecureCalculator")
    print("=" * 80)

    generated_file = Path("generated_SecureCalculator.py")
    if generated_file.exists():
        code = generated_file.read_text()
        profiles = analyze_code(code, 'generated_SecureCalculator', harmonizer)
        for name, profile in profiles.items():
            key = f"SecureCalculator.{name}"
            all_profiles[key] = profile
            print(f"✓ {key:<35} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")
    else:
        print("⚠ generated_SecureCalculator.py not found")

    # ========================================================================
    # SECTION 3: Simple Functions (Primitive Wrapping)
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 3: SIMPLE FUNCTIONS (Primitive Wrapping)")
    print("=" * 80)

    simple_add = '''
def simple_add(a, b):
    """Simple addition"""
    return a + b
'''

    simple_multiply = '''
def simple_multiply(a, b):
    """Simple multiplication"""
    return a * b
'''

    profiles = analyze_code(simple_add, 'simple_add', harmonizer)
    for name, profile in profiles.items():
        all_profiles[f"simple_add_function"] = profile
        print(f"✓ simple_add_function{'':<20} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    profiles = analyze_code(simple_multiply, 'simple_multiply', harmonizer)
    for name, profile in profiles.items():
        all_profiles[f"simple_multiply_function"] = profile
        print(f"✓ simple_multiply_function{'':<15} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    # ========================================================================
    # SECTION 4: Simple Classes
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 4: SIMPLE CLASSES (Level 2)")
    print("=" * 80)

    simple_calculator_class = '''
class SimpleCalculator:
    """A simple calculator with basic operations"""

    def add(self, a, b):
        """Add two numbers"""
        return a + b

    def multiply(self, a, b):
        """Multiply two numbers"""
        return a * b
'''

    profiles = analyze_code(simple_calculator_class, 'SimpleCalculator', harmonizer)
    for name, profile in profiles.items():
        key = f"SimpleCalculator.{name}"
        all_profiles[key] = profile
        print(f"✓ {key:<35} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    # ========================================================================
    # SECTION 5: Stateful Classes
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 5: STATEFUL CLASSES")
    print("=" * 80)

    stateful_calculator = '''
class StatefulCalculator:
    """Calculator that maintains state and history"""

    def __init__(self):
        """Initialize with empty history"""
        self.history = []
        self.last_result = None

    def add(self, a, b):
        """Add two numbers and record in history"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a + b
        print(f"[LOG] add({a}, {b}) = {result}")
        self.last_result = result
        self.history.append(('add', a, b, result))
        return result

    def multiply(self, a, b):
        """Multiply two numbers and record in history"""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a * b
        print(f"[LOG] multiply({a}, {b}) = {result}")
        self.last_result = result
        self.history.append(('multiply', a, b, result))
        return result

    def get_history(self):
        """Get operation history"""
        return self.history
'''

    profiles = analyze_code(stateful_calculator, 'StatefulCalculator', harmonizer)
    for name, profile in profiles.items():
        key = f"StatefulCalculator.{name}"
        all_profiles[key] = profile
        print(f"✓ {key:<35} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    # ========================================================================
    # SECTION 6: Primitive Aggregation Patterns
    # ========================================================================
    print("\n" + "=" * 80)
    print("SECTION 6: PRIMITIVE AGGREGATION PATTERNS")
    print("=" * 80)

    # Zero aggregation
    zero_aggregate = '''
def zero_aggregate(a, b):
    """Function with zero semantic content"""
    pass
'''

    profiles = analyze_code(zero_aggregate, 'zero_aggregate', harmonizer)
    for name, profile in profiles.items():
        all_profiles['zero_aggregate'] = profile
        print(f"✓ zero_aggregate{'':<22} L={profile.love:.3f}, J={profile.justice:.3f}, P={profile.power:.3f}, W={profile.wisdom:.3f}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("SUMMARY - ALL EXTRACTED PROFILES")
    print("=" * 80)
    print(f"\nTotal profiles extracted: {len(all_profiles)}")
    print()

    # Group by type
    functions = {k: v for k, v in all_profiles.items() if '_function' in k or k == 'zero_aggregate'}
    class_methods = {k: v for k, v in all_profiles.items() if '.' in k}

    print(f"Standalone functions: {len(functions)}")
    print(f"Class methods: {len(class_methods)}")

    # Save to file for import
    print("\n" + "=" * 80)
    print("SAVING PROFILES FOR TRAINING")
    print("=" * 80)

    output_file = Path("extracted_profiles.txt")
    with output_file.open('w') as f:
        f.write("# Extracted LJPW Profiles\n")
        f.write("# Format: name = L, J, P, W\n\n")
        for name, profile in sorted(all_profiles.items()):
            f.write(f"{name} = {profile.love:.3f}, {profile.justice:.3f}, {profile.power:.3f}, {profile.wisdom:.3f}\n")

    print(f"✓ Saved {len(all_profiles)} profiles to {output_file}")

    # Print Python code for easy import
    print("\n" + "=" * 80)
    print("PYTHON CODE FOR CALIBRATION SCRIPT")
    print("=" * 80)
    print("\n# Add these profiles to calibrate_composition_rules.py:")
    print()

    for name, profile in sorted(all_profiles.items()):
        safe_name = name.replace('.', '_').replace('_function', '')
        print(f"# {name}")
        print(f"{safe_name}_profile = LJPWProfile({profile.love:.3f}, {profile.justice:.3f}, {profile.power:.3f}, {profile.wisdom:.3f})")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
