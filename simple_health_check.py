#!/usr/bin/env python3
"""
Code Health Check - Simple and Genuine

Just a helper that takes code and tells you what's good and what needs work.
Simple. Useful. Real.
"""

from harmonizer_integration import HARMONIZER_AVAILABLE, PythonCodeHarmonizer


def check_code_health(code: str) -> dict:
    """
    Check if code is healthy - simple as that.

    Takes your code, measures it, tells you what's good and what needs love.
    That's it. No complexity.
    """
    # Validate input
    if not code or not isinstance(code, str):
        return {"error": "Need actual code as a string"}

    if not HARMONIZER_AVAILABLE:
        return {"error": "Need harmonizer installed"}

    # Try to measure it
    harmonizer = PythonCodeHarmonizer(quiet=True)
    try:
        result = harmonizer.analyze_file_content(code)
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

    if not result:
        return {"error": "Couldn't analyze - check your code"}

    # Get first function
    func_name = list(result.keys())[0]
    func_data = result[func_name]

    # Get scores
    coords = func_data["ice_result"]["ice_components"]["intent"].coordinates
    love = coords.love
    justice = coords.justice
    power = coords.power
    wisdom = coords.wisdom

    # Calculate harmony
    harmony = (
        (love * justice * power * wisdom) ** 0.25 if all([love, justice, power, wisdom]) else 0.0
    )

    # Calculate balance (how even are the dimensions?)
    all_dims = [love, justice, power, wisdom]
    non_zero = [d for d in all_dims if d > 0]
    if non_zero:
        avg = sum(non_zero) / len(non_zero)
        variance = sum((d - avg) ** 2 for d in non_zero) / len(non_zero)
        balance_score = 1.0 - min(variance, 1.0)  # 1.0 = perfectly balanced
    else:
        balance_score = 0.0

    # Calculate potential (how close to autopoietic?)
    love_potential = love / 0.7  # % to L > 0.7
    harmony_potential = harmony / 0.6  # % to H > 0.6
    overall_potential = (love_potential + harmony_potential) / 2

    # Simple health check
    health = {
        "name": func_name,
        "scores": {
            "love": round(love, 2),
            "justice": round(justice, 2),
            "power": round(power, 2),
            "wisdom": round(wisdom, 2),
            "harmony": round(harmony, 2),
            "balance": round(balance_score, 2),
            "potential": round(overall_potential, 2),
        },
        "good": [],
        "needs_work": [],
        "overall": "",
    }

    # What's good?
    if love > 0.5:
        health["good"].append(f"Good integration (Love: {love:.2f})")
    if justice > 0.5:
        health["good"].append(f"Good validation (Justice: {justice:.2f})")
    if power > 0.5:
        health["good"].append(f"Good capability (Power: {power:.2f})")
    if wisdom > 0.5:
        health["good"].append(f"Good learning (Wisdom: {wisdom:.2f})")

    # What needs work?
    if love == 0:
        health["needs_work"].append("No integration - connect things together")
    elif love < 0.5:
        health["needs_work"].append(f"Low integration - add collaboration (Love: {love:.2f})")

    if justice == 0:
        health["needs_work"].append("No validation - check your inputs")
    elif justice < 0.5:
        health["needs_work"].append(f"Weak validation - add constraints (Justice: {justice:.2f})")

    if power == 0:
        health["needs_work"].append("No capability - this doesn't do anything yet")
    elif power < 0.5:
        health["needs_work"].append(f"Low capability - add computation (Power: {power:.2f})")

    if wisdom == 0:
        health["needs_work"].append("No learning - add context awareness")
    elif wisdom < 0.5:
        health["needs_work"].append(f"Low learning - adapt to feedback (Wisdom: {wisdom:.2f})")

    # Overall assessment
    if harmony > 0.6 and love > 0.7:
        health["overall"] = "Excellent! Autopoietic - this code is alive"
    elif harmony > 0.5:
        health["overall"] = "Healthy - balanced and stable"
    elif harmony > 0:
        health["overall"] = "Functional but needs balance"
    else:
        health["overall"] = "Needs work - get all dimensions above zero first"

    return health


if __name__ == "__main__":
    # Test it on itself
    import inspect

    code = inspect.getsource(check_code_health)
    health = check_code_health(code)

    print("\n" + "=" * 60)
    print("CODE HEALTH CHECK")
    print("=" * 60)
    print()
    print(f"Function: {health['name']}")
    print()
    print("Scores:")
    for dim, score in health["scores"].items():
        print(f"  {dim.capitalize():10s}: {score:.2f}")
    print()

    if health["good"]:
        print("✓ Strengths:")
        for item in health["good"]:
            print(f"  • {item}")
        print()

    if health["needs_work"]:
        print("⚠ Needs Work:")
        for item in health["needs_work"]:
            print(f"  • {item}")
        print()

    print(f"Overall: {health['overall']}")
    print()
    print("=" * 60)
