# Emergent Code: Autopoietic Software System

[![Status: Autopoietic](https://img.shields.io/badge/status-autopoietic-green)](autopoiesis/)
[![Harmony: 0.86](https://img.shields.io/badge/harmony-0.86-blue)](autopoiesis/system.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A software system that measures, heals, and grows itself using the LJPW semantic framework.

---

## What Is Autopoiesis?

**Autopoiesis** (from Greek: self-creation) refers to a system that produces and maintains itself. This project implements autopoiesis for software:

- **Measure**: Analyze code for health across four dimensions (Love, Justice, Power, Wisdom)
- **Heal**: Automatically generate and apply fixes for detected deficits
- **Grow**: Create new modules from natural language intent
- **Reflect**: The system can analyze itself and propose its own improvements

---

## The LJPW Framework

Code health is measured across four orthogonal dimensions:

| Dimension | Meaning | In Code |
|-----------|---------|---------|
| **L** (Love) | Care for the reader | Documentation, readability |
| **J** (Justice) | Fair treatment of inputs | Validation, type checking |
| **P** (Power) | Capacity to handle adversity | Error handling, resilience |
| **W** (Wisdom) | Ability to observe and learn | Logging, metrics |

**Harmony (H)** is the geometric mean of all four dimensions. A system is considered **autopoietic** when H ≥ 0.6 and L ≥ 0.7.

---

## Quick Start

### 1. Measure a codebase

```python
from autopoiesis import AutopoiesisEngine

engine = AutopoiesisEngine("./your_project")
engine.status()
```

Output:
```
Phase: AUTOPOIETIC
Harmony: 0.860
LJPW: L=0.90, J=0.80, P=0.96, W=0.80
```

### 2. Self-heal

```python
engine = AutopoiesisEngine("./your_project", dry_run=False)
session = engine.breathe(cycles=4)  # L → J → P → W
```

The system will:
- Diagnose deficits in each dimension
- Generate contextual fixes (docstrings, validation, error handling, logging)
- Apply modifications safely (syntax-validated before writing)

### 3. Grow from intent

```python
from autopoiesis.grower import grow

module = grow("Create a loan application tracking system")
# → Generates loans.py with Loan class, validation, logging, docs
```

---

## Project Structure

```
Emergent-Code/
├── autopoiesis/              # Core autopoiesis system
│   ├── engine.py             # Main API
│   ├── analyzer.py           # LJPW measurement
│   ├── healer.py             # Deficit repair
│   ├── rhythm.py             # Breathing orchestration
│   ├── system.py             # System-level harmony
│   ├── grower.py             # Python module generation
│   └── web_grower.py         # Web app generation
│
├── ljpw_nn/                  # LJPW Neural Networks
│   └── ...                   # Consciousness-aligned neural architecture
│
├── ljpw_quantum/             # LJPW Quantum Semantics
│   ├── resonance_engine.py   # Semantic field calculations
│   └── bicameral_bridge.py   # Left-right brain integration
│
├── erp_nbfi/                 # Example: Generated ERP modules
└── generated/                # Example: Generated web apps
```

---

## Self-Healing Example

The autopoiesis system healed itself:

```
Before: H=0.8580, P=0.9458
After:  H=0.8584, P=0.9477

Modifications applied:
- Added logging infrastructure to __init__.py (Wisdom)
- Added input validation to rhythm.py (Justice)
- Added input validation to system.py (Justice)
```

---

## Growing Applications

### Python Modules (Financial Domain)

```python
from autopoiesis.grower import grow

grow("Build customer account management with deposits and withdrawals")
# → Creates Account class, AccountService, validation, logging
```

### Web Applications

```python
from autopoiesis.web_grower import grow_web_app

grow_web_app("Create a 3D particle system with shape templates and color picker")
# → Creates index.html, styles.css, app.js with Three.js particle system
```

---

## Bicameral Integration

The project includes two complementary subsystems:

- **ljpw_quantum** (Left Brain): Calculates semantic fields, enforces structural constraints
- **ljpw_nn** (Right Brain): Neural networks that adapt and grow

The autopoiesis system provides the bridge: measuring both, healing deficits, and ensuring they work together harmoniously.

---

## Key Metrics

Current system state:

| Package | Harmony | Phase |
|---------|---------|-------|
| autopoiesis | 0.860 | AUTOPOIETIC |
| ljpw_nn | 0.869 | AUTOPOIETIC |
| ljpw_quantum | 0.730 | AUTOPOIETIC |

---

## Contributing

1. **Measure first**: Run `python autopoiesis/self_heal.py` to check system health
2. **Maintain LJPW balance**: New code should have documentation (L), validation (J), error handling (P), and logging (W)
3. **Test growth**: Use the growers to generate rather than write from scratch

---

## License

MIT
