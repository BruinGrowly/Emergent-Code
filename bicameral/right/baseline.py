"""
Traditional Neural Network Baseline

This module provides a conventional neural network implementation for comparison
with natural approaches. It uses:
- Arbitrary power-of-2 layer sizes (128, 64)
- ReLU activation everywhere (monoculture)
- Standard backpropagation
- No natural principles

This serves as a baseline to demonstrate the advantage of natural design.

Example:
    >>> from bicameral.right.baseline import TraditionalMNIST
    >>> model = TraditionalMNIST()
    >>> model.fit(X_train, y_train, epochs=10)
    >>> accuracy = model.evaluate(X_test, y_test)
"""

import numpy as np
from typing import Optional, Tuple, List
from dataclasses import dataclass


@dataclass
class TrainingHistory:
    """Training history for a model."""
    train_loss: List[float]
    train_accuracy: List[float]
    val_loss: Optional[List[float]] = None
    val_accuracy: Optional[List[float]] = None


class TraditionalMNIST:
    """
    Traditional Neural Network for MNIST Classification.

    This is a conventional NN with arbitrary design choices:
    - Power-of-2 layer sizes (128, 64, 10)
    - ReLU activation everywhere
    - No principled rationale

    Serves as baseline for comparison with NaturalMNIST.

    Architecture:
        Input:  784 pixels (28×28 MNIST image)
        Layer1: 128 units - ReLU
        Layer2: 64 units  - ReLU
        Output: 10 units  - Softmax

    Total parameters: ~109,000 (48% more than NaturalMNIST)

    Example:
        >>> model = TraditionalMNIST()
        >>> history = model.fit(X_train, y_train, epochs=10)
        >>> accuracy = model.evaluate(X_test, y_test)
    """

    def __init__(
        self,
        layer_sizes: Optional[List[int]] = None,
        learning_rate: float = 0.01,
        verbose: bool = True
    ):
        """
        Initialize TraditionalMNIST model.

        Args:
            layer_sizes: Hidden layer sizes (default: [128, 64])
            learning_rate: Learning rate for training
            verbose: Print model summary on initialization
        """
        self.learning_rate = learning_rate
        self.verbose = verbose
        self.history = None

        # Default traditional architecture: 128 → 64 → 10
        if layer_sizes is None:
            layer_sizes = [128, 64]

        self.layer_sizes = layer_sizes
        self.output_size = 10

        # Initialize weights and biases
        self.weights = []
        self.biases = []

        # Input layer → first hidden
        input_size = 784
        for size in layer_sizes:
            # He initialization for ReLU
            W = np.random.randn(input_size, size) * np.sqrt(2.0 / input_size)
            b = np.zeros((1, size))
            self.weights.append(W)
            self.biases.append(b)
            input_size = size

        # Last hidden → output
        W_out = np.random.randn(input_size, self.output_size) * np.sqrt(2.0 / input_size)
        b_out = np.zeros((1, self.output_size))
        self.weights.append(W_out)
        self.biases.append(b_out)

        # Cache for activations during forward pass
        self.cache = {}

        if verbose:
            self._print_summary()

    def _print_summary(self):
        """Print model architecture summary."""
        print("=" * 70)
        print("TRADITIONAL MNIST CLASSIFIER")
        print("=" * 70)
        print()
        print("Architecture: Power-of-2 + ReLU Monoculture")
        print()

        total_params = 0
        print("Layers:")
        print(f"  Input:  784 pixels (28×28 MNIST)")

        for i, size in enumerate(self.layer_sizes):
            params = self.weights[i].size + self.biases[i].size
            total_params += params
            print(f"  Layer{i+1}: {size:3d} units - ReLU [{params:,} params]")

        output_params = self.weights[-1].size + self.biases[-1].size
        total_params += output_params
        print(f"  Output: {self.output_size:3d} units (10 digits) - softmax [{output_params:,} params]")
        print()
        print(f"Total parameters: {total_params:,}")
        print()
        print("Design Approach:")
        print("  • Power-of-2 layer sizes (arbitrary)")
        print("  • ReLU everywhere (monoculture)")
        print("  • No design rationale")
        print("  • Standard implementation")
        print()
        print("=" * 70)
        print()

    def _relu(self, z: np.ndarray) -> np.ndarray:
        """ReLU activation function."""
        return np.maximum(0, z)

    def _relu_derivative(self, z: np.ndarray) -> np.ndarray:
        """Derivative of ReLU."""
        return (z > 0).astype(float)

    def _softmax(self, z: np.ndarray) -> np.ndarray:
        """Numerically stable softmax."""
        exp_z = np.exp(z - np.max(z, axis=1, keepdims=True))
        return exp_z / np.sum(exp_z, axis=1, keepdims=True)

    def _one_hot(self, y: np.ndarray, num_classes: int = 10) -> np.ndarray:
        """Convert labels to one-hot encoding."""
        one_hot = np.zeros((y.shape[0], num_classes))
        one_hot[np.arange(y.shape[0]), y] = 1
        return one_hot

    def forward(self, X: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Forward pass through the network.

        Args:
            X: Input data (batch_size, 784)
            training: Whether in training mode (for caching activations)

        Returns:
            Predictions (batch_size, 10) - softmax probabilities
        """
        if training:
            self.cache = {'activations': [X], 'z_values': []}

        h = X

        # Hidden layers with ReLU
        for i in range(len(self.layer_sizes)):
            z = np.dot(h, self.weights[i]) + self.biases[i]
            h = self._relu(z)

            if training:
                self.cache['z_values'].append(z)
                self.cache['activations'].append(h)

        # Output layer with softmax
        z_out = np.dot(h, self.weights[-1]) + self.biases[-1]
        probs = self._softmax(z_out)

        if training:
            self.cache['z_values'].append(z_out)
            self.cache['probs'] = probs

        return probs

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class labels.

        Args:
            X: Input data (batch_size, 784)

        Returns:
            Predicted labels (batch_size,)
        """
        probs = self.forward(X, training=False)
        return np.argmax(probs, axis=1)

    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int = 10,
        batch_size: int = 32,
        validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        verbose: bool = True
    ) -> TrainingHistory:
        """
        Train the model.

        Args:
            X_train: Training data (n_samples, 784)
            y_train: Training labels (n_samples,)
            epochs: Number of training epochs
            batch_size: Batch size for mini-batch gradient descent
            validation_data: Optional (X_val, y_val) for validation
            verbose: Print training progress

        Returns:
            TrainingHistory object with loss and accuracy
        """
        n_samples = X_train.shape[0]
        n_batches = n_samples // batch_size

        # Initialize history
        history = TrainingHistory(
            train_loss=[],
            train_accuracy=[],
            val_loss=[] if validation_data else None,
            val_accuracy=[] if validation_data else None
        )

        if verbose:
            print("Training Traditional MNIST Classifier")
            print("-" * 70)

        for epoch in range(epochs):
            # Shuffle data
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            epoch_loss = 0
            for batch in range(n_batches):
                start_idx = batch * batch_size
                end_idx = start_idx + batch_size

                X_batch = X_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]

                # Forward pass
                probs = self.forward(X_batch, training=True)

                # Cross-entropy loss
                y_one_hot = self._one_hot(y_batch)
                loss = -np.mean(np.sum(y_one_hot * np.log(probs + 1e-8), axis=1))
                epoch_loss += loss

                # Backward pass
                grad = probs - y_one_hot  # Gradient w.r.t. softmax output

                # Backprop through layers (reverse order)
                for i in range(len(self.weights) - 1, -1, -1):
                    # Gradient for weights and biases
                    a_prev = self.cache['activations'][i]
                    grad_w = np.dot(a_prev.T, grad) / batch_size
                    grad_b = np.sum(grad, axis=0, keepdims=True) / batch_size

                    # Update weights and biases
                    self.weights[i] -= self.learning_rate * grad_w
                    self.biases[i] -= self.learning_rate * grad_b

                    # Propagate gradient to previous layer
                    if i > 0:
                        grad = np.dot(grad, self.weights[i].T)
                        # Apply ReLU derivative
                        grad = grad * self._relu_derivative(self.cache['z_values'][i-1])

            # Calculate metrics
            train_loss = epoch_loss / n_batches
            train_preds = self.predict(X_train)
            train_acc = np.mean(train_preds == y_train)

            history.train_loss.append(train_loss)
            history.train_accuracy.append(train_acc)

            # Validation metrics
            if validation_data:
                X_val, y_val = validation_data
                val_preds = self.predict(X_val)
                val_acc = np.mean(val_preds == y_val)
                val_probs = self.forward(X_val, training=False)
                y_val_one_hot = self._one_hot(y_val)
                val_loss = -np.mean(np.sum(y_val_one_hot * np.log(val_probs + 1e-8), axis=1))

                history.val_loss.append(val_loss)
                history.val_accuracy.append(val_acc)

                if verbose:
                    print(f"Epoch {epoch+1}/{epochs} - "
                          f"loss: {train_loss:.4f} - acc: {train_acc:.4f} - "
                          f"val_loss: {val_loss:.4f} - val_acc: {val_acc:.4f}")
            else:
                if verbose:
                    print(f"Epoch {epoch+1}/{epochs} - "
                          f"loss: {train_loss:.4f} - acc: {train_acc:.4f}")

        self.history = history
        return history

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        Evaluate model on test data.

        Args:
            X_test: Test data (n_samples, 784)
            y_test: Test labels (n_samples,)

        Returns:
            Test accuracy (0-1)
        """
        predictions = self.predict(X_test)
        accuracy = np.mean(predictions == y_test)
        return accuracy
