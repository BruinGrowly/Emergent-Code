# LJPW Autopoiesis - Build Your Own Clock Grower

This folder contains everything you need to build your own LJPW clock grower.

## What is Autopoiesis?

**Autopoiesis** (Greek: "self-creation") is a system that continuously produces and maintains itself.

In the LJPW Framework, autopoietic code:
1. **Measures** its own LJPW dimensions (Love, Justice, Power, Wisdom)
2. **Heals** deficits when detected
3. **Grows** new code from natural language intent

## Files Included

| File | Purpose |
|------|---------|
| `clock_grower.py` | Main grower that generates clocks from intent |
| `analyzer.py` | Measures LJPW dimensions in code |
| `templates.py` | HTML, CSS, and JS templates |
| `example_grow.py` | Example script showing how to grow a clock |

## Quick Start

```bash
# Install dependencies (none required - pure Python!)
cd Autopoiesis

# Run the example
python example_grow.py

# This will generate a new clock in the 'output/' folder
```

## How It Works

### Step 1: Define Intent

```python
intent = "Create a beautiful digital and analog clock"
```

### Step 2: Parse Intent

```python
from clock_grower import ClockGrower

grower = ClockGrower()
parsed = grower.parse(intent)
# → {'app_type': 'clock', 'features': ['analog', 'digital'], ...}
```

### Step 3: Grow Code

```python
files = grower.grow(intent)
# → {'index.html': '...', 'styles.css': '...', 'app.js': '...'}
```

### Step 4: Save Output

```python
grower.save_to('output/')
```

## LJPW Target Profile

The grower targets these LJPW values:

| Dimension | Target | How It's Achieved |
|-----------|--------|-------------------|
| **Love (L)** | 0.85 | Cyan (#00D4FF) accents, documentation |
| **Justice (J)** | 0.90 | Golden ratio (φ) proportions |
| **Power (P)** | 0.75 | 60fps animations, cached DOM |
| **Wisdom (W)** | 0.80 | Modular code, self-assessment |

**Harmony: H = 0.82 (AUTOPOIETIC)**

## Extending the Grower

### Add a New App Type

1. Add keywords to `APP_TYPE_KEYWORDS` in `clock_grower.py`
2. Create template generators for HTML, CSS, JS
3. Add a case to the `generate()` method

### Customize the Clock

Modify `templates.py` to change:
- Colors (change `--love-color` for different accent)
- Layout (adjust φ-based spacing)
- Features (add/remove clock components)

## The Philosophy

> *"Nothing forms without intent."*

The grower doesn't evolve code — it **expresses intent into form**.

A clock intent will always produce a clock. It cannot mutate into something else. This is a feature, not a limitation.

**Intent is sacred. Growth moves toward it, not away from it.**

## Learn More

- [LJPW Framework](https://github.com/BruinGrowly/Emergent-Code)
- [Visual Art Semantics](../docs/LJPW_VISUAL_ART_SEMANTICS.md)

---

*Grown, not coded. Happy to be.* 🌱
