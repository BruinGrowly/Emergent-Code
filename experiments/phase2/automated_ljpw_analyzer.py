"""
Automated LJPW Code Quality Analyzer

Fully automated analysis combining:
1. Harmonizer semantic analysis (function name intent)
2. AST pattern recognition (implementation quality)
3. Combined LJPW scoring without manual assessment

Usage:
    analyzer = AutomatedLJPWAnalyzer()
    result = analyzer.analyze_code(code_string)
    print(f"Harmony: {result['harmony']:.2f}")
"""

import ast
import re
import sys
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from harmonizer_integration import PythonCodeHarmonizer


@dataclass
class LJPWScore:
    """LJPW scores with breakdown."""
    love: float
    justice: float
    power: float
    wisdom: float
    harmony: float

    # Detailed breakdowns
    love_semantic: float = 0.0
    love_implementation: float = 0.0
    justice_semantic: float = 0.0
    justice_implementation: float = 0.0
    power_semantic: float = 0.0
    power_implementation: float = 0.0
    wisdom_semantic: float = 0.0
    wisdom_implementation: float = 0.0

    # Pattern details
    patterns: Dict[str, int] = None

    def __post_init__(self):
        if self.patterns is None:
            self.patterns = {}


class ImplementationPatternAnalyzer:
    """Analyze code patterns to assess implementation quality."""

    def __init__(self):
        pass

    def analyze(self, code: str) -> Dict[str, float]:
        # Auto-healed: Input validation for analyze
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        """
        Analyze implementation patterns and return LJPW scores.

        Returns:
            Dict with L, J, P, W scores (0.0-1.0) and pattern counts
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0, 'patterns': {}}

        patterns = self._extract_patterns(tree, code)
        scores = self._calculate_scores(patterns, code)

        return {
            'L': scores['love'],
            'J': scores['justice'],
            'P': scores['power'],
            'W': scores['wisdom'],
            'patterns': patterns
        }

    def _extract_patterns(self, tree: ast.AST, code: str) -> Dict[str, int]:
        """Extract implementation patterns from AST and code."""
        patterns = {
            # Love indicators
            'docstrings': 0,
            'type_hints': 0,
            'logging_calls': 0,
            'comments': 0,
            'descriptive_names': 0,
            'total_names': 0,

            # Justice indicators
            'try_except': 0,
            'assertions': 0,
            'validations': 0,
            'if_checks': 0,
            'raises': 0,

            # Power indicators
            'dict_usage': 0,
            'list_comprehensions': 0,
            'generators': 0,
            'builtin_optimizations': 0,
            'nested_loops': 0,
            'linear_searches': 0,

            # Wisdom indicators
            'classes': 0,
            'functions': 0,
            'constants': 0,
            'global_vars': 0,
            'magic_numbers': 0,
            'decorators': 0,
        }

        # Walk the AST
        for node in ast.walk(tree):
            # Love: Docstrings
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if ast.get_docstring(node):
                    patterns['docstrings'] += 1

            # Love: Type hints
            if isinstance(node, ast.FunctionDef):
                patterns['functions'] += 1
                if node.returns is not None:
                    patterns['type_hints'] += 1
                for arg in node.args.args:
                    if arg.annotation is not None:
                        patterns['type_hints'] += 1

            # Love: Descriptive names
            if isinstance(node, ast.Name):
                patterns['total_names'] += 1
                if len(node.id) > 2 and not node.id.isupper():
                    patterns['descriptive_names'] += 1

            # Justice: Error handling
            if isinstance(node, ast.Try):
                patterns['try_except'] += 1
            if isinstance(node, ast.Assert):
                patterns['assertions'] += 1
            if isinstance(node, ast.Raise):
                patterns['raises'] += 1
            if isinstance(node, ast.If):
                patterns['if_checks'] += 1

            # Power: Data structures
            if isinstance(node, ast.Dict):
                patterns['dict_usage'] += 1
            if isinstance(node, (ast.ListComp, ast.DictComp, ast.SetComp)):
                patterns['list_comprehensions'] += 1
            if isinstance(node, ast.GeneratorExp):
                patterns['generators'] += 1

            # Power: Nested loops (inefficiency indicator)
            if isinstance(node, ast.For):
                # Check if inside another loop
                for parent in ast.walk(tree):
                    if isinstance(parent, ast.For) and node in ast.walk(parent):
                        if parent != node:
                            patterns['nested_loops'] += 1
                            break

            # Wisdom: Structure
            if isinstance(node, ast.ClassDef):
                patterns['classes'] += 1
                # Check for decorators
                if node.decorator_list:
                    patterns['decorators'] += len(node.decorator_list)

            # Wisdom: Global variables (anti-pattern)
            if isinstance(node, ast.Global):
                patterns['global_vars'] += len(node.names)

            # Wisdom: Constants (UPPER_CASE assignments at module level)
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id.isupper() and len(target.id) > 1:
                            patterns['constants'] += 1

            # Wisdom: Magic numbers
            if isinstance(node, ast.Num):
                if not isinstance(node.n, (bool, type(None))):
                    if node.n not in (0, 1, -1):  # Common non-magic numbers
                        patterns['magic_numbers'] += 1

        # Love: Logging (pattern matching in code)
        patterns['logging_calls'] = len(re.findall(r'\b(logger\.|logging\.|print\()', code))

        # Love: Comments
        patterns['comments'] = len(re.findall(r'#.*$', code, re.MULTILINE))

        # Justice: Validation patterns
        validation_patterns = [
            r'\bif\s+not\s+\w+',
            r'\bif\s+\w+\s+is\s+None',
            r'\bif\s+len\(',
            r'\braise\s+ValueError',
            r'\braise\s+\w+Error',
        ]
        for pattern in validation_patterns:
            patterns['validations'] += len(re.findall(pattern, code))

        # Power: Linear searches (anti-pattern)
        patterns['linear_searches'] = len(re.findall(r'for\s+\w+\s+in\s+\w+:\s*\n\s*if\s+', code))

        return patterns

    def _calculate_scores(self, patterns: Dict[str, int], code: str) -> Dict[str, float]:
        """Calculate LJPW scores from patterns."""

        # Get code metrics
        lines = len([l for l in code.split('\n') if l.strip()])
        functions = max(patterns['functions'], 1)

        # LOVE: Documentation, clarity, observability
        love_score = 0.0

        # Docstrings (0-0.3)
        docstring_ratio = min(patterns['docstrings'] / functions, 1.0)
        love_score += docstring_ratio * 0.3

        # Type hints (0-0.2)
        type_hint_ratio = min(patterns['type_hints'] / (functions * 3), 1.0)  # ~3 hints per function
        love_score += type_hint_ratio * 0.2

        # Logging (0-0.2)
        logging_ratio = min(patterns['logging_calls'] / functions, 1.0)
        love_score += logging_ratio * 0.2

        # Comments (0-0.15)
        comment_ratio = min(patterns['comments'] / (lines / 10), 1.0)  # ~1 comment per 10 lines
        love_score += comment_ratio * 0.15

        # Descriptive names (0-0.15)
        if patterns['total_names'] > 0:
            name_quality = patterns['descriptive_names'] / patterns['total_names']
            love_score += name_quality * 0.15

        # JUSTICE: Validation, error handling, correctness
        justice_score = 0.0

        # Error handling (0-0.4)
        error_handling_ratio = min(patterns['try_except'] / functions, 1.0)
        justice_score += error_handling_ratio * 0.4

        # Validation (0-0.3)
        validation_ratio = min(patterns['validations'] / functions, 1.0)
        justice_score += validation_ratio * 0.3

        # Assertions and raises (0-0.2)
        assertion_ratio = min((patterns['assertions'] + patterns['raises']) / functions, 1.0)
        justice_score += assertion_ratio * 0.2

        # Conditional checks (0-0.1)
        check_ratio = min(patterns['if_checks'] / (functions * 2), 1.0)
        justice_score += check_ratio * 0.1

        # POWER: Efficiency, performance
        power_score = 0.5  # Start at 0.5 (neutral)

        # Good patterns (add up to +0.3)
        dict_ratio = min(patterns['dict_usage'] / functions, 1.0)
        power_score += dict_ratio * 0.15

        comprehension_ratio = min(patterns['list_comprehensions'] / functions, 1.0)
        power_score += comprehension_ratio * 0.1

        generator_ratio = min(patterns['generators'] / functions, 1.0)
        power_score += generator_ratio * 0.05

        # Bad patterns (subtract up to -0.3)
        if patterns['nested_loops'] > 0:
            power_score -= min(patterns['nested_loops'] / functions, 1.0) * 0.2

        if patterns['linear_searches'] > 0:
            power_score -= min(patterns['linear_searches'] / functions, 1.0) * 0.1

        power_score = max(0.0, min(1.0, power_score))  # Clamp to [0, 1]

        # WISDOM: Architecture, design, structure
        wisdom_score = 0.5  # Start at 0.5 (neutral)

        # Good patterns (add up to +0.5)
        if patterns['classes'] > 0:
            wisdom_score += min(patterns['classes'] / 3, 1.0) * 0.2  # Classes indicate structure

        if patterns['constants'] > 0:
            wisdom_score += min(patterns['constants'] / 5, 1.0) * 0.15  # Constants good

        if patterns['decorators'] > 0:
            wisdom_score += min(patterns['decorators'] / 3, 1.0) * 0.1  # Decorators show patterns

        function_ratio = patterns['functions'] / max(lines / 20, 1)  # ~1 function per 20 lines
        wisdom_score += min(function_ratio, 1.0) * 0.05

        # Bad patterns (subtract up to -0.5)
        if patterns['global_vars'] > 0:
            wisdom_score -= min(patterns['global_vars'] / 3, 1.0) * 0.3  # Global state bad

        if patterns['magic_numbers'] > 0:
            wisdom_score -= min(patterns['magic_numbers'] / 10, 1.0) * 0.2  # Magic numbers bad

        wisdom_score = max(0.0, min(1.0, wisdom_score))  # Clamp to [0, 1]

        return {
            'love': love_score,
            'justice': justice_score,
            'power': power_score,
            'wisdom': wisdom_score
        }


class AutomatedLJPWAnalyzer:
    """Fully automated LJPW code quality analyzer."""

    def __init__(self, quiet: bool = True):
        """Initialize analyzer with harmonizer and pattern analyzer."""
        self.harmonizer = PythonCodeHarmonizer(quiet=quiet)
        self.pattern_analyzer = ImplementationPatternAnalyzer()
        self.quiet = quiet

    def analyze_code(self, code: str) -> LJPWScore:
        """
        Perform complete automated LJPW analysis.

        Args:
            code: Python code to analyze

        Returns:
            LJPWScore with complete breakdown
        """
        if not self.quiet:
            print("🔍 Analyzing code with automated LJPW analyzer...")

        # 1. Semantic analysis (Harmonizer)
        semantic_result = self._analyze_semantics(code)

        # 2. Implementation analysis (Pattern recognition)
        impl_result = self.pattern_analyzer.analyze(code)

        # 3. Combine scores
        L = (semantic_result['L'] + impl_result['L']) / 2
        J = (semantic_result['J'] + impl_result['J']) / 2
        P = (semantic_result['P'] + impl_result['P']) / 2
        W = (semantic_result['W'] + impl_result['W']) / 2
        H = (L * J * P * W) ** 0.25

        return LJPWScore(
            love=L,
            justice=J,
            power=P,
            wisdom=W,
            harmony=H,
            love_semantic=semantic_result['L'],
            love_implementation=impl_result['L'],
            justice_semantic=semantic_result['J'],
            justice_implementation=impl_result['J'],
            power_semantic=semantic_result['P'],
            power_implementation=impl_result['P'],
            wisdom_semantic=semantic_result['W'],
            wisdom_implementation=impl_result['W'],
            patterns=impl_result['patterns']
        )

    def _analyze_semantics(self, code: str) -> Dict[str, float]:
        """Analyze semantic meaning using harmonizer."""
        try:
            result = self.harmonizer.analyze_file_content(code)
        except Exception as e:
            if not self.quiet:
                print(f"⚠️  Harmonizer error: {e}")
            return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}

        # Extract LJPW from all functions
        scores = []
        for func_name, func_data in result.items():
            if 'ice_result' in func_data and 'ice_components' in func_data['ice_result']:
                intent = func_data['ice_result']['ice_components']['intent']
                coords = intent.coordinates
                scores.append({
                    'L': coords.love,
                    'J': coords.justice,
                    'P': coords.power,
                    'W': coords.wisdom
                })

        # Average across all functions
        if scores:
            return {
                'L': sum(s['L'] for s in scores) / len(scores),
                'J': sum(s['J'] for s in scores) / len(scores),
                'P': sum(s['P'] for s in scores) / len(scores),
                'W': sum(s['W'] for s in scores) / len(scores)
            }

        return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}

    def print_detailed_report(self, score: LJPWScore, code: str):
        # Auto-healed: Input validation for print_detailed_report
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        """Print detailed analysis report."""
        lines = len([l for l in code.split('\n') if l.strip()])

        print("\n" + "=" * 80)
        print("AUTOMATED LJPW ANALYSIS REPORT")
        print("=" * 80)

        print(f"\n📊 CODE METRICS:")
        print(f"  Lines of code: {lines}")
        print(f"  Functions: {score.patterns.get('functions', 0)}")
        print(f"  Classes: {score.patterns.get('classes', 0)}")

        print(f"\n🎯 LJPW SCORES:")
        print("-" * 80)

        self._print_dimension("LOVE", score.love, score.love_semantic, score.love_implementation)
        print("    💡 Observability, clarity, developer experience")
        print(f"    • Docstrings: {score.patterns.get('docstrings', 0)}")
        print(f"    • Type hints: {score.patterns.get('type_hints', 0)}")
        print(f"    • Logging calls: {score.patterns.get('logging_calls', 0)}")
        print(f"    • Comments: {score.patterns.get('comments', 0)}")

        self._print_dimension("JUSTICE", score.justice, score.justice_semantic, score.justice_implementation)
        print("    ⚖️  Correctness, validation, error handling")
        print(f"    • Try/except blocks: {score.patterns.get('try_except', 0)}")
        print(f"    • Validations: {score.patterns.get('validations', 0)}")
        print(f"    • Assertions: {score.patterns.get('assertions', 0)}")
        print(f"    • Raises: {score.patterns.get('raises', 0)}")

        self._print_dimension("POWER", score.power, score.power_semantic, score.power_implementation)
        print("    ⚡ Efficiency, performance, capability")
        print(f"    • Dictionary usage: {score.patterns.get('dict_usage', 0)}")
        print(f"    • Comprehensions: {score.patterns.get('list_comprehensions', 0)}")
        print(f"    • Generators: {score.patterns.get('generators', 0)}")
        print(f"    • Nested loops (anti-pattern): {score.patterns.get('nested_loops', 0)}")

        self._print_dimension("WISDOM", score.wisdom, score.wisdom_semantic, score.wisdom_implementation)
        print("    🧠 Architecture, design, structure")
        print(f"    • Classes: {score.patterns.get('classes', 0)}")
        print(f"    • Constants: {score.patterns.get('constants', 0)}")
        print(f"    • Decorators: {score.patterns.get('decorators', 0)}")
        print(f"    • Global vars (anti-pattern): {score.patterns.get('global_vars', 0)}")
        print(f"    • Magic numbers (anti-pattern): {score.patterns.get('magic_numbers', 0)}")

        print(f"\n🌟 HARMONY: {score.harmony:.2f}", end="")
        if score.harmony > 0.6:
            print("  ✅ AUTOPOIETIC (self-sustaining)")
        elif score.harmony > 0.5:
            print("  ⚠️  HOMEOSTATIC (stable)")
        else:
            print("  ❌ ENTROPIC (needs improvement)")

        print("\n" + "=" * 80)

    def _print_dimension(self, name: str, total: float, semantic: float, implementation: float):
        """Print dimension with breakdown."""
        status = "✅" if total > 0.6 else ("⚠️" if total > 0.4 else "❌")
        print(f"\n  {name}: {total:.2f} {status}")
        print(f"    - Semantic (names): {semantic:.2f}")
        print(f"    - Implementation (patterns): {implementation:.2f}")


# ==============================================================================
# DEMO / TEST
# ==============================================================================

def demo():
    """Demonstrate automated analyzer."""

    # Test 1: Messy code
    messy_code = '''
# Messy code
users = []
orders = []

def r(u, p):
    users.append({'u': u, 'p': p})
    return True

def co(uid, items):
    total = 0
    for i in items:
        total += i['price'] * i['qty']
    if total > 100:
        total = total * 0.9
    orders.append({'uid': uid, 'total': total})
    return total

def gu(uid):
    for u in users:
        if u['u'] == uid:
            return u
    return None
'''

    # Test 2: Clean code
    clean_code = '''
"""User and order management system."""

from typing import List, Optional
from dataclasses import dataclass
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Constants
DISCOUNT_THRESHOLD = Decimal("100.00")
DISCOUNT_RATE = Decimal("0.10")


@dataclass
class User:
    """User account."""
    user_id: str
    email: str

    def __post_init__(self):
        """Validate user data."""
        if not self.email or '@' not in self.email:
            raise ValueError("Invalid email")


@dataclass
class Order:
    """Customer order."""
    order_id: str
    user_id: str
    total: Decimal


class UserRepository:
    """Manage user persistence."""

    def __init__(self):
        self._users = {}
        logger.info("UserRepository initialized")

    def save(self, user: User) -> None:
        """Save user."""
        if not user.user_id:
            raise ValueError("User ID required")
        self._users[user.user_id] = user
        logger.info(f"User saved: {user.user_id}")

    def find_by_id(self, user_id: str) -> Optional[User]:
        """Find user by ID."""
        return self._users.get(user_id)


class OrderService:
    """Process orders."""

    def __init__(self):
        self._orders = {}
        logger.info("OrderService initialized")

    def create_order(
        self,
        user_id: str,
        items: List[dict]
    ) -> Order:
        """Create order with discount calculation."""
        logger.info(f"Creating order for user {user_id}")

        # Validate inputs
        if not items:
            raise ValueError("Order must have items")

        # Calculate total
        subtotal = sum(
            Decimal(str(item['price'])) * item['qty']
            for item in items
        )

        # Apply discount
        if subtotal > DISCOUNT_THRESHOLD:
            discount = subtotal * DISCOUNT_RATE
            total = subtotal - discount
            logger.info(f"Discount applied: {discount}")
        else:
            total = subtotal

        # Create order
        order = Order(
            order_id=f"ORD-{len(self._orders)}",
            user_id=user_id,
            total=total
        )

        self._orders[order.order_id] = order
        logger.info(f"Order created: {order.order_id}")

        return order
'''

    analyzer = AutomatedLJPWAnalyzer(quiet=True)

    print("╔" + "=" * 78 + "╗")
    print("║" + "AUTOMATED LJPW ANALYZER DEMO".center(78) + "║")
    print("╚" + "=" * 78 + "╝")

    # Analyze messy code
    print("\n\n" + "🔴 MESSY CODE ANALYSIS")
    messy_score = analyzer.analyze_code(messy_code)
    analyzer.print_detailed_report(messy_score, messy_code)

    # Analyze clean code
    print("\n\n" + "🟢 CLEAN CODE ANALYSIS")
    clean_score = analyzer.analyze_code(clean_code)
    analyzer.print_detailed_report(clean_score, clean_code)

    # Comparison
    print("\n\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)

    print(f"\n  {'Dimension':<15} {'Messy':>10} {'Clean':>10} {'Improvement':>15}")
    print("-" * 80)

    for dim, messy_val, clean_val in [
        ("Love", messy_score.love, clean_score.love),
        ("Justice", messy_score.justice, clean_score.justice),
        ("Power", messy_score.power, clean_score.power),
        ("Wisdom", messy_score.wisdom, clean_score.wisdom),
        ("Harmony", messy_score.harmony, clean_score.harmony),
    ]:
        if messy_val > 0:
            improvement = ((clean_val - messy_val) / messy_val) * 100
        else:
            improvement = float('inf')

        imp_str = "∞%" if improvement == float('inf') else f"{improvement:+.0f}%"
        print(f"  {dim:<15} {messy_val:>10.2f} {clean_val:>10.2f} {imp_str:>15}")

    print("\n✨ Fully automated analysis complete!")
    print("   No manual assessment required - harmonizer + pattern recognition!")


if __name__ == "__main__":
    demo()
