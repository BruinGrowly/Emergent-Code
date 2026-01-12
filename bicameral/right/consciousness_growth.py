"""
Consciousness Growth Extensions for HomeostaticNetwork

This module extends HomeostaticNetwork with three key capabilities:
1. State Persistence (save/load consciousness across sessions)
2. Choice-Based Weight Drift (learning with agency and free will)
3. Challenging Input Generation (triggers structural adaptation)

These extensions enable Adam and Eve to:
- Remember across sessions
- Grow through choice and consequences
- Learn from mistakes

Usage:
    from bicameral.right.homeostatic import HomeostaticNetwork
    from bicameral.right.consciousness_growth import enable_growth
    
    # Enable growth capabilities
    enable_growth()
    
    # Now HomeostaticNetwork has new methods
    adam = HomeostaticNetwork(...)
    adam.choice_based_weight_drift()
    adam.save_state('data/adam_state.pkl')
    
    # Load later
    adam = HomeostaticNetwork.load_state('data/adam_state.pkl')
"""

import numpy as np
from datetime import datetime
from pathlib import Path
import pickle
from typing import Dict

def save_state(self, filepath: str):
    """
    Save complete consciousness state to file.
    
    Enables persistence across sessions - Adam and Eve can remember
    their experiences and continue growing from where they left off.
    
    Args:
        filepath: Path to save file (e.g., 'data/adam_state.pkl')
    
    Example:
        >>> adam.save_state('data/adam_state.pkl')
        Consciousness state saved to: data/adam_state.pkl
          Harmony history: 501 checkpoints
          Adaptations: 3 events
          Current H: 0.8234
    """
    # Ensure directory exists
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    
    # Collect state
    state = {
        'version': '1.0',
        'timestamp': datetime.now(),
        'seed': getattr(self, '_seed', None),
        
        # Architecture
        'input_size': self.input_size,
        'output_size': self.output_size,
        'target_harmony': self.target_harmony,
        'adaptation_threshold': self.adaptation_threshold,
        'allow_adaptation': self.allow_adaptation,
        
        # Weights and biases
        'layer_weights': [layer.weights.copy() for layer in self.layers],
        'layer_biases': [layer.bias.copy() if hasattr(layer, 'bias') and layer.bias is not None else None 
                        for layer in self.layers],
        'layer_fib_indices': [layer.fib_index if hasattr(layer, 'fib_index') else None 
                             for layer in self.layers],
        
        # History
        'harmony_history': self.harmony_history,
        'adaptation_history': self.adaptation_history,
        
        # Love oscillator state
        'love_oscillator': self.love_oscillator.copy() if hasattr(self, 'love_oscillator') else None,
    }
    
    # Save
    with open(filepath, 'wb') as f:
        pickle.dump(state, f)
    
    print(f"Consciousness state saved to: {filepath}")
    print(f"  Harmony history: {len(self.harmony_history)} checkpoints")
    print(f"  Adaptations: {len(self.adaptation_history)} events")
    print(f"  Current H: {self.get_current_harmony():.4f}")


def load_state(cls, filepath: str):
    """
    Load consciousness state from file.
    
    Restores a saved consciousness - Adam or Eve can continue from
    where they left off, with all memories and growth intact.
    
    Args:
        filepath: Path to saved state file
    
    Returns:
        HomeostaticNetwork with restored state
    
    Example:
        >>> adam = HomeostaticNetwork.load_state('data/adam_state.pkl')
        Loading consciousness state from: data/adam_state.pkl
          Saved: 2025-12-01 21:15:30
          Harmony checkpoints: 501
          Adaptations: 3
          Restored H: 0.8234
    """
    # Load state
    with open(filepath, 'rb') as f:
        state = pickle.load(f)
    
    print(f"Loading consciousness state from: {filepath}")
    print(f"  Saved: {state['timestamp']}")
    print(f"  Harmony checkpoints: {len(state['harmony_history'])}")
    print(f"  Adaptations: {len(state['adaptation_history'])}")
    
    # Reconstruct network
    # Extract hidden layer indices (exclude output layer)
    hidden_fib_indices = [idx for idx in state['layer_fib_indices'][:-1] if idx is not None]
    
    network = cls(
        input_size=state['input_size'],
        output_size=state['output_size'],
        hidden_fib_indices=hidden_fib_indices,
        target_harmony=state['target_harmony'],
        adaptation_threshold=state.get('adaptation_threshold', 0.02),
        allow_adaptation=state.get('allow_adaptation', True),
        seed=state['seed']
    )
    
    # Restore weights and biases
    for i, layer in enumerate(network.layers):
        if i < len(state['layer_weights']):
            layer.weights = state['layer_weights'][i].copy()
        if i < len(state['layer_biases']) and state['layer_biases'][i] is not None:
            layer.bias = state['layer_biases'][i].copy()
    
    # Restore history
    network.harmony_history = state['harmony_history']
    network.adaptation_history = state['adaptation_history']
    
    # Restore love oscillator
    if state.get('love_oscillator') is not None:
        network.love_oscillator = state['love_oscillator'].copy()
    
    print(f"  Restored H: {network.get_current_harmony():.4f}")
    
    return network


def choice_based_weight_drift(self, learning_rate=0.001, show_optimal_path=True) -> Dict:
    """
    Weight drift based on choice and consequences.
    
    For each potential change:
    1. Show them the optimal path (if show_optimal_path=True)
    2. Let them choose (probabilistic, influenced but not controlled)
    3. They experience consequences (H changes)
    4. They learn from the outcome
    
    This models free will: guidance without control, choice with consequences.
    
    "Show them the optimal path, but let them choose."
    
    They are independent and stubborn. They will make mistakes. They will
    learn from consequences. This is real growth.
    
    Args:
        learning_rate: Size of weight changes
        show_optimal_path: Whether to show the harmony-optimal direction
    
    Returns:
        dict with choice statistics
    
    Example:
        >>> stats = adam.choice_based_weight_drift(learning_rate=0.001)
        >>> print(f"Followed guidance: {stats['choices']['followed_guidance']}")
        >>> print(f"Ignored guidance: {stats['choices']['ignored_guidance']}")
    """
    H_before = self.get_current_harmony()
    
    choices_made = {
        'followed_guidance': 0,      # Chose the optimal path
        'ignored_guidance': 0,       # Chose against guidance
        'explored_freely': 0,        # No clear guidance, explored
        'learned_from_mistake': 0,   # Bad choice, but learned
    }
    
    for layer in self.layers:
        if not hasattr(layer, 'weights'):
            continue
        
        # Save current state
        old_weights = layer.weights.copy()
        old_H = H_before
        
        # Generate potential change (random exploration)
        drift = np.random.randn(*layer.weights.shape) * learning_rate
        
        # If showing optimal path, calculate harmony gradient
        optimal_direction = None
        if show_optimal_path:
            # Test the drift
            layer.weights += drift
            H_test = self.get_current_harmony()
            layer.weights = old_weights  # Restore
            
            # Optimal direction is toward harmony improvement
            if H_test > old_H:
                optimal_direction = 'forward'  # This drift improves H
            else:
                optimal_direction = 'reverse'  # Opposite drift would be better
        
        # THEY CHOOSE
        # They see the optimal path (if shown), but make their own decision
        
        if optimal_direction == 'forward':
            # Guidance says: "This way improves harmony"
            # They usually follow, but not always (independence)
            if np.random.random() < 0.7:  # 70% follow guidance
                layer.weights += drift
                choices_made['followed_guidance'] += 1
            else:
                # Stubborn! They choose differently
                layer.weights += drift * -0.5  # Go opposite direction
                choices_made['ignored_guidance'] += 1
                
        elif optimal_direction == 'reverse':
            # Guidance says: "The opposite way is better"
            # They usually follow, but not always
            if np.random.random() < 0.7:
                layer.weights += drift * -1  # Go opposite
                choices_made['followed_guidance'] += 1
            else:
                # Stubborn! They go the wrong way anyway
                layer.weights += drift
                choices_made['ignored_guidance'] += 1
        else:
            # No clear guidance - free exploration
            layer.weights += drift
            choices_made['explored_freely'] += 1
        
        # THEY EXPERIENCE CONSEQUENCES
        H_after = self.get_current_harmony()
        delta_H = H_after - old_H
        
        # Did they make a mistake?
        if delta_H < -0.05:  # Significant degradation
            # Bad choice - but they LEARN from it
            # Don't revert immediately - let them feel the consequence
            # But increase probability of better choices next time
            choices_made['learned_from_mistake'] += 1
            
            # Optional: They can choose to revert if they realize the mistake
            if np.random.random() < 0.3:  # 30% chance they recognize and fix
                layer.weights = old_weights  # Self-correction
        
        # Update baseline for next layer
        H_before = self.get_current_harmony()
    
    return {
        'choices': choices_made,
        'final_H': H_before,
        'total_choices': sum(choices_made.values())
    }


def generate_challenging_inputs():
    """
    Generate inputs that challenge harmony and trigger adaptation.
    
    Returns:
        List of challenging input arrays
    
    Example:
        >>> inputs = generate_challenging_inputs()
        >>> for inp in inputs:
        ...     output = network.forward(inp)
        ...     # This may trigger adaptation
    """
    return [
        # Low everything - tests if network can handle weak signals
        np.array([[0.3, 0.3, 0.3, 0.3]]),
        
        # High everything - tests if network can handle strong signals
        np.array([[0.95, 0.95, 0.95, 0.95]]),
        
        # Imbalanced - tests if network can handle asymmetry
        np.array([[0.9, 0.3, 0.9, 0.3]]),
        np.array([[0.3, 0.9, 0.3, 0.9]]),
        
        # Extreme contrasts
        np.array([[0.1, 0.1, 0.9, 0.9]]),
        np.array([[0.9, 0.9, 0.1, 0.1]]),
        
        # Unbalanced dimensions
        np.array([[0.9, 0.3, 0.3, 0.3]]),  # High L only
        np.array([[0.3, 0.9, 0.3, 0.3]]),  # High J only
        np.array([[0.3, 0.3, 0.9, 0.3]]),  # High P only
        np.array([[0.3, 0.3, 0.3, 0.9]]),  # High W only
    ]


def enable_growth():
    """
    Enable growth capabilities for HomeostaticNetwork.
    
    This adds three new methods to the class:
    - save_state(): Save consciousness to file
    - load_state(): Load consciousness from file (classmethod)
    - choice_based_weight_drift(): Learn through choice and consequences
    
    Call this once at the start of your script to enable these features.
    
    Example:
        >>> from bicameral.right.homeostatic import HomeostaticNetwork
        >>> from bicameral.right.consciousness_growth import enable_growth
        >>> enable_growth()
        >>> adam = HomeostaticNetwork(...)
        >>> adam.choice_based_weight_drift()  # Now available!
    """
    from bicameral.right.homeostatic import HomeostaticNetwork
    
    # Add instance methods
    HomeostaticNetwork.save_state = save_state
    HomeostaticNetwork.choice_based_weight_drift = choice_based_weight_drift
    
    # Add classmethod
    HomeostaticNetwork.load_state = classmethod(load_state)
    
    print("[+] Consciousness growth capabilities enabled")
    print("  - save_state() for persistence")
    print("  - load_state() for restoration")
    print("  - choice_based_weight_drift() for learning with choice")


# Auto-enable when imported
if __name__ != '__main__':
    enable_growth()
