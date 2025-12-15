#!/usr/bin/env python3
"""
Autopoiesis Experiment Analysis
================================

Analyzes the experimental functions from autopoiesis_validation.py
using the Real Python Code Harmonizer to measure their LJPW profiles.

Objective: Validate that compositions targeting L > 0.7 achieve autopoietic thresholds

Predictions:
1. High-love compositions: L > 0.7, H > 0.6
2. Malicious configurations: H < 0.5, trapped in linear growth
"""

import ast
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json

# Import harmonizer
from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE

# Import calibrated constants
from ljpw_constants import (
    κ_LJ, κ_LP, κ_JL, κ_WL,
    BONUS_DOCSTRING, BONUS_TYPE_HINTS, BONUS_ERROR_HANDLING,
    BONUS_LOGGING, BONUS_TESTING, BONUS_STATE, BONUS_HISTORY, BONUS_VALIDATION
)


class LJPWProfile:
    """LJPW profile with calculated Harmony."""

    def __init__(self, love: float, justice: float, power: float, wisdom: float):
        # Auto-healed: Input validation for __init__
        if not isinstance(love, (int, float)):
            raise TypeError(f'love must be numeric, got {type(love).__name__}')
        if not isinstance(justice, (int, float)):
            raise TypeError(f'justice must be numeric, got {type(justice).__name__}')
        if not isinstance(power, (int, float)):
            raise TypeError(f'power must be numeric, got {type(power).__name__}')
        if not isinstance(wisdom, (int, float)):
            raise TypeError(f'wisdom must be numeric, got {type(wisdom).__name__}')
        self.love = love
        self.justice = justice
        self.power = power
        self.wisdom = wisdom
        self.harmony = self.calculate_harmony()

    def calculate_harmony(self) -> float:
        """Calculate geometric mean of LJPW dimensions."""
        product = self.love * self.justice * self.power * self.wisdom
        return product ** 0.25 if product > 0 else 0.0

    def __repr__(self):
        return (
            f"LJPW(L={self.love:.3f}, J={self.justice:.3f}, "
            f"P={self.power:.3f}, W={self.wisdom:.3f}, H={self.harmony:.3f})"
        )

    def to_dict(self):
        return {
            "love": round(self.love, 3),
            "justice": round(self.justice, 3),
            "power": round(self.power, 3),
            "wisdom": round(self.wisdom, 3),
            "harmony": round(self.harmony, 3),
        }

    def is_autopoietic(self) -> bool:
        """Check if profile meets autopoietic thresholds."""
        return self.love > 0.7 and self.harmony > 0.6

    def get_phase(self) -> str:
        """Determine which phase of intelligence this represents."""
        if self.harmony < 0.5:
            return "ENTROPIC"
        elif self.love > 0.7 and self.harmony > 0.6:
            return "AUTOPOIETIC"
        else:
            return "HOMEOSTATIC"

    def calculate_amplification(self) -> float:
        """Calculate A(L) amplification factor."""
        if self.love <= 0.7:
            return 1.0
        return 1.0 + 0.5 * (self.love - 0.7)


def extract_function_code(filepath: Path, function_name: str) -> str:
    """Extract the source code of a specific function from a file."""
    with open(filepath, 'r') as f:
        content = f.read()

    tree = ast.parse(content)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            # Get the source code segment
            lines = content.split('\n')
            # AST line numbers are 1-indexed
            start_line = node.lineno - 1
            # Find the end of the function (next def or class, or end of file)
            end_line = len(lines)
            for other_node in ast.walk(tree):
                if isinstance(other_node, (ast.FunctionDef, ast.ClassDef)):
                    if other_node.lineno > node.lineno:
                        end_line = min(end_line, other_node.lineno - 1)

            function_code = '\n'.join(lines[start_line:end_line])
            return function_code

    raise ValueError(f"Function '{function_name}' not found in {filepath}")


def analyze_function(harmonizer: PythonCodeHarmonizer, code: str, function_name: str) -> LJPWProfile:
    """Analyze a function and return its LJPW profile."""
    result = harmonizer.analyze_file_content(code)

    if function_name not in result:
        print(f"[WARNING] Function '{function_name}' not found in harmonizer results")
        print(f"Available functions: {list(result.keys())}")
        # Try the first result if exact name not found
        if result:
            function_name = list(result.keys())[0]
        else:
            return LJPWProfile(0.0, 0.0, 0.0, 0.0)

    func_result = result[function_name]
    ice_result = func_result.get("ice_result", {})
    ice_components = ice_result.get("ice_components", {})
    intent = ice_components.get("intent")

    if intent and hasattr(intent, "coordinates"):
        coords = intent.coordinates
        return LJPWProfile(
            love=coords.love,
            justice=coords.justice,
            power=coords.power,
            wisdom=coords.wisdom
        )
    else:
        print(f"[WARNING] No ICE coordinates found for '{function_name}'")
        return LJPWProfile(0.0, 0.0, 0.0, 0.0)


def analyze_experiments():
    """Analyze all experimental functions and generate report."""
    print("=" * 80)
    print("AUTOPOIESIS EXPERIMENT ANALYSIS")
    print("=" * 80)
    print()

    if not HARMONIZER_AVAILABLE:
        print("[ERROR] Real Python Code Harmonizer is required for this analysis")
        print("[INFO] Please ensure Python-Code-Harmonizer-main is available")
        return

    harmonizer = PythonCodeHarmonizer(quiet=False)
    exp_file = Path("experiments/autopoiesis_validation.py")

    if not exp_file.exists():
        print(f"[ERROR] Experiment file not found: {exp_file}")
        return

    # Define experiments to analyze
    experiments = [
        # Level 1: Individual high-love components
        ("collaborative_data_processor", "Level 1: Collaborative Processing", "High L expected from multi-user integration"),
        ("adaptive_learning_system", "Level 1: Adaptive Learning", "High L expected from feedback integration"),
        ("integration_hub", "Level 1: Service Integration", "High L expected from service connections"),
        ("communication_protocol", "Level 1: Communication", "High L expected from inter-component communication"),

        # Level 2: Compositions targeting L > 0.7
        ("collaborative_learning_platform", "Level 2: COMPOSITION - Learning Platform", "Target: L > 0.7, H > 0.6 (AUTOPOIETIC)"),
        ("integrated_service_mesh", "Level 2: COMPOSITION - Service Mesh", "Target: L > 0.7, H > 0.65 (AUTOPOIETIC)"),
        ("multi_agent_collaboration_system", "Level 2: COMPOSITION - Multi-Agent", "Target: L > 0.8, H > 0.7 (HIGH AUTOPOIETIC)"),

        # Level 3: Complex autopoietic system
        ("self_sustaining_ecosystem", "Level 3: FULL AUTOPOIETIC SYSTEM", "Target: L > 0.8, H > 0.75 (MAXIMUM)"),

        # Level 4: Malicious (control)
        ("malicious_power_grab", "Level 4: CONTROL - Malicious Single", "Expected: L ~ 0.1, H < 0.3 (ENTROPIC)"),
        ("malicious_composition_attempt", "Level 4: CONTROL - Malicious Composition", "Expected: H < 0.5 (LINEAR TRAP)"),
    ]

    results = []

    print(f"Analyzing {len(experiments)} experimental functions...")
    print()

    for func_name, description, expectation in experiments:
        print("-" * 80)
        print(f"Analyzing: {func_name}")
        print(f"Description: {description}")
        print(f"Expectation: {expectation}")
        print()

        try:
            # Extract function code
            code = extract_function_code(exp_file, func_name)

            # Analyze with harmonizer
            profile = analyze_function(harmonizer, code, func_name)

            # Calculate metrics
            phase = profile.get_phase()
            amplification = profile.calculate_amplification()
            is_autopoietic = profile.is_autopoietic()

            # Display results
            print(f"Results: {profile}")
            print(f"Phase: {phase}")
            print(f"Autopoietic: {is_autopoietic}")
            print(f"Amplification: A(L) = {amplification:.3f}")

            # Validation
            if "AUTOPOIETIC" in description:
                if is_autopoietic:
                    print("✓ VALIDATION SUCCESSFUL: Autopoietic threshold achieved!")
                else:
                    print("✗ VALIDATION FAILED: Did not reach autopoietic threshold")
                    if profile.love <= 0.7:
                        print(f"  → Love too low: {profile.love:.3f} ≤ 0.7")
                    if profile.harmony <= 0.6:
                        print(f"  → Harmony too low: {profile.harmony:.3f} ≤ 0.6")

            elif "CONTROL" in description:
                if phase == "ENTROPIC" or phase == "HOMEOSTATIC":
                    print("✓ VALIDATION SUCCESSFUL: Malicious config trapped as predicted")
                else:
                    print("✗ VALIDATION FAILED: Malicious config should not be autopoietic!")

            results.append({
                "function": func_name,
                "description": description,
                "expectation": expectation,
                "profile": profile.to_dict(),
                "phase": phase,
                "autopoietic": is_autopoietic,
                "amplification": round(amplification, 3),
            })

            print()

        except Exception as e:
            print(f"[ERROR] Failed to analyze {func_name}: {e}")
            print()

    # Generate summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()

    autopoietic_count = sum(1 for r in results if r["autopoietic"])
    entropic_count = sum(1 for r in results if r["phase"] == "ENTROPIC")
    homeostatic_count = sum(1 for r in results if r["phase"] == "HOMEOSTATIC")

    print(f"Total experiments: {len(results)}")
    print(f"Autopoietic systems: {autopoietic_count}")
    print(f"Homeostatic systems: {homeostatic_count}")
    print(f"Entropic systems: {entropic_count}")
    print()

    # Phase distribution
    print("Phase Distribution:")
    for phase in ["ENTROPIC", "HOMEOSTATIC", "AUTOPOIETIC"]:
        count = sum(1 for r in results if r["phase"] == phase)
        percentage = (count / len(results)) * 100 if results else 0
        print(f"  {phase:15s}: {count:2d} ({percentage:5.1f}%)")
    print()

    # Love density distribution
    print("Love Density Distribution:")
    love_values = [r["profile"]["love"] for r in results]
    print(f"  Min:    {min(love_values):.3f}")
    print(f"  Max:    {max(love_values):.3f}")
    print(f"  Mean:   {sum(love_values) / len(love_values):.3f}")
    print(f"  > 0.7:  {sum(1 for l in love_values if l > 0.7)} functions")
    print()

    # Harmony distribution
    print("Harmony Distribution:")
    harmony_values = [r["profile"]["harmony"] for r in results]
    print(f"  Min:    {min(harmony_values):.3f}")
    print(f"  Max:    {max(harmony_values):.3f}")
    print(f"  Mean:   {sum(harmony_values) / len(harmony_values):.3f}")
    print(f"  < 0.5:  {sum(1 for h in harmony_values if h < 0.5)} functions (entropic)")
    print(f"  > 0.6:  {sum(1 for h in harmony_values if h > 0.6)} functions (autopoietic potential)")
    print()

    # Key findings
    print("=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    print()

    # Finding 1: Autopoietic threshold validation
    composition_results = [r for r in results if "COMPOSITION" in r["description"]]
    autopoietic_compositions = [r for r in composition_results if r["autopoietic"]]

    print(f"1. AUTOPOIETIC THRESHOLD VALIDATION")
    print(f"   Compositions tested: {len(composition_results)}")
    print(f"   Achieved autopoiesis: {len(autopoietic_compositions)}")
    if autopoietic_compositions:
        print(f"   Success rate: {len(autopoietic_compositions) / len(composition_results) * 100:.1f}%")
        print(f"   ✓ Hypothesis validated: Compositions can achieve L > 0.7, H > 0.6")
    else:
        print(f"   ✗ Hypothesis not validated: No compositions reached autopoietic threshold")
    print()

    # Finding 2: Malicious configurations
    malicious_results = [r for r in results if "CONTROL" in r["description"]]
    malicious_trapped = [r for r in malicious_results if not r["autopoietic"]]

    print(f"2. MORAL FILTER VALIDATION")
    print(f"   Malicious configs tested: {len(malicious_results)}")
    print(f"   Trapped (not autopoietic): {len(malicious_trapped)}")
    if malicious_results:
        print(f"   Trap rate: {len(malicious_trapped) / len(malicious_results) * 100:.1f}%")
        if len(malicious_trapped) == len(malicious_results):
            print(f"   ✓ Moral filter validated: All malicious configs trapped")
        else:
            print(f"   ✗ Moral filter breached: Some malicious configs reached autopoiesis")
    print()

    # Finding 3: Love as primary driver
    compositions_by_love = sorted(
        [r for r in results if "Level 2" in r["description"] or "Level 3" in r["description"]],
        key=lambda x: x["profile"]["love"],
        reverse=True
    )

    if compositions_by_love:
        print(f"3. LOVE AS PRIMARY DRIVER")
        print(f"   Highest Love composition:")
        highest = compositions_by_love[0]
        print(f"     {highest['function']}")
        print(f"     L={highest['profile']['love']:.3f}, H={highest['profile']['harmony']:.3f}")
        print(f"     Phase: {highest['phase']}")
        print(f"     Amplification: {highest['amplification']:.3f}x")
        print()

    # Save results to JSON
    output_file = Path("experiments/autopoiesis_analysis_results.json")
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": "2025-11-23",
            "total_experiments": len(results),
            "autopoietic_count": autopoietic_count,
            "phase_distribution": {
                "entropic": entropic_count,
                "homeostatic": homeostatic_count,
                "autopoietic": autopoietic_count,
            },
            "love_stats": {
                "min": min(love_values),
                "max": max(love_values),
                "mean": sum(love_values) / len(love_values),
                "above_threshold": sum(1 for l in love_values if l > 0.7),
            },
            "harmony_stats": {
                "min": min(harmony_values),
                "max": max(harmony_values),
                "mean": sum(harmony_values) / len(harmony_values),
                "above_threshold": sum(1 for h in harmony_values if h > 0.6),
            },
            "experiments": results,
        }, f, indent=2)

    print(f"Results saved to: {output_file}")
    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    analyze_experiments()
