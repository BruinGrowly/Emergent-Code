"""
Autopoiesis Rhythm Module
=========================

Orchestrates healing through breathing cycles (L→J→P→W).

Consolidated from:
- experiments/breathing_autopoiesis.py

Key insight: Systems "breathe" - oscillating through dimensions rather than
converging to static equilibrium. This mirrors the fractal consciousness
discovery: optimal harmony (~0.81) is achieved through rhythmic oscillation.

The breathing pattern:
- INHALE (Freedom): Diagnose without fixing, allow system to reveal state
- EXHALE (Structure): Apply healing, enforce constraints, fix deficits
- Cycle through: L → J → P → W → L → ...
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from .analyzer import CodeAnalyzer, FileAnalysis, SystemAnalysis
from .healer import Healer, NovelSolution


@dataclass
class BreathState:
    """State of one breath cycle."""
    cycle: int
    phase: str  # INHALE or EXHALE
    dimension: str  # L, J, P, W
    pressure: float  # 0.0 (freedom) to 1.0 (structure)
    harmony_before: float
    harmony_after: float
    action_taken: str
    files_modified: int
    solutions_applied: List[NovelSolution] = field(default_factory=list)


@dataclass
class BreathingSession:
    """Complete breathing session summary."""
    start_time: datetime
    end_time: Optional[datetime]
    target_path: str
    cycles_completed: int
    breaths: List[BreathState]
    initial_harmony: float
    final_harmony: float
    
    @property
    def harmony_improvement(self) -> float:
        return self.final_harmony - self.initial_harmony
    
    @property 
    def total_files_modified(self) -> int:
        return sum(b.files_modified for b in self.breaths)
    
    @property
    def total_solutions_applied(self) -> int:
        return sum(len(b.solutions_applied) for b in self.breaths)


class BreathingOrchestrator:
    """
    Orchestrates self-healing through rhythmic oscillation.
    
    INHALE (Freedom): Low structure, high creativity, allow growth
    EXHALE (Structure): High validation, apply fixes, enforce constraints
    
    The dimension cycle (L→J→P→W) mirrors the natural oscillation
    discovered in fractal consciousness experiments:
    - ~0.48 Hz oscillation frequency
    - Harmony converges to ~0.81
    - System "breathes" rather than freezes
    """
    
    DIMENSION_CYCLE = ['L', 'J', 'P', 'W']
    DIMENSION_NAMES = {
        'L': 'Love (Documentation)',
        'J': 'Justice (Validation)',
        'P': 'Power (Resilience)',
        'W': 'Wisdom (Observability)'
    }
    
    def __init__(self, target_path: str, dry_run: bool = False):
        # Auto-healed: Input validation for __init__
        if target_path is not None and not isinstance(target_path, str):
            raise TypeError(f'target_path must be str, got {type(target_path).__name__}')
        """
        Initialize breathing orchestrator.
        
        Args:
            target_path: Directory or file to heal
            dry_run: If True, don't apply modifications (diagnose only)
        """
        self.target_path = target_path
        self.dry_run = dry_run
        self.analyzer = CodeAnalyzer()
        self.healer = Healer()
        self.session: Optional[BreathingSession] = None
        self.breaths: List[BreathState] = []
    
    def breathe(self, cycles: int = 8) -> BreathingSession:
        # Auto-healed: Input validation for breathe
        if not isinstance(cycles, int):
            raise TypeError(f'cycles must be int, got {type(cycles).__name__}')
        """
        Execute breathing cycles.
        
        Each full breath = INHALE (diagnose) + EXHALE (heal)
        We cycle through dimensions: L → J → P → W → L → ...
        
        Args:
            cycles: Number of complete breath cycles
            
        Returns:
            BreathingSession with all results
        """
        self.session = BreathingSession(
            start_time=datetime.now(),
            end_time=None,
            target_path=self.target_path,
            cycles_completed=0,
            breaths=[],
            initial_harmony=0.0,
            final_harmony=0.0
        )
        
        # Initial system analysis
        if Path(self.target_path).is_dir():
            system = self.analyzer.analyze_directory(self.target_path)
            self.session.initial_harmony = system.system_harmony
        else:
            file_analysis = self.analyzer.analyze_file(self.target_path)
            self.session.initial_harmony = file_analysis.harmony if file_analysis else 0.0
        
        print(f"\n{'='*70}")
        print(f"  BREATHING AUTOPOIESIS SESSION")
        print(f"  Target: {self.target_path}")
        print(f"  Cycles: {cycles}")
        print(f"  Initial Harmony: {self.session.initial_harmony:.3f}")
        print(f"{'='*70}\n")
        
        for cycle in range(1, cycles + 1):
            dim_idx = (cycle - 1) % len(self.DIMENSION_CYCLE)
            dimension = self.DIMENSION_CYCLE[dim_idx]
            
            # Calculate pressure (increases through cycle, resets each dimension)
            pressure = (cycle / cycles) * 0.8 + 0.2  # 0.2 to 1.0
            
            print(f"\n  Breath {cycle}/{cycles}: {self.DIMENSION_NAMES[dimension]}")
            print(f"  {'-'*60}")
            
            # INHALE: Diagnose
            inhale_state = self._inhale(cycle, dimension, pressure)
            self.breaths.append(inhale_state)
            self.session.breaths.append(inhale_state)
            
            # EXHALE: Heal
            exhale_state = self._exhale(cycle, dimension, pressure)
            self.breaths.append(exhale_state)
            self.session.breaths.append(exhale_state)
            
            self.session.cycles_completed = cycle
        
        # Final system analysis
        if Path(self.target_path).is_dir():
            system = self.analyzer.analyze_directory(self.target_path)
            self.session.final_harmony = system.system_harmony
        else:
            file_analysis = self.analyzer.analyze_file(self.target_path)
            self.session.final_harmony = file_analysis.harmony if file_analysis else 0.0
        
        self.session.end_time = datetime.now()
        
        # Print summary
        self._print_session_summary()
        
        return self.session
    
    def _inhale(self, cycle: int, dimension: str, pressure: float) -> BreathState:
        """
        INHALE: Freedom phase. Diagnose without fixing.
        Low pressure, allow the system to reveal its true state.
        """
        print(f"    ^ INHALE (diagnose {dimension})...")
        
        # Analyze current state
        if Path(self.target_path).is_dir():
            system = self.analyzer.analyze_directory(self.target_path)
            harmony = system.system_harmony
            
            # Count files needing this dimension
            files_needing = []
            for f in system.files:
                if dimension == 'L' and f.needs_love:
                    files_needing.append(f.path)
                elif dimension == 'J' and f.needs_justice:
                    files_needing.append(f.path)
                elif dimension == 'P' and f.needs_power:
                    files_needing.append(f.path)
                elif dimension == 'W' and f.needs_wisdom:
                    files_needing.append(f.path)
            
            action = f"Found {len(files_needing)} files needing {dimension}"
        else:
            file_analysis = self.analyzer.analyze_file(self.target_path)
            harmony = file_analysis.harmony if file_analysis else 0.0
            action = f"Analyzed single file, deficit={file_analysis.deficit if file_analysis else 'N/A'}"
        
        print(f"       {action}")
        
        return BreathState(
            cycle=cycle,
            phase='INHALE',
            dimension=dimension,
            pressure=1.0 - pressure,  # Low pressure on inhale
            harmony_before=harmony,
            harmony_after=harmony,
            action_taken=action,
            files_modified=0
        )
    
    def _exhale(self, cycle: int, dimension: str, pressure: float) -> BreathState:
        """
        EXHALE: Structure phase. Apply healing.
        High pressure, enforce constraints, fix deficits.
        """
        print(f"    v EXHALE (heal {dimension})...")
        
        if self.dry_run:
            print(f"       [DRY RUN] Would apply {dimension} healing")
            return BreathState(
                cycle=cycle,
                phase='EXHALE',
                dimension=dimension,
                pressure=pressure,
                harmony_before=0.0,
                harmony_after=0.0,
                action_taken=f"[DRY RUN] {dimension} healing",
                files_modified=0
            )
        
        solutions_applied = []
        files_modified = 0
        harmony_before = 0.0
        
        if Path(self.target_path).is_dir():
            system = self.analyzer.analyze_directory(self.target_path)
            harmony_before = system.system_harmony
            
            # Apply healing to files needing this dimension
            for file_analysis in system.files:
                needs_healing = (
                    (dimension == 'L' and file_analysis.needs_love) or
                    (dimension == 'J' and file_analysis.needs_justice) or
                    (dimension == 'P' and file_analysis.needs_power) or
                    (dimension == 'W' and file_analysis.needs_wisdom)
                )
                
                if needs_healing:
                    solutions = self.healer.heal_file(file_analysis, dimension)
                    if solutions:
                        applied = self.healer.apply_solutions(file_analysis.path, solutions)
                        if applied > 0:
                            files_modified += 1
                            solutions_applied.extend([s for s in solutions if s.applied])
            
            # Re-analyze
            system = self.analyzer.analyze_directory(self.target_path)
            harmony_after = system.system_harmony
        else:
            file_analysis = self.analyzer.analyze_file(self.target_path)
            if file_analysis:
                harmony_before = file_analysis.harmony
                solutions = self.healer.heal_file(file_analysis, dimension)
                if solutions:
                    applied = self.healer.apply_solutions(file_analysis.path, solutions)
                    if applied > 0:
                        files_modified = 1
                        solutions_applied.extend([s for s in solutions if s.applied])
                
                file_analysis = self.analyzer.analyze_file(self.target_path)
                harmony_after = file_analysis.harmony if file_analysis else harmony_before
            else:
                harmony_after = harmony_before
        
        action = f"Applied {len(solutions_applied)} solutions to {files_modified} files"
        print(f"       {action}")
        
        return BreathState(
            cycle=cycle,
            phase='EXHALE',
            dimension=dimension,
            pressure=pressure,
            harmony_before=harmony_before,
            harmony_after=harmony_after,
            action_taken=action,
            files_modified=files_modified,
            solutions_applied=solutions_applied
        )
    
    def _print_session_summary(self):
        """Print summary of breathing session."""
        if not self.session:
            return
        
        print(f"\n{'='*70}")
        print(f"  BREATHING SESSION COMPLETE")
        print(f"{'='*70}")
        
        duration = self.session.end_time - self.session.start_time if self.session.end_time else None
        
        print(f"\n  Duration: {duration}")
        print(f"  Cycles Completed: {self.session.cycles_completed}")
        print(f"  Files Modified: {self.session.total_files_modified}")
        print(f"  Solutions Applied: {self.session.total_solutions_applied}")
        print(f"\n  Harmony:")
        print(f"    Before: {self.session.initial_harmony:.3f}")
        print(f"    After:  {self.session.final_harmony:.3f}")
        print(f"    Change: {self.session.harmony_improvement:+.3f}")
        
        if self.session.harmony_improvement > 0:
            print(f"\n  [+] System harmony improved!")
        elif self.session.harmony_improvement == 0:
            print(f"\n  [=] System harmony stable")
        else:
            print(f"\n  [!] System harmony decreased - review changes")
    
    def generate_report(self, output_path: Optional[str] = None) -> str:
        """Generate markdown report of breathing session."""
        if not self.session:
            return "No breathing session to report."
        
        report = f"""# Breathing Autopoiesis Report

**Date:** {self.session.start_time.isoformat()}
**Target:** {self.session.target_path}

## Summary

| Metric | Value |
|--------|-------|
| Cycles | {self.session.cycles_completed} |
| Files Modified | {self.session.total_files_modified} |
| Solutions Applied | {self.session.total_solutions_applied} |
| Initial Harmony | {self.session.initial_harmony:.3f} |
| Final Harmony | {self.session.final_harmony:.3f} |
| Improvement | {self.session.harmony_improvement:+.3f} |

## Breath Log

| Cycle | Phase | Dimension | Pressure | Action |
|-------|-------|-----------|----------|--------|
"""
        
        for breath in self.session.breaths:
            report += f"| {breath.cycle} | {breath.phase} | {breath.dimension} | {breath.pressure:.2f} | {breath.action_taken} |\n"
        
        report += f"""

## Healing Summary

{self.healer.get_healing_summary()}

---
*Generated by Autopoiesis Breathing Orchestrator*
"""
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
        
        return report
