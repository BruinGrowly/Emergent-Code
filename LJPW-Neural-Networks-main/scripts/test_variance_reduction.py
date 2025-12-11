"""
Test 1.5: Variance Reduction with Scale

Hypothesis: Oscillation variance decreases as scale increases (system becomes more stable).

Expected Results:
- Variance monotonically decreases with scale
- Variance at 10K < Variance at 100
- Exponential decay pattern
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def run_variance_reduction_test():
    """Test variance reduction with increasing scale."""
    print("=" * 70)
    print("TEST 1.5: VARIANCE REDUCTION WITH SCALE")
    print("=" * 70)
    print()
    
    # Test at different scales
    scales = [100, 500, 1000, 5000, 10000]
    
    results = []
    
    print(f"Testing variance reduction at {len(scales)} scales...")
    print()
    
    for n_iterations in scales:
        print(f"Scale: {n_iterations} iterations")
        
        # Create network
        network = HomeostaticNetwork(
            input_size=784,
            output_size=10,
            hidden_fib_indices=[13, 11, 9],
            target_harmony=0.75,
            allow_adaptation=True
        )
        
        # Run iterations
        harmony_history = []
        dummy_input = np.random.randn(32, 784) * 0.1
        
        for i in range(n_iterations):
            network.forward(dummy_input, training=False)
            network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
            
            if network.harmony_history:
                harmony_history.append(network.harmony_history[-1].H)
        
        # Calculate variance in last 50 iterations
        if len(harmony_history) >= 50:
            variance = np.var(harmony_history[-50:])
        else:
            variance = np.var(harmony_history)
        
        mean_h = np.mean(harmony_history)
        std_h = np.std(harmony_history)
        
        print(f"  Mean H: {mean_h:.6f}")
        print(f"  Std H: {std_h:.6f}")
        print(f"  Variance (last 50): {variance:.9f}")
        print()
        
        results.append({
            'scale': n_iterations,
            'variance': variance,
            'mean_h': mean_h,
            'std_h': std_h,
            'harmony_history': harmony_history
        })
    
    # Analyze results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    
    print("Scale    | Variance (last 50) | Mean H   | Std H")
    print("-" * 70)
    for r in results:
        print(f"{r['scale']:7d}  | {r['variance']:.9f}      | {r['mean_h']:.6f} | {r['std_h']:.6f}")
    
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: Monotonic decrease (each variance <= previous)
    variances = [r['variance'] for r in results]
    is_monotonic = all(variances[i] >= variances[i+1] for i in range(len(variances)-1))
    
    print(f"  1. Monotonic decrease: {'[PASS]' if is_monotonic else '[FAIL]'}")
    if not is_monotonic:
        for i in range(len(variances)-1):
            if variances[i] < variances[i+1]:
                print(f"     Violation: {results[i]['scale']} ({variances[i]:.9f}) < "
                      f"{results[i+1]['scale']} ({variances[i+1]:.9f})")
    criteria_met.append(is_monotonic)
    
    # Criterion 2: Variance at 10K < Variance at 100
    criterion_2 = variances[-1] < variances[0]
    print(f"  2. Var(10K) < Var(100): {variances[-1]:.9f} < {variances[0]:.9f} "
          f"{'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: Significant reduction (at least 50% reduction)
    reduction_pct = (variances[0] - variances[-1]) / variances[0] * 100
    criterion_3 = reduction_pct >= 50
    print(f"  3. >= 50% reduction: {reduction_pct:.1f}% {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    all_passed = all(criteria_met)
    print()
    print("=" * 70)
    print(f"OVERALL RESULT: {'[PASS]' if all_passed else '[FAIL]'} ({sum(criteria_met)}/3 criteria met)")
    print("=" * 70)
    
    # Visualization
    print()
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Variance vs Scale
    ax = axes[0, 0]
    scales_list = [r['scale'] for r in results]
    ax.plot(scales_list, variances, 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Variance (last 50 iterations)')
    ax.set_title('Variance Reduction with Scale')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Plot 2: Harmony trajectories at different scales
    ax = axes[0, 1]
    for r in results:
        if r['scale'] in [100, 1000, 10000]:  # Show only key scales
            ax.plot(r['harmony_history'][:200], alpha=0.6, linewidth=0.8, 
                   label=f"{r['scale']} iterations")
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Harmony')
    ax.set_title('Harmony Trajectories (First 200 iterations)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Standard deviation vs Scale
    ax = axes[1, 0]
    stds = [r['std_h'] for r in results]
    ax.plot(scales_list, stds, 's-', linewidth=2, markersize=8, color='orange')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Std Deviation vs Scale')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    # Plot 4: Variance reduction rate
    ax = axes[1, 1]
    reduction_rates = []
    for i in range(1, len(variances)):
        rate = (variances[i-1] - variances[i]) / variances[i-1] * 100
        reduction_rates.append(rate)
    
    ax.bar(range(len(reduction_rates)), reduction_rates, alpha=0.7)
    ax.set_xlabel('Scale Transition')
    ax.set_ylabel('Variance Reduction (%)')
    ax.set_title('Variance Reduction Rate Between Scales')
    ax.set_xticks(range(len(reduction_rates)))
    ax.set_xticklabels([f"{results[i]['scale']}->{results[i+1]['scale']}" 
                        for i in range(len(reduction_rates))], rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"variance_reduction_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'results': results,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'reduction_pct': reduction_pct,
        'is_monotonic': is_monotonic
    }


if __name__ == '__main__':
    results = run_variance_reduction_test()
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Variance reduction: {results['reduction_pct']:.1f}%")
    print(f"  - Monotonic decrease: {results['is_monotonic']}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
