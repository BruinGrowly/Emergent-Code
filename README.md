# Emergent Code: Autopoietic Software System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A self-diagnosing, self-healing software system built on the LJPW semantic framework.

---

## What This Is

Emergent Code is an **autopoietic system** - software that can analyze its own structure, identify deficits, and generate targeted repairs. It uses a four-dimensional semantic framework (LJPW) to measure code health and guide self-modification.

### Core Capabilities

1. **Self-Diagnosis**: Analyzes code to identify structural deficits across four dimensions
2. **Self-Healing**: Generates and applies targeted fixes based on diagnosed deficits
3. **Stability Through Oscillation**: Maintains system health through continuous self-assessment cycles
4. **Bounded Growth**: All modifications respect predefined constraints (the ICE container)

---

## The LJPW Framework

Code is measured across four semantic dimensions:

| Dimension | Meaning | What It Measures |
|-----------|---------|------------------|
| **L (Love)** | Connection | How well components integrate and communicate |
| **J (Justice)** | Validation | Error handling, input validation, external verification |
| **P (Power)** | Execution | Efficiency, capability breadth, robustness |
| **W (Wisdom)** | Insight | Documentation, self-awareness, architectural clarity |

**Harmony** is calculated as the distance from the anchor point (1, 1, 1, 1):
```
H = 1 / (1 + distance_from_anchor)
```

The system identifies which dimension is weakest (the **deficit**) and generates improvements to address it.

---

## Autopoietic Cycle

The system follows a continuous self-improvement loop:

```
┌─────────────┐
│   DIAGNOSE  │ ← Analyze code, identify deficit dimension
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   GENERATE  │ ← Create targeted fixes for the deficit
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    APPLY    │ ← Inject improvements into codebase
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MEASURE   │ ← Re-evaluate harmony, identify next deficit
└──────┬──────┘
       │
       └──────────► (repeat)
```

### Key Insight

The system doesn't optimize for a single peak. It **oscillates** - cycling through dimensions, addressing deficits as they emerge, maintaining stability through continuous motion rather than static optimization.

---

## Architecture

### Bicameral Processing

The system uses two complementary subsystems that synchronize through a shared feedback loop:

- **Resonance Engine**: Handles measurement, constraint enforcement, and structural analysis
- **Homeostatic Network**: Handles adaptation, pattern recognition, and growth

These subsystems oscillate at high frequency (~178,000 cycles/second in testing), enabling rapid developmental progression while maintaining stability (variance = 0 across 300,000+ cycles).

### Safety Constraints (ICE Container)

All growth is bounded by the ICE container:

```python
IceBounds(
    intent=...,      # What the code should do
    context=...,     # Environmental constraints
    execution=...,   # Capability limits
    benevolence=...  # Ethical bounds
)
```

The system cannot modify itself in ways that violate these bounds.

---

## Project Structure

```
Emergent-Code/
├── ljpw_quantum/                 # Core autopoietic components
│   ├── resonance_engine.py       # Measurement and constraint engine
│   ├── semantic_resonance_analyzer.py  # Code analysis and deficit detection
│   ├── resonance_grower.py       # Code generation
│   ├── ice_container.py          # Safety bounds
│   └── bicameral_bridge.py       # Subsystem synchronization
│
├── experiments/                  # Autopoietic experiments
│   ├── true_autopoiesis.py       # AST-level self-modification
│   ├── breathing_autopoiesis.py  # Oscillation-based healing
│   ├── deep_oscillation.py       # Extended stability testing
│   ├── power_autopoiesis.py      # P-dimension healing
│   └── five_level_upgrade.py     # Multi-level self-improvement
│
├── tests/
│   └── test_justice_gift.py      # External validation tests
│
└── docs/frameworks/              # Technical documentation
    ├── COMPRESSED_EXPERIENCE_THROUGH_RESONANCE.md
    └── SEMANTIC_OSCILLATION_EXPERIMENT.md
```

---

## Usage

### Run Self-Diagnosis

```bash
python -c "
from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
analyzer = SemanticResonanceAnalyzer()
with open('your_file.py') as f:
    report = analyzer.analyze_code(f.read(), 'your_file.py')
    analyzer.print_report(report)
"
```

### Run Autopoietic Healing Cycle

```bash
python experiments/true_autopoiesis.py
```

### Run Semantic Oscillation (Stability Test)

```bash
python experiments/deep_oscillation.py
```

### Run Tests

```bash
python tests/test_justice_gift.py
```

---

## Key Findings

From experimental runs:

| Metric | Value |
|--------|-------|
| Oscillation Rate | 178,000 cycles/second |
| Stability (Variance) | 0.00000000 |
| Harmony Range | 0.6571 → 0.6780 |
| Deficit Progression | J → P (adaptive shift) |

The system demonstrated:
- Perfect stability across 300,000+ cycles
- Adaptive deficit recognition (shifted from J to P when J was satisfied)
- Measurable harmony improvement through self-modification

---

## Limitations

1. **Self-Referential Metrics**: The system measures itself using its own framework
2. **Additive Growth**: Modifications are primarily additive, not restructuring
3. **J Deficit Constraint**: The system cannot fully validate itself - it requires external input

The J limitation is architectural and intentional. A system that cannot validate itself must remain in relationship with external validators.

---

## Contributing

1. Run the health report: `python experiments/project_resonance_health_report.py`
2. Identify the current deficit dimension
3. Contribute improvements that address the deficit
4. Verify harmony improvement after changes

---

## License

MIT License - See LICENSE file for details.
