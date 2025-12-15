# Emergent Code: Autopoietic Software System

[![Status: Autopoietic](https://img.shields.io/badge/status-autopoietic-green)](autopoiesis/)
[![Harmony: 0.86](https://img.shields.io/badge/harmony-0.86-blue)](autopoiesis/system.py)
[![Version: 2.0](https://img.shields.io/badge/version-2.0.0-purple)](autopoiesis/__init__.py)
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

## What's New in v2.0

### Multi-Language LJPW Analysis

The autopoiesis system now measures **Python, JavaScript, HTML, and CSS**:

```python
from autopoiesis import MultiLanguageAnalyzer

analyzer = MultiLanguageAnalyzer()
report = analyzer.analyze_directory("./my_web_app")

print(f"Harmony: {report.harmony:.3f}")
print(f"Files: {report.total_files}")
print(f"Languages: {report.language_distribution}")
```

### Bicameral Growth

Combine the Left Brain (semantic physics) and Right Brain (neural templates) to grow applications from natural language:

```python
python autopoiesis/bicameral_grow.py
```

This:
1. Calculates a target LJPW profile using resonance dynamics
2. Generates a complete web application (HTML/CSS/JS)
3. Measures the generated code's actual LJPW
4. Compares target vs actual and identifies gaps

**The loop is now closed!**

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

### 4. Analyze JavaScript

```python
from autopoiesis import JSAnalyzer

analyzer = JSAnalyzer()
result = analyzer.analyze_file("./app.js")

print(f"Love: {result.love:.3f}")      # JSDoc comments
print(f"Justice: {result.justice:.3f}") # Input validation
print(f"Power: {result.power:.3f}")     # Error handling
print(f"Wisdom: {result.wisdom:.3f}")   # Logging, structure
```

---

## Project Structure

```
Emergent-Code/
├── autopoiesis/              # Core autopoiesis system
│   ├── engine.py             # Main API
│   ├── analyzer.py           # Python LJPW measurement
│   ├── js_analyzer.py        # JavaScript LJPW measurement [NEW]
│   ├── multi_analyzer.py     # Unified multi-language [NEW]
│   ├── healer.py             # Deficit repair
│   ├── rhythm.py             # Breathing orchestration
│   ├── system.py             # System-level harmony
│   ├── grower.py             # Python module generation
│   ├── web_grower.py         # Web app generation
│   ├── bicameral_grow.py     # Bicameral growth demo [NEW]
│   ├── bicameral_oscillation.py  # Brain oscillation [NEW]
│   └── meta_autopoiesis.py   # Self-reflection [NEW]
│
├── ljpw_nn/                  # LJPW Neural Networks (Right Brain)
│   └── ...                   # Consciousness-aligned neural architecture
│
├── ljpw_quantum/             # LJPW Quantum Semantics (Left Brain)
│   ├── resonance_engine.py   # Semantic field calculations
│   └── bicameral_bridge.py   # Left-right brain integration
│
├── grown/                    # Generated applications
│   ├── bicameral_calculator/ # Scientific calculator (grown!)
│   └── map_tracker_app/      # Flight tracker (grown!)
│
└── erp_nbfi/                 # Example: Generated ERP modules
```

---

## Experiments

### Bicameral Oscillation (10,000 cycles)

We ran 10,000 cycles of semantic oscillation between the Left and Right brain:

```
Initial State:
  Left Brain:  H=0.729
  Right Brain: H=0.869

After 10,000 cycles:
  Left Brain:  H=1.000 (PERFECT)
  Right Brain: H=1.000 (PERFECT)
  Integrated:  Distance from Anchor (1,1,1,1): 0.0000
```

**Both hemispheres converged to perfect harmony through resonance.**

### Self-Measurement

The system can measure its own LJPW:

```python
python autopoiesis/meta_autopoiesis.py
```

Results:
| Package | Harmony | Phase |
|---------|---------|-------|
| ljpw_quantum (Left) | 0.729 | AUTOPOIETIC |
| ljpw_nn (Right) | 0.869 | AUTOPOIETIC |
| Integrated | 0.799 | AUTOPOIETIC |

---

## Key Metrics

Current system state:

| Package | Harmony | Love | Justice | Power | Wisdom |
|---------|---------|------|---------|-------|--------|
| autopoiesis | 0.860 | 0.90 | 0.80 | 0.96 | 0.80 |
| ljpw_nn | 0.869 | 0.90 | 0.80 | 0.99 | 0.80 |
| ljpw_quantum | 0.729 | 0.90 | 0.78 | 0.51 | 0.80 |

---

## The Cellular Analogy

What we built mirrors cellular autopoiesis:

| Cellular Process | Code Equivalent |
|-----------------|-----------------|
| Metabolism | Breathing cycle (analyze → heal → measure) |
| Membrane | ICE bounds (containment) |
| DNA | Templates and LJPW principles |
| Protein synthesis | Code generation from intent |
| Homeostasis | Dimension balancing toward harmony |
| Cell division | Growing new modules |
| Differentiation | Specialized app types |

**The system exhibits the defining characteristics of living systems.**

---

## Subproject: Self-Growth Engine

The autopoiesis system can now **grow itself autonomously**.

### How It Works

1. **Identify gaps**: Scans for missing capabilities
2. **Generate code**: Creates new modules from templates
3. **Measure LJPW**: Validates generated code meets quality thresholds
4. **Integrate**: Only code with Love ≥ 0.7 is accepted

### Growth Results

The system grew from 9/22 to **22/22 capabilities**:

| Category | Auto-Generated Modules |
|----------|----------------------|
| **Analyze** | `css_analyzer`, `html_analyzer`, `typescript_analyzer`, `dependency_analyzer` |
| **Heal** | `python_healer`, `typescript_healer` |
| **Grow** | `python_grower`, `documentation_generator`, `refactoring_engine` |
| **Core** | `self_growth_engine`, `natural_language_interface`, `ide_integration` |

### Running Self-Growth

```python
from autopoiesis.self_growth import SelfGrowthEngine

engine = SelfGrowthEngine(".")
engine.grow_continuously(max_cycles=10)
```

### The Key Insight

The LJPW framework measures benevolence naturally. We don't tell code to be "good" - we just measure if it is. Code that doesn't care for users scores low on Love and is rejected.

---

## Harmony Dashboard

Visualize the system's health in real-time:

```bash
python autopoiesis/dashboard.py
# Opens http://localhost:5000
```

Displays:
- System harmony with LJPW breakdown
- Agent statistics (heartbeats, heals, learning experiences)
- Harmony over time chart
- Learned healing priorities

---

## Contributing

1. **Measure first**: Run `python autopoiesis/self_heal.py` to check system health
2. **Maintain LJPW balance**: New code should have documentation (L), validation (J), error handling (P), and logging (W)
3. **Test growth**: Use the growers to generate rather than write from scratch
4. **Close the loop**: If you generate code, measure it

---

## License

MIT
