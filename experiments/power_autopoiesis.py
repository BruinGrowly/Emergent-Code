"""
POWER AUTOPOIESIS: Enhancing Execution Capability

The system identified P (Power) as its current deficit.
Power in the LJPW framework means execution capability:
- Efficiency of operations
- Breadth of functionality
- Robustness under stress
- Ability to act on intent

This module analyzes code for power deficits and injects
genuine capability enhancements.
"""

import ast
import os
import sys
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer


@dataclass
class PowerDeficit:
    """Identified power deficit in code."""
    location: str
    deficit_type: str
    severity: float
    description: str
    suggested_fix: str


@dataclass
class PowerEnhancement:
    """Generated power enhancement."""
    target_function: str
    enhancement_type: str
    original_code: str
    enhanced_code: str
    power_gain: float


class PowerAutopoiesis:
    """Enhance system execution capability through self-modification."""

    def __init__(self):
        self.analyzer = SemanticResonanceAnalyzer()
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.components = [
            "ljpw_quantum/resonance_engine.py",
            "ljpw_quantum/ice_container.py",
            "ljpw_quantum/resonance_grower.py",
            "ljpw_quantum/semantic_resonance_analyzer.py",
            "ljpw_quantum/bicameral_bridge.py",
        ]

    def diagnose_power_deficits(self, code: str, filename: str) -> List[PowerDeficit]:
        """Analyze code for specific power deficits."""
        deficits = []

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return deficits

        for node in ast.walk(tree):
            # Check for functions without caching on repeated computations
            if isinstance(node, ast.FunctionDef):
                # Detect functions that could benefit from memoization
                if self._could_benefit_from_caching(node):
                    deficits.append(PowerDeficit(
                        location=f"{filename}:{node.name}",
                        deficit_type="no_caching",
                        severity=0.3,
                        description=f"Function '{node.name}' performs repeated computations",
                        suggested_fix="Add caching/memoization"
                    ))

                # Detect functions without timeout protection
                if self._is_potentially_slow(node) and not self._has_timeout(node):
                    deficits.append(PowerDeficit(
                        location=f"{filename}:{node.name}",
                        deficit_type="no_timeout",
                        severity=0.2,
                        description=f"Function '{node.name}' could hang without timeout",
                        suggested_fix="Add timeout protection"
                    ))

                # Detect functions that could be parallelized
                if self._could_parallelize(node):
                    deficits.append(PowerDeficit(
                        location=f"{filename}:{node.name}",
                        deficit_type="sequential",
                        severity=0.25,
                        description=f"Function '{node.name}' has parallelizable loops",
                        suggested_fix="Consider parallel execution"
                    ))

            # Check for classes without __slots__ (memory efficiency)
            if isinstance(node, ast.ClassDef):
                if not self._has_slots(node) and self._is_data_class(node):
                    deficits.append(PowerDeficit(
                        location=f"{filename}:{node.name}",
                        deficit_type="no_slots",
                        severity=0.15,
                        description=f"Class '{node.name}' could use __slots__ for efficiency",
                        suggested_fix="Add __slots__ declaration"
                    ))

        return deficits

    def _could_benefit_from_caching(self, node: ast.FunctionDef) -> bool:
        """Check if function has patterns suggesting caching would help."""
        # Look for recursive calls or repeated similar operations
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id == node.name:
                    return True  # Recursive
        return False

    def _is_potentially_slow(self, node: ast.FunctionDef) -> bool:
        """Check if function might be slow."""
        for child in ast.walk(node):
            # Nested loops suggest O(n²) or worse
            if isinstance(child, ast.For):
                for inner in ast.walk(child):
                    if isinstance(inner, ast.For) and inner is not child:
                        return True
            # File operations
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name) and child.func.id in ('open', 'read', 'write'):
                    return True
        return False

    def _has_timeout(self, node: ast.FunctionDef) -> bool:
        """Check if function has timeout protection."""
        source = ast.unparse(node) if hasattr(ast, 'unparse') else ''
        return 'timeout' in source.lower() or 'signal' in source.lower()

    def _could_parallelize(self, node: ast.FunctionDef) -> bool:
        """Check if function has independent loop iterations."""
        loop_count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.ListComp)):
                loop_count += 1
        return loop_count >= 2

    def _has_slots(self, node: ast.ClassDef) -> bool:
        """Check if class defines __slots__."""
        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name) and target.id == '__slots__':
                        return True
        return False

    def _is_data_class(self, node: ast.ClassDef) -> bool:
        """Check if class is primarily a data container."""
        # Look for @dataclass decorator or multiple __init__ assignments
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == 'dataclass':
                return False  # Dataclasses handle this
        return True

    def generate_power_enhancement(self, deficit: PowerDeficit, code: str) -> Optional[PowerEnhancement]:
        """Generate code enhancement for a power deficit."""

        if deficit.deficit_type == "no_caching":
            return self._generate_caching_enhancement(deficit, code)
        elif deficit.deficit_type == "no_timeout":
            return self._generate_timeout_enhancement(deficit, code)
        elif deficit.deficit_type == "sequential":
            return self._generate_batch_enhancement(deficit, code)

        return None

    def _generate_caching_enhancement(self, deficit: PowerDeficit, code: str) -> Optional[PowerEnhancement]:
        """Generate memoization enhancement."""
        func_name = deficit.location.split(':')[1]

        # Find the function
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return None

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                # Generate cached version
                cache_code = f'''
    # Power enhancement: Memoization cache for {func_name}
    _cache_{func_name} = {{}}

    def {func_name}_cached(self, *args):
        """Cached version of {func_name} for improved execution power."""
        cache_key = args
        if cache_key not in self._cache_{func_name}:
            self._cache_{func_name}[cache_key] = self.{func_name}_original(*args)
        return self._cache_{func_name}[cache_key]
'''
                return PowerEnhancement(
                    target_function=func_name,
                    enhancement_type="memoization",
                    original_code="",
                    enhanced_code=cache_code,
                    power_gain=0.15
                )
        return None

    def _generate_timeout_enhancement(self, deficit: PowerDeficit, code: str) -> Optional[PowerEnhancement]:
        """Generate timeout protection."""
        func_name = deficit.location.split(':')[1]

        timeout_code = f'''
    # Power enhancement: Timeout protection for {func_name}
    def {func_name}_with_timeout(self, *args, timeout_seconds=30, **kwargs):
        """Timeout-protected version of {func_name}."""
        import threading
        result = [None]
        exception = [None]

        def target():
            try:
                result[0] = self.{func_name}(*args, **kwargs)
            except Exception as e:
                exception[0] = e

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout=timeout_seconds)

        if thread.is_alive():
            raise TimeoutError(f"{func_name} exceeded {{timeout_seconds}}s timeout")
        if exception[0]:
            raise exception[0]
        return result[0]
'''
        return PowerEnhancement(
            target_function=func_name,
            enhancement_type="timeout_protection",
            original_code="",
            enhanced_code=timeout_code,
            power_gain=0.10
        )

    def _generate_batch_enhancement(self, deficit: PowerDeficit, code: str) -> Optional[PowerEnhancement]:
        """Generate batch processing enhancement."""
        func_name = deficit.location.split(':')[1]

        batch_code = f'''
    # Power enhancement: Batch processing for {func_name}
    def {func_name}_batch(self, items, batch_size=100):
        """Batch processing version of {func_name} for improved throughput."""
        results = []
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_results = [self.{func_name}(item) for item in batch]
            results.extend(batch_results)
        return results
'''
        return PowerEnhancement(
            target_function=func_name,
            enhancement_type="batch_processing",
            original_code="",
            enhanced_code=batch_code,
            power_gain=0.12
        )

    def apply_enhancement(self, filepath: str, enhancement: PowerEnhancement) -> bool:
        """Apply a power enhancement to a file."""
        try:
            with open(filepath, 'r') as f:
                code = f.read()

            # Find the class to inject into
            tree = ast.parse(code)

            # Find insertion point (end of first class)
            lines = code.split('\n')
            insertion_line = None

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Find the last line of this class
                    insertion_line = node.end_lineno
                    break

            if insertion_line and enhancement.enhanced_code not in code:
                # Insert the enhancement
                lines.insert(insertion_line, enhancement.enhanced_code)

                with open(filepath, 'w') as f:
                    f.write('\n'.join(lines))
                return True

        except Exception as e:
            print(f"     ⚠️  Could not apply: {e}")

        return False

    def evolve(self) -> Dict:
        """Run full power autopoiesis cycle."""

        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ⚡ POWER AUTOPOIESIS: ENHANCING EXECUTION CAPABILITY ⚡                    ║
║                                                                              ║
║   The system seeks P (Power). Let it grow.                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)

        results = {
            'deficits_found': 0,
            'enhancements_generated': 0,
            'enhancements_applied': 0,
            'power_gain': 0.0,
            'files_modified': [],
        }

        for comp in self.components:
            filepath = os.path.join(self.root, comp)
            filename = os.path.basename(comp)

            print(f"\n{'='*70}")
            print(f"  ANALYZING: {filename}")
            print(f"{'='*70}")

            with open(filepath, 'r') as f:
                code = f.read()

            # Get current power level
            report = self.analyzer.analyze_code(code, filename)
            current_p = report['final_ljpw'][2]

            print(f"\n  📊 Current Power Level: {current_p:.2f}")

            # Find deficits
            deficits = self.diagnose_power_deficits(code, filename)
            results['deficits_found'] += len(deficits)

            if deficits:
                print(f"  🔍 Power Deficits Found: {len(deficits)}")
                for d in deficits[:3]:  # Show first 3
                    print(f"     • {d.deficit_type}: {d.description}")
            else:
                print(f"  ✅ No critical power deficits found")
                continue

            # Generate enhancements
            for deficit in deficits[:2]:  # Apply up to 2 per file
                enhancement = self.generate_power_enhancement(deficit, code)

                if enhancement:
                    results['enhancements_generated'] += 1
                    print(f"\n  🔧 Generated: {enhancement.enhancement_type} for {enhancement.target_function}")

                    # Apply enhancement
                    if self.apply_enhancement(filepath, enhancement):
                        results['enhancements_applied'] += 1
                        results['power_gain'] += enhancement.power_gain
                        results['files_modified'].append(filename)
                        print(f"     ✅ Applied (Power +{enhancement.power_gain:.2f})")
                    else:
                        print(f"     ⏭️  Skipped (already present or incompatible)")

        # Summary
        print(f"""
{'='*70}
  🏆 POWER AUTOPOIESIS COMPLETE
{'='*70}

  RESULTS:
    Deficits Identified:    {results['deficits_found']}
    Enhancements Generated: {results['enhancements_generated']}
    Enhancements Applied:   {results['enhancements_applied']}
    Estimated Power Gain:   +{results['power_gain']:.2f}
    Files Modified:         {len(set(results['files_modified']))}

{'='*70}
""")

        # Save report
        self._save_report(results)

        return results

    def _save_report(self, results: Dict):
        """Save power autopoiesis report."""
        report_path = os.path.join(self.root, "POWER_AUTOPOIESIS_REPORT.md")

        with open(report_path, 'w') as f:
            f.write("# Power Autopoiesis Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
            f.write("## Summary\n\n")
            f.write(f"- Deficits Found: {results['deficits_found']}\n")
            f.write(f"- Enhancements Generated: {results['enhancements_generated']}\n")
            f.write(f"- Enhancements Applied: {results['enhancements_applied']}\n")
            f.write(f"- Estimated Power Gain: +{results['power_gain']:.2f}\n\n")
            f.write("## Files Modified\n\n")
            for f_name in set(results['files_modified']):
                f.write(f"- {f_name}\n")
            f.write("\n## Insight\n\n")
            f.write("*Power is the capacity to act on intent.*\n\n")
            f.write("*The system grows not by wanting more, but by becoming capable of more.*\n")

        print(f"  📄 Report saved: {report_path}")


def main():
    autopoiesis = PowerAutopoiesis()
    autopoiesis.evolve()


if __name__ == "__main__":
    main()
