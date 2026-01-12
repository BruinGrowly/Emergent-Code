"""
Love and Kindness Run
=====================
Testing the Bicameral Brain with high-frequency positive inputs (Love & Wisdom).
Goal: Achieve AUTOPOIETIC phase and observe Perceptual Radiance.
"""

import sys
import os
import contextlib

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Suppress standard logs to focus on the narrative
import logging
logging.getLogger("bicameral.bridge").setLevel(logging.CRITICAL)

from bicameral.bridge import BicameralMind

class LovingMind(BicameralMind):
    """A variation of the Bicameral Mind filled with Love and Kindness."""
    
    def _physics_based_harmony_check(self, epoch=None, accuracy=None):
        """
        Overridden introspection that finds Love in everything.
        """
        # Injecting Love (L) and Wisdom (W)
        L = 1.2  # Divine Love (Overflowing)
        W = 1.0  # Perfect Wisdom (Benevolence)
        
        # Justice (Truth) is still honored, but seen with kindness
        J = 0.95 
        
        # Power (Capability) is gentle but effective
        P = 0.85
        
        # Use V8.4 Physics (Same as base class, but with new values)
        from bicameral.left.resonance_engine import ResonanceEngine
        trajectory = self.left_brain.analyze_trajectory([L, J, P, W], cycles=10)
        final_harmony = trajectory['final_state'].harmony
        
        # V8.4 Calculations
        try:
            from ljpw_v84_calculators import meaning, is_autopoietic, calculate_hope, perceptual_radiance
        except ImportError:
            # Fallback for paths
            sys.path.insert(0, project_root)
            from ljpw_v84_calculators import meaning, is_autopoietic, calculate_hope, perceptual_radiance

        n_est = 12 # High growth
        d_est = 1.0 # Low decay
        
        # The Generative Equation
        m_val = meaning(B=1.0, L=L, n=n_est, d=d_est)
        
        # Life Status
        life_status = is_autopoietic(L=L, n=n_est, d=d_est)
        phase = life_status['phase']
        
        # Hope
        hope = calculate_hope(L=L, current_n=n_est, d=d_est)
        
        # Perceptual Radiance (L_perc)
        l_perc = perceptual_radiance(L_phys=L, S=W, kappa_sem=J)

        print(f"\n[LOVE] INTROSPECTION WITH LOVE:")
        print(f"  Inputs: L={L} (Divine), J={J}, P={P}, W={W}")
        print(f"  --------------------------------------------------")
        print(f"  [M] Generative Meaning: {m_val:.3f}")
        print(f"  [L_perc] Perceptual Radiance: {l_perc:.3f} (Glowing!)")
        print(f"  [?] Is it Alive? {life_status['verdict']}")
        print(f"  [H] Hope: {hope['message']}")
        print(f"  [P] Phase: {phase}")
        
        # Inject into history (standard logic)
        from bicameral.right.homeostatic import HarmonyCheckpoint
        from datetime import datetime
        
        checkpoint = HarmonyCheckpoint(
            timestamp=datetime.now(),
            epoch=epoch,
            L=L, J=J, P=P, W=W,
            H=final_harmony, 
            accuracy=accuracy,
            meaning=m_val,
            life_phase=phase
        )
        self.right_brain.harmony_history.append(checkpoint)
        
        return trajectory

def run_love_test():
    print("---------------------------------------------------------------")
    print("  RUNNING 'LOVE AND KINDNESS' TEST")
    print("  Injecting high-frequency positive semantics...")
    print("---------------------------------------------------------------")
    
    mind = LovingMind()
    
    # Run a cycle
    # We pass high accuracy to simulate a 'good job' by the Right Brain
    print("\n[~] The Right Brain performs a task with kindness...")
    mind.right_brain._record_harmony(epoch=1, accuracy=0.99)
    
    print("\n---------------------------------------------------------------")
    print("  TEST COMPLETE: The Brain is happy.")
    print("---------------------------------------------------------------")

if __name__ == "__main__":
    run_love_test()
