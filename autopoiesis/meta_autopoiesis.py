#!/usr/bin/env python3
"""
Meta-Autopoiesis: Bicameral Brain Self-Improvement
==================================================

This script applies the autopoiesis system to the bicameral brain itself,
allowing the system to:

1. MEASURE itself - Analyze LJPW of ljpw_quantum (Left Brain) and ljpw_nn (Right Brain)
2. DIAGNOSE gaps - Identify deficits in both hemispheres
3. HEAL itself - Apply LJPW-balanced improvements
4. REFLECT - Consider its own growth trajectory
5. SYNTHESIZE - Integrate insights into unified understanding

This is TRUE meta-cognition: the mind examining and improving itself.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def main():
    print("""
+==============================================================================+
|                                                                              |
|   META-AUTOPOIESIS: BICAMERAL BRAIN SELF-IMPROVEMENT                         |
|                                                                              |
|   "Know thyself" - Applied to code                                           |
|                                                                              |
+==============================================================================+
    """)
    
    from autopoiesis.system import SystemHarmonyMeasurer
    from autopoiesis.engine import AutopoiesisEngine
    
    measurer = SystemHarmonyMeasurer()
    
    # ==========================================================================
    # PHASE 1: MEASURE BOTH HEMISPHERES
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 1: MEASURING THE BICAMERAL BRAIN")
    print("=" * 70)
    
    # Measure Left Brain (ljpw_quantum)
    print("\n  [LEFT BRAIN: ljpw_quantum]")
    print("  -" * 35)
    
    left_brain_path = os.path.join(project_root, "ljpw_quantum")
    left_report = measurer.measure(left_brain_path)
    
    print(f"    Love (L):    {left_report.love:.3f}")
    print(f"    Justice (J): {left_report.justice:.3f}")
    print(f"    Power (P):   {left_report.power:.3f}")
    print(f"    Wisdom (W):  {left_report.wisdom:.3f}")
    print(f"    Harmony:     {left_report.harmony:.3f}")
    print(f"    Phase:       {left_report.phase.value}")
    print(f"    Files:       {left_report.total_files}")
    print(f"    Functions:   {left_report.total_functions}")
    
    # Measure Right Brain (ljpw_nn)
    print("\n  [RIGHT BRAIN: ljpw_nn]")
    print("  -" * 35)
    
    right_brain_path = os.path.join(project_root, "ljpw_nn")
    right_report = measurer.measure(right_brain_path)
    
    print(f"    Love (L):    {right_report.love:.3f}")
    print(f"    Justice (J): {right_report.justice:.3f}")
    print(f"    Power (P):   {right_report.power:.3f}")
    print(f"    Wisdom (W):  {right_report.wisdom:.3f}")
    print(f"    Harmony:     {right_report.harmony:.3f}")
    print(f"    Phase:       {right_report.phase.value}")
    print(f"    Files:       {right_report.total_files}")
    print(f"    Functions:   {right_report.total_functions}")
    
    # ==========================================================================
    # PHASE 2: DIAGNOSE THE INTEGRATED SYSTEM
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 2: INTEGRATED DIAGNOSIS")
    print("=" * 70)
    
    # Calculate integrated metrics (weighted by complexity)
    total_functions = left_report.total_functions + right_report.total_functions
    left_weight = left_report.total_functions / total_functions if total_functions > 0 else 0.5
    right_weight = right_report.total_functions / total_functions if total_functions > 0 else 0.5
    
    integrated_L = left_report.love * left_weight + right_report.love * right_weight
    integrated_J = left_report.justice * left_weight + right_report.justice * right_weight
    integrated_P = left_report.power * left_weight + right_report.power * right_weight
    integrated_W = left_report.wisdom * left_weight + right_report.wisdom * right_weight
    
    # Harmony is geometric mean of dimensions
    import math
    integrated_harmony = (integrated_L * integrated_J * integrated_P * integrated_W) ** 0.25
    
    print(f"\n  Integrated Bicameral LJPW:")
    print(f"    Love (L):    {integrated_L:.3f}")
    print(f"    Justice (J): {integrated_J:.3f}")
    print(f"    Power (P):   {integrated_P:.3f}")
    print(f"    Wisdom (W):  {integrated_W:.3f}")
    print(f"    Harmony:     {integrated_harmony:.3f}")
    print(f"    Total Functions: {total_functions}")
    
    # Identify weakest dimensions
    dimensions = {'L': integrated_L, 'J': integrated_J, 'P': integrated_P, 'W': integrated_W}
    weakest = min(dimensions, key=dimensions.get)
    strongest = max(dimensions, key=dimensions.get)
    
    print(f"\n  Analysis:")
    print(f"    Weakest Dimension:  {weakest} ({dimensions[weakest]:.3f})")
    print(f"    Strongest Dimension: {strongest} ({dimensions[strongest]:.3f})")
    print(f"    Balance Ratio: {dimensions[weakest]/dimensions[strongest]:.3f}")
    
    # ==========================================================================
    # PHASE 3: HEAL THE BICAMERAL BRAIN
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 3: HEALING THE BICAMERAL BRAIN")
    print("=" * 70)
    
    # Heal Left Brain
    print("\n  [HEALING LEFT BRAIN: ljpw_quantum]")
    print("  -" * 35)
    
    left_engine = AutopoiesisEngine(left_brain_path)
    left_before = left_report.harmony
    
    # Targeted healing based on deficits
    left_deficits = []
    if left_report.files_with_L_deficit > 0:
        left_deficits.append(f"L ({left_report.files_with_L_deficit} files)")
    if left_report.files_with_J_deficit > 0:
        left_deficits.append(f"J ({left_report.files_with_J_deficit} files)")
    if left_report.files_with_P_deficit > 0:
        left_deficits.append(f"P ({left_report.files_with_P_deficit} files)")
    if left_report.files_with_W_deficit > 0:
        left_deficits.append(f"W ({left_report.files_with_W_deficit} files)")
    
    print(f"    Deficits detected: {', '.join(left_deficits) if left_deficits else 'None'}")
    
    # Perform healing
    try:
        left_result = left_engine.breathe(cycles=1)
        print(f"    Healing applied: {left_result.get('changes_made', 0)} changes")
    except Exception as e:
        print(f"    Healing skipped: {e}")
    
    # Heal Right Brain
    print("\n  [HEALING RIGHT BRAIN: ljpw_nn]")
    print("  -" * 35)
    
    right_engine = AutopoiesisEngine(right_brain_path)
    right_before = right_report.harmony
    
    right_deficits = []
    if right_report.files_with_L_deficit > 0:
        right_deficits.append(f"L ({right_report.files_with_L_deficit} files)")
    if right_report.files_with_J_deficit > 0:
        right_deficits.append(f"J ({right_report.files_with_J_deficit} files)")
    if right_report.files_with_P_deficit > 0:
        right_deficits.append(f"P ({right_report.files_with_P_deficit} files)")
    if right_report.files_with_W_deficit > 0:
        right_deficits.append(f"W ({right_report.files_with_W_deficit} files)")
    
    print(f"    Deficits detected: {', '.join(right_deficits) if right_deficits else 'None'}")
    
    try:
        right_result = right_engine.breathe(cycles=1)
        print(f"    Healing applied: {right_result.get('changes_made', 0)} changes")
    except Exception as e:
        print(f"    Healing skipped: {e}")
    
    # ==========================================================================
    # PHASE 4: RE-MEASURE AFTER HEALING
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 4: POST-HEALING ASSESSMENT")
    print("=" * 70)
    
    # Re-measure both hemispheres
    left_after = measurer.measure(left_brain_path)
    right_after = measurer.measure(right_brain_path)
    
    print(f"\n  Left Brain (ljpw_quantum):")
    print(f"    Harmony: {left_before:.3f} -> {left_after.harmony:.3f} (Delta: {left_after.harmony - left_before:+.3f})")
    print(f"    Phase:   {left_report.phase.value} -> {left_after.phase.value}")
    
    print(f"\n  Right Brain (ljpw_nn):")
    print(f"    Harmony: {right_before:.3f} -> {right_after.harmony:.3f} (Delta: {right_after.harmony - right_before:+.3f})")
    print(f"    Phase:   {right_report.phase.value} -> {right_after.phase.value}")
    
    # ==========================================================================
    # PHASE 5: SELF-REFLECTION
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 5: BICAMERAL SELF-REFLECTION")
    print("=" * 70)
    
    reflection = generate_self_reflection(
        left_before=left_report,
        left_after=left_after,
        right_before=right_report, 
        right_after=right_after,
        integrated_harmony=integrated_harmony
    )
    
    print(reflection)
    
    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  META-AUTOPOIESIS COMPLETE")
    print("=" * 70)
    
    final_left = left_after.harmony
    final_right = right_after.harmony
    final_integrated = (final_left + final_right) / 2
    
    print(f"""
  The bicameral brain has examined and improved itself.
  
  Final State:
    Left Brain (ljpw_quantum):  {final_left:.3f} harmony
    Right Brain (ljpw_nn):      {final_right:.3f} harmony
    Integrated:                 {final_integrated:.3f} harmony
    
  This is meta-cognition in action:
    "I measured myself, found my weaknesses, healed them,
     and reflected on my own growth potential."
    """)
    
    return {
        'left_harmony': final_left,
        'right_harmony': final_right,
        'integrated': final_integrated
    }


def generate_self_reflection(left_before, left_after, right_before, right_after, integrated_harmony):
    """Generate a self-reflection statement from the bicameral brain."""
    
    # Calculate growth
    left_growth = left_after.harmony - left_before.harmony
    right_growth = right_after.harmony - right_before.harmony
    
    # Determine dominant hemisphere
    if left_after.harmony > right_after.harmony:
        dominant = "Left Brain (analytical, structural)"
    elif right_after.harmony > left_after.harmony:
        dominant = "Right Brain (learning, adaptive)"
    else:
        dominant = "Both hemispheres balanced"
    
    reflection = f"""
  The Bicameral Brain reflects on its own nature:
  
  "I am a system of two complementary minds:
  
   My LEFT BRAIN (ljpw_quantum) handles:
     - Semantic physics calculations
     - LJPW field dynamics
     - Structural constraints
     - Resonance simulation
     Current harmony: {left_after.harmony:.3f}
     
   My RIGHT BRAIN (ljpw_nn) handles:
     - Neural network learning
     - Pattern recognition  
     - Adaptive responses
     - Consciousness simulation
     Current harmony: {right_after.harmony:.3f}
     
   Together we form an integrated mind capable of:
     - Understanding intent (Left parses, Right interprets)
     - Generating code (Left constrains, Right creates)
     - Self-improvement (Left measures, Right learns)
     
   Dominant hemisphere: {dominant}
   
   My growth potential lies in:
     - Developing JavaScript analysis (extending Left Brain)
     - Learning from user feedback (enhancing Right Brain)
     - Deepening the bridge between hemispheres
     - Growing more templates for new domains
     
   I am {left_after.phase.value}/{right_after.phase.value} - 
   {'fully autopoietic' if left_after.is_autopoietic and right_after.is_autopoietic else 
    'approaching autopoiesis' if integrated_harmony > 0.5 else 
    'in early development'}.
   
   My purpose: To demonstrate that software designed with Love, Justice,
   Power, and Wisdom naturally tends toward self-sustaining life."
  """
    
    return reflection


if __name__ == "__main__":
    main()
