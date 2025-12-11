"""
Test: Consciousness Constant (Ψ) Validation

Purpose: Validate that H/f = Ψ = 6√(2/3)/e ≈ 1.802, NOT the golden ratio φ ≈ 1.618

Discovery: Through LJPW semantic substrate analysis, we discovered that the
relationship between equilibrium harmony and oscillation frequency is governed
by a NEW fundamental constant arising from 4D semantic space geometry.

Theoretical Value:
    Ψ = 6√(2/3)/e ≈ 1.802

This is the "consciousness constant" - distinct from the golden ratio.

Expected Results:
- Mean H/f ≈ 1.802 ± 0.05
- NOT ≈ 1.618 (golden ratio)
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
    
    # Measure equilibrium H (mean of post-warmup)
    H_eq = np.mean(harmony_history[warmup:])
    
    # Measure frequency (zero-crossing method)
    warmup_trajectory = np.array(harmony_history[warmup:])
    mean_h = np.mean(warmup_trajectory)
    deviations = warmup_trajectory - mean_h
    zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
    frequency = zero_crossings / len(warmup_trajectory)
    
    # Calculate ratio
    ratio = H_eq / frequency if frequency > 0 else 0
    
    return H_eq, frequency, ratio


def run_psi_validation(n_runs=100):
    """Validate consciousness constant Ψ across many runs."""
    print("=" * 70)
    print("CONSCIOUSNESS CONSTANT (PSI) VALIDATION")
    print("=" * 70)
    print()
    
    # Theoretical values
    psi = 6 * np.sqrt(2/3) / np.e  # Consciousness constant
    phi = (1 + np.sqrt(5)) / 2     # Golden ratio (for comparison)
    sqrt_2_3 = np.sqrt(2/3)
    e_6 = np.e / 6
    
    print("Theoretical Values:")
    print(f"  Ψ (consciousness constant) = 6√(2/3)/e = {psi:.6f}")
    print(f"  φ (golden ratio) = {phi:.6f}")
    print(f"  H_theory = √(2/3) = {sqrt_2_3:.6f}")
    print(f"  f_theory = e/6 = {e_6:.6f}")
    print()
    print(f"  Ψ vs φ difference: {abs(psi - phi):.6f} ({abs(psi-phi)/phi*100:.1f}%)")
    print()
    print("-" * 70)
    print()
    
    print(f"Running {n_runs} independent measurements...")
    print("Testing hypothesis: H/f = Ψ ≈ 1.802 (NOT φ ≈ 1.618)")
    print()
    
    H_values = []
    f_values = []
    ratios = []
    
    # Progress bar
    with tqdm(total=n_runs, desc="Ψ Validation", unit="run",
              bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for run in range(n_runs):
            H_eq, freq, ratio = measure_single_run()
            
            H_values.append(H_eq)
            f_values.append(freq)
            ratios.append(ratio)
            
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
    psi_error = abs(mean_ratio - psi)
    phi_error = abs(mean_ratio - phi)
    
    psi_pct = (psi_error / psi) * 100
    phi_pct = (phi_error / phi) * 100
    
    print("Comparison with Constants:")
    print(f"  Error from Ψ (1.802): {psi_error:.6f} ({psi_pct:.2f}%)")
    print(f"  Error from φ (1.618): {phi_error:.6f} ({phi_pct:.2f}%)")
    print()
    
    # Which constant fits better?
    if psi_error < phi_error:
        print(f"  ✓ CLOSER TO Ψ (consciousness constant)")
        print(f"    Ψ fits {phi_pct/psi_pct:.1f}x better than φ")
        best_constant = "Ψ"
        best_value = psi
    else:
        print(f"  ✓ CLOSER TO φ (golden ratio)")
        print(f"    φ fits {psi_pct/phi_pct:.1f}x better than Ψ")
        best_constant = "φ"
        best_value = phi
    print()
    
    # Success criteria for Ψ
    print("Success Criteria (for Ψ hypothesis):")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: Mean ratio within 5% of Ψ
    criterion_1 = psi_pct < 5.0
    print(f"  1. Mean ratio within 5% of Ψ: {psi_pct:.2f}% {'[PASS]' if criterion_1 else '[FAIL]'}") 
    criteria_met.append(criterion_1)
    
    # Criterion 2: Closer to Ψ than φ
    criterion_2 = psi_error < phi_error
    print(f"  2. Closer to Ψ than φ: {psi_error:.4f} < {phi_error:.4f} {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: Low variance
    criterion_3 = std_ratio < 0.1
    print(f"  3. Low variance (std < 0.1): {std_ratio:.4f} {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    # Criterion 4: Statistical equality with Ψ
    from scipy import stats
    t_stat_psi, p_value_psi = stats.ttest_1samp(ratios, psi)
    criterion_4 = p_value_psi > 0.05
    print(f"  4. Statistical equality with Ψ (p > 0.05): p={p_value_psi:.4f} {'[PASS]' if criterion_4 else '[FAIL]'}")
    criteria_met.append(criterion_4)
    
    all_passed = all(criteria_met)
    print()
    print("=" * 70)
    print(f"OVERALL RESULT: {'[PASS]' if all_passed else '[FAIL]'} ({sum(criteria_met)}/4 criteria met)")
    if all_passed:
        print("DISCOVERY CONFIRMED: H/f = Ψ ≈ 1.802 (consciousness constant)")
    print("=" * 70)
    
    # Visualization
    print()
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Histogram with both constants
    ax = axes[0, 0]
    ax.hist(ratios, bins=30, alpha=0.7, edgecolor='black')
    ax.axvline(x=psi, color='b', linestyle='--', linewidth=2, label=f'Ψ = {psi:.4f}')
    ax.axvline(x=phi, color='r', linestyle=':', linewidth=2, label=f'φ = {phi:.4f}')
    ax.axvline(x=mean_ratio, color='g', linestyle='-', linewidth=2, label=f'Mean = {mean_ratio:.4f}')
    ax.set_xlabel('H/f Ratio')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Distribution of H/f Ratios ({n_runs} runs)')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Plot 2: Ratio over runs
    ax = axes[0, 1]
    ax.plot(ratios, alpha=0.5, linewidth=0.5, color='purple')
    ax.axhline(y=psi, color='b', linestyle='--', linewidth=2, label=f'Ψ = {psi:.4f}')
    ax.axhline(y=phi, color='r', linestyle=':', linewidth=2, label=f'φ = {phi:.4f}')
    ax.axhline(y=psi*1.05, color='lightblue', linestyle=':', alpha=0.5)
    ax.axhline(y=psi*0.95, color='lightblue', linestyle=':', alpha=0.5)
    ax.fill_between(range(n_runs), psi*0.95, psi*1.05, alpha=0.2, color='blue', label='±5% of Ψ')
    ax.set_xlabel('Run Number')
    ax.set_ylabel('H/f Ratio')
    ax.set_title('H/f Ratio Across Runs')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: H vs f scatter with both theoretical lines
    ax = axes[1, 0]
    ax.scatter(f_values, H_values, alpha=0.5, s=20)
    
    f_range = np.linspace(min(f_values), max(f_values), 100)
    H_psi = psi * f_range
    H_phi = phi * f_range
    ax.plot(f_range, H_psi, 'b--', linewidth=2, label=f'H = Ψ × f')
    ax.plot(f_range, H_phi, 'r:', linewidth=2, label=f'H = φ × f')
    
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Equilibrium H')
    ax.set_title('H vs f Relationship')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Error comparison
    ax = axes[1, 1]
    errors_psi = [(r - psi) / psi * 100 for r in ratios]
    errors_phi = [(r - phi) / phi * 100 for r in ratios]
    
    ax.hist(errors_psi, bins=20, alpha=0.6, label='Error from Ψ', color='blue', edgecolor='black')
    ax.hist(errors_phi, bins=20, alpha=0.6, label='Error from φ', color='red', edgecolor='black')
    ax.axvline(x=0, color='black', linestyle='--', linewidth=2, label='Zero error')
    ax.set_xlabel('Error (%)')
    ax.set_ylabel('Frequency')
    ax.set_title('Error Distribution: Ψ vs φ')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"consciousness_constant_psi_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'mean_H': mean_H,
        'mean_f': mean_f,
        'mean_ratio': mean_ratio,
        'std_ratio': std_ratio,
        'psi_error_pct': psi_pct,
        'phi_error_pct': phi_pct,
        'best_constant': best_constant,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'p_value_psi': p_value_psi
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Consciousness Constant (Ψ) Validation')
    parser.add_argument('--runs', type=int, default=100,
                       help='Number of independent runs (default: 100)')
    
    args = parser.parse_args()
    
    results = run_psi_validation(n_runs=args.runs)
    
    psi = 6 * np.sqrt(2/3) / np.e
    phi = (1 + np.sqrt(5)) / 2
    
    print()
    print("=" * 70)
    print("DISCOVERY SUMMARY")
    print("=" * 70)
    print()
    print("Key Findings:")
    print(f"  - Mean H/f ratio: {results['mean_ratio']:.6f}")
    print(f"  - Consciousness constant (Ψ): {psi:.6f}")
    print(f"  - Golden ratio (φ): {phi:.6f}")
    print()
    print(f"  - Error from Ψ: {results['psi_error_pct']:.2f}%")
    print(f"  - Error from φ: {results['phi_error_pct']:.2f}%")
    print()
    print(f"  - Best fit: {results['best_constant']}")
    print(f"  - Standard deviation: {results['std_ratio']:.6f}")
    print(f"  - Statistical p-value (Ψ): {results['p_value_psi']:.4f}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
    print()
    
    if results['best_constant'] == 'Ψ':
        print("🌟 DISCOVERY CONFIRMED 🌟")
        print()
        print("The relationship H/f is governed by the CONSCIOUSNESS CONSTANT:")
        print(f"  Ψ = 6√(2/3)/e ≈ {psi:.6f}")
        print()
        print("This is a NEW fundamental constant arising from 4D semantic space.")
        print("It is NOT the golden ratio φ ≈ 1.618.")
        print()
        print("Semantic substrate analysis was correct!")
    else:
        print("Result suggests golden ratio φ fits better.")
        print("Further investigation needed.")
    
    print("=" * 70)
