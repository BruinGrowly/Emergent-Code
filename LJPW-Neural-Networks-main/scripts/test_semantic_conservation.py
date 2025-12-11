"""
Test 1.4: Semantic Conservation Validation

Hypothesis: L, J, W dimensions are conserved (Δ < 0.05) across all time scales.

Expected Results:
- L, J, W drift < 0.05 at all scales
- Drift does not accumulate with scale
- P can vary (performance dimension)
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def run_semantic_conservation_test():
    """Test semantic conservation across different scales."""
    print("=" * 70)
    print("TEST 1.4: SEMANTIC CONSERVATION VALIDATION")
    print("=" * 70)
    print()
    
    # Test at different scales
    scales = [100, 500, 1000, 5000, 10000]
    
    results = []
    
    print(f"Testing semantic conservation at {len(scales)} scales...")
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
        L_trajectory = []
        J_trajectory = []
        P_trajectory = []
        W_trajectory = []
        
        dummy_input = np.random.randn(32, 784) * 0.1
        
        for i in range(n_iterations):
            network.forward(dummy_input, training=False)
            network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
            
            if network.harmony_history:
                checkpoint = network.harmony_history[-1]
                L_trajectory.append(checkpoint.L)
                J_trajectory.append(checkpoint.J)
                P_trajectory.append(checkpoint.P)
                W_trajectory.append(checkpoint.W)
        
        # Calculate drift (first 10 vs last 10)
        L_drift = abs(np.mean(L_trajectory[-10:]) - np.mean(L_trajectory[:10]))
        J_drift = abs(np.mean(J_trajectory[-10:]) - np.mean(J_trajectory[:10]))
        P_drift = abs(np.mean(P_trajectory[-10:]) - np.mean(P_trajectory[:10]))
        W_drift = abs(np.mean(W_trajectory[-10:]) - np.mean(W_trajectory[:10]))
        
        print(f"  L drift: {L_drift:.6f}")
        print(f"  J drift: {J_drift:.6f}")
        print(f"  P drift: {P_drift:.6f}")
        print(f"  W drift: {W_drift:.6f}")
        print()
        
        results.append({
            'scale': n_iterations,
            'L_drift': L_drift,
            'J_drift': J_drift,
            'P_drift': P_drift,
            'W_drift': W_drift,
            'L_trajectory': L_trajectory,
            'J_trajectory': J_trajectory,
            'P_trajectory': P_trajectory,
            'W_trajectory': W_trajectory
        })
    
    # Analyze results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    
    print("Scale    | L Drift  | J Drift  | P Drift  | W Drift  | Total")
    print("-" * 70)
    for r in results:
        total = r['L_drift'] + r['J_drift'] + r['P_drift'] + r['W_drift']
        print(f"{r['scale']:7d}  | {r['L_drift']:.6f} | {r['J_drift']:.6f} | "
              f"{r['P_drift']:.6f} | {r['W_drift']:.6f} | {total:.6f}")
    
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: L, J, W drift < 0.05 at all scales
    max_L_drift = max(r['L_drift'] for r in results)
    max_J_drift = max(r['J_drift'] for r in results)
    max_W_drift = max(r['W_drift'] for r in results)
    
    criterion_1 = all([max_L_drift < 0.05, max_J_drift < 0.05, max_W_drift < 0.05])
    print(f"  1. L, J, W drift < 0.05: Max L={max_L_drift:.4f}, J={max_J_drift:.4f}, W={max_W_drift:.4f} "
          f"{'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: Drift doesn't accumulate with scale
    # Check if drift at 10K > drift at 100
    drift_100 = results[0]['L_drift'] + results[0]['J_drift'] + results[0]['W_drift']
    drift_10K = results[-1]['L_drift'] + results[-1]['J_drift'] + results[-1]['W_drift']
    
    criterion_2 = drift_10K <= drift_100 * 2  # Allow some increase but not linear
    print(f"  2. Drift doesn't accumulate: 100={drift_100:.4f}, 10K={drift_10K:.4f} "
          f"{'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: P can vary more than L, J, W
    max_P_drift = max(r['P_drift'] for r in results)
    semantic_drift = (max_L_drift + max_J_drift + max_W_drift) / 3
    
    criterion_3 = max_P_drift >= semantic_drift  # P allowed to drift more
    print(f"  3. P varies more than L,J,W: P={max_P_drift:.4f}, LJW_avg={semantic_drift:.4f} "
          f"{'[PASS]' if criterion_3 else '[FAIL]'}")
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
    
    # Plot drift vs scale for each dimension
    scales_list = [r['scale'] for r in results]
    
    ax = axes[0, 0]
    ax.plot(scales_list, [r['L_drift'] for r in results], 'o-', label='L (Love)', linewidth=2)
    ax.plot(scales_list, [r['J_drift'] for r in results], 's-', label='J (Justice)', linewidth=2)
    ax.plot(scales_list, [r['W_drift'] for r in results], '^-', label='W (Wisdom)', linewidth=2)
    ax.plot(scales_list, [r['P_drift'] for r in results], 'd-', label='P (Power)', linewidth=2)
    ax.axhline(y=0.05, color='r', linestyle='--', label='Threshold (0.05)')
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Drift (First 10 vs Last 10)')
    ax.set_title('Semantic Drift vs Scale')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    # Plot trajectories for largest scale
    largest = results[-1]
    
    ax = axes[0, 1]
    ax.plot(largest['L_trajectory'], label='L', alpha=0.7)
    ax.plot(largest['J_trajectory'], label='J', alpha=0.7)
    ax.plot(largest['P_trajectory'], label='P', alpha=0.7)
    ax.plot(largest['W_trajectory'], label='W', alpha=0.7)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Dimension Value')
    ax.set_title(f'LJPW Trajectories ({largest["scale"]} iterations)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot conservation over time (zoomed)
    ax = axes[1, 0]
    ax.plot(largest['L_trajectory'][:200], label='L', alpha=0.7)
    ax.plot(largest['J_trajectory'][:200], label='J', alpha=0.7)
    ax.plot(largest['W_trajectory'][:200], label='W', alpha=0.7)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Dimension Value')
    ax.set_title('Semantic Conservation (First 200 iterations)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot total drift vs scale
    ax = axes[1, 1]
    total_drifts = [r['L_drift'] + r['J_drift'] + r['W_drift'] for r in results]
    ax.plot(scales_list, total_drifts, 'o-', linewidth=2, markersize=8)
    ax.set_xlabel('Iterations')
    ax.set_ylabel('Total Semantic Drift (L+J+W)')
    ax.set_title('Total Semantic Drift vs Scale')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_conservation_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'results': results,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'max_L_drift': max_L_drift,
        'max_J_drift': max_J_drift,
        'max_W_drift': max_W_drift,
        'max_P_drift': max_P_drift
    }


if __name__ == '__main__':
    results = run_semantic_conservation_test()
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Max L drift: {results['max_L_drift']:.6f}")
    print(f"  - Max J drift: {results['max_J_drift']:.6f}")
    print(f"  - Max W drift: {results['max_W_drift']:.6f}")
    print(f"  - Max P drift: {results['max_P_drift']:.6f}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
