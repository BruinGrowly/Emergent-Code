"""
Composition Discovery Experiment (Experiment C)

This module implements a search algorithm that can discover optimal compositions
of atomic components to achieve target LJPW coordinates, without requiring
manual recipe specification.

Core Innovation: Instead of manually defining:
    "composition": {"core": "add_simple", "guard": "validate_numeric", ...}

We provide only:
    "target_profile": {"L": 0.65, "J": 0.75, "P": 0.55, "W": 0.45}

And the system discovers which composition achieves this profile.
"""

import math
import os
import sys
from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Use unified harmonizer integration
from calculator_components import SOURCES
from harmonizer_integration import PythonCodeHarmonizer as StringHarmonizer


@dataclass
class LJPWProfile:
    """Represents a 4D LJPW semantic profile."""

    L: float
    J: float
    P: float
    W: float

    def distance_to(self, other: "LJPWProfile") -> float:
        """Euclidean distance in 4D LJPW space."""
        return math.sqrt(
            (self.L - other.L) ** 2
            + (self.J - other.J) ** 2
            + (self.P - other.P) ** 2
            + (self.W - other.W) ** 2
        )

    def __repr__(self):
        return f"LJPW(L={self.L:.3f}, J={self.J:.3f}, P={self.P:.3f}, W={self.W:.3f})"


@dataclass
class CompositionRecipe:
    """Represents a composition of atomic components."""

    core: str
    guard: Optional[str] = None
    observer: Optional[str] = None

    def __repr__(self):
        parts = [f"core={self.core}"]
        if self.guard:
            parts.append(f"guard={self.guard}")
        if self.observer:
            parts.append(f"observer={self.observer}")
        return f"Recipe({', '.join(parts)})"

    def to_dict(self):
        """Convert to dictionary format for ComponentComposer."""
        recipe = {"core": self.core}
        if self.guard:
            recipe["guard"] = self.guard
        if self.observer:
            recipe["observer"] = self.observer
        return recipe


class CompositionRuleEngine:
    """
    Understands how LJPW profiles combine when components are composed.

    This is the KEY innovation - we need to predict the emergent LJPW profile
    of a composition WITHOUT actually creating and analyzing it.
    """

    def __init__(self, atomic_profiles: Dict[str, LJPWProfile]):
        self.atomic_profiles = atomic_profiles

    def predict_composition_profile(self, recipe: CompositionRecipe) -> LJPWProfile:
        """
        Predict the emergent LJPW profile of a composition.

        Model v2 - Coupling-Aware Amplification:
        Based on empirical observation that:
        - secure_add (validate + add + log) → L=0.9, J=0.9, P=0.5, W=0.5
        - Components amplify each other through coupling dynamics
        - Love amplifies other dimensions (κ_L→* > 1)
        - Composition creates emergent properties greater than simple sum

        Key insight: Composition doesn't just add - it creates SYNERGY.
        """
        # Get component profiles
        core_profile = self.atomic_profiles.get(recipe.core, LJPWProfile(0, 0, 0, 0))
        guard_profile = (
            self.atomic_profiles.get(recipe.guard, LJPWProfile(0, 0, 0, 0))
            if recipe.guard
            else None
        )
        obs_profile = (
            self.atomic_profiles.get(recipe.observer, LJPWProfile(0, 0, 0, 0))
            if recipe.observer
            else None
        )

        # Start with base from each layer's PRIMARY dimension
        L_base = obs_profile.L if obs_profile else 0.0  # Observer contributes Love
        J_base = guard_profile.J if guard_profile else 0.0  # Guard contributes Justice
        P_base = max(
            core_profile.P, 0.5
        )  # Core contributes Power (assume 0.5 minimum for operations)
        W_base = max(
            core_profile.W,
            guard_profile.W if guard_profile else 0.0,
            obs_profile.W if obs_profile else 0.0,
        )  # Best wisdom from any layer

        # Apply coupling amplification
        # When Love is present, it amplifies Justice and Power (κ_LJ = 1.4, κ_LP = 1.3)
        if obs_profile and obs_profile.L > 0.5:
            love_amplifier = 1.0 + (obs_profile.L - 0.5)  # Amplification factor
            J_base = min(J_base * love_amplifier, 1.0)
            P_base = min(P_base * love_amplifier, 1.0)
            L_base = obs_profile.L  # Love maintains its strength

        # When Justice is present, it supports Wisdom (κ_JW = 1.2)
        if guard_profile and guard_profile.J > 0.5:
            justice_amplifier = 1.0 + (guard_profile.J - 0.5) * 0.5
            W_base = min(W_base * justice_amplifier, 1.0)
            J_base = max(J_base, guard_profile.J)  # Justice maintains its strength

        # Integration bonus: Multiple layers create emergent Wisdom
        num_layers = 1 + (1 if recipe.guard else 0) + (1 if recipe.observer else 0)
        if num_layers >= 3:
            # Full composition (core + guard + observer) = high Wisdom from integration
            W_base = min(W_base + 0.3, 1.0)
        elif num_layers == 2:
            W_base = min(W_base + 0.15, 1.0)

        # When all three layers present, create HARMONY (all dimensions elevated)
        if recipe.guard and recipe.observer:
            # This is the "secure" pattern - elevates all dimensions
            harmony_boost = 0.1
            L_base = min(L_base + harmony_boost, 1.0)
            J_base = min(J_base + harmony_boost, 1.0)
            P_base = min(P_base + harmony_boost, 1.0)
            W_base = min(W_base + harmony_boost, 1.0)

        return LJPWProfile(L_base, J_base, P_base, W_base)


class CompositionSearchEngine:
    """
    Searches the space of possible compositions to find ones that match
    a target LJPW profile.
    """

    def __init__(self, atomic_components: Dict[str, str], harmonizer: StringHarmonizer):
        self.atomic_components = atomic_components
        self.harmonizer = harmonizer
        self.atomic_profiles = self._analyze_atomic_components()
        self.rule_engine = CompositionRuleEngine(self.atomic_profiles)

    def _analyze_atomic_components(self) -> Dict[str, LJPWProfile]:
        """Analyze all atomic components to get their LJPW profiles."""
        print("[ANALYSIS] Analyzing atomic components...")
        profiles = {}

        for name, source in self.atomic_components.items():
            print(f"  - Analyzing '{name}'...")
            report = self.harmonizer.analyze_file_content(source)

            if report:
                func_name = list(report.keys())[0]
                coords = report[func_name]["ice_result"]["ice_components"]["intent"].coordinates
                profiles[name] = LJPWProfile(
                    L=coords.love, J=coords.justice, P=coords.power, W=coords.wisdom
                )
                print(f"    -> {profiles[name]}")
            else:
                print("    -> Analysis failed, using defaults")
                profiles[name] = LJPWProfile(0.0, 0.0, 0.0, 0.0)

        return profiles

    def generate_all_recipes(
        self,
        core_components: List[str],
        guard_components: List[str],
        observer_components: List[str],
    ) -> List[CompositionRecipe]:
        """Generate all possible composition recipes from available components."""
        recipes = []

        # Core only
        for core in core_components:
            recipes.append(CompositionRecipe(core=core))

        # Core + Guard
        for core, guard in product(core_components, guard_components):
            recipes.append(CompositionRecipe(core=core, guard=guard))

        # Core + Observer
        for core, obs in product(core_components, observer_components):
            recipes.append(CompositionRecipe(core=core, observer=obs))

        # Core + Guard + Observer (full composition)
        for core, guard, obs in product(core_components, guard_components, observer_components):
            recipes.append(CompositionRecipe(core=core, guard=guard, observer=obs))

        return recipes

    def search(
        self,
        target_profile: LJPWProfile,
        core_components: List[str],
        guard_components: List[str],
        observer_components: List[str],
        top_k: int = 5,
    ) -> List[Tuple[CompositionRecipe, LJPWProfile, float]]:
        """
        Search for compositions that best match the target profile.

        Returns:
            List of (recipe, predicted_profile, distance) tuples, sorted by distance
        """
        print(f"\n[SEARCH] Searching for compositions matching target: {target_profile}")
        print(f"  - Core candidates: {core_components}")
        print(f"  - Guard candidates: {guard_components}")
        print(f"  - Observer candidates: {observer_components}")

        # Generate all possible recipes
        all_recipes = self.generate_all_recipes(
            core_components, guard_components, observer_components
        )
        print(f"  - Generated {len(all_recipes)} possible recipes")

        # Predict profile for each recipe and calculate distance to target
        results = []
        for recipe in all_recipes:
            predicted_profile = self.rule_engine.predict_composition_profile(recipe)
            distance = predicted_profile.distance_to(target_profile)
            results.append((recipe, predicted_profile, distance))

        # Sort by distance (best matches first)
        results.sort(key=lambda x: x[2])

        return results[:top_k]


def run_experiment():
    """
    Run Experiment C: Composition Discovery

    Test Cases:
    1. Validate known composition (secure_add) - can we predict its profile?
    2. Discover novel compositions for new target profiles
    """
    print("=" * 80)
    print("EXPERIMENT C: COMPOSITION DISCOVERY")
    print("=" * 80)

    harmonizer = StringHarmonizer(quiet=True)

    # Get atomic components from calculator_components
    atomic_components = SOURCES["functions"]

    # Filter to get just the atomic building blocks
    atomic_names = [
        "validate_numeric",
        "log_operation",
        "add_simple",
        "subtract_simple",
        "multiply_simple",
        "divide_simple",
    ]
    atomic_pool = {
        name: atomic_components[name] for name in atomic_names if name in atomic_components
    }

    # Initialize search engine
    search_engine = CompositionSearchEngine(atomic_pool, harmonizer)

    print("\n" + "=" * 80)
    print("TEST 1: Validate Known Composition (secure_add)")
    print("=" * 80)

    # What is the target profile for secure_add based on the DNA?
    # From calculator_dna_fractal.json, we don't have explicit target,
    # but we know the recipe. Let's predict what it SHOULD be.

    known_recipe = CompositionRecipe(
        core="add_simple", guard="validate_numeric", observer="log_operation"
    )

    predicted = search_engine.rule_engine.predict_composition_profile(known_recipe)
    print(f"\nKnown recipe: {known_recipe}")
    print(f"Predicted profile: {predicted}")

    # Now let's analyze the ACTUAL secure_add to compare
    print("\nAnalyzing actual generated secure_add for comparison...")
    secure_add_source = '''
def secure_add(a, b):
    """
    Fractally composed function: secure_add
    Core: add_simple (Power)
    Guard: validate_numeric (Justice)
    Observer: log_operation (Love)
    """
    validate_numeric(a, b)
    result = a + b
    log_operation('secure_add', a, b, result)
    return result
'''

    report = harmonizer.analyze_file_content(secure_add_source)
    if report:
        func_name = list(report.keys())[0]
        actual = report[func_name]["ice_result"]["ice_components"]["intent"].coordinates
        actual_profile = LJPWProfile(
            L=actual.love, J=actual.justice, P=actual.power, W=actual.wisdom
        )
        print(f"Actual profile: {actual_profile}")
        print(f"Prediction error: {predicted.distance_to(actual_profile):.4f}")

    print("\n" + "=" * 80)
    print("TEST 2: Discover Novel Compositions")
    print("=" * 80)

    # Test Case 2a: High Justice, Moderate Power (secure operation)
    target_1 = LJPWProfile(L=0.3, J=0.7, P=0.4, W=0.3)
    print(f"\nTarget Profile 1: {target_1} (High Justice, Moderate Power)")

    results = search_engine.search(
        target_profile=target_1,
        core_components=["add_simple", "subtract_simple", "multiply_simple"],
        guard_components=["validate_numeric"],
        observer_components=["log_operation"],
        top_k=3,
    )

    print("\nTop 3 matches:")
    for i, (recipe, profile, distance) in enumerate(results, 1):
        print(f"\n{i}. {recipe}")
        print(f"   Predicted: {profile}")
        print(f"   Distance: {distance:.4f}")

    # Test Case 2b: High Love, Low Power (observable but simple)
    target_2 = LJPWProfile(L=0.6, J=0.2, P=0.3, W=0.2)
    print(f"\n\nTarget Profile 2: {target_2} (High Love, Low Power)")

    results = search_engine.search(
        target_profile=target_2,
        core_components=["add_simple", "subtract_simple"],
        guard_components=["validate_numeric"],
        observer_components=["log_operation"],
        top_k=3,
    )

    print("\nTop 3 matches:")
    for i, (recipe, profile, distance) in enumerate(results, 1):
        print(f"\n{i}. {recipe}")
        print(f"   Predicted: {profile}")
        print(f"   Distance: {distance:.4f}")

    # Test Case 2c: Balanced profile (all dimensions moderate)
    target_3 = LJPWProfile(L=0.4, J=0.4, P=0.4, W=0.4)
    print(f"\n\nTarget Profile 3: {target_3} (Balanced)")

    results = search_engine.search(
        target_profile=target_3,
        core_components=["add_simple", "multiply_simple"],
        guard_components=["validate_numeric"],
        observer_components=["log_operation"],
        top_k=3,
    )

    print("\nTop 3 matches:")
    for i, (recipe, profile, distance) in enumerate(results, 1):
        print(f"\n{i}. {recipe}")
        print(f"   Predicted: {profile}")
        print(f"   Distance: {distance:.4f}")

    print("\n" + "=" * 80)
    print("EXPERIMENT COMPLETE")
    print("=" * 80)
    print("\nKey Questions:")
    print("1. How accurate is our composition rule model?")
    print("2. Can we discover optimal recipes for arbitrary target profiles?")
    print("3. Do the discovered recipes make semantic sense?")
    print("\nNext Steps:")
    print("- Refine composition rules based on empirical validation")
    print("- Learn rule weights from analyzing many composition examples")
    print("- Integrate discovery into master_grower.py")
    print("=" * 80)


if __name__ == "__main__":
    run_experiment()
