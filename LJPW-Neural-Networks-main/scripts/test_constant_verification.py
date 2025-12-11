"""
Test 2.1: Constant Verification Across Conditions

Purpose: Verify that the three fundamental constants hold across different
network configurations:
- H ≈ √(2/3) ≈ 0.816
- f ≈ e/6 ≈ 0.453 Hz
- H/f ≈ φ ≈ 1.618

Expected Results:
- All constants within 5% tolerance across all architectures
- Golden ratio relationship maintained
- Constants independent of network size/depth
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def measure_equilibrium_and_frequency(network, iterations=5000, warmup=1000):
    """
    Measure equilibrium harmony and oscillation frequency.
    
    Args:
        network: HomeostaticNetwork to measure
        iterations: Total iterations to run
        warmup: Iterations to skip before measuring
        
    Returns:
        tuple: (equilibrium_H, frequency)
    """
    harmony_history = []
    dummy_input = np.random.randn(32, network.input_size) * 0.1
    
    for i in range(iterations):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        if network.harmony_history:
            harmony_history.append(network.harmony_history[-1].H)
    
    # Measure equilibrium (mean after warmup)
    equilibrium_H = np.mean(harmony_history[warmup:])
    
    # Measure frequency (zero crossings after warmup)
    warmup_trajectory = np.array(harmony_history[warmup:])
    mean_h = np.mean(warmup_trajectory)
    deviations = warmup_trajectory - mean_h
    zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
    frequency = zero_crossings / len(warmup_trajectory)
    
    return equilibrium_H, frequency


def run_constant_verification():
    """Test constants across different network configurations."""
    print("=" * 70)
    print("TEST 2.1: CONSTANT VERIFICATION ACROSS CONDITIONS")
    print("=" * 70)
    print()
    
    # Define theoretical constants
    sqrt_2_3 = np.sqrt(2/3)
    e_6 = np.e / 6
    phi = (1 + np.sqrt(5)) / 2
    
    print("Theoretical Constants:")
    print(f"  H_theory = sqrt(2/3) = {sqrt_2_3:.6f}")
    print(f"  f_theory = e/6 = {e_6:.6f}")
    print(f"  phi = (1+sqrt(5))/2 = {phi:.6f}")
    print()
    print("-" * 70)
    print()
    
    # Test different configurations
    configurations = [
        {
            'name': 'Standard (784->10, [13,11,9])',
            'input_size': 784,
            'output_size': 10,
            'hidden_fib_indices': [13, 11, 9]
        },
        {
            'name': 'Shallow (784->10, [11,9])',
            'input_size': 784,
            'output_size': 10,
            'hidden_fib_indices': [11, 9]
        },
        {
            'name': 'Wide (784->10, [15,13,11])',
            'input_size': 784,
            'output_size': 10,
            'hidden_fib_indices': [15, 13, 11]
        },
        {
            'name': 'Narrow (784->10, [11,9,7])',
            'input_size': 784,
            'output_size': 10,
            'hidden_fib_indices': [11, 9, 7]
        },
        {
            'name': 'Large I/O (1000->20, [13,11,9])',
            'input_size': 1000,
            'output_size': 20,
            'hidden_fib_indices': [13, 11, 9]
        },
        {
            'name': 'Small (500->5, [11,9])',
            'input_size': 500,
            'output_size': 5,
            'hidden_fib_indices': [11, 9]
        },
    ]
    
    results = []
    
    print(f"Testing {len(configurations)} configurations...")
    print()
    
    for config in configurations:
        print(f"Configuration: {config['name']}")
        
        # Create network
        network = HomeostaticNetwork(
            input_size=config['input_size'],
            output_size=config['output_size'],
            hidden_fib_indices=config['hidden_fib_indices'],
            target_harmony=0.75,
            allow_adaptation=True
        )
        
        # Measure constants
        H_eq, freq = measure_equilibrium_and_frequency(network, iterations=5000)
        ratio = H_eq / freq if freq > 0 else 0
        
        # Calculate errors
        H_error = abs(H_eq - sqrt_2_3)
        f_error = abs(freq - e_6)
        ratio_error = abs(ratio - phi)
        
        H_pct = (H_error / sqrt_2_3) * 100
        f_pct = (f_error / e_6) * 100
        ratio_pct = (ratio_error / phi) * 100
        
        print(f"  H = {H_eq:.6f} (error: {H_error:.6f}, {H_pct:.2f}%)")
        print(f"  f = {freq:.6f} (error: {f_error:.6f}, {f_pct:.2f}%)")
        print(f"  H/f = {ratio:.6f} (error: {ratio_error:.6f}, {ratio_pct:.2f}%)")
        print()
        
        results.append({
            'name': config['name'],
            'H': H_eq,
            'f': freq,
            'ratio': ratio,
            'H_error': H_error,
            'f_error': f_error,
            'ratio_error': ratio_error,
            'H_pct': H_pct,
            'f_pct': f_pct,
            'ratio_pct': ratio_pct
        })
    
    # Analyze results
    print("=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print()
    
    print(f"{'Configuration':<35} | {'H':<8} | {'f':<8} | {'H/f':<8}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<35} | {r['H']:.6f} | {r['f']:.6f} | {r['ratio']:.6f}")
    
    print()
    print("Errors from Theoretical Values:")
    print("-" * 70)
    print(f"{'Configuration':<35} | {'H %':<6} | {'f %':<6} | {'phi %':<6}")
    print("-" * 70)
    for r in results:
        print(f"{r['name']:<35} | {r['H_pct']:5.2f}% | {r['f_pct']:5.2f}% | {r['ratio_pct']:5.2f}%")
    
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: All H within 5%
    max_H_error_pct = max(r['H_pct'] for r in results)
    criterion_1 = max_H_error_pct < 5.0
    print(f"  1. All H within 5%: Max error {max_H_error_pct:.2f}% {'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: All f within 5%
    max_f_error_pct = max(r['f_pct'] for r in results)
    criterion_2 = max_f_error_pct < 5.0
    print(f"  2. All f within 5%: Max error {max_f_error_pct:.2f}% {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: All H/f within 10% (more tolerance for ratio)
    max_ratio_error_pct = max(r['ratio_pct'] for r in results)
    criterion_3 = max_ratio_error_pct < 10.0
    print(f"  3. All H/f within 10%: Max error {max_ratio_error_pct:.2f}% {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    # Criterion 4: Low variance across configurations
    H_values = [r['H'] for r in results]
    f_values = [r['f'] for r in results]
    
    H_std = np.std(H_values)
    f_std = np.std(f_values)
    
    criterion_4 = H_std < 0.05 and f_std < 0.05
    print(f"  4. Low variance: H_std={H_std:.4f}, f_std={f_std:.4f} {'[PASS]' if criterion_4 else '[FAIL]'}")
    criteria_met.append(criterion_4)
    
    all_passed = all(criteria_met)
    print()
    print("=" * 70)
    print(f"OVERALL RESULT: {'[PASS]' if all_passed else '[FAIL]'} ({sum(criteria_met)}/4 criteria met)")
    print("=" * 70)
    
    # Visualization
    print()
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: H values
    ax = axes[0, 0]
    names = [r['name'].split('(')[0].strip() for r in results]
    H_vals = [r['H'] for r in results]
    
    ax.bar(range(len(names)), H_vals, alpha=0.7)
    ax.axhline(y=sqrt_2_3, color='r', linestyle='--', linewidth=2, label=f'Theory: sqrt(2/3)={sqrt_2_3:.3f}')
    ax.axhline(y=sqrt_2_3*1.05, color='orange', linestyle=':', alpha=0.5, label='±5%')
    ax.axhline(y=sqrt_2_3*0.95, color='orange', linestyle=':', alpha=0.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('Equilibrium H')
    ax.set_title('Equilibrium Harmony Across Configurations')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Frequency values
    ax = axes[0, 1]
    f_vals = [r['f'] for r in results]
    
    ax.bar(range(len(names)), f_vals, alpha=0.7, color='green')
    ax.axhline(y=e_6, color='r', linestyle='--', linewidth=2, label=f'Theory: e/6={e_6:.3f}')
    ax.axhline(y=e_6*1.05, color='orange', linestyle=':', alpha=0.5, label='±5%')
    ax.axhline(y=e_6*0.95, color='orange', linestyle=':', alpha=0.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title('Oscillation Frequency Across Configurations')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 3: H/f ratio
    ax = axes[1, 0]
    ratio_vals = [r['ratio'] for r in results]
    
    ax.bar(range(len(names)), ratio_vals, alpha=0.7, color='purple')
    ax.axhline(y=phi, color='r', linestyle='--', linewidth=2, label=f'Theory: phi={phi:.3f}')
    ax.axhline(y=phi*1.1, color='orange', linestyle=':', alpha=0.5, label='±10%')
    ax.axhline(y=phi*0.9, color='orange', linestyle=':', alpha=0.5)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('H/f Ratio')
    ax.set_title('Golden Ratio (H/f) Across Configurations')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 4: Error percentages
    ax = axes[1, 1]
    x = np.arange(len(names))
    width = 0.25
    
    ax.bar(x - width, [r['H_pct'] for r in results], width, label='H error %', alpha=0.7)
    ax.bar(x, [r['f_pct'] for r in results], width, label='f error %', alpha=0.7)
    ax.bar(x + width, [r['ratio_pct'] for r in results], width, label='H/f error %', alpha=0.7)
    
    ax.axhline(y=5, color='r', linestyle='--', label='5% threshold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right')
    ax.set_ylabel('Error (%)')
    ax.set_title('Percentage Errors from Theoretical Values')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"constant_verification_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'results': results,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'mean_H': np.mean(H_values),
        'mean_f': np.mean(f_values),
        'mean_ratio': np.mean(ratio_vals)
    }


if __name__ == '__main__':
    results = run_constant_verification()
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Mean H: {results['mean_H']:.6f} (theory: {np.sqrt(2/3):.6f})")
    print(f"  - Mean f: {results['mean_f']:.6f} (theory: {np.e/6:.6f})")
    print(f"  - Mean H/f: {results['mean_ratio']:.6f} (theory: {(1+np.sqrt(5))/2:.6f})")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
