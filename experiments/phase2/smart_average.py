#!/usr/bin/env python3
"""
Smart Average - Does what it says, simply.

Takes numbers, checks them, averages them, learns from history.
"""

def smart_average(numbers: list, history: list = None) -> dict:
    """
    Average numbers smartly - checks them, learns from past averages.

    Simple: Give it numbers, it gives you the average.
    Smart: It validates, handles errors, learns from history.
    """
    if history is None:
        history = []

    # Validate inputs
    if not numbers:
        return {"error": "Need some numbers to average"}

    if not isinstance(numbers, list):
        return {"error": "Numbers must be in a list"}

    # Clean the data - only keep valid numbers
    valid_numbers = []
    rejected = []

    for num in numbers:
        try:
            val = float(num)
            if val != val:  # NaN check
                rejected.append(f"{num} (not a number)")
            elif val > 1e10 or val < -1e10:  # Sanity check
                rejected.append(f"{num} (too extreme)")
            else:
                valid_numbers.append(val)
        except (ValueError, TypeError):
            rejected.append(f"{num} (can't convert)")

    if not valid_numbers:
        return {"error": "No valid numbers found", "rejected": rejected}

    # Calculate average
    total = sum(valid_numbers)
    count = len(valid_numbers)
    average = total / count

    # Learn from history
    all_averages = history + [average]
    trend = "stable"

    if len(all_averages) >= 2:
        recent_avg = sum(all_averages[-3:]) / min(3, len(all_averages))
        older_avg = sum(all_averages[:-1]) / len(all_averages[:-1])

        if recent_avg > older_avg * 1.1:
            trend = "increasing"
        elif recent_avg < older_avg * 0.9:
            trend = "decreasing"

    # Return results
    return {
        "average": round(average, 2),
        "count": count,
        "rejected": len(rejected),
        "trend": trend,
        "history_size": len(all_averages),
    }


if __name__ == "__main__":
    # Test it
    print("Smart Average - Testing\n")

    # Test 1: Simple average
    result = smart_average([1, 2, 3, 4, 5])
    print(f"Test 1: {result}")

    # Test 2: With bad data
    result = smart_average([1, 2, "bad", None, 5, 1e20])
    print(f"Test 2: {result}")

    # Test 3: With history (learning)
    history = [2.0, 2.1, 2.2]
    result = smart_average([5, 6, 7], history)
    print(f"Test 3: {result}")

    # Test 4: Empty
    result = smart_average([])
    print(f"Test 4: {result}")
