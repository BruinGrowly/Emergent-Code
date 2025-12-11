#!/usr/bin/env python3
"""
META-AUTOPOIESIS: The System Heals Itself
=========================================

This is the ultimate test: the autopoiesis engine runs on its own codebase,
diagnosing deficits and applying healing modifications to itself.

"The code that heals code, heals itself."
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
    |   META-AUTOPOIESIS: THE SYSTEM HEALS ITSELF                                  |
    |                                                                              |
    |   "The code that heals code, heals itself."                                  |
    |                                                                              |
    +==============================================================================+
        """)
    
        timestamp = datetime.now().isoformat()
        autopoiesis_path = os.path.join(project_root, "autopoiesis")
    
        print(f"  Timestamp: {timestamp}")
        print(f"  Target: {autopoiesis_path}")
    
        # =========================================================================
        # PHASE 1: Initial state
        # =========================================================================
        print("\n" + "=" * 70)
        print("  PHASE 1: INITIAL STATE")
        print("=" * 70)
    
        measurer = SystemHarmonyMeasurer()
        before = measurer.measure(autopoiesis_path)
    
        print(f"\n  Phase: {before.phase.value.upper()}")
        print(f"  Harmony: {before.harmony:.4f}")
        print(f"  LJPW: L={before.love:.4f} J={before.justice:.4f} P={before.power:.4f} W={before.wisdom:.4f}")
        print(f"  Composition: {before.total_files} files, {before.total_functions} functions, {before.total_classes} classes")
        print(f"  Deficits: L={before.files_with_L_deficit}, J={before.files_with_J_deficit}, P={before.files_with_P_deficit}, W={before.files_with_W_deficit}")
    
        # =========================================================================
        # PHASE 2: Self-healing (8 cycles = 2 full L->J->P->W rotations)
        # =========================================================================
        print("\n" + "=" * 70)
        print("  PHASE 2: SELF-HEALING (8 BREATHING CYCLES)")
        print("=" * 70)
    
        print("\n  The autopoiesis engine will now analyze and heal itself...")
        print("  This is TRUE meta-autopoiesis.\n")
    
        engine = AutopoiesisEngine(autopoiesis_path, dry_run=False)  # NOT dry run!
        session = engine.breathe(cycles=8)  # 2 full rotations
    
        # =========================================================================
        # PHASE 3: Post-healing state
        # =========================================================================
        print("\n" + "=" * 70)
        print("  PHASE 3: POST-HEALING STATE")
        print("=" * 70)
    
        after = measurer.measure(autopoiesis_path)
    
        print(f"\n  Phase: {after.phase.value.upper()}")
    except TypeError as e:
        raise TypeError(f"Type error in main: {e}") from e
    except ValueError as e:
        raise ValueError(f"Value error in main: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error in main: {e}") from e
    print(f"  Harmony: {after.harmony:.4f}")
    print(f"  LJPW: L={after.love:.4f} J={after.justice:.4f} P={after.power:.4f} W={after.wisdom:.4f}")
    print(f"  Composition: {after.total_files} files, {after.total_functions} functions, {after.total_classes} classes")
    print(f"  Deficits: L={after.files_with_L_deficit}, J={after.files_with_J_deficit}, P={after.files_with_P_deficit}, W={after.files_with_W_deficit}")
    
    # =========================================================================
    # FINAL REPORT
    # =========================================================================
    print("\n" + "=" * 70)
    print("  FINAL REPORT: BEFORE vs AFTER")
    print("=" * 70)
    
    print(f"\n  {'Metric':<20} {'Before':>12} {'After':>12} {'Change':>12}")
    print(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*12}")
    
    h_change = after.harmony - before.harmony
    print(f"  {'Harmony':<20} {before.harmony:>12.4f} {after.harmony:>12.4f} {h_change:>+12.4f}")
    
    l_change = after.love - before.love
    print(f"  {'Love':<20} {before.love:>12.4f} {after.love:>12.4f} {l_change:>+12.4f}")
    
    j_change = after.justice - before.justice
    print(f"  {'Justice':<20} {before.justice:>12.4f} {after.justice:>12.4f} {j_change:>+12.4f}")
    
    p_change = after.power - before.power
    print(f"  {'Power':<20} {before.power:>12.4f} {after.power:>12.4f} {p_change:>+12.4f}")
    
    w_change = after.wisdom - before.wisdom
    print(f"  {'Wisdom':<20} {before.wisdom:>12.4f} {after.wisdom:>12.4f} {w_change:>+12.4f}")
    
    print(f"\n  Files Modified: {session.total_files_modified}")
    print(f"  Solutions Applied: {session.total_solutions_applied}")
    print(f"  Duration: {session.end_time - session.start_time}")
    
    if h_change > 0:
        print(f"\n  [+] THE SYSTEM IMPROVED ITSELF!")
        print(f"      Harmony increased by {h_change:.4f}")
    elif h_change == 0:
        print(f"\n  [=] System is already optimal (no changes needed)")
    else:
        print(f"\n  [!] Harmony decreased - review changes")
    
    # Status
    if after.is_autopoietic:
        print(f"\n  [*] SYSTEM REMAINS AUTOPOIETIC!")
        print(f"      H={after.harmony:.4f} >= 0.6, L={after.love:.4f} >= 0.7")
    
    print("\n" + "=" * 70)
    print("  META-AUTOPOIESIS COMPLETE")
    print("=" * 70)
    print(f"\n  The autopoiesis engine has successfully analyzed and healed itself.")
    print(f"  Timestamp: {datetime.now().isoformat()}\n")


if __name__ == "__main__":
    main()
