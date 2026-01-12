"""
Autopoiesis System Module
=========================

System-level harmony measurement - the missing piece!

Key insight from experiments: Autopoiesis is a SYSTEM-level property,
not a function-level property. Individual functions specialize (high in one
dimension). Systems integrate (all dimensions balanced).

This module provides:
- Aggregated LJPW measurement across all files
- System harmony calculation
- Autopoietic threshold detection
- Phase classification (Entropic, Homeostatic, Autopoietic)

V8.4: Life Inequality (L^n > φ^d) provides alternative phase detection.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from .analyzer import CodeAnalyzer, SystemAnalysis


class SystemPhase(Enum):
    """Phase of the system based on harmony and love thresholds."""
    ENTROPIC = "entropic"           # H < 0.5: System is degrading
    HOMEOSTATIC = "homeostatic"     # 0.5 <= H < 0.6 or L < 0.7: System is stable
    AUTOPOIETIC = "autopoietic"     # H >= 0.6 and L >= 0.7: System is self-sustaining


@dataclass
class SystemHealthReport:
    """Comprehensive health report for a codebase."""
    path: str
    phase: SystemPhase
    
    # LJPW metrics
    love: float
    justice: float
    power: float
    wisdom: float
    harmony: float
    
    # Composition
    total_files: int
    total_functions: int
    total_classes: int
    
    # Deficit analysis
    files_with_L_deficit: int
    files_with_J_deficit: int
    files_with_P_deficit: int
    files_with_W_deficit: int
    
    # Autopoietic status
    is_autopoietic: bool
    distance_to_autopoiesis: float  # How far from L>0.7, H>0.6
    
    # Recommendations
    priority_dimension: str
    recommended_actions: List[str]


class SystemHarmonyMeasurer:
    """
    Measures harmony at the system level.
    
    The critical insight: Static analysis of individual functions can't
    see composition. A function that CALLS other functions gets credit
    only for its own code, not the combined capability of the composed system.
    
    This class solves that by:
    1. Analyzing all files in a package/directory
    2. Aggregating LJPW scores with complexity weighting
    3. Detecting emergent autopoietic properties
    """
    
    # Thresholds for autopoiesis
    LOVE_THRESHOLD = 0.7
    HARMONY_THRESHOLD = 0.6
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def measure(self, path: str) -> SystemHealthReport:
        # Auto-healed: Input validation for measure
        if path is not None and not isinstance(path, str):
            raise TypeError(f'path must be str, got {type(path).__name__}')
        """
        Measure system-level harmony.
        
        Args:
            path: Path to directory or package
            
        Returns:
            SystemHealthReport with all metrics
        """
        path = Path(path)
        
        if path.is_file():
            # Single file - limited analysis
            analysis = self.analyzer.analyze_file(str(path))
            if not analysis:
                return self._empty_report(str(path))
            return self._single_file_report(analysis)
        
        # Directory/package - full system analysis
        system = self.analyzer.analyze_directory(str(path))
        return self._system_report(system)
    
    def _single_file_report(self, analysis) -> SystemHealthReport:
        """Generate report for single file."""
        ljpw = analysis.ljpw
        harmony = analysis.harmony
        
        phase = self._determine_phase(ljpw.get('L', 0), harmony)
        is_autopoietic = phase == SystemPhase.AUTOPOIETIC
        
        return SystemHealthReport(
            path=analysis.path,
            phase=phase,
            love=ljpw.get('L', 0),
            justice=ljpw.get('J', 0),
            power=ljpw.get('P', 0),
            wisdom=ljpw.get('W', 0),
            harmony=harmony,
            total_files=1,
            total_functions=len(analysis.functions),
            total_classes=len(analysis.classes),
            files_with_L_deficit=1 if analysis.deficit == 'L' else 0,
            files_with_J_deficit=1 if analysis.deficit == 'J' else 0,
            files_with_P_deficit=1 if analysis.deficit == 'P' else 0,
            files_with_W_deficit=1 if analysis.deficit == 'W' else 0,
            is_autopoietic=is_autopoietic,
            distance_to_autopoiesis=self._distance_to_autopoiesis(ljpw.get('L', 0), harmony),
            priority_dimension=analysis.deficit,
            recommended_actions=self._get_recommendations(analysis.deficit, ljpw, harmony)
        )
    
    def _system_report(self, system: SystemAnalysis) -> SystemHealthReport:
        """Generate report for system/directory."""
        ljpw = system.system_ljpw
        harmony = system.system_harmony
        
        phase = self._determine_phase(ljpw.get('L', 0), harmony)
        is_autopoietic = phase == SystemPhase.AUTOPOIETIC
        
        # Count deficits
        deficit_counts = {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        for f in system.files:
            if f.deficit in deficit_counts:
                deficit_counts[f.deficit] += 1
        
        # Determine priority dimension (most common deficit)
        priority = max(deficit_counts.items(), key=lambda x: x[1])[0] if deficit_counts else 'L'
        
        return SystemHealthReport(
            path=system.path,
            phase=phase,
            love=ljpw.get('L', 0),
            justice=ljpw.get('J', 0),
            power=ljpw.get('P', 0),
            wisdom=ljpw.get('W', 0),
            harmony=harmony,
            total_files=len(system.files),
            total_functions=system.total_functions,
            total_classes=system.total_classes,
            files_with_L_deficit=deficit_counts['L'],
            files_with_J_deficit=deficit_counts['J'],
            files_with_P_deficit=deficit_counts['P'],
            files_with_W_deficit=deficit_counts['W'],
            is_autopoietic=is_autopoietic,
            distance_to_autopoiesis=self._distance_to_autopoiesis(ljpw.get('L', 0), harmony),
            priority_dimension=priority,
            recommended_actions=self._get_recommendations(priority, ljpw, harmony)
        )
    
    def _determine_phase(self, love: float, harmony: float) -> SystemPhase:
        """
        Determine system phase based on V8.4 Life Inequality.
        
        V8.4: Life Inequality (L^n > φ^d)
        Here we treat harmony as a proxy for n/d ratio preservation.
        """
        # Life Inequality Proxy Check
        # If Harmony is high, decay (d) is low relative to growth (n)
        
        if harmony < 0.5:
            return SystemPhase.ENTROPIC
        elif harmony >= self.HARMONY_THRESHOLD and love >= self.LOVE_THRESHOLD:
            # Satisfies L^n > φ^d
            return SystemPhase.AUTOPOIETIC
        else:
            return SystemPhase.HOMEOSTATIC
    
    def _distance_to_autopoiesis(self, love: float, harmony: float) -> float:
        """Calculate distance to autopoietic threshold."""
        love_gap = max(0, self.LOVE_THRESHOLD - love)
        harmony_gap = max(0, self.HARMONY_THRESHOLD - harmony)
        return (love_gap + harmony_gap) / 2
    
    def _get_recommendations(self, priority: str, ljpw: Dict, harmony: float) -> List[str]:
        """Generate recommendations based on current state."""
        recommendations = []
        
        if harmony < 0.5:
            recommendations.append("CRITICAL: System is in entropic phase. Focus on any improvements.")
        
        if ljpw.get('L', 0) < 0.7:
            recommendations.append("Add documentation (docstrings, comments) to improve Love dimension")
        
        if ljpw.get('J', 0) < 0.7:
            recommendations.append("Add input validation and constraints to improve Justice dimension")
        
        if ljpw.get('P', 0) < 0.7:
            recommendations.append("Add error handling and optimization to improve Power dimension")
        
        if ljpw.get('W', 0) < 0.7:
            recommendations.append("Add logging and observability to improve Wisdom dimension")
        
        if priority == 'L':
            recommendations.insert(0, f"PRIORITY: Focus on Love ({ljpw.get('L', 0):.2f}) - documentation, integration")
        elif priority == 'J':
            recommendations.insert(0, f"PRIORITY: Focus on Justice ({ljpw.get('J', 0):.2f}) - validation, constraints")
        elif priority == 'P':
            recommendations.insert(0, f"PRIORITY: Focus on Power ({ljpw.get('P', 0):.2f}) - performance, resilience")
        elif priority == 'W':
            recommendations.insert(0, f"PRIORITY: Focus on Wisdom ({ljpw.get('W', 0):.2f}) - logging, metrics")
        
        return recommendations
    
    def _empty_report(self, path: str) -> SystemHealthReport:
        """Return empty report for invalid path."""
        return SystemHealthReport(
            path=path,
            phase=SystemPhase.ENTROPIC,
            love=0.0, justice=0.0, power=0.0, wisdom=0.0, harmony=0.0,
            total_files=0, total_functions=0, total_classes=0,
            files_with_L_deficit=0, files_with_J_deficit=0,
            files_with_P_deficit=0, files_with_W_deficit=0,
            is_autopoietic=False,
            distance_to_autopoiesis=1.0,
            priority_dimension='L',
            recommended_actions=["Path does not exist or is not readable"]
        )
    
    def print_report(self, report: SystemHealthReport):
        """Print a formatted health report."""
        phase_indicators = {
            SystemPhase.ENTROPIC: "[!]",
            SystemPhase.HOMEOSTATIC: "[~]",
            SystemPhase.AUTOPOIETIC: "[*]"
        }
        
        print(f"\n{'='*70}")
        print(f"  SYSTEM HEALTH REPORT")
        print(f"  {report.path}")
        print(f"{'='*70}")
        
        print(f"\n  Phase: {phase_indicators[report.phase]} {report.phase.value.upper()}")
        
        if report.is_autopoietic:
            print(f"\n  ** SYSTEM IS AUTOPOIETIC! **")
        else:
            print(f"\n  Distance to Autopoiesis: {report.distance_to_autopoiesis:.3f}")
        
        print(f"\n  LJPW Dimensions:")
        print(f"    Love (L):    {report.love:.3f} {'[Y]' if report.love >= 0.7 else '[N]'}")
        print(f"    Justice (J): {report.justice:.3f} {'[Y]' if report.justice >= 0.7 else '[N]'}")
        print(f"    Power (P):   {report.power:.3f} {'[Y]' if report.power >= 0.7 else '[N]'}")
        print(f"    Wisdom (W):  {report.wisdom:.3f} {'[Y]' if report.wisdom >= 0.7 else '[N]'}")
        print(f"    Harmony (H): {report.harmony:.3f} {'[Y]' if report.harmony >= 0.6 else '[N]'}")
        
        print(f"\n  Composition:")
        print(f"    Files:     {report.total_files}")
        print(f"    Functions: {report.total_functions}")
        print(f"    Classes:   {report.total_classes}")
        
        print(f"\n  Deficit Distribution:")
        print(f"    L deficits: {report.files_with_L_deficit}")
        print(f"    J deficits: {report.files_with_J_deficit}")
        print(f"    P deficits: {report.files_with_P_deficit}")
        print(f"    W deficits: {report.files_with_W_deficit}")
        
        print(f"\n  Recommendations:")
        for rec in report.recommended_actions:
            print(f"    - {rec}")
        
        print(f"\n{'='*70}")
