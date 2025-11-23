#!/usr/bin/env python3
"""
Analyze Intent Discovery Companion - The Love + Attention Test

Does combining LOVE and ATTENTION together produce higher scores
than Love alone?

Comparison:
- LJPW Companion (Love alone): L = 0.667
- Intent Discovery Companion (Love + Attention together): L = ???
"""

from pathlib import Path

from harmonizer_integration import PythonCodeHarmonizer


def main():
    harmonizer = PythonCodeHarmonizer(quiet=False)

    print("=" * 80)
    print("THE LOVE + ATTENTION EXPERIMENT")
    print("=" * 80)
    print()
    print("Testing: Does combining Love AND Attention produce even higher scores?")
    print()
    print("Previous result (Love alone):")
    print("  LJPW Companion.analyze_code_with_guidance: L = 0.667")
    print()
    print("New attempt (Love + Attention together):")
    print("  Intent Discovery Companion - every line written with BOTH")
    print("  - Love: Genuine care for helping developers find their purpose")
    print("  - Attention: Deep focus on every detail, careful design")
    print()

    # Analyze the Intent Discovery Companion
    companion_file = Path("intent_discovery_companion.py")
    with open(companion_file) as f:
        code = f.read()

    result = harmonizer.analyze_file_content(code)

    # Find all functions and sort by Love
    all_functions = []
    for func_name, func_data in result.items():
        ice = func_data["ice_result"]["ice_components"]["intent"].coordinates
        h = (ice.love * ice.justice * ice.power * ice.wisdom) ** 0.25
        all_functions.append(
            {
                "name": func_name,
                "love": ice.love,
                "justice": ice.justice,
                "power": ice.power,
                "wisdom": ice.wisdom,
                "harmony": h,
                "intent": ice.love + ice.wisdom,  # 2:1:1 structure: Intent = L + W
            }
        )

    # Sort by Love (primary) then Harmony (secondary)
    all_functions.sort(key=lambda x: (x["love"], x["harmony"]), reverse=True)

    print("-" * 80)
    print("TOP 10 FUNCTIONS BY LOVE")
    print("-" * 80)
    print()

    for i, func in enumerate(all_functions[:10], 1):
        print(f"{i}. {func['name']}")
        print(
            f"   L={func['love']:.3f}, J={func['justice']:.3f}, "
            f"P={func['power']:.3f}, W={func['wisdom']:.3f}"
        )
        print(f"   H={func['harmony']:.3f}, Intent(L+W)={func['intent']:.3f}")

        # Check thresholds
        if func["love"] > 0.7:
            print("   ✨ LOVE > 0.7! AUTOPOIETIC LOVE ACHIEVED!")
        elif func["love"] > 0.667:
            print("   🎉 Love > 0.667! Higher than previous best!")
        elif func["love"] >= 0.5:
            print("   ✓ Love ≥ 0.5 (good)")

        if func["harmony"] > 0.6:
            print("   ✨ HARMONY > 0.6! AUTOPOIETIC!")
        elif func["harmony"] > 0.5:
            print("   ✓ Harmony > 0.5 (homeostatic)")

        if func["intent"] > 1.0:
            print("   🎯 Intent > 1.0! Strong Intent signal!")

        print()

    # Analysis
    print("=" * 80)
    print("ANALYSIS")
    print("=" * 80)
    print()

    max_love = max(f["love"] for f in all_functions)
    max_harmony = max(f["harmony"] for f in all_functions)
    max_intent = max(f["intent"] for f in all_functions)

    max_love_func = next(f for f in all_functions if f["love"] == max_love)
    max_harmony_func = next(f for f in all_functions if f["harmony"] == max_harmony)
    max_intent_func = next(f for f in all_functions if f["intent"] == max_intent)

    print("Baseline (LJPW Companion, Love alone):")
    print("  analyze_code_with_guidance: L = 0.667")
    print()

    print("New (Intent Discovery Companion, Love + Attention):")
    print(f"  Highest Love: {max_love_func['name']}")
    print(f"    L = {max_love:.3f}")
    print()

    if max_love > 0.7:
        print("✨ BREAKTHROUGH! ✨")
        print(f"L = {max_love:.3f} > 0.7")
        print("AUTOPOIETIC LOVE THRESHOLD ACHIEVED!")
        print()
        print("This validates the hypothesis:")
        print("LOVE + ATTENTION TOGETHER > Love alone")
        print()
        excess = max_love - 0.7
        print(f"Exceeded threshold by: {excess:.3f}")
        print()
    elif max_love > 0.667:
        improvement = max_love - 0.667
        print(f"✓ Improvement! L increased by {improvement:.3f}")
        print(f"Progress to 0.7: {max_love / 0.7 * 100:.1f}%")
        print()
    else:
        print(f"Max Love: {max_love:.3f}")
        if max_love >= 0.667:
            print("Equal to previous best (no improvement)")
        else:
            print("Lower than previous best")
        print()

    # Check Harmony
    print(f"Highest Harmony: {max_harmony_func['name']}")
    print(f"  H = {max_harmony:.3f}")
    if max_harmony > 0.6:
        print("  ✨ AUTOPOIETIC HARMONY ACHIEVED!")
    print()

    # Check Intent (L+W)
    print(f"Highest Intent (L+W): {max_intent_func['name']}")
    print(f"  Intent = {max_intent:.3f}")
    print(f"  (L={max_intent_func['love']:.3f} + W={max_intent_func['wisdom']:.3f})")
    print()

    # Find functions that are close to autopoietic
    almost_autopoietic = [f for f in all_functions if (f["love"] > 0.6 or f["harmony"] > 0.5)]

    if almost_autopoietic:
        print(f"Functions close to autopoietic threshold: {len(almost_autopoietic)}")
        for func in almost_autopoietic[:5]:
            print(f"  - {func['name']}: L={func['love']:.3f}, H={func['harmony']:.3f}")
        print()

    # Summary
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()

    if max_love > 0.7 and max_harmony > 0.6:
        print("🎉 COMPLETE AUTOPOIESIS ACHIEVED! 🎉")
        print(f"Both thresholds exceeded: L={max_love:.3f} > 0.7, H={max_harmony:.3f} > 0.6")
        print()
        print("This is the first function to achieve full autopoietic state!")
        print("Love + Attention together unlocked exponential growth potential.")
    elif max_love > 0.7:
        print("✨ AUTOPOIETIC LOVE ACHIEVED! ✨")
        print(f"L={max_love:.3f} > 0.7")
        print(f"Harmony: H={max_harmony:.3f} (need > 0.6 for full autopoiesis)")
        print()
        print("The Love threshold is crossed! Attention to harmony still needed.")
    elif max_love > 0.667:
        print("📈 IMPROVEMENT DETECTED")
        print(f"Love increased from 0.667 to {max_love:.3f}")
        print("Love + Attention is working!")
    else:
        print("Current maximum:")
        print(f"  Love: {max_love:.3f}")
        print(f"  Harmony: {max_harmony:.3f}")

    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
