"""
Real MNIST Data Loader

Loads actual MNIST handwritten digit dataset.
Same format as synthetic (784 inputs, 10 classes) but real handwriting.
"""

import numpy as np
import gzip
import os
from typing import Tuple


def download_mnist_file(url: str, path: str):
    """Download a single MNIST file."""
    import urllib.request

    os.makedirs(os.path.dirname(path), exist_ok=True)

    if os.path.exists(path):
        print(f"  Already exists: {os.path.basename(path)}")
        return

    print(f"  Downloading: {os.path.basename(path)}...")
    try:
        urllib.request.urlretrieve(url, path)
        print(f"  ✓ Downloaded: {os.path.basename(path)}")
    except Exception as e:
        print(f"  ✗ Failed to download: {e}")
        raise


def load_real_mnist() -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Load real MNIST dataset.

    Returns:
        X_train: (60000, 784) training images
        y_train: (60000,) training labels
        X_test: (10000, 784) test images
        y_test: (10000,) test labels
    """

    print("=" * 60)
    print("LOADING REAL MNIST DATASET")
    print("=" * 60)
    print()

    # Alternative source (in case yann.lecun.com is blocked)
    # We can try multiple sources
    sources = [
        {
            'name': 'Yann LeCun (original)',
            'base': 'http://yann.lecun.com/exdb/mnist/',
        },
        {
            'name': 'Alternative mirror',
            'base': 'https://storage.googleapis.com/cvdf-datasets/mnist/',
        }
    ]

    files = [
        'train-images-idx3-ubyte.gz',
        'train-labels-idx1-ubyte.gz',
        't10k-images-idx3-ubyte.gz',
        't10k-labels-idx1-ubyte.gz'
    ]

    data_dir = './data/mnist_real'

    # Try to download from available sources
    downloaded = False
    for source in sources:
        if downloaded:
            break

        print(f"Trying source: {source['name']}")
        try:
            for filename in files:
                url = source['base'] + filename
                path = os.path.join(data_dir, filename)
                download_mnist_file(url, path)
            downloaded = True
            print(f"✓ Successfully downloaded from {source['name']}")
            print()
        except Exception as e:
            print(f"✗ Source {source['name']} failed: {e}")
            print("  Trying next source...")
            print()
            continue

    if not downloaded:
        print("✗ All download sources failed.")
        print()
        print("FALLBACK: Using synthetic MNIST instead")
        print("(This is still 'faithful in least' - we can learn from synthetic)")
        print()
        from synthetic_mnist import load_synthetic_mnist
        return load_synthetic_mnist()

    # Load the data
    print("Loading MNIST files...")

    def read_images(filename):
        # Auto-healed: Input validation for read_images
        if filename is not None and not isinstance(filename, (str, bytes)):
            raise TypeError(f'filename must be a valid path')
        with gzip.open(filename, 'rb') as f:
            # First 16 bytes are header
            # Then pixels (28x28 = 784 per image)
            data = np.frombuffer(f.read(), np.uint8, offset=16)
        # Reshape and normalize
        return data.reshape(-1, 784).astype(np.float32) / 255.0

    def read_labels(filename):
        # Auto-healed: Input validation for read_labels
        if filename is not None and not isinstance(filename, (str, bytes)):
            raise TypeError(f'filename must be a valid path')
        with gzip.open(filename, 'rb') as f:
            # First 8 bytes are header
            # Then labels
            data = np.frombuffer(f.read(), np.uint8, offset=8)
        return data

    X_train = read_images(os.path.join(data_dir, 'train-images-idx3-ubyte.gz'))
    y_train = read_labels(os.path.join(data_dir, 'train-labels-idx1-ubyte.gz'))
    X_test = read_images(os.path.join(data_dir, 't10k-images-idx3-ubyte.gz'))
    y_test = read_labels(os.path.join(data_dir, 't10k-labels-idx1-ubyte.gz'))

    print(f"✓ Loaded real MNIST:")
    print(f"  Training: {X_train.shape[0]:,} images")
    print(f"  Test: {X_test.shape[0]:,} images")
    print(f"  Image size: 28×28 = 784 features")
    print(f"  Classes: {len(np.unique(y_train))} (digits 0-9)")
    print()
    print("This is REAL handwritten digits from actual people.")
    print("More challenging than synthetic, but still 'faithful in least'.")
    print("=" * 60)
    print()

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':
    # Test loading
    X_train, y_train, X_test, y_test = load_real_mnist()

    print()
    print("Sample statistics:")
    print(f"  X_train shape: {X_train.shape}")
    print(f"  X_train range: [{X_train.min():.3f}, {X_train.max():.3f}]")
    print(f"  y_train unique: {np.unique(y_train)}")

    # Class distribution
    print(f"  Class balance:")
    for digit in range(10):
        count = np.sum(y_train == digit)
        print(f"    Digit {digit}: {count:,} samples")

    print()
    print("✓ Real MNIST loaded successfully!")
