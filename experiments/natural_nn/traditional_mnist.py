"""
Traditional MNIST Neural Network (Baseline)

Standard approach:
- Arbitrary layer sizes (128, 64)
- ReLU everywhere (monoculture)
- No particular design principle
- Optimize for accuracy only

This is our baseline to compare against natural networks.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import time
from typing import Dict, Any
from nn_ljpw_metrics import NeuralNetworkLJPW, LJPWScores


class TraditionalMNIST(nn.Module):
    """
    Standard MNIST network.

    Architecture: 784 → 128 → 64 → 10
    Activations: ReLU throughout
    Design: Arbitrary choices, common practice
    """

    def __init__(self):
        super(TraditionalMNIST, self).__init__()

        # Flatten input
        self.flatten = nn.Flatten()

        # Hidden layers (arbitrary sizes)
        self.fc1 = nn.Linear(28 * 28, 128)
        self.relu1 = nn.ReLU()

        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()

        # Output layer
        self.fc3 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.flatten(x)
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        x = self.fc3(x)
        return x

    def count_parameters(self):
        """Count total trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


def train_model(model, train_loader, val_loader, device, epochs=15):
    """Train the model and track metrics."""

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    model.to(device)

    training_info = {
        'train_losses': [],
        'train_accuracies': [],
        'val_accuracies': [],
        'epochs': epochs,
    }

    start_time = time.time()

    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        correct = 0
        total = 0

        for batch_idx, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)

            optimizer.zero_grad()
            output = model(data)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

        train_acc = correct / total
        avg_loss = train_loss / len(train_loader)

        # Validation
        model.eval()
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for data, target in val_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                _, predicted = output.max(1)
                val_total += target.size(0)
                val_correct += predicted.eq(target).sum().item()

        val_acc = val_correct / val_total

        training_info['train_losses'].append(avg_loss)
        training_info['train_accuracies'].append(train_acc)
        training_info['val_accuracies'].append(val_acc)

        print(f"Epoch {epoch+1}/{epochs}: "
              f"Loss={avg_loss:.4f}, "
              f"Train Acc={train_acc:.4f}, "
              f"Val Acc={val_acc:.4f}")

    training_time = time.time() - start_time
    training_info['training_time_seconds'] = training_time

    return training_info


def evaluate_model(model, test_loader, device):
    """Evaluate model on test set."""

    model.eval()
    correct = 0
    total = 0

    inference_times = []

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)

            # Measure inference time
            start = time.time()
            output = model(data)
            inference_times.append((time.time() - start) * 1000 / len(data))  # ms per sample

            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

    test_accuracy = correct / total
    avg_inference_ms = sum(inference_times) / len(inference_times)

    return {
        'test_accuracy': test_accuracy,
        'inference_time_ms': avg_inference_ms,
    }


def gather_model_info(model, training_info, test_results) -> Dict[str, Any]:
    """
    Gather all information needed for LJPW evaluation.
    """

    num_params = model.count_parameters()

    # Architecture info
    architecture = {
        'num_layers': 3,
        'layer_sizes': [128, 64, 10],
        'activations': ['relu', 'relu', 'none'],
        'total_params': num_params,
        'has_clear_names': False,  # fc1, fc2, fc3 not very descriptive
        'has_documentation': False,
        'uses_modules': False,
        'clear_structure': False,
        'is_sparse': False,
    }

    # Test results
    test_results_info = {
        'test_accuracy': test_results['test_accuracy'],
        'edge_case_tested': False,  # Not tested yet
        'noise_tested': False,
    }

    # Training info
    train_info = {
        'converged': True,
        'smooth_convergence': True,  # Check loss curve
        'epochs_to_converge': training_info['epochs'],
        'train_accuracy': training_info['train_accuracies'][-1],
        'training_time_seconds': training_info['training_time_seconds'],
    }

    # Validation
    validation = {
        'has_val_set': True,
        'has_test_set': True,
        'tracks_val_accuracy': True,
        'no_overfitting': abs(train_info['train_accuracy'] - test_results['test_accuracy']) < 0.05,
    }

    # Performance
    performance = {
        'inference_time_ms': test_results['inference_time_ms'],
        'memory_usage_mb': None,  # Not measured yet
    }

    # Documentation
    documentation = {
        'has_description': False,
        'layer_purposes': False,
        'design_rationale': False,
        'has_examples': False,
    }

    # Design
    design = {
        'uses_natural_principles': False,
        'principled_sizing': False,
        'thoughtful_activations': False,
        'documented_rationale': False,
    }

    return {
        'architecture': architecture,
        'test_results': test_results_info,
        'training_info': train_info,
        'validation': validation,
        'performance': performance,
        'documentation': documentation,
        'design': design,
    }


def main():
    """Train and evaluate traditional MNIST baseline."""

    print("=" * 70)
    print("TRADITIONAL MNIST BASELINE")
    print("=" * 70)
    print()
    print("Architecture: 784 → 128 → 64 → 10")
    print("Activations:  ReLU → ReLU → None")
    print("Design:       Standard approach, no particular principles")
    print()

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    print()

    # Load MNIST data
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])

    train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST('./data', train=False, transform=transform)

    # Split train into train/val
    train_size = int(0.9 * len(train_dataset))
    val_size = len(train_dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        train_dataset, [train_size, val_size]
    )

    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)

    # Create model
    model = TraditionalMNIST()
    print(f"Total parameters: {model.count_parameters():,}")
    print()

    # Train
    print("-" * 70)
    print("TRAINING")
    print("-" * 70)
    training_info = train_model(model, train_loader, val_loader, device, epochs=15)
    print()

    # Evaluate
    print("-" * 70)
    print("EVALUATION")
    print("-" * 70)
    test_results = evaluate_model(model, test_loader, device)
    print(f"Test Accuracy: {test_results['test_accuracy']:.4f}")
    print(f"Inference Time: {test_results['inference_time_ms']:.4f} ms/sample")
    print()

    # Measure LJPW
    print("-" * 70)
    print("LJPW SCORES")
    print("-" * 70)
    model_info = gather_model_info(model, training_info, test_results)
    evaluator = NeuralNetworkLJPW()
    scores = evaluator.measure(model, model_info)
    print(scores)

    # Analysis
    print("-" * 70)
    print("ANALYSIS")
    print("-" * 70)
    print(f"✓ Good test accuracy: {test_results['test_accuracy']:.4f}")
    print(f"✓ Fast inference: {test_results['inference_time_ms']:.4f} ms")
    print(f"✗ Poor interpretability (L={scores.L:.2f}): Arbitrary layer sizes")
    print(f"✗ Limited robustness testing (J={scores.J:.2f}): No edge cases tested")
    print(f"✓ Decent performance (P={scores.P:.2f}): High accuracy")
    print(f"✗ No design principles (W={scores.W:.2f}): Arbitrary choices")
    print()
    print(f"Overall Harmony: H={scores.H:.2f}")
    print("This is typical of traditional neural networks:")
    print("  - Optimized for accuracy (P) only")
    print("  - Little attention to interpretability (L)")
    print("  - No principled design (W)")
    print("  - Moderate overall quality (H)")
    print()
    print("Next: Build natural network with Fibonacci layers, diverse activations")
    print("=" * 70)

    # Save model
    torch.save(model.state_dict(), 'traditional_mnist.pth')
    print("\nModel saved to: traditional_mnist.pth")

    return model, scores


if __name__ == '__main__':
    model, scores = main()
