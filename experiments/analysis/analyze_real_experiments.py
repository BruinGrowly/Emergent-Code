#!/usr/bin/env python3
"""
Analyze Real Autopoiesis Experiments
=====================================

Analyzes the REAL, functional implementations from real_autopoiesis_experiments.py
to validate the autopoiesis hypothesis with actual working code.
"""

import ast
from pathlib import Path
from typing import Dict
import json

from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE


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
            lines = content.split('\n')
            start_line = node.lineno - 1
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


def analyze_real_experiments():
    """Analyze all REAL experimental functions."""
    print("=" * 80)
    print("REAL AUTOPOIESIS EXPERIMENT ANALYSIS")
    print("=" * 80)
    print()

    if not HARMONIZER_AVAILABLE:
        print("[ERROR] Real Python Code Harmonizer is required")
        return

    harmonizer = PythonCodeHarmonizer(quiet=False)
    exp_file = Path("experiments/real_autopoiesis_experiments.py")

    if not exp_file.exists():
        print(f"[ERROR] Experiment file not found: {exp_file}")
        return

    # Define REAL experiments to analyze
    experiments = [
        # Level 1: Real high-love components
        ("integrate_user_data", "Level 1: REAL User Integration",
         "Actual weighted consensus from multiple users"),

        ("validate_with_constraints", "Level 1: REAL Validation",
         "Actual constraint checking with detailed errors"),

        ("adaptive_weight_calculator", "Level 1: REAL Adaptation",
         "Actual learning from historical performance"),

        ("execute_with_retry", "Level 1: REAL Power",
         "Actual execution with retry logic"),

        # Level 2: Real compositions
        ("collaborative_consensus_system", "Level 2: REAL COMPOSITION",
         "Target: L > 0.7, H > 0.6 - All 4 dimensions working together"),

        ("feedback_learning_loop", "Level 3: REAL AUTOPOIETIC LOOP",
         "Target: L > 0.8, H > 0.7 - Self-improving feedback system"),

        ("multi_agent_task_solver", "Level 3: REAL MULTI-AGENT",
         "Target: L > 0.8, H > 0.7 - Agents with collective intelligence"),
    ]

    results = []

    print(f"Analyzing {len(experiments)} REAL functional implementations...")
    print()

    for func_name, description, expectation in experiments:
        print("-" * 80)
        print(f"Analyzing: {func_name}")
        print(f"Description: {description}")
        print(f"Expectation: {expectation}")
        print()

        try:
            code = extract_function_code(exp_file, func_name)
            profile = analyze_function(harmonizer, code, func_name)

            phase = profile.get_phase()
            amplification = profile.calculate_amplification()
            is_autopoietic = profile.is_autopoietic()

            print(f"Results: {profile}")
            print(f"Phase: {phase}")
            print(f"Autopoietic: {is_autopoietic}")
            print(f"Amplification: A(L) = {amplification:.3f}")

            # Detailed dimension analysis
            print()
            print("Dimension Analysis:")
            print(f"  Love (L):    {profile.love:.3f} {'✓ > 0.7' if profile.love > 0.7 else '✗ ≤ 0.7'}")
            print(f"  Justice (J): {profile.justice:.3f}")
            print(f"  Power (P):   {profile.power:.3f} {'✓ > 0' if profile.power > 0 else '✗ = 0 (NO CAPABILITY!)'}")
            print(f"  Wisdom (W):  {profile.wisdom:.3f}")
            print(f"  Harmony (H): {profile.harmony:.3f} {'✓ > 0.6' if profile.harmony > 0.6 else '✗ ≤ 0.6'}")

            # Validation against targets
            if "COMPOSITION" in description or "AUTOPOIETIC" in description or "MULTI-AGENT" in description:
                print()
                if is_autopoietic:
                    print("✓✓✓ AUTOPOIESIS ACHIEVED! ✓✓✓")
                    print(f"  This system has crossed the threshold into self-sustaining growth!")
                else:
                    print("Autopoiesis status:")
                    if profile.love <= 0.7:
                        print(f"  ⚠ Love: {profile.love:.3f} ≤ 0.7 (need more integration)")
                    else:
                        print(f"  ✓ Love: {profile.love:.3f} > 0.7 (sufficient)")

                    if profile.harmony <= 0.6:
                        print(f"  ⚠ Harmony: {profile.harmony:.3f} ≤ 0.6 (dimensions imbalanced)")
                        if profile.power == 0:
                            print(f"    → Power = 0 (system has no capability!)")
                        if profile.justice == 0:
                            print(f"    → Justice = 0 (no validation!)")
                    else:
                        print(f"  ✓ Harmony: {profile.harmony:.3f} > 0.6 (balanced)")

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
            import traceback
            traceback.print_exc()
            print()

    # SUMMARY
    print("=" * 80)
    print("SUMMARY - REAL IMPLEMENTATIONS")
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

    # Comparison with stub experiments
    print("Comparison: REAL vs STUB implementations")
    print(f"  Stub experiments: 0 autopoietic (all P=0)")
    print(f"  Real experiments: {autopoietic_count} autopoietic")
    print()

    if autopoietic_count > 0:
        print("🎉 HYPOTHESIS VALIDATED! 🎉")
        print()
        print("REAL implementations with actual Love (integration) CAN achieve")
        print("the autopoietic threshold (L > 0.7, H > 0.6)!")
        print()
        print("Autopoietic functions:")
        for r in results:
            if r["autopoietic"]:
                print(f"  - {r['function']}")
                print(f"    L={r['profile']['love']:.3f}, H={r['profile']['harmony']:.3f}")
                print(f"    Amplification: {r['amplification']:.3f}x")
        print()
    else:
        print("Analysis of why autopoiesis was not achieved:")
        for r in results:
            if "COMPOSITION" in r["description"]:
                print(f"  {r['function']}:")
                p = r['profile']
                if p['power'] == 0:
                    print(f"    ⚠ Power = 0 (no capability detected)")
                if p['love'] <= 0.7:
                    print(f"    ⚠ Love = {p['love']} ≤ 0.7 (insufficient integration)")
                if p['harmony'] <= 0.6:
                    print(f"    ⚠ Harmony = {p['harmony']} ≤ 0.6")
        print()

    # Save results
    output_file = Path("experiments/real_autopoiesis_analysis.json")
    with open(output_file, 'w') as f:
        json.dump({
            "timestamp": "2025-11-23",
            "experiment_type": "REAL_FUNCTIONAL_CODE",
            "total_experiments": len(results),
            "autopoietic_count": autopoietic_count,
            "phase_distribution": {
                "entropic": entropic_count,
                "homeostatic": homeostatic_count,
                "autopoietic": autopoietic_count,
            },
            "experiments": results,
        }, f, indent=2)

    print(f"Results saved to: {output_file}")
    print()
    print("=" * 80)


if __name__ == "__main__":
    analyze_real_experiments()
