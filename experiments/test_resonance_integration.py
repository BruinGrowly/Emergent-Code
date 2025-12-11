"""
Integration Test for Resonance Engine and ICE Framework
Verifies:
1. Resonance cycles produce expected growth.
2. ICE Bounds correctly constrain overflow.
3. Deficit detection works.
"""

import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine, ResonanceState
from ljpw_quantum.ice_container import IceContainer, IceBounds

class TestResonanceIntegration(unittest.TestCase):
    
    def setUp(self):
        self.engine = ResonanceEngine()
        
    def test_resonance_growth(self):
        """Test that resonance grows values over time."""
        # Start low
        start = [0.2, 0.2, 0.2, 0.2]
        res = self.engine.analyze_trajectory(start, cycles=10)
        
        final = res['final_state']
        # Should grow because even low values couple and amplify
        self.assertGreater(final.L, 0.2)
        self.assertGreater(final.W, 0.2)
        
    def test_ice_bounding(self):
        """Test that ICE bounds prevent overflow."""
        # Unbounded run (simulated by high bounds) -> should grow large
        # Bounded run -> should clamp
        
        start = [0.5, 0.5, 0.5, 0.5]
        
        # Strict bounds
        bounds = IceBounds(intent=0.6, context=0.6, execution=0.6, benevolence=0.6)
        container = IceContainer(bounds)
        
        res = self.engine.analyze_trajectory(
            start, 
            cycles=50, 
            ice_bounds=container.get_ljpw_limits()
        )
        
        final = res['final_state']
        
        # Check limits (allow tiny float margin)
        self.assertLessEqual(final.W, 0.601) # Intent -> Wisdom
        self.assertLessEqual(final.J, 0.601) # Context -> Justice
        self.assertLessEqual(final.P, 0.601) # Execution -> Power
        self.assertLessEqual(final.L, 0.601) # Benevolence -> Love
        
    def test_deficit_detection(self):
        """Test that the engine finds the deficit."""
        # Scenario: High Power, Low Love
        # Love amplifies strongly, so if we start with some seed, it should grow fast
        start = [0.3, 0.5, 0.8, 0.5] 
        
        res = self.engine.analyze_trajectory(start, cycles=20)
        
        # In v6.0 dynamics, Love is the strongest amplifier
        # It should show significant growth or be identified as a key mover
        # Deficit detection identifies what GREW the most (filled the gap)
        
        # If Love is low but has high coupling input from others (J->L 0.8, P->L 0.6, W->L 1.3)
        # It gets pushed up hard.
        
        print(f"\nDeficit detected: {res['dominant_deficit']}")
        self.assertTrue(res['dominant_deficit'] in ['L', 'W', 'J']) # High Power drives Justice strongly

if __name__ == '__main__':
    unittest.main()
