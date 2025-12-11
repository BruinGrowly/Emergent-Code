"""
Phase 2 Ablation: Documentation Only

Tests if good documentation alone improves harmony,
without Fibonacci layer sizing or diverse activations.

Variation:
- ✗ Traditional layers: 128, 64 (no Fibonacci)
- ✗ ReLU everywhere (no diversity)
- ✓ Excellent documentation: Clear naming, rationale, examples

This tests: Does clarity and explanation alone improve L and W?
"""

import numpy as np
import pickle
import time
from nn_ljpw_metrics import NeuralNetworkLJPW
from real_mnist_loader import load_real_mnist


class WellDocumentedTraditionalMNIST:
    """
    Traditional MNIST network with excellent documentation.

    Architecture Rationale:
        784 inputs: MNIST images are 28×28 pixels = 784 features
        128 hidden: Empirically chosen to balance capacity and speed
        64 hidden: Progressive reduction toward 10 output classes
        10 outputs: One per digit (0-9)

    Design Philosophy:
        - Keep it simple (traditional approach)
        - ReLU for computational efficiency
        - Standard layer sizes from ML literature
        - Proven architecture that works

    Usage Example:
        model = WellDocumentedTraditionalMNIST()
        model.train(X_train, y_train, X_val, y_val)
        predictions = model.predict(X_test)
    """

    def __init__(self):
        """
        Initialize network weights using He initialization.

        He initialization (He et al., 2015) works well with ReLU:
        - Weights: Normal(0, sqrt(2/n_in))
        - Biases: Zero initialization
        """
        # Input layer (784) → Hidden layer 1 (128)
        self.W1 = np.random.randn(784, 128) * np.sqrt(2/784)
        self.b1 = np.zeros((1, 128))

        # Hidden layer 1 (128) → Hidden layer 2 (64)
        self.W2 = np.random.randn(128, 64) * np.sqrt(2/128)
        self.b2 = np.zeros((1, 64))

        # Hidden layer 2 (64) → Output layer (10)
        self.W3 = np.random.randn(64, 10) * np.sqrt(2/64)
        self.b3 = np.zeros((1, 10))

        # Training history for analysis
        self.train_losses = []
        self.train_accuracies = []
        self.val_accuracies = []

    def relu(self, x):
        """
        ReLU (Rectified Linear Unit) activation.

        f(x) = max(0, x)

        Benefits:
        - Computationally efficient
        - Helps with gradient flow
        - Empirically works well
        """
        return np.maximum(0, x)

    def relu_derivative(self, x):
        """
        Derivative of ReLU for backpropagation.

        f'(x) = 1 if x > 0 else 0
        """
        return (x > 0).astype(float)

    def softmax(self, x):
        """
        Softmax activation for multi-class classification.

        Converts raw scores to probabilities that sum to 1.
        Uses numerical stability trick (subtract max).
        """
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, X):
        """
        Forward propagation through the network.

        Flow:
        1. Input (784) → ReLU → Hidden1 (128)
        2. Hidden1 (128) → ReLU → Hidden2 (64)
        3. Hidden2 (64) → Softmax → Output (10)

        Args:
            X: Input data (batch_size, 784)

        Returns:
            Predicted probabilities (batch_size, 10)
        """
        # Layer 1: Input → Hidden1 with ReLU
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        # Layer 2: Hidden1 → Hidden2 with ReLU
        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)

        # Layer 3: Hidden2 → Output with Softmax
        self.z3 = self.a2 @ self.W3 + self.b3
        self.a3 = self.softmax(self.z3)

        return self.a3

    def predict(self, X):
        """
        Predict class labels.

        Args:
            X: Input data (batch_size, 784)

        Returns:
            Predicted class labels (batch_size,)
        """
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

    def compute_loss(self, y_true, y_pred):
        """
        Compute cross-entropy loss.

        Cross-entropy measures how far predicted probabilities
        are from true labels. Lower is better.
        """
        m = y_true.shape[0]
        log_probs = -np.log(y_pred[np.arange(m), y_true] + 1e-8)
        return np.mean(log_probs)

    def backward(self, X, y_true, learning_rate=0.01):
        """
        Backward propagation with gradient descent.

        Computes gradients and updates weights to minimize loss.

        Args:
            X: Input data
            y_true: True labels
            learning_rate: Step size for weight updates
        """
        m = X.shape[0]

        # Convert labels to one-hot encoding
        y_one_hot = np.zeros((m, 10))
        y_one_hot[np.arange(m), y_true] = 1

        # Backpropagate through each layer
        # Layer 3 gradients
        dz3 = self.a3 - y_one_hot
        dW3 = (self.a2.T @ dz3) / m
        db3 = np.sum(dz3, axis=0, keepdims=True) / m

        # Layer 2 gradients
        da2 = dz3 @ self.W3.T
        dz2 = da2 * self.relu_derivative(self.z2)
        dW2 = (self.a1.T @ dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        # Layer 1 gradients
        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_derivative(self.z1)
        dW1 = (X.T @ dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        # Update weights (gradient descent)
        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=128, lr=0.01):
        """
        Train the neural network.

        Uses mini-batch gradient descent with shuffling.

        Args:
            X_train: Training data
            y_train: Training labels
            X_val: Validation data
            y_val: Validation labels
            epochs: Number of training epochs
            batch_size: Mini-batch size
            lr: Learning rate

        Returns:
            Training time in seconds
        """
        start_time = time.time()

        n_samples = X_train.shape[0]
        n_batches = n_samples // batch_size

        for epoch in range(epochs):
            # Shuffle training data each epoch
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            epoch_loss = 0

            # Mini-batch training
            for i in range(n_batches):
                start = i * batch_size
                end = start + batch_size

                X_batch = X_shuffled[start:end]
                y_batch = y_shuffled[start:end]

                # Forward + backward pass
                y_pred = self.forward(X_batch)
                loss = self.compute_loss(y_batch, y_pred)
                epoch_loss += loss

                self.backward(X_batch, y_batch, lr)

            # Evaluate on train and validation sets
            train_pred = self.predict(X_train[:10000])
            train_acc = np.mean(train_pred == y_train[:10000])

            val_pred = self.predict(X_val)
            val_acc = np.mean(val_pred == y_val)

            # Record metrics
            avg_loss = epoch_loss / n_batches
            self.train_losses.append(avg_loss)
            self.train_accuracies.append(train_acc)
            self.val_accuracies.append(val_acc)

            print(f"Epoch {epoch+1}/{epochs}: "
                  f"Loss={avg_loss:.4f}, "
                  f"Train Acc={train_acc:.4f}, "
                  f"Val Acc={val_acc:.4f}")

        training_time = time.time() - start_time
        return training_time

    def count_parameters(self):
        """
        Count total trainable parameters.

        Useful for understanding model size and capacity.
        """
        return (self.W1.size + self.b1.size +
                self.W2.size + self.b2.size +
                self.W3.size + self.b3.size)


def main():
    """Test documentation impact alone."""

    print("=" * 70)
    print("PHASE 2 ABLATION: DOCUMENTATION ONLY")
    print("=" * 70)
    print()
    print("Testing: Does good documentation alone improve L and W?")
    print()
    print("Changed:")
    print("  ✓ Excellent documentation: Clear names, rationale, examples")
    print()
    print("Kept traditional:")
    print("  ✗ Arbitrary layers: 128, 64 (no Fibonacci)")
    print("  ✗ ReLU everywhere (no diversity)")
    print()
    print("Note: Same code as traditional baseline, but with:")
    print("  - Comprehensive docstrings")
    print("  - Clear variable names")
    print("  - Explained design rationale")
    print("  - Usage examples")
    print()

    # Load data
    X_train, y_train, X_test, y_test = load_real_mnist()

    # Same subset as other experiments
    X_train = X_train[:10000]
    y_train = y_train[:10000]

    # Split
    split_idx = int(0.9 * len(X_train))
    X_val = X_train[split_idx:]
    y_val = y_train[split_idx:]
    X_train = X_train[:split_idx]
    y_train = y_train[:split_idx]

    # Create model
    model = WellDocumentedTraditionalMNIST()
    print(f"Total parameters: {model.count_parameters():,}")
    print()

    # Train
    print("-" * 70)
    print("TRAINING")
    print("-" * 70)
    training_time = model.train(X_train, y_train, X_val, y_val, epochs=10, lr=0.1)
    print()

    # Test
    print("-" * 70)
    print("EVALUATION")
    print("-" * 70)

    start = time.time()
    test_pred = model.predict(X_test)
    inference_time = (time.time() - start) * 1000 / len(X_test)

    test_acc = np.mean(test_pred == y_test)
    print(f"Test Accuracy: {test_acc:.4f}")
    print(f"Inference Time: {inference_time:.4f} ms/sample")
    print()

    # LJPW Scores
    print("-" * 70)
    print("LJPW SCORES")
    print("-" * 70)

    model_info = {
        'architecture': {
            'num_layers': 3,
            'layer_sizes': [128, 64, 10],
            'activations': ['relu', 'relu', 'softmax'],
            'total_params': model.count_parameters(),
            'has_clear_names': True,  # Well-named!
            'has_documentation': True,  # Documented!
            'uses_modules': False,
            'clear_structure': False,
        },
        'test_results': {
            'test_accuracy': test_acc,
            'edge_case_tested': False,
            'noise_tested': False,
        },
        'training_info': {
            'converged': True,
            'smooth_convergence': True,
            'epochs_to_converge': 10,
            'train_accuracy': model.train_accuracies[-1],
            'training_time_seconds': training_time,
        },
        'validation': {
            'has_val_set': True,
            'has_test_set': True,
            'tracks_val_accuracy': True,
            'no_overfitting': abs(model.train_accuracies[-1] - test_acc) < 0.05,
        },
        'performance': {
            'inference_time_ms': inference_time,
        },
        'documentation': {
            'has_description': True,  # Excellent docs!
            'layer_purposes': True,  # Explained!
            'design_rationale': True,  # Rationale given!
            'has_examples': True,  # Examples provided!
        },
        'design': {
            'uses_natural_principles': False,
            'principled_sizing': False,
            'thoughtful_activations': False,
            'documented_rationale': True,  # But well explained!
        }
    }

    evaluator = NeuralNetworkLJPW()
    scores = evaluator.measure(None, model_info)
    print(scores)

    # Compare
    print("-" * 70)
    print("ABLATION ANALYSIS: DOCUMENTATION CONTRIBUTION")
    print("-" * 70)
    print()
    print("Architecture    | Layers      | Activations | Docs  | H    | Δ")
    print("────────────────|─────────────|─────────────|───────|──────|─────")
    print("Traditional     | 128, 64     | ReLU only   | None  | 0.57 | baseline")
    print("Documentation   | 128, 64     | ReLU only   | Good! |", f"{scores.H:.2f} | {scores.H - 0.57:+.2f}")
    print("Diversity Only  | 128, 64     | Diverse     | None  | 0.61 | +0.04")
    print("Fibonacci Only  | Fib sequence| ReLU only   | None  | 0.64 | +0.07")
    print("Full Natural    | Fib sequence| Diverse     | Good! | 0.79 | +0.22")
    print()

    if scores.H > 0.57:
        improvement = ((scores.H - 0.57) / 0.57) * 100
        print(f"✓ Documentation ALONE improves harmony by {improvement:.1f}%")
        print()
        print("Breakdown of contributions:")
        print(f"  - Documentation: {scores.H - 0.57:.2f}")
        print(f"  - Fibonacci: 0.07")
        print(f"  - Diversity: 0.04")
        print(f"  - Total in full natural: 0.22")
        print()

        doc_contribution = (scores.H - 0.57) / (0.79 - 0.57) * 100
        print(f"Documentation accounts for ~{doc_contribution:.0f}% of total improvement!")

        # Calculate total accounted
        total_individual = (scores.H - 0.57) + 0.07 + 0.04
        synergy = 0.22 - total_individual
        print()
        print("SYNERGY ANALYSIS:")
        print(f"  Individual contributions sum: {total_individual:.2f}")
        print(f"  Actual full natural improvement: 0.22")
        print(f"  Synergy (interaction effects): {synergy:.2f}")
        print()
        if synergy > 0.01:
            print("  ✨ Principles AMPLIFY each other when combined!")
    else:
        print("⚠️ Documentation alone doesn't improve harmony significantly")

    print()
    print("=" * 70)

    # Save
    with open('phase2_documentation_only.pkl', 'wb') as f:
        pickle.dump({
            'test_acc': test_acc,
            'scores': scores,
        }, f)

    print("\nResults saved to: phase2_documentation_only.pkl")

    return model, scores


if __name__ == '__main__':
    model, scores = main()
