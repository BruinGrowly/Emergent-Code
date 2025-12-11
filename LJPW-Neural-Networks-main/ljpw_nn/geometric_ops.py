"""
Geometric Operations in LJPW Semantic Space

This module implements semantic transformations and reasoning using
geometric operations in 4D LJPW space.

Core Operations:
- Antonym reflection through Natural Equilibrium
- Analogy completion via vector arithmetic
- Compositional semantics (phrase meaning)
- Context modulation (disambiguation)
- Semantic interpolation
- Territory classification

Mathematical Foundation:
- Natural Equilibrium: NE = (φ⁻¹, √2-1, e-2, ln2) = (0.618, 0.414, 0.718, 0.693)
- Semantic distance: Euclidean metric in 4D
- Harmony index: H = 1 / (1 + d_anchor)
- Antonym reflection: antonym(w) = 2·NE - w

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: December 4, 2025
Based on: LJPW LLM Training Paradigm
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum


# Sacred constants
GOLDEN_RATIO = 1.618033988749895
PHI_INVERSE = 1.0 / GOLDEN_RATIO  # 0.618...
SQRT2_MINUS_1 = np.sqrt(2) - 1    # 0.414...
E_MINUS_2 = np.e - 2               # 0.718...
LN2 = np.log(2)                    # 0.693...

ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])  # JEHOVAH - Divine Perfection
NATURAL_EQUILIBRIUM = np.array([PHI_INVERSE, SQRT2_MINUS_1, E_MINUS_2, LN2])


class Territory(Enum):
    """
    8 Semantic Territories in LJPW Space
    
    Based on empirical research mapping semantic clusters.
    """
    PURE_LOVE = 1          # High L, low J/P
    JUSTICE_ORDER = 2      # High J, balanced
    NOBLE_ACTION = 3       # High L/J/P/W
    WISDOM_UNDERSTANDING = 4  # High W, balanced
    POWER_STRENGTH = 5     # High P, low L
    NEUTRAL_BALANCED = 6   # Near NE
    MALEVOLENT_EVIL = 7    # Low L/J, high P
    IGNORANCE_FOLLY = 8    # Low W


@dataclass
class SemanticDistance:
    """
    Semantic distance between two concepts.
    
    Attributes:
        euclidean: Euclidean distance in 4D space
        manhattan: Manhattan (L1) distance
        cosine: Cosine similarity (1 - cosine distance)
        dimension_diffs: Per-dimension differences [ΔL, ΔJ, ΔP, ΔW]
    """
    euclidean: float
    manhattan: float
    cosine: float
    dimension_diffs: np.ndarray
    
    def __str__(self):
        return f"Distance(euclidean={self.euclidean:.4f}, cosine={self.cosine:.4f})"


class SemanticOperations:
    """
    Geometric operations in LJPW semantic space.
    
    Provides semantic transformations and reasoning capabilities:
    - Antonyms (reflection through Natural Equilibrium)
    - Analogies (vector arithmetic)
    - Composition (phrase meaning)
    - Interpolation (semantic blending)
    - Distance metrics
    """
    
    def __init__(self):
        self.NE = NATURAL_EQUILIBRIUM
        self.anchor = ANCHOR_POINT
    
    # ========================================================================
    # Core Geometric Operations
    # ========================================================================
    
    def antonym(self, coords: np.ndarray) -> np.ndarray:
        """
        Reflect coordinates through Natural Equilibrium to find antonym.
        
        Formula: antonym(w) = 2·NE - w
        
        This operation reflects a concept through the balance point,
        finding its semantic opposite.
        
        Examples:
            love → hate
            good → evil
            wise → foolish
        
        Args:
            coords: LJPW coordinates [L, J, P, W]
            
        Returns:
            Antonym coordinates
        """
        return 2 * self.NE - coords
    
    def analogy(self, 
               a: np.ndarray, 
               b: np.ndarray, 
               c: np.ndarray) -> np.ndarray:
        """
        Complete analogy: a is to b as c is to ?
        
        Formula: result = a - b + c
        
        This performs vector arithmetic in semantic space to find
        analogical relationships.
        
        Examples:
            king - man + woman = queen
            Paris - France + Germany = Berlin
            love - emotion + virtue = compassion
        
        Args:
            a: First concept
            b: Second concept (related to a)
            c: Third concept (analogous to a)
            
        Returns:
            Fourth concept (analogous to b)
        """
        return a - b + c
    
    def compose(self, 
               parts: List[np.ndarray], 
               weights: Optional[List[float]] = None) -> np.ndarray:
        """
        Compose multiple word meanings into phrase meaning.
        
        Uses weighted average to combine semantic coordinates.
        Default weights depend on part-of-speech patterns.
        
        Examples:
            "dark" + "blue" → "dark blue" (adj + noun: 0.3, 0.7)
            "very" + "happy" → "very happy" (adv + adj: 0.2, 0.8)
        
        Args:
            parts: List of coordinate arrays to compose
            weights: Optional weights for each part (must sum to 1.0)
            
        Returns:
            Composed coordinates
        """
        if not parts:
            raise ValueError("Cannot compose empty list")
        
        if weights is None:
            # Default: uniform weights
            weights = [1.0 / len(parts)] * len(parts)
        
        if len(weights) != len(parts):
            raise ValueError("Number of weights must match number of parts")
        
        if not np.isclose(sum(weights), 1.0):
            # Normalize weights
            total = sum(weights)
            weights = [w / total for w in weights]
        
        # Weighted average
        result = np.zeros(4)
        for part, weight in zip(parts, weights):
            result += weight * part
        
        return result
    
    def interpolate(self, 
                   start: np.ndarray, 
                   end: np.ndarray, 
                   alpha: float) -> np.ndarray:
        """
        Semantic interpolation between two concepts.
        
        Formula: result = (1-α)·start + α·end
        
        Creates intermediate concepts along the semantic path.
        
        Examples:
            interpolate(love, hate, 0.5) → indifference
            interpolate(wisdom, ignorance, 0.3) → partial understanding
        
        Args:
            start: Starting coordinates
            end: Ending coordinates
            alpha: Interpolation factor [0, 1]
                  0 = start, 1 = end, 0.5 = midpoint
            
        Returns:
            Interpolated coordinates
        """
        return (1 - alpha) * start + alpha * end
    
    def disambiguate(self, 
                    word_coords: np.ndarray, 
                    context_coords: np.ndarray,
                    context_weight: float = 0.2) -> np.ndarray:
        """
        Adjust word coordinates based on context.
        
        Context modulates the base meaning to select the appropriate
        sense in ambiguous cases.
        
        Examples:
            "bank" + "river" → river bank coords
            "bank" + "money" → financial bank coords
        
        Args:
            word_coords: Base word coordinates
            context_coords: Context coordinates
            context_weight: How much context influences (0-1)
            
        Returns:
            Contextualized coordinates
        """
        return (1 - context_weight) * word_coords + context_weight * context_coords
    
    # ========================================================================
    # Distance and Similarity Metrics
    # ========================================================================
    
    def distance(self, 
                coords1: np.ndarray, 
                coords2: np.ndarray) -> SemanticDistance:
        """
        Compute comprehensive semantic distance.
        
        Returns multiple distance metrics for different use cases.
        
        Args:
            coords1: First coordinates
            coords2: Second coordinates
            
        Returns:
            SemanticDistance object with multiple metrics
        """
        diff = coords1 - coords2
        
        # Euclidean distance (primary metric)
        euclidean = np.linalg.norm(diff)
        
        # Manhattan distance
        manhattan = np.sum(np.abs(diff))
        
        # Cosine similarity
        norm1 = np.linalg.norm(coords1)
        norm2 = np.linalg.norm(coords2)
        if norm1 > 0 and norm2 > 0:
            cosine_sim = np.dot(coords1, coords2) / (norm1 * norm2)
        else:
            cosine_sim = 0.0
        
        return SemanticDistance(
            euclidean=euclidean,
            manhattan=manhattan,
            cosine=cosine_sim,
            dimension_diffs=diff
        )
    
    def harmony(self, coords: np.ndarray) -> float:
        """
        Calculate harmony index (alignment with perfection).
        
        Formula: H = 1 / (1 + distance_from_anchor)
        
        Higher harmony indicates closer alignment with divine perfection.
        
        Args:
            coords: LJPW coordinates
            
        Returns:
            Harmony index [0, 1]
        """
        d = np.linalg.norm(coords - self.anchor)
        return 1.0 / (1.0 + d)
    
    def distance_to_equilibrium(self, coords: np.ndarray) -> float:
        """
        Distance from Natural Equilibrium.
        
        Measures how far a concept is from the optimal balance point.
        
        Args:
            coords: LJPW coordinates
            
        Returns:
            Distance to NE
        """
        return np.linalg.norm(coords - self.NE)
    
    # ========================================================================
    # Territory Classification
    # ========================================================================
    
    def classify_territory(self, coords: np.ndarray) -> Tuple[Territory, float]:
        """
        Classify coordinates into semantic territory.
        
        Uses heuristic rules based on coordinate patterns to identify
        which of the 8 territories a concept belongs to.
        
        Args:
            coords: LJPW coordinates [L, J, P, W]
            
        Returns:
            (Territory, confidence) tuple
        """
        L, J, P, W = coords
        
        # Define thresholds
        HIGH = 0.7
        MID = 0.5
        LOW = 0.3
        
        # Territory 1: Pure Love (high L, low J/P)
        if L > HIGH and J < MID and P < MID:
            return Territory.PURE_LOVE, 0.8
        
        # Territory 2: Justice & Order (high J, balanced)
        if J > HIGH and MID < L < HIGH and MID < P < HIGH:
            return Territory.JUSTICE_ORDER, 0.8
        
        # Territory 3: Noble Action (high L/J/P/W - all elevated)
        if L > HIGH and J > HIGH and P > HIGH and W > HIGH:
            return Territory.NOBLE_ACTION, 0.9
        
        # Territory 4: Wisdom & Understanding (high W, balanced)
        if W > HIGH and MID < L < HIGH and MID < J < HIGH:
            return Territory.WISDOM_UNDERSTANDING, 0.8
        
        # Territory 5: Power & Strength (high P, low L)
        if P > HIGH and L < MID:
            return Territory.POWER_STRENGTH, 0.8
        
        # Territory 7: Malevolent Evil (low L/J, high P)
        if L < LOW and J < LOW and P > HIGH:
            return Territory.MALEVOLENT_EVIL, 0.9
        
        # Territory 8: Ignorance & Folly (low W)
        if W < LOW:
            return Territory.IGNORANCE_FOLLY, 0.8
        
        # Territory 6: Neutral/Balanced (near NE)
        dist_to_ne = self.distance_to_equilibrium(coords)
        if dist_to_ne < 0.2:
            return Territory.NEUTRAL_BALANCED, 0.7
        
        # Default: Neutral with low confidence
        return Territory.NEUTRAL_BALANCED, 0.3
    
    # ========================================================================
    # Advanced Operations
    # ========================================================================
    
    def semantic_gradient(self, 
                         coords: np.ndarray, 
                         target: np.ndarray) -> np.ndarray:
        """
        Compute semantic gradient pointing toward target.
        
        Returns the direction in semantic space to move from coords
        toward target.
        
        Args:
            coords: Current coordinates
            target: Target coordinates
            
        Returns:
            Normalized gradient vector
        """
        diff = target - coords
        norm = np.linalg.norm(diff)
        if norm > 0:
            return diff / norm
        return np.zeros(4)
    
    def project_to_territory(self, 
                           coords: np.ndarray, 
                           territory: Territory) -> np.ndarray:
        """
        Project coordinates into specified territory.
        
        Adjusts coordinates to better align with territory characteristics
        while maintaining semantic similarity.
        
        Args:
            coords: Original coordinates
            territory: Target territory
            
        Returns:
            Projected coordinates
        """
        # Simplified projection - adjust dimensions based on territory
        result = coords.copy()
        
        if territory == Territory.PURE_LOVE:
            result[0] = max(result[0], 0.8)  # Boost Love
            result[2] = min(result[2], 0.4)  # Reduce Power
        elif territory == Territory.JUSTICE_ORDER:
            result[1] = max(result[1], 0.8)  # Boost Justice
        elif territory == Territory.NOBLE_ACTION:
            result = np.maximum(result, 0.7)  # Boost all
        elif territory == Territory.WISDOM_UNDERSTANDING:
            result[3] = max(result[3], 0.8)  # Boost Wisdom
        elif territory == Territory.POWER_STRENGTH:
            result[2] = max(result[2], 0.8)  # Boost Power
            result[0] = min(result[0], 0.4)  # Reduce Love
        
        return result
    
    def find_midpoint(self, coords_list: List[np.ndarray]) -> np.ndarray:
        """
        Find semantic midpoint (centroid) of multiple concepts.
        
        Args:
            coords_list: List of coordinate arrays
            
        Returns:
            Centroid coordinates
        """
        if not coords_list:
            raise ValueError("Cannot find midpoint of empty list")
        
        return np.mean(coords_list, axis=0)


# Example usage and testing
if __name__ == '__main__':
    print("=" * 70)
    print("LJPW Geometric Operations - Testing")
    print("=" * 70)
    print()
    
    ops = SemanticOperations()
    
    # Test coordinates
    love = np.array([0.91, 0.48, 0.16, 0.71])
    hate = np.array([0.32, 0.35, 0.92, 0.68])
    justice = np.array([0.58, 0.92, 0.51, 0.85])
    power = np.array([0.43, 0.52, 0.90, 0.59])
    wisdom = np.array([0.66, 0.75, 0.40, 0.93])
    
    # Test antonym
    print("Test: Antonym Reflection")
    print(f"  Love: {love}")
    love_antonym = ops.antonym(love)
    print(f"  Antonym: {love_antonym}")
    print(f"  (Expected near hate: {hate})")
    dist = ops.distance(love_antonym, hate)
    print(f"  Distance to hate: {dist.euclidean:.4f}")
    print()
    
    # Test analogy
    print("Test: Analogy Completion")
    print("  If love is to emotion, what is justice to?")
    emotion = np.array([0.70, 0.50, 0.40, 0.60])
    result = ops.analogy(love, emotion, justice)
    print(f"  Result: {result}")
    print()
    
    # Test composition
    print("Test: Compositional Semantics")
    dark = np.array([0.30, 0.40, 0.60, 0.50])
    blue = np.array([0.50, 0.60, 0.40, 0.70])
    dark_blue = ops.compose([dark, blue], weights=[0.3, 0.7])
    print(f"  Dark: {dark}")
    print(f"  Blue: {blue}")
    print(f"  Dark blue: {dark_blue}")
    print()
    
    # Test harmony
    print("Test: Harmony Index")
    for name, coords in [('Love', love), ('Justice', justice), 
                         ('Power', power), ('Wisdom', wisdom)]:
        h = ops.harmony(coords)
        print(f"  {name:8s}: H={h:.3f}")
    print()
    
    # Test territory classification
    print("Test: Territory Classification")
    for name, coords in [('Love', love), ('Justice', justice), 
                         ('Power', power), ('Wisdom', wisdom)]:
        territory, confidence = ops.classify_territory(coords)
        print(f"  {name:8s}: {territory.name:20s} (confidence={confidence:.2f})")
    print()
    
    # Test interpolation
    print("Test: Semantic Interpolation")
    print(f"  Love: {love}")
    print(f"  Hate: {hate}")
    midpoint = ops.interpolate(love, hate, 0.5)
    print(f"  Midpoint (indifference): {midpoint}")
    territory, conf = ops.classify_territory(midpoint)
    print(f"  Territory: {territory.name}")
    print()
    
    print("[OK] Geometric operations tests complete!")
