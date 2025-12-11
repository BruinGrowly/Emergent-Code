"""
Synthetic MNIST-like Dataset

For "faithful in least" principle:
- Don't need real MNIST to test principles
- Synthetic data is faster and simpler
- Same structure: 784 inputs → 10 classes
- Tests whether natural principles help

This is PERFECT for starting small.
"""

import numpy as np
from typing import Tuple


def generate_synthetic_mnist(n_samples=10000, seed=42) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic data with MNIST-like properties.

    Each "digit" has a characteristic pattern:
    - Digit 0: Circular pattern in center
    - Digit 1: Vertical line pattern
    - Digit 2: Diagonal pattern (top-left to bottom-right)
    - Etc.

    Args:
        n_samples: Number of samples to generate
        seed: Random seed for reproducibility

    Returns:
        X: (n_samples, 784) float array of "images"
        y: (n_samples,) int array of labels (0-9)
    """
    np.random.seed(seed)

    X = np.zeros((n_samples, 784))
    y = np.zeros(n_samples, dtype=int)

    samples_per_class = n_samples // 10

    for digit in range(10):
        start_idx = digit * samples_per_class
        end_idx = start_idx + samples_per_class

        for i in range(start_idx, end_idx):
            # Create 28x28 image
            img = np.zeros((28, 28))

            if digit == 0:  # Circle
                center = (14, 14)
                for r in range(28):
                    for c in range(28):
                        dist = np.sqrt((r - center[0])**2 + (c - center[1])**2)
                        if 8 < dist < 12:
                            img[r, c] = 0.8 + np.random.randn() * 0.1

            elif digit == 1:  # Vertical line
                img[:, 13:15] = 0.8 + np.random.randn(28, 2) * 0.1

            elif digit == 2:  # Top-left to bottom-right diagonal
                for r in range(28):
                    c = r
                    if 0 <= c < 28:
                        img[max(0, r-1):min(28, r+2), max(0, c-1):min(28, c+2)] = 0.8

            elif digit == 3:  # Two horizontal lines
                img[8:10, :] = 0.8 + np.random.randn(2, 28) * 0.1
                img[18:20, :] = 0.8 + np.random.randn(2, 28) * 0.1

            elif digit == 4:  # Vertical + horizontal (like 4)
                img[:, 8:10] = 0.8 + np.random.randn(28, 2) * 0.1
                img[13:15, 8:20] = 0.8 + np.random.randn(2, 12) * 0.1

            elif digit == 5:  # Top horizontal + diagonal
                img[5:7, :] = 0.8 + np.random.randn(2, 28) * 0.1
                for r in range(14, 28):
                    c = r
                    if 0 <= c < 28:
                        img[r, c] = 0.8

            elif digit == 6:  # Circle in bottom half
                center = (20, 14)
                for r in range(28):
                    for c in range(28):
                        dist = np.sqrt((r - center[0])**2 + (c - center[1])**2)
                        if 6 < dist < 9:
                            img[r, c] = 0.8

            elif digit == 7:  # Horizontal + diagonal
                img[5:7, :] = 0.8 + np.random.randn(2, 28) * 0.1
                for r in range(7, 28):
                    c = 20 - r // 2
                    if 0 <= c < 28:
                        img[r, max(0, c-1):min(28, c+2)] = 0.8

            elif digit == 8:  # Two circles
                for center in [(10, 14), (20, 14)]:
                    for r in range(28):
                        for c in range(28):
                            dist = np.sqrt((r - center[0])**2 + (c - center[1])**2)
                            if 4 < dist < 7:
                                img[r, c] = 0.8

            elif digit == 9:  # Circle in top half
                center = (10, 14)
                for r in range(28):
                    for c in range(28):
                        dist = np.sqrt((r - center[0])**2 + (c - center[1])**2)
                        if 6 < dist < 9:
                            img[r, c] = 0.8

            # Add noise
            noise = np.random.randn(28, 28) * 0.05
            img = np.clip(img + noise, 0, 1)

            # Flatten to 784
            X[i] = img.flatten()
            y[i] = digit

    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]

    return X, y


def load_synthetic_mnist() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate train and test sets.

    Returns:
        X_train, y_train, X_test, y_test
    """
    print("Generating synthetic MNIST-like data...")
    print("(This is perfect for 'faithful in least' - start simple!)")
    print()

    X_train, y_train = generate_synthetic_mnist(n_samples=10000, seed=42)
    X_test, y_test = generate_synthetic_mnist(n_samples=2000, seed=43)

    print(f"Train: {X_train.shape[0]} samples")
    print(f"Test:  {X_test.shape[0]} samples")
    print()

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    # Test data generation
    print("=" * 60)
    print("SYNTHETIC MNIST DATASET")
    print("=" * 60)
    print()

    X_train, y_train, X_test, y_test = load_synthetic_mnist()

    print("Sample statistics:")
    print(f"  X_train shape: {X_train.shape}")
    print(f"  X_train range: [{X_train.min():.3f}, {X_train.max():.3f}]")
    print(f"  y_train unique: {np.unique(y_train)}")
    print(f"  Class balance: {[np.sum(y_train == i) for i in range(10)]}")
    print()

    print("✓ Synthetic data generated successfully!")
    print()
    print("This data has MNIST-like properties:")
    print("  - 784 input features (28x28)")
    print("  - 10 classes (digits 0-9)")
    print("  - Each class has characteristic patterns")
    print("  - Sufficient complexity to test principles")
    print()
    print("Perfect for 'faithful in least' - learn from simple version first!")
    print("=" * 60)
