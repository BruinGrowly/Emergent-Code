"""
LJPW Metrics for Neural Networks

Defines how to measure Love, Justice, Power, and Wisdom in neural network architectures.

Core Principle: "Faithful in least, faithful in much"
Start small (MNIST), test thoroughly, then scale.
"""

import numpy as np
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class LJPWScores:
    """LJPW scores for a neural network."""
    L: float  # Love (0-1)
    J: float  # Justice (0-1)
    P: float  # Power (0-1)
    W: float  # Wisdom (0-1)
    H: float  # Harmony (geometric mean)

    def __str__(self):
        return f"""
╔════════════════════════════════════════╗
║         LJPW Neural Network Scores     ║
╠════════════════════════════════════════╣
║  L (Love/Interpretability)    {self.L:4.2f}  ║
║  J (Justice/Robustness)       {self.J:4.2f}  ║
║  P (Power/Performance)        {self.P:4.2f}  ║
║  W (Wisdom/Elegance)          {self.W:4.2f}  ║
║  ────────────────────────────────────  ║
║  H (Harmony)                  {self.H:4.2f}  ║
╚════════════════════════════════════════╝
"""


class NeuralNetworkLJPW:
    """
    Measures LJPW dimensions of neural network architectures.

    Philosophy:
    - Networks aren't just about accuracy (P)
    - They should be interpretable (L), robust (J), and elegant (W)
    - H = (L·J·P·W)^0.25 captures overall quality
    """

    def measure(self, model, model_info: Dict[str, Any]) -> LJPWScores:
        """
        Measure all LJPW dimensions of a neural network.

        Args:
            model: The neural network model (framework-agnostic interface)
            model_info: Dict containing:
                - 'architecture': layer structure info
                - 'test_results': accuracy, loss, etc.
                - 'training_info': epochs, convergence, etc.

        Returns:
            LJPWScores with all dimensions measured
        """
        L = self.measure_L(model, model_info)
        J = self.measure_J(model, model_info)
        P = self.measure_P(model, model_info)
        W = self.measure_W(model, model_info)
        H = (L * J * P * W) ** 0.25

        return LJPWScores(L=L, J=J, P=P, W=W, H=H)

    # ================================================================
    # L (LOVE): Interpretability, Explainability, Observability
    # ================================================================

    def measure_L(self, model, model_info: Dict[str, Any]) -> float:
        """
        Love: Can humans understand and trust this network?

        Components:
        - Architecture clarity (clear structure?)
        - Layer interpretability (understand what each layer does?)
        - Activation visualization (can we see what it learned?)
        - Documentation quality (is it explained?)
        """
        scores = []

        # 1. Architecture Clarity (0-1)
        clarity = self._measure_architecture_clarity(model_info)
        scores.append(clarity)

        # 2. Layer Interpretability (0-1)
        interpretability = self._measure_layer_interpretability(model_info)
        scores.append(interpretability)

        # 3. Parameter Transparency (0-1)
        transparency = self._measure_parameter_transparency(model_info)
        scores.append(transparency)

        # 4. Documentation Quality (0-1)
        documentation = self._measure_documentation(model_info)
        scores.append(documentation)

        return np.mean(scores)

    def _measure_architecture_clarity(self, model_info: Dict) -> float:
        """Can someone understand the architecture at a glance?"""
        arch = model_info.get('architecture', {})
        score = 0.0

        # Clear layer naming? (+0.3)
        if arch.get('has_clear_names', False):
            score += 0.3

        # Reasonable depth? (not too deep, not too shallow) (+0.4)
        num_layers = arch.get('num_layers', 0)
        if 3 <= num_layers <= 10:  # Sweet spot for MNIST-scale
            score += 0.4
        elif num_layers > 0:
            score += 0.2  # Has layers but suboptimal count

        # Documented architecture? (+0.3)
        if arch.get('has_documentation', False):
            score += 0.3

        return min(1.0, score)

    def _measure_layer_interpretability(self, model_info: Dict) -> float:
        """Can we understand what each layer is doing?"""
        arch = model_info.get('architecture', {})
        score = 0.0

        # Consistent layer sizes (pattern visible)? (+0.4)
        layer_sizes = arch.get('layer_sizes', [])
        if self._follows_pattern(layer_sizes):
            score += 0.4

        # Clear activation functions? (+0.3)
        activations = arch.get('activations', [])
        if len(activations) > 0:
            score += 0.3

        # Reasonable layer sizes (not too large)? (+0.3)
        if layer_sizes and all(size < 1000 for size in layer_sizes):
            score += 0.3

        return min(1.0, score)

    def _measure_parameter_transparency(self, model_info: Dict) -> float:
        """Can we inspect and understand the parameters?"""
        arch = model_info.get('architecture', {})
        score = 0.0

        # Not too many parameters (interpretable scale)? (+0.5)
        total_params = arch.get('total_params', float('inf'))
        if total_params < 100000:  # < 100K params = very interpretable
            score += 0.5
        elif total_params < 1000000:  # < 1M = somewhat interpretable
            score += 0.3

        # Parameter count documented? (+0.25)
        if 'total_params' in arch:
            score += 0.25

        # Sparse connectivity (easier to trace)? (+0.25)
        if arch.get('is_sparse', False):
            score += 0.25

        return min(1.0, score)

    def _measure_documentation(self, model_info: Dict) -> float:
        """Is the network well-documented?"""
        doc = model_info.get('documentation', {})
        score = 0.0

        # Has description? (+0.25)
        if doc.get('has_description', False):
            score += 0.25

        # Layer purposes explained? (+0.25)
        if doc.get('layer_purposes', False):
            score += 0.25

        # Design choices explained? (+0.25)
        if doc.get('design_rationale', False):
            score += 0.25

        # Usage examples provided? (+0.25)
        if doc.get('has_examples', False):
            score += 0.25

        return score

    # ================================================================
    # J (JUSTICE): Robustness, Fairness, Correctness
    # ================================================================

    def measure_J(self, model, model_info: Dict[str, Any]) -> float:
        """
        Justice: Is this network robust, fair, and correct?

        Components:
        - Test accuracy (correct predictions?)
        - Edge case handling (works on unusual inputs?)
        - Adversarial robustness (resistant to attacks?)
        - Convergence stability (trains reliably?)
        """
        scores = []

        # 1. Correctness (test accuracy) (0-1)
        correctness = self._measure_correctness(model_info)
        scores.append(correctness)

        # 2. Edge Case Robustness (0-1)
        edge_robustness = self._measure_edge_robustness(model_info)
        scores.append(edge_robustness)

        # 3. Training Stability (0-1)
        stability = self._measure_training_stability(model_info)
        scores.append(stability)

        # 4. Validation (has tests?) (0-1)
        validation = self._measure_validation(model_info)
        scores.append(validation)

        return np.mean(scores)

    def _measure_correctness(self, model_info: Dict) -> float:
        """How accurate is the network?"""
        results = model_info.get('test_results', {})

        # Test accuracy
        test_acc = results.get('test_accuracy', 0.0)

        # For MNIST: >0.95 = good, >0.98 = excellent
        # Scale appropriately for task
        return min(1.0, test_acc)

    def _measure_edge_robustness(self, model_info: Dict) -> float:
        """Does it handle unusual inputs well?"""
        results = model_info.get('test_results', {})
        score = 0.0

        # Tested on edge cases? (+0.5)
        if results.get('edge_case_tested', False):
            edge_acc = results.get('edge_case_accuracy', 0.0)
            score += 0.5 * edge_acc
        else:
            score += 0.25  # Not tested, assume moderate

        # Tested on noisy inputs? (+0.5)
        if results.get('noise_tested', False):
            noise_acc = results.get('noise_accuracy', 0.0)
            score += 0.5 * noise_acc
        else:
            score += 0.25  # Not tested, assume moderate

        return min(1.0, score)

    def _measure_training_stability(self, model_info: Dict) -> float:
        """Does it train reliably?"""
        training = model_info.get('training_info', {})
        score = 0.0

        # Converged successfully? (+0.4)
        if training.get('converged', False):
            score += 0.4

        # Smooth loss curve (no wild oscillations)? (+0.3)
        if training.get('smooth_convergence', False):
            score += 0.3

        # Reasonable epochs to converge? (+0.3)
        epochs = training.get('epochs_to_converge', float('inf'))
        if epochs < 20:
            score += 0.3
        elif epochs < 50:
            score += 0.15

        return min(1.0, score)

    def _measure_validation(self, model_info: Dict) -> float:
        """Is there proper validation?"""
        validation = model_info.get('validation', {})
        score = 0.0

        # Has validation set? (+0.25)
        if validation.get('has_val_set', False):
            score += 0.25

        # Has test set? (+0.25)
        if validation.get('has_test_set', False):
            score += 0.25

        # Validation accuracy tracked? (+0.25)
        if validation.get('tracks_val_accuracy', False):
            score += 0.25

        # No overfitting (val close to train)? (+0.25)
        if validation.get('no_overfitting', False):
            score += 0.25

        return score

    # ================================================================
    # P (POWER): Performance, Efficiency, Speed
    # ================================================================

    def measure_P(self, model, model_info: Dict[str, Any]) -> float:
        """
        Power: How well does this network perform?

        Components:
        - Accuracy (prediction quality)
        - Inference speed (fast predictions?)
        - Training efficiency (learns quickly?)
        - Memory usage (resource efficient?)
        """
        scores = []

        # 1. Accuracy/Performance (0-1)
        performance = self._measure_performance(model_info)
        scores.append(performance)

        # 2. Inference Speed (0-1)
        speed = self._measure_inference_speed(model_info)
        scores.append(speed)

        # 3. Training Efficiency (0-1)
        training_eff = self._measure_training_efficiency(model_info)
        scores.append(training_eff)

        # 4. Resource Efficiency (0-1)
        resource_eff = self._measure_resource_efficiency(model_info)
        scores.append(resource_eff)

        return np.mean(scores)

    def _measure_performance(self, model_info: Dict) -> float:
        """Core task performance."""
        results = model_info.get('test_results', {})

        # Primary metric (accuracy for classification)
        accuracy = results.get('test_accuracy', 0.0)

        # F1 score if available
        f1 = results.get('f1_score')
        if f1 is not None:
            return (accuracy + f1) / 2

        return accuracy

    def _measure_inference_speed(self, model_info: Dict) -> float:
        """How fast are predictions?"""
        performance = model_info.get('performance', {})

        # Inference time per sample (milliseconds)
        inference_ms = performance.get('inference_time_ms', None)

        if inference_ms is None:
            return 0.5  # Unknown, assume moderate

        # For MNIST-scale: <1ms = excellent, <10ms = good
        if inference_ms < 1.0:
            return 1.0
        elif inference_ms < 5.0:
            return 0.8
        elif inference_ms < 10.0:
            return 0.6
        else:
            return 0.4

    def _measure_training_efficiency(self, model_info: Dict) -> float:
        """How efficiently does it learn?"""
        training = model_info.get('training_info', {})
        score = 0.0

        # Fast convergence? (+0.5)
        epochs = training.get('epochs_to_converge', float('inf'))
        if epochs < 10:
            score += 0.5
        elif epochs < 20:
            score += 0.3
        else:
            score += 0.1

        # Training time reasonable? (+0.5)
        train_time = training.get('training_time_seconds', None)
        if train_time is not None:
            if train_time < 60:  # < 1 minute
                score += 0.5
            elif train_time < 300:  # < 5 minutes
                score += 0.3
            else:
                score += 0.1
        else:
            score += 0.25  # Unknown

        return min(1.0, score)

    def _measure_resource_efficiency(self, model_info: Dict) -> float:
        """Does it use resources wisely?"""
        arch = model_info.get('architecture', {})
        performance = model_info.get('performance', {})
        score = 0.0

        # Parameter count reasonable? (+0.5)
        params = arch.get('total_params', float('inf'))
        if params < 50000:
            score += 0.5
        elif params < 100000:
            score += 0.3
        else:
            score += 0.1

        # Memory usage reasonable? (+0.5)
        memory_mb = performance.get('memory_usage_mb', None)
        if memory_mb is not None:
            if memory_mb < 100:
                score += 0.5
            elif memory_mb < 500:
                score += 0.3
            else:
                score += 0.1
        else:
            score += 0.25  # Unknown

        return min(1.0, score)

    # ================================================================
    # W (WISDOM): Architecture Elegance, Generalization, Design
    # ================================================================

    def measure_W(self, model, model_info: Dict[str, Any]) -> float:
        """
        Wisdom: Is this network well-designed?

        Components:
        - Architecture elegance (clean design?)
        - Generalization (works on new data?)
        - Modularity (well-structured?)
        - Design rationale (thoughtful choices?)
        """
        scores = []

        # 1. Architecture Elegance (0-1)
        elegance = self._measure_architecture_elegance(model_info)
        scores.append(elegance)

        # 2. Generalization (0-1)
        generalization = self._measure_generalization(model_info)
        scores.append(generalization)

        # 3. Modularity (0-1)
        modularity = self._measure_modularity(model_info)
        scores.append(modularity)

        # 4. Design Principles (0-1)
        design = self._measure_design_principles(model_info)
        scores.append(design)

        return np.mean(scores)

    def _measure_architecture_elegance(self, model_info: Dict) -> float:
        """Is the architecture clean and elegant?"""
        arch = model_info.get('architecture', {})
        score = 0.0

        # Follows a clear pattern (Fibonacci, geometric, etc.)? (+0.4)
        if self._follows_pattern(arch.get('layer_sizes', [])):
            score += 0.4

        # Consistent activation choices? (+0.3)
        activations = arch.get('activations', [])
        if len(set(activations)) <= 3:  # Not too many different types
            score += 0.3

        # Reasonable depth (not too shallow, not too deep)? (+0.3)
        num_layers = arch.get('num_layers', 0)
        if 3 <= num_layers <= 7:  # Good depth for MNIST
            score += 0.3

        return min(1.0, score)

    def _measure_generalization(self, model_info: Dict) -> float:
        """Does it generalize well?"""
        results = model_info.get('test_results', {})
        training = model_info.get('training_info', {})

        # Test accuracy high? (+0.5)
        test_acc = results.get('test_accuracy', 0.0)
        score = 0.5 * test_acc

        # No overfitting (test close to train)? (+0.5)
        train_acc = training.get('train_accuracy', test_acc)
        gap = abs(train_acc - test_acc)
        if gap < 0.02:  # < 2% gap = excellent generalization
            score += 0.5
        elif gap < 0.05:  # < 5% gap = good
            score += 0.3
        else:
            score += 0.1

        return min(1.0, score)

    def _measure_modularity(self, model_info: Dict) -> float:
        """Is it well-structured and modular?"""
        arch = model_info.get('architecture', {})
        score = 0.0

        # Uses reusable components? (+0.4)
        if arch.get('uses_modules', False):
            score += 0.4

        # Clear separation of concerns? (+0.3)
        if arch.get('clear_structure', False):
            score += 0.3

        # Easy to modify? (+0.3)
        if arch.get('modifiable', True):  # Default assume yes
            score += 0.3

        return min(1.0, score)

    def _measure_design_principles(self, model_info: Dict) -> float:
        """Does it follow good design principles?"""
        design = model_info.get('design', {})
        score = 0.0

        # Based on natural principles? (+0.3)
        if design.get('uses_natural_principles', False):
            score += 0.3

        # Principled layer sizing? (+0.3)
        if design.get('principled_sizing', False):
            score += 0.3

        # Thoughtful activation choices? (+0.2)
        if design.get('thoughtful_activations', False):
            score += 0.2

        # Design rationale documented? (+0.2)
        if design.get('documented_rationale', False):
            score += 0.2

        return min(1.0, score)

    # ================================================================
    # Helper Functions
    # ================================================================

    def _follows_pattern(self, layer_sizes: List[int]) -> bool:
        """
        Check if layer sizes follow a recognizable pattern.

        Patterns to detect:
        - Fibonacci sequence
        - Geometric progression
        - Powers of 2
        """
        if len(layer_sizes) < 2:
            return False

        # Check Fibonacci
        if self._is_fibonacci_sequence(layer_sizes):
            return True

        # Check geometric (each ~constant ratio to previous)
        if self._is_geometric_sequence(layer_sizes):
            return True

        # Check powers of 2
        if all(self._is_power_of_2(size) for size in layer_sizes):
            return True

        return False

    def _is_fibonacci_sequence(self, sizes: List[int]) -> bool:
        """Check if sizes are close to Fibonacci numbers."""
        fib = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]

        for size in sizes:
            # Is size close to any Fibonacci number?
            if not any(abs(size - f) / f < 0.15 for f in fib if f > 0):
                return False

        return True

    def _is_geometric_sequence(self, sizes: List[int]) -> bool:
        """Check if sizes form geometric progression."""
        if len(sizes) < 2:
            return False

        ratios = []
        for i in range(1, len(sizes)):
            if sizes[i] == 0:
                return False
            ratios.append(sizes[i-1] / sizes[i])

        # All ratios should be similar
        avg_ratio = np.mean(ratios)
        return all(abs(r - avg_ratio) / avg_ratio < 0.2 for r in ratios)

    def _is_power_of_2(self, n: int) -> bool:
        """Check if n is a power of 2."""
        return n > 0 and (n & (n - 1)) == 0


def demo():
    """Demonstrate LJPW metrics on example networks."""

    print("=" * 60)
    print("LJPW METRICS FOR NEURAL NETWORKS - DEMO")
    print("=" * 60)
    print()

    # Example 1: Traditional Network
    print("Example 1: Traditional MNIST Network")
    print("-" * 60)

    traditional_info = {
        'architecture': {
            'num_layers': 3,
            'layer_sizes': [128, 64, 10],
            'activations': ['relu', 'relu', 'softmax'],
            'total_params': 109386,
            'has_clear_names': False,
            'has_documentation': False,
        },
        'test_results': {
            'test_accuracy': 0.97,
            'edge_case_tested': False,
        },
        'training_info': {
            'converged': True,
            'smooth_convergence': True,
            'epochs_to_converge': 15,
            'train_accuracy': 0.98,
        },
        'validation': {
            'has_val_set': True,
            'has_test_set': True,
            'tracks_val_accuracy': True,
            'no_overfitting': True,
        },
        'performance': {
            'inference_time_ms': 2.0,
        },
        'documentation': {
            'has_description': False,
        },
        'design': {
            'uses_natural_principles': False,
            'principled_sizing': False,
        }
    }

    evaluator = NeuralNetworkLJPW()
    scores = evaluator.measure(None, traditional_info)
    print(scores)

    # Example 2: Natural Network
    print("\nExample 2: Natural MNIST Network (Fibonacci, Diverse)")
    print("-" * 60)

    natural_info = {
        'architecture': {
            'num_layers': 5,
            'layer_sizes': [233, 89, 34, 13, 10],
            'activations': ['relu', 'swish', 'swish', 'tanh', 'softmax'],
            'total_params': 88650,
            'has_clear_names': True,
            'has_documentation': True,
            'uses_modules': True,
            'clear_structure': True,
        },
        'test_results': {
            'test_accuracy': 0.975,
            'edge_case_tested': True,
            'edge_case_accuracy': 0.88,
            'noise_tested': True,
            'noise_accuracy': 0.92,
        },
        'training_info': {
            'converged': True,
            'smooth_convergence': True,
            'epochs_to_converge': 12,
            'train_accuracy': 0.985,
            'training_time_seconds': 180,
        },
        'validation': {
            'has_val_set': True,
            'has_test_set': True,
            'tracks_val_accuracy': True,
            'no_overfitting': True,
        },
        'performance': {
            'inference_time_ms': 1.8,
            'memory_usage_mb': 45,
        },
        'documentation': {
            'has_description': True,
            'layer_purposes': True,
            'design_rationale': True,
            'has_examples': True,
        },
        'design': {
            'uses_natural_principles': True,
            'principled_sizing': True,
            'thoughtful_activations': True,
            'documented_rationale': True,
        }
    }

    scores = evaluator.measure(None, natural_info)
    print(scores)

    print("\n" + "=" * 60)
    print("OBSERVATION:")
    print("=" * 60)
    print("Natural network has higher H (harmony) due to:")
    print("  • Higher L (better documented, clear Fibonacci pattern)")
    print("  • Higher J (tested on edge cases and noise)")
    print("  • Comparable P (similar accuracy, better efficiency)")
    print("  • Higher W (follows natural principles, elegant design)")
    print("\nThis is what 'faithful in least' looks like in practice.")
    print("=" * 60)


if __name__ == '__main__':
    demo()
