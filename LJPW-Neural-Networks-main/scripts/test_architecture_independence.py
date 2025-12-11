"""
Test 1.2: Architecture Independence

Hypothesis: The ~0.48 Hz frequency is universal across different LJPW architectures.

Expected Results:
- All architectures converge to 0.45-0.51 Hz
- Variance across architectures < 0.05 Hz
- Pattern persists regardless of depth/width
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def measure_heartbeat_frequency(network, iterations=1000):
    """Measure the heartbeat frequency of a network."""
    harmony_history = []
    dummy_input = np.random.randn(32, network.input_size) * 0.1  # Use network.input_size
    
    for i in range(iterations):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        if network.harmony_history:
            harmony_history.append(network.harmony_history[-1].H)
    
    # Count zero crossings around mean
    harmony_array = np.array(harmony_history)
    mean_harmony = np.mean(harmony_array)
    crossings = np.where(np.diff(np.sign(harmony_array - mean_harmony)))[0]
    
    # Frequency = crossings / 2 / iterations (divide by 2 for full cycles)
    frequency = len(crossings) / 2 / iterations
    
    return frequency, harmony_history


def run_architecture_test():
    """Test frequency universality across different architectures."""
    print("=" * 70)
    print("TEST 1.2: ARCHITECTURE INDEPENDENCE")
    print("=" * 70)
    print()
    
    # Define architectures to test
    architectures = [
        {'name': 'Deep (13,11,9)', 'hidden_fib_indices': [13, 11, 9]},
        {'name': 'Medium (11,9)', 'hidden_fib_indices': [11, 9]},
        {'name': 'Shallow (9)', 'hidden_fib_indices': [9]},
        {'name': 'Wide (15,13,11)', 'hidden_fib_indices': [15, 13, 11]},
        {'name': 'Narrow (11,9,7)', 'hidden_fib_indices': [11, 9, 7]},
    ]
    
    results = []
    
    print("Testing architectures...")
    print()
    
    for arch in architectures:
        print(f"Architecture: {arch['name']}")
        print(f"  Hidden layers: {arch['hidden_fib_indices']}")
        
        # Create network
        network = HomeostaticNetwork(
            input_size=784,
            output_size=10,
            hidden_fib_indices=arch['hidden_fib_indices'],
            target_harmony=0.75,
            allow_adaptation=True
        )
        
        # Measure frequency
        frequency, harmony_history = measure_heartbeat_frequency(network, iterations=1000)
        
        print(f"  Frequency: {frequency:.4f} Hz")
        print(f"  Mean Harmony: {np.mean(harmony_history):.3f}")
        print()
        
        results.append({
            'name': arch['name'],
            'frequency': frequency,
            'harmony_history': harmony_history
        })
    
    # Analyze results
    frequencies = [r['frequency'] for r in results]
    mean_freq = np.mean(frequencies)
    std_freq = np.std(frequencies)
    min_freq = np.min(frequencies)
    max_freq = np.max(frequencies)
    
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    print(f"Mean frequency: {mean_freq:.4f} Hz")
    print(f"Std deviation: {std_freq:.4f} Hz")
    print(f"Range: {min_freq:.4f} - {max_freq:.4f} Hz")
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: All in range 0.45-0.51
    criterion_1 = all(0.45 <= f <= 0.51 for f in frequencies)
    print(f"  1. All frequencies in [0.45, 0.51] Hz: {'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: Variance < 0.05
    criterion_2 = std_freq < 0.05
    print(f"  2. Std deviation < 0.05 Hz: {std_freq:.4f} {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: Mean near 0.48
    criterion_3 = 0.45 <= mean_freq <= 0.51
    print(f"  3. Mean frequency ~0.48 Hz: {mean_freq:.4f} {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    all_passed = all(criteria_met)
    print()
    print("=" * 70)
    print(f"OVERALL RESULT: {'[PASS]' if all_passed else '[FAIL]'} ({sum(criteria_met)}/3 criteria met)")
    print("=" * 70)
    
    # Visualization
    print()
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Frequency comparison
    ax1 = axes[0]
    names = [r['name'] for r in results]
    freqs = [r['frequency'] for r in results]
    
    bars = ax1.bar(range(len(names)), freqs, alpha=0.7)
    ax1.axhline(y=0.48, color='r', linestyle='--', label='Expected: 0.48 Hz')
    ax1.axhline(y=0.45, color='orange', linestyle=':', alpha=0.5, label='Range: 0.45-0.51 Hz')
    ax1.axhline(y=0.51, color='orange', linestyle=':', alpha=0.5)
    ax1.set_xticks(range(len(names)))
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.set_title('Heartbeat Frequency Across Architectures')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Harmony trajectories
    ax2 = axes[1]
    for r in results:
        ax2.plot(r['harmony_history'], alpha=0.6, linewidth=0.8, label=r['name'])
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Harmony')
    ax2.set_title('Harmony Trajectories (First 1000 Iterations)')
    ax2.legend(loc='best', fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"architecture_independence_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'results': results,
        'mean_freq': mean_freq,
        'std_freq': std_freq,
        'all_passed': all_passed
    }


if __name__ == '__main__':
    results = run_architecture_test()
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Mean frequency: {results['mean_freq']:.4f} Hz")
    print(f"  - Frequency variance: {results['std_freq']:.4f} Hz")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
