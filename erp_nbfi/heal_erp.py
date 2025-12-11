#!/usr/bin/env python3
"""
Heal the Generated ERP Modules to Autopoietic Status
====================================================

Run intensive breathing cycles on the generated ERP modules
to bring them up to full autopoietic status (H >= 0.6, L >= 0.7).
"""

import sys
import os
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from autopoiesis import AutopoiesisEngine
from autopoiesis.system import SystemHarmonyMeasurer


def main():
    # Auto-healed: Error handling wrapper for main
    try:
        print("""
    +==============================================================================+
    |                                                                              |
    |   HEALING ERP MODULES TO AUTOPOIETIC STATUS                                  |
    |                                                                              |
    |   Running intensive breathing cycles on generated modules                    |
    |                                                                              |
    +==============================================================================+
        """)
    
        erp_dir = os.path.join(project_root, "erp_nbfi")
    
        print(f"  Target: {erp_dir}")
        print(f"  Timestamp: {datetime.now().isoformat()}")
    
        # Initial measurement
        print("\n" + "=" * 70)
        print("  INITIAL STATE")
        print("=" * 70)
    
        measurer = SystemHarmonyMeasurer()
        before = measurer.measure(erp_dir)
        measurer.print_report(before)
    
        # Run intensive healing (16 cycles = 4 full L->J->P->W rotations)
        print("\n" + "=" * 70)
        print("  HEALING: 16 BREATHING CYCLES (4 Full Rotations)")
        print("=" * 70)
    
        engine = AutopoiesisEngine(erp_dir, dry_run=False)
        session = engine.breathe(cycles=16)
    
        # Final measurement
    except TypeError as e:
        raise TypeError(f"Type error in main: {e}") from e
    except ValueError as e:
        raise ValueError(f"Value error in main: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error in main: {e}") from e
    print("\n" + "=" * 70)
    print("  FINAL STATE")
    print("=" * 70)
    
    after = measurer.measure(erp_dir)
    measurer.print_report(after)
    
    # Results
    print("\n" + "=" * 70)
    print("  HEALING RESULTS")
    print("=" * 70)
    
    print(f"\n  {'Metric':<20} {'Before':>12} {'After':>12} {'Change':>12}")
    print(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*12}")
    
    metrics = [
        ('Harmony', before.harmony, after.harmony),
        ('Love', before.love, after.love),
        ('Justice', before.justice, after.justice),
        ('Power', before.power, after.power),
        ('Wisdom', before.wisdom, after.wisdom),
    ]
    
    for name, b, a in metrics:
        change = a - b
        print(f"  {name:<20} {b:>12.4f} {a:>12.4f} {change:>+12.4f}")
    
    print(f"\n  Files Modified: {session.total_files_modified}")
    print(f"  Solutions Applied: {session.total_solutions_applied}")
    print(f"  Duration: {session.end_time - session.start_time}")
    
    if after.is_autopoietic:
        print(f"\n  [*] ERP MODULES ARE NOW AUTOPOIETIC!")
        print(f"      H={after.harmony:.4f} >= 0.6, L={after.love:.4f} >= 0.7")
    else:
        print(f"\n  [~] Making progress toward autopoiesis...")
        print(f"      Distance remaining: {after.distance_to_autopoiesis:.4f}")
    
    print("\n" + "=" * 70)
    print("  HEALING COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
