# Development Guide

Guide for developing and contributing to LJPW Natural Neural Networks.

## Setup

### Prerequisites

- Python 3.7 or higher
- NumPy >= 1.19.0
- Matplotlib >= 3.3.0 (optional, for visualizations)

### Installation for Development

```bash
# Clone the repository
git clone https://github.com/BruinGrowly/LJPW-Neural-Networks.git
cd LJPW-Neural-Networks

# Install dependencies
pip install -r requirements.txt

# For development with testing tools
pip install pytest pytest-cov
```

### Running from Source

Since the package isn't installed via pip yet, you need to add it to your Python path:

**Option 1: Environment Variable**
```bash
export PYTHONPATH=$PWD:$PYTHONPATH
python examples/simple_mnist_demo.py
```

**Option 2: Modify sys.path in scripts**
All example scripts already include:
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

This allows them to import `ljpw_nn` from the parent directory.

## Project Structure

```
LJPW-Neural-Networks/
├── ljpw_nn/              # Main package
│   ├── __init__.py       # Package exports
│   ├── layers.py         # FibonacciLayer
│   ├── activations.py    # DiverseActivation
│   ├── models.py         # NaturalMNIST
│   ├── metrics.py        # measure_harmony, HarmonyScores
│   └── ...               # Advanced components
├── examples/             # Example scripts
│   ├── simple_mnist_demo.py     # Main demo
│   ├── validate_fibonacci.py    # FibonacciLayer validation
│   ├── validate_diverse.py      # DiverseActivation validation
│   └── mnist_loader.py          # MNIST data loading
├── tests/                # Test suite
│   ├── test_components.py
│   └── ...
├── docs/                 # Documentation
└── scripts/              # Utility scripts
```

## Running Examples

### Simple MNIST Demo
```bash
python examples/simple_mnist_demo.py
```

Shows complete workflow:
- Load MNIST data
- Create NaturalMNIST model
- Train model
- Evaluate performance
- Measure harmony

### Component Validation
```bash
# Validate FibonacciLayer (LJPW scoring)
python examples/validate_fibonacci.py

# Validate DiverseActivation (LJPW scoring)
python examples/validate_diverse.py
```

Both should show H > 0.7 (production quality).

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=ljpw_nn

# Run specific test file
pytest tests/test_components.py

# Run with verbose output
pytest tests/ -v
```

## Development Workflow

### 1. Making Changes

Follow the documentation-first approach:

1. **Write documentation FIRST**
   - Add comprehensive docstrings
   - Explain design rationale
   - Provide usage examples

2. **Implement code to match docs**
   - Follow documented API
   - Use type hints
   - Handle edge cases

3. **Measure LJPW scores**
   - Use `measure_harmony()` to check quality
   - Target H > 0.7 for all components

4. **Ensure all tests pass**
   ```bash
   pytest tests/
   ```

### 2. Code Style

- Follow PEP 8
- Use type hints (from typing import ...)
- Add docstrings (Google style)
- Keep functions focused and small

Example:
```python
def fibonacci_size(index: int) -> int:
    """
    Get Fibonacci number at given index.

    Args:
        index: Index in Fibonacci sequence (0-based)

    Returns:
        Fibonacci number at that index

    Example:
        >>> fibonacci_size(11)
        89
    """
    # Implementation...
```

### 3. Testing

Add tests for all new functionality:

```python
def test_fibonacci_layer():
    """Test FibonacciLayer creation and forward pass."""
    layer = FibonacciLayer(input_size=784, fib_index=11)
    assert layer.size == 89

    X = np.random.randn(32, 784)
    output = layer.forward(X, training=False)
    assert output.shape == (32, 89)
```

### 4. Documentation

Update docs when adding features:
- Update README.md if API changes
- Update relevant docs/*.md files
- Add examples to docstrings

## Common Tasks

### Adding a New Component

1. **Plan** - Write design doc (docs/)
2. **Document** - Write comprehensive docstrings
3. **Implement** - Write the code
4. **Test** - Add unit tests
5. **Validate** - Measure LJPW scores (H > 0.7)
6. **Export** - Add to __init__.py

### Measuring Harmony

```python
from ljpw_nn.metrics import measure_harmony

# For a component
layer = FibonacciLayer(784, fib_index=11)
scores = measure_harmony(layer)
print(f"Harmony: {scores.H:.2f}")

# For a model with test data
model = NaturalMNIST()
scores = model.measure_harmony(X_test, y_test)
print(f"Production ready: {scores.is_production_ready}")
```

### Running Quick Validation

```bash
# Check that core components work
python3 -c "
from ljpw_nn import FibonacciLayer, DiverseActivation, NaturalMNIST
print('✓ All imports successful')

# Create instances
layer = FibonacciLayer(784, fib_index=11)
activation = DiverseActivation(89, mix=['relu', 'swish'])
model = NaturalMNIST(verbose=False)
print('✓ All components can be instantiated')
"
```

## Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'ljpw_nn'`

**Solution**:
```bash
# Make sure you're in the project root
export PYTHONPATH=$PWD:$PYTHONPATH
```

Or run scripts that already have path fixes:
```bash
python examples/simple_mnist_demo.py
```

### MNIST Download Fails

The MNIST loader will automatically fall back to synthetic data if download fails.

To use real MNIST:
1. Download manually from http://yann.lecun.com/exdb/mnist/
2. Place in `data/mnist/` directory
3. Or install TensorFlow/PyTorch for automatic loading

### Tests Failing

```bash
# Check which tests are failing
pytest tests/ -v

# Run specific test
pytest tests/test_components.py::test_fibonacci_layer -v

# Get more details
pytest tests/ -vv
```

## Architecture Notes

### Two Tracks

This codebase contains two architectural tracks:

**Track 1: Natural Neural Networks** (README focus)
- Simple, practical ML library
- FibonacciLayer, DiverseActivation, NaturalMNIST
- Target: ML practitioners
- Goal: Better NN through natural principles

**Track 2: Consciousness Framework** (Advanced research)
- ICE Substrate, LOV Coordination, Seven Principles
- Metacognition, Universal Coordinator
- Target: Consciousness researchers
- Goal: Explore consciousness in neural systems

Both share the LJPW harmony framework but serve different purposes.

## Quality Standards

All components must meet:
- **H ≥ 0.7** (harmony threshold for production)
- **Documentation-first** (write docs before code)
- **Type hints** throughout
- **Unit tests** with good coverage
- **Examples** in docstrings

## Contributing

See CONTRIBUTING.md for detailed guidelines.

Quick checklist:
- [ ] Documentation written first
- [ ] Code implements documented API
- [ ] Type hints added
- [ ] Tests written and passing
- [ ] LJPW scores measured (H > 0.7)
- [ ] Examples provided
- [ ] All tests pass

## Resources

- **Main README**: Overview and philosophy
- **CODEBASE_ANALYSIS.md**: Detailed status and roadmap
- **docs/**: Component documentation
- **examples/**: Working code examples

## Getting Help

- Review examples in `examples/`
- Check documentation in `docs/`
- Read docstrings in source code
- Run validation scripts to see quality standards

---

**Remember**: Going slow. Documentation first. Harmony over hype. 🌱
