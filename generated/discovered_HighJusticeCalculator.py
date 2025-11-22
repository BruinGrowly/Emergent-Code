class HighJusticeCalculator:
    """
    HighJusticeCalculator - Generated class
    Methods: secure_add, secure_subtract, secure_multiply, secure_divide
    """

    def __init__(self):
        self.precision = 10  # Calculation precision
        self.debug_mode = False  # Debug flag
        self.history = []  # Operation history

    @property
    def last_result(self):
        """Get the last operation result from history."""
        if hasattr(self, "history") and self.history:
            return self.history[-1].get("result")
        return None

    def secure_add(self, a, b):
        """Validated addition with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a + b
        print(f"[LOG] secure_add({a}, {b}) = {result}")
        return result

    def secure_subtract(self, a, b):
        """Validated subtraction with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a - b
        print(f"[LOG] secure_subtract({a}, {b}) = {result}")
        return result

    def secure_multiply(self, a, b):
        """Validated multiplication with logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a * b
        print(f"[LOG] secure_multiply({a}, {b}) = {result}")
        return result

    def secure_divide(self, a, b):
        """Validated division with zero-check and logging."""
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        print(f"[LOG] secure_divide({a}, {b}) = {result}")
        return result

    def _internal_validate(self, value):
        """Private validation helper."""
        return isinstance(value, (int, float))
