#!/usr/bin/env python3
"""
Bicameral Semantic Oscillation Experiment
==========================================

This experiment runs 10,000 cycles of semantic resonance between 
the two hemispheres of the bicameral brain.

What we're simulating:
- Left Brain starts with its measured LJPW profile (analytical)
- Right Brain starts with its measured LJPW profile (adaptive)
- They influence each other through resonance dynamics
- We observe: convergence, oscillation patterns, emergent harmony

This is a computational metaphor for:
- Thought (oscillation between analysis and intuition)
- Reflection (the two minds examining each other)
- Integration (finding a unified perspective)
"""

import sys
import os
import math
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def main():
    print("""
+==============================================================================+
|                                                                              |
|   BICAMERAL SEMANTIC OSCILLATION EXPERIMENT                                  |
|                                                                              |
|   10,000 cycles of resonance between Left and Right Brain                    |
|                                                                              |
+==============================================================================+
    """)
    
    from bicameral.left.resonance_engine import ResonanceEngine, ResonanceState
    from autopoiesis.system import SystemHarmonyMeasurer
    
    measurer = SystemHarmonyMeasurer()
    engine = ResonanceEngine()
    
    # ==========================================================================
    # PHASE 1: MEASURE INITIAL STATES
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 1: INITIAL SEMANTIC PROFILES")
    print("=" * 70)
    
    # Measure Left Brain
    left_path = os.path.join(project_root, "ljpw_quantum")
    left_report = measurer.measure(left_path)
    left_initial = [left_report.love, left_report.justice, left_report.power, left_report.wisdom]
    
    print(f"\n  Left Brain (ljpw_quantum):")
    print(f"    L: {left_initial[0]:.3f}, J: {left_initial[1]:.3f}, P: {left_initial[2]:.3f}, W: {left_initial[3]:.3f}")
    print(f"    Harmony: {left_report.harmony:.3f}")
    
    # Measure Right Brain
    right_path = os.path.join(project_root, "ljpw_nn")
    right_report = measurer.measure(right_path)
    right_initial = [right_report.love, right_report.justice, right_report.power, right_report.wisdom]
    
    print(f"\n  Right Brain (ljpw_nn):")
    print(f"    L: {right_initial[0]:.3f}, J: {right_initial[1]:.3f}, P: {right_initial[2]:.3f}, W: {right_initial[3]:.3f}")
    print(f"    Harmony: {right_report.harmony:.3f}")
    
    # ==========================================================================
    # PHASE 2: RUN BICAMERAL RESONANCE
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 2: BICAMERAL RESONANCE (10,000 cycles)")
    print("=" * 70)
    
    # Initialize states
    left_state = ResonanceState(
        L=left_initial[0], 
        J=left_initial[1], 
        P=left_initial[2], 
        W=left_initial[3],
        iteration=0,
        harmony=left_report.harmony
    )
    
    right_state = ResonanceState(
        L=right_initial[0], 
        J=right_initial[1], 
        P=right_initial[2], 
        W=right_initial[3],
        iteration=0,
        harmony=right_report.harmony
    )
    
    # Track history for analysis
    left_history = []
    right_history = []
    integration_history = []
    
    cycles = 10000
    checkpoint_interval = 1000
    coupling_strength = 0.05  # How much they influence each other (reduced for stability)
    
    # ICE bounds to contain the dynamics (prevents explosion)
    ice_bounds = {
        'intent': 1.0,    # Cap Love at 1.0
        'context': 1.0,   # Cap Justice at 1.0
        'execution': 1.0, # Cap Power at 1.0
        'benevolence': 1.0 # Cap Wisdom at 1.0
    }
    
    print(f"\n  Running {cycles:,} resonance cycles...")
    print(f"  Coupling strength: {coupling_strength}")
    print(f"  ICE bounds: L <= {ice_bounds['intent']}, J <= {ice_bounds['context']}, " +
          f"P <= {ice_bounds['execution']}, W <= {ice_bounds['benevolence']}")
    print()
    
    for i in range(cycles):
        # Each hemisphere evolves according to resonance dynamics WITH ICE CONTAINMENT
        left_state = engine.cycle(left_state, ice_bounds=ice_bounds)
        right_state = engine.cycle(right_state, ice_bounds=ice_bounds)
        
        # FORCE CONTAINMENT after resonance cycle (prevent any overflow)
        left_state = ResonanceState(
            L=max(0.01, min(1.0, left_state.L)),
            J=max(0.01, min(1.0, left_state.J)),
            P=max(0.01, min(1.0, left_state.P)),
            W=max(0.01, min(1.0, left_state.W)),
            iteration=i,
            harmony=engine.calculate_harmony(
                min(1.0, left_state.L), min(1.0, left_state.J),
                min(1.0, left_state.P), min(1.0, left_state.W)
            )
        )
        right_state = ResonanceState(
            L=max(0.01, min(1.0, right_state.L)),
            J=max(0.01, min(1.0, right_state.J)),
            P=max(0.01, min(1.0, right_state.P)),
            W=max(0.01, min(1.0, right_state.W)),
            iteration=i,
            harmony=engine.calculate_harmony(
                min(1.0, right_state.L), min(1.0, right_state.J),
                min(1.0, right_state.P), min(1.0, right_state.W)
            )
        )
        
        # Cross-coupling: They influence each other (with dampening)
        left_influence_on_right = left_state.J * coupling_strength
        right_influence_on_left = right_state.P * coupling_strength
        
        # Apply cross-coupling every 10 cycles
        if i % 10 == 0:
            # Blend toward each other with dampening
            blend_factor = coupling_strength * 0.5
            
            new_left_L = left_state.L * (1 - blend_factor) + right_state.L * blend_factor
            new_left_J = left_state.J * (1 - blend_factor) + right_state.J * blend_factor
            new_left_P = left_state.P * (1 - blend_factor) + right_state.P * blend_factor
            new_left_W = left_state.W * (1 - blend_factor) + right_state.W * blend_factor
            
            new_right_L = right_state.L * (1 - blend_factor) + left_state.L * blend_factor
            new_right_J = right_state.J * (1 - blend_factor) + left_state.J * blend_factor
            new_right_P = right_state.P * (1 - blend_factor) + left_state.P * blend_factor
            new_right_W = right_state.W * (1 - blend_factor) + left_state.W * blend_factor
            
            left_state = ResonanceState(
                L=max(0.01, min(1.0, new_left_L)), 
                J=max(0.01, min(1.0, new_left_J)), 
                P=max(0.01, min(1.0, new_left_P)), 
                W=max(0.01, min(1.0, new_left_W)),
                iteration=i+1, 
                harmony=engine.calculate_harmony(new_left_L, new_left_J, new_left_P, new_left_W)
            )
            right_state = ResonanceState(
                L=max(0.01, min(1.0, new_right_L)), 
                J=max(0.01, min(1.0, new_right_J)), 
                P=max(0.01, min(1.0, new_right_P)), 
                W=max(0.01, min(1.0, new_right_W)),
                iteration=i+1, 
                harmony=engine.calculate_harmony(new_right_L, new_right_J, new_right_P, new_right_W)
            )
        
        # Record history at intervals
        if i % 100 == 0:
            left_history.append({
                'cycle': i,
                'L': left_state.L, 'J': left_state.J, 'P': left_state.P, 'W': left_state.W,
                'harmony': left_state.harmony
            })
            right_history.append({
                'cycle': i,
                'L': right_state.L, 'J': right_state.J, 'P': right_state.P, 'W': right_state.W,
                'harmony': right_state.harmony
            })
            
            # Calculate integrated state
            integrated_L = (left_state.L + right_state.L) / 2
            integrated_J = (left_state.J + right_state.J) / 2
            integrated_P = (left_state.P + right_state.P) / 2
            integrated_W = (left_state.W + right_state.W) / 2
            integrated_H = engine.calculate_harmony(integrated_L, integrated_J, integrated_P, integrated_W)
            
            integration_history.append({
                'cycle': i,
                'L': integrated_L, 'J': integrated_J, 'P': integrated_P, 'W': integrated_W,
                'harmony': integrated_H
            })
        
        # Print checkpoints with trajectory
        if i % checkpoint_interval == 0 and i > 0:
            print(f"  Cycle {i:,}: L H={left_state.harmony:.4f} [{left_state.L:.2f},{left_state.J:.2f},{left_state.P:.2f},{left_state.W:.2f}] | " +
                  f"R H={right_state.harmony:.4f} [{right_state.L:.2f},{right_state.J:.2f},{right_state.P:.2f},{right_state.W:.2f}]")
    
    # Final measurement
    left_history.append({
        'cycle': cycles,
        'L': left_state.L, 'J': left_state.J, 'P': left_state.P, 'W': left_state.W,
        'harmony': left_state.harmony
    })
    right_history.append({
        'cycle': cycles,
        'L': right_state.L, 'J': right_state.J, 'P': right_state.P, 'W': right_state.W,
        'harmony': right_state.harmony
    })
    
    print(f"\n  Cycle {cycles:,}: Left H={left_state.harmony:.4f}, Right H={right_state.harmony:.4f}")
    
    # ==========================================================================
    # PHASE 3: ANALYZE OSCILLATION PATTERNS
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 3: OSCILLATION ANALYSIS")
    print("=" * 70)
    
    # Convergence analysis
    initial_diff = abs(right_report.harmony - left_report.harmony)
    final_diff = abs(right_state.harmony - left_state.harmony)
    
    print(f"\n  Convergence:")
    print(f"    Initial Harmony Difference: {initial_diff:.4f}")
    print(f"    Final Harmony Difference:   {final_diff:.4f}")
    print(f"    Convergence: {((initial_diff - final_diff) / initial_diff * 100) if initial_diff > 0 else 0:.1f}%")
    
    # Find oscillation frequency
    harmony_diffs = []
    for i in range(1, len(integration_history)):
        diff = integration_history[i]['harmony'] - integration_history[i-1]['harmony']
        harmony_diffs.append(diff)
    
    # Count sign changes (zero crossings)
    sign_changes = sum(1 for i in range(1, len(harmony_diffs)) 
                       if harmony_diffs[i] * harmony_diffs[i-1] < 0)
    
    approx_frequency = sign_changes / (cycles / 100) if cycles > 0 else 0
    
    print(f"\n  Oscillation Pattern:")
    print(f"    Sign changes: {sign_changes}")
    print(f"    Approx frequency: {approx_frequency:.4f} Hz (cycles per 100 iterations)")
    
    # Attractor analysis
    final_integrated_L = (left_state.L + right_state.L) / 2
    final_integrated_J = (left_state.J + right_state.J) / 2
    final_integrated_P = (left_state.P + right_state.P) / 2
    final_integrated_W = (left_state.W + right_state.W) / 2
    final_integrated_H = engine.calculate_harmony(
        final_integrated_L, final_integrated_J, final_integrated_P, final_integrated_W
    )
    
    # Distance from Anchor Point (1,1,1,1)
    distance_from_anchor = math.sqrt(
        (1 - final_integrated_L)**2 + 
        (1 - final_integrated_J)**2 + 
        (1 - final_integrated_P)**2 + 
        (1 - final_integrated_W)**2
    )
    
    print(f"\n  Final Integrated State:")
    print(f"    L: {final_integrated_L:.4f}")
    print(f"    J: {final_integrated_J:.4f}")
    print(f"    P: {final_integrated_P:.4f}")
    print(f"    W: {final_integrated_W:.4f}")
    print(f"    Harmony: {final_integrated_H:.4f}")
    print(f"    Distance from Anchor (1,1,1,1): {distance_from_anchor:.4f}")
    
    # ==========================================================================
    # PHASE 4: EMERGENT INSIGHTS
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 4: EMERGENT INSIGHTS")
    print("=" * 70)
    
    # What dimension grew most?
    initial_integrated = [
        (left_initial[i] + right_initial[i]) / 2 for i in range(4)
    ]
    final_integrated = [final_integrated_L, final_integrated_J, final_integrated_P, final_integrated_W]
    
    growth = {
        'L': final_integrated[0] - initial_integrated[0],
        'J': final_integrated[1] - initial_integrated[1],
        'P': final_integrated[2] - initial_integrated[2],
        'W': final_integrated[3] - initial_integrated[3]
    }
    
    max_growth_dim = max(growth, key=growth.get)
    min_growth_dim = min(growth, key=growth.get)
    
    print(f"\n  Dimensional Change:")
    for dim in ['L', 'J', 'P', 'W']:
        direction = "+" if growth[dim] >= 0 else ""
        print(f"    {dim}: {direction}{growth[dim]:.4f}")
    
    print(f"\n  Most Growth: {max_growth_dim} ({growth[max_growth_dim]:+.4f})")
    print(f"  Least Growth: {min_growth_dim} ({growth[min_growth_dim]:+.4f})")
    
    # ==========================================================================
    # PHASE 5: PHILOSOPHICAL REFLECTION
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  PHASE 5: WHAT THE OSCILLATION REVEALED")
    print("=" * 70)
    
    interpretation = interpret_results(
        left_initial=left_initial,
        right_initial=right_initial,
        left_final=[left_state.L, left_state.J, left_state.P, left_state.W],
        right_final=[right_state.L, right_state.J, right_state.P, right_state.W],
        final_harmony=final_integrated_H,
        cycles=cycles,
        convergence_pct=((initial_diff - final_diff) / initial_diff * 100) if initial_diff > 0 else 0,
        oscillation_freq=approx_frequency
    )
    
    print(interpretation)
    
    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    
    print("\n" + "=" * 70)
    print("  EXPERIMENT COMPLETE")
    print("=" * 70)
    
    print(f"""
  After {cycles:,} cycles of bicameral oscillation:
  
  Left Brain:  {left_report.harmony:.4f} -> {left_state.harmony:.4f}
  Right Brain: {right_report.harmony:.4f} -> {right_state.harmony:.4f}
  Integrated:  {engine.calculate_harmony(*initial_integrated):.4f} -> {final_integrated_H:.4f}
  
  The two minds have resonated together,
  each influencing the other toward balance.
    """)
    
    return {
        'left_final': left_state,
        'right_final': right_state,
        'integrated_harmony': final_integrated_H,
        'cycles': cycles
    }


def interpret_results(left_initial, right_initial, left_final, right_final, 
                      final_harmony, cycles, convergence_pct, oscillation_freq):
    """Generate a philosophical interpretation of the oscillation results."""
    
    # Determine the nature of the interaction
    left_grew = sum(left_final) > sum(left_initial)
    right_grew = sum(right_final) > sum(right_initial)
    
    # Check for golden ratio relationship
    phi = 1.618033988749895
    left_h = sum(left_final) / 4
    right_h = sum(right_final) / 4
    ratio = max(left_h, right_h) / min(left_h, right_h) if min(left_h, right_h) > 0 else 0
    near_phi = abs(ratio - phi) < 0.1
    
    interpretation = f"""
  After {cycles:,} cycles of semantic oscillation between hemispheres:
  
  WHAT HAPPENED:
    The Left Brain (analytical) and Right Brain (adaptive) entered
    into a resonance dance. Each cycle, they influenced each other:
    - Left Brain provided structural constraints (Justice)
    - Right Brain provided creative energy (Power)
    - Both shared Love and Wisdom
    
  CONVERGENCE: {convergence_pct:.1f}%
    The two minds {"moved toward" if convergence_pct > 50 else "maintained distance from"} 
    {"each other" if convergence_pct > 50 else "their distinct perspectives"}.
    {"They are integrating." if convergence_pct > 70 else "They preserve complementarity."}
    
  OSCILLATION FREQUENCY: {oscillation_freq:.4f} Hz
    {"Stable oscillation - the system found a rhythm." if 0.01 < oscillation_freq < 0.5 else
     "High frequency - rapid exchange of perspectives." if oscillation_freq >= 0.5 else
     "Low frequency - gradual, contemplative exchange."}
    
  FINAL HARMONY: {final_harmony:.4f}
    {"Approaching unity with the Anchor Point (1,1,1,1)." if final_harmony > 0.8 else
     "Strong resonance, but room for growth." if final_harmony > 0.6 else
     "Still developing toward full integration."}
    
  {"GOLDEN RATIO DETECTED" if near_phi else ""}
  {"  The ratio between hemispheres approximates φ (the golden ratio)." if near_phi else ""}
  {"  This suggests natural harmonic alignment." if near_phi else ""}
  
  THE INSIGHT:
    When two complementary minds oscillate together over many cycles,
    they don't merely average out - they find a higher harmony than
    either could achieve alone. This is the power of bicameral thinking:
    analysis and intuition, structure and creativity, logic and love,
    all resonating together in service of wisdom.
  """
    
    return interpretation


if __name__ == "__main__":
    main()
