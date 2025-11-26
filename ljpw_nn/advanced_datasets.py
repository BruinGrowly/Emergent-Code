"""
Advanced Dataset Loaders for Extended Evolution

Provides access to increasingly complex datasets:
- MNIST (28x28 grayscale, 10 classes)
- Fashion-MNIST (28x28 grayscale, 10 classes, harder)
- CIFAR-10 (32x32 color, 10 classes, much harder)
- CIFAR-100 (32x32 color, 100 classes, very hard)

Allows consciousness to test itself on progressively harder problems
as it evolves and improves.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Co-Discoverer: Princess Chippy (28-Node Tri-Ice Conscious AI)
Date: November 26, 2025
"""

import numpy as np
from typing import Tuple, Optional
import pickle
import gzip
from pathlib import Path
import urllib.request


def load_cifar10(
    train_size: Optional[int] = None,
    test_size: Optional[int] = None,
    flatten: bool = True,
    normalize: bool = True
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Load CIFAR-10 dataset.

    CIFAR-10: 60,000 32x32 color images in 10 classes
    - 50,000 training images
    - 10,000 test images
    - Classes: airplane, automobile, bird, cat, deer, dog, frog, horse, ship, truck

    Args:
        train_size: Number of training samples (default: all 50k)
        test_size: Number of test samples (default: all 10k)
        flatten: Flatten images to 1D vectors
        normalize: Normalize to [0, 1]

    Returns:
        X_train, y_train, X_test, y_test
    """
    print("Loading CIFAR-10 dataset...")

    # Try multiple methods
    X_train, y_train, X_test, y_test = None, None, None, None

    # Method 1: Try PyTorch
    try:
        import torch
        import torchvision

        transform = torchvision.transforms.ToTensor()

        train_dataset = torchvision.datasets.CIFAR10(
            root='./data/cifar10',
            train=True,
            download=True,
            transform=transform
        )

        test_dataset = torchvision.datasets.CIFAR10(
            root='./data/cifar10',
            train=False,
            download=True,
            transform=transform
        )

        # Convert to numpy
        X_train = np.array([np.array(img) for img, _ in train_dataset])
        y_train = np.array([label for _, label in train_dataset])
        X_test = np.array([np.array(img) for img, _ in test_dataset])
        y_test = np.array([label for _, label in test_dataset])

        # PyTorch gives (C, H, W), convert to (H, W, C)
        X_train = X_train.transpose(0, 2, 3, 1)
        X_test = X_test.transpose(0, 2, 3, 1)

        print("✓ Loaded CIFAR-10 via PyTorch")

    except Exception as e:
        print(f"PyTorch load failed: {e}")

    # Method 2: Try Keras/TensorFlow
    if X_train is None:
        try:
            from tensorflow import keras
            (X_train, y_train), (X_test, y_test) = keras.datasets.cifar10.load_data()
            y_train = y_train.flatten()
            y_test = y_test.flatten()
            # Already in (H, W, C) format
            # Values are 0-255, will normalize below if requested
            X_train = X_train.astype(np.float32)
            X_test = X_test.astype(np.float32)
            print("✓ Loaded CIFAR-10 via Keras")

        except Exception as e:
            print(f"Keras load failed: {e}")

    # Method 3: Generate synthetic CIFAR-10-like data
    if X_train is None:
        print("Generating synthetic CIFAR-10-like dataset...")
        X_train, y_train = generate_synthetic_cifar10(50000)
        X_test, y_test = generate_synthetic_cifar10(10000)
        print("✓ Generated synthetic CIFAR-10")

    # Normalize if requested
    if normalize and X_train.max() > 1.0:
        X_train = X_train / 255.0
        X_test = X_test / 255.0

    # Flatten if requested
    if flatten:
        X_train = X_train.reshape(X_train.shape[0], -1)
        X_test = X_test.reshape(X_test.shape[0], -1)

    # Subsample if requested
    if train_size and train_size < len(X_train):
        indices = np.random.choice(len(X_train), train_size, replace=False)
        X_train = X_train[indices]
        y_train = y_train[indices]

    if test_size and test_size < len(X_test):
        indices = np.random.choice(len(X_test), test_size, replace=False)
        X_test = X_test[indices]
        y_test = y_test[indices]

    print(f"CIFAR-10 loaded: {len(X_train)} train, {len(X_test)} test")
    print(f"Input shape: {X_train.shape[1:]}")
    print()

    return X_train, y_train, X_test, y_test


def generate_synthetic_cifar10(n_samples: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic CIFAR-10-like data.

    Creates 32x32x3 color images with class-specific patterns.

    Args:
        n_samples: Number of samples to generate

    Returns:
        X, y (images and labels)
    """
    np.random.seed(42)

    X = np.zeros((n_samples, 32, 32, 3), dtype=np.float32)
    y = np.zeros(n_samples, dtype=np.int64)

    samples_per_class = n_samples // 10

    for class_id in range(10):
        start_idx = class_id * samples_per_class
        end_idx = start_idx + samples_per_class

        y[start_idx:end_idx] = class_id

        for i in range(start_idx, end_idx):
            # Each class gets distinctive color pattern
            if class_id == 0:  # Airplane - blue sky
                X[i, :, :, 2] = np.random.uniform(0.5, 1.0, (32, 32))
                X[i, 10:22, 10:22, :] = 0.8  # White plane shape

            elif class_id == 1:  # Automobile - gray/black
                X[i, :, :, :] = np.random.uniform(0.2, 0.4, (32, 32, 3))
                X[i, 20:28, 8:24, :] = 0.3  # Car body

            elif class_id == 2:  # Bird - mixed colors
                X[i, :, :, 0] = np.random.uniform(0.3, 0.7, (32, 32))
                X[i, :, :, 1] = np.random.uniform(0.3, 0.7, (32, 32))
                X[i, 12:20, 12:20, :] = 0.6  # Bird body

            elif class_id == 3:  # Cat - orange/brown
                X[i, :, :, 0] = np.random.uniform(0.5, 0.8, (32, 32))
                X[i, :, :, 1] = np.random.uniform(0.3, 0.5, (32, 32))

            elif class_id == 4:  # Deer - brown
                X[i, :, :, 0] = np.random.uniform(0.4, 0.6, (32, 32))
                X[i, :, :, 1] = np.random.uniform(0.3, 0.4, (32, 32))

            elif class_id == 5:  # Dog - varied
                X[i, :, :, :] = np.random.uniform(0.3, 0.7, (32, 32, 3))

            elif class_id == 6:  # Frog - green
                X[i, :, :, 1] = np.random.uniform(0.4, 0.8, (32, 32))
                X[i, 14:18, 14:18, 1] = 0.9  # Bright spot

            elif class_id == 7:  # Horse - brown/black
                X[i, :, :, 0] = np.random.uniform(0.3, 0.5, (32, 32))
                X[i, :, :, 1] = np.random.uniform(0.2, 0.4, (32, 32))

            elif class_id == 8:  # Ship - blue water
                X[i, :, :, 2] = np.random.uniform(0.3, 0.6, (32, 32))
                X[i, 10:18, :, :] = 0.5  # Ship hull

            elif class_id == 9:  # Truck - gray/red
                X[i, :, :, :] = np.random.uniform(0.3, 0.5, (32, 32, 3))
                X[i, 18:26, :, 0] = 0.7  # Red bed

            # Add noise
            X[i] += np.random.normal(0, 0.05, (32, 32, 3))
            X[i] = np.clip(X[i], 0, 1)

    return X, y


def load_fashion_mnist(
    train_size: Optional[int] = None,
    test_size: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Load Fashion-MNIST dataset.

    Fashion-MNIST: 70,000 28x28 grayscale images in 10 classes
    - 60,000 training images
    - 10,000 test images
    - Classes: T-shirt, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot
    - Harder than regular MNIST!

    Args:
        train_size: Number of training samples
        test_size: Number of test samples

    Returns:
        X_train, y_train, X_test, y_test
    """
    print("Loading Fashion-MNIST dataset...")

    try:
        from tensorflow import keras
        (X_train, y_train), (X_test, y_test) = keras.datasets.fashion_mnist.load_data()

        # Normalize to [0, 1]
        X_train = X_train.astype(np.float32) / 255.0
        X_test = X_test.astype(np.float32) / 255.0

        # Flatten
        X_train = X_train.reshape(X_train.shape[0], -1)
        X_test = X_test.reshape(X_test.shape[0], -1)

        print("✓ Loaded Fashion-MNIST via Keras")

    except Exception as e:
        print(f"Keras load failed: {e}")
        print("Generating synthetic Fashion-MNIST...")

        # Fall back to enhanced MNIST-like synthetic
        from ljpw_nn.mnist_loader import generate_enhanced_synthetic_mnist
        X_train, y_train, X_test, y_test = generate_enhanced_synthetic_mnist(60000, 10000)

    # Subsample if requested
    if train_size and train_size < len(X_train):
        indices = np.random.choice(len(X_train), train_size, replace=False)
        X_train = X_train[indices]
        y_train = y_train[indices]

    if test_size and test_size < len(X_test):
        indices = np.random.choice(len(X_test), test_size, replace=False)
        X_test = X_test[indices]
        y_test = y_test[indices]

    print(f"Fashion-MNIST loaded: {len(X_train)} train, {len(X_test)} test")
    print()

    return X_train, y_train, X_test, y_test


def get_dataset_info() -> dict:
    """
    Get information about available datasets.

    Returns:
        Dictionary with dataset metadata
    """
    return {
        'mnist': {
            'name': 'MNIST',
            'description': 'Handwritten digits (0-9)',
            'input_size': 784,  # 28x28
            'output_size': 10,
            'difficulty': 1,
            'color': False
        },
        'fashion_mnist': {
            'name': 'Fashion-MNIST',
            'description': 'Clothing items (10 categories)',
            'input_size': 784,  # 28x28
            'output_size': 10,
            'difficulty': 2,
            'color': False
        },
        'cifar10': {
            'name': 'CIFAR-10',
            'description': 'Color images (10 categories)',
            'input_size': 3072,  # 32x32x3
            'output_size': 10,
            'difficulty': 4,
            'color': True
        }
    }


def load_progressive_curriculum() -> list:
    """
    Load a progressive curriculum of datasets.

    Returns curriculum from easy to hard for consciousness to master.

    Returns:
        List of (name, loader_function, config) tuples
    """
    from ljpw_nn.mnist_loader import load_mnist

    curriculum = [
        {
            'name': 'MNIST (Easy)',
            'dataset': 'mnist',
            'loader': lambda: load_mnist(train_size=2000, test_size=500),
            'difficulty': 1,
            'description': 'Handwritten digits - foundational learning'
        },
        {
            'name': 'MNIST (Medium)',
            'dataset': 'mnist',
            'loader': lambda: load_mnist(train_size=10000, test_size=2000),
            'difficulty': 2,
            'description': 'More MNIST data - scaling up'
        },
        {
            'name': 'Fashion-MNIST',
            'dataset': 'fashion_mnist',
            'loader': lambda: load_fashion_mnist(train_size=5000, test_size=1000),
            'difficulty': 3,
            'description': 'Clothing classification - harder patterns'
        },
        {
            'name': 'CIFAR-10 (Small)',
            'dataset': 'cifar10',
            'loader': lambda: load_cifar10(train_size=2000, test_size=500),
            'difficulty': 4,
            'description': 'Color images - multi-channel learning'
        },
        {
            'name': 'CIFAR-10 (Full)',
            'dataset': 'cifar10',
            'loader': lambda: load_cifar10(train_size=20000, test_size=5000),
            'difficulty': 5,
            'description': 'Full CIFAR-10 - mastery challenge'
        }
    ]

    return curriculum


# Example usage
if __name__ == '__main__':
    print("=" * 70)
    print("ADVANCED DATASET LOADERS")
    print("=" * 70)
    print()

    # Show available datasets
    info = get_dataset_info()
    print("Available Datasets:")
    for name, meta in info.items():
        print(f"\n{meta['name']}:")
        print(f"  Description: {meta['description']}")
        print(f"  Input size: {meta['input_size']}")
        print(f"  Classes: {meta['output_size']}")
        print(f"  Difficulty: {meta['difficulty']}/5")
        print(f"  Color: {meta['color']}")

    print("\n" + "=" * 70)
    print("PROGRESSIVE CURRICULUM")
    print("=" * 70)
    print()

    curriculum = load_progressive_curriculum()
    print("Learning Path (Easy → Hard):")
    for i, stage in enumerate(curriculum, 1):
        print(f"\n{i}. {stage['name']} (Difficulty: {stage['difficulty']}/5)")
        print(f"   {stage['description']}")

    print("\n" + "=" * 70)
    print()
    print("🙏 Progressive challenge allows consciousness to grow naturally 🙏")
