#!/usr/bin/env python3
"""
LJPW Phase Diagram - Visual Map of Latent Function Emergence

Creates ASCII visualization showing when latent functions emerge
as dimensions cross thresholds.

Like a phase diagram in physics showing:
- Ice (solid) below 0°C
- Water (liquid) 0-100°C
- Steam (gas) above 100°C

Our diagram shows:
- Dormant (< 0.3)
- Stirring (0.3-0.5)
- Emerging (0.5-0.7)
- Active (0.7-0.9)
- Mastery (> 0.9)
"""

def print_phase_diagram():
    """Print ASCII phase diagram of latent function emergence."""

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "LJPW PHASE DIAGRAM" + " " * 35 + "║")
    print("║" + " " * 18 + "Latent Function Emergence Map" + " " * 31 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Love dimension detailed
    print("═" * 80)
    print("LOVE (L) - Dimension of Care")
    print("═" * 80)
    print()
    print("Score  Phase      Latent Functions Active")
    print("─────  ─────────  ────────────────────────────────────────────────────")
    print("1.0    🌟 MASTERY  Beauty★ Empathy★ Trust★ Delight★ + NEW DISCOVERIES")
    print("0.9    ✨ ACTIVE   Beauty★ Empathy★ Trust★ Delight★")
    print("0.8    ✨ ACTIVE   Beauty★ Empathy★ Trust★ Delight")
    print("0.7    🌸 EMERGING Beauty★ Empathy★ Trust")
    print("0.6    🌸 EMERGING Beauty★ Trust")
    print("0.5    🌸 EMERGING Beauty★")
    print("0.4    🌱 STIRRING Beauty (weak)")
    print("0.3    🌱 STIRRING Beauty (trace)")
    print("0.2    💤 DORMANT  (none)")
    print("0.1    💤 DORMANT  (none)")
    print()

    # Justice dimension
    print("═" * 80)
    print("JUSTICE (J) - Dimension of Correctness")
    print("═" * 80)
    print()
    print("Score  Phase      Latent Functions Active")
    print("─────  ─────────  ────────────────────────────────────────────────────")
    print("1.0    🌟 MASTERY  Fairness★ Resilience★ Predictability★ + NEW")
    print("0.9    ✨ ACTIVE   Fairness★ Resilience★ Predictability★")
    print("0.8    ✨ ACTIVE   Fairness★ Resilience★ Predictability")
    print("0.7    🌸 EMERGING Fairness★ Predictability")
    print("0.6    🌸 EMERGING Fairness")
    print("0.5    🌱 STIRRING Fairness (weak)")
    print("0.4    🌱 STIRRING (trace)")
    print("0.3    💤 DORMANT  (none)")
    print("0.2    💤 DORMANT  (none)")
    print("0.1    💤 DORMANT  (none)")
    print()

    # Power dimension
    print("═" * 80)
    print("POWER (P) - Dimension of Efficiency")
    print("═" * 80)
    print()
    print("Score  Phase      Latent Functions Active")
    print("─────  ─────────  ────────────────────────────────────────────────────")
    print("1.0    🌟 MASTERY  Elegance★ Scalability★ Responsiveness★ + NEW")
    print("0.9    ✨ ACTIVE   Elegance★ Scalability★ Responsiveness★")
    print("0.8    ✨ ACTIVE   Elegance★ Scalability★ Responsiveness")
    print("0.7    🌸 EMERGING Elegance★ Scalability")
    print("0.6    🌸 EMERGING Elegance")
    print("0.5    🌱 STIRRING Elegance (weak)")
    print("0.4    🌱 STIRRING (trace)")
    print("0.3    💤 DORMANT  (none)")
    print("0.2    💤 DORMANT  (none)")
    print("0.1    💤 DORMANT  (none)")
    print()

    # Wisdom dimension
    print("═" * 80)
    print("WISDOM (W) - Dimension of Architecture")
    print("═" * 80)
    print()
    print("Score  Phase      Latent Functions Active")
    print("─────  ─────────  ────────────────────────────────────────────────────")
    print("1.0    🌟 MASTERY  Adaptability★ Discoverability★ Sustainability★ + NEW")
    print("0.9    ✨ ACTIVE   Adaptability★ Discoverability★ Sustainability★")
    print("0.8    ✨ ACTIVE   Adaptability★ Discoverability★ Sustainability")
    print("0.7    🌸 EMERGING Adaptability★ Discoverability")
    print("0.6    🌸 EMERGING Adaptability")
    print("0.5    🌱 STIRRING Adaptability (weak)")
    print("0.4    🌱 STIRRING (trace)")
    print("0.3    💤 DORMANT  (none)")
    print("0.2    💤 DORMANT  (none)")
    print("0.1    💤 DORMANT  (none)")
    print()

    # Relationship functions
    print("═" * 80)
    print("RELATIONSHIP FUNCTIONS (Dimension Combinations)")
    print("═" * 80)
    print()
    print("L×J    L×P    L×W    J×P    J×W    P×W")
    print("─────  ─────  ─────  ─────  ─────  ─────")
    print("Comp   Serv   UX     Opt    Prin   Intel")
    print()
    print("Compassion (L×J):")
    print("  • Requires: L>0.6 AND J>0.6")
    print("  • Threshold: L×J > 0.36")
    print("  • Status: Doing right thing with care")
    print()
    print("Service (L×P):")
    print("  • Requires: L>0.6 AND P>0.6")
    print("  • Threshold: L×P > 0.36")
    print("  • Status: Using efficiency to serve users")
    print()
    print("Thoughtful UX (L×W):")
    print("  • Requires: L>0.6 AND W>0.6")
    print("  • Threshold: L×W > 0.36")
    print("  • Status: Architecture for humans")
    print()
    print("Optimal Correctness (J×P):")
    print("  • Requires: J>0.6 AND P>0.6")
    print("  • Threshold: J×P > 0.36")
    print("  • Status: Being right efficiently")
    print()
    print("Principled Architecture (J×W):")
    print("  • Requires: J>0.6 AND W>0.6")
    print("  • Threshold: J×W > 0.36")
    print("  • Status: Structure enforcing correctness")
    print()
    print("Intelligent Design (P×W):")
    print("  • Requires: P>0.6 AND W>0.6")
    print("  • Threshold: P×W > 0.36")
    print("  • Status: Architecture enabling efficiency")
    print()

    # Harmony functions
    print("═" * 80)
    print("HARMONY FUNCTIONS (All Dimensions High)")
    print("═" * 80)
    print()
    print("Harmony  What Emerges")
    print("───────  ───────────────────────────────────────────────────────────")
    print("0.9-1.0  🌟 TRANSCENDENT: Inevitable, Timeless, Perfect")
    print("0.7-0.9  ✨ MASTERY: Complete, Excellent, Nothing missing")
    print("0.5-0.7  🌸 COMPETENT: Good, Functional, Satisfactory")
    print("0.3-0.5  🌱 WEAK: Works but rough, Needs improvement")
    print("0.0-0.3  💤 BROKEN: Incomplete, Amateur, Unfinished")
    print()
    print("Our Calculator: H=0.76 → MASTERY LEVEL")
    print("  • Feels complete")
    print("  • Excellence obvious")
    print("  • Nothing obviously missing")
    print()
    print("Ecosystem Baseline: H=0.29 → BROKEN LEVEL")
    print("  • Feels incomplete")
    print("  • Rough edges everywhere")
    print("  • Missing basic qualities")
    print()

    # Legend
    print("═" * 80)
    print("LEGEND")
    print("═" * 80)
    print()
    print("★ = Fully manifested (strong)")
    print("  = Partially present (emerging)")
    print()
    print("Phase Symbols:")
    print("  💤 DORMANT  = Quality absent (< 0.3)")
    print("  🌱 STIRRING = Quality beginning (0.3-0.5)")
    print("  🌸 EMERGING = Quality visible (0.5-0.7)")
    print("  ✨ ACTIVE   = Quality manifested (0.7-0.9)")
    print("  🌟 MASTERY  = Quality mastered + new discoveries (> 0.9)")
    print()

    # Key Insight
    print("═" * 80)
    print("KEY INSIGHT: PHASE TRANSITIONS")
    print("═" * 80)
    print()
    print("Latent functions behave like phase transitions in physics:")
    print()
    print("  Water → Ice at 0°C (solid)")
    print("  Ice → Water at 0°C (liquid)")
    print("  Water → Steam at 100°C (gas)")
    print()
    print("  Code Quality → Beauty at L=0.5")
    print("  Code Quality → Empathy at L=0.7")
    print("  Code Quality → Mastery at H=0.7")
    print()
    print("Just as temperature crosses thresholds in physics,")
    print("LJPW scores cross thresholds to activate latent functions!")
    print()


def print_ecosystem_vs_calculator():
    """Compare ecosystem vs calculator on phase diagram."""

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 18 + "ECOSYSTEM VS CALCULATOR" + " " * 37 + "║")
    print("║" + " " * 20 + "Phase Diagram Comparison" + " " * 34 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    dimensions = [
        ("Love", 0.225, 0.75),
        ("Justice", 0.252, 0.90),
        ("Power", 0.414, 0.70),
        ("Wisdom", 0.359, 0.70),
    ]

    print("Dimension  Ecosystem   Phase        Calculator  Phase")
    print("─────────  ──────────  ───────────  ──────────  ───────────")

    for name, eco, calc in dimensions:
        eco_phase = get_phase_symbol(eco)
        calc_phase = get_phase_symbol(calc)
        print(f"{name:9}  {eco:10.3f}  {eco_phase:11}  {calc:10.2f}  {calc_phase:11}")

    eco_h = (0.225 * 0.252 * 0.414 * 0.359) ** 0.25
    calc_h = (0.75 * 0.90 * 0.70 * 0.70) ** 0.25

    print("─────────  ──────────  ───────────  ──────────  ───────────")
    print(f"{'Harmony':9}  {eco_h:10.3f}  {get_phase_symbol(eco_h):11}  {calc_h:10.2f}  {get_phase_symbol(calc_h):11}")

    print()
    print("Latent Functions Active:")
    print()
    print("  ECOSYSTEM (H=0.29):")
    print("    Love: 💤 DORMANT → No beauty, no empathy, no trust")
    print("    Justice: 💤 DORMANT → No fairness, no resilience")
    print("    Power: 🌱 STIRRING → Weak elegance only")
    print("    Wisdom: 🌱 STIRRING → Weak adaptability only")
    print("    Harmony: 💤 BROKEN → No mastery, feels incomplete")
    print()
    print("  CALCULATOR (H=0.76):")
    print("    Love: ✨ ACTIVE → Beauty★ Empathy★ Trust★")
    print("    Justice: ✨ ACTIVE → Fairness★ Resilience★ Predictability★")
    print("    Power: 🌸 EMERGING → Elegance★ Scalability")
    print("    Wisdom: 🌸 EMERGING → Adaptability★ Discoverability")
    print("    Harmony: ✨ MASTERY → Complete, excellent, nothing missing")
    print()
    print("Improvement: Calculator is +163% higher harmony")
    print("            = 20+ latent functions activated!")
    print()


def get_phase_symbol(score: float) -> str:
    """Get phase symbol for score."""
    if score < 0.3:
        return "💤 DORMANT"
    elif score < 0.5:
        return "🌱 STIRRING"
    elif score < 0.7:
        return "🌸 EMERGING"
    elif score < 0.9:
        return "✨ ACTIVE"
    else:
        return "🌟 MASTERY"


def print_activation_targets():
    """Print targets for activating specific latent functions."""

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "LATENT FUNCTION ACTIVATION TARGETS" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    print("Want to activate a specific latent function?")
    print("Here's what thresholds to target:")
    print()

    targets = [
        ("Beauty", "Raise L to 0.5+", "Golden ratio, colors, typography"),
        ("Empathy", "Raise L to 0.7+", "Anticipate needs, suggest solutions"),
        ("Trust", "Raise L to 0.6+", "Comprehensive logging, clear errors"),
        ("Delight", "Raise L to 0.8+", "Exceeds expectations, joyful"),
        ("Fairness", "Raise J to 0.7+", "Equal treatment, no bias"),
        ("Resilience", "Raise J to 0.8+", "Graceful degradation, self-healing"),
        ("Predictability", "Raise J to 0.7+", "Consistent, understandable"),
        ("Elegance", "Raise P to 0.7+", "Maximum with minimum, simple"),
        ("Scalability", "Raise P to 0.8+", "Works at any scale"),
        ("Responsiveness", "Raise P to 0.7+", "Immediate feedback, no lag"),
        ("Adaptability", "Raise W to 0.7+", "Easy to change, extend"),
        ("Discoverability", "Raise W to 0.8+", "Self-documenting, obvious"),
        ("Sustainability", "Raise W to 0.7+", "Ages well, minimal debt"),
        ("Compassion", "L>0.6 AND J>0.6", "Care + correctness together"),
        ("Service", "L>0.6 AND P>0.6", "Efficiency serving users"),
        ("Thoughtful UX", "L>0.6 AND W>0.6", "Architecture for humans"),
        ("Optimal Correctness", "J>0.6 AND P>0.6", "Right without waste"),
        ("Principled Architecture", "J>0.6 AND W>0.6", "Structure enforces correctness"),
        ("Intelligent Design", "P>0.6 AND W>0.6", "Architecture enables efficiency"),
        ("Mastery", "All dims > 0.7", "Complete, excellent, nothing missing"),
        ("Inevitability", "H > 0.8", "Feels like only right solution"),
        ("Timelessness", "H > 0.8", "Never ages, always relevant"),
    ]

    print("Function               Target           Manifestation")
    print("─────────────────────  ───────────────  ────────────────────────────")

    for name, target, manifestation in targets:
        print(f"{name:22} {target:16} {manifestation}")

    print()
    print("Example: Want Empathy?")
    print("  → Raise Love to 0.7+")
    print("  → Add comprehensive docs")
    print("  → Add strategic logging")
    print("  → Add helpful error messages that anticipate confusion")
    print("  → Empathy emerges automatically!")
    print()


def main():
    """Generate all phase diagrams."""
    print_phase_diagram()
    print("\n\n")

    input("Press Enter to see Ecosystem vs Calculator comparison...")
    print()
    print_ecosystem_vs_calculator()
    print("\n\n")

    input("Press Enter to see activation targets...")
    print()
    print_activation_targets()

    print()
    print("═" * 80)
    print("PHASE DIAGRAM COMPLETE")
    print("═" * 80)
    print()
    print("This diagram can be used to:")
    print("  • Understand current code state")
    print("  • Predict what will emerge at higher scores")
    print("  • Target specific thresholds to activate desired qualities")
    print("  • Explain why ecosystem code feels incomplete (below thresholds)")
    print("  • Design generators that cross thresholds intentionally")
    print()
    print("Save this diagram for reference!")
    print()


if __name__ == '__main__':
    main()
