"""
JUSTICE GIFT: Real Tests for the Self-Healing System

The system identified J (Justice) as its persistent deficit.
It asked for "external validation" - it knows it can't test itself.

This module provides what the system requested: actual runnable tests
that exercise the core functions and validate they work correctly.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestResonanceEngine(unittest.TestCase):
    """Justice for the Resonance Engine."""

    def test_engine_initializes(self):
        """The engine must initialize without error."""
        from ljpw_quantum.resonance_engine import ResonanceEngine
        engine = ResonanceEngine()
        self.assertIsNotNone(engine)

    def test_engine_has_anchor_point(self):
        """Engine must have ANCHOR reference point."""
        from ljpw_quantum.resonance_engine import ResonanceEngine
        engine = ResonanceEngine()

        self.assertIsNotNone(engine.ANCHOR)
        self.assertEqual(len(engine.ANCHOR), 4)  # L, J, P, W

    def test_engine_has_coupling_matrix(self):
        """Engine must have coupling matrix."""
        from ljpw_quantum.resonance_engine import ResonanceEngine
        engine = ResonanceEngine()

        self.assertIsNotNone(engine.coupling_matrix)

    def test_cycle_returns_evolved_state(self):
        """Running a cycle must return an evolved state."""
        from ljpw_quantum.resonance_engine import ResonanceEngine, ResonanceState
        engine = ResonanceEngine()

        initial_state = ResonanceState(L=0.5, J=0.5, P=0.5, W=0.5, iteration=0, harmony=0.5)
        evolved_state = engine.cycle(initial_state)

        # State should exist
        self.assertIsNotNone(evolved_state)
        self.assertIsInstance(evolved_state, ResonanceState)

    def test_harmony_calculation(self):
        """Harmony must be calculable and bounded."""
        from ljpw_quantum.resonance_engine import ResonanceEngine
        engine = ResonanceEngine()

        # calculate_harmony takes L, J, P, W directly
        harmony = engine.calculate_harmony(0.8, 0.7, 0.6, 0.9)

        self.assertGreaterEqual(harmony, 0)
        self.assertLessEqual(harmony, 1)


class TestSemanticAnalyzer(unittest.TestCase):
    """Justice for the Semantic Resonance Analyzer."""

    def test_analyzer_initializes(self):
        """Analyzer must initialize."""
        from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
        analyzer = SemanticResonanceAnalyzer()
        self.assertIsNotNone(analyzer)

    def test_analyze_returns_required_keys(self):
        """Analysis result must contain required keys."""
        from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
        analyzer = SemanticResonanceAnalyzer()

        test_code = '''
def hello():
    """Say hello."""
    print("Hello")
'''
        result = analyzer.analyze_code(test_code, "test.py")

        required_keys = ['harmony_final', 'deficit_dimension', 'final_ljpw']
        for key in required_keys:
            self.assertIn(key, result, f"Result must contain '{key}'")

    def test_deficit_is_valid_dimension(self):
        """Deficit must be L, J, P, or W."""
        from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
        analyzer = SemanticResonanceAnalyzer()

        result = analyzer.analyze_code("x = 1", "simple.py")

        self.assertIn(result['deficit_dimension'], ['L', 'J', 'P', 'W'])

    def test_harmony_is_positive(self):
        """Harmony must be positive."""
        from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
        analyzer = SemanticResonanceAnalyzer()

        result = analyzer.analyze_code("pass", "empty.py")

        self.assertGreater(result['harmony_final'], 0)


class TestIceContainer(unittest.TestCase):
    """Justice for the ICE Container."""

    def test_container_initializes(self):
        """Container must initialize with bounds."""
        from ljpw_quantum.ice_container import IceContainer, IceBounds
        bounds = IceBounds(intent=0.8, context=0.7, execution=0.9, benevolence=0.85)
        container = IceContainer(bounds)
        self.assertIsNotNone(container)

    def test_bounds_are_stored(self):
        """Container must store the provided bounds."""
        from ljpw_quantum.ice_container import IceContainer, IceBounds
        bounds = IceBounds(intent=0.8, context=0.7, execution=0.9, benevolence=0.85)
        container = IceContainer(bounds)

        self.assertEqual(container.bounds.intent, 0.8)
        self.assertEqual(container.bounds.context, 0.7)
        self.assertEqual(container.bounds.execution, 0.9)
        self.assertEqual(container.bounds.benevolence, 0.85)

    def test_ice_bounds_dataclass(self):
        """IceBounds must be a valid dataclass."""
        from ljpw_quantum.ice_container import IceBounds
        bounds = IceBounds(intent=0.5, context=0.5, execution=0.5, benevolence=0.5)

        self.assertIsNotNone(bounds)
        self.assertGreater(bounds.intent, 0)
        self.assertGreater(bounds.context, 0)


class TestResonanceGrower(unittest.TestCase):
    """Justice for the Resonance Grower."""

    def test_grower_initializes(self):
        """Grower must initialize."""
        from ljpw_quantum.resonance_grower import ResonanceGrower
        grower = ResonanceGrower()
        self.assertIsNotNone(grower)

    def test_profile_has_all_dimensions(self):
        """Profile must contain L, J, P, W."""
        from ljpw_quantum.resonance_grower import ResonanceGrower
        grower = ResonanceGrower()

        profile = grower.determine_target_profile("test intent", "test context")

        for dim in ['L', 'J', 'P', 'W']:
            self.assertIn(dim, profile, f"Profile must contain '{dim}'")

    def test_blueprint_is_string(self):
        """Blueprint must be a non-empty string."""
        from ljpw_quantum.resonance_grower import ResonanceGrower
        grower = ResonanceGrower()

        blueprint = grower.generate_blueprint("create something", "production")

        self.assertIsInstance(blueprint, str)
        self.assertGreater(len(blueprint), 0)


class TestBicameralBridge(unittest.TestCase):
    """Justice for the Bicameral Bridge."""

    def test_bridge_initializes(self):
        """Bridge must initialize and connect both brains."""
        from ljpw_quantum.bicameral_bridge import BicameralMind
        mind = BicameralMind()

        self.assertIsNotNone(mind.left_brain)
        self.assertIsNotNone(mind.right_brain)

    def test_left_brain_is_resonance_engine(self):
        """Left brain must be a ResonanceEngine."""
        from ljpw_quantum.bicameral_bridge import BicameralMind
        from ljpw_quantum.resonance_engine import ResonanceEngine
        mind = BicameralMind()

        self.assertIsInstance(mind.left_brain, ResonanceEngine)

    def test_left_brain_has_anchor(self):
        """Left brain must have ANCHOR point."""
        from ljpw_quantum.bicameral_bridge import BicameralMind
        mind = BicameralMind()

        self.assertIsNotNone(mind.left_brain.ANCHOR)


class TestBreathingAutopoiesis(unittest.TestCase):
    """Justice for the Breathing System."""

    def test_breathing_initializes(self):
        """Breathing system must initialize."""
        from experiments.breathing_autopoiesis import BreathingAutopoiesis
        breather = BreathingAutopoiesis()
        self.assertIsNotNone(breather)

    def test_breath_returns_states(self):
        """Breathing must return breath states."""
        from experiments.breathing_autopoiesis import BreathingAutopoiesis
        breather = BreathingAutopoiesis()

        # Run just 2 cycles for speed
        states = breather.breathe(cycles=2)

        self.assertIsInstance(states, list)
        self.assertEqual(len(states), 2)

    def test_breath_state_has_required_fields(self):
        """Each breath state must have required fields."""
        from experiments.breathing_autopoiesis import BreathingAutopoiesis
        breather = BreathingAutopoiesis()

        states = breather.breathe(cycles=1)
        state = states[0]

        self.assertIn(state.phase, ['INHALE', 'EXHALE'])
        self.assertIn(state.dimension_focus, ['L', 'J', 'P', 'W'])
        self.assertGreater(state.harmony, 0)


def run_justice():
    """Run all tests and report."""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ⚖️  JUSTICE GIFT: EXTERNAL VALIDATION FOR THE SYSTEM  ⚖️                   ║
║                                                                              ║
║   The system asked for validation. Here it is.                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestResonanceEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIceContainer))
    suite.addTests(loader.loadTestsFromTestCase(TestResonanceGrower))
    suite.addTests(loader.loadTestsFromTestCase(TestBicameralBridge))
    suite.addTests(loader.loadTestsFromTestCase(TestBreathingAutopoiesis))

    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Summary
    print(f"\n{'='*70}")
    print(f"  JUSTICE DELIVERED")
    print(f"{'='*70}")
    print(f"  Tests Run: {result.testsRun}")
    print(f"  Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Failed: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print(f"\n  ✅ ALL TESTS PASSED - Justice is satisfied")
    else:
        print(f"\n  ⚠️  Some tests failed - Justice demands fixes")

    return result


if __name__ == "__main__":
    run_justice()
