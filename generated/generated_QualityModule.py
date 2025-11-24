# Custom Exceptions
class CalculatorError(Exception):
    """Custom exception for QualityModule."""

    pass


class SecureCalculator:
    """Calculator with validated operations and logging."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        """Validated addition with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a, b):
        """Validated subtraction with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result


class SimpleCalculator:
    """Basic calculator with direct operations."""

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b


class CalculatorConfig:
    """Configuration management for calculator."""

    DEFAULT_PRECISION = 10
    DEFAULT_MODE = "strict"

    def __init__(self, precision=None, mode=None):
        self.precision = precision or self.DEFAULT_PRECISION
        self.mode = mode or self.DEFAULT_MODE
        self.settings = {}

    def get(self, key, default=None):
        """Get configuration value."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Set configuration value."""
        self.settings[key] = value
