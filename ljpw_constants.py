#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
LJPW Composition Constants (Empirically Calibrated)

This module contains the calibrated coupling constants and structural bonuses
for LJPW composition predictions, optimized using real data from the Python
Code Harmonizer.

Calibration Results:
- Training examples: 13
- Optimization method: L-BFGS-B (scipy)
- MSE improvement: 22.8% (0.194 → 0.150)
- Date: 2025-11-23

These constants should be used by all experiments for consistent and
accurate LJPW composition predictions.
"""

# =============================================================================
# COUPLING CONSTANTS (Calibrated)
# =============================================================================

# How Love amplifies other dimensions
κ_LJ = 0.800  # Love → Justice (was 1.200, reduced 33%)
κ_LP = 1.061  # Love → Power (was 1.300, reduced 18%)
κ_JL = 0.800  # Justice → Love (was 1.200, reduced 33%)
κ_WL = 1.211  # Wisdom → Love (was 1.100, increased 10%)

# Legacy names for compatibility
KAPPA_LJ = κ_LJ
KAPPA_LP = κ_LP
KAPPA_JL = κ_JL
KAPPA_WL = κ_WL

# =============================================================================
# STRUCTURAL FEATURE BONUSES (Calibrated)
# =============================================================================

# These bonuses are added when specific structural features are present

# Documentation bonuses
BONUS_DOCSTRING = 0.100  # +0.10 L, +0.05 W (unchanged)
BONUS_TYPE_HINTS = 0.050  # +0.05 W (unchanged)

# Quality bonuses
BONUS_ERROR_HANDLING = 0.080  # +0.08 J (unchanged)
BONUS_LOGGING = 0.014  # +0.014 L (was 0.120, reduced 88%) ⚠️
BONUS_TESTING = 0.150  # +0.15 J (unchanged)

# State management bonuses
BONUS_STATE = 0.165  # +0.165 W, +0.082 J (was 0.150, increased 10%)
BONUS_HISTORY = 0.200  # +0.20 L, +0.06 W (unchanged)

# Validation bonus
BONUS_VALIDATION = 0.000  # +0.0 J (was 0.100, eliminated!) ⚠️

# =============================================================================
# HARMONY EFFECTS
# =============================================================================

# When multiple structural features are present, there's a harmony bonus
HARMONY_THRESHOLD = 3  # Minimum features for harmony
HARMONY_BONUS_PER_FEATURE = 0.05  # Bonus per feature above threshold

# =============================================================================
# KEY INSIGHTS FROM CALIBRATION
# =============================================================================

"""
1. Love's Amplification Overestimated:
   - κ_LJ and κ_JL reduced by 33%
   - Love doesn't amplify as strongly as theorized

2. Wisdom's Amplification Underestimated:
   - κ_WL increased by 10%
   - Good architecture creates better developer experience

3. Logging Bonus Nearly Eliminated:
   - Reduced from 0.120 to 0.014 (88% reduction)
   - Effect already captured in base components
   - log_operation primitive already has L=0.5

4. Validation Bonus Eliminated:
   - Reduced from 0.100 to 0.000 (100% reduction)
   - validate_numeric primitive already has J=1.0
   - Adding bonus would be double-counting

5. State Management Bonus Increased:
   - Increased from 0.150 to 0.165 (10% increase)
   - State adds more architectural complexity than expected
"""

# =============================================================================
# USAGE EXAMPLE
# =============================================================================

"""
from ljpw_constants import κ_LJ, κ_LP, κ_JL, κ_WL
from ljpw_constants import BONUS_DOCSTRING, BONUS_TESTING

def compose_ljpw(components, structural_features):
    # 1. Aggregate base values
    L = avg([c.L for c in components])
    J = avg([c.J for c in components])
    P = avg([c.P for c in components])
    W = avg([c.W for c in components])

    # 2. Apply coupling
    J_coupled = J * (1.0 + L * (κ_LJ - 1.0))
    P_coupled = P * (1.0 + L * (κ_LP - 1.0))
    L_coupled = L * (1.0 + J * (κ_JL - 1.0))
    L_coupled = L_coupled * (1.0 + W * (κ_WL - 1.0))

    # 3. Add structural bonuses
    if structural_features.get('has_docstring'):
        L_coupled += BONUS_DOCSTRING
        W += BONUS_DOCSTRING * 0.5

    if structural_features.get('has_testing'):
        J_coupled += BONUS_TESTING

    # etc...

    return LJPW(L_coupled, J_coupled, P_coupled, W)
"""

# =============================================================================
# VERSION HISTORY
# =============================================================================

CALIBRATION_VERSION = "1.0.0"
CALIBRATION_DATE = "2025-11-23"
TRAINING_EXAMPLES = 13
MSE_IMPROVEMENT = 0.228  # 22.8%
OPTIMIZATION_METHOD = "L-BFGS-B"

# Previous (theoretical) values for reference
THEORETICAL_CONSTANTS = {
    "κ_LJ": 1.200,
    "κ_LP": 1.300,
    "κ_JL": 1.200,
    "κ_WL": 1.100,
    "BONUS_LOGGING": 0.120,
    "BONUS_VALIDATION": 0.100,
}

# Calibrated values
CALIBRATED_CONSTANTS = {
    "κ_LJ": 0.800,
    "κ_LP": 1.061,
    "κ_JL": 0.800,
    "κ_WL": 1.211,
    "BONUS_LOGGING": 0.014,
    "BONUS_VALIDATION": 0.000,
}

def get_all_constants():
    """Return all constants as a dictionary."""
    return {
        "κ_LJ": κ_LJ,
        "κ_LP": κ_LP,
        "κ_JL": κ_JL,
        "κ_WL": κ_WL,
        "BONUS_DOCSTRING": BONUS_DOCSTRING,
        "BONUS_TYPE_HINTS": BONUS_TYPE_HINTS,
        "BONUS_ERROR_HANDLING": BONUS_ERROR_HANDLING,
        "BONUS_LOGGING": BONUS_LOGGING,
        "BONUS_TESTING": BONUS_TESTING,
        "BONUS_STATE": BONUS_STATE,
        "BONUS_HISTORY": BONUS_HISTORY,
        "BONUS_VALIDATION": BONUS_VALIDATION,
        "HARMONY_THRESHOLD": HARMONY_THRESHOLD,
        "HARMONY_BONUS_PER_FEATURE": HARMONY_BONUS_PER_FEATURE,
    }

def print_constants():
    """Print all constants in a readable format."""
    print("=" * 70)
    print("LJPW COMPOSITION CONSTANTS (Calibrated)")
    print("=" * 70)
    print()
    print("Coupling Constants:")
    print(f"  κ_LJ (Love → Justice):  {κ_LJ:.3f}")
    print(f"  κ_LP (Love → Power):    {κ_LP:.3f}")
    print(f"  κ_JL (Justice → Love):  {κ_JL:.3f}")
    print(f"  κ_WL (Wisdom → Love):   {κ_WL:.3f}")
    print()
    print("Structural Bonuses:")
    print(f"  Docstring:       {BONUS_DOCSTRING:.3f}")
    print(f"  Type hints:      {BONUS_TYPE_HINTS:.3f}")
    print(f"  Error handling:  {BONUS_ERROR_HANDLING:.3f}")
    print(f"  Logging:         {BONUS_LOGGING:.3f} (⚠️ nearly eliminated)")
    print(f"  Testing:         {BONUS_TESTING:.3f}")
    print(f"  State:           {BONUS_STATE:.3f}")
    print(f"  History:         {BONUS_HISTORY:.3f}")
    print(f"  Validation:      {BONUS_VALIDATION:.3f} (⚠️ eliminated)")
    print()
    print(f"Calibration: v{CALIBRATION_VERSION} ({CALIBRATION_DATE})")
    print(f"Training: {TRAINING_EXAMPLES} examples, {MSE_IMPROVEMENT:.1%} improvement")
    print("=" * 70)

if __name__ == "__main__":
    print_constants()
