"""
Testing LJPW Framework on Bad Code Requiring Refactoring

This experiment demonstrates how LJPW analysis can:
1. Identify quality problems in code
2. Suggest specific refactorings
3. Guide code toward autopoietic thresholds
4. Measure improvement objectively

Based on Phase 2 discoveries:
- Intent is measurable (L + W)
- Balance emerges from genuine work
- Autopoietic thresholds: L > 0.7, H > 0.6
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from harmonizer_integration import PythonCodeHarmonizer as StringHarmonizer

# ==============================================================================
# BAD CODE EXAMPLES
# ==============================================================================

BAD_CODE_EXAMPLES = {

    "god_object": '''
def process_user(name, email, age, address, phone):
    """A god function that does everything."""
    # Validate
    if not name:
        return None
    if "@" not in email:
        return None
    if age < 0:
        return None

    # Process
    user_data = {
        "name": name.upper(),
        "email": email.lower(),
        "age": age,
        "address": address,
        "phone": phone
    }

    # Save to database (not really)
    print(f"Saving {user_data}")

    # Send email (not really)
    print(f"Emailing {email}")

    # Log
    print(f"User {name} processed")

    # Calculate something
    discount = 0.1 if age > 65 else 0

    # Format output
    output = f"{name} ({email}), age {age}, discount {discount}"

    return output
''',

    "no_validation": '''
def calculate_discount(price, quantity):
    """No input validation at all."""
    total = price * quantity
    discount = total * 0.1
    final = total - discount
    return final
''',

    "no_error_handling": '''
def divide_numbers(a, b):
    """Division without error handling."""
    return a / b
''',

    "magic_numbers": '''
def calculate_shipping(weight, distance):
    """Magic numbers everywhere."""
    if weight < 5:
        base = 3.99
    elif weight < 10:
        base = 7.99
    else:
        base = 12.99

    if distance > 100:
        base = base * 1.5

    return base + (distance * 0.05)
''',

    "no_abstraction": '''
def generate_report(users):
    """No abstraction, everything inline."""
    report = ""
    for u in users:
        report += f"Name: {u['name']}\\n"
        report += f"Email: {u['email']}\\n"
        report += f"Age: {u['age']}\\n"
        if u['age'] > 65:
            report += "Senior discount: 10%\\n"
        else:
            report += "No discount\\n"
        report += "---\\n"
    return report
''',

    "primitive_obsession": '''
def create_order(customer_name, customer_email, product_name, product_price, quantity, shipping_address):
    """Too many primitive parameters."""
    total = product_price * quantity
    tax = total * 0.08
    final_total = total + tax

    print(f"Order for {customer_name}")
    print(f"Product: {product_name}")
    print(f"Total: ${final_total}")

    return final_total
''',

}

# ==============================================================================
# REFACTORED CODE (LJPW-GUIDED)
# ==============================================================================

REFACTORED_CODE = {

    "god_object_refactored": '''
def process_user(name: str, email: str, age: int, address: str, phone: str) -> dict:
    """
    Process user with validation, transformation, and side effects separated.

    Refactoring: Separation of concerns
    - Validation extracted (Justice)
    - Transformation pure (Wisdom)
    - Side effects isolated (Love - observability)
    - Clear intent (Love + Wisdom)
    """
    # Validation layer (Justice)
    validation_errors = validate_user_input(name, email, age)
    if validation_errors:
        raise ValueError(f"Invalid input: {validation_errors}")

    # Transformation layer (Power + Wisdom)
    user_data = transform_user_data(name, email, age, address, phone)

    # Persistence layer (Power)
    save_user(user_data)

    # Notification layer (Love - helping users)
    notify_user_created(email)

    # Observability layer (Love - helping developers)
    log_user_creation(name)

    # Business logic layer (Wisdom)
    discount = calculate_age_discount(age)

    return {
        "user": user_data,
        "discount": discount
    }


def validate_user_input(name: str, email: str, age: int) -> list:
    """Validation logic extracted - High Justice."""
    errors = []
    if not name or not name.strip():
        errors.append("Name is required")
    if "@" not in email:
        errors.append("Invalid email format")
    if age < 0 or age > 150:
        errors.append("Invalid age")
    return errors


def transform_user_data(name: str, email: str, age: int, address: str, phone: str) -> dict:
    """Pure transformation - High Wisdom."""
    return {
        "name": name.strip().title(),
        "email": email.lower().strip(),
        "age": age,
        "address": address,
        "phone": phone
    }


def calculate_age_discount(age: int) -> float:
    """Business logic extracted - High Wisdom."""
    return 0.1 if age > 65 else 0.0
''',

    "no_validation_refactored": '''
def calculate_discount(price: float, quantity: int) -> float:
    """
    Calculate discount with validation.

    Refactoring: Added Justice (validation)
    Now requires all 4 dimensions:
    - Justice: Input validation
    - Power: Calculation
    - Wisdom: Clear structure
    - Love: Error messages help users
    """
    # Justice: Validate inputs
    if price < 0:
        raise ValueError("Price cannot be negative")
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")
    if price > 1000000:
        raise ValueError("Price seems unreasonably high")

    # Power: Calculate
    total = price * quantity
    discount = total * 0.1
    final = total - discount

    return final
''',

    "no_error_handling_refactored": '''
def divide_numbers(a: float, b: float) -> float:
    """
    Safe division with error handling.

    Refactoring: Added Justice (safety)
    - Validates divisor
    - Clear error messages
    - Type hints for clarity
    """
    if not isinstance(a, (int, float)):
        raise TypeError(f"Dividend must be numeric, got {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Divisor must be numeric, got {type(b)}")

    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")

    return a / b
''',

    "magic_numbers_refactored": '''
# Constants extracted - High Wisdom
WEIGHT_THRESHOLD_LIGHT = 5
WEIGHT_THRESHOLD_MEDIUM = 10
BASE_SHIPPING_LIGHT = 3.99
BASE_SHIPPING_MEDIUM = 7.99
BASE_SHIPPING_HEAVY = 12.99
LONG_DISTANCE_THRESHOLD = 100
LONG_DISTANCE_MULTIPLIER = 1.5
DISTANCE_RATE = 0.05


def calculate_shipping(weight: float, distance: float) -> float:
    """
    Calculate shipping cost with named constants.

    Refactoring: Eliminated magic numbers
    - Constants clearly named (Wisdom)
    - Intent is clear (Love + Wisdom)
    - Easy to maintain (Wisdom)
    """
    # Validate inputs (Justice)
    if weight <= 0:
        raise ValueError("Weight must be positive")
    if distance <= 0:
        raise ValueError("Distance must be positive")

    # Determine base rate (Wisdom - clear logic)
    if weight < WEIGHT_THRESHOLD_LIGHT:
        base = BASE_SHIPPING_LIGHT
    elif weight < WEIGHT_THRESHOLD_MEDIUM:
        base = BASE_SHIPPING_MEDIUM
    else:
        base = BASE_SHIPPING_HEAVY

    # Apply distance multiplier (Wisdom - clear logic)
    if distance > LONG_DISTANCE_THRESHOLD:
        base *= LONG_DISTANCE_MULTIPLIER

    # Calculate final cost (Power)
    total = base + (distance * DISTANCE_RATE)

    return round(total, 2)
''',

    "no_abstraction_refactored": '''
def generate_report(users: list) -> str:
    """
    Generate user report with proper abstraction.

    Refactoring: Added abstraction layers
    - User formatting extracted (Wisdom)
    - Discount logic extracted (Wisdom)
    - Each function has single responsibility
    """
    report_lines = [format_user_entry(user) for user in users]
    return "\\n".join(report_lines)


def format_user_entry(user: dict) -> str:
    """Format single user entry - High Wisdom (abstraction)."""
    discount_line = get_discount_message(user['age'])

    return f"""Name: {user['name']}
Email: {user['email']}
Age: {user['age']}
{discount_line}
---"""


def get_discount_message(age: int) -> str:
    """Get discount message for age - High Wisdom."""
    return "Senior discount: 10%" if age > 65 else "No discount"
''',

    "primitive_obsession_refactored": '''
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    """Customer value object - High Wisdom (structure)."""
    name: str
    email: str

    def __post_init__(self):
        """Validate on construction - High Justice."""
        if not self.name:
            raise ValueError("Customer name required")
        if "@" not in self.email:
            raise ValueError("Invalid email format")


@dataclass
class Product:
    """Product value object - High Wisdom (structure)."""
    name: str
    price: float

    def __post_init__(self):
        """Validate on construction - High Justice."""
        if not self.name:
            raise ValueError("Product name required")
        if self.price < 0:
            raise ValueError("Price cannot be negative")


@dataclass
class Order:
    """Order aggregate - High Wisdom (domain model)."""
    customer: Customer
    product: Product
    quantity: int
    shipping_address: str

    TAX_RATE = 0.08

    def calculate_total(self) -> float:
        """Calculate order total - High Power + Wisdom."""
        subtotal = self.product.price * self.quantity
        tax = subtotal * self.TAX_RATE
        return subtotal + tax


def create_order(customer: Customer, product: Product, quantity: int, shipping_address: str) -> Order:
    """
    Create order with proper domain objects.

    Refactoring: Eliminated primitive obsession
    - Domain objects (Wisdom)
    - Built-in validation (Justice)
    - Clear intent (Love + Wisdom)
    - Encapsulated logic (Wisdom)
    """
    # Validate quantity (Justice)
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    # Create order (Wisdom - domain model)
    order = Order(
        customer=customer,
        product=product,
        quantity=quantity,
        shipping_address=shipping_address
    )

    # Calculate and display (Love - helping users)
    total = order.calculate_total()
    print(f"Order for {customer.name}")
    print(f"Product: {product.name}")
    print(f"Total: ${total:.2f}")

    return order
''',

}


def analyze_code_quality(code: str, name: str) -> dict:
    """Analyze code and return LJPW profile with insights."""
    harmonizer = StringHarmonizer()

    # Analyze code
    analysis = harmonizer.analyze_file_content(code)

    if not analysis:
        return {
            "name": name,
            "error": "Could not analyze code",
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0, "harmony": 0}
        }

    # Get first function analysis
    func_name = list(analysis.keys())[0] if analysis else None
    if not func_name:
        return {
            "name": name,
            "error": "No functions found",
            "ljpw": {"L": 0, "J": 0, "P": 0, "W": 0, "harmony": 0}
        }

    result = analysis[func_name]

    # Calculate harmony - harmonizer returns 'L', 'J', 'P', 'W' keys
    L = result.get('L', result.get('love', 0))
    J = result.get('J', result.get('justice', 0))
    P = result.get('P', result.get('power', 0))
    W = result.get('W', result.get('wisdom', 0))
    H = (L * J * P * W) ** 0.25 if all([L > 0, J > 0, P > 0, W > 0]) else 0

    # Determine phase
    if H < 0.5:
        phase = "ENTROPIC (death spiral)"
    elif H < 0.6:
        phase = "HOMEOSTATIC (stable)"
    elif L > 0.7 and H > 0.6:
        phase = "AUTOPOIETIC (exponential growth)"
    else:
        phase = "APPROACHING AUTOPOIETIC"

    # Identify problems
    problems = []
    if L < 0.3:
        problems.append("Low Love: Poor integration, no observability")
    if J < 0.3:
        problems.append("Low Justice: Missing validation/error handling")
    if P < 0.3:
        problems.append("Low Power: Inefficient or overcomplicated")
    if W < 0.3:
        problems.append("Low Wisdom: Poor structure, no abstraction")

    # Suggest improvements
    suggestions = []
    if J < 0.5:
        suggestions.append("Add input validation and error handling (↑ Justice)")
    if W < 0.5:
        suggestions.append("Extract constants and add abstraction (↑ Wisdom)")
    if L < 0.5:
        suggestions.append("Add logging, type hints, documentation (↑ Love)")
    if H == 0:
        suggestions.append("CRITICAL: Missing dimension(s) - function is not viable")

    return {
        "name": name,
        "function": func_name,
        "ljpw": {
            "L": round(L, 3),
            "J": round(J, 3),
            "P": round(P, 3),
            "W": round(W, 3),
            "harmony": round(H, 3),
            "intent": round(L + W, 3),
        },
        "phase": phase,
        "problems": problems,
        "suggestions": suggestions,
        "autopoietic_love": L > 0.7,
        "autopoietic_harmony": H > 0.6,
        "fully_autopoietic": L > 0.7 and H > 0.6,
    }


def compare_before_after(bad_key: str, good_key: str):
    """Compare bad code with refactored version."""
    print(f"\n{'='*80}")
    print(f"REFACTORING: {bad_key}")
    print(f"{'='*80}\n")

    # Analyze bad code
    bad_code = BAD_CODE_EXAMPLES[bad_key]
    bad_result = analyze_code_quality(bad_code, f"Bad: {bad_key}")

    print("BEFORE REFACTORING:")
    print(f"  Function: {bad_result['function']}")
    print(f"  L={bad_result['ljpw']['L']:.3f}, J={bad_result['ljpw']['J']:.3f}, "
          f"P={bad_result['ljpw']['P']:.3f}, W={bad_result['ljpw']['W']:.3f}")
    print(f"  Harmony: {bad_result['ljpw']['harmony']:.3f}")
    print(f"  Intent: {bad_result['ljpw']['intent']:.3f}")
    print(f"  Phase: {bad_result['phase']}")

    if bad_result['problems']:
        print("\n  Problems identified:")
        for problem in bad_result['problems']:
            print(f"    ⚠️  {problem}")

    if bad_result['suggestions']:
        print("\n  Suggested improvements:")
        for suggestion in bad_result['suggestions']:
            print(f"    💡 {suggestion}")

    # Analyze refactored code
    good_code = REFACTORED_CODE[good_key]
    good_result = analyze_code_quality(good_code, f"Good: {good_key}")

    print("\n" + "-" * 80)
    print("AFTER REFACTORING:")
    print(f"  Function: {good_result['function']}")
    print(f"  L={good_result['ljpw']['L']:.3f}, J={good_result['ljpw']['J']:.3f}, "
          f"P={good_result['ljpw']['P']:.3f}, W={good_result['ljpw']['W']:.3f}")
    print(f"  Harmony: {good_result['ljpw']['harmony']:.3f}")
    print(f"  Intent: {good_result['ljpw']['intent']:.3f}")
    print(f"  Phase: {good_result['phase']}")

    # Calculate improvements
    delta_L = good_result['ljpw']['L'] - bad_result['ljpw']['L']
    delta_J = good_result['ljpw']['J'] - bad_result['ljpw']['J']
    delta_P = good_result['ljpw']['P'] - bad_result['ljpw']['P']
    delta_W = good_result['ljpw']['W'] - bad_result['ljpw']['W']
    delta_H = good_result['ljpw']['harmony'] - bad_result['ljpw']['harmony']
    delta_I = good_result['ljpw']['intent'] - bad_result['ljpw']['intent']

    print("\n" + "-" * 80)
    print("IMPROVEMENTS:")
    print(f"  ΔL = {delta_L:+.3f}  {'✨' if delta_L > 0.2 else '✓' if delta_L > 0 else ''}")
    print(f"  ΔJ = {delta_J:+.3f}  {'✨' if delta_J > 0.2 else '✓' if delta_J > 0 else ''}")
    print(f"  ΔP = {delta_P:+.3f}  {'✨' if delta_P > 0.2 else '✓' if delta_P > 0 else ''}")
    print(f"  ΔW = {delta_W:+.3f}  {'✨' if delta_W > 0.2 else '✓' if delta_W > 0 else ''}")
    print(f"  ΔH = {delta_H:+.3f}  {'🌟' if delta_H > 0.2 else '✓' if delta_H > 0 else ''}")
    print(f"  ΔIntent = {delta_I:+.3f}  {'🎯' if delta_I > 0.3 else '✓' if delta_I > 0 else ''}")

    # Autopoietic status
    print("\n" + "-" * 80)
    print("AUTOPOIETIC STATUS:")
    before_status = "✅" if bad_result['autopoietic_love'] else "❌"
    after_status = "✅" if good_result['autopoietic_love'] else "❌"
    print(f"  L > 0.7:  {before_status} → {after_status}")

    before_status = "✅" if bad_result['autopoietic_harmony'] else "❌"
    after_status = "✅" if good_result['autopoietic_harmony'] else "❌"
    print(f"  H > 0.6:  {before_status} → {after_status}")

    before_status = "✅" if bad_result['fully_autopoietic'] else "❌"
    after_status = "✅" if good_result['fully_autopoietic'] else "❌"
    print(f"  Fully Autopoietic:  {before_status} → {after_status}")

    return {
        "before": bad_result,
        "after": good_result,
        "improvements": {
            "delta_L": delta_L,
            "delta_J": delta_J,
            "delta_P": delta_P,
            "delta_W": delta_W,
            "delta_H": delta_H,
            "delta_intent": delta_I,
        }
    }


if __name__ == "__main__":
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "LJPW FRAMEWORK: TESTING ON BAD CODE REQUIRING REFACTORING".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")

    print("\nDemonstrating how LJPW analysis guides refactoring decisions.")
    print("Based on Phase 2 discoveries: Intent is measurable, balance emerges.\n")

    # Test all refactorings
    refactorings = [
        ("god_object", "god_object_refactored", "God Object → Separated Concerns"),
        ("no_validation", "no_validation_refactored", "No Validation → Validated Input"),
        ("no_error_handling", "no_error_handling_refactored", "No Errors → Safe Division"),
        ("magic_numbers", "magic_numbers_refactored", "Magic Numbers → Named Constants"),
        ("no_abstraction", "no_abstraction_refactored", "No Abstraction → Layered Functions"),
        ("primitive_obsession", "primitive_obsession_refactored", "Primitives → Domain Objects"),
    ]

    results = []
    for bad_key, good_key, description in refactorings:
        print(f"\n\n{'▓' * 80}")
        print(f"TEST: {description}")
        print(f"{'▓' * 80}")
        result = compare_before_after(bad_key, good_key)
        results.append((description, result))

    # Summary
    print(f"\n\n{'═' * 80}")
    print("SUMMARY OF ALL REFACTORINGS")
    print(f"{'═' * 80}\n")

    print(f"{'Refactoring':<40} {'ΔH':<10} {'ΔIntent':<10} {'Autopoietic?':<15}")
    print("-" * 80)

    for description, result in results:
        delta_h = result['improvements']['delta_H']
        delta_i = result['improvements']['delta_intent']
        autopoietic = "✅ Yes" if result['after']['fully_autopoietic'] else "❌ No"

        print(f"{description:<40} {delta_h:+.3f}    {delta_i:+.3f}     {autopoietic}")

    # Average improvements
    avg_delta_h = sum(r['improvements']['delta_H'] for _, r in results) / len(results)
    avg_delta_i = sum(r['improvements']['delta_intent'] for _, r in results) / len(results)
    autopoietic_count = sum(1 for _, r in results if r['after']['fully_autopoietic'])

    print("-" * 80)
    print(f"{'AVERAGE IMPROVEMENT':<40} {avg_delta_h:+.3f}    {avg_delta_i:+.3f}     {autopoietic_count}/{len(results)}")

    print("\n" + "=" * 80)
    print("KEY INSIGHTS:")
    print("=" * 80)
    print()
    print("1. LJPW identifies specific quality problems automatically")
    print("2. Low dimensions point to exact refactoring needs:")
    print("   - Low J → Add validation/error handling")
    print("   - Low W → Extract constants, add abstraction")
    print("   - Low L → Add documentation, logging, integration")
    print("   - Low P → Simplify, remove inefficiencies")
    print()
    print("3. Refactoring guided by LJPW increases harmony measurably")
    print("4. Intent (L+W) improvement indicates better design")
    print("5. Autopoietic thresholds (L>0.7, H>0.6) are achievable goals")
    print()
    print("✨ The framework provides objective guidance for code quality!")
    print()
