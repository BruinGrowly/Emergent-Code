"""
Test 2.5: Golden Ratio Validation

Purpose: Confirm that the H/f ratio equals the golden ratio (φ) across
many independent measurements.

Expected Results:
- Mean ratio ≈ φ ± 0.05
- Low variance (std < 0.1)
- Consistent across 100 runs
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def measure_single_run(iterations=3000, warmup=500):
    """
    Run a single measurement of H and frequency.
    
    Returns:
        tuple: (H_equilibrium, frequency, ratio)
    """
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 11, 9],
        target_harmony=0.75,
        allow_adaptation=True
    )
    
    harmony_history = []
    dummy_input = np.random.randn(32, 784) * 0.1
    
    for i in range(iterations):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        if network.harmony_history:
            harmony_history.append(network.harmony_history[-1].H)
    
    # Measure equilibrium
    H_eq = np.mean(harmony_history[warmup:])
    
    # Measure frequency
    warmup_trajectory = np.array(harmony_history[warmup:])
    mean_h = np.mean(warmup_trajectory)
    deviations = warmup_trajectory - mean_h
    zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
    frequency = zero_crossings / len(warmup_trajectory)
    
    # Calculate ratio
    ratio = H_eq / frequency if frequency > 0 else 0
    
    return H_eq, frequency, ratio


def run_golden_ratio_validation(n_runs=100):
    """Validate golden ratio relationship across many runs."""
    print("=" * 70)
    print("TEST 2.5: GOLDEN RATIO VALIDATION")
    print("=" * 70)
    print()
    
    # Theoretical values
    phi = (1 + np.sqrt(5)) / 2
    sqrt_2_3 = np.sqrt(2/3)
    e_6 = np.e / 6
    
    print("Theoretical Values:")
    print(f"  Golden Ratio (phi) = {phi:.6f}")
    print(f"  H_theory = sqrt(2/3) = {sqrt_2_3:.6f}")
    print(f"  f_theory = e/6 = {e_6:.6f}")
    print(f"  Expected ratio = {sqrt_2_3/e_6:.6f}")
    print()
    print("-" * 70)
    print()
    
    print(f"Running {n_runs} independent measurements...")
    print()
    
    H_values = []
    f_values = []
    ratios = []
    
    # Use tqdm for progress bar with detailed stats
    with tqdm(total=n_runs, desc="Golden Ratio Test", unit="run", 
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for run in range(n_runs):
            H_eq, freq, ratio = measure_single_run()
            
            H_values.append(H_eq)
            f_values.append(freq)
            ratios.append(ratio)
            
            # Update progress bar with current values
            pbar.set_postfix({
                'H': f'{H_eq:.4f}',
                'f': f'{freq:.4f}',
                'H/f': f'{ratio:.4f}'
            })
            pbar.update(1)
    
    # Analyze results
    print()
    print("=" * 70)
    print("RESULTS ANALYSIS")
    print("=" * 70)
    print()
    
    mean_H = np.mean(H_values)
    std_H = np.std(H_values)
    mean_f = np.mean(f_values)
    std_f = np.std(f_values)
    mean_ratio = np.mean(ratios)
    std_ratio = np.std(ratios)
    
    print("Measured Values:")
    print(f"  H: {mean_H:.6f} ± {std_H:.6f}")
    print(f"  f: {mean_f:.6f} ± {std_f:.6f}")
    print(f"  H/f: {mean_ratio:.6f} ± {std_ratio:.6f}")
    print()
    
    # Errors from theory
    H_error = abs(mean_H - sqrt_2_3)
    f_error = abs(mean_f - e_6)
    ratio_error = abs(mean_ratio - phi)
    
    H_pct = (H_error / sqrt_2_3) * 100
    f_pct = (f_error / e_6) * 100
    ratio_pct = (ratio_error / phi) * 100
    
    print("Errors from Theory:")
    print(f"  H error: {H_error:.6f} ({H_pct:.2f}%)")
    print(f"  f error: {f_error:.6f} ({f_pct:.2f}%)")
    print(f"  Ratio error: {ratio_error:.6f} ({ratio_pct:.2f}%)")
    print()
    
    # Success criteria
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: Mean ratio within 5% of phi
    criterion_1 = ratio_pct < 5.0
    print(f"  1. Mean ratio within 5% of phi: {ratio_pct:.2f}% {'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: Low variance (std < 0.1)
    criterion_2 = std_ratio < 0.1
    print(f"  2. Low variance (std < 0.1): {std_ratio:.4f} {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: 95% of measurements within 10% of phi
    within_10pct = sum(1 for r in ratios if abs(r - phi) / phi < 0.1)
    pct_within = (within_10pct / n_runs) * 100
    criterion_3 = pct_within >= 95
    print(f"  3. 95% within 10% of phi: {pct_within:.1f}% {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    # Criterion 4: Ratio statistically equals phi (t-test)
    from scipy import stats
    t_stat, p_value = stats.ttest_1samp(ratios, phi)
    criterion_4 = p_value > 0.05  # Cannot reject null hypothesis that mean = phi
    print(f"  4. Statistical equality (p > 0.05): p={p_value:.4f} {'[PASS]' if criterion_4 else '[FAIL]'}")
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
    
    # Plot 1: Histogram of ratios
    ax = axes[0, 0]
    ax.hist(ratios, bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(x=phi, color='r', linestyle='--', linewidth=2, label=f'phi = {phi:.4f}')
    ax.axvline(x=mean_ratio, color='g', linestyle='-', linewidth=2, label=f'Mean = {mean_ratio:.4f}')
    ax.set_xlabel('H/f Ratio')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of H/f Ratios ({n_runs} runs)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Ratio over runs
    ax = axes[0, 1]
    ax.plot(ratios, alpha=0.5, linewidth=0.5)
    ax.axhline(y=phi, color='r', linestyle='--', linewidth=2, label=f'phi = {phi:.4f}')
    ax.axhline(y=phi*1.05, color='orange', linestyle=':', alpha=0.5, label='±5%')
    ax.axhline(y=phi*0.95, color='orange', linestyle=':', alpha=0.5)
    ax.fill_between(range(n_runs), phi*0.95, phi*1.05, alpha=0.2, color='orange')
    ax.set_xlabel('Run Number')
    ax.set_ylabel('H/f Ratio')
    ax.set_title('H/f Ratio Across Runs')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: H vs f scatter
    ax = axes[1, 0]
    ax.scatter(f_values, H_values, alpha=0.5)
    
    # Plot theoretical line H = phi * f
    f_range = np.linspace(min(f_values), max(f_values), 100)
    H_theoretical = phi * f_range
    ax.plot(f_range, H_theoretical, 'r--', linewidth=2, label=f'H = phi * f')
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Equilibrium H')
    ax.set_title('H vs f Relationship')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Error distribution
    ax = axes[1, 1]
    errors = [(r - phi) / phi * 100 for r in ratios]
    ax.hist(errors, bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(x=0, color='r', linestyle='--', linewidth=2, label='Zero error')
    ax.axvline(x=np.mean(errors), color='g', linestyle='-', linewidth=2, 
               label=f'Mean error = {np.mean(errors):.2f}%')
    ax.set_xlabel('Error from phi (%)')
    ax.set_ylabel('Frequency')
    ax.set_title('Distribution of Errors')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"golden_ratio_validation_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'mean_H': mean_H,
        'mean_f': mean_f,
        'mean_ratio': mean_ratio,
        'std_ratio': std_ratio,
        'ratio_error_pct': ratio_pct,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'p_value': p_value
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Golden Ratio Validation Test')
    parser.add_argument('--runs', type=int, default=100,
                       help='Number of independent runs (default: 100)')
    
    args = parser.parse_args()
    
    results = run_golden_ratio_validation(n_runs=args.runs)
    
    phi = (1 + np.sqrt(5)) / 2
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Mean H/f ratio: {results['mean_ratio']:.6f}")
    print(f"  - Golden ratio (phi): {phi:.6f}")
    print(f"  - Error: {results['ratio_error_pct']:.2f}%")
    print(f"  - Standard deviation: {results['std_ratio']:.6f}")
    print(f"  - Statistical p-value: {results['p_value']:.4f}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
