"""
Investigation: Why H Converges to 0.82 and Frequency is ~0.46 Hz

This script investigates two mysteries:
1. Why does harmony always converge to H ≈ 0.82 regardless of target?
2. Why is the oscillation frequency ~0.46 Hz?

Explores relationships to:
- Golden ratio (φ ≈ 1.618)
- Pi (π ≈ 3.14159)
- Natural constants
- LJPW framework constants
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def investigate_equilibrium():
    """Investigate the natural equilibrium point."""
    print("=" * 70)
    print("INVESTIGATION: NATURAL EQUILIBRIUM AND FREQUENCY")
    print("=" * 70)
    print()
    
    print("Part 1: Why H -> 0.82?")
    print("-" * 70)
    print()
    
    # Mathematical constants
    phi = (1 + np.sqrt(5)) / 2  # Golden ratio
    pi = np.pi
    e = np.e
    
    print("Testing relationships to known constants:")
    print()
    
    # Test various relationships
    observed_h = 0.822
    
    relationships = [
        ("1/phi", 1/phi, abs(observed_h - 1/phi)),
        ("phi/2", phi/2, abs(observed_h - phi/2)),
        ("sqrt(phi)", np.sqrt(phi), abs(observed_h - np.sqrt(phi))),
        ("1/sqrt(phi)", 1/np.sqrt(phi), abs(observed_h - 1/np.sqrt(phi))),
        ("phi^2/pi", phi**2 / pi, abs(observed_h - phi**2 / pi)),
        ("pi/4", pi/4, abs(observed_h - pi/4)),
        ("e/pi", e/pi, abs(observed_h - e/pi)),
        ("sqrt(2/3)", np.sqrt(2/3), abs(observed_h - np.sqrt(2/3))),
        ("4/5", 4/5, abs(observed_h - 4/5)),
        ("5/6", 5/6, abs(observed_h - 5/6)),
        ("4throot(LJPW)", np.power(0.79 * 0.86 * 0.77 * 0.82, 0.25), 
         abs(observed_h - np.power(0.79 * 0.86 * 0.77 * 0.82, 0.25))),
    ]
    
    # Sort by error
    relationships.sort(key=lambda x: x[2])
    
    print(f"Observed H: {observed_h:.6f}")
    print()
    print("Closest matches:")
    for name, value, error in relationships[:5]:
        pct_error = error / observed_h * 100
        print(f"  {name:20s} = {value:.6f}  (error: {error:.6f}, {pct_error:.2f}%)")
    
    print()
    print("-" * 70)
    print()
    
    # Part 2: Frequency investigation
    print("Part 2: Why frequency ~= 0.46 Hz?")
    print("-" * 70)
    print()
    
    observed_freq = 0.46
    
    freq_relationships = [
        ("1/phi", 1/phi, abs(observed_freq - 1/phi)),
        ("phi/4", phi/4, abs(observed_freq - phi/4)),
        ("1/2", 0.5, abs(observed_freq - 0.5)),
        ("sqrt(2)/3", np.sqrt(2)/3, abs(observed_freq - np.sqrt(2)/3)),
        ("pi/7", pi/7, abs(observed_freq - pi/7)),
        ("e/6", e/6, abs(observed_freq - e/6)),
        ("1/sqrt(5)", 1/np.sqrt(5), abs(observed_freq - 1/np.sqrt(5))),
        ("2/phi^2", 2/phi**2, abs(observed_freq - 2/phi**2)),
        ("H/sqrt(2)", observed_h/np.sqrt(2), abs(observed_freq - observed_h/np.sqrt(2))),
        ("sqrt(H)", np.sqrt(observed_h), abs(observed_freq - np.sqrt(observed_h))),
    ]
    
    freq_relationships.sort(key=lambda x: x[2])
    
    print(f"Observed frequency: {observed_freq:.6f} Hz")
    print()
    print("Closest matches:")
    for name, value, error in freq_relationships[:5]:
        pct_error = error / observed_freq * 100
        print(f"  {name:20s} = {value:.6f}  (error: {error:.6f}, {pct_error:.2f}%)")
    
    print()
    print("-" * 70)
    print()
    
    # Part 3: Empirical measurement
    print("Part 3: Empirical Measurement")
    print("-" * 70)
    print()
    
    print("Running network to measure actual equilibrium...")
    
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 11, 9],
        target_harmony=0.75,
        allow_adaptation=True
    )
    
    harmony_history = []
    L_history = []
    J_history = []
    P_history = []
    W_history = []
    
    dummy_input = np.random.randn(32, 784) * 0.1
    
    iterations = 5000
    for i in range(iterations):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        if network.harmony_history:
            checkpoint = network.harmony_history[-1]
            harmony_history.append(checkpoint.H)
            L_history.append(checkpoint.L)
            J_history.append(checkpoint.J)
            P_history.append(checkpoint.P)
            W_history.append(checkpoint.W)
    
    # Analyze equilibrium
    mean_h = np.mean(harmony_history[1000:])  # Skip first 1000 for warmup
    mean_l = np.mean(L_history[1000:])
    mean_j = np.mean(J_history[1000:])
    mean_p = np.mean(P_history[1000:])
    mean_w = np.mean(W_history[1000:])
    
    print()
    print(f"Equilibrium values (after 1000 iterations):")
    print(f"  H: {mean_h:.6f}")
    print(f"  L: {mean_l:.6f}")
    print(f"  J: {mean_j:.6f}")
    print(f"  P: {mean_p:.6f}")
    print(f"  W: {mean_w:.6f}")
    print()
    
    # Calculate geometric mean
    geometric_mean = np.power(mean_l * mean_j * mean_p * mean_w, 0.25)
    print(f"Geometric mean (4throot LJPW): {geometric_mean:.6f}")
    print(f"Difference from H: {abs(geometric_mean - mean_h):.6f}")
    print()
    
    # Measure frequency
    deviations = np.array(harmony_history[1000:]) - mean_h
    zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
    measured_freq = zero_crossings / len(deviations)
    
    print(f"Measured frequency: {measured_freq:.6f} Hz")
    print()
    
    # Part 4: Relationship between H and frequency
    print("-" * 70)
    print()
    print("Part 4: Relationship Between H and Frequency")
    print("-" * 70)
    print()
    
    # Test if frequency is related to H
    freq_h_ratio = measured_freq / mean_h
    h_freq_ratio = mean_h / measured_freq
    
    print(f"Frequency / H: {freq_h_ratio:.6f}")
    print(f"H / Frequency: {h_freq_ratio:.6f}")
    print()
    
    # Check if ratio matches known constants
    ratio_relationships = [
        ("sqrt(2)", np.sqrt(2), abs(h_freq_ratio - np.sqrt(2))),
        ("phi", phi, abs(h_freq_ratio - phi)),
        ("pi/2", pi/2, abs(h_freq_ratio - pi/2)),
        ("e", e, abs(h_freq_ratio - e)),
        ("2", 2.0, abs(h_freq_ratio - 2.0)),
    ]
    
    ratio_relationships.sort(key=lambda x: x[2])
    
    print("H/Frequency ratio matches:")
    for name, value, error in ratio_relationships[:3]:
        pct_error = error / h_freq_ratio * 100
        print(f"  {name:10s} = {value:.6f}  (error: {error:.6f}, {pct_error:.2f}%)")
    
    print()
    print("=" * 70)
    print("CONCLUSIONS")
    print("=" * 70)
    print()
    
    # Find best matches
    best_h_match = relationships[0]
    best_freq_match = freq_relationships[0]
    best_ratio_match = ratio_relationships[0]
    
    print(f"1. H ~= {mean_h:.6f} is closest to {best_h_match[0]} = {best_h_match[1]:.6f}")
    print(f"   Error: {best_h_match[2]:.6f} ({best_h_match[2]/mean_h*100:.2f}%)")
    print()
    
    print(f"2. Frequency ~= {measured_freq:.6f} Hz is closest to {best_freq_match[0]} = {best_freq_match[1]:.6f}")
    print(f"   Error: {best_freq_match[2]:.6f} ({best_freq_match[2]/measured_freq*100:.2f}%)")
    print()
    
    print(f"3. H/Frequency ratio ~= {h_freq_ratio:.6f} is closest to {best_ratio_match[0]} = {best_ratio_match[1]:.6f}")
    print(f"   Error: {best_ratio_match[2]:.6f} ({best_ratio_match[2]/h_freq_ratio*100:.2f}%)")
    print()
    
    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Harmony trajectory
    ax = axes[0, 0]
    ax.plot(harmony_history, linewidth=0.5, alpha=0.7)
    ax.axhline(y=mean_h, color='r', linestyle='--', label=f'Mean: {mean_h:.3f}')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Harmony')
    ax.set_title('Harmony Trajectory')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: LJPW dimensions
    ax = axes[0, 1]
    ax.plot(L_history, label=f'L (mean: {mean_l:.3f})', alpha=0.7)
    ax.plot(J_history, label=f'J (mean: {mean_j:.3f})', alpha=0.7)
    ax.plot(P_history, label=f'P (mean: {mean_p:.3f})', alpha=0.7)
    ax.plot(W_history, label=f'W (mean: {mean_w:.3f})', alpha=0.7)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Dimension Value')
    ax.set_title('LJPW Dimensions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Constant relationships for H
    ax = axes[1, 0]
    names = [r[0] for r in relationships[:8]]
    values = [r[1] for r in relationships[:8]]
    errors = [r[2] for r in relationships[:8]]
    
    bars = ax.barh(range(len(names)), errors, alpha=0.7)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel('Absolute Error from Observed H')
    ax.set_title(f'H ~= {mean_h:.4f} - Closest Constant Matches')
    ax.grid(True, alpha=0.3, axis='x')
    
    # Plot 4: Constant relationships for frequency
    ax = axes[1, 1]
    names = [r[0] for r in freq_relationships[:8]]
    values = [r[1] for r in freq_relationships[:8]]
    errors = [r[2] for r in freq_relationships[:8]]
    
    bars = ax.barh(range(len(names)), errors, alpha=0.7, color='orange')
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names)
    ax.set_xlabel('Absolute Error from Observed Frequency')
    ax.set_title(f'Frequency ~= {measured_freq:.4f} Hz - Closest Constant Matches')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"equilibrium_investigation_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'mean_h': mean_h,
        'measured_freq': measured_freq,
        'best_h_match': best_h_match,
        'best_freq_match': best_freq_match,
        'best_ratio_match': best_ratio_match,
        'h_freq_ratio': h_freq_ratio
    }


if __name__ == '__main__':
    results = investigate_equilibrium()
    
    print()
    print("Investigation complete!")
