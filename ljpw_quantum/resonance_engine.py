"""
LJPW Resonance Engine
Implements the v6.0 Resonance Mechanics for semantic oscillation and deficit detection.
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import sys
import os

# Add project root to path to find ljpw_constants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_constants import RESONANCE_COUPLING, PHI, ROOT_2, E_EULER, LN_2

@dataclass
class ResonanceState:
    """Represents the semantic state at a specific moment in resonance."""
    L: float
    J: float
    P: float
    W: float
    iteration: int
    harmony: float = 0.0
    
    def as_vector(self) -> List[float]:
        return [self.L, self.J, self.P, self.W]

class ResonanceEngine:
    """
    Simulates the dynamical evolution of semantic states through LJPW space.
    Uses asymmetric coupling to reveal hidden deficits.
    """
    
    def __init__(self):
        self.coupling_matrix = RESONANCE_COUPLING
        # Natural Equilibrium constants
        self.NE = {
            'L': 1.0 / PHI,       # 0.618
            'J': ROOT_2 - 1.0,    # 0.414
            'P': E_EULER - 2.0,   # 0.718
            'W': LN_2             # 0.693
        }
        self.ANCHOR = {'L': 1.0, 'J': 1.0, 'P': 1.0, 'W': 1.0}

    def calculate_harmony(self, L: float, J: float, P: float, W: float) -> float:
        """
        Calculate harmony as inverse distance from the Anchor Point (1,1,1,1).
        H = 1 / (1 + distance)
        """
        dist = math.sqrt(
            (1.0 - L)**2 + 
            (1.0 - J)**2 + 
            (1.0 - P)**2 + 
            (1.0 - W)**2
        )
        return 1.0 / (1.0 + dist)

    def cycle(self, state: ResonanceState, ice_bounds: Optional[Dict[str, float]] = None) -> ResonanceState:
        """
        Perform one resonance cycle (timestep).
        Applies the asymmetric coupling matrix: dX/dt = coupling * X
        """
        # Current values
        current = {'L': state.L, 'J': state.J, 'P': state.P, 'W': state.W}
        next_vals = {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}
        
        # Calculate coupling strength based on current harmony (Law of Karma)
        # Higher harmony = stronger coupling (positive feedback)
        kappa = 0.5 + state.harmony
        
        # Apply matrix: Target = Sum(Source * Coupling[Source][Target])
        # We calculate the *influence* from other dimensions
        for target in ['L', 'J', 'P', 'W']:
            influence_sum = 0.0
            
            for source in ['L', 'J', 'P', 'W']:
                # Basic influence
                factor = self.coupling_matrix[source][target]
                
                # Calculate the "pull"
                # If source is high, it pulls target up via the coupling factor
                # Differential equation approximation: dTarget += Source * Factor * dt
                # Using a small timestep dt for stability
                dt = 0.1
                influence = current[source] * factor * dt
                influence_sum += influence
            
            # Update value
            # New = Old + (Influence - Decay) * kappa
            # Decay towards Natural Equilibrium to prevent explosion without bounds
            # (In bounded mode, ICE handles the limits)
            
            decay = (current[target] - self.NE[target]) * 0.05
            
            # The core dynamic equation
            delta = (influence_sum - decay) * kappa
            next_val = current[target] + delta * dt
            
            # Apply bounds if provided (ICE Framework)
            if ice_bounds:
                bound_key_map = {'L': 'Benevolence', 'J': 'Context', 'P': 'Execution', 'W': 'Intent'}
                bound = ice_bounds.get(bound_key_map.get(target, target), 1.5) # Default loose bound
                next_val = min(next_val, bound)
            
            next_vals[target] = next_val

        # Create new state
        new_harmony = self.calculate_harmony(**next_vals)
        return ResonanceState(
            L=next_vals['L'],
            J=next_vals['J'],
            P=next_vals['P'],
            W=next_vals['W'],
            iteration=state.iteration + 1,
            harmony=new_harmony
        )

    def analyze_trajectory(self, start_coords: List[float], cycles: int = 100, ice_bounds: Optional[Dict[str, float]] = None) -> Dict:
        """
        Run a full resonance simulation to find deficits and attractors.
        """
        initial_harmony = self.calculate_harmony(*start_coords)
        current_state = ResonanceState(
            L=start_coords[0], 
            J=start_coords[1], 
            P=start_coords[2], 
            W=start_coords[3], 
            iteration=0,
            harmony=initial_harmony
        )
        
        history = [current_state]
        
        for _ in range(cycles):
            current_state = self.cycle(current_state, ice_bounds)
            history.append(current_state)
            
        # Analysis
        final_state = history[-1]
        
        # Deficit detection: Which dimension grew the most?
        # That dimension was the "deficit" that needed filling.
        deltas = {
            'L': final_state.L - history[0].L,
            'J': final_state.J - history[0].J,
            'P': final_state.P - history[0].P,
            'W': final_state.W - history[0].W
        }
        
        dominant_deficit = max(deltas.items(), key=lambda x: x[1])
        
        return {
            'initial_state': history[0],
            'final_state': final_state,
            'history': history,
            'dominant_deficit': dominant_deficit[0],
            'growth': dominant_deficit[1],
            'converged': abs(history[-1].harmony - history[-2].harmony) < 0.001
        }

if __name__ == "__main__":
    # Quick test
    engine = ResonanceEngine()
    print("Resonance Engine Initialized.")
    results = engine.analyze_trajectory([0.2, 0.2, 0.8, 0.2], cycles=50) # High Power, others low
    print(f"Initial: {results['initial_state'].as_vector()}")
    print(f"Final:   {results['final_state'].as_vector()}")
    print(f"Deficit: {results['dominant_deficit']} (Growth: {results['growth']:.3f})")
