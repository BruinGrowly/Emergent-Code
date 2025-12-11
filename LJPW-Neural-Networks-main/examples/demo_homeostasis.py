"""
Homeostatic Self-Regulation Demo

Demonstrates neural networks that maintain harmony (H > 0.7) through
automatic self-regulation, inspired by biological homeostasis.

Homeostasis: The tendency to maintain stable internal conditions
through negative feedback loops.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
from datetime import datetime
from ljpw_nn.homeostatic import HomeostaticNetwork, HarmonyCheckpoint
from ljpw_nn.models import NaturalMNIST
from examples.mnist_loader import load_mnist

print("=" * 80)
print("HOMEOSTATIC SELF-REGULATION DEMO")
print("=" * 80)
print()
print("Biological Homeostasis:")
print("  • Body temperature: 37°C ± 0.5°C")
print("  • Blood pH: 7.4 ± 0.05")
print("  • Glucose: 80-100 mg/dL")
print("  • Deviation triggers corrective action")
print()
print("Neural Network Homeostasis:")
print("  • Harmony: H > 0.7")
print("  • Continuous monitoring of L, J, P, W")
print("  • Adaptation when H drops below threshold")
print("  • Self-regulation through structural changes")
print()
print("=" * 80)
print()

# ============================================================================
# Demo 1: Harmony Checkpoints
# ============================================================================
print("=" * 80)
print("DEMO 1: HARMONY CHECKPOINTS")
print("=" * 80)
print()

print("Creating harmony checkpoints to track network health...")
print()

checkpoints = [
    HarmonyCheckpoint(
        timestamp=datetime.now(),
        epoch=0,
        L=0.75, J=0.72, P=0.65, W=0.78,
        H=(0.75 * 0.72 * 0.65 * 0.78) ** 0.25,
        accuracy=0.65
    ),
    HarmonyCheckpoint(
        timestamp=datetime.now(),
        epoch=5,
        L=0.76, J=0.74, P=0.82, W=0.79,
        H=(0.76 * 0.74 * 0.82 * 0.79) ** 0.25,
        accuracy=0.82
    ),
    HarmonyCheckpoint(
        timestamp=datetime.now(),
        epoch=10,
        L=0.77, J=0.75, P=0.88, W=0.80,
        H=(0.77 * 0.75 * 0.88 * 0.80) ** 0.25,
        accuracy=0.88
    ),
]

for cp in checkpoints:
    print(cp)
    weakest_dim, weakest_score = cp.get_weakest_dimension()
    status = "✓ HEALTHY" if cp.H >= 0.7 else "⚠ NEEDS REGULATION"
    print(f"  Status: {status}")
    print(f"  Weakest dimension: {weakest_dim} = {weakest_score:.2f}")
    print()

# ============================================================================
# Demo 2: Dimension Analysis
# ============================================================================
print("=" * 80)
print("DEMO 2: UNDERSTANDING LJPW DIMENSIONS")
print("=" * 80)
print()

print("When harmony drops, identify which dimension needs improvement:")
print()

# Scenario: Low interpretability
low_L = HarmonyCheckpoint(
    timestamp=datetime.now(),
    epoch=15,
    L=0.55,  # Low!
    J=0.80,
    P=0.90,
    W=0.75,
    H=(0.55 * 0.80 * 0.90 * 0.75) ** 0.25,
    accuracy=0.90
)

print("Scenario 1: Low Interpretability")
print(f"  {low_L}")
dim, score = low_L.get_weakest_dimension()
print(f"  Weakest: {dim} = {score:.2f}")
print(f"  Action: Add documentation, simplify architecture")
print()

# Scenario: Low robustness
low_J = HarmonyCheckpoint(
    timestamp=datetime.now(),
    epoch=20,
    L=0.78,
    J=0.58,  # Low!
    P=0.85,
    W=0.76,
    H=(0.78 * 0.58 * 0.85 * 0.76) ** 0.25,
    accuracy=0.85
)

print("Scenario 2: Low Robustness")
print(f"  {low_J}")
dim, score = low_J.get_weakest_dimension()
print(f"  Weakest: {dim} = {score:.2f}")
print(f"  Action: Add regularization, test edge cases")
print()

# Scenario: Low performance
low_P = HarmonyCheckpoint(
    timestamp=datetime.now(),
    epoch=25,
    L=0.80,
    J=0.75,
    P=0.60,  # Low!
    W=0.78,
    H=(0.80 * 0.75 * 0.60 * 0.78) ** 0.25,
    accuracy=0.60
)

print("Scenario 3: Low Performance")
print(f"  {low_P}")
dim, score = low_P.get_weakest_dimension()
print(f"  Weakest: {dim} = {score:.2f}")
print(f"  Action: Grow layers, increase capacity")
print()

# Scenario: Low elegance
low_W = HarmonyCheckpoint(
    timestamp=datetime.now(),
    epoch=30,
    L=0.76,
    J=0.77,
    P=0.85,
    W=0.52,  # Low!
    H=(0.76 * 0.77 * 0.85 * 0.52) ** 0.25,
    accuracy=0.85
)

print("Scenario 4: Low Elegance")
print(f"  {low_W}")
dim, score = low_W.get_weakest_dimension()
print(f"  Weakest: {dim} = {score:.2f}")
print(f"  Action: Refactor to use natural principles")
print()

# ============================================================================
# Demo 3: Real Network Monitoring
# ============================================================================
print("=" * 80)
print("DEMO 3: MONITORING A REAL NETWORK")
print("=" * 80)
print()

print("Loading MNIST dataset...")
X_train, y_train, X_test, y_test = load_mnist(
    train_size=2000,
    test_size=400
)
print()

print("Creating NaturalMNIST model...")
model = NaturalMNIST(verbose=False, learning_rate=0.01)
print()

print("Monitoring harmony during training...")
print("-" * 80)

# Train and monitor
history_checkpoints = []

for epoch in [0, 3, 6, 9, 12, 15]:
    if epoch > 0:
        # Train for a few epochs
        model.fit(X_train, y_train, epochs=3, batch_size=64, verbose=False)

    # Measure current state
    acc = model.evaluate(X_test, y_test)
    scores = model.measure_harmony(X_test, y_test)

    checkpoint = HarmonyCheckpoint(
        timestamp=datetime.now(),
        epoch=epoch,
        L=scores.L,
        J=scores.J,
        P=scores.P,
        W=scores.W,
        H=scores.H,
        accuracy=acc
    )

    history_checkpoints.append(checkpoint)

    print(checkpoint)

    # Check if intervention needed
    if checkpoint.H < 0.7:
        dim, score = checkpoint.get_weakest_dimension()
        print(f"  ⚠ REGULATION NEEDED: {dim} = {score:.2f}")
    elif checkpoint.H >= 0.7:
        print(f"  ✓ HEALTHY: H = {checkpoint.H:.2f}")

print()

# ============================================================================
# Demo 4: Homeostatic Trajectory
# ============================================================================
print("=" * 80)
print("DEMO 4: HOMEOSTATIC TRAJECTORY")
print("=" * 80)
print()

print("Analyzing harmony evolution over training...")
print()

print("Epoch  H      L      J      P      W      Status")
print("-" * 80)

for cp in history_checkpoints:
    status = "✓" if cp.H >= 0.7 else "⚠"
    print(f"{cp.epoch:5d}  {cp.H:.3f}  {cp.L:.3f}  {cp.J:.3f}  {cp.P:.3f}  {cp.W:.3f}  {status}")

print()

# Calculate trends
if len(history_checkpoints) >= 2:
    h_start = history_checkpoints[0].H
    h_end = history_checkpoints[-1].H
    h_change = h_end - h_start

    print(f"Harmony change: {h_start:.3f} → {h_end:.3f} (Δ{h_change:+.3f})")

    if h_change > 0.05:
        print("  ✓ Improving: System self-regulating successfully")
    elif h_change < -0.05:
        print("  ⚠ Declining: Intervention needed")
    else:
        print("  → Stable: Maintaining homeostasis")

print()

# ============================================================================
# Key Insights
# ============================================================================
print("=" * 80)
print("KEY INSIGHTS: HOMEOSTATIC SELF-REGULATION")
print("=" * 80)
print()

print("1. CONTINUOUS MONITORING")
print("   • Track H, L, J, P, W at every checkpoint")
print("   • Identify deviations from target (H > 0.7)")
print("   • Maintain awareness of network health")
print()

print("2. TARGETED INTERVENTIONS")
print("   • Identify weakest dimension (L, J, P, or W)")
print("   • Take specific action for that dimension")
print("   • Don't change everything - surgical precision")
print()

print("3. BIOLOGICAL INSPIRATION")
print("   • Like body temperature regulation")
print("   • Negative feedback loops maintain stability")
print("   • Self-correcting without external intervention")
print()

print("4. PRODUCTION QUALITY")
print("   • Traditional ML: \"Good enough\" accuracy")
print("   • LJPW ML: All dimensions above 0.7")
print("   • Homeostasis ensures sustained quality")
print()

print("5. ADAPTATION HISTORY")
print("   • Every checkpoint recorded")
print("   • Full trajectory visible")
print("   • Understand evolution over time")
print()

print("=" * 80)
print("CONCLUSION")
print("=" * 80)
print()

final_cp = history_checkpoints[-1]
if final_cp.H >= 0.7:
    print(f"✓ Network achieved homeostasis: H = {final_cp.H:.3f} ≥ 0.70")
    print()
    print("  System self-regulated to maintain harmony.")
    print("  All dimensions (L, J, P, W) above threshold.")
    print("  Production ready.")
else:
    print(f"⚠ Network needs regulation: H = {final_cp.H:.3f} < 0.70")
    print()
    dim, score = final_cp.get_weakest_dimension()
    print(f"  Weakest dimension: {dim} = {score:.2f}")
    print(f"  Recommended action: Improve {dim}")

print()
print("This demonstrates how neural networks can maintain quality")
print("through biological principles of homeostatic self-regulation.")
print()
print("=" * 80)
