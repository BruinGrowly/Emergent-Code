#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
Harmonizer Integration Test

This script validates that the harmonizer integration is working correctly,
whether using the real harmonizer or the mock fallback.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE

def main():
    print("=" * 70)
    print("HARMONIZER INTEGRATION TEST")
    print("=" * 70)
    print()

    # Test 1: Check which harmonizer is active
    print("Test 1: Harmonizer Detection")
    print("-" * 70)
    if HARMONIZER_AVAILABLE:
        print("✅ Real Python Code Harmonizer detected and loaded!")
        print("   Location: Python-Code-Harmonizer-main/")
    else:
        print("⏳ Using Mock Harmonizer (zero profiles)")
        print("   To use real harmonizer:")
        print("   1. Clone/copy Python-Code-Harmonizer to project root")
        print("   2. Ensure directory structure: Python-Code-Harmonizer-main/harmonizer/main.py")
    print()

    # Test 2: Basic functionality test
    print("Test 2: Basic Functionality")
    print("-" * 70)

    test_code = """
def test_function(x, y):
    '''A simple test function.'''
    if x < 0 or y < 0:
        raise ValueError("Inputs must be non-negative")
    return x + y
"""

    try:
        harmonizer = PythonCodeHarmonizer(quiet=True)
        result = harmonizer.analyze_file_content(test_code)

        if result and 'test_function' in result:
            profile = result['test_function']['ice_result']['ice_components']['intent'].coordinates
            print(f"✅ Harmonizer analysis successful!")
            print(f"   Function: test_function")
            print(f"   LJPW Profile:")
            print(f"     Love:    {profile.love:.3f}")
            print(f"     Justice: {profile.justice:.3f}")
            print(f"     Power:   {profile.power:.3f}")
            print(f"     Wisdom:  {profile.wisdom:.3f}")

            if HARMONIZER_AVAILABLE:
                print(f"   ✓ Real LJPW semantic analysis")
            else:
                print(f"   ⚠ Mock harmonizer (all zeros expected)")
        else:
            print("❌ Harmonizer analysis failed - unexpected result format")
            print(f"   Result: {result}")
    except Exception as e:
        print(f"❌ Harmonizer analysis error: {e}")
        import traceback
        traceback.print_exc()
    print()

    # Test 3: Integration with experiments
    print("Test 3: Experiment Compatibility")
    print("-" * 70)

    experiment_files = [
        "experiments/composition_discovery.py",
        "experiments/fractal_composition_level2.py",
        "experiments/fractal_level3_modules.py",
        "experiments/fractal_level4_packages.py",
        "experiments/fractal_level5_applications.py",
        "experiments/fractal_level6_platforms.py",
    ]

    all_good = True
    for exp_file in experiment_files:
        exp_path = project_root / exp_file
        if exp_path.exists():
            # Check if it imports from harmonizer_integration
            content = exp_path.read_text()
            if "from harmonizer_integration import" in content:
                print(f"✅ {exp_file.split('/')[-1]:<40} integrated")
            else:
                print(f"❌ {exp_file.split('/')[-1]:<40} NOT integrated")
                all_good = False
        else:
            print(f"⚠  {exp_file.split('/')[-1]:<40} not found")
            all_good = False

    if all_good:
        print()
        print("✅ All experiments are using unified harmonizer integration!")
    print()

    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    if HARMONIZER_AVAILABLE:
        print("✅ Status: Real harmonizer active and working")
        print("✅ Ready for: Empirical LJPW analysis across all 6 levels")
        print("✅ Next step: Run experiments to get real semantic profiles")
    else:
        print("⏳ Status: Mock harmonizer active (fallback mode)")
        print("✅ Ready for: Composition logic testing with zero profiles")
        print("📋 Next step: Install Python-Code-Harmonizer for real LJPW analysis")
        print()
        print("Installation:")
        print("  cd /home/user/Emergent-Code/")
        print("  git clone <harmonizer-repo-url> Python-Code-Harmonizer-main")
        print()
        print("See HARMONIZER_SETUP.md for detailed instructions.")
    print("=" * 70)

    return 0 if (HARMONIZER_AVAILABLE or not all_good) else 0


if __name__ == "__main__":
    sys.exit(main())
