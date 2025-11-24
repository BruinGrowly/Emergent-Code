"""
Enhanced LJPW Analyzer with Advanced Metrics

Adds sophisticated pattern detection:
1. Cyclomatic Complexity - Measures code complexity
2. Coupling Metrics - Analyzes dependencies between modules/classes
3. Cohesion Metrics - Measures internal coherence of classes/modules
4. Dependency Analysis - Tracks import patterns and external dependencies

These metrics enhance the Power and Wisdom dimensions significantly.
"""

import ast
import re
import sys
import os
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from harmonizer_integration import PythonCodeHarmonizer


@dataclass
class ComplexityMetrics:
    """Cyclomatic complexity metrics."""
    total_complexity: int = 0
    avg_complexity: float = 0.0
    max_complexity: int = 0
    high_complexity_functions: List[Tuple[str, int]] = field(default_factory=list)

    # Thresholds
    SIMPLE_THRESHOLD = 10
    COMPLEX_THRESHOLD = 20
    VERY_COMPLEX_THRESHOLD = 50


@dataclass
class CouplingMetrics:
    """Coupling metrics between modules/classes."""
    total_imports: int = 0
    external_dependencies: Set[str] = field(default_factory=set)
    internal_references: int = 0
    fan_out: int = 0  # Number of other modules this depends on
    fan_in: int = 0   # Number of modules that depend on this
    coupling_score: float = 0.0  # 0-1, lower is better


@dataclass
class CohesionMetrics:
    """Cohesion metrics for classes."""
    avg_cohesion: float = 0.0
    low_cohesion_classes: List[str] = field(default_factory=list)
    lcom_score: float = 0.0  # Lack of Cohesion of Methods


@dataclass
class DependencyMetrics:
    """Dependency analysis metrics."""
    stdlib_imports: Set[str] = field(default_factory=set)
    third_party_imports: Set[str] = field(default_factory=set)
    local_imports: Set[str] = field(default_factory=set)
    circular_dependencies: List[Tuple[str, str]] = field(default_factory=list)
    dependency_depth: int = 0


@dataclass
class EnhancedLJPWScore:
    """Enhanced LJPW scores with advanced metrics."""
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

    # Enhanced metrics
    complexity: ComplexityMetrics = None
    coupling: CouplingMetrics = None
    cohesion: CohesionMetrics = None
    dependencies: DependencyMetrics = None

    # Pattern details
    patterns: Dict[str, int] = None

    def __post_init__(self):
        if self.patterns is None:
            self.patterns = {}
        if self.complexity is None:
            self.complexity = ComplexityMetrics()
        if self.coupling is None:
            self.coupling = CouplingMetrics()
        if self.cohesion is None:
            self.cohesion = CohesionMetrics()
        if self.dependencies is None:
            self.dependencies = DependencyMetrics()


class CyclomaticComplexityAnalyzer(ast.NodeVisitor):
    """Calculate cyclomatic complexity using AST."""

    def __init__(self):
        self.function_complexity = {}
        self.current_function = None
        self.complexity = 0

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        # Save previous function state
        prev_function = self.current_function
        prev_complexity = self.complexity

        # Start new function
        self.current_function = node.name
        self.complexity = 1  # Start at 1

        # Visit function body
        self.generic_visit(node)

        # Save complexity
        self.function_complexity[node.name] = self.complexity

        # Restore previous state
        self.current_function = prev_function
        self.complexity = prev_complexity

    def visit_If(self, node):
        """If statement adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        """For loop adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        """While loop adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        """Except handler adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        """With statement adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_Assert(self, node):
        """Assert adds 1 to complexity."""
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        """Boolean operators (and/or) add to complexity."""
        if isinstance(node.op, ast.And) or isinstance(node.op, ast.Or):
            self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def analyze(self, tree: ast.AST) -> ComplexityMetrics:
        """Analyze complexity and return metrics."""
        self.visit(tree)

        if not self.function_complexity:
            return ComplexityMetrics()

        total = sum(self.function_complexity.values())
        avg = total / len(self.function_complexity)
        max_comp = max(self.function_complexity.values())

        # Find high complexity functions
        high_complexity = [
            (name, comp) for name, comp in self.function_complexity.items()
            if comp > ComplexityMetrics.SIMPLE_THRESHOLD
        ]
        high_complexity.sort(key=lambda x: x[1], reverse=True)

        return ComplexityMetrics(
            total_complexity=total,
            avg_complexity=avg,
            max_complexity=max_comp,
            high_complexity_functions=high_complexity[:5]
        )


class CouplingAnalyzer(ast.NodeVisitor):
    """Analyze coupling between modules and classes."""

    def __init__(self):
        self.imports = set()
        self.from_imports = set()
        self.class_dependencies = defaultdict(set)
        self.function_calls = set()

    def visit_Import(self, node):
        """Track import statements."""
        for alias in node.names:
            self.imports.add(alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Track from...import statements."""
        if node.module:
            self.from_imports.add(node.module.split('.')[0])
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Track class dependencies (base classes)."""
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.class_dependencies[node.name].add(base.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        """Track function/method calls."""
        if isinstance(node.func, ast.Name):
            self.function_calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                self.function_calls.add(f"{node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)

    def analyze(self, tree: ast.AST) -> CouplingMetrics:
        """Analyze coupling and return metrics."""
        self.visit(tree)

        # Categorize imports
        stdlib = {'os', 'sys', 're', 'ast', 'json', 'datetime', 'time', 'math',
                  'random', 'collections', 'itertools', 'functools', 'typing',
                  'pathlib', 'logging', 'dataclasses', 'enum', 'decimal'}

        external = self.imports.union(self.from_imports) - stdlib
        total_imports = len(self.imports) + len(self.from_imports)

        # Calculate fan-out (dependencies)
        fan_out = len(self.imports.union(self.from_imports))

        # Calculate coupling score (0-1, lower is better)
        # High coupling = many external dependencies
        if fan_out == 0:
            coupling_score = 0.0
        else:
            # Normalize: 0 imports = 0.0, 20+ imports = 1.0
            coupling_score = min(fan_out / 20.0, 1.0)

        return CouplingMetrics(
            total_imports=total_imports,
            external_dependencies=external,
            internal_references=len(self.class_dependencies),
            fan_out=fan_out,
            coupling_score=coupling_score
        )


class CohesionAnalyzer(ast.NodeVisitor):
    """Analyze cohesion within classes (LCOM - Lack of Cohesion of Methods)."""

    def __init__(self):
        self.classes = {}
        self.current_class = None

    def visit_ClassDef(self, node):
        """Analyze class cohesion."""
        self.current_class = node.name
        self.classes[node.name] = {
            'methods': [],
            'attributes': set(),
            'method_attributes': defaultdict(set)
        }

        # Visit class body
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_name = item.name
                self.classes[node.name]['methods'].append(method_name)

                # Find attributes accessed by this method
                for subnode in ast.walk(item):
                    if isinstance(subnode, ast.Attribute):
                        if isinstance(subnode.value, ast.Name) and subnode.value.id == 'self':
                            attr = subnode.attr
                            self.classes[node.name]['attributes'].add(attr)
                            self.classes[node.name]['method_attributes'][method_name].add(attr)

        self.current_class = None
        self.generic_visit(node)

    def analyze(self, tree: ast.AST) -> CohesionMetrics:
        """Calculate LCOM (Lack of Cohesion of Methods)."""
        self.visit(tree)

        if not self.classes:
            return CohesionMetrics()

        cohesion_scores = []
        low_cohesion = []

        for class_name, data in self.classes.items():
            methods = data['methods']
            attributes = data['attributes']
            method_attrs = data['method_attributes']

            if len(methods) <= 1 or len(attributes) == 0:
                # Single method or no attributes - perfect cohesion
                cohesion_scores.append(1.0)
                continue

            # Calculate LCOM: pairs of methods that don't share attributes
            shared_pairs = 0
            total_pairs = 0

            for i, m1 in enumerate(methods):
                for m2 in methods[i+1:]:
                    total_pairs += 1
                    # Check if methods share any attributes
                    if method_attrs[m1] & method_attrs[m2]:
                        shared_pairs += 1

            if total_pairs == 0:
                cohesion = 1.0
            else:
                # Cohesion = shared pairs / total pairs
                cohesion = shared_pairs / total_pairs

            cohesion_scores.append(cohesion)

            # Flag low cohesion classes (< 0.5)
            if cohesion < 0.5:
                low_cohesion.append(class_name)

        avg_cohesion = sum(cohesion_scores) / len(cohesion_scores) if cohesion_scores else 1.0

        return CohesionMetrics(
            avg_cohesion=avg_cohesion,
            low_cohesion_classes=low_cohesion,
            lcom_score=1.0 - avg_cohesion  # Lack of cohesion
        )


class DependencyAnalyzer(ast.NodeVisitor):
    """Analyze dependency patterns."""

    def __init__(self):
        self.stdlib = {'os', 'sys', 're', 'ast', 'json', 'datetime', 'time',
                      'math', 'random', 'collections', 'itertools', 'functools',
                      'typing', 'pathlib', 'logging', 'dataclasses', 'enum',
                      'decimal', 'uuid', 'hashlib', 'secrets', 'copy', 'io'}

        self.imports = set()
        self.from_imports = set()

    def visit_Import(self, node):
        """Track import statements."""
        for alias in node.names:
            module = alias.name.split('.')[0]
            self.imports.add(module)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Track from...import statements."""
        if node.module:
            module = node.module.split('.')[0]
            self.from_imports.add(module)
        self.generic_visit(node)

    def analyze(self, tree: ast.AST) -> DependencyMetrics:
        """Analyze dependencies."""
        self.visit(tree)

        all_imports = self.imports.union(self.from_imports)

        stdlib_imports = all_imports & self.stdlib
        third_party = all_imports - self.stdlib - {''}

        # Estimate dependency depth (simple heuristic)
        depth = len(third_party) + len(stdlib_imports) // 2

        return DependencyMetrics(
            stdlib_imports=stdlib_imports,
            third_party_imports=third_party,
            dependency_depth=depth
        )


class EnhancedPatternAnalyzer:
    """Enhanced pattern analyzer with advanced metrics."""

    def __init__(self):
        pass

    def analyze(self, code: str) -> Dict:
        """Analyze code with enhanced metrics."""
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return self._empty_result()

        # Run all analyzers
        complexity = CyclomaticComplexityAnalyzer().analyze(tree)
        coupling = CouplingAnalyzer().analyze(tree)
        cohesion = CohesionAnalyzer().analyze(tree)
        dependencies = DependencyAnalyzer().analyze(tree)

        # Basic pattern extraction (from original analyzer)
        patterns = self._extract_basic_patterns(tree, code)

        # Calculate enhanced LJPW scores
        scores = self._calculate_enhanced_scores(
            patterns, complexity, coupling, cohesion, dependencies, code
        )

        return {
            'L': scores['love'],
            'J': scores['justice'],
            'P': scores['power'],
            'W': scores['wisdom'],
            'patterns': patterns,
            'complexity': complexity,
            'coupling': coupling,
            'cohesion': cohesion,
            'dependencies': dependencies
        }

    def _extract_basic_patterns(self, tree: ast.AST, code: str) -> Dict[str, int]:
        """Extract basic patterns (simplified from original)."""
        patterns = {
            'docstrings': 0,
            'type_hints': 0,
            'logging_calls': 0,
            'comments': 0,
            'try_except': 0,
            'validations': 0,
            'classes': 0,
            'functions': 0,
            'constants': 0,
            'global_vars': 0,
            'dict_usage': 0,
            'comprehensions': 0,
        }

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    patterns['docstrings'] += 1

            if isinstance(node, ast.FunctionDef):
                patterns['functions'] += 1
                if node.returns:
                    patterns['type_hints'] += 1

            if isinstance(node, ast.Try):
                patterns['try_except'] += 1

            if isinstance(node, ast.ClassDef):
                patterns['classes'] += 1

            if isinstance(node, ast.Dict):
                patterns['dict_usage'] += 1

            if isinstance(node, (ast.ListComp, ast.DictComp)):
                patterns['comprehensions'] += 1

        patterns['logging_calls'] = len(re.findall(r'\b(logger\.|logging\.)', code))
        patterns['comments'] = len(re.findall(r'#.*$', code, re.MULTILINE))
        patterns['validations'] = len(re.findall(r'\bif\s+not\s+\w+|\braise\s+\w+Error', code))

        return patterns

    def _calculate_enhanced_scores(
        self,
        patterns: Dict,
        complexity: ComplexityMetrics,
        coupling: CouplingMetrics,
        cohesion: CohesionMetrics,
        dependencies: DependencyMetrics,
        code: str
    ) -> Dict[str, float]:
        """Calculate LJPW scores with enhanced metrics."""

        lines = len([l for l in code.split('\n') if l.strip()])
        functions = max(patterns['functions'], 1)

        # LOVE (same as before)
        love = self._calculate_love(patterns, functions, lines)

        # JUSTICE (same as before)
        justice = self._calculate_justice(patterns, functions)

        # POWER (enhanced with complexity)
        power = self._calculate_power_enhanced(patterns, complexity, functions)

        # WISDOM (enhanced with coupling/cohesion)
        wisdom = self._calculate_wisdom_enhanced(
            patterns, coupling, cohesion, dependencies, functions, lines
        )

        return {
            'love': love,
            'justice': justice,
            'power': power,
            'wisdom': wisdom
        }

    def _calculate_love(self, patterns: Dict, functions: int, lines: int) -> float:
        """Calculate Love score."""
        love = 0.0
        love += min(patterns['docstrings'] / functions, 1.0) * 0.3
        love += min(patterns['type_hints'] / (functions * 3), 1.0) * 0.2
        love += min(patterns['logging_calls'] / functions, 1.0) * 0.2
        love += min(patterns['comments'] / (lines / 10), 1.0) * 0.15
        love += 0.15  # Base for descriptive names
        return love

    def _calculate_justice(self, patterns: Dict, functions: int) -> float:
        """Calculate Justice score."""
        justice = 0.0
        justice += min(patterns['try_except'] / functions, 1.0) * 0.4
        justice += min(patterns['validations'] / functions, 1.0) * 0.4
        justice += 0.2  # Base
        return justice

    def _calculate_power_enhanced(
        self,
        patterns: Dict,
        complexity: ComplexityMetrics,
        functions: int
    ) -> float:
        """Calculate Power score enhanced with cyclomatic complexity."""
        power = 0.5  # Start at neutral

        # Good patterns
        power += min(patterns['dict_usage'] / functions, 1.0) * 0.15
        power += min(patterns['comprehensions'] / functions, 1.0) * 0.10

        # Complexity penalty (lower complexity = higher power)
        if complexity.avg_complexity > 0:
            if complexity.avg_complexity <= ComplexityMetrics.SIMPLE_THRESHOLD:
                # Low complexity = good (+0.2)
                power += 0.2
            elif complexity.avg_complexity <= ComplexityMetrics.COMPLEX_THRESHOLD:
                # Medium complexity = neutral
                pass
            else:
                # High complexity = bad (-0.3)
                power -= 0.3

        # Max complexity penalty
        if complexity.max_complexity > ComplexityMetrics.VERY_COMPLEX_THRESHOLD:
            power -= 0.2

        return max(0.0, min(1.0, power))

    def _calculate_wisdom_enhanced(
        self,
        patterns: Dict,
        coupling: CouplingMetrics,
        cohesion: CohesionMetrics,
        dependencies: DependencyMetrics,
        functions: int,
        lines: int
    ) -> float:
        """Calculate Wisdom score enhanced with coupling/cohesion."""
        wisdom = 0.5  # Start at neutral

        # Good structural patterns
        if patterns['classes'] > 0:
            wisdom += min(patterns['classes'] / 3, 1.0) * 0.15
        if patterns['constants'] > 0:
            wisdom += min(patterns['constants'] / 5, 1.0) * 0.10

        # Coupling penalty (lower coupling = higher wisdom)
        coupling_penalty = coupling.coupling_score * 0.3
        wisdom -= coupling_penalty

        # Cohesion bonus (higher cohesion = higher wisdom)
        if cohesion.avg_cohesion > 0:
            cohesion_bonus = cohesion.avg_cohesion * 0.2
            wisdom += cohesion_bonus

        # Dependency depth penalty
        if dependencies.dependency_depth > 10:
            wisdom -= 0.15

        # Modularity (function count vs lines)
        modularity = functions / max(lines / 20, 1)
        wisdom += min(modularity, 1.0) * 0.05

        return max(0.0, min(1.0, wisdom))

    def _empty_result(self) -> Dict:
        """Return empty result for unparseable code."""
        return {
            'L': 0.0,
            'J': 0.0,
            'P': 0.0,
            'W': 0.0,
            'patterns': {},
            'complexity': ComplexityMetrics(),
            'coupling': CouplingMetrics(),
            'cohesion': CohesionMetrics(),
            'dependencies': DependencyMetrics()
        }


class EnhancedLJPWAnalyzer:
    """Enhanced automated LJPW analyzer with advanced metrics."""

    def __init__(self, quiet: bool = True):
        """Initialize with harmonizer and enhanced pattern analyzer."""
        self.harmonizer = PythonCodeHarmonizer(quiet=quiet)
        self.pattern_analyzer = EnhancedPatternAnalyzer()
        self.quiet = quiet

    def analyze_code(self, code: str) -> EnhancedLJPWScore:
        """Perform complete enhanced LJPW analysis."""
        if not self.quiet:
            print("🔍 Enhanced LJPW analysis with advanced metrics...")

        # 1. Semantic analysis
        semantic_result = self._analyze_semantics(code)

        # 2. Enhanced implementation analysis
        impl_result = self.pattern_analyzer.analyze(code)

        # 3. Combine scores
        L = (semantic_result['L'] + impl_result['L']) / 2
        J = (semantic_result['J'] + impl_result['J']) / 2
        P = (semantic_result['P'] + impl_result['P']) / 2
        W = (semantic_result['W'] + impl_result['W']) / 2
        H = (L * J * P * W) ** 0.25

        return EnhancedLJPWScore(
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
            complexity=impl_result['complexity'],
            coupling=impl_result['coupling'],
            cohesion=impl_result['cohesion'],
            dependencies=impl_result['dependencies'],
            patterns=impl_result['patterns']
        )

    def _analyze_semantics(self, code: str) -> Dict[str, float]:
        """Analyze semantics using harmonizer."""
        try:
            result = self.harmonizer.analyze_file_content(code)
        except Exception as e:
            if not self.quiet:
                print(f"⚠️  Harmonizer error: {e}")
            return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}

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

        if scores:
            return {
                'L': sum(s['L'] for s in scores) / len(scores),
                'J': sum(s['J'] for s in scores) / len(scores),
                'P': sum(s['P'] for s in scores) / len(scores),
                'W': sum(s['W'] for s in scores) / len(scores)
            }

        return {'L': 0.0, 'J': 0.0, 'P': 0.0, 'W': 0.0}

    def print_detailed_report(self, score: EnhancedLJPWScore, code: str):
        """Print enhanced detailed report."""
        lines = len([l for l in code.split('\n') if l.strip()])

        print("\n" + "=" * 80)
        print("ENHANCED LJPW ANALYSIS REPORT")
        print("=" * 80)

        print(f"\n📊 CODE METRICS:")
        print(f"  Lines of code: {lines}")
        print(f"  Functions: {score.patterns.get('functions', 0)}")
        print(f"  Classes: {score.patterns.get('classes', 0)}")

        # Complexity metrics
        print(f"\n📈 COMPLEXITY METRICS:")
        print(f"  Average cyclomatic complexity: {score.complexity.avg_complexity:.1f}")
        print(f"  Maximum complexity: {score.complexity.max_complexity}")
        if score.complexity.high_complexity_functions:
            print(f"  High complexity functions:")
            for name, comp in score.complexity.high_complexity_functions[:3]:
                status = "🔴" if comp > 20 else "🟡"
                print(f"    {status} {name}: {comp}")

        # Coupling metrics
        print(f"\n🔗 COUPLING METRICS:")
        print(f"  Total imports: {score.coupling.total_imports}")
        print(f"  External dependencies: {len(score.coupling.external_dependencies)}")
        if score.coupling.external_dependencies:
            deps = list(score.coupling.external_dependencies)[:5]
            print(f"    {', '.join(deps)}")
        print(f"  Coupling score: {score.coupling.coupling_score:.2f} ", end="")
        print("✅ Low" if score.coupling.coupling_score < 0.3 else
              "⚠️  Medium" if score.coupling.coupling_score < 0.6 else "❌ High")

        # Cohesion metrics
        print(f"\n🎯 COHESION METRICS:")
        print(f"  Average class cohesion: {score.cohesion.avg_cohesion:.2f}")
        print(f"  LCOM (lack of cohesion): {score.cohesion.lcom_score:.2f} ", end="")
        print("✅ Low" if score.cohesion.lcom_score < 0.3 else
              "⚠️  Medium" if score.cohesion.lcom_score < 0.6 else "❌ High")
        if score.cohesion.low_cohesion_classes:
            print(f"  Low cohesion classes: {', '.join(score.cohesion.low_cohesion_classes[:3])}")

        # Dependency analysis
        print(f"\n📦 DEPENDENCY ANALYSIS:")
        print(f"  Standard library: {len(score.dependencies.stdlib_imports)}")
        print(f"  Third-party: {len(score.dependencies.third_party_imports)}")
        print(f"  Dependency depth: {score.dependencies.dependency_depth}")

        # LJPW Scores
        print(f"\n🎯 LJPW SCORES:")
        print("-" * 80)

        self._print_dimension("LOVE", score.love, score.love_semantic, score.love_implementation)
        print("    💡 Observability, clarity, developer experience")

        self._print_dimension("JUSTICE", score.justice, score.justice_semantic, score.justice_implementation)
        print("    ⚖️  Correctness, validation, error handling")

        self._print_dimension("POWER", score.power, score.power_semantic, score.power_implementation)
        print("    ⚡ Efficiency, performance (enhanced with complexity)")
        print(f"    • Avg complexity: {score.complexity.avg_complexity:.1f} ", end="")
        print("✅" if score.complexity.avg_complexity < 10 else "❌")

        self._print_dimension("WISDOM", score.wisdom, score.wisdom_semantic, score.wisdom_implementation)
        print("    🧠 Architecture, design (enhanced with coupling/cohesion)")
        print(f"    • Coupling: {score.coupling.coupling_score:.2f} ", end="")
        print("✅ Low" if score.coupling.coupling_score < 0.3 else "❌ High")
        print(f"    • Cohesion: {score.cohesion.avg_cohesion:.2f} ", end="")
        print("✅ High" if score.cohesion.avg_cohesion > 0.7 else "❌ Low")

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
        print(f"    - Implementation (patterns + metrics): {implementation:.2f}")


if __name__ == "__main__":
    # Demo
    print("Enhanced LJPW Analyzer with Advanced Metrics\n")
    print("Features:")
    print("  ✅ Cyclomatic Complexity")
    print("  ✅ Coupling Analysis")
    print("  ✅ Cohesion Metrics (LCOM)")
    print("  ✅ Dependency Tracking")
    print("\nSee test_enhanced_analyzer.py for demo")
