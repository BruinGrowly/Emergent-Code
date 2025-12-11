"""
Adaptive Layer Sizing Demo - Neuroplasticity in Action

This demonstrates how neural networks can dynamically adjust their architecture
based on learning progress, inspired by biological neuroplasticity.

Key Concepts:
1. Growth: Add neurons when learning plateaus
2. Pruning: Remove underutilized neurons
3. Self-Regulation: Network optimizes its own structure

This follows nature's principle: "structure follows function"
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from ljpw_nn.neuroplasticity import AdaptiveNaturalLayer, AdaptationEvent
from ljpw_nn.layers import FibonacciLayer
from ljpw_nn.activations import DiverseActivation
from examples.mnist_loader import load_mnist

print("=" * 80)
print("ADAPTIVE LAYER SIZING DEMO")
print("=" * 80)
print()
print("Neuroplasticity: Networks that adapt their own structure")
print()
print("Traditional Approach:")
print("  • Fixed architecture chosen before training")
print("  • Never changes during learning")
print("  • May be too small (underfitting) or too large (overfitting)")
print()
print("Natural Approach:")
print("  • Start with modest architecture")
print("  • Grow when learning plateaus")
print("  • Prune underutilized neurons")
print("  • Self-optimize structure")
print()
print("=" * 80)
print()

# Load small dataset for demo
print("Loading MNIST dataset (small subset for demo)...")
X_train, y_train, X_test, y_test = load_mnist(
    train_size=1000,
    test_size=200
)
print()

# ============================================================================
# Demo 1: Basic Adaptive Layer
# ============================================================================
print("=" * 80)
print("DEMO 1: BASIC ADAPTIVE LAYER")
print("=" * 80)
print()

print("Creating adaptive layer...")
layer = AdaptiveNaturalLayer(
    input_size=784,
    fib_index=9,  # Start with F9 = 34 units
    activation_mix=['relu', 'swish']
)

print(f"Initial configuration:")
print(f"  Size: {layer.size} units (F{layer.fib_index} = {layer.size})")
print(f"  Activations: {layer.activation_mix}")
print(f"  Adaptation enabled: {layer.adaptation_enabled}")
print()

# Simulate some forward passes
print("Simulating forward passes...")
for i in range(5):
    batch = X_train[i*20:(i+1)*20]
    output = layer.forward(batch)
    print(f"  Batch {i+1}: input={batch.shape}, output={output.shape}")

print()

# Check adaptation history
if layer.adaptation_history:
    print(f"Adaptation events recorded: {len(layer.adaptation_history)}")
    for event in layer.adaptation_history[:3]:  # Show first 3
        print(f"  • {event.event_type} at step {event.step}")
else:
    print("No adaptation events yet (layer still learning)")

print()

# ============================================================================
# Demo 2: Growth Trigger
# ============================================================================
print("=" * 80)
print("DEMO 2: GROWTH TRIGGER")
print("=" * 80)
print()

print("Demonstrating layer growth when learning plateaus...")
print()

# Create new adaptive layer
layer_growth = AdaptiveNaturalLayer(
    input_size=100,
    fib_index=7,  # Start small: F7 = 13 units
    activation_mix=['relu']
)

print(f"Starting size: {layer_growth.size} units (F{layer_growth.fib_index})")
print()

# Simulate plateau by calling should_grow()
print("Checking growth conditions...")
if hasattr(layer_growth, 'should_grow'):
    should_grow = layer_growth.should_grow()
    print(f"  Should grow? {should_grow}")
else:
    print("  (Growth logic embedded in layer)")

print()

# Manually trigger growth for demonstration
if hasattr(layer_growth, 'grow'):
    old_size = layer_growth.size
    layer_growth.grow()
    new_size = layer_growth.size
    print(f"After growth: {old_size} → {new_size} units")
    print(f"  Growth ratio: {new_size / old_size:.3f}x (approaching φ = 1.618)")
else:
    print("Growth happens automatically during training")

print()

# ============================================================================
# Demo 3: Pruning Underutilized Neurons
# ============================================================================
print("=" * 80)
print("DEMO 3: PRUNING UNDERUTILIZED NEURONS")
print("=" * 80)
print()

print("Demonstrating neuron pruning...")
print()

# Create layer with pruning capability
layer_prune = AdaptiveNaturalLayer(
    input_size=100,
    fib_index=11,  # Start large: F11 = 89 units
    activation_mix=['relu', 'swish', 'tanh']
)

print(f"Starting size: {layer_prune.size} units (F{layer_prune.fib_index})")
print()

# Simulate some activations
X_sample = np.random.randn(50, 100)
output = layer_prune.forward(X_sample)

print("Analyzing neuron utilization...")
# Calculate activation statistics
activation_mean = np.abs(output).mean(axis=0)
low_util = np.sum(activation_mean < 0.01)
high_util = np.sum(activation_mean > 0.1)

print(f"  High utilization: {high_util} neurons")
print(f"  Low utilization: {low_util} neurons")
print(f"  Pruning candidates: {low_util} neurons")
print()

if hasattr(layer_prune, 'prune'):
    old_size = layer_prune.size
    layer_prune.prune(threshold=0.01)
    new_size = layer_prune.size
    print(f"After pruning: {old_size} → {new_size} units")
    print(f"  Removed: {old_size - new_size} underutilized neurons")
else:
    print("Pruning happens automatically during training")

print()

# ============================================================================
# Demo 4: Adaptation Events
# ============================================================================
print("=" * 80)
print("DEMO 4: ADAPTATION EVENTS")
print("=" * 80)
print()

print("Understanding adaptation events...")
print()

# Create sample events
events = [
    AdaptationEvent(
        step=100,
        event_type='growth',
        old_size=34,
        new_size=55,
        trigger='learning_plateau',
        details={'plateau_epochs': 5, 'loss_change': 0.001}
    ),
    AdaptationEvent(
        step=500,
        event_type='pruning',
        old_size=55,
        new_size=34,
        trigger='low_utilization',
        details={'pruned_neurons': 21, 'utilization_threshold': 0.01}
    ),
    AdaptationEvent(
        step=1000,
        event_type='activation_diversification',
        old_size=34,
        new_size=34,
        trigger='convergence_instability',
        details={'added_activations': ['tanh'], 'diversity_score': 0.85}
    )
]

for event in events:
    print(f"Step {event.step}: {event.event_type.upper()}")
    print(f"  Size change: {event.old_size} → {event.new_size}")
    print(f"  Trigger: {event.trigger}")
    print(f"  Details: {event.details}")
    print()

# ============================================================================
# Key Insights
# ============================================================================
print("=" * 80)
print("KEY INSIGHTS: NEUROPLASTICITY")
print("=" * 80)
print()

print("1. DYNAMIC ARCHITECTURE")
print("   • Networks adapt structure during training")
print("   • No need to guess optimal size upfront")
print("   • Structure follows function (natural principle)")
print()

print("2. GROWTH MECHANISMS")
print("   • Triggered by learning plateaus")
print("   • Follows Fibonacci sequence (F7 → F9 → F11 → ...)")
print("   • Golden ratio growth (φ ≈ 1.618x)")
print()

print("3. PRUNING MECHANISMS")
print("   • Remove neurons with low activation")
print("   • Prevent overfitting")
print("   • Maintain efficiency")
print()

print("4. BIOLOGICAL INSPIRATION")
print("   • Human brain: ~50% synapses pruned in childhood")
print("   • \"Use it or lose it\" principle")
print("   • Efficient resource allocation")
print()

print("5. ADAPTATION EVENTS")
print("   • Track all structural changes")
print("   • Understand model evolution")
print("   • Debug and optimize adaptation")
print()

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print()

print("Adaptive layers demonstrate neuroplasticity:")
print()
print("  Traditional ML: Fixed architecture, manual tuning")
print("  Natural ML: Self-adapting structure, automatic optimization")
print()
print("This is just one example of how natural principles create")
print("more intelligent, self-regulating neural networks.")
print()
print("=" * 80)
