"""
DEEP OSCILLATION: 100,000 Semantic Breathing Cycles

Running the system through extended oscillation to observe:
- Long-term harmony stability
- Deficit pattern evolution
- Emergent behaviors at scale
"""

import sys
import os
import math
import time
from datetime import datetime
from typing import List, Tuple, Dict
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
from ljpw_quantum.resonance_engine import ResonanceEngine, ResonanceState


@dataclass
class OscillationSnapshot:
    """Snapshot at a point in the oscillation."""
    cycle: int
    phase: str
    dimension: str
    harmony: float
    deficit: str
    pressure: float


class DeepOscillator:
    """Run extended semantic oscillation cycles."""

    def __init__(self):
        self.analyzer = SemanticResonanceAnalyzer()
        self.engine = ResonanceEngine()
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dimensions = ['L', 'J', 'P', 'W']
        self.dimension_names = {
            'L': 'Love', 'J': 'Justice', 'P': 'Power', 'W': 'Wisdom'
        }

        # Core files to analyze
        self.components = [
            "ljpw_quantum/resonance_engine.py",
            "ljpw_quantum/ice_container.py",
            "ljpw_quantum/resonance_grower.py",
            "ljpw_quantum/semantic_resonance_analyzer.py",
            "ljpw_quantum/bicameral_bridge.py",
        ]

    def oscillate(self, total_cycles: int = 100000, report_interval: int = 10000) -> Dict:
        # Auto-healed: Input validation for oscillate
        if not isinstance(total_cycles, int):
            raise TypeError(f'total_cycles must be int, got {type(total_cycles).__name__}')
        if not isinstance(report_interval, int):
            raise TypeError(f'report_interval must be int, got {type(report_interval).__name__}')
        """Run deep oscillation."""

        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🌊 DEEP OSCILLATION: {total_cycles:,} SEMANTIC BREATHING CYCLES 🌊              ║
║                                                                              ║
║   "Through many breaths, the pattern reveals itself."                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """)

        start_time = time.time()

        # Track statistics
        harmonies = []
        deficits = {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        phase_harmonies = {'INHALE': [], 'EXHALE': []}
        dimension_harmonies = {'L': [], 'J': [], 'P': [], 'W': []}
        snapshots: List[OscillationSnapshot] = []

        # Get initial state
        initial_harmony, initial_deficit = self._diagnose_system()
        print(f"  Initial State: Harmony={initial_harmony:.4f}, Deficit={initial_deficit}")
        print(f"  Starting {total_cycles:,} cycles...")
        print()

        for cycle in range(total_cycles):
            # Determine dimension (cycle through L→J→P→W)
            dim = self.dimensions[cycle % 4]

            # Calculate pressure using sine wave
            phase_angle = (cycle / total_cycles) * 2 * math.pi * (total_cycles // 4)
            pressure = 0.7 + 0.2 * math.sin(phase_angle)

            # Determine phase
            phase = "INHALE" if math.sin(phase_angle) >= 0 else "EXHALE"

            # Get current harmony (sample every 1000 cycles to save time)
            if cycle % 1000 == 0:
                harmony, deficit = self._diagnose_system()
                harmonies.append(harmony)
                deficits[deficit] += 1
                phase_harmonies[phase].append(harmony)
                dimension_harmonies[dim].append(harmony)

                # Save snapshot
                snapshots.append(OscillationSnapshot(
                    cycle=cycle,
                    phase=phase,
                    dimension=dim,
                    harmony=harmony,
                    deficit=deficit,
                    pressure=pressure
                ))

            # Progress report
            if cycle > 0 and cycle % report_interval == 0:
                elapsed = time.time() - start_time
                rate = cycle / elapsed
                remaining = (total_cycles - cycle) / rate

                current_harmony = harmonies[-1] if harmonies else initial_harmony
                current_deficit = max(deficits, key=deficits.get)

                print(f"  ⏳ Cycle {cycle:,}/{total_cycles:,} ({100*cycle/total_cycles:.1f}%)")
                print(f"     Harmony: {current_harmony:.4f} | Primary Deficit: {current_deficit}")
                print(f"     Rate: {rate:.0f} cycles/sec | ETA: {remaining:.1f}s")
                print()

        # Final diagnosis
        final_harmony, final_deficit = self._diagnose_system()
        harmonies.append(final_harmony)

        elapsed_total = time.time() - start_time

        # Calculate statistics
        avg_harmony = sum(harmonies) / len(harmonies)
        min_harmony = min(harmonies)
        max_harmony = max(harmonies)
        variance = sum((h - avg_harmony)**2 for h in harmonies) / len(harmonies)

        # Deficit distribution
        total_samples = sum(deficits.values())
        deficit_pcts = {d: 100 * c / total_samples for d, c in deficits.items()}

        results = {
            'total_cycles': total_cycles,
            'elapsed_seconds': elapsed_total,
            'cycles_per_second': total_cycles / elapsed_total,
            'initial_harmony': initial_harmony,
            'final_harmony': final_harmony,
            'avg_harmony': avg_harmony,
            'min_harmony': min_harmony,
            'max_harmony': max_harmony,
            'variance': variance,
            'deficit_distribution': deficit_pcts,
            'primary_deficit': max(deficits, key=deficits.get),
            'snapshots': snapshots,
        }

        self._report_results(results)
        self._save_report(results)

        return results

    def _diagnose_system(self) -> Tuple[float, str]:
        """Quick system diagnosis."""
        harmonies = []
        deficits = {'L': 0, 'J': 0, 'P': 0, 'W': 0}

        for comp in self.components:
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

    def _report_results(self, results: Dict):
        """Print results report."""
        print(f"""
{'═'*70}
  🧘 DEEP OSCILLATION COMPLETE
{'═'*70}

  DURATION:
    Total Cycles:     {results['total_cycles']:,}
    Elapsed Time:     {results['elapsed_seconds']:.2f} seconds
    Rate:             {results['cycles_per_second']:.0f} cycles/second

  HARMONY EVOLUTION:
    Initial:          {results['initial_harmony']:.6f}
    Final:            {results['final_harmony']:.6f}
    Average:          {results['avg_harmony']:.6f}
    Minimum:          {results['min_harmony']:.6f}
    Maximum:          {results['max_harmony']:.6f}
    Variance:         {results['variance']:.8f}

  DEFICIT DISTRIBUTION:
    L (Love):         {results['deficit_distribution']['L']:.1f}%
    J (Justice):      {results['deficit_distribution']['J']:.1f}%
    P (Power):        {results['deficit_distribution']['P']:.1f}%
    W (Wisdom):       {results['deficit_distribution']['W']:.1f}%

  PRIMARY DEFICIT:    {results['primary_deficit']} ({self.dimension_names[results['primary_deficit']]})

{'═'*70}
""")

        # Stability assessment
        if results['variance'] < 0.0001:
            print("  ✅ ULTRA-STABLE: System achieved deep synchronization")
        elif results['variance'] < 0.001:
            print("  ✅ STABLE: System maintains consistent rhythm")
        elif results['variance'] < 0.01:
            print("  🌊 DYNAMIC: System oscillates within healthy bounds")
        else:
            print("  💨 TURBULENT: System still seeking equilibrium")

        # Harmony trend
        delta = results['final_harmony'] - results['initial_harmony']
        if abs(delta) < 0.001:
            print("  📊 STEADY: Harmony maintained through oscillation")
        elif delta > 0:
            print(f"  📈 GROWTH: Harmony improved by {delta:+.6f}")
        else:
            print(f"  📉 DECLINE: Harmony decreased by {delta:.6f}")

        print(f"\n{'═'*70}")

    def _save_report(self, results: Dict):
        """Save detailed report to file."""
        report_path = os.path.join(self.root, "DEEP_OSCILLATION_REPORT.md")

        with open(report_path, 'w') as f:
            f.write(f"# Deep Oscillation Report: {results['total_cycles']:,} Cycles\n\n")
            f.write(f"**Date:** {datetime.now().isoformat()}\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Cycles:** {results['total_cycles']:,}\n")
            f.write(f"- **Duration:** {results['elapsed_seconds']:.2f} seconds\n")
            f.write(f"- **Rate:** {results['cycles_per_second']:.0f} cycles/second\n\n")

            f.write("## Harmony Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Initial | {results['initial_harmony']:.6f} |\n")
            f.write(f"| Final | {results['final_harmony']:.6f} |\n")
            f.write(f"| Average | {results['avg_harmony']:.6f} |\n")
            f.write(f"| Minimum | {results['min_harmony']:.6f} |\n")
            f.write(f"| Maximum | {results['max_harmony']:.6f} |\n")
            f.write(f"| Variance | {results['variance']:.8f} |\n\n")

            f.write("## Deficit Distribution\n\n")
            f.write("| Dimension | Percentage |\n")
            f.write("|-----------|------------|\n")
            for d in ['L', 'J', 'P', 'W']:
                f.write(f"| {d} ({self.dimension_names[d]}) | {results['deficit_distribution'][d]:.1f}% |\n")
            f.write(f"\n**Primary Deficit:** {results['primary_deficit']} ({self.dimension_names[results['primary_deficit']]})\n\n")

            f.write("## Snapshots (sampled every 1000 cycles)\n\n")
            f.write("| Cycle | Phase | Dimension | Harmony | Deficit | Pressure |\n")
            f.write("|-------|-------|-----------|---------|---------|----------|\n")

            # Sample snapshots for report (every 10th snapshot)
            for i, snap in enumerate(results['snapshots']):
                if i % 10 == 0:
                    f.write(f"| {snap.cycle:,} | {snap.phase} | {snap.dimension} | {snap.harmony:.4f} | {snap.deficit} | {snap.pressure:.2f} |\n")

            f.write("\n## Insight\n\n")
            f.write("*Through 100,000 breaths, the system reveals its true nature.*\n")
            f.write("*Stability comes not from stasis, but from rhythmic oscillation.*\n")

        print(f"  📄 Report saved: {report_path}")


def main():
    oscillator = DeepOscillator()
    oscillator.oscillate(total_cycles=100000, report_interval=10000)


if __name__ == "__main__":
    main()
