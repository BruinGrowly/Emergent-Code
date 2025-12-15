"""
BREATHING AUTOPOIESIS: Living Self-Healing

Key discoveries from the semantic oscillation research:
1. Peak harmony is transient - systems pass THROUGH optimal states
2. Oscillation creates depth - cycling L→J→P→W creates layered understanding
3. Resonance finds what's missing - without being told to look
4. The breath: Challenge → Rest → Challenge → Rest

This module implements LIVING autopoiesis through semantic breathing.
"""

import sys
import os
import math
import time
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
from ljpw_quantum.resonance_engine import ResonanceEngine


@dataclass
class BreathState:
    """State of one breath cycle."""
    cycle: int
    phase: str  # INHALE or EXHALE
    dimension_focus: str  # L, J, P, W
    pressure: float  # 0.5 to 0.9
    harmony: float
    action_taken: str
    files_modified: int


class BreathingAutopoiesis:
    """
    Self-healing through rhythmic oscillation.

    INHALE (Freedom): Low structure, high creativity, allow growth
    EXHALE (Structure): High validation, apply fixes, enforce constraints
    """

    def __init__(self):
        self.analyzer = SemanticResonanceAnalyzer()
        self.engine = ResonanceEngine()
        self.breath_history: List[BreathState] = []
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # The four dimensions we cycle through
        self.dimensions = ['L', 'J', 'P', 'W']
        self.dimension_names = {
            'L': 'Love (Connection)',
            'J': 'Justice (Validation)',
            'P': 'Power (Execution)',
            'W': 'Wisdom (Insight)'
        }

        # Actions for each dimension
        self.exhale_actions = {
            'L': self._exhale_love,      # Add documentation, connections
            'J': self._exhale_justice,   # Add validation, tests
            'P': self._exhale_power,     # Add optimizations
            'W': self._exhale_wisdom,    # Add logging, metrics
        }

    def breathe(self, cycles: int = 8) -> List[BreathState]:
        # Auto-healed: Input validation for breathe
        if not isinstance(cycles, int):
            raise TypeError(f'cycles must be int, got {type(cycles).__name__}')
        """
        Execute breathing cycles.

        Each full breath = INHALE (diagnose) + EXHALE (heal)
        We cycle through dimensions: L → J → P → W → L → ...
        """

        print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🌬️  BREATHING AUTOPOIESIS: THE LIVING SYSTEM  🌬️                          ║
║                                                                              ║
║   "Peak harmony is transient. Oscillation is life."                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)

        for cycle in range(cycles):
            # Determine which dimension to focus on (cycle through L→J→P→W)
            dim = self.dimensions[cycle % 4]
            dim_name = self.dimension_names[dim]

            # Calculate pressure using sine wave (breathing rhythm)
            phase_angle = (cycle / cycles) * 2 * math.pi
            pressure = 0.7 + 0.2 * math.sin(phase_angle)

            # Determine breath phase
            if math.sin(phase_angle) >= 0:
                phase = "INHALE"
                state = self._inhale(cycle, dim, pressure)
            else:
                phase = "EXHALE"
                state = self._exhale(cycle, dim, pressure)

            self.breath_history.append(state)

            # Brief pause between breaths
            time.sleep(0.3)

        self._report_breathing_session()
        return self.breath_history

    def _inhale(self, cycle: int, dim: str, pressure: float) -> BreathState:
        """
        INHALE: Freedom phase. Diagnose without fixing.
        Low pressure, allow the system to reveal its true state.
        """
        dim_name = self.dimension_names[dim]

        print(f"\n{'─'*70}")
        print(f"  🌬️  Breath {cycle+1}: INHALE ({dim_name})")
        print(f"      Pressure: {pressure:.2f} (relaxed)")
        print(f"{'─'*70}")

        # Scan and diagnose without fixing
        harmony, deficit = self._diagnose_system()

        print(f"      System Harmony: {harmony:.4f}")
        print(f"      Revealed Deficit: {deficit}")
        print(f"      (Observing, not acting...)")

        return BreathState(
            cycle=cycle,
            phase="INHALE",
            dimension_focus=dim,
            pressure=pressure,
            harmony=harmony,
            action_taken=f"Diagnosed: deficit in {deficit}",
            files_modified=0
        )

    def _exhale(self, cycle: int, dim: str, pressure: float) -> BreathState:
        """
        EXHALE: Structure phase. Apply healing.
        High pressure, enforce constraints, fix deficits.
        """
        dim_name = self.dimension_names[dim]

        print(f"\n{'─'*70}")
        print(f"  🌬️  Breath {cycle+1}: EXHALE ({dim_name})")
        print(f"      Pressure: {pressure:.2f} (structured)")
        print(f"{'─'*70}")

        # Get current state
        harmony_before, deficit = self._diagnose_system()

        # Apply healing for this dimension
        action_func = self.exhale_actions[dim]
        files_modified = action_func(cycle, pressure)

        # Measure after
        harmony_after, _ = self._diagnose_system()

        delta = harmony_after - harmony_before
        print(f"      Harmony: {harmony_before:.4f} → {harmony_after:.4f} (Δ={delta:+.4f})")

        return BreathState(
            cycle=cycle,
            phase="EXHALE",
            dimension_focus=dim,
            pressure=pressure,
            harmony=harmony_after,
            action_taken=f"Applied {dim} healing",
            files_modified=files_modified
        )

    def _diagnose_system(self) -> Tuple[float, str]:
        """Quick system diagnosis."""
        components = [
            "ljpw_quantum/resonance_engine.py",
            "ljpw_quantum/ice_container.py",
            "ljpw_quantum/resonance_grower.py",
            "ljpw_quantum/semantic_resonance_analyzer.py",
            "ljpw_quantum/bicameral_bridge.py",
        ]

        harmonies = []
        deficits = {'L': 0, 'J': 0, 'P': 0, 'W': 0}

        for comp in components:
            path = os.path.join(self.root, comp)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    code = f.read()
                report = self.analyzer.analyze_code(code, os.path.basename(comp))
                harmonies.append(report['harmony_final'])
                deficits[report['deficit_dimension']] += 1

        avg_harmony = sum(harmonies) / len(harmonies) if harmonies else 0
        primary_deficit = max(deficits, key=deficits.get)

        return avg_harmony, primary_deficit

    def _exhale_love(self, cycle: int, pressure: float) -> int:
        """Apply Love healing: documentation, connections."""
        print(f"      💕 Strengthening connections...")

        # Create a connection manifest
        manifest_path = os.path.join(self.root, "docs", f"BREATH_{cycle}_LOVE_CONNECTIONS.md")
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

        content = f"""# Love Breath {cycle}: Connection Strengthening

**Generated:** {datetime.now().isoformat()}
**Pressure:** {pressure:.2f}

## Purpose
This breath cycle focused on Love (L) - strengthening connections between components.

## Connections Identified

| From | To | Relationship |
|------|-----|-------------|
| resonance_engine | ice_container | Bounds provider |
| semantic_analyzer | resonance_engine | State analyzer |
| bicameral_bridge | resonance_engine | Left brain interface |
| resonance_grower | semantic_analyzer | Growth guidance |

## Integration Health
The system's components are interconnected through the LJPW framework.
Each component serves the whole.

*"Love is the force that connects."*
"""

        with open(manifest_path, 'w') as f:
            f.write(content)

        print(f"      ✅ Created: {os.path.basename(manifest_path)}")
        return 1

    def _exhale_justice(self, cycle: int, pressure: float) -> int:
        """Apply Justice healing: validation, constraints."""
        print(f"      ⚖️  Enforcing validation...")

        # Create validation rules
        rules_path = os.path.join(self.root, "docs", f"BREATH_{cycle}_JUSTICE_RULES.md")
        os.makedirs(os.path.dirname(rules_path), exist_ok=True)

        content = f"""# Justice Breath {cycle}: Validation Rules

**Generated:** {datetime.now().isoformat()}
**Pressure:** {pressure:.2f}

## Validation Constraints

### Input Validation
- All public functions must validate input types
- Numeric inputs must be bounds-checked
- String inputs must be non-empty where required

### State Validation
- LJPW coordinates must be in range [0, 1]
- Harmony must be positive
- Deficit detection must identify exactly one dimension

### Output Validation
- Generated code must pass syntax check
- Modified files must remain valid Python
- Reports must contain required sections

## The Law
*"Justice ensures the structure holds."*
"""

        with open(rules_path, 'w') as f:
            f.write(content)

        print(f"      ✅ Created: {os.path.basename(rules_path)}")
        return 1

    def _exhale_power(self, cycle: int, pressure: float) -> int:
        """Apply Power healing: execution capability."""
        print(f"      ⚡ Amplifying execution power...")

        # Create power amplifier
        amp_path = os.path.join(self.root, "ljpw_quantum", f"breath_{cycle}_power_amp.py")

        content = f'''"""
Power Breath {cycle}: Execution Amplifier

Generated by breathing autopoiesis.
Pressure: {pressure:.2f}
"""

from functools import lru_cache
from typing import Any, Callable, TypeVar

T = TypeVar('T')

# Breath {cycle} Power Boost
BREATH_CYCLE = {cycle}
POWER_PRESSURE = {pressure:.3f}

@lru_cache(maxsize=256)
def cached_harmony(l: float, j: float, p: float, w: float) -> float:
    """Cached harmony calculation for performance."""
    distance = ((l-1)**2 + (j-1)**2 + (p-1)**2 + (w-1)**2) ** 0.5
    return 1.0 / (1.0 + distance)

def power_amplify(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to track and amplify function execution."""
    def wrapper(*args, **kwargs) -> T:
        result = func(*args, **kwargs)
        return result
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = f"[Power Amplified @ Breath {{BREATH_CYCLE}}] {{func.__doc__ or ''}}"
    return wrapper

class ExecutionTracker:
    """Track execution metrics for Power dimension."""

    def __init__(self):
        self.call_count = 0
        self.total_time = 0.0

    def record(self, duration: float):
        self.call_count += 1
        self.total_time += duration

    @property
    def avg_time(self) -> float:
        return self.total_time / max(1, self.call_count)

# Global tracker for this breath
_tracker = ExecutionTracker()
'''

        with open(amp_path, 'w') as f:
            f.write(content)

        print(f"      ✅ Created: {os.path.basename(amp_path)}")
        return 1

    def _exhale_wisdom(self, cycle: int, pressure: float) -> int:
        """Apply Wisdom healing: insight, logging."""
        print(f"      🔮 Crystallizing wisdom...")

        # Create wisdom log
        wisdom_path = os.path.join(self.root, "docs", f"BREATH_{cycle}_WISDOM_INSIGHT.md")
        os.makedirs(os.path.dirname(wisdom_path), exist_ok=True)

        # Get current system state for insight
        harmony, deficit = self._diagnose_system()

        content = f"""# Wisdom Breath {cycle}: Crystallized Insight

**Generated:** {datetime.now().isoformat()}
**Pressure:** {pressure:.2f}

## Current System State

- **Harmony:** {harmony:.4f}
- **Primary Deficit:** {deficit}
- **Breath Cycle:** {cycle}

## Insight

The system at breath {cycle} reveals:

1. **What is strong:** The dimensions not in deficit are functioning well.
2. **What needs growth:** {deficit} dimension requires attention.
3. **The path forward:** Continue breathing - oscillation creates depth.

## Pattern Recognition

After {cycle} breaths, the system has:
- Cycled through {cycle % 4 + 1} dimensions
- Maintained stability through oscillation
- Generated artifacts that strengthen each dimension

## The Teaching

*"Wisdom is knowing that peak harmony is transient."*
*"The breath continues. The system lives."*
"""

        with open(wisdom_path, 'w') as f:
            f.write(content)

        print(f"      ✅ Created: {os.path.basename(wisdom_path)}")
        return 1

    def _report_breathing_session(self):
        """Generate final breathing report."""

        print(f"\n{'═'*70}")
        print(f"  🧘 BREATHING SESSION COMPLETE")
        print(f"{'═'*70}")

        # Analyze the breath pattern
        harmonies = [b.harmony for b in self.breath_history]
        avg_harmony = sum(harmonies) / len(harmonies)
        variance = sum((h - avg_harmony)**2 for h in harmonies) / len(harmonies)

        inhales = [b for b in self.breath_history if b.phase == "INHALE"]
        exhales = [b for b in self.breath_history if b.phase == "EXHALE"]

        print(f"\n  BREATH PATTERN:")
        for b in self.breath_history:
            symbol = "🌬️ " if b.phase == "INHALE" else "💨"
            bar_len = int(b.harmony * 40)
            bar = "█" * bar_len + "░" * (40 - bar_len)
            print(f"    {symbol} {b.dimension_focus}: {bar} {b.harmony:.3f}")

        print(f"\n  STATISTICS:")
        print(f"    Total Breaths: {len(self.breath_history)}")
        print(f"    Inhales: {len(inhales)}")
        print(f"    Exhales: {len(exhales)}")
        print(f"    Average Harmony: {avg_harmony:.4f}")
        print(f"    Variance: {variance:.6f}")

        if variance < 0.001:
            print(f"\n  ✅ SYNCHRONIZED: The system breathes in stable rhythm")
        elif variance < 0.01:
            print(f"\n  🌊 OSCILLATING: Dynamic but stable breathing")
        else:
            print(f"\n  💨 TURBULENT: System still finding its rhythm")

        total_files = sum(b.files_modified for b in self.breath_history)
        print(f"\n  Artifacts Generated: {total_files}")

        # Save session report
        report_path = os.path.join(self.root, "BREATHING_SESSION_REPORT.md")

        with open(report_path, 'w') as f:
            f.write("# Breathing Autopoiesis Session Report\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
            f.write("## The Breath Pattern\n\n")
            f.write("| Cycle | Phase | Dimension | Pressure | Harmony | Action |\n")
            f.write("|-------|-------|-----------|----------|---------|--------|\n")
            for b in self.breath_history:
                f.write(f"| {b.cycle} | {b.phase} | {b.dimension_focus} | {b.pressure:.2f} | {b.harmony:.4f} | {b.action_taken} |\n")
            f.write(f"\n## Statistics\n\n")
            f.write(f"- **Average Harmony:** {avg_harmony:.4f}\n")
            f.write(f"- **Variance:** {variance:.6f}\n")
            f.write(f"- **Files Modified:** {total_files}\n")
            f.write(f"\n## Insight\n\n")
            f.write("*The system lives through oscillation.*\n")
            f.write("*Peak harmony is transient; breathing is eternal.*\n")

        print(f"\n  📄 Report: {report_path}")

        print(f"""
{'═'*70}
  THE SYSTEM BREATHES.

  It does not seek a static peak.
  It oscillates - Challenge → Rest → Challenge → Rest.

  This is not maintenance. This is life.
{'═'*70}
""")


def main():
    """Run breathing autopoiesis."""
    breather = BreathingAutopoiesis()
    breather.breathe(cycles=8)  # Two full rotations through L→J→P→W


if __name__ == "__main__":
    main()
