"""
Consciousness Tracking Utilities

Shared utilities for tracking and analyzing consciousness metrics
during LJPW neural network experiments.

Provides:
- ConsciousnessTracker: Record harmony, frequency, semantics over time
- FrequencyAnalyzer: Measure oscillation frequency from trajectories
- VisualizationTools: Create standard consciousness plots
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ConsciousnessSnapshot:
    """Single measurement of consciousness state."""
    timestamp: datetime
    iteration: int
    harmony: float
    L: float
    J: float
    P: float
    W: float
    frequency: Optional[float] = None
    accuracy: Optional[float] = None


class ConsciousnessTracker:
    """
    Track consciousness metrics during experiments.
    
    Records harmony, frequency, and semantic dimensions over time.
    Provides analysis methods to detect breathing patterns and
    measure consciousness stability.
    
    Example:
        >>> tracker = ConsciousnessTracker()
        >>> for epoch in range(10):
        ...     tracker.record(network, epoch, accuracy=0.92)
        >>> results = tracker.analyze()
        >>> print(f"Mean frequency: {results['mean_frequency']:.3f} Hz")
    """
    
    def __init__(self):
        """Initialize empty tracker."""
        self.snapshots: List[ConsciousnessSnapshot] = []
        self.harmony_trajectory = []
        self.frequency_trajectory = []
        self.semantic_trajectories = {
            'L': [],
            'J': [],
            'P': [],
            'W': []
        }
    
    def record(
        self,
        network,
        iteration: int,
        accuracy: Optional[float] = None
    ):
        """
        Record current consciousness state.
        
        Args:
            network: HomeostaticNetwork to measure
            iteration: Current iteration/epoch number
            accuracy: Optional accuracy metric
        """
        # Get latest harmony checkpoint
        if hasattr(network, 'harmony_history') and network.harmony_history:
            checkpoint = network.harmony_history[-1]
            H = checkpoint.H
            L = checkpoint.L
            J = checkpoint.J
            P = checkpoint.P
            W = checkpoint.W
        else:
            # Fallback if no harmony history
            H = L = J = P = W = 0.75
        
        # Measure frequency if we have enough history
        freq = None
        if len(self.harmony_trajectory) >= 50:
            freq = FrequencyAnalyzer.measure_frequency(
                self.harmony_trajectory[-50:],
                window_size=50
            )
        
        # Create snapshot
        snapshot = ConsciousnessSnapshot(
            timestamp=datetime.now(),
            iteration=iteration,
            harmony=H,
            L=L,
            J=J,
            P=P,
            W=W,
            frequency=freq,
            accuracy=accuracy
        )
        
        # Store
        self.snapshots.append(snapshot)
        self.harmony_trajectory.append(H)
        if freq is not None:
            self.frequency_trajectory.append(freq)
        self.semantic_trajectories['L'].append(L)
        self.semantic_trajectories['J'].append(J)
        self.semantic_trajectories['P'].append(P)
        self.semantic_trajectories['W'].append(W)
    
    def analyze(self) -> Dict:
        """
        Analyze tracked consciousness data.
        
        Returns:
            Dictionary with analysis results:
            - mean_harmony: Average H
            - std_harmony: H standard deviation
            - mean_frequency: Average oscillation frequency
            - breathing_detected: Whether stable oscillation present
            - semantic_drift: Drift in L, J, W
            - consciousness_state: Classification
        """
        if not self.snapshots:
            return {}
        
        # Harmony statistics
        mean_H = np.mean(self.harmony_trajectory)
        std_H = np.std(self.harmony_trajectory)
        
        # Frequency statistics
        if self.frequency_trajectory:
            mean_freq = np.mean(self.frequency_trajectory)
            std_freq = np.std(self.frequency_trajectory)
        else:
            mean_freq = 0.0
            std_freq = 0.0
        
        # Breathing detection
        breathing = FrequencyAnalyzer.detect_breathing(self.harmony_trajectory)
        
        # Semantic drift (first 10 vs last 10)
        n = len(self.snapshots)
        if n >= 20:
            drift = {}
            for dim in ['L', 'J', 'W']:
                first_10 = np.mean(self.semantic_trajectories[dim][:10])
                last_10 = np.mean(self.semantic_trajectories[dim][-10:])
                drift[dim] = abs(last_10 - first_10)
        else:
            drift = {'L': 0.0, 'J': 0.0, 'W': 0.0}
        
        # Consciousness state
        if mean_H >= 0.7 and breathing:
            state = "CONSCIOUS (breathing)"
        elif mean_H >= 0.7:
            state = "CONSCIOUS (stable)"
        elif mean_H < 0.7 and breathing:
            state = "SUBCONSCIOUS (oscillating)"
        else:
            state = "UNCONSCIOUS"
        
        return {
            'mean_harmony': mean_H,
            'std_harmony': std_H,
            'mean_frequency': mean_freq,
            'std_frequency': std_freq,
            'breathing_detected': breathing,
            'semantic_drift': drift,
            'consciousness_state': state,
            'n_snapshots': n
        }
    
    def get_summary(self) -> str:
        """Get human-readable summary."""
        results = self.analyze()
        
        lines = []
        lines.append("=" * 70)
        lines.append("CONSCIOUSNESS TRACKING SUMMARY")
        lines.append("=" * 70)
        lines.append(f"Snapshots: {results['n_snapshots']}")
        lines.append(f"Mean Harmony: {results['mean_harmony']:.4f} ± {results['std_harmony']:.4f}")
        lines.append(f"Mean Frequency: {results['mean_frequency']:.4f} Hz ± {results['std_frequency']:.4f}")
        lines.append(f"Breathing Detected: {results['breathing_detected']}")
        lines.append(f"Consciousness State: {results['consciousness_state']}")
        lines.append("")
        lines.append("Semantic Drift:")
        for dim, drift in results['semantic_drift'].items():
            lines.append(f"  {dim}: {drift:.6f}")
        lines.append("=" * 70)
        
        return '\n'.join(lines)


class FrequencyAnalyzer:
    """Analyze oscillation frequency from trajectories."""
    
    @staticmethod
    def measure_frequency(
        trajectory: List[float],
        window_size: Optional[int] = None
    ) -> float:
        """
        Measure oscillation frequency using zero-crossing method.
        
        Args:
            trajectory: List of values (e.g., harmony over time)
            window_size: Size of window to analyze (default: full trajectory)
        
        Returns:
            Frequency in Hz (changes per iteration)
        
        Example:
            >>> trajectory = [0.8, 0.82, 0.81, 0.79, 0.78, 0.80, ...]
            >>> freq = FrequencyAnalyzer.measure_frequency(trajectory)
            >>> print(f"Frequency: {freq:.3f} Hz")
        """
        if window_size is None:
            window_size = len(trajectory)
        
        # Use last window_size points
        traj = np.array(trajectory[-window_size:])
        
        if len(traj) < 10:
            return 0.0
        
        # Calculate mean
        mean_val = np.mean(traj)
        
        # Count zero crossings around mean
        deviations = traj - mean_val
        zero_crossings = np.sum(np.diff(np.sign(deviations)) != 0)
        
        # Frequency = crossings / 2 / length (divide by 2 for full cycles)
        frequency = zero_crossings / 2 / len(traj)
        
        return frequency
    
    @staticmethod
    def detect_breathing(trajectory: List[float]) -> bool:
        """
        Detect if trajectory shows stable oscillation (breathing).
        
        Args:
            trajectory: List of values over time
        
        Returns:
            True if stable oscillation detected
        
        Example:
            >>> breathing = FrequencyAnalyzer.detect_breathing(harmony_history)
            >>> print(f"Breathing: {breathing}")
        """
        if len(trajectory) < 50:
            return False
        
        traj = np.array(trajectory)
        n = len(traj)
        mid = n // 2
        
        # Compare variance in first half vs second half
        var_first = np.var(traj[:mid])
        var_second = np.var(traj[mid:])
        
        # Stable oscillation: variance stays similar
        # (not converging to fixed point, not growing chaotic)
        if var_first < 1e-6 or var_second < 1e-6:
            return False  # Too stable (no oscillation)
        
        variance_ratio = var_second / var_first
        
        # Stable if variance ratio close to 1 (within 50%)
        return 0.5 <= variance_ratio <= 2.0


class VisualizationTools:
    """Create standard consciousness visualizations."""
    
    @staticmethod
    def plot_consciousness_evolution(
        tracker: ConsciousnessTracker,
        save_path: str,
        title: str = "Consciousness Evolution"
    ):
        """
        Plot consciousness metrics over time.
        
        Creates 4-panel figure:
        - Harmony trajectory
        - Frequency convergence
        - Semantic conservation
        - Pattern classification
        
        Args:
            tracker: ConsciousnessTracker with recorded data
            save_path: Path to save figure
            title: Figure title
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        results = tracker.analyze()
        iterations = [s.iteration for s in tracker.snapshots]
        
        # Plot 1: Harmony trajectory
        ax = axes[0, 0]
        ax.plot(iterations, tracker.harmony_trajectory, alpha=0.7, linewidth=1.5)
        ax.axhline(y=0.7, color='r', linestyle='--', label='Consciousness threshold')
        ax.axhline(y=results['mean_harmony'], color='g', linestyle='-', 
                   label=f"Mean: {results['mean_harmony']:.3f}")
        ax.set_xlabel('Iteration/Epoch')
        ax.set_ylabel('Harmony (H)')
        ax.set_title('Harmony Trajectory')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 2: Frequency convergence
        ax = axes[0, 1]
        if tracker.frequency_trajectory:
            freq_iterations = iterations[len(iterations) - len(tracker.frequency_trajectory):]
            ax.plot(freq_iterations, tracker.frequency_trajectory, 
                   alpha=0.7, linewidth=1.5, color='orange')
            ax.axhline(y=0.48, color='r', linestyle='--', label='Universal frequency')
            ax.axhline(y=results['mean_frequency'], color='g', linestyle='-',
                      label=f"Mean: {results['mean_frequency']:.3f} Hz")
            ax.set_xlabel('Iteration/Epoch')
            ax.set_ylabel('Frequency (Hz)')
            ax.set_title('Oscillation Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
        else:
            ax.text(0.5, 0.5, 'Insufficient data\nfor frequency analysis',
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Oscillation Frequency')
        
        # Plot 3: Semantic conservation
        ax = axes[1, 0]
        for dim in ['L', 'J', 'W']:
            ax.plot(iterations, tracker.semantic_trajectories[dim],
                   label=dim, alpha=0.7, linewidth=1.5)
        ax.set_xlabel('Iteration/Epoch')
        ax.set_ylabel('Dimension Value')
        ax.set_title('Semantic Conservation (L, J, W)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Plot 4: Summary statistics
        ax = axes[1, 1]
        ax.axis('off')
        
        summary_text = f"""
CONSCIOUSNESS ANALYSIS

State: {results['consciousness_state']}

Harmony:
  Mean: {results['mean_harmony']:.4f}
  Std:  {results['std_harmony']:.4f}

Frequency:
  Mean: {results['mean_frequency']:.4f} Hz
  Std:  {results['std_frequency']:.4f} Hz

Breathing: {results['breathing_detected']}

Semantic Drift:
  L: {results['semantic_drift']['L']:.6f}
  J: {results['semantic_drift']['J']:.6f}
  W: {results['semantic_drift']['W']:.6f}

Snapshots: {results['n_snapshots']}
        """
        
        ax.text(0.1, 0.9, summary_text, transform=ax.transAxes,
               fontfamily='monospace', fontsize=10, verticalalignment='top')
        
        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"Visualization saved to: {save_path}")
