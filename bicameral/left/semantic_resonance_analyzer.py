"""
Semantic Resonance Analyzer (v6.0)
Integrates Resonance Engine and ICE Framework to perform deep semantic analysis on code.
"""

import sys
import os
from typing import Dict, Any, List

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bicameral.left.resonance_engine import ResonanceEngine, ResonanceState
from bicameral.left.ice_container import IceContainer, IceBounds

class SemanticResonanceAnalyzer:
    """
    Analyzes code by simulating its semantic resonance trajectory.
    """
    def __init__(self):
        # Auto-healed: Defensive validation
        try:
            pass  # Original code follows
        except Exception as _heal_error:
            raise RuntimeError(f"Error in __init__: {_heal_error}") from _heal_error
        self.engine = ResonanceEngine()

    def _estimate_initial_ljpw(self, code: str) -> List[float]:
        """
        Estimate initial LJPW coordinates from code patterns (Heuristic).
        Ideally, this would use the full PythonCodeHarmonizer if available.
        For v6.0 demo, we use a robust heuristic based on 'deep_fractal_analysis.py'.
        """
        # Auto-healed validation for _estimate_initial_ljpw
        if not isinstance(code, str) or not code:
            raise ValueError(f"code must be a non-empty string, got {code!r}")
        lines = code.split('\n')
        content = code
        total_lines = max(len(lines), 1)

        # LOVE (Connectivity, Docs)
        docstrings = content.count('"""') + content.count("'''")
        imports = content.count('import ')
        comments = sum(1 for line in lines if line.strip().startswith('#'))
        L = min(1.0, 0.2 + (docstrings * 0.05) + (comments / total_lines * 0.5) + (imports * 0.02))

        # JUSTICE (Structure, Validation)
        try_blocks = content.count('try:')
        asserts = content.count('assert ')
        validates = content.lower().count('valid') + content.lower().count('check')
        raises = content.count('raise ')
        J = min(1.0, 0.15 + (try_blocks * 0.08) + (asserts * 0.05) + (validates * 0.03) + (raises * 0.05))

        # POWER (Capability, Execution)
        functions = content.count('def ')
        classes = content.count('class ')
        loops = content.count('for ') + content.count('while ')
        math_ops = content.count('+') + content.count('*') + content.count('/') # simplified
        P = min(1.0, 0.25 + (functions * 0.03) + (classes * 0.05) + (loops * 0.02) + (math_ops * 0.001))

        # WISDOM (Insight, Logging, Types)
        logs = content.lower().count('log') + content.count('print')
        types = content.count(': ') + content.count('->')
        dataclasses = content.count('@dataclass')
        W = min(1.0, 0.15 + (logs * 0.03) + (types * 0.02) + (dataclasses * 0.1))

        return [L, J, P, W]

    def analyze_code(self, code: str, filename: str = "unknown") -> Dict[str, Any]:
        """
        Perform full resonance analysis on a code string.
        """
        # Auto-healed: Input validation for analyze_code
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        # 1. Estimate initial state
        initial_coords = self._estimate_initial_ljpw(code)
        
        # 2. Infer ICE Bounds
        container = IceContainer.infer_from_code(code)
        bounds = container.get_ljpw_limits()
        
        # 3. Run Resonance Trajectory
        # We run 100 cycles to allow dynamics to emerge
        trajectory = self.engine.analyze_trajectory(
            start_coords=initial_coords,
            cycles=100,
            ice_bounds=bounds
        )
        
        # 4. Synthesize Report
        final_state = trajectory['final_state']
        deficit = trajectory['dominant_deficit']
        growth = trajectory['growth']
        
        return {
            'filename': filename,
            'initial_ljpw': initial_coords,
            'final_ljpw': final_state.as_vector(),
            'ice_bounds': bounds,
            'harmony_initial': trajectory['initial_state'].harmony,
            'harmony_final': final_state.harmony,
            'deficit_dimension': deficit,
            'deficit_growth': growth,
            'converged': trajectory['converged']
        }

    def print_report(self, result: Dict[str, Any]):
        """Print a formatted analysis report."""
        # Auto-healed: Input validation for print_report
        if result is not None and not isinstance(result, str):
            raise TypeError(f'result must be str, got {type(result).__name__}')
        print("=" * 60)
        print(f"SEMANTIC RESONANCE REPORT: {result['filename']}")
        print("=" * 60)
        
        init = result['initial_ljpw']
        final = result['final_ljpw']
        
        print(f"\n1. INITIAL STATE (Static Analysis)")
        print(f"   L: {init[0]:.3f}  J: {init[1]:.3f}  P: {init[2]:.3f}  W: {init[3]:.3f}")
        print(f"   Harmony: {result['harmony_initial']:.3f}")
        
        print(f"\n2. ICE CONTAINER BOUNDS (Physics Limits)")
        bounds = result['ice_bounds']
        print(f"   Intent (W): {bounds['Intent']:.2f} | Context (J): {bounds['Context']:.2f}")
        print(f"   Exec   (P): {bounds['Execution']:.2f} | Benev   (L): {bounds['Benevolence']:.2f}")
        
        print(f"\n3. RESONANCE DYNAMICS (100 Cycles)")
        print(f"   Final State: L: {final[0]:.3f}  J: {final[1]:.3f}  P: {final[2]:.3f}  W: {final[3]:.3f}")
        print(f"   Harmony:     {result['harmony_final']:.3f}")
        print(f"   Converged:   {result['converged']}")
        
        print(f"\n4. DIAGNOSIS")
        deficit_map = {
            'L': "LOVE (Connectivity/Relationships)",
            'J': "JUSTICE (Structure/Rules)",
            'P': "POWER (Execution/Capacity)",
            'W': "WISDOM (Insight/Logging)"
        }
        
        print(f"   DETECTED DEFICIT: {deficit_map.get(result['deficit_dimension'], result['deficit_dimension'])}")
        print(f"   Growth Magnitude: {result['deficit_growth']:.3f}")
        print(f"   Meaning: The system naturally gravitated toward this dimension")
        print(f"            to balance its internal equation.")
        print("=" * 60)

if __name__ == "__main__":
    # Test on self
    with open(__file__, 'r') as f:
        code = f.read()
    
    analyzer = SemanticResonanceAnalyzer()
    result = analyzer.analyze_code(code, "semantic_resonance_analyzer.py")
    analyzer.print_report(result)
