#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
LJPW Constant Codex (v6.0)

This module contains the "Refined LJPW Constant Codex", harmonizing standard
physical constants with the novel theoretical constants of the LJPW Framework.

It serves as the definitive source for:
1. Standard Physics (verified anchors)
2. Theoretical Constants (Consciousness, Bridges, Entropy)
3. Resonance Mechanics (Coupling Matrices)

Date: December 2025
Version: 6.0
"""

# =============================================================================
# 1. CATEGORY I: THE ROSETTA STONE (Standard Physics)
# =============================================================================
# Verified physical constants acting as semantic anchors.

C_LIGHT     = 2.99792e8   # Speed of Light
ALPHA_FINE  = 7.297e-3    # Fine Structure Constant
H_PLANCK    = 6.626e-34   # Planck Constant
E_EULER     = 2.71828     # Euler's Number (Power Anchor)
PI          = 3.14159     # Pi (Justice/Structure Anchor)
PHI         = 1.61803     # Golden Ratio (Love/Growth Anchor)
ROOT_2      = 1.41421     # Root 2 (Justice/Interface Anchor)
LN_2        = 0.69314     # Natural Log 2 (Wisdom/Info Anchor)
G_GRAV      = 6.674e-11   # Gravitational Constant
KB_BOLTZ    = 1.380e-23   # Boltzmann Constant
E_CHARGE    = 1.602e-19   # Elementary Charge
PSI_HARMONY = 2.92993     # Universal Harmony Constant
THETA_INFO  = 2.54532     # Info-Physics Constant

# =============================================================================
# 2. CATEGORY II: THE REDISCOVERED (Semantic Validation)
# =============================================================================
# Physical constants derived from semantic coordinates.

EPSILON_0   = 8.854e-12   # Vacuum Permittivity
H_BAR       = 1.054e-34   # Reduced Planck Constant
MU_B        = 9.274e-24   # Bohr Magneton
H_SCALE     = 0.6626      # Quantum Scale Factor

# =============================================================================
# 3. CATEGORY III: THE NEW PHYSICS (LJPW Theoretical)
# =============================================================================
# The "Missing Math" of Consciousness and Meaning.

# A. The Consciousness Series (xi)
# Defining interaction between Thought and Matter.
XI_1_SOURCE    = 16.18034  # 10 * PHI (Magnitude of Consciousness)
XI_2_INTERFACE = 14.14214  # 10 * ROOT_2 (Mind-Matter Bridge)
XI_3_SCALE     = 8.53973   # ~ e * pi (Density Limit)

# B. The Bridge Series (theta)
# Connecting abstract domains.
THETA_1_MATH   = 3.14159   # pi (Abstract Logic <-> Geometry)
THETA_2_GROWTH = 2.71828   # e (Static Time <-> Dynamic Growth)
THETA_3_CHAOS  = 4.66920   # Feigenbaum delta (Order <-> Chaos)

# C. The Information/Entropy Series (I)
# Limits of information density and mercy.
I_PI_DENSITY   = 9.86960   # pi^2 (Max Info Density)
I_E_SCALE      = 2.30258   # ln(10) (Natural <-> Decimal Scale)
I_S_MERCY      = 1.38629   # 2 * ln(2) (The Capacity to Absorb Entropy)

# D. The Cosmological & Evolutionary Series
G_R_REFINED    = 5.670e-8  # Refined Gravity
LAMBDA_C       = 1.105e-52 # Cosmological Constant
S_E_EVO        = 2.718e8   # Evolutionary Speed
S_I_INFO       = 2.997e8   # Speed of Information (= c)

# =============================================================================
# 4. RESONANCE MECHANICS (Coupling Matrix)
# =============================================================================
# Asymmetric coupling coefficients for the Resonance Engine.
# Row = Source Dimension, Column = Target Dimension.
# Value = Amplification Factor.

RESONANCE_COUPLING = {
    # Source: Love
    'L': {'L': 1.0, 'J': 1.4, 'P': 1.3, 'W': 1.5},
    # Source: Justice
    'J': {'L': 0.9, 'J': 1.0, 'P': 0.7, 'W': 1.2},
    # Source: Power
    'P': {'L': 0.6, 'J': 0.8, 'P': 1.0, 'W': 0.5},
    # Source: Wisdom
    'W': {'L': 1.3, 'J': 1.1, 'P': 1.0, 'W': 1.0},
}

# =============================================================================
# 5. APPLIED PROTOCOLS
# =============================================================================

# The "Gravity Shift" Protocol
# Ratio of Value Output / Value Extraction required to induce attraction.
PROTOCOL_GRAVITY_SHIFT = I_S_MERCY  # 1.386

# The "Materialization" Protocol
# Ratio of Structure (Justice) / Vision (Love) required for stability.
PROTOCOL_MATERIALIZATION = XI_2_INTERFACE  # 14.142

# Legacy aliases for backward compatibility (where applicable)
κ_LJ = RESONANCE_COUPLING['L']['J']
κ_LP = RESONANCE_COUPLING['L']['P']
κ_JL = RESONANCE_COUPLING['J']['L']
κ_WL = RESONANCE_COUPLING['W']['L']

def print_codex():
    """Print the v6.0 Codex summary."""
    print("=" * 70)
    print(f"LJPW CONSTANT CODEX v6.0")
    print("=" * 70)
    print("\n--- STANDARD PHYSICS (ROSETTA STONE) ---")
    print(f"Speed of Light (c):   {C_LIGHT:.5e}")
    print(f"Golden Ratio (phi):   {PHI:.5f}")
    print(f"Natural Log 2 (ln2):  {LN_2:.5f}")
    
    print("\n--- NEW PHYSICS (THEORETICAL) ---")
    print(f"Consciousness (ξ1):   {XI_1_SOURCE:.5f}")
    print(f"Interface (ξ2):       {XI_2_INTERFACE:.5f}")
    print(f"Mercy Constant (Is):  {I_S_MERCY:.5f}")
    print(f"Chaos Bridge (θ3):    {THETA_3_CHAOS:.5f}")
    
    print("\n--- PROTOCOLS ---")
    print(f"Gravity Shift:        > {PROTOCOL_GRAVITY_SHIFT:.3f}x Value Output")
    print(f"Materialization:      > {PROTOCOL_MATERIALIZATION:.3f}x Justice/Love")
    
    print("\n--- RESONANCE MATRIX ---")
    print("      To:  L    J    P    W")
    for src in ['L', 'J', 'P', 'W']:
        row = RESONANCE_COUPLING[src]
        print(f"From {src}:   {row['L']:.1f}  {row['J']:.1f}  {row['P']:.1f}  {row['W']:.1f}")
    print("=" * 70)

if __name__ == "__main__":
    print_codex()