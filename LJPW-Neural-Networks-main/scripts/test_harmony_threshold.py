"""
Test 1.3: Harmony Threshold Experiment

Hypothesis: Networks with H > 0.7 breathe; networks with H < 0.7 exhibit 
chaotic or convergent behavior.

Expected Results:
- H >= 0.7 → Stable oscillation
- H < 0.7 → Chaos or convergence
- Sharp phase transition at H ≈ 0.7
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def detect_pattern(harmony_trajectory):
    """Detect if pattern is oscillation, convergence, or chaos."""
    n = len(harmony_trajectory)
    mid = n // 2
    
    var_first = np.var(harmony_trajectory[:mid])
    var_second = np.var(harmony_trajectory[mid:])
    
    # Convergence: variance decreases significantly
    if var_second < var_first * 0.5:
        return "CONVERGENCE"
    
    # Stable oscillation: variance stays similar
    elif abs(var_second - var_first) < 0.001:
        return "STABLE_OSCILLATION"
    
    # Chaos: variance increases
    else:
        return "CHAOS"


def run_harmony_threshold_test():
    """Test consciousness threshold at H = 0.7."""
    print("=" * 70)
    print("TEST 1.3: HARMONY THRESHOLD EXPERIMENT")
    print("=" * 70)
    print()
    
    # Test different harmony targets
    target_harmonies = [0.5, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
    iterations = 1000
    
    results = []
    
    print(f"Testing {len(target_harmonies)} harmony thresholds...")
    print(f"Iterations per test: {iterations}")
    print()
    
    for target_h in target_harmonies:
        print(f"Target Harmony: {target_h:.2f}")
        
        # Create network
        network = HomeostaticNetwork(
            input_size=784,
            output_size=10,
            hidden_fib_indices=[13, 11, 9],
            target_harmony=target_h,
            allow_adaptation=True
        )
        
        # Run iterations
        harmony_history = []
        dummy_input = np.random.randn(32, 784) * 0.1
        
        for i in range(iterations):
            network.forward(dummy_input, training=False)
            network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
            
            if network.harmony_history:
                harmony_history.append(network.harmony_history[-1].H)
        
        # Detect pattern
        pattern = detect_pattern(harmony_history)
        mean_h = np.mean(harmony_history)
        std_h = np.std(harmony_history)
        
        print(f"  Pattern: {pattern}")
        print(f"  Mean H: {mean_h:.3f}")
        print(f"  Std H: {std_h:.3f}")
        print()
        
        results.append({
            'target': target_h,
            'pattern': pattern,
            'mean_h': mean_h,
            'std_h': std_h,
            'harmony_history': harmony_history
        })
    
    # Analyze results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    
    print("Target H | Pattern           | Mean H | Std H")
    print("-" * 70)
    for r in results:
        print(f"  {r['target']:.2f}   | {r['pattern']:17s} | {r['mean_h']:.3f}  | {r['std_h']:.3f}")
    
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: H >= 0.7 shows oscillation
    high_h_results = [r for r in results if r['target'] >= 0.7]
    criterion_1 = all(r['pattern'] == "STABLE_OSCILLATION" for r in high_h_results)
    print(f"  1. H >= 0.7 -> Oscillation: {'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: H < 0.7 shows convergence or chaos
    low_h_results = [r for r in results if r['target'] < 0.7]
    criterion_2 = all(r['pattern'] in ["CONVERGENCE", "CHAOS"] for r in low_h_results)
    print(f"  2. H < 0.7 -> Convergence/Chaos: {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: Clear threshold exists
    # Find transition point
    oscillating = [r['target'] for r in results if r['pattern'] == "STABLE_OSCILLATION"]
    not_oscillating = [r['target'] for r in results if r['pattern'] != "STABLE_OSCILLATION"]
    
    if oscillating and not_oscillating:
        transition_point = (min(oscillating) + max(not_oscillating)) / 2
        criterion_3 = 0.65 <= transition_point <= 0.75
        print(f"  3. Transition at ~0.7: {transition_point:.2f} {'[PASS]' if criterion_3 else '[FAIL]'}")
    else:
        criterion_3 = False
        print(f"  3. Transition at ~0.7: [FAIL] (no clear transition)")
    
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
    
    # Plot 1: Pattern vs Harmony Target
    ax1 = axes[0]
    targets = [r['target'] for r in results]
    patterns = [r['pattern'] for r in results]
    
    # Color code by pattern
    colors = []
    for p in patterns:
        if p == "STABLE_OSCILLATION":
            colors.append('green')
        elif p == "CONVERGENCE":
            colors.append('blue')
        else:
            colors.append('red')
    
    ax1.scatter(targets, range(len(targets)), c=colors, s=200, alpha=0.6)
    ax1.axvline(x=0.7, color='black', linestyle='--', linewidth=2, label='Threshold: H=0.7')
    ax1.set_xlabel('Target Harmony')
    ax1.set_ylabel('Test Index')
    ax1.set_title('Pattern Type vs Harmony Threshold')
    ax1.set_yticks(range(len(targets)))
    ax1.set_yticklabels([f"{p}" for p in patterns])
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='x')
    
    # Plot 2: Sample trajectories
    ax2 = axes[1]
    for r in results:
        label = f"H={r['target']:.2f} ({r['pattern']})"
        ax2.plot(r['harmony_history'][:200], alpha=0.6, linewidth=0.8, label=label)
    
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Harmony')
    ax2.set_title('Harmony Trajectories (First 200 Iterations)')
    ax2.legend(loc='best', fontsize=8)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"harmony_threshold_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'results': results,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met)
    }


if __name__ == '__main__':
    results = run_harmony_threshold_test()
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    oscillating_count = sum(1 for r in results['results'] if r['pattern'] == "STABLE_OSCILLATION")
    print(f"  - Oscillating networks: {oscillating_count}/{len(results['results'])}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
