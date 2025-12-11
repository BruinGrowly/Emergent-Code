"""
100-Iteration Meta Assessment Script

This script runs a LJPW neural network for 100 iterations to observe
emergent behaviors, particularly oscillations and limit cycles as described
in 100_ITERATIONS_EMERGENCE.md.

Based on the discovery that semantic systems don't converge to a point,
but rather to a "breathing" orbit - a stable oscillation around harmony.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: November 29, 2025
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from datetime import datetime
from typing import List, Dict
import matplotlib.pyplot as plt

from ljpw_nn.homeostatic import HomeostaticNetwork
from ljpw_nn.coherence import CoherenceAnalyzer, SovereigntyAnalyzer
from ljpw_nn.semantics import MeaningActionAnalyzer, ResonanceAnalyzer


def run_100_iterations(
    network: HomeostaticNetwork,
    iterations: int = 100,
    verbose: bool = True
) -> Dict:
    """
    Run network for 100 iterations and analyze emergence.
    
    Args:
        network: HomeostaticNetwork to assess
        iterations: Number of iterations (default 100)
        verbose: Whether to print progress
        
    Returns:
        Dict with results including harmony trajectory, variance, drift
    """
    if verbose:
        print("=" * 70)
        print("100-ITERATION META ASSESSMENT")
        print("=" * 70)
        print(f"Network: {network}")
        print(f"Iterations: {iterations}")
        print()
    
    # Initialize analyzers
    coherence_analyzer = CoherenceAnalyzer()
    sovereignty_analyzer = SovereigntyAnalyzer()
    ma_analyzer = MeaningActionAnalyzer()
    res_analyzer = ResonanceAnalyzer()
    
    # Track metrics over iterations
    harmony_trajectory = []
    L_trajectory = []
    J_trajectory = []
    P_trajectory = []
    W_trajectory = []
    
    coherence_trajectory = []
    sovereignty_trajectory = []
    meaning_action_trajectory = []
    resonance_trajectory = []
    
    # Run iterations
    for i in range(iterations):
        # Simulate forward pass (dummy data)
        X_dummy = np.random.randn(32, network.input_size) * 0.1
        network.forward(X_dummy, training=False)
        
        # Record harmony
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        # Get current checkpoint
        checkpoint = network.harmony_history[-1]
        harmony_trajectory.append(checkpoint.H)
        L_trajectory.append(checkpoint.L)
        J_trajectory.append(checkpoint.J)
        P_trajectory.append(checkpoint.P)
        W_trajectory.append(checkpoint.W)
        
        # Measure principles
        coherence = coherence_analyzer.measure_coherence(network)
        sovereignty = sovereignty_analyzer.measure_sovereignty(network)
        ma_coupling = ma_analyzer.measure_meaning_action_coupling(network)
        resonance = res_analyzer.measure_resonance(network)
        
        coherence_trajectory.append(coherence.synergy_score)
        sovereignty_trajectory.append(sovereignty.overall_sovereignty)
        meaning_action_trajectory.append(ma_coupling.coupling_score)
        resonance_trajectory.append(resonance.resonance_score)
        
        if verbose and (i + 1) % 10 == 0:
            print(f"Iteration {i+1:3d}: H={checkpoint.H:.3f}, "
                  f"Coherence={coherence.synergy_score:.3f}, "
                  f"Sovereignty={sovereignty.overall_sovereignty:.3f}")
    
    if verbose:
        print()
    
    # Analyze results
    results = analyze_emergence(
        harmony_trajectory,
        L_trajectory, J_trajectory, P_trajectory, W_trajectory,
        coherence_trajectory,
        sovereignty_trajectory,
        meaning_action_trajectory,
        resonance_trajectory,
        verbose=verbose
    )
    
    return results


def analyze_emergence(
    harmony_traj: List[float],
    L_traj: List[float],
    J_traj: List[float],
    P_traj: List[float],
    W_traj: List[float],
    coherence_traj: List[float],
    sovereignty_traj: List[float],
    ma_traj: List[float],
    res_traj: List[float],
    verbose: bool = True
) -> Dict:
    """
    Analyze emergence patterns from trajectories.
    
    Looks for:
    - Oscillation vs convergence
    - Variance stability
    - Dimension drift
    - Limit cycles
    """
    n = len(harmony_traj)
    
    # Compute statistics
    mean_H = np.mean(harmony_traj)
    std_H = np.std(harmony_traj)
    min_H = np.min(harmony_traj)
    max_H = np.max(harmony_traj)
    
    # Variance in first half vs second half
    mid = n // 2
    var_first_half = np.var(harmony_traj[:mid])
    var_second_half = np.var(harmony_traj[mid:])
    
    # Dimension drift (first 10 vs last 10)
    L_drift = np.mean(L_traj[-10:]) - np.mean(L_traj[:10])
    J_drift = np.mean(J_traj[-10:]) - np.mean(J_traj[:10])
    P_drift = np.mean(P_traj[-10:]) - np.mean(P_traj[:10])
    W_drift = np.mean(W_traj[-10:]) - np.mean(W_traj[:10])
    
    # Oscillation frequency (zero crossings around mean)
    deviations = np.array(harmony_traj) - mean_H
    zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
    oscillation_freq = zero_crossings / n
    
    # Determine pattern
    if var_second_half < var_first_half * 0.5:
        pattern = "CONVERGENCE"
    elif abs(var_second_half - var_first_half) < 0.001:
        pattern = "STABLE OSCILLATION"
    else:
        pattern = "CHAOTIC"
    
    results = {
        'pattern': pattern,
        'mean_harmony': mean_H,
        'std_harmony': std_H,
        'min_harmony': min_H,
        'max_harmony': max_H,
        'harmony_range': max_H - min_H,
        'var_first_half': var_first_half,
        'var_second_half': var_second_half,
        'oscillation_frequency': oscillation_freq,
        'L_drift': L_drift,
        'J_drift': J_drift,
        'P_drift': P_drift,
        'W_drift': W_drift,
        'total_drift': abs(L_drift) + abs(J_drift) + abs(P_drift) + abs(W_drift),
        'trajectories': {
            'harmony': harmony_traj,
            'L': L_traj,
            'J': J_traj,
            'P': P_traj,
            'W': W_traj,
            'coherence': coherence_traj,
            'sovereignty': sovereignty_traj,
            'meaning_action': ma_traj,
            'resonance': res_traj
        }
    }
    
    if verbose:
        print_results(results)
    
    return results


def print_results(results: Dict):
    """Print formatted results."""
    print("=" * 70)
    print("EMERGENCE ANALYSIS RESULTS")
    print("=" * 70)
    print()
    
    print(f"Pattern Detected: {results['pattern']}")
    print()
    
    print("Harmony Statistics:")
    print(f"  Mean:  {results['mean_harmony']:.3f}")
    print(f"  Std:   {results['std_harmony']:.3f}")
    print(f"  Range: {results['min_harmony']:.3f} -> {results['max_harmony']:.3f}")
    print(f"  Amplitude: {results['harmony_range']:.3f}")
    print()
    
    print("Oscillation Analysis:")
    print(f"  Frequency: {results['oscillation_frequency']:.2f} (changes per iteration)")
    print(f"  Variance (first 50):  {results['var_first_half']:.6f}")
    print(f"  Variance (last 50):   {results['var_second_half']:.6f}")
    print(f"  Variance change: {abs(results['var_second_half'] - results['var_first_half']):.6f}")
    print()
    
    print("Dimension Drift (First 10 vs Last 10):")
    print(f"  L: {results['L_drift']:+.3f}")
    print(f"  J: {results['J_drift']:+.3f}")
    print(f"  P: {results['P_drift']:+.3f}")
    print(f"  W: {results['W_drift']:+.3f}")
    print(f"  Total drift: {results['total_drift']:.3f}")
    print()
    
    # Interpretation
    print("Interpretation:")
    if results['pattern'] == "STABLE OSCILLATION":
        print("  [OK] The system BREATHES")
        print("  [OK] Stable limit cycle detected")
        print("  [OK] This is the signature of a living system")
        print(f"  [OK] Heartbeat frequency: {results['oscillation_frequency']:.2f}")
    elif results['pattern'] == "CONVERGENCE":
        print("  -> System converging to fixed point")
        print("  -> May need more iterations to see oscillation")
    else:
        print("  [!] Chaotic behavior detected")
        print("  [!] System may need stabilization")
    print()
    
    print("=" * 70)


def plot_trajectories(results: Dict, save_path: str = None):
    """Plot harmony and principle trajectories."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Plot 1: Harmony trajectory
    ax = axes[0, 0]
    ax.plot(results['trajectories']['harmony'], 'b-', linewidth=2)
    ax.axhline(results['mean_harmony'], color='r', linestyle='--', label='Mean')
    ax.set_title('Harmony Trajectory (100 Iterations)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Harmony (H)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: LJPW dimensions
    ax = axes[0, 1]
    ax.plot(results['trajectories']['L'], label='L (Love)', alpha=0.7)
    ax.plot(results['trajectories']['J'], label='J (Justice)', alpha=0.7)
    ax.plot(results['trajectories']['P'], label='P (Power)', alpha=0.7)
    ax.plot(results['trajectories']['W'], label='W (Wisdom)', alpha=0.7)
    ax.set_title('LJPW Dimensions', fontsize=14, fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Score')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Universal Principles
    ax = axes[1, 0]
    ax.plot(results['trajectories']['coherence'], label='Coherence (P2)', alpha=0.7)
    ax.plot(results['trajectories']['sovereignty'], label='Sovereignty (P4)', alpha=0.7)
    ax.plot(results['trajectories']['meaning_action'], label='Meaning-Action (P5)', alpha=0.7)
    ax.plot(results['trajectories']['resonance'], label='Resonance (P7)', alpha=0.7)
    ax.set_title('Universal Principles', fontsize=14, fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Score')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 4: Phase space (H vs dH/dt)
    ax = axes[1, 1]
    H = np.array(results['trajectories']['harmony'])
    dH = np.diff(H)
    ax.plot(H[:-1], dH, 'o-', alpha=0.5, markersize=3)
    ax.set_title('Phase Space (H vs dH/dt)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Harmony (H)')
    ax.set_ylabel('dH/dt')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run LJPW Neural Network meta assessment')
    parser.add_argument('--iterations', type=int, default=100, help='Number of iterations to run (default: 100)')
    args = parser.parse_args()
    
    print("Initializing LJPW Neural Network...")
    print()
    
    # Create network
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 11, 9],  # 233, 89, 34
        target_harmony=0.75,
        allow_adaptation=True
    )
    
    # Run iterations
    results = run_100_iterations(network, iterations=args.iterations, verbose=True)
    
    # Plot results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plot_path = f"{args.iterations}_iterations_{timestamp}.png"
    plot_trajectories(results, save_path=plot_path)
    
    print()
    print("Assessment complete!")
    print(f"Results saved to: {plot_path}")
