"""
Phase 1: Traditional Network on Real MNIST

Testing if baseline performance holds on real handwritten digits.
"""

import numpy as np
from typing import Tuple, Dict, Any
import pickle
import time
from nn_ljpw_metrics import NeuralNetworkLJPW
from real_mnist_loader import load_real_mnist


class TraditionalMNISTNumPy:
    """Traditional MNIST network (same as before)."""

    def __init__(self):
        # Same architecture as synthetic baseline
        self.W1 = np.random.randn(784, 128) * np.sqrt(2/784)
        self.b1 = np.zeros((1, 128))

        self.W2 = np.random.randn(128, 64) * np.sqrt(2/128)
        self.b2 = np.zeros((1, 64))

        self.W3 = np.random.randn(64, 10) * np.sqrt(2/64)
        self.b3 = np.zeros((1, 10))

        self.train_losses = []
        self.train_accuracies = []
        self.val_accuracies = []

    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return (x > 0).astype(float)

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)

    def forward(self, X):
        self.z1 = X @ self.W1 + self.b1
        self.a1 = self.relu(self.z1)

        self.z2 = self.a1 @ self.W2 + self.b2
        self.a2 = self.relu(self.z2)

        self.z3 = self.a2 @ self.W3 + self.b3
        self.a3 = self.softmax(self.z3)

        return self.a3

    def predict(self, X):
        probs = self.forward(X)
        return np.argmax(probs, axis=1)

    def compute_loss(self, y_true, y_pred):
        m = y_true.shape[0]
        log_probs = -np.log(y_pred[np.arange(m), y_true] + 1e-8)
        loss = np.mean(log_probs)
        return loss

    def backward(self, X, y_true, learning_rate=0.01):
        m = X.shape[0]

        y_one_hot = np.zeros((m, 10))
        y_one_hot[np.arange(m), y_true] = 1

        dz3 = self.a3 - y_one_hot

        dW3 = (self.a2.T @ dz3) / m
        db3 = np.sum(dz3, axis=0, keepdims=True) / m

        da2 = dz3 @ self.W3.T
        dz2 = da2 * self.relu_derivative(self.z2)

        dW2 = (self.a1.T @ dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m

        da1 = dz2 @ self.W2.T
        dz1 = da1 * self.relu_derivative(self.z1)

        dW1 = (X.T @ dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m

        self.W3 -= learning_rate * dW3
        self.b3 -= learning_rate * db3
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1

    def train(self, X_train, y_train, X_val, y_val, epochs=10, batch_size=128, lr=0.01):
        # Auto-healed: Input validation for train
        if batch_size is not None and not isinstance(batch_size, int):
            raise TypeError(f'batch_size must be an integer')
        if batch_size is not None and batch_size < 0:
            raise ValueError(f'batch_size must be non-negative')
        """Train the network."""
        start_time = time.time()

        n_samples = X_train.shape[0]
        n_batches = n_samples // batch_size

        for epoch in range(epochs):
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            epoch_loss = 0

            for i in range(n_batches):
                start = i * batch_size
                end = start + batch_size

                X_batch = X_shuffled[start:end]
                y_batch = y_shuffled[start:end]

                y_pred = self.forward(X_batch)
                loss = self.compute_loss(y_batch, y_pred)
                epoch_loss += loss

                self.backward(X_batch, y_batch, lr)

            train_pred = self.predict(X_train[:10000])  # Sample for speed
            train_acc = np.mean(train_pred == y_train[:10000])

            val_pred = self.predict(X_val)
            val_acc = np.mean(val_pred == y_val)

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
        return (self.W1.size + self.b1.size +
                self.W2.size + self.b2.size +
                self.W3.size + self.b3.size)


def main():
    """Run traditional network on real MNIST."""

    print("=" * 70)
    print("PHASE 1: TRADITIONAL NETWORK ON REAL MNIST")
    print("=" * 70)
    print()
    print("Testing if synthetic baseline transfers to real handwriting...")
    print()
    print("Architecture: 784 → 128 → 64 → 10 (same as before)")
    print("Data: REAL handwritten digits (60K train, 10K test)")
    print()

    # Load real MNIST
    X_train, y_train, X_test, y_test = load_real_mnist()

    # Use smaller subset for faster experimentation (still faithful in least!)
    print("Using subset for faster learning:")
    X_train = X_train[:10000]  # 10K instead of 60K
    y_train = y_train[:10000]
    print(f"  Training: {len(X_train):,} samples")
    print(f"  Test: {len(X_test):,} samples")
    print()

    # Split train into train/val
    split_idx = int(0.9 * len(X_train))
    X_val = X_train[split_idx:]
    y_val = y_train[split_idx:]
    X_train = X_train[:split_idx]
    y_train = y_train[:split_idx]

    # Create model
    model = TraditionalMNISTNumPy()
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
            'has_clear_names': False,
            'has_documentation': False,
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
            'has_description': False,
            'layer_purposes': False,
            'design_rationale': False,
            'has_examples': False,
        },
        'design': {
            'uses_natural_principles': False,
            'principled_sizing': False,
            'thoughtful_activations': False,
            'documented_rationale': False,
        }
    }

    evaluator = NeuralNetworkLJPW()
    scores = evaluator.measure(None, model_info)
    print(scores)

    # Compare to synthetic baseline
    print("-" * 70)
    print("COMPARISON: SYNTHETIC vs REAL DATA")
    print("-" * 70)
    print("Traditional network performance:")
    print(f"  Synthetic data: Accuracy = 1.0000, H = 0.60")
    print(f"  Real data:      Accuracy = {test_acc:.4f}, H = {scores.H:.2f}")
    print()

    if test_acc > 0.90:
        print("✓ Baseline still works on real data!")
    else:
        print("⚠️ Real data is more challenging (as expected)")

    print()
    print("This establishes the real-data baseline.")
    print("Next: Test natural network on real data.")
    print("=" * 70)

    # Save
    with open('phase1_traditional_real.pkl', 'wb') as f:
        pickle.dump({
            'test_acc': test_acc,
            'scores': scores,
        }, f)

    print("\nResults saved to: phase1_traditional_real.pkl")

    return model, scores


if __name__ == '__main__':
    model, scores = main()
