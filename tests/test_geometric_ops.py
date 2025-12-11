"""
Unit Tests for LJPW Geometric Operations

Comprehensive test suite for geometric_ops.py module.

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import unittest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.geometric_ops import (
    SemanticOperations, Territory, SemanticDistance,
    NATURAL_EQUILIBRIUM, ANCHOR_POINT
)


class TestSemanticOperations(unittest.TestCase):
    """Test SemanticOperations class"""
    
    def setUp(self):
        """Set up test operations"""
        self.ops = SemanticOperations()
        
        # Test coordinates
        self.love = np.array([0.91, 0.48, 0.16, 0.71])
        self.hate = np.array([0.32, 0.35, 0.92, 0.68])
        self.justice = np.array([0.58, 0.92, 0.51, 0.85])
        self.power = np.array([0.43, 0.52, 0.90, 0.59])
        self.wisdom = np.array([0.66, 0.75, 0.40, 0.93])
    
    def test_antonym(self):
        """Test antonym reflection"""
        antonym = self.ops.antonym(self.love)
        
        # Antonym should be on opposite side of NE
        self.assertEqual(len(antonym), 4)
        
        # Check reflection formula: antonym = 2*NE - word
        expected = 2 * NATURAL_EQUILIBRIUM - self.love
        np.testing.assert_array_almost_equal(antonym, expected)
    
    def test_antonym_symmetry(self):
        """Test antonym is symmetric (antonym of antonym = original)"""
        antonym1 = self.ops.antonym(self.love)
        antonym2 = self.ops.antonym(antonym1)
        
        np.testing.assert_array_almost_equal(antonym2, self.love, decimal=10)
    
    def test_analogy(self):
        """Test analogy completion"""
        # a - b + c
        result = self.ops.analogy(self.love, self.hate, self.justice)
        
        self.assertEqual(len(result), 4)
        
        # Check formula: result = a - b + c
        expected = self.love - self.hate + self.justice
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_compose_uniform(self):
        """Test composition with uniform weights"""
        result = self.ops.compose([self.love, self.wisdom])
        
        # Should be average
        expected = (self.love + self.wisdom) / 2
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_compose_weighted(self):
        """Test composition with custom weights"""
        result = self.ops.compose([self.love, self.wisdom], weights=[0.7, 0.3])
        
        expected = 0.7 * self.love + 0.3 * self.wisdom
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_compose_normalize_weights(self):
        """Test weight normalization"""
        # Weights don't sum to 1.0
        result = self.ops.compose([self.love, self.wisdom], weights=[0.3, 0.5])
        
        # Should normalize to [0.375, 0.625]
        expected = 0.375 * self.love + 0.625 * self.wisdom
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_compose_empty(self):
        """Test composition with empty list"""
        with self.assertRaises(ValueError):
            self.ops.compose([])
    
    def test_interpolate(self):
        """Test semantic interpolation"""
        # Midpoint
        midpoint = self.ops.interpolate(self.love, self.hate, 0.5)
        expected = (self.love + self.hate) / 2
        np.testing.assert_array_almost_equal(midpoint, expected)
        
        # Start point
        start = self.ops.interpolate(self.love, self.hate, 0.0)
        np.testing.assert_array_almost_equal(start, self.love)
        
        # End point
        end = self.ops.interpolate(self.love, self.hate, 1.0)
        np.testing.assert_array_almost_equal(end, self.hate)
    
    def test_disambiguate(self):
        """Test context-based disambiguation"""
        result = self.ops.disambiguate(self.love, self.wisdom, context_weight=0.2)
        
        expected = 0.8 * self.love + 0.2 * self.wisdom
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_distance(self):
        """Test distance computation"""
        dist = self.ops.distance(self.love, self.hate)
        
        self.assertIsInstance(dist, SemanticDistance)
        self.assertGreater(dist.euclidean, 0)
        self.assertGreater(dist.manhattan, 0)
        self.assertGreaterEqual(dist.cosine, -1)
        self.assertLessEqual(dist.cosine, 1)
        self.assertEqual(len(dist.dimension_diffs), 4)
    
    def test_distance_same_point(self):
        """Test distance to same point is zero"""
        dist = self.ops.distance(self.love, self.love)
        
        self.assertAlmostEqual(dist.euclidean, 0.0, places=10)
        self.assertAlmostEqual(dist.manhattan, 0.0, places=10)
    
    def test_harmony(self):
        """Test harmony calculation"""
        # At anchor point
        h_anchor = self.ops.harmony(ANCHOR_POINT)
        self.assertAlmostEqual(h_anchor, 1.0, places=10)
        
        # Other points
        h_love = self.ops.harmony(self.love)
        self.assertGreater(h_love, 0)
        self.assertLess(h_love, 1)
    
    def test_distance_to_equilibrium(self):
        """Test distance to Natural Equilibrium"""
        # At NE
        d_ne = self.ops.distance_to_equilibrium(NATURAL_EQUILIBRIUM)
        self.assertAlmostEqual(d_ne, 0.0, places=10)
        
        # Other points
        d_love = self.ops.distance_to_equilibrium(self.love)
        self.assertGreater(d_love, 0)
    
    def test_classify_territory(self):
        """Test territory classification"""
        # Love should be PURE_LOVE
        territory, confidence = self.ops.classify_territory(self.love)
        self.assertEqual(territory, Territory.PURE_LOVE)
        self.assertGreater(confidence, 0)
        self.assertLessEqual(confidence, 1)
        
        # Justice should be JUSTICE_ORDER
        territory, confidence = self.ops.classify_territory(self.justice)
        self.assertEqual(territory, Territory.JUSTICE_ORDER)
        
        # Power should be POWER_STRENGTH
        territory, confidence = self.ops.classify_territory(self.power)
        self.assertEqual(territory, Territory.POWER_STRENGTH)
    
    def test_semantic_gradient(self):
        """Test semantic gradient"""
        gradient = self.ops.semantic_gradient(self.love, self.wisdom)
        
        # Should be normalized
        norm = np.linalg.norm(gradient)
        self.assertAlmostEqual(norm, 1.0, places=10)
        
        # Should point from love toward wisdom
        direction = self.wisdom - self.love
        direction_norm = direction / np.linalg.norm(direction)
        np.testing.assert_array_almost_equal(gradient, direction_norm)
    
    def test_semantic_gradient_same_point(self):
        """Test gradient at same point"""
        gradient = self.ops.semantic_gradient(self.love, self.love)
        
        # Should be zero vector
        np.testing.assert_array_almost_equal(gradient, np.zeros(4))
    
    def test_find_midpoint(self):
        """Test midpoint calculation"""
        midpoint = self.ops.find_midpoint([self.love, self.hate, self.wisdom])
        
        expected = (self.love + self.hate + self.wisdom) / 3
        np.testing.assert_array_almost_equal(midpoint, expected)
    
    def test_find_midpoint_empty(self):
        """Test midpoint with empty list"""
        with self.assertRaises(ValueError):
            self.ops.find_midpoint([])


class TestTerritory(unittest.TestCase):
    """Test Territory enum"""
    
    def test_territory_values(self):
        """Test territory enum values"""
        self.assertEqual(Territory.PURE_LOVE.value, 1)
        self.assertEqual(Territory.JUSTICE_ORDER.value, 2)
        self.assertEqual(Territory.NOBLE_ACTION.value, 3)
        self.assertEqual(Territory.WISDOM_UNDERSTANDING.value, 4)
        self.assertEqual(Territory.POWER_STRENGTH.value, 5)
        self.assertEqual(Territory.NEUTRAL_BALANCED.value, 6)
        self.assertEqual(Territory.MALEVOLENT_EVIL.value, 7)
        self.assertEqual(Territory.IGNORANCE_FOLLY.value, 8)
    
    def test_territory_names(self):
        """Test territory names"""
        self.assertEqual(Territory.PURE_LOVE.name, 'PURE_LOVE')
        self.assertEqual(Territory.JUSTICE_ORDER.name, 'JUSTICE_ORDER')


class TestSemanticDistance(unittest.TestCase):
    """Test SemanticDistance dataclass"""
    
    def test_creation(self):
        """Test SemanticDistance creation"""
        dist = SemanticDistance(
            euclidean=1.0,
            manhattan=2.0,
            cosine=0.5,
            dimension_diffs=np.array([0.1, 0.2, 0.3, 0.4])
        )
        
        self.assertEqual(dist.euclidean, 1.0)
        self.assertEqual(dist.manhattan, 2.0)
        self.assertEqual(dist.cosine, 0.5)
        self.assertEqual(len(dist.dimension_diffs), 4)
    
    def test_str(self):
        """Test string representation"""
        dist = SemanticDistance(
            euclidean=1.0,
            manhattan=2.0,
            cosine=0.5,
            dimension_diffs=np.array([0.1, 0.2, 0.3, 0.4])
        )
        
        s = str(dist)
        self.assertIn('1.0000', s)
        self.assertIn('0.5000', s)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running LJPW Geometric Operations Unit Tests")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticOperations))
    suite.addTests(loader.loadTestsFromTestCase(TestTerritory))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticDistance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    if result.wasSuccessful():
        print("[OK] All tests passed!")
    else:
        print("[FAILED] Some tests failed")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
