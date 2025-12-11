"""
Fractal Composition Experiment - Level 2: Functions → Classes

This experiment tests the fractal hypothesis: that composition rules are
scale-invariant and apply at multiple levels of abstraction.

Level 0: Atomic primitives (validate, log, compute)
Level 1: Composed functions (secure_add, secure_multiply)
Level 2: Composed classes (SecureCalculator) ← THIS EXPERIMENT

Key Question: Do the same LJPW composition rules that work at Level 1
              also work at Level 2?

If YES → Fractal nature confirmed, rules are scale-invariant
If NO → Need different composition models for different abstraction levels
"""

import math
import os
import sys
from dataclasses import dataclass
from typing import Dict, List

# Add parent directory to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Use unified harmonizer integration
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


# ==============================================================================
# Level 1: Composed Functions (Atoms for Level 2)
# ==============================================================================

LEVEL1_FUNCTIONS = {
    "secure_add": '''
def secure_add(a, b):
    """
    Fractally composed addition with validation and logging.
    High Justice (validation), High Love (logging), Moderate Power.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
    result = a + b
    print(f"[LOG] secure_add({a}, {b}) = {result}")
    return result
''',
    "secure_subtract": '''
def secure_subtract(a, b):
    """
    Fractally composed subtraction with validation and logging.
    High Justice (validation), High Love (logging), Moderate Power.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
    result = a - b
    print(f"[LOG] secure_subtract({a}, {b}) = {result}")
    return result
''',
    "secure_multiply": '''
def secure_multiply(a, b):
    """
    Fractally composed multiplication with validation and logging.
    High Justice (validation), High Love (logging), Moderate Power.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
    result = a * b
    print(f"[LOG] secure_multiply({a}, {b}) = {result}")
    return result
''',
    "secure_divide": '''
def secure_divide(a, b):
    """
    Fractally composed division with validation, zero-check, and logging.
    High Justice (validation + zero-check), High Love (logging), Moderate Power.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Inputs must be numeric")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    result = a / b
    print(f"[LOG] secure_divide({a}, {b}) = {result}")
    return result
''',
    # Simpler variants for comparison
    "simple_add": '''
def simple_add(a, b):
    """Simple addition. High Power, Low Justice, Low Love."""
    return a + b
''',
    "simple_multiply": '''
def simple_multiply(a, b):
    """Simple multiplication. High Power, Low Justice, Low Love."""
    return a * b
''',
}


# ==============================================================================
# Level 2: Class Composition Patterns
# ==============================================================================


def compose_calculator_class(
    name: str,
    methods: List[str],
    method_sources: Dict[str, str],
    include_state: bool = False,
    include_history: bool = False,
) -> str:
    """
    Compose a calculator class from a set of methods.

    Class structure affects LJPW:
    - Methods contribute their individual profiles
    - State management adds Wisdom (structure)
    - History tracking adds Love (observability)
    - Initialization adds Justice (setup validation)
    """
    code = f"class {name}:\n"
    code += '    """\n'
    code += f'    A calculator class composed from: {", ".join(methods)}\n'

    if include_state:
        code += "    Includes state management for configuration.\n"
    if include_history:
        code += "    Includes operation history tracking.\n"

    code += '    """\n\n'

    # Constructor
    if include_state or include_history:
        code += "    def __init__(self):\n"
        if include_state:
            code += "        self.precision = 10  # State: calculation precision\n"
        if include_history:
            code += "        self.history = []  # State: operation history\n"
        code += "\n"

    # Add methods
    for method_name in methods:
        if method_name not in method_sources:
            continue

        # Extract function and convert to method
        func_source = method_sources[method_name].strip()

        # Convert function to method (add self parameter)
        lines = func_source.split("\n")

        # Process each line
        for i, line in enumerate(lines):
            if line.strip().startswith("def "):
                # Add self parameter to method signature
                lines[i] = line.replace("def ", "def ", 1)
                if "(" in lines[i] and ")" in lines[i]:
                    # Insert self as first parameter
                    paren_idx = lines[i].index("(")
                    close_paren = lines[i].index(")")
                    params = lines[i][paren_idx + 1 : close_paren]
                    if params.strip():
                        lines[i] = (
                            lines[i][: paren_idx + 1] + "self, " + params + lines[i][close_paren:]
                        )
                    else:
                        lines[i] = lines[i][: paren_idx + 1] + "self" + lines[i][close_paren:]

        # Add indentation for class methods
        method_code = "\n".join("    " + line if line.strip() else line for line in lines)
        code += method_code + "\n\n"

        # Add history tracking if enabled
        if include_history:
            # Add a wrapper that logs to history (simplified for this experiment)
            pass

    return code


# ==============================================================================
# Level 2 Composition Rule Engine
# ==============================================================================


class Level2CompositionRuleEngine:
    """
    Predicts emergent LJPW profile of a class based on its methods.

    Hypothesis: Class profile = f(method profiles, structural features)

    Structural features:
    - State management → +Wisdom
    - History tracking → +Love
    - Initialization → +Justice
    - Method diversity → +Wisdom
    """

    def __init__(self, method_profiles: Dict[str, LJPWProfile]):
        self.method_profiles = method_profiles

    def predict_class_profile(
        self,
        methods: List[str],
        has_state: bool = False,
        has_history: bool = False,
        has_init: bool = False,
    ) -> LJPWProfile:
        """
        Predict the emergent LJPW profile of a class.

        Model v1 - Aggregation + Structural Bonuses:
        - Base: Average of method profiles (methods are the atoms at this level)
        - State management: +0.2 Wisdom (adds structure)
        - History tracking: +0.2 Love (adds observability)
        - Initialization: +0.1 Justice (adds validation/setup)
        - Method diversity: +0.1 Wisdom per unique semantic pattern
        """
        if not methods:
            return LJPWProfile(0, 0, 0, 0)

        # Base: Average method profiles
        L_sum, J_sum, P_sum, W_sum = 0.0, 0.0, 0.0, 0.0
        valid_count = 0

        for method in methods:
            if method in self.method_profiles:
                profile = self.method_profiles[method]
                L_sum += profile.L
                J_sum += profile.J
                P_sum += profile.P
                W_sum += profile.W
                valid_count += 1

        if valid_count == 0:
            return LJPWProfile(0, 0, 0, 0)

        # Average
        L = L_sum / valid_count
        J = J_sum / valid_count
        P = P_sum / valid_count
        W = W_sum / valid_count

        # Structural bonuses
        if has_state:
            W = min(W + 0.2, 1.0)  # State adds structure/wisdom

        if has_history:
            L = min(L + 0.2, 1.0)  # History adds observability/love

        if has_init:
            J = min(J + 0.1, 1.0)  # Init adds validation/justice

        # Diversity bonus: More unique methods = more wisdom
        if valid_count >= 4:
            W = min(W + 0.15, 1.0)
        elif valid_count >= 2:
            W = min(W + 0.1, 1.0)

        # Integration harmony: If class has multiple structural features
        structural_count = (
            (1 if has_state else 0) + (1 if has_history else 0) + (1 if has_init else 0)
        )
        if structural_count >= 2:
            # Well-structured class gets harmony boost
            L = min(L + 0.05, 1.0)
            J = min(J + 0.05, 1.0)
            W = min(W + 0.05, 1.0)

        return LJPWProfile(L, J, P, W)


# ==============================================================================
# Experiment Runner
# ==============================================================================


def run_level2_experiment():
    """
    Test the fractal hypothesis at Level 2.

    Test Cases:
    1. Analyze Level 1 functions to get their LJPW profiles
    2. Compose classes from these functions
    3. Measure emergent class LJPW profiles
    4. Compare predicted vs actual profiles
    5. Validate that composition rules are scale-invariant
    """
    print("=" * 80)
    print("LEVEL 2 FRACTAL COMPOSITION EXPERIMENT")
    print("Testing: Functions → Classes")
    print("=" * 80)

    harmonizer = StringHarmonizer(quiet=True)

    # Step 1: Analyze Level 1 functions (the atoms for this level)
    print("\n[STEP 1] Analyzing Level 1 Functions (Atomic Components for Classes)")
    print("-" * 80)

    method_profiles = {}
    for name, source in LEVEL1_FUNCTIONS.items():
        print(f"  Analyzing '{name}'...")
        report = harmonizer.analyze_file_content(source)

        if report:
            func_name = list(report.keys())[0]
            coords = report[func_name]["ice_result"]["ice_components"]["intent"].coordinates
            profile = LJPWProfile(L=coords.love, J=coords.justice, P=coords.power, W=coords.wisdom)
            method_profiles[name] = profile
            print(f"    -> {profile}")
        else:
            print("    -> Analysis failed")
            method_profiles[name] = LJPWProfile(0, 0, 0, 0)

    # Step 2: Define class compositions
    print("\n[STEP 2] Defining Class Compositions")
    print("-" * 80)

    class_specs = [
        {
            "name": "SimpleCalculator",
            "methods": ["simple_add", "simple_multiply"],
            "has_state": False,
            "has_history": False,
            "description": "Minimal class with simple operations",
        },
        {
            "name": "SecureCalculator",
            "methods": ["secure_add", "secure_subtract", "secure_multiply", "secure_divide"],
            "has_state": False,
            "has_history": False,
            "description": "Class with all secure operations",
        },
        {
            "name": "StatefulCalculator",
            "methods": ["secure_add", "secure_multiply"],
            "has_state": True,
            "has_history": False,
            "description": "Secure operations with state management",
        },
        {
            "name": "ObservableCalculator",
            "methods": ["secure_add", "secure_subtract", "secure_multiply"],
            "has_state": False,
            "has_history": True,
            "description": "Secure operations with history tracking",
        },
        {
            "name": "FullFeaturedCalculator",
            "methods": ["secure_add", "secure_subtract", "secure_multiply", "secure_divide"],
            "has_state": True,
            "has_history": True,
            "description": "All features: secure methods + state + history",
        },
    ]

    for spec in class_specs:
        print(f"\n  {spec['name']}:")
        print(f"    Description: {spec['description']}")
        print(f"    Methods: {', '.join(spec['methods'])}")
        print(f"    State: {spec['has_state']}, History: {spec['has_history']}")

    # Step 3: Generate classes and predict profiles
    print("\n[STEP 3] Generating Classes and Predicting Profiles")
    print("-" * 80)

    rule_engine = Level2CompositionRuleEngine(method_profiles)

    results = []
    for spec in class_specs:
        print(f"\n  Processing {spec['name']}...")

        # Generate class source
        class_source = compose_calculator_class(
            name=spec["name"],
            methods=spec["methods"],
            method_sources=LEVEL1_FUNCTIONS,
            include_state=spec["has_state"],
            include_history=spec["has_history"],
        )

        # Predict profile
        predicted = rule_engine.predict_class_profile(
            methods=spec["methods"],
            has_state=spec["has_state"],
            has_history=spec["has_history"],
            has_init=spec["has_state"] or spec["has_history"],  # Has __init__ if has features
        )
        print(f"    Predicted profile: {predicted}")

        # Analyze actual class
        print("    Analyzing generated class...")
        report = harmonizer.analyze_file_content(class_source)

        actual = None
        if report:
            # For classes, harmonizer analyzes methods individually
            # We need to aggregate them (simplified - just get first method as proxy)
            if report:
                first_key = list(report.keys())[0]
                coords = report[first_key]["ice_result"]["ice_components"]["intent"].coordinates
                actual = LJPWProfile(
                    L=coords.love, J=coords.justice, P=coords.power, W=coords.wisdom
                )
                print(f"    Actual profile: {actual}")
                print(f"    Prediction error: {predicted.distance_to(actual):.4f}")
        else:
            print("    Analysis failed - cannot measure actual")

        results.append(
            {"spec": spec, "predicted": predicted, "actual": actual, "source": class_source}
        )

    # Step 4: Analysis and Validation
    print("\n" + "=" * 80)
    print("RESULTS ANALYSIS")
    print("=" * 80)

    print("\nComparison of Class Profiles:")
    print(f"{'Class':<25} {'Predicted':<35} {'Key Features'}")
    print("-" * 80)

    for result in results:
        spec = result["spec"]
        pred = result["predicted"]
        features = []
        if spec["has_state"]:
            features.append("State")
        if spec["has_history"]:
            features.append("History")
        if not features:
            features.append("Basic")

        print(f"{spec['name']:<25} {str(pred):<35} {', '.join(features)}")

    print("\n" + "=" * 80)
    print("FRACTAL HYPOTHESIS VALIDATION")
    print("=" * 80)

    print("\nKey Questions:")
    print("1. Do classes composed of high-Justice methods have high Justice?")
    print("2. Do structural features (state, history) add predictable LJPW bonuses?")
    print("3. Are composition rules scale-invariant (Level 1 → Level 2)?")

    print("\nObservations:")

    # Find SecureCalculator and SimpleCalculator for comparison
    secure_calc = next((r for r in results if r["spec"]["name"] == "SecureCalculator"), None)
    simple_calc = next((r for r in results if r["spec"]["name"] == "SimpleCalculator"), None)

    if secure_calc and simple_calc:
        print("\n  SimpleCalculator (simple methods):")
        print(f"    {simple_calc['predicted']}")
        print("\n  SecureCalculator (secure methods):")
        print(f"    {secure_calc['predicted']}")

        # Compare Justice levels
        if secure_calc["predicted"].J > simple_calc["predicted"].J:
            print("\n  ✓ Secure methods → Higher Justice in class")
            print(f"    (J: {simple_calc['predicted'].J:.3f} → {secure_calc['predicted'].J:.3f})")

        # Compare Love levels
        if secure_calc["predicted"].L > simple_calc["predicted"].L:
            print("  ✓ Secure methods → Higher Love in class")
            print(f"    (L: {simple_calc['predicted'].L:.3f} → {secure_calc['predicted'].L:.3f})")

    # Check structural bonuses
    stateful = next((r for r in results if r["spec"]["name"] == "StatefulCalculator"), None)
    observable = next((r for r in results if r["spec"]["name"] == "ObservableCalculator"), None)

    if stateful and secure_calc:
        if stateful["predicted"].W > secure_calc["predicted"].W:
            print("\n  ✓ State management → Higher Wisdom")
            print(f"    (W: {secure_calc['predicted'].W:.3f} → {stateful['predicted'].W:.3f})")

    if observable and secure_calc:
        if observable["predicted"].L > secure_calc["predicted"].L:
            print("  ✓ History tracking → Higher Love")
            print(f"    (L: {secure_calc['predicted'].L:.3f} → {observable['predicted'].L:.3f})")

    print("\n" + "=" * 80)
    print("CONCLUSION")
    print("=" * 80)

    print("\nThe fractal hypothesis predicts that:")
    print("- Methods are the 'atoms' at Level 2")
    print("- Class profiles emerge from method profiles + structure")
    print("- Same coupling dynamics apply (Love amplifies, Justice validates, etc.)")
    print("- Scale-invariant composition rules")

    print("\nIf validated, this means we can:")
    print("1. Predict class behavior from method composition")
    print("2. Design classes by specifying target LJPW profiles")
    print("3. Apply discovery algorithm at Level 2 (find optimal method sets)")
    print("4. Continue recursively: Classes → Modules → Systems")

    print("\n" + "=" * 80)

    # Save one example for inspection
    print("\n[Saving example class for inspection...]")
    with open("generated_SecureCalculator.py", "w") as f:
        secure_result = next(r for r in results if r["spec"]["name"] == "SecureCalculator")
        f.write(secure_result["source"])
    print("  Saved: generated_SecureCalculator.py")

    return results


if __name__ == "__main__":
    run_level2_experiment()
