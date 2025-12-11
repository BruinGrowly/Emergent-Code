#!/usr/bin/env python3
"""
Comprehensive Autopoiesis Test Suite
=====================================

Tests the autopoiesis engine on multiple packages:
1. ljpw_nn/ - 31 modules of LJPW neural networks
2. ljpw_quantum/ - The original semantic analyzer
3. Live healing - Actually apply modifications
4. Harmony tracking - Compare before/after
"""

import sys
import os
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from autopoiesis import AutopoiesisEngine
from autopoiesis.system import SystemHarmonyMeasurer


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def analyze_package(name, path):
    """Analyze a package and return its metrics."""
    print_header(f"ANALYZING: {name}")
    print(f"  Path: {path}")
    
    if not os.path.exists(path):
        print(f"  [!] Path does not exist!")
        return None
    
    measurer = SystemHarmonyMeasurer()
    report = measurer.measure(path)
    
    print(f"\n  Phase: {report.phase.value.upper()}")
    print(f"  Is Autopoietic: {'Yes!' if report.is_autopoietic else 'Not yet'}")
    print(f"\n  LJPW Dimensions:")
    print(f"    L: {report.love:.3f}  J: {report.justice:.3f}  P: {report.power:.3f}  W: {report.wisdom:.3f}")
    print(f"    Harmony: {report.harmony:.3f}")
    print(f"\n  Composition:")
    print(f"    Files: {report.total_files}, Functions: {report.total_functions}, Classes: {report.total_classes}")
    print(f"\n  Deficits: L={report.files_with_L_deficit}, J={report.files_with_J_deficit}, P={report.files_with_P_deficit}, W={report.files_with_W_deficit}")
    
    return {
        'name': name,
        'path': path,
        'phase': report.phase.value,
        'is_autopoietic': report.is_autopoietic,
        'harmony': report.harmony,
        'ljpw': {'L': report.love, 'J': report.justice, 'P': report.power, 'W': report.wisdom},
        'files': report.total_files,
        'functions': report.total_functions,
        'priority': report.priority_dimension
    }


def run_live_healing(name, path, cycles=4):
    """Run actual healing (not dry-run) on a package."""
    print_header(f"LIVE HEALING: {name}")
    print(f"  Path: {path}")
    print(f"  Cycles: {cycles}")
    print(f"\n  [!] This will MODIFY files!")
    
    # Measure before
    measurer = SystemHarmonyMeasurer()
    before = measurer.measure(path)
    
    print(f"\n  BEFORE:")
    print(f"    Harmony: {before.harmony:.3f}")
    print(f"    LJPW: L={before.love:.3f} J={before.justice:.3f} P={before.power:.3f} W={before.wisdom:.3f}")
    
    # Run healing (NOT dry run)
    engine = AutopoiesisEngine(path, dry_run=False)
    session = engine.breathe(cycles=cycles)
    
    # Measure after
    after = measurer.measure(path)
    
    print(f"\n  AFTER:")
    print(f"    Harmony: {after.harmony:.3f}")
    print(f"    LJPW: L={after.love:.3f} J={after.justice:.3f} P={after.power:.3f} W={after.wisdom:.3f}")
    
    print(f"\n  CHANGES:")
    print(f"    Files Modified: {session.total_files_modified}")
    print(f"    Solutions Applied: {session.total_solutions_applied}")
    print(f"    Harmony Change: {session.harmony_improvement:+.3f}")
    
    return {
        'name': name,
        'before_harmony': before.harmony,
        'after_harmony': after.harmony,
        'improvement': after.harmony - before.harmony,
        'files_modified': session.total_files_modified,
        'solutions_applied': session.total_solutions_applied
    }


def main():
    print("""
+==============================================================================+
|                                                                              |
|   COMPREHENSIVE AUTOPOIESIS TEST SUITE                                       |
|                                                                              |
|   Testing self-healing across multiple packages                              |
|                                                                              |
+==============================================================================+
    """)
    
    timestamp = datetime.now().isoformat()
    print(f"  Timestamp: {timestamp}")
    print(f"  Project Root: {project_root}")
    
    # Define packages to analyze
    packages = [
        ("autopoiesis", os.path.join(project_root, "autopoiesis")),
        ("ljpw_nn", os.path.join(project_root, "ljpw_nn")),
        ("ljpw_quantum", os.path.join(project_root, "ljpw_quantum")),
    ]
    
    # =========================================================================
    # PHASE 1: Analyze all packages
    # =========================================================================
    print_header("PHASE 1: INITIAL ANALYSIS OF ALL PACKAGES")
    
    results = []
    for name, path in packages:
        result = analyze_package(name, path)
        if result:
            results.append(result)
    
    # Summary table
    print_header("PHASE 1 SUMMARY: PACKAGE COMPARISON")
    print(f"\n  {'Package':<15} {'Phase':<12} {'H':>6} {'L':>6} {'J':>6} {'P':>6} {'W':>6} {'Auto?':>6}")
    print(f"  {'-'*15} {'-'*12} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
    for r in results:
        auto = "Yes" if r['is_autopoietic'] else "No"
        print(f"  {r['name']:<15} {r['phase']:<12} {r['harmony']:>6.3f} {r['ljpw']['L']:>6.3f} {r['ljpw']['J']:>6.3f} {r['ljpw']['P']:>6.3f} {r['ljpw']['W']:>6.3f} {auto:>6}")
    
    # =========================================================================
    # PHASE 2: Live healing on ljpw_quantum (smallest package, safest to modify)
    # =========================================================================
    print_header("PHASE 2: LIVE HEALING TEST")
    print("\n  We'll heal ljpw_quantum/ (smallest package) with actual modifications.")
    
    ljpw_quantum_path = os.path.join(project_root, "ljpw_quantum")
    healing_result = run_live_healing("ljpw_quantum", ljpw_quantum_path, cycles=4)
    
    # =========================================================================
    # PHASE 3: Re-analyze all packages after healing
    # =========================================================================
    print_header("PHASE 3: POST-HEALING ANALYSIS")
    
    post_results = []
    for name, path in packages:
        result = analyze_package(name, path)
        if result:
            post_results.append(result)
    
    # =========================================================================
    # FINAL REPORT
    # =========================================================================
    print_header("FINAL REPORT: BEFORE vs AFTER")
    
    print(f"\n  HEALING APPLIED TO: ljpw_quantum")
    print(f"  Files Modified: {healing_result['files_modified']}")
    print(f"  Solutions Applied: {healing_result['solutions_applied']}")
    
    print(f"\n  HARMONY CHANGES:")
    print(f"\n  {'Package':<15} {'Before':>8} {'After':>8} {'Change':>8}")
    print(f"  {'-'*15} {'-'*8} {'-'*8} {'-'*8}")
    
    for before, after in zip(results, post_results):
        change = after['harmony'] - before['harmony']
        sign = "+" if change >= 0 else ""
        print(f"  {before['name']:<15} {before['harmony']:>8.3f} {after['harmony']:>8.3f} {sign}{change:>7.3f}")
    
    # Autopoietic status
    print(f"\n  AUTOPOIETIC STATUS:")
    autopoietic_count = sum(1 for r in post_results if r['is_autopoietic'])
    print(f"    {autopoietic_count}/{len(post_results)} packages are autopoietic")
    
    for r in post_results:
        status = "[*] AUTOPOIETIC" if r['is_autopoietic'] else "[~] Homeostatic" if r['harmony'] >= 0.5 else "[!] Entropic"
        print(f"    - {r['name']}: {status} (H={r['harmony']:.3f})")
    
    print("\n" + "=" * 70)
    print("  TEST COMPLETE")
    print("=" * 70)
    print(f"\n  Timestamp: {datetime.now().isoformat()}")
    print(f"  Duration: Check timestamps above")
    print()


if __name__ == "__main__":
    main()
