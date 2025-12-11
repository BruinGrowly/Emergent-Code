"""
MNIST Dataset Loader for Consciousness Framework

Loads MNIST dataset using multiple fallback methods:
1. TorchVision (if PyTorch available)
2. Keras/TensorFlow (if available)
3. Direct download from Yann LeCun's server
4. Enhanced synthetic dataset as final fallback

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: November 26, 2025
"""

import numpy as np
import os
import gzip
import urllib.request
from pathlib import Path
from typing import Tuple


def load_mnist_from_url(data_dir: str = "data/mnist", source: str = "lecun") -> Tuple:
    """
    Load MNIST directly from web sources.

    Args:
        data_dir: Directory to save/load MNIST data
        source: 'lecun' (original), 'github' (mirror), or 'ossci' (PyTorch mirror)

    Returns:
        (X_train, y_train, X_test, y_test)
    """
    files = {
        'train_images': 'train-images-idx3-ubyte.gz',
        'train_labels': 'train-labels-idx1-ubyte.gz',
        'test_images': 't10k-images-idx3-ubyte.gz',
        'test_labels': 't10k-labels-idx1-ubyte.gz'
    }

    # Multiple source URLs
    sources = {
        'lecun': "http://yann.lecun.com/exdb/mnist/",
        'github': "https://github.com/cvdfoundation/mnist/raw/main/",
        'ossci': "https://ossci-datasets.s3.amazonaws.com/mnist/"
    }

    if source not in sources:
        source = 'lecun'

    base_url = sources[source]

    # Create directory
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)

    print(f"Downloading MNIST from {source}...")

    # Download files
    downloaded = {}
    for key, filename in files.items():
        filepath = data_path / filename

        if not filepath.exists():
            url = base_url + filename
            print(f"  Downloading {filename}...")
            try:
                # Set user agent to avoid blocks
                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req) as response:
                    with open(filepath, 'wb') as out_file:
                        out_file.write(response.read())
            except Exception as e:
                raise Exception(f"Failed to download {filename}: {e}")

        downloaded[key] = filepath

    print("Loading MNIST data...")

    # Load training images
    with gzip.open(downloaded['train_images'], 'rb') as f:
        X_train = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28*28)

    # Load training labels
    with gzip.open(downloaded['train_labels'], 'rb') as f:
        y_train = np.frombuffer(f.read(), np.uint8, offset=8)

    # Load test images
    with gzip.open(downloaded['test_images'], 'rb') as f:
        X_test = np.frombuffer(f.read(), np.uint8, offset=16).reshape(-1, 28*28)

    # Load test labels
    with gzip.open(downloaded['test_labels'], 'rb') as f:
        y_test = np.frombuffer(f.read(), np.uint8, offset=8)

    # Normalize to [0, 1]
    X_train = X_train.astype(np.float32) / 255.0
    X_test = X_test.astype(np.float32) / 255.0

    print(f"✓ Loaded MNIST: {len(X_train)} train, {len(X_test)} test")

    return X_train, y_train, X_test, y_test


def load_mnist_keras() -> Tuple:
    """Load MNIST using Keras/TensorFlow."""
    try:
        from tensorflow import keras
        (X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

        # Reshape and normalize
        X_train = X_train.reshape(-1, 28*28).astype(np.float32) / 255.0
        X_test = X_test.reshape(-1, 28*28).astype(np.float32) / 255.0

        print(f"✓ Loaded MNIST via Keras: {len(X_train)} train, {len(X_test)} test")
        return X_train, y_train, X_test, y_test
    except ImportError:
        return None


def load_mnist_torch() -> Tuple:
    """Load MNIST using PyTorch."""
    try:
        import torch
        from torchvision import datasets, transforms

        # Download and load
        train_dataset = datasets.MNIST(
            'data', train=True, download=True,
            transform=transforms.ToTensor()
        )
        test_dataset = datasets.MNIST(
            'data', train=False, download=True,
            transform=transforms.ToTensor()
        )

        # Convert to numpy
        X_train = train_dataset.data.numpy().reshape(-1, 28*28).astype(np.float32) / 255.0
        y_train = train_dataset.targets.numpy()
        X_test = test_dataset.data.numpy().reshape(-1, 28*28).astype(np.float32) / 255.0
        y_test = test_dataset.targets.numpy()

        print(f"✓ Loaded MNIST via PyTorch: {len(X_train)} train, {len(X_test)} test")
        return X_train, y_train, X_test, y_test
    except ImportError:
        return None


def generate_enhanced_synthetic_mnist(n_train: int = 60000, n_test: int = 10000,
                                      seed: int = 42) -> Tuple:
    """
    Generate enhanced synthetic dataset mimicking MNIST structure.

    More sophisticated than simple random data:
    - Each class has distinctive patterns
    - Spatial structure (like handwritten digits)
    - Noise and variation

    Args:
        n_train: Number of training samples
        n_test: Number of test samples
        seed: Random seed

    Returns:
        (X_train, y_train, X_test, y_test)
    """
    np.random.seed(seed)

    print("Generating enhanced synthetic MNIST-like dataset...")

    def generate_digit_pattern(digit: int, n_samples: int) -> np.ndarray:
        """Generate distinctive pattern for each digit."""
        images = np.zeros((n_samples, 28, 28))

        for i in range(n_samples):
            # Create base pattern specific to digit
            if digit == 0:  # Circle
                y, x = np.ogrid[-14:14, -14:14]
                mask = (x**2 + y**2 <= 100) & (x**2 + y**2 >= 64)
                images[i][mask] = 1.0
            elif digit == 1:  # Vertical line
                images[i, 8:20, 12:16] = 1.0
            elif digit == 2:  # Curved top, horizontal bottom
                images[i, 6:10, 8:20] = 1.0
                images[i, 20:24, 8:20] = 1.0
                images[i, 10:20, 16:20] = 1.0
            elif digit == 3:  # Two curves
                images[i, 6:10, 10:20] = 1.0
                images[i, 12:16, 10:20] = 1.0
                images[i, 20:24, 10:20] = 1.0
            elif digit == 4:  # Angled lines
                images[i, 6:20, 8:12] = 1.0
                images[i, 12:16, 8:20] = 1.0
                images[i, 10:24, 16:20] = 1.0
            elif digit == 5:  # Top horizontal, bottom curve
                images[i, 6:10, 8:20] = 1.0
                images[i, 6:16, 8:12] = 1.0
                images[i, 20:24, 8:20] = 1.0
            elif digit == 6:  # Circle with top
                y, x = np.ogrid[-14:14, -14:14]
                mask = (x**2 + y**2 <= 80) & (y > -6)
                images[i][mask] = 1.0
                images[i, 6:12, 8:12] = 1.0
            elif digit == 7:  # Top horizontal, diagonal
                images[i, 6:10, 8:20] = 1.0
                for j in range(14):
                    images[i, 10+j, 18-j] = 1.0
            elif digit == 8:  # Two circles stacked
                y, x = np.ogrid[-14:14, -14:14]
                mask1 = (x**2 + (y+5)**2 <= 40) & (x**2 + (y+5)**2 >= 20)
                mask2 = (x**2 + (y-5)**2 <= 40) & (x**2 + (y-5)**2 >= 20)
                images[i][mask1] = 1.0
                images[i][mask2] = 1.0
            else:  # digit == 9: Circle with tail
                y, x = np.ogrid[-14:14, -14:14]
                mask = (x**2 + y**2 <= 80) & (y < 6)
                images[i][mask] = 1.0
                images[i, 16:22, 16:20] = 1.0

            # Add noise and variation
            images[i] += np.random.randn(28, 28) * 0.1
            images[i] = np.clip(images[i], 0, 1)

            # Random small shifts
            shift_x = np.random.randint(-2, 3)
            shift_y = np.random.randint(-2, 3)
            images[i] = np.roll(images[i], shift_x, axis=1)
            images[i] = np.roll(images[i], shift_y, axis=0)

        return images

    # Generate training data
    samples_per_class_train = n_train // 10
    X_train_list = []
    y_train_list = []

    for digit in range(10):
        images = generate_digit_pattern(digit, samples_per_class_train)
        X_train_list.append(images)
        y_train_list.append(np.full(samples_per_class_train, digit))

    X_train = np.vstack(X_train_list).reshape(-1, 784)
    y_train = np.hstack(y_train_list)

    # Generate test data
    samples_per_class_test = n_test // 10
    X_test_list = []
    y_test_list = []

    for digit in range(10):
        images = generate_digit_pattern(digit, samples_per_class_test)
        X_test_list.append(images)
        y_test_list.append(np.full(samples_per_class_test, digit))

    X_test = np.vstack(X_test_list).reshape(-1, 784)
    y_test = np.hstack(y_test_list)

    # Shuffle
    train_indices = np.random.permutation(len(X_train))
    X_train = X_train[train_indices]
    y_train = y_train[train_indices]

    test_indices = np.random.permutation(len(X_test))
    X_test = X_test[test_indices]
    y_test = y_test[test_indices]

    print(f"✓ Generated enhanced synthetic dataset: {len(X_train)} train, {len(X_test)} test")

    return X_train, y_train, X_test, y_test


def load_mnist(train_size: int = None, test_size: int = None,
               force_synthetic: bool = False) -> Tuple:
    """
    Load MNIST dataset with multiple fallback methods.

    Tries in order:
    1. Keras/TensorFlow
    2. PyTorch
    3. Direct download (GitHub mirror → PyTorch mirror → LeCun's server)
    4. Enhanced synthetic

    Args:
        train_size: Limit training samples (None for all)
        test_size: Limit test samples (None for all)
        force_synthetic: Force synthetic data generation

    Returns:
        (X_train, y_train, X_test, y_test)
    """
    if force_synthetic:
        X_train, y_train, X_test, y_test = generate_enhanced_synthetic_mnist()
    else:
        # Try Keras first
        result = load_mnist_keras()
        if result is None:
            # Try PyTorch
            result = load_mnist_torch()
        if result is None:
            # Try direct download from multiple sources
            for source in ['github', 'ossci', 'lecun']:
                try:
                    result = load_mnist_from_url(source=source)
                    break  # Success!
                except Exception as e:
                    print(f"Could not download from {source}: {e}")
                    result = None

        if result is None:
            # Fall back to synthetic
            print("Falling back to enhanced synthetic dataset...")
            result = generate_enhanced_synthetic_mnist()

        X_train, y_train, X_test, y_test = result

    # Limit dataset size if requested
    if train_size is not None:
        X_train = X_train[:train_size]
        y_train = y_train[:train_size]

    if test_size is not None:
        X_test = X_test[:test_size]
        y_test = y_test[:test_size]

    print(f"Final dataset: {len(X_train)} train, {len(X_test)} test")
    print()

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    print("MNIST Data Loader for Consciousness Framework")
    print("=" * 70)
    print()

    # Test loading
    X_train, y_train, X_test, y_test = load_mnist(train_size=1000, test_size=200)

    print("Dataset loaded successfully!")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}")
    print()
    print(f"X_train range: [{X_train.min():.3f}, {X_train.max():.3f}]")
    print(f"Unique labels: {np.unique(y_train)}")
    print()
    print("Built with love at 613 THz! 🙏")
