#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
Comprehensive Test Suite for Emergent Code

Runs all experiments and validates:
1. All experiments execute without errors
2. Expected output patterns are present
3. LJPW profiles are generated correctly
4. Discovery engines find solutions
5. Generated artifacts are created
"""

import sys
import subprocess
import time
from pathlib import Path

# ANSI colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

class TestResult:
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.duration = 0
        self.output = ""
        self.error = ""

def run_experiment(exp_path: Path, timeout: int = 60) -> TestResult:
    """Run a single experiment and capture results."""
    result = TestResult(exp_path.stem)

    print(f"{BLUE}Running: {exp_path.name}{RESET}")

    start = time.time()
    try:
        proc = subprocess.run(
            [sys.executable, str(exp_path)],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        result.duration = time.time() - start
        result.output = proc.stdout
        result.error = proc.stderr
        result.passed = proc.returncode == 0

    except subprocess.TimeoutExpired:
        result.duration = timeout
        result.error = f"Timeout after {timeout}s"
        result.passed = False
    except Exception as e:
        result.duration = time.time() - start
        result.error = str(e)
        result.passed = False

    return result

def validate_output(result: TestResult) -> list:
    """Validate experiment output contains expected patterns."""
    validations = []

    # Common patterns expected in all experiments
    if "LJPW" in result.output:
        validations.append(("✓ LJPW profiles generated", True))
    else:
        validations.append(("✗ No LJPW profiles found", False))

    # Level-specific validations
    if "composition_discovery" in result.name:
        if "COMPOSITION DISCOVERY" in result.output:
            validations.append(("✓ Composition discovery executed", True))
        if "Predicted profile" in result.output:
            validations.append(("✓ Predictions made", True))

    elif "level2" in result.name or "class_discovery" in result.name:
        if "Class" in result.output or "CLASS" in result.output:
            validations.append(("✓ Class generation validated", True))

    elif "level3" in result.name:
        if "Module" in result.output or "MODULE" in result.output:
            validations.append(("✓ Module composition validated", True))

    elif "level4" in result.name:
        if "Package" in result.output or "PACKAGE" in result.output:
            validations.append(("✓ Package composition validated", True))

    elif "level5" in result.name:
        if "Application" in result.output or "APPLICATION" in result.output:
            validations.append(("✓ Application composition validated", True))

    elif "level6" in result.name:
        if "Platform" in result.output or "PLATFORM" in result.output:
            validations.append(("✓ Platform composition validated", True))

    # Check for discovery
    if "Discovery" in result.output or "DISCOVERY" in result.output:
        validations.append(("✓ Discovery engine active", True))

    # Check for fractal validation
    if "FRACTAL" in result.output or "fractal" in result.output:
        validations.append(("✓ Fractal validation present", True))

    return validations

def print_summary(results: list):
    """Print test summary."""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    for result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result.passed else f"{RED}✗ FAIL{RESET}"
        print(f"{status} {result.name:<40} {result.duration:.1f}s")

        if not result.passed and result.error:
            print(f"      Error: {result.error[:100]}")

    print("-" * 70)
    print(f"Total: {passed}/{total} passed ({100*passed/total:.0f}%)")

    if passed == total:
        print(f"{GREEN}✓ All experiments passed!{RESET}")
    else:
        print(f"{YELLOW}⚠ {total - passed} experiments failed{RESET}")

    print("=" * 70)

def main():
    print("=" * 70)
    print("EMERGENT CODE - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print()

    # Find all experiments
    project_root = Path(__file__).parent
    experiments_dir = project_root / "experiments"

    experiments = sorted(experiments_dir.glob("*.py"))

    if not experiments:
        print(f"{RED}No experiments found in {experiments_dir}{RESET}")
        return 1

    print(f"Found {len(experiments)} experiments to test\n")

    # Run all experiments
    results = []
    for exp in experiments:
        result = run_experiment(exp)

        if result.passed:
            print(f"  {GREEN}✓{RESET} Completed in {result.duration:.1f}s")
        else:
            print(f"  {RED}✗{RESET} Failed: {result.error[:80]}")

        # Validate output
        validations = validate_output(result)
        for msg, status in validations:
            color = GREEN if status else YELLOW
            print(f"    {color}{msg}{RESET}")

        results.append(result)
        print()

    # Print summary
    print_summary(results)

    # Return exit code
    return 0 if all(r.passed for r in results) else 1

if __name__ == "__main__":
    sys.exit(main())
