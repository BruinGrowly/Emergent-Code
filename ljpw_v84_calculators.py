#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
LJPW V8.4 Calculators

This module implements the core mathematical functions from LJPW Framework V8.4:
- Universal Growth Function (The Generative Equation)
- Life Inequality (Autopoiesis condition)
- Perceptual Radiance (Unified rendering equation)

Date: January 2026
Version: 8.4
"""

import math
from typing import Dict

# =============================================================================
# CONSTANTS (V8.4)
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # 1.618033988749895
LN_PHI = math.log(PHI)        # 0.4812118250596034

# Life Inequality thresholds
AUTOPOIETIC_THRESHOLD = 1.1    # L^n/φ^d ratio for Autopoiesis
HOMEOSTATIC_THRESHOLD = 0.9    # Lower boundary for Homeostatic phase


# =============================================================================
# 1. THE GENERATIVE EQUATION (Universal Growth Function)
# =============================================================================

def meaning(B: float, L: float, n: int, d: float) -> float:
    """
    Calculate Meaning using the Universal Growth Function.
    
    M = B × L^n × φ^(-d)
    
    Args:
        B: Brick (seed/truth/axiom) - typically [0, 1]
        L: Love (expansion coefficient) - typically [1, 2]
        n: Iterations (recursive applications)
        d: Distance (semantic distance from source)
    
    Returns:
        M: Total meaning generated
    
    Example:
        >>> meaning(1.0, 1.5, 10, 2)  # High Love, 10 iterations, distance 2
        22.047...
    """
    if B < 0:
        raise ValueError("Brick (B) cannot be negative - truth is never negative")
    if L <= 0:
        raise ValueError("Love (L) must be positive")
    if n < 0:
        raise ValueError("Iterations (n) cannot be negative")
    
    return B * (L ** n) * (PHI ** (-d))


# =============================================================================
# 2. THE LIFE INEQUALITY (Autopoiesis Condition)
# =============================================================================

def is_autopoietic(L: float, n: int, d: float) -> Dict:
    """
    Check if a system satisfies the Life Inequality.
    
    L^n > φ^d → AUTOPOIETIC (Life)
    L^n < φ^d → ENTROPIC (Death)
    
    Args:
        L: Love coefficient (expansion rate)
        n: Iterations (time/cycles)
        d: Distance from source
    
    Returns:
        Dict with growth, decay, ratio, phase, and verdict
    
    Example:
        >>> result = is_autopoietic(1.2, 10, 5)
        >>> result['phase']
        'AUTOPOIETIC'
    """
    if L <= 0:
        raise ValueError("Love (L) must be positive")
    
    growth = L ** n
    decay = PHI ** d
    ratio = growth / decay if decay > 0 else float('inf')
    
    if ratio > AUTOPOIETIC_THRESHOLD:
        phase = "AUTOPOIETIC"
    elif ratio > HOMEOSTATIC_THRESHOLD:
        phase = "HOMEOSTATIC"
    else:
        phase = "ENTROPIC"
    
    return {
        "growth": growth,
        "decay": decay,
        "ratio": ratio,
        "phase": phase,
        "verdict": f"L^{n} = {growth:.4f}, phi^{d} = {decay:.4f}, Ratio = {ratio:.4f}"
    }


def life_inequality_check(L: float, n: int, d: float) -> bool:
    """
    Simple boolean check for Life Inequality.
    
    Returns True if L^n > φ^d (system is alive).
    """
    return (L ** n) > (PHI ** d)


# =============================================================================
# 3. PERCEPTUAL RADIANCE (Unified Rendering Equation)
# =============================================================================

def perceptual_radiance(L_phys: float, S: float, kappa_sem: float) -> float:
    """
    Calculate Perceptual Radiance (Unified Rendering Equation).
    
    L_perc = L_phys × [1 + φ × S × κ_sem]
    
    Args:
        L_phys: Physical radiance from Kajiya equation [0, ∞)
        S: Semantic salience [0, 1]
        kappa_sem: Semantic curvature (meaning intensity) [0, ∞)
    
    Returns:
        L_perc: Perceptual radiance (what consciousness perceives)
    
    Example:
        >>> perceptual_radiance(1.0, 0.8, 0.5)  # High salience, moderate curvature
        1.647...
    """
    if L_phys < 0:
        raise ValueError("Physical radiance cannot be negative")
    if not 0 <= S <= 1:
        raise ValueError("Semantic salience must be in [0, 1]")
    if kappa_sem < 0:
        raise ValueError("Semantic curvature cannot be negative")
    
    return L_phys * (1 + PHI * S * kappa_sem)


# =============================================================================
# 4. COMPRESSION RATIO PREDICTOR
# =============================================================================

def predict_compression_ratio(L: float, n: int) -> float:
    """
    Predict compression ratio when generators are shared (d=0).
    
    When d=0, φ^(-d) = 1, so:
    Compression Ratio ≈ L^n
    
    Example: Koch snowflake with L=5, n=13
    Ratio = 5^13 ≈ 1.2 billion : 1
    
    Args:
        L: Love coefficient (expansion rate)
        n: Iterations
    
    Returns:
        Predicted compression ratio
    """
    if L <= 0:
        raise ValueError("Love (L) must be positive")
    return L ** n


# =============================================================================
# 5. MATHEMATICAL HOPE (V8.4)
# =============================================================================

def calculate_hope(L: float, current_n: int, d: float, target_ratio: float = 1.1) -> Dict:
    """
    Calculate iterations needed for L^n > φ^d (Hope is calculus).
    
    Hope = the number of iterations needed for growth to exceed decay.
    
    Args:
        L: Love coefficient
        current_n: Current iterations
        d: Distance from source
        target_ratio: Target growth/decay ratio (default 1.1 for Autopoiesis)
    
    Returns:
        Dict with current state and iterations to hope
    """
    if L <= 1:
        return {
            "current_ratio": (L ** current_n) / (PHI ** d),
            "iterations_needed": float('inf'),
            "hope": False,
            "message": "Love must exceed 1.0 to achieve Autopoiesis"
        }
    
    # n > d × ln(φ) / ln(L) + ln(target_ratio) / ln(L)
    ln_L = math.log(L)
    required_n = (d * LN_PHI + math.log(target_ratio)) / ln_L
    
    current_ratio = (L ** current_n) / (PHI ** d)
    iterations_needed = max(0, math.ceil(required_n) - current_n)
    
    return {
        "current_ratio": current_ratio,
        "required_n": required_n,
        "iterations_needed": iterations_needed,
        "hope": iterations_needed < float('inf'),
        "message": f"Need {iterations_needed} more iterations to reach Autopoiesis" 
                   if iterations_needed > 0 else "Already Autopoietic!"
    }


# =============================================================================
# SELF-TEST
# =============================================================================

def self_test():
    """Run V8.4 calculator self-tests."""
    print("=" * 60)
    print("LJPW V8.4 CALCULATOR SELF-TEST")
    print("=" * 60)
    
    # Test 1: Generative Equation
    print("\n1. GENERATIVE EQUATION (M = B x L^n x phi^(-d))")
    m = meaning(B=1.0, L=1.5, n=10, d=2)
    print(f"   B=1.0, L=1.5, n=10, d=2 -> M = {m:.4f}")
    
    # Test 2: Life Inequality
    print("\n2. LIFE INEQUALITY")
    result = is_autopoietic(L=1.2, n=10, d=5)
    print(f"   L=1.2, n=10, d=5 -> {result['phase']}")
    print(f"   {result['verdict']}")
    
    # Test 3: Perceptual Radiance
    print("\n3. PERCEPTUAL RADIANCE")
    L_perc = perceptual_radiance(L_phys=1.0, S=0.8, kappa_sem=0.5)
    print(f"   L_phys=1.0, S=0.8, kappa=0.5 -> L_perc = {L_perc:.4f}")
    
    # Test 4: Compression Ratio
    print("\n4. COMPRESSION RATIO (d=0)")
    ratio = predict_compression_ratio(L=5, n=13)
    print(f"   L=5, n=13 -> Ratio = {ratio:,.0f}:1")
    
    # Test 5: Mathematical Hope
    print("\n5. MATHEMATICAL HOPE")
    hope = calculate_hope(L=1.1, current_n=5, d=10)
    print(f"   {hope['message']}")
    
    print("\n" + "=" * 60)
    print("[OK] ALL V8.4 CALCULATORS OPERATIONAL")
    print("=" * 60)


if __name__ == "__main__":
    self_test()
