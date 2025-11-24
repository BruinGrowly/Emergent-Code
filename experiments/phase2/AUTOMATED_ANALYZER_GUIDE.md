# Automated LJPW Analyzer - Usage Guide

## Overview

The Automated LJPW Analyzer provides **fully automated code quality assessment** without any manual intervention. It combines:

1. **Semantic Analysis** (Python Code Harmonizer) - Analyzes function names for intent
2. **Pattern Recognition** (AST + Regex) - Detects implementation patterns
3. **Combined Scoring** - Merges both approaches for complete LJPW profiles

## Quick Start

### Basic Usage

```python
from automated_ljpw_analyzer import AutomatedLJPWAnalyzer

# Initialize analyzer
analyzer = AutomatedLJPWAnalyzer(quiet=True)

# Analyze code
code = """
def calculate_total(items):
    return sum(item.price for item in items)
"""

result = analyzer.analyze_code(code)

# Access scores
print(f"Harmony: {result.harmony:.2f}")
print(f"Love: {result.love:.2f}")
print(f"Justice: {result.justice:.2f}")
print(f"Power: {result.power:.2f}")
print(f"Wisdom: {result.wisdom:.2f}")
```

### Detailed Report

```python
# Get detailed breakdown
analyzer.print_detailed_report(result, code)
```

Output:
```
================================================================================
AUTOMATED LJPW ANALYSIS REPORT
================================================================================

📊 CODE METRICS:
  Lines of code: 3
  Functions: 1
  Classes: 0

🎯 LJPW SCORES:
--------------------------------------------------------------------------------

  LOVE: 0.15 ❌
    - Semantic (names): 0.00
    - Implementation (patterns): 0.30
    💡 Observability, clarity, developer experience
    • Docstrings: 0
    • Type hints: 0
    • Logging calls: 0
    • Comments: 0

  JUSTICE: 0.00 ❌
    - Semantic (names): 0.00
    - Implementation (patterns): 0.00
    ⚖️  Correctness, validation, error handling
    • Try/except blocks: 0
    • Validations: 0
    • Assertions: 0
    • Raises: 0

🌟 HARMONY: 0.00  ❌ ENTROPIC (needs improvement)
```

## Pattern Detection Details

### Love (Observability & Developer Experience)

**Patterns Detected:**
- ✅ **Docstrings** - Functions/classes with documentation
- ✅ **Type hints** - Function parameters and return types
- ✅ **Logging calls** - logger.*, logging.*, print() calls
- ✅ **Comments** - Inline # comments
- ✅ **Descriptive names** - Variables > 2 characters

**Scoring:**
```
Love = Weighted sum of:
  • Docstrings:       0.30 (30%)
  • Type hints:       0.20 (20%)
  • Logging:          0.20 (20%)
  • Comments:         0.15 (15%)
  • Descriptive names: 0.15 (15%)
```

**Example:**
```python
# Love = 0.9 (excellent)
def validate_user_email(email: str) -> bool:
    """
    Validate email address format.

    Args:
        email: Email address to validate

    Returns:
        True if valid, False otherwise
    """
    logger.info(f"Validating email: {email}")  # Logging
    # Check for @ symbol  # Comment
    return '@' in email and '.' in email.split('@')[1]
```

### Justice (Correctness & Validation)

**Patterns Detected:**
- ✅ **Try/except blocks** - Error handling
- ✅ **Validation patterns** - if not, if None, len() checks
- ✅ **Assertions** - assert statements
- ✅ **Raises** - Explicit exceptions

**Scoring:**
```
Justice = Weighted sum of:
  • Error handling:   0.40 (40%)
  • Validations:      0.30 (30%)
  • Assertions/raises: 0.20 (20%)
  • Conditional checks: 0.10 (10%)
```

**Example:**
```python
# Justice = 0.8 (strong)
def process_order(order_id: str, items: List[Item]) -> Order:
    """Process order with validation."""
    # Validation
    if not order_id:
        raise ValueError("Order ID is required")

    if not items:
        raise ValueError("Order must have items")

    # Error handling
    try:
        total = sum(item.price * item.quantity for item in items)
    except (AttributeError, TypeError) as e:
        raise ValueError(f"Invalid item data: {e}")

    # Business validation
    if total < 0:
        raise ValueError("Total cannot be negative")

    return Order(order_id=order_id, total=total)
```

### Power (Efficiency & Performance)

**Patterns Detected:**
- ✅ **Dictionary usage** - O(1) lookups
- ✅ **Comprehensions** - Efficient iteration
- ✅ **Generators** - Memory-efficient iteration
- ❌ **Nested loops** - Anti-pattern (reduces score)
- ❌ **Linear searches** - Anti-pattern (reduces score)

**Scoring:**
```
Power = Base 0.5 + Good patterns - Bad patterns
  Good:
    • Dict usage:      +0.15
    • Comprehensions:  +0.10
    • Generators:      +0.05
  Bad:
    • Nested loops:    -0.20
    • Linear searches: -0.10
```

**Good Example (Power = 0.7):**
```python
# Efficient: O(1) lookup with dict
user_index = {user.id: user for user in users}

def find_user(user_id):
    return user_index.get(user_id)  # O(1)
```

**Bad Example (Power = 0.3):**
```python
# Inefficient: O(n) linear search
def find_user(user_id):
    for user in users:  # Linear search
        if user.id == user_id:
            return user
```

### Wisdom (Architecture & Design)

**Patterns Detected:**
- ✅ **Classes** - Object-oriented structure
- ✅ **Constants** - UPPER_CASE values
- ✅ **Decorators** - Design patterns
- ❌ **Global variables** - Anti-pattern (reduces score)
- ❌ **Magic numbers** - Anti-pattern (reduces score)

**Scoring:**
```
Wisdom = Base 0.5 + Good patterns - Bad patterns
  Good:
    • Classes:     +0.20
    • Constants:   +0.15
    • Decorators:  +0.10
    • Modularity:  +0.05
  Bad:
    • Global vars: -0.30
    • Magic numbers: -0.20
```

**Good Example (Wisdom = 0.85):**
```python
# Constants (no magic numbers)
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Class structure
class APIClient:
    """API client with retry logic."""

    @retry(max_retries=MAX_RETRIES)  # Decorator
    def fetch_data(self, url: str) -> dict:
        """Fetch data from API."""
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        return response.json()
```

**Bad Example (Wisdom = 0.2):**
```python
# Global variable
api_cache = {}  # Global!

# Magic numbers
def fetch_with_retry(url):
    for i in range(3):  # Magic number!
        try:
            return requests.get(url, timeout=30)  # Magic number!
        except:
            time.sleep(2 ** i)  # Magic number!
```

## Real-World Examples

### Example 1: Analyzing a File

```python
from automated_ljpw_analyzer import AutomatedLJPWAnalyzer

# Read code from file
with open('mymodule.py', 'r') as f:
    code = f.read()

# Analyze
analyzer = AutomatedLJPWAnalyzer(quiet=False)
result = analyzer.analyze_code(code)

# Check harmony threshold
if result.harmony < 0.5:
    print("⚠️  Code needs improvement!")
    print(f"   Focus on: ", end="")

    # Identify weakest dimension
    dimensions = [
        ("Love", result.love),
        ("Justice", result.justice),
        ("Power", result.power),
        ("Wisdom", result.wisdom)
    ]
    weakest = min(dimensions, key=lambda x: x[1])
    print(f"{weakest[0]} (score: {weakest[1]:.2f})")
else:
    print("✅ Code quality is good!")
```

### Example 2: CI/CD Integration

```python
#!/usr/bin/env python3
"""
LJPW quality gate for CI/CD pipeline.

Usage:
    python ljpw_gate.py src/ --threshold 0.5
"""

import sys
import os
import argparse
from pathlib import Path
from automated_ljpw_analyzer import AutomatedLJPWAnalyzer

def analyze_directory(directory: Path, analyzer: AutomatedLJPWAnalyzer):
    """Analyze all Python files in directory."""
    results = []

    for filepath in directory.rglob('*.py'):
        with open(filepath, 'r') as f:
            code = f.read()

        result = analyzer.analyze_code(code)
        results.append((filepath, result))

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    parser.add_argument('--threshold', type=float, default=0.5)
    args = parser.parse_args()

    analyzer = AutomatedLJPWAnalyzer(quiet=True)
    results = analyze_directory(args.directory, analyzer)

    # Calculate average
    avg_harmony = sum(r[1].harmony for r in results) / len(results)

    print(f"Analyzed {len(results)} files")
    print(f"Average Harmony: {avg_harmony:.2f}")
    print(f"Threshold: {args.threshold:.2f}")

    # Find files below threshold
    failing = [(f, r) for f, r in results if r.harmony < args.threshold]

    if failing:
        print(f"\n❌ {len(failing)} files below threshold:")
        for filepath, result in failing:
            print(f"  {filepath}: H={result.harmony:.2f}")
        sys.exit(1)
    else:
        print("\n✅ All files pass quality gate!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Example 3: Before/After Refactoring

```python
from automated_ljpw_analyzer import AutomatedLJPWAnalyzer

before_code = """
def process(data):
    result = []
    for item in data:
        if item > 10:
            result.append(item * 2)
    return result
"""

after_code = """
from typing import List

def process_items(data: List[int]) -> List[int]:
    '''
    Process items: double values > threshold.

    Args:
        data: List of integers to process

    Returns:
        Processed list with values doubled
    '''
    THRESHOLD = 10
    MULTIPLIER = 2

    return [
        item * MULTIPLIER
        for item in data
        if item > THRESHOLD
    ]
"""

analyzer = AutomatedLJPWAnalyzer(quiet=True)

before = analyzer.analyze_code(before_code)
after = analyzer.analyze_code(after_code)

print("REFACTORING IMPROVEMENT:")
print(f"  Love:    {before.love:.2f} → {after.love:.2f}")
print(f"  Justice: {before.justice:.2f} → {after.justice:.2f}")
print(f"  Power:   {before.power:.2f} → {after.power:.2f}")
print(f"  Wisdom:  {before.wisdom:.2f} → {after.wisdom:.2f}")
print(f"  Harmony: {before.harmony:.2f} → {after.harmony:.2f}")

if after.harmony > before.harmony:
    improvement = ((after.harmony - before.harmony) / before.harmony) * 100
    print(f"\n✅ {improvement:.0f}% improvement!")
```

## Interpretation Guide

### Harmony Levels

| Harmony | Level | Meaning | Action |
|---------|-------|---------|--------|
| **H > 0.6** | 🟢 **Autopoietic** | Self-sustaining, production-ready | Maintain quality |
| **0.5 < H ≤ 0.6** | 🟡 **Homeostatic** | Stable but needs attention | Focus on lowest dimension |
| **0.3 < H ≤ 0.5** | 🟠 **Degrading** | Needs improvement soon | Refactor before adding features |
| **H ≤ 0.3** | 🔴 **Entropic** | Critical issues | Stop and refactor immediately |

### Dimension Priority

When harmony is low, focus on dimensions in this order:

1. **Justice first** - Correctness is critical
   - Add validation
   - Add error handling
   - Add tests

2. **Love second** - Makes code maintainable
   - Add docstrings
   - Add logging
   - Add type hints

3. **Wisdom third** - Prevents future issues
   - Extract constants
   - Create classes
   - Remove globals

4. **Power last** - Optimize only after correctness
   - Use efficient data structures
   - Remove nested loops
   - Add comprehensions

### Common Patterns

**Low Love (< 0.4):**
```python
# Add: docstrings, type hints, logging
def process_data(data: List[dict]) -> List[dict]:
    """Process user data with validation."""
    logger.info(f"Processing {len(data)} items")
    # ... implementation ...
```

**Low Justice (< 0.4):**
```python
# Add: validation, error handling
if not data:
    raise ValueError("Data cannot be empty")

try:
    result = dangerous_operation(data)
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise
```

**Low Power (< 0.4):**
```python
# Replace linear search with dict
items_by_id = {item.id: item for item in items}
return items_by_id.get(target_id)  # O(1) not O(n)
```

**Low Wisdom (< 0.4):**
```python
# Extract constants, create classes
class Config:
    MAX_RETRIES = 3
    TIMEOUT = 30

class DataProcessor:
    def process(self, data):
        # ...
```

## Limitations

### What the Analyzer CAN detect:
✅ Function/class structure (AST)
✅ Naming patterns (semantic + pattern)
✅ Documentation presence
✅ Error handling structure
✅ Data structure usage
✅ Basic architectural patterns

### What the Analyzer CANNOT detect:
❌ Logical correctness (semantic bugs)
❌ Test coverage
❌ Security vulnerabilities
❌ Performance bottlenecks (runtime)
❌ Business logic quality
❌ API design quality

### Best Combined With:
- **Unit tests** (correctness)
- **Linters** (style, bugs)
- **Type checkers** (mypy, pyright)
- **Security scanners** (bandit)
- **Code review** (business logic)

## Calibration Notes

The automated analyzer is **more conservative** than manual expert assessment:

| Assessment Type | E-Commerce Messy | E-Commerce Clean | Difference |
|----------------|------------------|------------------|------------|
| Manual Expert | H=0.06 | H=0.55 | 830% improvement |
| Automated | H=0.10 | H=0.44 | 364% improvement |

**Why the difference?**
- **Pattern recognition** can't assess qualitative factors
- **Semantic analysis** only sees function names, not implementation quality
- **Conservative scoring** prevents false positives

**When to use each:**
- **Automated**: Real-time feedback, CI/CD gates, quick assessment
- **Manual**: Final validation, architecture review, critical systems

## Future Enhancements

Planned improvements:

1. **More sophisticated patterns:**
   - Cyclomatic complexity
   - Coupling/cohesion metrics
   - Dependency analysis

2. **Context-aware scoring:**
   - Different thresholds by code type (test vs prod)
   - Domain-specific patterns (web, ML, data)

3. **IDE integration:**
   - Real-time analysis as you type
   - Inline suggestions
   - Refactoring hints

4. **Machine learning:**
   - Learn from human assessments
   - Calibrate scoring weights
   - Detect project-specific patterns

## Contributing

To improve the automated analyzer:

1. **Report false positives/negatives**
2. **Suggest new patterns to detect**
3. **Provide calibration data** (manual vs automated scores)
4. **Submit pattern detection improvements**

---

## Summary

The Automated LJPW Analyzer provides:
- ✅ **Zero manual assessment** - Fully automated
- ✅ **Consistent scoring** - Objective patterns
- ✅ **Real-time feedback** - Fast analysis
- ✅ **Actionable insights** - Specific pattern counts
- ✅ **Production-ready** - Validated on real codebases

Use it for continuous quality monitoring without human intervention!
