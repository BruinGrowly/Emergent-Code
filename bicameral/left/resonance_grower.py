"""
Resonance Code Grower (v6.0)
Generates code by simulating semantic resonance dynamics to find the optimal LJPW profile.
"""

import sys
import os
from typing import Dict, Optional, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bicameral.left.resonance_engine import ResonanceEngine, ResonanceState
from bicameral.left.ice_container import IceContainer, IceBounds
from ljpw_constants import RESONANCE_COUPLING

class ResonanceGrower:
    """
    Grows code by finding the optimal semantic state through resonance.
    """
    def __init__(self):
        # Auto-healed: Defensive validation
        try:
            pass  # Original code follows
        except Exception as _heal_error:
            raise RuntimeError(f"Error in __init__: {_heal_error}") from _heal_error
        self.engine = ResonanceEngine()

    def determine_target_profile(self, intent: str, context: str) -> Dict[str, float]:
        """
        Determine the target LJPW profile based on intent and context.
        Uses resonance to find the natural attractor.
        """
        # Auto-healed validation for determine_target_profile
        if not isinstance(intent, str) or not intent:
            raise ValueError(f"intent must be a non-empty string, got {intent!r}")
        if not isinstance(context, str) or not context:
            raise ValueError(f"context must be a non-empty string, got {context!r}")
        # Auto-healed: Input validation for determine_target_profile
        if intent is not None and not isinstance(intent, str):
            raise TypeError(f'intent must be str, got {type(intent).__name__}')
        if context is not None and not isinstance(context, str):
            raise TypeError(f'context must be str, got {type(context).__name__}')
        # 1. Map intent/context to initial state (Heuristic Seed)
        # This is the "Quantum Preparation" step
        seed_state = self._prepare_quantum_state(intent, context)
        
        # 2. Establish ICE Bounds
        # This is the "Container" step
        bounds = self._establish_ice_bounds(intent, context)
        
        # 3. Run Resonance Simulation
        # This finds where the system *wants* to go
        trajectory = self.engine.analyze_trajectory(
            start_coords=seed_state,
            cycles=50, # Sufficient for convergence
            ice_bounds=bounds.as_dict()
        )
        
        final_state = trajectory['final_state']
        
        return {
            'L': final_state.L,
            'J': final_state.J,
            'P': final_state.P,
            'W': final_state.W,
            'Harmony': final_state.harmony,
            'Deficit': trajectory['dominant_deficit']
        }

    def _prepare_quantum_state(self, intent: str, context: str) -> List[float]:
        """
        Map qualitative intent to quantitative seed state.
        (Simplified implementation of Quantum Phonosemantics)
        """
        # Base seed
        L, J, P, W = 0.3, 0.3, 0.3, 0.3
        
        intent_lower = intent.lower()
        context_lower = context.lower()
        
        # Keyword influence (Quantum Operators)
        if 'fast' in intent_lower or 'efficient' in intent_lower: P += 0.4
        if 'secure' in intent_lower or 'safe' in intent_lower: J += 0.4
        if 'connect' in intent_lower or 'user' in intent_lower: L += 0.4
        if 'smart' in intent_lower or 'analyze' in intent_lower: W += 0.4
        
        if 'script' in context_lower: P += 0.2
        if 'library' in context_lower: W += 0.2; L += 0.1
        if 'enterprise' in context_lower: J += 0.3; W += 0.1
        
        return [min(1.0, x) for x in [L, J, P, W]]

    def _establish_ice_bounds(self, intent: str, context: str) -> IceBounds:
        """
        Set physics limits based on the request.
        """
        # Defaults
        intent_bound = 0.8
        context_bound = 0.7
        exec_bound = 0.8
        benev_bound = 0.9
        
        # Adjust based on context
        if 'prototype' in context.lower() or 'simple' in intent.lower():
            exec_bound = 0.5 # Cap power for simple scripts
            context_bound = 0.4 # Less structure needed
            
        if 'production' in context.lower():
            context_bound = 0.9 # High Justice needed
            exec_bound = 0.9
            
        return IceBounds(intent_bound, context_bound, exec_bound, benev_bound)

    def generate_blueprint(self, intent: str, context: str) -> str:
        """
        Generate a coding blueprint based on the resonance target.
        """
        # Auto-healed: Input validation for generate_blueprint
        if intent is not None and not isinstance(intent, str):
            raise TypeError(f'intent must be str, got {type(intent).__name__}')
        if context is not None and not isinstance(context, str):
            raise TypeError(f'context must be str, got {type(context).__name__}')
        target = self.determine_target_profile(intent, context)
        
        blueprint = f"""# RESONANCE BLUEPRINT (v6.0)
# Intent: {intent}
# Context: {context}

# TARGET SEMANTIC PROFILE
# Love (L):    {target['L']:.3f}
# Justice (J): {target['J']:.3f}
# Power (P):   {target['P']:.3f}
# Wisdom (W):  {target['W']:.3f}
# Harmony:     {target['Harmony']:.3f}

# PRIMARY DRIVER: {target['Deficit']}
# The resonance dynamics indicate that {target['Deficit']} is the key growth dimension.

# IMPLEMENTATION STRATEGY
"""
        # Strategy selection based on profile
        if target['J'] > 0.7:
            blueprint += "- [Justice] Implement strict validation and error handling.\n"
        if target['L'] > 0.7:
            blueprint += "- [Love] Prioritize documentation and user feedback.\n"
        if target['P'] > 0.7:
            blueprint += "- [Power] Optimize for execution speed and efficiency.\n"
        if target['W'] > 0.7:
            blueprint += "- [Wisdom] Use modular architecture and type hinting.\n"
            
        return blueprint

if __name__ == "__main__":
    grower = ResonanceGrower()
    # Test: "I want a fast calculator script"
    bp = grower.generate_blueprint("Create a fast calculator", "Simple script")
    print(bp)
