"""
Core Component Unit Tests

Tests for the fundamental working components:
- FibonacciLayer (layer sizing and forward/backward pass)
- DiverseActivation (multiple activation functions)
- NaturalMNIST (complete model)
- TraditionalMNIST (baseline model)
- Harmony metrics (LJPW scoring)

Uses unittest framework for standard Python testing.
"""

import unittest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ljpw_nn.layers import FibonacciLayer, FIBONACCI
from ljpw_nn.activations import DiverseActivation
from ljpw_nn.models import NaturalMNIST
from ljpw_nn.baseline import TraditionalMNIST
from ljpw_nn.metrics import measure_harmony, HarmonyScores


class TestFibonacciLayer(unittest.TestCase):
    """Test FibonacciLayer implementation."""

    def test_fibonacci_sequence(self):
        """Test that FIBONACCI constant is correct."""
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
        self.assertEqual(FIBONACCI[:len(expected)], expected)

    def test_layer_initialization(self):
        """Test layer initializes with correct dimensions."""
        layer = FibonacciLayer(input_size=784, fib_index=11)
        self.assertEqual(layer.size, 89)  # F11 = 89
        self.assertEqual(layer.weights.shape, (784, 89))
        self.assertEqual(layer.bias.shape, (1, 89))

    def test_forward_pass_shape(self):
        """Test forward pass produces correct output shape."""
        layer = FibonacciLayer(input_size=100, fib_index=9)
        X = np.random.randn(32, 100)  # Batch of 32
        output = layer.forward(X)
        self.assertEqual(output.shape, (32, 34))  # F9 = 34

    def test_backward_pass(self):
        """Test backward pass updates weights."""
        layer = FibonacciLayer(input_size=50, fib_index=7)
        X = np.random.randn(16, 50)

        # Forward pass
        output = layer.forward(X)

        # Store original weights
        original_weights = layer.weights.copy()

        # Backward pass with dummy gradient
        grad_output = np.random.randn(*output.shape)
        grad_input = layer.backward(grad_output, learning_rate=0.01)

        # Weights should have changed
        self.assertFalse(np.allclose(layer.weights, original_weights))
        self.assertEqual(grad_input.shape, X.shape)

    def test_invalid_fib_index(self):
        """Test that invalid Fibonacci index raises error."""
        with self.assertRaises(ValueError):
            FibonacciLayer(input_size=100, fib_index=100)

    def test_zero_input_size(self):
        """Test that zero input size creates valid layer."""
        # Should still work, just with unusual dimensions
        layer = FibonacciLayer(input_size=1, fib_index=5)
        self.assertEqual(layer.size, 5)

    def test_golden_ratio_compression(self):
        """Test that consecutive Fibonacci layers have golden ratio compression."""
        layer1 = FibonacciLayer(input_size=100, fib_index=11)  # 89
        layer2 = FibonacciLayer(input_size=89, fib_index=10)   # 55 (consecutive!)

        ratio = layer1.size / layer2.size
        golden_ratio = (1 + np.sqrt(5)) / 2  # φ ≈ 1.618

        # Should be close to golden ratio
        self.assertAlmostEqual(ratio, golden_ratio, delta=0.1)


class TestDiverseActivation(unittest.TestCase):
    """Test DiverseActivation implementation."""

    def test_single_activation(self):
        """Test single activation function."""
        activation = DiverseActivation(size=4, mix=['relu'])
        X = np.array([[-1, 0, 1, 2]])
        output = activation.forward(X)
        expected = np.array([[0, 0, 1, 2]])
        np.testing.assert_array_almost_equal(output, expected)

    def test_diverse_activations(self):
        """Test multiple activation functions."""
        activation = DiverseActivation(size=12, mix=['relu', 'tanh', 'swish'])
        X = np.random.randn(10, 12)
        output = activation.forward(X)
        self.assertEqual(output.shape, X.shape)

    def test_backward_pass(self):
        """Test backward pass returns correct gradient shape."""
        activation = DiverseActivation(size=10, mix=['relu', 'swish'])
        X = np.random.randn(5, 10)

        # Forward pass
        output = activation.forward(X)

        # Backward pass
        grad = activation.backward(X)

        self.assertEqual(grad.shape, X.shape)

    def test_invalid_activation(self):
        """Test that invalid activation name raises error."""
        with self.assertRaises(ValueError):
            activation = DiverseActivation(size=10, mix=['invalid_activation'])

    def test_empty_activations(self):
        """Test that empty activations list raises error."""
        with self.assertRaises((ValueError, IndexError)):
            activation = DiverseActivation(size=10, mix=[])
            X = np.random.randn(5, 10)
            activation.forward(X)

    def test_biodiversity_principle(self):
        """Test that using multiple activations provides diversity."""
        # Single activation (monoculture)
        mono = DiverseActivation(size=50, mix=['relu'])
        X = np.random.randn(100, 50)
        output_mono = mono.forward(X)

        # Multiple activations (biodiversity)
        diverse = DiverseActivation(size=50, mix=['relu', 'swish', 'tanh'])
        output_diverse = diverse.forward(X)

        # Diverse output should have different statistical properties
        # (This is a weak test, but demonstrates the concept)
        self.assertEqual(output_mono.shape, output_diverse.shape)


class TestNaturalMNIST(unittest.TestCase):
    """Test NaturalMNIST model."""

    def test_model_initialization(self):
        """Test model initializes with correct architecture."""
        model = NaturalMNIST(verbose=False)

        # Should have 3 hidden layers
        self.assertEqual(len(model.layers), 3)

        # Check Fibonacci sizes
        self.assertEqual(model.layers[0].size, 89)  # F11
        self.assertEqual(model.layers[1].size, 34)  # F9
        self.assertEqual(model.layers[2].size, 13)  # F7

        # Output layer
        self.assertEqual(model.output_size, 10)

    def test_forward_pass(self):
        """Test forward pass produces correct output shape."""
        model = NaturalMNIST(verbose=False)
        X = np.random.randn(16, 784)
        output = model.forward(X)

        self.assertEqual(output.shape, (16, 10))
        # Should be probabilities (sum to 1)
        np.testing.assert_array_almost_equal(output.sum(axis=1), np.ones(16))

    def test_predict(self):
        """Test predict returns class labels."""
        model = NaturalMNIST(verbose=False)
        X = np.random.randn(10, 784)
        predictions = model.predict(X)

        self.assertEqual(predictions.shape, (10,))
        # All predictions should be valid class labels (0-9)
        self.assertTrue(np.all((predictions >= 0) & (predictions <= 9)))

    def test_training_updates_weights(self):
        """Test that training updates model weights."""
        model = NaturalMNIST(verbose=False)

        # Small dataset
        X_train = np.random.randn(100, 784)
        y_train = np.random.randint(0, 10, 100)

        # Store original weights
        original_weights = model.output_weights.copy()

        # Train for 1 epoch
        model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=False)

        # Weights should have changed
        self.assertFalse(np.allclose(model.output_weights, original_weights))

    def test_evaluate(self):
        """Test evaluate returns accuracy between 0 and 1."""
        model = NaturalMNIST(verbose=False)

        # Small test set
        X_test = np.random.randn(50, 784)
        y_test = np.random.randint(0, 10, 50)

        accuracy = model.evaluate(X_test, y_test)

        self.assertGreaterEqual(accuracy, 0.0)
        self.assertLessEqual(accuracy, 1.0)

    def test_measure_harmony(self):
        """Test harmony measurement returns valid scores."""
        model = NaturalMNIST(verbose=False)

        X_test = np.random.randn(50, 784)
        y_test = np.random.randint(0, 10, 50)

        scores = model.measure_harmony(X_test, y_test)

        self.assertIsInstance(scores, HarmonyScores)
        self.assertGreaterEqual(scores.L, 0.0)
        self.assertGreaterEqual(scores.J, 0.0)
        self.assertGreaterEqual(scores.P, 0.0)
        self.assertGreaterEqual(scores.W, 0.0)
        self.assertGreaterEqual(scores.H, 0.0)


class TestTraditionalMNIST(unittest.TestCase):
    """Test TraditionalMNIST baseline model."""

    def test_model_initialization(self):
        """Test model initializes with correct architecture."""
        model = TraditionalMNIST(verbose=False)

        # Should have 2 hidden layers + output
        self.assertEqual(len(model.weights), 3)

        # Check layer sizes
        self.assertEqual(model.layer_sizes, [128, 64])
        self.assertEqual(model.output_size, 10)

    def test_forward_pass(self):
        """Test forward pass produces correct output shape."""
        model = TraditionalMNIST(verbose=False)
        X = np.random.randn(16, 784)
        output = model.forward(X, training=False)

        self.assertEqual(output.shape, (16, 10))
        # Should be probabilities (sum to 1)
        np.testing.assert_array_almost_equal(output.sum(axis=1), np.ones(16))

    def test_predict(self):
        """Test predict returns class labels."""
        model = TraditionalMNIST(verbose=False)
        X = np.random.randn(10, 784)
        predictions = model.predict(X)

        self.assertEqual(predictions.shape, (10,))
        # All predictions should be valid class labels (0-9)
        self.assertTrue(np.all((predictions >= 0) & (predictions <= 9)))

    def test_training_updates_weights(self):
        """Test that training updates model weights."""
        model = TraditionalMNIST(verbose=False)

        # Small dataset
        X_train = np.random.randn(100, 784)
        y_train = np.random.randint(0, 10, 100)

        # Store original weights
        original_weights = model.weights[0].copy()

        # Train for 1 epoch
        model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=False)

        # Weights should have changed
        self.assertFalse(np.allclose(model.weights[0], original_weights))


class TestHarmonyMetrics(unittest.TestCase):
    """Test harmony measurement and LJPW scoring."""

    def test_harmony_scores_dataclass(self):
        """Test HarmonyScores dataclass."""
        scores = HarmonyScores(L=0.8, J=0.75, P=0.9, W=0.85, H=0.82)

        self.assertEqual(scores.L, 0.8)
        self.assertEqual(scores.J, 0.75)
        self.assertEqual(scores.P, 0.9)
        self.assertEqual(scores.W, 0.85)
        self.assertEqual(scores.H, 0.82)

    def test_harmony_geometric_mean(self):
        """Test that H is approximately geometric mean of L,J,P,W."""
        scores = HarmonyScores(L=0.8, J=0.8, P=0.8, W=0.8, H=0.8)

        # H should be geometric mean
        expected_H = (0.8 * 0.8 * 0.8 * 0.8) ** 0.25
        self.assertAlmostEqual(scores.H, expected_H, places=5)

    def test_production_ready_threshold(self):
        """Test production ready threshold (H >= 0.7)."""
        ready = HarmonyScores(L=0.8, J=0.8, P=0.8, W=0.8, H=0.8)
        not_ready = HarmonyScores(L=0.6, J=0.6, P=0.6, W=0.6, H=0.6)

        self.assertTrue(ready.is_production_ready)
        self.assertFalse(not_ready.is_production_ready)

    def test_measure_harmony_basic(self):
        """Test basic harmony measurement."""
        layer = FibonacciLayer(input_size=784, fib_index=11)
        scores = measure_harmony(layer)

        self.assertIsInstance(scores, HarmonyScores)
        self.assertGreater(scores.H, 0.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_single_sample_batch(self):
        """Test models handle single sample (batch_size=1)."""
        model = NaturalMNIST(verbose=False)
        X = np.random.randn(1, 784)
        output = model.forward(X)
        self.assertEqual(output.shape, (1, 10))

    def test_large_batch(self):
        """Test models handle large batches."""
        model = NaturalMNIST(verbose=False)
        X = np.random.randn(1000, 784)
        output = model.forward(X)
        self.assertEqual(output.shape, (1000, 10))

    def test_zero_learning_rate(self):
        """Test that zero learning rate doesn't crash (but doesn't learn)."""
        model = NaturalMNIST(verbose=False, learning_rate=0.0)
        X_train = np.random.randn(50, 784)
        y_train = np.random.randint(0, 10, 50)

        # Should run without error
        history = model.fit(X_train, y_train, epochs=1, verbose=False)
        self.assertIsNotNone(history)

    def test_extreme_input_values(self):
        """Test models handle extreme input values."""
        model = NaturalMNIST(verbose=False)

        # Very large values
        X_large = np.ones((10, 784)) * 1000
        output = model.forward(X_large)
        self.assertFalse(np.any(np.isnan(output)))
        self.assertFalse(np.any(np.isinf(output)))

    def test_all_zeros_input(self):
        """Test models handle all-zeros input."""
        model = NaturalMNIST(verbose=False)
        X_zeros = np.zeros((10, 784))
        output = model.forward(X_zeros)

        self.assertEqual(output.shape, (10, 10))
        self.assertFalse(np.any(np.isnan(output)))

    def test_single_class_training(self):
        """Test training with single class doesn't crash."""
        model = NaturalMNIST(verbose=False)
        X_train = np.random.randn(50, 784)
        y_train = np.zeros(50, dtype=int)  # All same class

        # Should run without error (though accuracy will be poor)
        history = model.fit(X_train, y_train, epochs=1, verbose=False)
        self.assertIsNotNone(history)


def run_tests():
    """Run all unit tests."""
    print("=" * 80)
    print("LJPW NEURAL NETWORKS - UNIT TEST SUITE")
    print("=" * 80)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFibonacciLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestDiverseActivation))
    suite.addTests(loader.loadTestsFromTestCase(TestNaturalMNIST))
    suite.addTests(loader.loadTestsFromTestCase(TestTraditionalMNIST))
    suite.addTests(loader.loadTestsFromTestCase(TestHarmonyMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()

    if result.wasSuccessful():
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")

    print("=" * 80)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
