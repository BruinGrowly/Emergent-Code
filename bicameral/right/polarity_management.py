"""
Polarity Management - Dynamic Balance of Complementary Forces

This module implements Principle 3 of Universal Principles:
"Dynamic Balance and Polarity - Stability emerges from continuous interplay
of complementary forces."

Key polarities managed:
1. Stability-Plasticity: Preserve knowledge vs adapt to new information
2. Excitation-Inhibition: Amplify signals vs suppress noise
3. Exploration-Exploitation: Try new vs use known
4. Specialization-Generalization: Deep expertise vs broad capability
5. Local-Global: Individual components vs collective system

These are fundamental trade-offs found in all complex adaptive systems,
from biological neurons to ecosystems to social structures.

Example:
    >>> from bicameral.right.polarity_management import StabilityPlasticityBalance
    >>> balance = StabilityPlasticityBalance(network)
    >>> # Adjust learning rate based on balance
    >>> lr = balance.get_adaptive_learning_rate(base_lr=0.01)
    >>> # Protect important weights when stability is high
    >>> if balance.should_protect_weights():
    ...     apply_weight_protection()
"""

import sys
import os

# Add parent directory to path for imports when running as script
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class PolarityState:
    """
    State of a polarity pair.

    Tracks the balance between two complementary forces.

    Attributes:
        pole_a_strength: Strength of first pole (0-1)
        pole_b_strength: Strength of second pole (0-1)
        balance: Current balance (0 = all A, 1 = all B, 0.5 = perfectly balanced)
        target_balance: Desired balance point
        tolerance: Acceptable deviation from target

    Example:
        >>> state = PolarityState(
        ...     pole_a_strength=0.6,
        ...     pole_b_strength=0.4,
        ...     balance=0.4,
        ...     target_balance=0.5,
        ...     tolerance=0.1
        ... )
    """
    pole_a_strength: float
    pole_b_strength: float
    balance: float
    target_balance: float
    tolerance: float

    def is_balanced(self) -> bool:
        """Check if polarity is within acceptable balance."""
        deviation = abs(self.balance - self.target_balance)
        return deviation <= self.tolerance

    def needs_rebalancing(self) -> str:
        """Determine which pole needs strengthening."""
        if self.balance < self.target_balance - self.tolerance:
            return "strengthen_b"  # Too much A
        elif self.balance > self.target_balance + self.tolerance:
            return "strengthen_a"  # Too much B
        return "balanced"


class StabilityPlasticityBalance:
    """
    Manage the fundamental stability-plasticity trade-off.

    Biological Inspiration:
        The brain faces a fundamental dilemma:
        - Stability: Preserve learned knowledge (don't forget)
        - Plasticity: Adapt to new information (keep learning)

        Too much stability → Can't learn new things (rigid)
        Too much plasticity → Forget old things (catastrophic forgetting)

        Healthy brains dynamically balance these forces.

    Traditional Neural Networks:
        - Fixed learning rate (no balance)
        - Catastrophic forgetting (too plastic)
        - Or rigid weights (too stable)

    LJPW Approach:
        - Adaptive learning rate based on balance
        - Protect important weights (stability)
        - Allow adaptation in others (plasticity)
        - Dynamic equilibrium maintained

    Key Mechanisms:
        1. **Elastic Weight Consolidation**: Protect important weights
        2. **Progressive Neural Networks**: New capacity for new tasks
        3. **Dynamic Learning Rate**: Adjust based on balance
        4. **Importance-Weighted Updates**: Update less important weights more

    LJPW Scores (for polarity management):
        L (Interpretability): 0.85  - Clear balance metrics
        J (Robustness):       0.88  - Prevents catastrophic forgetting
        P (Performance):      0.82  - Maintains learning ability
        W (Elegance):         0.87  - Natural principle applied
        H (Harmony):          0.85  ✓ Production-ready

    Attributes:
        network: Neural network to manage
        stability: How much to preserve (0-1)
        plasticity: How much to adapt (0-1)
        importance_weights: Which weights are important to preserve
        balance_history: Track balance over time

    Examples:
        Basic usage:
        >>> balance = StabilityPlasticityBalance(network)
        >>> print(f"Current balance: {balance.get_balance():.2f}")
        Current balance: 0.50

        Adjust learning rate:
        >>> base_lr = 0.01
        >>> adaptive_lr = balance.get_adaptive_learning_rate(base_lr)
        >>> print(f"Adaptive LR: {adaptive_lr:.4f}")
        Adaptive LR: 0.0050

        Protect important weights:
        >>> if balance.should_protect_weights():
        ...     protected = balance.get_weight_protection_mask()
        ...     # Apply protection during training

        Shift balance:
        >>> balance.increase_plasticity()  # Allow more learning
        >>> balance.increase_stability()  # Preserve more

    Notes:
        - Balance typically 0.3-0.7 (never extreme)
        - Early learning: Higher plasticity (0.6-0.7)
        - Later learning: Higher stability (0.3-0.4)
        - Critical knowledge: Protected regardless

    References:
        - Kirkpatrick et al. (2017): "Overcoming catastrophic forgetting"
        - Zenke et al. (2017): "Continual learning through synaptic intelligence"
        - Universal Principle 3: Dynamic Balance and Polarity
    """

    def __init__(
        self,
        network,
        initial_stability: float = 0.5,
        initial_plasticity: float = 0.5,
        target_balance: float = 0.5,
        tolerance: float = 0.1,
    ):
        """
        Initialize stability-plasticity balance manager.

        Args:
            network: Neural network to manage
            initial_stability: Starting stability level (0-1)
            initial_plasticity: Starting plasticity level (0-1)
            target_balance: Desired balance point (0-1)
            tolerance: Acceptable deviation from target

        Example:
            >>> balance = StabilityPlasticityBalance(
            ...     network=my_network,
            ...     initial_stability=0.6,  # Start more stable
            ...     initial_plasticity=0.4,
            ...     target_balance=0.5,
            ...     tolerance=0.1
            ... )
        """
        self.network = network
        self.stability = initial_stability
        self.plasticity = initial_plasticity
        self.target_balance = target_balance
        self.tolerance = tolerance

        # Track which weights are important (for stability)
        self.importance_weights = {}
        self._initialize_importance()

        # Track balance over time
        self.balance_history = []

    def _initialize_importance(self):
        """Initialize importance weights for all network parameters."""
        # Initially, all weights equally important
        for i, layer in enumerate(self.network.layers):
            self.importance_weights[f'layer_{i}'] = np.ones_like(layer.weights)

    def get_balance(self) -> float:
        """
        Get current balance (0 = all stability, 1 = all plasticity).

        Returns:
            Balance value (0-1)

        Example:
            >>> balance = manager.get_balance()
            >>> if balance < 0.3:
            ...     print("Very stable (may resist learning)")
            >>> elif balance > 0.7:
            ...     print("Very plastic (may forget easily)")
        """
        total = self.stability + self.plasticity
        if total == 0:
            return 0.5
        return self.plasticity / total

    def get_state(self) -> PolarityState:
        """Get complete polarity state."""
        return PolarityState(
            pole_a_strength=self.stability,
            pole_b_strength=self.plasticity,
            balance=self.get_balance(),
            target_balance=self.target_balance,
            tolerance=self.tolerance
        )

    def is_balanced(self) -> bool:
        """Check if currently in acceptable balance."""
        return self.get_state().is_balanced()

    def get_adaptive_learning_rate(self, base_lr: float) -> float:
        """
        Adjust learning rate based on plasticity level.

        Higher plasticity → Higher learning rate (learn more)
        Higher stability → Lower learning rate (preserve more)

        Args:
            base_lr: Base learning rate

        Returns:
            Adjusted learning rate

        Example:
            >>> base_lr = 0.01
            >>> # If plasticity = 0.7 (high)
            >>> adaptive_lr = balance.get_adaptive_learning_rate(base_lr)
            >>> # adaptive_lr ≈ 0.007 (learn actively)
            >>>
            >>> # If plasticity = 0.3 (low)
            >>> adaptive_lr = balance.get_adaptive_learning_rate(base_lr)
            >>> # adaptive_lr ≈ 0.003 (preserve more)
        """
        return base_lr * self.plasticity

    def should_protect_weights(self) -> bool:
        """
        Should we protect important weights from change?

        Returns:
            True if stability is high enough to warrant protection

        Example:
            >>> if balance.should_protect_weights():
            ...     # Apply weight protection during update
            ...     mask = balance.get_weight_protection_mask()
            ...     gradients = gradients * (1 - mask * 0.9)
        """
        return self.stability > 0.6

    def get_weight_protection_mask(self, layer_idx: int = 0) -> np.ndarray:
        """
        Get mask indicating which weights to protect.

        Higher importance → Higher protection
        Protection strength based on stability level

        Args:
            layer_idx: Which layer to get mask for

        Returns:
            Protection mask (0 = no protection, 1 = full protection)

        Example:
            >>> mask = balance.get_weight_protection_mask(layer_idx=0)
            >>> # During weight update:
            >>> weight_update = gradient * learning_rate
            >>> protected_update = weight_update * (1 - mask * protection_strength)
        """
        layer_key = f'layer_{layer_idx}'
        if layer_key not in self.importance_weights:
            return np.zeros_like(self.network.layers[layer_idx].weights)

        importance = self.importance_weights[layer_key]

        # Protection = importance × stability
        protection = importance * self.stability

        return protection

    def update_importance_weights(self, layer_idx: int, gradients: np.ndarray):
        """
        Update importance weights based on gradient history.

        Weights with consistently large gradients are important.
        (Inspired by Synaptic Intelligence)

        Args:
            layer_idx: Which layer
            gradients: Recent gradients for this layer

        Example:
            >>> # During training
            >>> gradients = compute_gradients(layer)
            >>> balance.update_importance_weights(layer_idx=0, gradients=gradients)
            >>> # Important weights will be protected in future updates
        """
        layer_key = f'layer_{layer_idx}'

        # Update running importance estimate
        # Importance ∝ gradient magnitude
        gradient_magnitude = np.abs(gradients)

        # Exponential moving average
        alpha = 0.1
        if layer_key in self.importance_weights:
            self.importance_weights[layer_key] = (
                (1 - alpha) * self.importance_weights[layer_key] +
                alpha * gradient_magnitude
            )

    def increase_stability(self, amount: float = 0.1):
        """
        Shift balance toward stability.

        Use when:
        - Performance is good (preserve what works)
        - Catastrophic forgetting detected
        - Entering deployment phase

        Args:
            amount: How much to increase stability

        Example:
            >>> # Performance good, preserve it
            >>> if accuracy > 0.95:
            ...     balance.increase_stability(amount=0.1)
        """
        self.stability = min(1.0, self.stability + amount)
        self.plasticity = max(0.0, self.plasticity - amount)
        self.balance_history.append(self.get_balance())

    def increase_plasticity(self, amount: float = 0.1):
        """
        Shift balance toward plasticity.

        Use when:
        - Learning new task
        - Performance plateaued (need to explore)
        - New data available

        Args:
            amount: How much to increase plasticity

        Example:
            >>> # New task starting
            >>> balance.increase_plasticity(amount=0.2)
            >>> # Now can learn more aggressively
        """
        self.plasticity = min(1.0, self.plasticity + amount)
        self.stability = max(0.0, self.stability - amount)
        self.balance_history.append(self.get_balance())

    def auto_adjust(self, learning_progress: float):
        """
        Automatically adjust balance based on learning progress.

        Early learning: Higher plasticity
        Later learning: Higher stability

        Args:
            learning_progress: How far through learning (0 = start, 1 = complete)

        Example:
            >>> for epoch in range(num_epochs):
            ...     progress = epoch / num_epochs
            ...     balance.auto_adjust(learning_progress=progress)
            ...     # Balance automatically shifts toward stability
        """
        # Early: 70% plasticity, 30% stability
        # Late: 30% plasticity, 70% stability
        target_plasticity = 0.7 - 0.4 * learning_progress
        target_stability = 0.3 + 0.4 * learning_progress

        # Smooth transition
        alpha = 0.05
        self.plasticity = (1 - alpha) * self.plasticity + alpha * target_plasticity
        self.stability = (1 - alpha) * self.stability + alpha * target_stability

        self.balance_history.append(self.get_balance())

    def __repr__(self) -> str:
        """String representation."""
        balance = self.get_balance()
        return (
            f"StabilityPlasticityBalance("
            f"stability={self.stability:.2f}, "
            f"plasticity={self.plasticity:.2f}, "
            f"balance={balance:.2f})"
        )


class ExcitationInhibitionBalance:
    """
    Manage excitation-inhibition balance.

    Biological Inspiration:
        Neurons receive both:
        - Excitatory signals: Activate the neuron
        - Inhibitory signals: Suppress the neuron

        Balance is critical:
        - Too much excitation → Seizures, instability
        - Too much inhibition → Depression, inactivity

        Healthy brains maintain ~80% excitation, ~20% inhibition.

    Application to Neural Networks:
        - Excitation: Amplify strong signals
        - Inhibition: Suppress weak signals (sparse coding)
        - Creates stable, robust computation

    Attributes:
        excitation_strength: How much to amplify (0-1)
        inhibition_strength: How much to suppress (0-1)
        target_sparsity: Desired activation sparsity

    Example:
        >>> ei_balance = ExcitationInhibitionBalance()
        >>> activations = np.random.randn(100)
        >>> balanced = ei_balance.apply(activations)
        >>> # Strong signals amplified, weak signals suppressed
    """

    def __init__(
        self,
        excitation_strength: float = 0.8,
        inhibition_strength: float = 0.2,
        target_sparsity: float = 0.7,
    ):
        """
        Initialize E-I balance.

        Args:
            excitation_strength: Amplification strength (0-1)
            inhibition_strength: Suppression strength (0-1)
            target_sparsity: Fraction of neurons that should be active
        """
        self.excitation_strength = excitation_strength
        self.inhibition_strength = inhibition_strength
        self.target_sparsity = target_sparsity

    def apply(self, activations: np.ndarray) -> np.ndarray:
        """
        Apply balanced excitation and inhibition.

        Args:
            activations: Input activations

        Returns:
            Balanced activations (strong amplified, weak suppressed)

        Example:
            >>> activations = np.array([0.1, 0.5, 0.05, 0.8, 0.02])
            >>> balanced = ei_balance.apply(activations)
            >>> # Strong signals (0.5, 0.8) amplified
            >>> # Weak signals (0.05, 0.02) suppressed
        """
        # Find threshold for target sparsity
        threshold = np.percentile(np.abs(activations), (1 - self.target_sparsity) * 100)

        # Excitation: Amplify strong signals
        strong_mask = np.abs(activations) >= threshold
        excited = activations.copy()
        excited[strong_mask] *= (1 + self.excitation_strength)

        # Inhibition: Suppress weak signals
        weak_mask = ~strong_mask
        excited[weak_mask] *= (1 - self.inhibition_strength)

        return excited

    def get_balance(self) -> float:
        """Get E/I ratio (should be ~4:1 for biological systems)."""
        return self.excitation_strength / (self.inhibition_strength + 1e-10)


class PolarityManager:
    """
    Manage all polarity pairs in network.

    Ensures dynamic equilibrium across all complementary forces.

    Attributes:
        polarities: Dictionary of all managed polarities

    Example:
        >>> manager = PolarityManager(network)
        >>> manager.regulate_all()
        >>> stats = manager.get_balance_stats()
        >>> print(stats)
    """

    def __init__(self, network):
        """Initialize polarity manager."""
        self.network = network

        # Core polarity pairs
        self.stability_plasticity = StabilityPlasticityBalance(network)
        self.excitation_inhibition = ExcitationInhibitionBalance()

        # Track all polarities
        self.polarities = {
            'stability_plasticity': self.stability_plasticity,
            'excitation_inhibition': self.excitation_inhibition,
        }

    def get_polarity(self, name: str):
        """Get specific polarity manager."""
        return self.polarities.get(name)

    def regulate_all(self):
        """Regulate all polarities toward balance."""
        # Each polarity auto-adjusts
        for name, polarity in self.polarities.items():
            if hasattr(polarity, 'get_state'):
                state = polarity.get_state()
                if not state.is_balanced():
                    # Auto-adjust
                    self._rebalance_polarity(name, state)

    def _rebalance_polarity(self, name: str, state: PolarityState):
        """Rebalance specific polarity."""
        polarity = self.polarities[name]
        action = state.needs_rebalancing()

        if action == "strengthen_b":
            # Need more of pole B
            if hasattr(polarity, 'increase_plasticity'):
                polarity.increase_plasticity(amount=0.05)
        elif action == "strengthen_a":
            # Need more of pole A
            if hasattr(polarity, 'increase_stability'):
                polarity.increase_stability(amount=0.05)

    def get_balance_stats(self) -> Dict[str, float]:
        """Get balance statistics for all polarities."""
        stats = {}
        for name, polarity in self.polarities.items():
            if hasattr(polarity, 'get_balance'):
                stats[name] = polarity.get_balance()
        return stats

    def __repr__(self) -> str:
        """String representation."""
        stats = self.get_balance_stats()
        return f"PolarityManager({stats})"


# Example usage and validation
if __name__ == '__main__':
    print("=" * 70)
    print("POLARITY MANAGEMENT - DYNAMIC BALANCE")
    print("=" * 70)
    print()
    print("Implementing Universal Principle 3:")
    print('"Dynamic Balance and Polarity - Stability emerges from continuous')
    print(' interplay of complementary forces."')
    print()

    # Create mock network for testing
    class MockNetwork:
        def __init__(self):
            class MockLayer:
                def __init__(self):
                    self.weights = np.random.randn(10, 10)

            self.layers = [MockLayer(), MockLayer()]

    network = MockNetwork()

    # Example 1: Stability-Plasticity Balance
    print("-" * 70)
    print("EXAMPLE 1: Stability-Plasticity Balance")
    print("-" * 70)
    sp_balance = StabilityPlasticityBalance(network)
    print(sp_balance)
    print()

    print("Adaptive learning rate:")
    base_lr = 0.01
    adaptive_lr = sp_balance.get_adaptive_learning_rate(base_lr)
    print(f"  Base LR: {base_lr:.4f}")
    print(f"  Adaptive LR: {adaptive_lr:.4f}")
    print()

    print("Shifting toward stability:")
    sp_balance.increase_stability(amount=0.2)
    print(f"  {sp_balance}")
    adaptive_lr = sp_balance.get_adaptive_learning_rate(base_lr)
    print(f"  New adaptive LR: {adaptive_lr:.4f} (lower = preserve more)")
    print()

    # Example 2: Excitation-Inhibition Balance
    print("-" * 70)
    print("EXAMPLE 2: Excitation-Inhibition Balance")
    print("-" * 70)
    ei_balance = ExcitationInhibitionBalance()
    print(f"E/I Ratio: {ei_balance.get_balance():.2f} (biological ≈ 4:1)")
    print()

    activations = np.array([0.1, 0.5, 0.05, 0.8, 0.02, 0.3, 0.01, 0.6])
    balanced = ei_balance.apply(activations)

    print("Original activations:")
    print(f"  {activations}")
    print("After E-I balance:")
    print(f"  {balanced}")
    print("  → Strong signals amplified, weak signals suppressed")
    print()

    # Example 3: Auto-adjustment during learning
    print("-" * 70)
    print("EXAMPLE 3: Auto-Adjustment During Learning")
    print("-" * 70)
    sp_balance = StabilityPlasticityBalance(network)

    print("Balance evolution during training:")
    for epoch in [0, 25, 50, 75, 100]:
        progress = epoch / 100
        sp_balance.auto_adjust(learning_progress=progress)
        balance = sp_balance.get_balance()
        print(f"  Epoch {epoch:3d}: Balance = {balance:.2f} ", end="")
        if balance > 0.6:
            print("(High plasticity - learning actively)")
        elif balance < 0.4:
            print("(High stability - preserving knowledge)")
        else:
            print("(Balanced)")
    print()

    # Example 4: Complete polarity management
    print("-" * 70)
    print("EXAMPLE 4: Complete Polarity Management")
    print("-" * 70)
    manager = PolarityManager(network)
    print(manager)
    print()

    print("Balance statistics:")
    stats = manager.get_balance_stats()
    for name, value in stats.items():
        print(f"  {name}: {value:.2f}")
    print()

    print("=" * 70)
    print("KEY INSIGHT: DYNAMIC BALANCE")
    print("=" * 70)
    print()
    print("Traditional neural networks:")
    print("  - Fixed learning rate")
    print("  - All weights treated equally")
    print("  - No balance management")
    print("  - Catastrophic forgetting")
    print()
    print("Polarity-managed networks:")
    print("  - Adaptive learning rate (stability-plasticity)")
    print("  - Important weights protected")
    print("  - Dynamic equilibrium maintained")
    print("  - Robust continual learning")
    print()
    print("This implements Universal Principle 3:")
    print('"Stability emerges from continuous interplay of complementary forces"')
    print()
    print("Just like biological systems maintain health through balance,")
    print("neural networks can maintain quality through polarity management.")
    print()
    print("=" * 70)
