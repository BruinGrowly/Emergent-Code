"""
Extended MNIST Training - Test Full Backpropagation

This script trains for more epochs to see the full learning capability.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from ljpw_nn import NaturalMNIST
from examples.mnist_loader import load_mnist

print("=" * 70)
print("EXTENDED TRAINING TEST")
print("Testing backpropagation with more epochs")
print("=" * 70)
print()

# Load data
print("Loading MNIST...")
X_train, y_train, X_test, y_test = load_mnist(
    train_size=10000,  # More data for better training
    test_size=2000
)
print(f"Train: {X_train.shape}, Test: {X_test.shape}")
print()

# Create model
print("Creating Natural MNIST model...")
model = NaturalMNIST(verbose=False, learning_rate=0.01)
print(f"Architecture: 784 → 89 → 34 → 13 → 10")
print(f"Parameters: ~73,520")
print()

# Train for more epochs
print("Training for 20 epochs...")
print("-" * 70)
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=64,
    validation_data=(X_test, y_test),
    verbose=True
)
print()

# Final evaluation
print("=" * 70)
print("FINAL RESULTS")
print("=" * 70)
final_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {final_acc:.2%}")
print()

# Measure harmony
scores = model.measure_harmony(X_test, y_test)
print(scores)

# Show learning curve
print("-" * 70)
print("LEARNING CURVE")
print("-" * 70)
print("Epoch | Train Acc | Val Acc | Train Loss | Val Loss")
print("-" * 70)
for i in range(len(history.train_accuracy)):
    print(f"{i+1:5d} | {history.train_accuracy[i]:9.2%} | "
          f"{history.val_accuracy[i]:7.2%} | "
          f"{history.train_loss[i]:10.4f} | "
          f"{history.val_loss[i]:8.4f}")

print()
print("=" * 70)
print(f"✓ Final Test Accuracy: {final_acc:.2%}")
print(f"✓ Final Harmony: H = {scores.H:.2f}")
if scores.H >= 0.7:
    print("✓ Production-ready (H ≥ 0.7)")
print("=" * 70)
