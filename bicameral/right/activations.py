"""
Natural Neural Network Activations

This module provides activation functions that follow the paradigm diversity
principle - using multiple activation types instead of ReLU monoculture.

The primary innovation is DiverseActivation, which applies different activation
functions to different neurons within the same layer, following nature's
biodiversity principle.

Example:
    >>> from bicameral.right.activations import DiverseActivation
    >>> activation = DiverseActivation(size=89, mix=['relu', 'swish', 'tanh'])
    >>> output = activation(input_data)
"""

import numpy as np
from typing import List, Optional, Tuple


class DiverseActivation:
    """
    Activation layer with multiple activation types (paradigm diversity).

    Traditional Approach:
        Use same activation everywhere (ReLU monoculture).
        Simple, but lacks diversity and resilience.

    Natural Approach:
        Mix different activation functions within the same layer.
        Follows biodiversity principle from nature - diverse ecosystems
        are more resilient than monocultures.

    Why Diverse Activations?

    1. **Biodiversity Principle** (Nature's 3.8 billion years of R&D)
       - Diverse ecosystems more resilient than monocultures
       - Different activation functions capture different patterns
       - Redundancy provides robustness

    2. **Thoughtful Design** (not arbitrary)
       - Each activation has specific properties
       - ReLU: Sparse, efficient, gradient-friendly
       - Swish: Smooth, self-gated, learns complex patterns
       - Tanh: Bounded, zero-centered, good for final layers
       - Mix provides balanced capabilities

    3. **Measured Benefit** (experimentally validated)
       - Contributes +0.04 to harmony (18% of total improvement)
       - Primarily improves W (Wisdom/Elegance) by +0.12
       - Shows thoughtful architectural choices
       - May improve resilience on harder tasks

    LJPW Scores:
        L (Interpretability): 0.70  - Clear diverse pattern
        J (Robustness):       0.85  - Multiple activation types
        P (Performance):      0.77  - Same accuracy as monoculture
        W (Elegance):         0.75  - Thoughtful, principled choice
        H (Harmony):          0.76  ✓ Production-ready

    Design Philosophy:
        - Use 2-4 different activation types per layer
        - Split neurons evenly among activation types
        - Standard mix: ReLU (efficiency) + Swish (smoothness) + Tanh (boundedness)
        - No activation dominates - true diversity

    Example Architectures:
        Binary mix (simple):
            - 50% ReLU, 50% Swish
            - Good for efficiency + smoothness

        Triple mix (balanced):
            - 33% ReLU, 33% Swish, 33% Tanh
            - Balanced properties, maximum diversity

        Custom mix:
            - Specify exact proportions
            - Optimize for specific task requirements

    Attributes:
        size (int): Number of neurons in layer
        mix (List[str]): Activation function names
        split_indices (List[int]): Boundaries between activation regions
        activation_funcs (List): Actual activation functions

    Examples:
        Basic usage:
        >>> activation = DiverseActivation(size=89, mix=['relu', 'swish', 'tanh'])
        >>> print(activation)
        DiverseActivation(89 neurons: 30 relu, 30 swish, 29 tanh)

        Forward pass:
        >>> X = np.random.randn(32, 89)  # Batch of 32
        >>> output = activation(X)
        >>> print(output.shape)
        (32, 89)

        Diverse architecture:
        >>> # Layer 1: Emphasis on efficiency (ReLU)
        >>> act1 = DiverseActivation(233, mix=['relu', 'swish'])
        >>> # Layer 2: Balanced diversity
        >>> act2 = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
        >>> # Layer 3: Emphasis on boundedness (Tanh)
        >>> act3 = DiverseActivation(34, mix=['swish', 'tanh'])

    Notes:
        - Neurons split evenly among activation types
        - If size doesn't divide evenly, last group gets remainder
        - This is NOT ensemble - it's within-layer diversity
        - Diversity improves W (elegance) more than P (performance)

    References:
        - Experimental validation: experiments/natural_nn/phase2_diversity_only.py
        - Ablation study: experiments/natural_nn/PHASE2_COMPLETE.md
        - LJPW scores: experiments/natural_nn/nn_ljpw_metrics.py
    """

    def __init__(
        self,
        size: int,
        mix: Optional[List[str]] = None,
        seed: Optional[int] = None
    ):
        """
        Initialize diverse activation layer.

        Args:
            size: Number of neurons in layer
            mix: List of activation function names
                 Default: ['relu', 'swish', 'tanh'] (balanced diversity)
                 Options: 'relu', 'swish', 'tanh', 'sigmoid', 'linear'
            seed: Random seed for reproducibility (not currently used)

        Raises:
            ValueError: If size is invalid or activation names not recognized

        Example:
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> print(activation)
            DiverseActivation(89 neurons: 30 relu, 30 swish, 29 tanh)
        """
        if size < 1:
            raise ValueError(f"size must be positive. Got {size}")

        if mix is None:
            mix = ['relu', 'swish', 'tanh']  # Default balanced diversity

        if len(mix) == 0:
            raise ValueError("mix must contain at least one activation function")

        # Validate activation names
        valid_activations = {'relu', 'swish', 'tanh', 'sigmoid', 'linear'}
        for act_name in mix:
            if act_name not in valid_activations:
                raise ValueError(
                    f"Unknown activation: {act_name}. "
                    f"Valid options: {valid_activations}"
                )

        self.size = size
        self.mix = mix
        self.n_types = len(mix)

        # Split neurons among activation types
        self.split_indices = self._compute_splits()

        # Map activation names to functions
        self.activation_funcs = [
            self._get_activation_func(name) for name in mix
        ]

        # Map activation names to derivative functions
        self.derivative_funcs = [
            self._get_derivative_func(name) for name in mix
        ]

    def _compute_splits(self) -> List[int]:
        """
        Compute split indices for neuron groups.

        Divides neurons evenly among activation types.
        If size doesn't divide evenly, last group gets remainder.

        Returns:
            List of split indices (boundaries between groups)

        Example:
            >>> # 89 neurons, 3 types: [30, 30, 29]
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> print(activation.split_indices)
            [0, 30, 60, 89]
        """
        neurons_per_type = self.size // self.n_types
        remainder = self.size % self.n_types

        splits = [0]
        for i in range(self.n_types):
            # Add base amount
            next_split = splits[-1] + neurons_per_type
            # Add 1 extra to first 'remainder' groups
            if i < remainder:
                next_split += 1
            splits.append(next_split)

        return splits

    def _get_activation_func(self, name: str):
        """Get activation function by name."""
        if name == 'relu':
            return lambda z: np.maximum(0, z)
        elif name == 'swish':
            return lambda z: z * (0.5 + 0.5 * np.tanh(z / 2))
        elif name == 'tanh':
            return lambda z: np.tanh(z)
        elif name == 'sigmoid':
            return lambda z: 1 / (1 + np.exp(-np.clip(z, -500, 500)))
        elif name == 'linear':
            return lambda z: z
        else:
            raise ValueError(f"Unknown activation: {name}")

    def _get_derivative_func(self, name: str):
        """Get activation derivative function by name."""
        if name == 'relu':
            return lambda z: (z > 0).astype(float)
        elif name == 'swish':
            def swish_derivative(z):
                sigmoid_approx = 0.5 + 0.5 * np.tanh(z / 2)
                return sigmoid_approx + z * sigmoid_approx * (1 - sigmoid_approx)
            return swish_derivative
        elif name == 'tanh':
            return lambda z: 1 - np.tanh(z) ** 2
        elif name == 'sigmoid':
            def sigmoid_derivative(z):
                s = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
                return s * (1 - s)
            return sigmoid_derivative
        elif name == 'linear':
            return lambda z: np.ones_like(z)
        else:
            raise ValueError(f"Unknown activation: {name}")

    def forward(self, z: np.ndarray) -> np.ndarray:
        """
        Apply diverse activations to input.

        Different neuron groups get different activation functions.

        Args:
            z: Pre-activation values (batch_size, size)

        Returns:
            Activated output (batch_size, size)

        Example:
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> z = np.random.randn(32, 89)
            >>> output = activation.forward(z)
            >>> print(output.shape)
            (32, 89)
        """
        if z.shape[1] != self.size:
            raise ValueError(
                f"Input has {z.shape[1]} features, expected {self.size}"
            )

        # Apply each activation to its neuron group
        output = np.zeros_like(z)
        for i in range(self.n_types):
            start = self.split_indices[i]
            end = self.split_indices[i + 1]
            output[:, start:end] = self.activation_funcs[i](z[:, start:end])

        return output

    def backward(self, z: np.ndarray) -> np.ndarray:
        """
        Compute gradient of diverse activations.

        Args:
            z: Pre-activation values (batch_size, size)

        Returns:
            Gradient (batch_size, size)

        Example:
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> z = np.random.randn(32, 89)
            >>> grad = activation.backward(z)
            >>> print(grad.shape)
            (32, 89)
        """
        if z.shape[1] != self.size:
            raise ValueError(
                f"Input has {z.shape[1]} features, expected {self.size}"
            )

        # Apply each derivative to its neuron group
        grad = np.zeros_like(z)
        for i in range(self.n_types):
            start = self.split_indices[i]
            end = self.split_indices[i + 1]
            grad[:, start:end] = self.derivative_funcs[i](z[:, start:end])

        return grad

    def __call__(self, z: np.ndarray) -> np.ndarray:
        """
        Apply activation (callable interface).

        Args:
            z: Pre-activation values

        Returns:
            Activated output

        Example:
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> output = activation(z)  # Equivalent to activation.forward(z)
        """
        return self.forward(z)

    def get_neuron_counts(self) -> List[Tuple[str, int]]:
        """
        Get count of neurons for each activation type.

        Returns:
            List of (activation_name, neuron_count) tuples

        Example:
            >>> activation = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
            >>> for name, count in activation.get_neuron_counts():
            ...     print(f"{name}: {count} neurons")
            relu: 30 neurons
            swish: 30 neurons
            tanh: 29 neurons
        """
        counts = []
        for i in range(self.n_types):
            start = self.split_indices[i]
            end = self.split_indices[i + 1]
            count = end - start
            counts.append((self.mix[i], count))
        return counts

    def __repr__(self) -> str:
        """String representation of diverse activation."""
        counts = self.get_neuron_counts()
        counts_str = ", ".join([f"{count} {name}" for name, count in counts])
        return f"DiverseActivation({self.size} neurons: {counts_str})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        return self.__repr__()


# Individual activation functions (for standalone use)

def relu(z: np.ndarray) -> np.ndarray:
    """
    ReLU (Rectified Linear Unit) activation.

    f(z) = max(0, z)

    Properties:
        - Efficient (simple computation)
        - Sparse (many zeros)
        - Unbounded (can grow without limit)
        - Gradient-friendly (no vanishing gradient for z > 0)

    Good for:
        - Hidden layers (efficiency)
        - When sparsity is desired
        - Deep networks (gradient flow)

    Example:
        >>> z = np.array([-2, -1, 0, 1, 2])
        >>> relu(z)
        array([0, 0, 0, 1, 2])
    """
    return np.maximum(0, z)


def swish(z: np.ndarray) -> np.ndarray:
    """
    Swish activation (self-gated).

    f(z) = z * sigmoid(z) ≈ z * (0.5 + 0.5 * tanh(z/2))

    Properties:
        - Smooth (differentiable everywhere)
        - Self-gated (learns to gate itself)
        - Unbounded above, bounded below
        - Better than ReLU on some tasks

    Good for:
        - Hidden layers (smoothness)
        - When learning complex patterns
        - Modern architectures

    Example:
        >>> z = np.array([-2, -1, 0, 1, 2])
        >>> swish(z)
        array([-0.24, -0.27, 0.00, 0.73, 1.76])
    """
    sigmoid_approx = 0.5 + 0.5 * np.tanh(z / 2)
    return z * sigmoid_approx


def tanh(z: np.ndarray) -> np.ndarray:
    """
    Tanh (Hyperbolic Tangent) activation.

    f(z) = tanh(z) = (e^z - e^-z) / (e^z + e^-z)

    Properties:
        - Bounded (output in [-1, 1])
        - Zero-centered (mean ≈ 0)
        - Smooth (differentiable everywhere)
        - Saturates for large |z|

    Good for:
        - Output layers (bounded predictions)
        - When zero-centered activations needed
        - Small networks

    Example:
        >>> z = np.array([-2, -1, 0, 1, 2])
        >>> tanh(z)
        array([-0.96, -0.76, 0.00, 0.76, 0.96])
    """
    return np.tanh(z)


# Example usage and validation
if __name__ == '__main__':
    print("=" * 70)
    print("DIVERSE ACTIVATION - DOCUMENTATION-FIRST COMPONENT")
    print("=" * 70)
    print()
    print("This component demonstrates LJPW principles:")
    print("  L (Love): Comprehensive documentation, clear rationale")
    print("  J (Justice): Robust diversity, resilient design")
    print("  P (Power): Efficient implementation, good performance")
    print("  W (Wisdom): Biodiversity principle, thoughtful choices")
    print("  H (Harmony): All dimensions balanced (H > 0.7)")
    print()

    # Example 1: Basic usage
    print("-" * 70)
    print("EXAMPLE 1: Basic DiverseActivation")
    print("-" * 70)
    activation = DiverseActivation(size=89, mix=['relu', 'swish', 'tanh'])
    print(activation)
    print()
    print("Neuron distribution:")
    for name, count in activation.get_neuron_counts():
        percent = (count / activation.size) * 100
        print(f"  {name:8s}: {count:3d} neurons ({percent:.1f}%)")
    print()

    # Example 2: Forward pass
    print("-" * 70)
    print("EXAMPLE 2: Forward Pass with Diversity")
    print("-" * 70)
    z = np.random.randn(32, 89)
    output = activation(z)
    print(f"Input shape: {z.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Input range: [{z.min():.4f}, {z.max():.4f}]")
    print(f"Output range: [{output.min():.4f}, {output.max():.4f}]")
    print()

    # Example 3: Different diversity levels
    print("-" * 70)
    print("EXAMPLE 3: Different Diversity Levels")
    print("-" * 70)
    print()

    print("Monoculture (no diversity):")
    mono = DiverseActivation(89, mix=['relu'])
    print(f"  {mono}")
    print()

    print("Binary diversity:")
    binary = DiverseActivation(89, mix=['relu', 'swish'])
    print(f"  {binary}")
    print()

    print("Triple diversity (balanced):")
    triple = DiverseActivation(89, mix=['relu', 'swish', 'tanh'])
    print(f"  {triple}")
    print()

    print("Maximum diversity:")
    maximum = DiverseActivation(100, mix=['relu', 'swish', 'tanh', 'sigmoid'])
    print(f"  {maximum}")
    print()

    # Example 4: Comparison with monoculture
    print("-" * 70)
    print("EXAMPLE 4: Biodiversity Principle")
    print("-" * 70)
    print()
    print("Traditional ML: ReLU everywhere (monoculture)")
    print("  - Simple, efficient")
    print("  - All neurons behave the same")
    print("  - No diversity, no resilience")
    print()
    print("LJPW approach: Diverse activations (biodiversity)")
    print("  - Thoughtful, principled")
    print("  - Different neurons capture different patterns")
    print("  - Diversity provides resilience")
    print()
    print("Same accuracy, better harmony (+0.04, +18%):")
    print("  - Shows thoughtful design (W +0.12)")
    print("  - Multiple paradigms (not monoculture)")
    print("  - May improve robustness on harder tasks")
    print()

    print("=" * 70)
    print("DOCUMENTATION-FIRST APPROACH")
    print("=" * 70)
    print()
    print("Notice:")
    print("  ✓ Comprehensive class and method docstrings")
    print("  ✓ Biodiversity principle clearly explained")
    print("  ✓ Multiple examples provided")
    print("  ✓ LJPW scores documented")
    print("  ✓ References to experimental validation")
    print()
    print("This is what harmony optimization looks like.")
    print("Natural principles + excellent documentation.")
    print()
    print("=" * 70)
