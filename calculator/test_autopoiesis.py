#!/usr/bin/env python3
"""
Test the Autopoiesis Engine

This script demonstrates the self-healing capabilities by:
1. Analyzing the autopoiesis package itself for LJPW deficits
2. Showing the current system health
3. Optionally running breathing cycles to heal
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autopoiesis import AutopoiesisEngine
from autopoiesis.system import SystemHarmonyMeasurer


def main():
    print("""
+==============================================================================+
|                                                                              |
|   AUTOPOIESIS ENGINE TEST                                                    |
|                                                                              |
|   Testing self-healing on the autopoiesis package itself                     |
|                                                                              |
+==============================================================================+
    """)
    
    # Path to autopoiesis package (analyze itself!)
    target_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "autopoiesis"
    )
    
    print(f"  Target: {target_path}\n")
    
    # Step 1: Measure initial system health
    print("=" * 70)
    print("  STEP 1: INITIAL SYSTEM HEALTH MEASUREMENT")
    print("=" * 70)
    
    measurer = SystemHarmonyMeasurer()
    report = measurer.measure(target_path)
    measurer.print_report(report)
    
    # Step 2: Create engine and get diagnosis
    print("\n" + "=" * 70)
    print("  STEP 2: DIAGNOSIS")
    print("=" * 70)
    
    engine = AutopoiesisEngine(target_path, dry_run=True)
    diagnosis = engine.diagnose()
    
    print(f"\n  Phase: {diagnosis['phase'].upper()}")
    print(f"  Is Autopoietic: {'Yes!' if diagnosis['is_autopoietic'] else 'Not yet'}")
    print(f"  Harmony: {diagnosis['harmony']:.3f}")
    print(f"  Priority Dimension: {diagnosis['priority_dimension']}")
    print(f"  Distance to Autopoiesis: {diagnosis['distance_to_autopoiesis']:.3f}")
    
    print("\n  LJPW Scores:")
    for dim, score in diagnosis['ljpw'].items():
        status = "[Y]" if score >= 0.7 else "[N]"
        print(f"    {dim}: {score:.3f} {status}")
    
    print("\n  Recommendations:")
    for rec in diagnosis['recommendations']:
        print(f"    - {rec}")
    
    # Step 3: Show what breathing would do (dry run)
    print("\n" + "=" * 70)
    print("  STEP 3: BREATHING SIMULATION (DRY RUN)")
    print("=" * 70)
    
    print("\n  Running 4 breathing cycles (L->J->P->W) in dry-run mode...")
    session = engine.breathe(cycles=4)
    
    print(f"\n  Session Summary:")
    print(f"    Cycles: {session.cycles_completed}")
    print(f"    Initial Harmony: {session.initial_harmony:.3f}")
    print(f"    Final Harmony: {session.final_harmony:.3f}")
    
    # Final status
    print("\n" + "=" * 70)
    print("  FINAL STATUS")
    print("=" * 70)
    print(engine.status())
    
    print("\n  [OK] Autopoiesis engine test complete!")
    print("  The package has been analyzed for LJPW dimensions.")
    print("  Run without dry_run=True to apply actual healing modifications.\n")


if __name__ == "__main__":
    main()
