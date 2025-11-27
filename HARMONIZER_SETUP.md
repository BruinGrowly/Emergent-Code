# Python Code Harmonizer Integration

## Overview

This project uses the Python Code Harmonizer to analyze LJPW (Love, Justice, Power, Wisdom) semantic profiles of code. The harmonizer provides the foundation for fractal composition experiments across all abstraction levels.

## Current Status

✅ **Unified Harmonizer Integration** - All experiments use `harmonizer_integration.py`
⏳ **Awaiting Real Harmonizer** - Currently using mock implementation

## Setup Instructions

### Option 1: Use Mock Harmonizer (Current Default)

The project includes a mock harmonizer that returns zero profiles for all code. This allows testing composition logic independently of LJPW analysis.

**No setup required** - Mock harmonizer works out of the box.

### Option 2: Install Real Python Code Harmonizer

To get actual LJPW profiles instead of zeros:

1. **Clone the Python Code Harmonizer repository:**
   ```bash
   cd /home/user/Emergent-Code/
   git clone https://github.com/[USERNAME]/Python-Code-Harmonizer.git Python-Code-Harmonizer
   ```

   Or if you have it locally:
   ```bash
   cp -r /path/to/Python-Code-Harmonizer Python-Code-Harmonizer
   ```

   Note: The integration also supports `Python-Code-Harmonizer-main` for backwards compatibility.

2. **Verify the structure:**
   ```
   Emergent-Code/
   ├── Python-Code-Harmonizer/        (or Python-Code-Harmonizer-main/)
   │   └── harmonizer/
   │       └── main.py  (contains PythonCodeHarmonizer class)
   ├── harmonizer_integration.py
   └── experiments/
   ```

3. **Run experiments:**
   ```bash
   python experiments/composition_discovery.py
   ```

   You should see:
   ```
   [OK] Real Python Code Harmonizer loaded successfully.
   ```

## How It Works

### Unified Integration Module

`harmonizer_integration.py` provides a single point of harmonizer access:

```python
from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE

harmonizer = PythonCodeHarmonizer()

if HARMONIZER_AVAILABLE:
    # Using real harmonizer - get actual LJPW profiles
    profile = harmonizer.analyze_file_content(code)
else:
    # Using mock - composition logic still works with zero profiles
    profile = harmonizer.analyze_file_content(code)
```

### Automatic Fallback

The integration automatically:
1. **Attempts** to load the real harmonizer from `Python-Code-Harmonizer-main/`
2. **Falls back** to mock harmonizer if real one is unavailable
3. **Provides** consistent API regardless of which implementation is active

### Files Updated

All experiment files now use the unified integration:

- ✅ `experiments/composition_discovery.py` (Level 1)
- ✅ `experiments/fractal_composition_level2.py` (Level 2)
- ✅ `experiments/class_discovery_enhanced.py` (Level 2 enhanced)
- ✅ `experiments/fractal_level3_modules.py` (Level 3)
- ✅ `experiments/fractal_level4_packages.py` (Level 4)
- ✅ `experiments/fractal_level5_applications.py` (Level 5)
- ✅ `experiments/fractal_level6_platforms.py` (Level 6)

## Benefits

### With Mock Harmonizer
- ✅ Test composition algebra independently
- ✅ Validate discovery patterns
- ✅ Prove fractal structure
- ✅ No external dependencies

### With Real Harmonizer
- ✅ Get actual LJPW semantic profiles
- ✅ Measure real composition accuracy
- ✅ Empirically validate composition predictions
- ✅ Calibrate composition coefficients

## Troubleshooting

### Import Error

**Problem:**
```
ImportError: No module named 'harmonizer.main'
```

**Solution:**
Check that `Python-Code-Harmonizer-main/harmonizer/main.py` exists and contains `PythonCodeHarmonizer` class.

### Missing Dependencies Error

**Problem:**
```
[WARNING] Failed to load real harmonizer: No module named 'matplotlib'
[WARNING] Failed to load real harmonizer: No module named 'black'
```

**Reason:**
The Python Code Harmonizer requires several dependencies that may not be installed.

**Solution:**
Install all required dependencies:
```bash
pip install -r requirements.txt
```

The harmonizer requires:
- matplotlib (for LJPW visualizations)
- numpy (for numerical computations)
- black (for code formatting)
- astunparse (for AST processing)
- tomli (for TOML parsing)
- pyyaml (for YAML configuration)

All of these are now included in `requirements.txt`.

### Wrong Profiles

**Problem:**
All LJPW values are 0.0

**Reason:**
You're using the mock harmonizer (which is normal if real harmonizer isn't installed).

**Solution:**
To get real profiles, install the Python Code Harmonizer as described above.

### Path Issues

**Problem:**
```
[INFO] Python-Code-Harmonizer not found.
[INFO] Expected location: /home/user/Emergent-Code/Python-Code-Harmonizer
```

**Solution:**
The harmonizer must be in the project root as either `Python-Code-Harmonizer/` or `Python-Code-Harmonizer-main/`, not in `experiments/` or elsewhere.

## Next Steps

Once the real Python Code Harmonizer is installed:

1. **Run baseline experiments** to get actual LJPW profiles
2. **Calibrate composition rules** with empirical data
3. **Validate predictions** against real measurements
4. **Refine coupling constants** (κ_LJ, κ_LP, etc.) based on observations

This will transform the fractal composition proof from **theoretical** (with mock data) to **empirical** (with real LJPW analysis).

## Support

If you need help obtaining or installing the Python Code Harmonizer, please contact the project maintainers.

---

**Current Configuration:**
- Mock Harmonizer: Available (fallback) ✅
- Real Harmonizer: Active ✅
- All Experiments: Updated ✅
- Dependencies: Installed ✅
