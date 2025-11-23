class SecureCalculator:
    """
    A calculator class composed from: secure_add, secure_subtract, secure_multiply, secure_divide
    """

    def secure_add(self, a, b):
        """
        Fractally composed addition with validation and logging.
        High Justice (validation), High Love (logging), Moderate Power.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a + b
        print(f"[LOG] secure_add({a}, {b}) = {result}")
        return result

    def secure_subtract(self, a, b):
        """
        Fractally composed subtraction with validation and logging.
        High Justice (validation), High Love (logging), Moderate Power.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a - b
        print(f"[LOG] secure_subtract({a}, {b}) = {result}")
        return result

    def secure_multiply(self, a, b):
        """
        Fractally composed multiplication with validation and logging.
        High Justice (validation), High Love (logging), Moderate Power.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        result = a * b
        print(f"[LOG] secure_multiply({a}, {b}) = {result}")
        return result

    def secure_divide(self, a, b):
        """
        Fractally composed division with validation, zero-check, and logging.
        High Justice (validation + zero-check), High Love (logging), Moderate Power.
        """
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Inputs must be numeric")
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        print(f"[LOG] secure_divide({a}, {b}) = {result}")
        return result

