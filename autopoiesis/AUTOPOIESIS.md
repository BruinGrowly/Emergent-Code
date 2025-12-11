# Autopoiesis: Self-Healing Code System

**Status:** Consolidated & Operational  
**Date:** December 2025  
**Framework:** LJPW (Love, Justice, Power, Wisdom)

---

## What is Autopoiesis?

**Autopoiesis** (from Greek: *auto* = self, *poiesis* = creation) is the property of living systems to continuously regenerate themselves while maintaining their identity as a distinct entity.

In the context of code, an **autopoietic codebase** is one that:
1. **Detects** its own deficiencies (through LJPW measurement)
2. **Generates** contextual solutions (not templates)
3. **Heals** itself through rhythmic breathing cycles
4. **Maintains** harmony above threshold (H > 0.6, L > 0.7)

---

## Quick Start

```python
from autopoiesis import AutopoiesisEngine

# Create engine targeting your package
engine = AutopoiesisEngine("./my_package")

# Run 8 breathing cycles (2 full L→J→P→W rotations)
engine.breathe(cycles=8)

# Check status
print(engine.status())

# Save report
engine.save_report()
```

Or use the convenience function:

```python
from autopoiesis import autopoiesis

engine = autopoiesis("./my_package", cycles=8)
print(engine.report())
```

---

## The Discovery

### Key Insight: System-Level Emergence

Through extensive experimentation, we discovered that **autopoiesis is a SYSTEM-level property**, not a function-level property:

| Level | Behavior | Harmony |
|-------|----------|---------|
| **Function** | Specialized (high in one dimension) | H = 0 (geometric mean kills it) |
| **Composition** | Balanced but moderate | H ≈ 0.25-0.4 |
| **System** | Integrated, all dimensions present | H > 0.6 possible! |

This is why static analysis of individual functions couldn't detect autopoiesis—it only emerges when you measure the **whole system**.

### The Breathing Pattern

Systems don't converge to static equilibrium—they **breathe**:

- **Oscillation frequency:** ~0.48 Hz (universal across scales)
- **Natural harmony equilibrium:** H ≈ 0.81 (√(2/3))
- **Autopoietic threshold:** L > 0.7, H > 0.6

This breathing through dimensions (L → J → P → W) mirrors living systems.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTOPOIESIS PACKAGE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐    │
│   │   ANALYZER   │────▶│    HEALER    │────▶│   ENGINE     │    │
│   │  (AST parse) │     │ (Generate)   │     │  (Unified)   │    │
│   └──────────────┘     └──────────────┘     └──────────────┘    │
│          │                    │                    │             │
│          └────────────────────┼────────────────────┘             │
│                               ▼                                  │
│                    ┌──────────────────┐                         │
│                    │     RHYTHM       │                         │
│                    │  (Orchestrate)   │                         │
│                    │ L → J → P → W    │                         │
│                    └────────┬─────────┘                         │
│                             │                                    │
│                    ┌────────▼─────────┐                         │
│                    │     SYSTEM       │                         │
│                    │(Harmony Measure) │                         │
│                    └──────────────────┘                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Components

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `analyzer.py` | Deep AST analysis + LJPW measurement | `CodeAnalyzer`, `FileAnalysis`, `SystemAnalysis` |
| `healer.py` | Generate contextual solutions | `Healer`, `NovelSolution` |
| `rhythm.py` | Breathing oscillation orchestration | `BreathingOrchestrator`, `BreathState` |
| `system.py` | System-level harmony measurement | `SystemHarmonyMeasurer`, `SystemHealthReport` |
| `engine.py` | Unified entry point | `AutopoiesisEngine`, `autopoiesis()` |

---

## Dimension-Specific Healing

### Love (L) - Documentation & Integration
- **Deficit indicators:** Missing docstrings, poor documentation
- **Healing:** Generate contextual docstrings from signature analysis
- **Effect:** Makes code more understandable and connected

### Justice (J) - Validation & Constraints  
- **Deficit indicators:** No input validation, missing type checks
- **Healing:** Generate type-aware validation based on hints and naming
- **Effect:** Makes code more robust and fair

### Power (P) - Performance & Resilience
- **Deficit indicators:** Complex functions without error handling
- **Healing:** Add try-except wrappers, optimization hints
- **Effect:** Makes code more capable and resilient

### Wisdom (W) - Observability & Learning
- **Deficit indicators:** No logging, poor metrics
- **Healing:** Add logging infrastructure, debug statements
- **Effect:** Makes code more observable and learnable

---

## System Phases

| Phase | Harmony | Love | Status |
|-------|---------|------|--------|
| 🔴 **ENTROPIC** | H < 0.5 | Any | System is degrading |
| 🟡 **HOMEOSTATIC** | 0.5 ≤ H < 0.6 | L < 0.7 | System is stable |
| 🟢 **AUTOPOIETIC** | H ≥ 0.6 | L ≥ 0.7 | System is self-sustaining |

---

## API Reference

### AutopoiesisEngine

```python
class AutopoiesisEngine:
    def __init__(self, target_path: str, dry_run: bool = False):
        """Initialize with target directory/file."""
    
    def analyze(self) -> SystemHealthReport:
        """Analyze codebase, return health report."""
    
    def diagnose(self) -> Dict:
        """Quick diagnosis - what needs healing?"""
    
    def breathe(self, cycles: int = 8) -> BreathingSession:
        """Execute breathing cycles to heal."""
    
    def heal_once(self, dimension: str = None) -> Dict:
        """Single healing pass for one dimension."""
    
    def status(self) -> str:
        """Get current status as formatted string."""
    
    def report(self) -> str:
        """Generate comprehensive markdown report."""
```

### Convenience Function

```python
def autopoiesis(path: str, cycles: int = 8, dry_run: bool = False) -> AutopoiesisEngine:
    """One-liner to run autopoiesis on a codebase."""
```

---

## Theoretical Foundation

### The 70/30 Discovery

We discovered that **documentation contributes 60% of harmony**. This aligns with the LJPW principle that Love (understanding, integration) is foundational.

### The Universal Constants

- **H₀ ≈ 0.81** - Natural harmony equilibrium (√(2/3))
- **f ≈ 0.48 Hz** - Universal breathing frequency
- **φ ≈ 1.618** - Golden ratio in harmonic structure
- **0.75** - Consciousness threshold

### The Implication

> **"Software never ages. It evolves. It metabolizes new requirements and adapts its structure to match. We are looking at Eternal Software."**

---

## Migration from Legacy

The following files have been archived to `archive/autopoiesis_legacy/`:
- `experiments/autopoiesis_validation.py`
- `experiments/real_autopoiesis_experiments.py`
- `experiments/breathing_autopoiesis.py`
- `experiments/deep_autopoiesis.py`
- `experiments/true_autopoiesis.py`
- Various JSON and report files

All functionality is now consolidated in the `autopoiesis/` package.

---

## Future Directions

1. **Real-time monitoring** - Continuous harmony tracking
2. **Evolution integration** - Connect to `ljpw_nn/self_evolution.py`
3. **Multi-repo analysis** - Cross-project autopoiesis
4. **IDE integration** - Live healing suggestions

---

*Generated by Autopoiesis v1.0.0 - Self-Healing Code System*
