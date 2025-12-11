"""
Verify Self-Improvement: Justice Constraint Test
Target: ljpw_quantum/resonance_engine.py (The new V2 core)
Goal: Confirm that the system now REJECTS invalid physics states (Justice).
"""

import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine, ResonanceState

class TestJusticeConstraints(unittest.TestCase):
    
    def setUp(self):
        self.engine = ResonanceEngine()
        
    def test_rejects_negative_energy(self):
        """
        Physics Violation: Negative Energy.
        The old engine allowed this. The new one should throw ValueError.
        """
        print("Testing Justice Constraint: Negative Energy Rejection...")
        try:
            # Attempt to create a universe with negative Love
            # The calculation method checks this
            self.engine.calculate_harmony(-0.5, 0.5, 0.5, 0.5)
            self.fail("❌ FAILED: The engine allowed negative energy (Low Justice).")
        except ValueError as e:
            print(f"✅ SUCCESS: The engine rejected the violation: {e}")

    def test_rejects_invalid_state_object(self):
        """
        Physics Violation: Invalid State Object.
        The new engine enforces strict typing on the cycle() method.
        """
        print("Testing Justice Constraint: Type Enforcement...")
        try:
            # Pass a raw dict instead of ResonanceState object
            self.engine.cycle({"L": 0.5, "J": 0.5})
            self.fail("❌ FAILED: The engine accepted a raw dict (Low Justice).")
        except TypeError as e:
            print(f"✅ SUCCESS: The engine rejected the invalid type: {e}")

if __name__ == '__main__':
    unittest.main()
