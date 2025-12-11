#!/usr/bin/env python3
"""
Test Intent-to-Module: Growing an NBFI ERP from Natural Language
================================================================

This demonstrates the core vision: users express business intent,
and the system grows self-healing modules.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from autopoiesis.grower import IntentToModuleGenerator, grow


def main():
    print("""
+==============================================================================+
|                                                                              |
|   INTENT-TO-MODULE: GROWING AN NBFI ERP FROM NATURAL LANGUAGE                |
|                                                                              |
|   Users express business intent. The system grows self-healing code.         |
|                                                                              |
+==============================================================================+
    """)
    
    # Create output directory for the ERP modules
    erp_dir = os.path.join(project_root, "erp_nbfi")
    os.makedirs(erp_dir, exist_ok=True)
    
    print(f"  Output directory: {erp_dir}")
    
    # Create generator
    generator = IntentToModuleGenerator(erp_dir)
    
    # =========================================================================
    # GROW MODULES FROM BUSINESS INTENTS
    # =========================================================================
    
    intents = [
        "Create a loan application and approval tracking system",
        "Build customer account management with deposits and withdrawals",
        "Implement payment processing between accounts",
    ]
    
    results = []
    
    for i, intent in enumerate(intents, 1):
        print(f"\n{'#'*70}")
        print(f"  MODULE {i}/{len(intents)}")
        print(f"{'#'*70}")
        
        module = generator.grow(intent, auto_heal=True)
        results.append(module)
    
    # =========================================================================
    # SUMMARY
    # =========================================================================
    
    print("\n" + "=" * 70)
    print("  SUMMARY: GENERATED ERP MODULES")
    print("=" * 70)
    
    print(f"\n  {'Module':<30} {'Entities':<20} {'Harmony':>10}")
    print(f"  {'-'*30} {'-'*20} {'-'*10}")
    
    for module in results:
        entities = ', '.join(module.entities[:2])
        print(f"  {os.path.basename(module.path):<30} {entities:<20} {module.harmony_score:>10.3f}")
    
    # Overall statistics
    total_entities = sum(len(m.entities) for m in results)
    avg_harmony = sum(m.harmony_score for m in results) / len(results) if results else 0
    
    print(f"\n  Total modules: {len(results)}")
    print(f"  Total entities: {total_entities}")
    print(f"  Average harmony: {avg_harmony:.3f}")
    
    # Show generated files
    print(f"\n  Generated files:")
    for f in os.listdir(erp_dir):
        if f.endswith('.py'):
            size = os.path.getsize(os.path.join(erp_dir, f))
            print(f"    - {f} ({size} bytes)")
    
    print("\n" + "=" * 70)
    print("  ERP MODULES GROWN SUCCESSFULLY")
    print("=" * 70)
    
    print(f"""
  The system has grown {len(results)} self-healing modules from natural language.
  Each module includes:
    - Comprehensive documentation (Love)
    - Input validation (Justice)
    - Error handling (Power)
    - Logging infrastructure (Wisdom)
  
  These modules can now:
    - Heal themselves via autopoiesis
    - Be extended through more natural language
    - Maintain their own integrity
    """)


if __name__ == "__main__":
    main()
