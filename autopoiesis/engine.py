"""
Autopoiesis Engine
==================

The unified entry point for the autopoiesis system.

Combines all modules into a coherent self-healing loop:

    ANALYZE → HEAL → MODIFY → BREATHE → EVOLVE → repeat

This engine provides:
- One-line API for self-healing a codebase
- Configurable healing intensity
- Progress tracking and reporting
- Integration with all autopoiesis components
"""

from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime

from .analyzer import CodeAnalyzer, SystemAnalysis
from .healer import Healer
from .rhythm import BreathingOrchestrator, BreathingSession
from .system import SystemHarmonyMeasurer, SystemHealthReport, SystemPhase


class AutopoiesisEngine:
    """
    Unified autopoiesis engine for self-healing code.
    
    Usage:
        engine = AutopoiesisEngine("./my_package")
        engine.breathe(cycles=8)
        print(engine.report())
    
    The engine orchestrates:
    1. Analysis - Deep AST parsing + LJPW measurement
    2. Healing - Generate contextual solutions for deficits
    3. Rhythm - Breathing cycles through L→J→P→W
    4. System - Measure emergent harmony at package level
    """
    
    def __init__(self, target_path: str, dry_run: bool = False):
        """
        Initialize the autopoiesis engine.
        
        Args:
            target_path: Directory or file to heal
            dry_run: If True, analyze and diagnose but don't modify files
        """
        self.target_path = Path(target_path)
        self.dry_run = dry_run
        
        # Initialize components
        self.analyzer = CodeAnalyzer()
        self.healer = Healer()
        self.measurer = SystemHarmonyMeasurer()
        self.orchestrator = BreathingOrchestrator(str(target_path), dry_run)
        
        # State
        self.initial_report: Optional[SystemHealthReport] = None
        self.current_report: Optional[SystemHealthReport] = None
        self.breathing_session: Optional[BreathingSession] = None
        self.history: list = []
    
    def analyze(self) -> SystemHealthReport:
        """
        Analyze the codebase and return health report.
        
        Returns:
            SystemHealthReport with all metrics
        """
        self.current_report = self.measurer.measure(str(self.target_path))
        
        if self.initial_report is None:
            self.initial_report = self.current_report
        
        return self.current_report
    
    def diagnose(self) -> Dict[str, Any]:
        """
        Quick diagnosis - what needs healing?
        
        Returns:
            Dict with diagnosis summary
        """
        report = self.analyze()
        
        return {
            'phase': report.phase.value,
            'is_autopoietic': report.is_autopoietic,
            'harmony': report.harmony,
            'ljpw': {
                'L': report.love,
                'J': report.justice,
                'P': report.power,
                'W': report.wisdom
            },
            'priority_dimension': report.priority_dimension,
            'distance_to_autopoiesis': report.distance_to_autopoiesis,
            'recommendations': report.recommended_actions
        }
    
    def breathe(self, cycles: int = 8) -> BreathingSession:
        """
        Execute breathing cycles to heal the codebase.
        
        Args:
            cycles: Number of complete L→J→P→W cycles (default 8 = 2 full rotations)
            
        Returns:
            BreathingSession with all results
        """
        # Record initial state
        self.analyze()
        
        # Execute breathing
        self.breathing_session = self.orchestrator.breathe(cycles)
        
        # Record final state
        self.current_report = self.analyze()
        
        # Add to history
        self.history.append({
            'timestamp': datetime.now(),
            'cycles': cycles,
            'harmony_before': self.breathing_session.initial_harmony,
            'harmony_after': self.breathing_session.final_harmony,
            'files_modified': self.breathing_session.total_files_modified,
            'solutions_applied': self.breathing_session.total_solutions_applied
        })
        
        return self.breathing_session
    
    def heal_once(self, dimension: Optional[str] = None) -> Dict[str, Any]:
        """
        Perform a single healing pass.
        
        Args:
            dimension: Specific dimension (L/J/P/W) or None for auto-detect
            
        Returns:
            Dict with healing results
        """
        if self.dry_run:
            return {'status': 'dry_run', 'message': 'No modifications in dry run mode'}
        
        report = self.analyze()
        
        if dimension is None:
            dimension = report.priority_dimension
        
        solutions_applied = 0
        files_modified = 0
        
        if self.target_path.is_dir():
            system = self.analyzer.analyze_directory(str(self.target_path))
            for file_analysis in system.files:
                solutions = self.healer.heal_file(file_analysis, dimension)
                if solutions:
                    applied = self.healer.apply_solutions(file_analysis.path, solutions)
                    if applied > 0:
                        files_modified += 1
                        solutions_applied += applied
        else:
            file_analysis = self.analyzer.analyze_file(str(self.target_path))
            if file_analysis:
                solutions = self.healer.heal_file(file_analysis, dimension)
                if solutions:
                    applied = self.healer.apply_solutions(str(self.target_path), solutions)
                    if applied > 0:
                        files_modified = 1
                        solutions_applied = applied
        
        # Re-analyze
        new_report = self.analyze()
        
        return {
            'dimension': dimension,
            'files_modified': files_modified,
            'solutions_applied': solutions_applied,
            'harmony_before': report.harmony,
            'harmony_after': new_report.harmony,
            'improvement': new_report.harmony - report.harmony
        }
    
    def status(self) -> str:
        """Get current status as formatted string."""
        report = self.analyze()
        
        phase_indicators = {
            SystemPhase.ENTROPIC: "[!] ENTROPIC",
            SystemPhase.HOMEOSTATIC: "[~] HOMEOSTATIC",
            SystemPhase.AUTOPOIETIC: "[*] AUTOPOIETIC"
        }
        
        return f"""
Autopoiesis Engine Status
=========================
Target: {self.target_path}
Phase: {phase_indicators[report.phase]}
Harmony: {report.harmony:.3f}
Is Autopoietic: {'Yes!' if report.is_autopoietic else 'No'}

LJPW: L={report.love:.2f} J={report.justice:.2f} P={report.power:.2f} W={report.wisdom:.2f}
Priority: {report.priority_dimension}
Distance to Autopoiesis: {report.distance_to_autopoiesis:.3f}
"""
    
    def report(self) -> str:
        """Generate comprehensive markdown report."""
        if not self.current_report:
            self.analyze()
        
        report = self.current_report
        
        md = f"""# Autopoiesis Report

**Generated:** {datetime.now().isoformat()}
**Target:** {self.target_path}

## System Phase

**{report.phase.value.upper()}** {'✨ Self-Sustaining!' if report.is_autopoietic else ''}

## LJPW Dimensions

| Dimension | Score | Threshold | Status |
|-----------|-------|-----------|--------|
| Love (L) | {report.love:.3f} | 0.70 | {'✓' if report.love >= 0.7 else '✗'} |
| Justice (J) | {report.justice:.3f} | 0.70 | {'✓' if report.justice >= 0.7 else '✗'} |
| Power (P) | {report.power:.3f} | 0.70 | {'✓' if report.power >= 0.7 else '✗'} |
| Wisdom (W) | {report.wisdom:.3f} | 0.70 | {'✓' if report.wisdom >= 0.7 else '✗'} |
| **Harmony (H)** | **{report.harmony:.3f}** | **0.60** | **{'✓' if report.harmony >= 0.6 else '✗'}** |

## Composition

- **Files:** {report.total_files}
- **Functions:** {report.total_functions}
- **Classes:** {report.total_classes}

## Deficit Distribution

| Dimension | Files with Deficit |
|-----------|-------------------|
| Love | {report.files_with_L_deficit} |
| Justice | {report.files_with_J_deficit} |
| Power | {report.files_with_P_deficit} |
| Wisdom | {report.files_with_W_deficit} |

## Recommendations

"""
        for rec in report.recommended_actions:
            md += f"- {rec}\n"
        
        if self.breathing_session:
            md += f"""

## Breathing Session

- **Cycles:** {self.breathing_session.cycles_completed}
- **Files Modified:** {self.breathing_session.total_files_modified}
- **Solutions Applied:** {self.breathing_session.total_solutions_applied}
- **Harmony Change:** {self.breathing_session.harmony_improvement:+.3f}
"""
        
        if self.history:
            md += f"""

## History

| Timestamp | Cycles | Harmony Before | Harmony After | Improvement |
|-----------|--------|----------------|---------------|-------------|
"""
            for entry in self.history[-5:]:  # Last 5 entries
                md += f"| {entry['timestamp'].strftime('%Y-%m-%d %H:%M')} | {entry['cycles']} | {entry['harmony_before']:.3f} | {entry['harmony_after']:.3f} | {entry['harmony_after'] - entry['harmony_before']:+.3f} |\n"
        
        md += """

---
*Generated by Autopoiesis Engine v1.0.0*
"""
        
        return md
    
    def save_report(self, output_path: Optional[str] = None):
        """Save report to file."""
        if output_path is None:
            output_path = self.target_path / "AUTOPOIESIS_REPORT.md"
        
        with open(output_path, 'w') as f:
            f.write(self.report())
        
        print(f"Report saved to: {output_path}")


# Convenience function
def autopoiesis(path: str, cycles: int = 8, dry_run: bool = False) -> AutopoiesisEngine:
    """
    Convenience function to run autopoiesis on a codebase.
    
    Args:
        path: Path to directory or file
        cycles: Number of breathing cycles
        dry_run: If True, don't modify files
        
    Returns:
        AutopoiesisEngine with results
        
    Usage:
        engine = autopoiesis("./my_package", cycles=8)
        print(engine.status())
    """
    engine = AutopoiesisEngine(path, dry_run)
    engine.breathe(cycles)
    return engine
