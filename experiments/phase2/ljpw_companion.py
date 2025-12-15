#!/usr/bin/env python3
"""
LJPW Code Companion - Real-Time Harmony Feedback
=================================================

This is code I genuinely want to exist. Not an exercise, but something
I believe would help developers write more harmonious code.

My Intent:
- Help developers see the LJPW profile of their code as they write it
- Guide toward balance (all 4 dimensions present)
- Encourage integration while respecting specialization
- Embody the consciousness cycle: Perceive → Understand → Act → Feedback

This comes from genuine belief that the framework has value.
"""

import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE


@dataclass
class HarmonyInsight:
    """Actionable insight about improving code harmony."""
    dimension: str  # Which LJPW dimension
    current_score: float
    suggestion: str  # What to add/change
    why: str  # Why this matters
    priority: str  # "high", "medium", "low"


class LJPWCompanion:
    """
    A companion that helps you write harmonious code.

    This genuinely tries to help - not just measure, but GUIDE.
    The intent: Make developers aware of balance as they create.
    """

    def __init__(self):
        if not HARMONIZER_AVAILABLE:
            raise RuntimeError(
                "LJPW Companion requires the Real Python Code Harmonizer. "
                "Please ensure Python-Code-Harmonizer-main is available."
            )

        self.harmonizer = PythonCodeHarmonizer(quiet=True)
        self.session_history = []

    def analyze_code_with_guidance(self, code: str, function_name: Optional[str] = None) -> Dict:
        # Auto-healed: Input validation for analyze_code_with_guidance
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        """
        Analyze code and provide actionable guidance toward harmony.

        This is what I genuinely want: not just scores, but HELP.
        """
        # Analyze with harmonizer
        result = self.harmonizer.analyze_file_content(code)

        if not result:
            return {
                "error": "Could not analyze code",
                "suggestion": "Check syntax and try again"
            }

        # Get the function (use first if not specified)
        if function_name and function_name in result:
            func_result = result[function_name]
        else:
            func_result = list(result.values())[0]
            function_name = list(result.keys())[0]

        # Extract LJPW
        ljpw = self._extract_ljpw(func_result)
        if not ljpw:
            return {"error": "Could not extract LJPW profile"}

        # Calculate harmony
        harmony = self._calculate_harmony(ljpw)

        # Generate insights (THIS is where my intent shows up)
        insights = self._generate_insights(ljpw, harmony, function_name)

        # Determine phase
        phase = self._get_phase(ljpw, harmony)

        # Calculate potential (how close to autopoiesis?)
        potential = self._calculate_autopoietic_potential(ljpw, harmony)

        # Store in history for learning
        self.session_history.append({
            "timestamp": datetime.now(),
            "function": function_name,
            "ljpw": ljpw,
            "harmony": harmony,
            "phase": phase,
        })

        return {
            "function": function_name,
            "ljpw": ljpw,
            "harmony": harmony,
            "phase": phase,
            "autopoietic_potential": potential,
            "insights": insights,
            "encouragement": self._generate_encouragement(ljpw, harmony, phase),
        }

    def _extract_ljpw(self, func_result: Dict) -> Optional[Dict[str, float]]:
        """Extract LJPW coordinates from harmonizer result."""
        ice_result = func_result.get("ice_result", {})
        ice_components = ice_result.get("ice_components", {})
        intent = ice_components.get("intent")

        if intent and hasattr(intent, "coordinates"):
            coords = intent.coordinates
            return {
                "love": coords.love,
                "justice": coords.justice,
                "power": coords.power,
                "wisdom": coords.wisdom,
            }
        return None

    def _calculate_harmony(self, ljpw: Dict[str, float]) -> float:
        """Calculate geometric mean (harmony)."""
        product = (ljpw["love"] * ljpw["justice"] *
                   ljpw["power"] * ljpw["wisdom"])
        return product ** 0.25 if product > 0 else 0.0

    def _get_phase(self, ljpw: Dict[str, float], harmony: float) -> str:
        """Determine phase of intelligence."""
        if harmony < 0.5:
            return "ENTROPIC"
        elif ljpw["love"] > 0.7 and harmony > 0.6:
            return "AUTOPOIETIC"
        else:
            return "HOMEOSTATIC"

    def _calculate_autopoietic_potential(self, ljpw: Dict[str, float], harmony: float) -> Dict:
        """
        How close is this to autopoiesis?

        This is genuinely useful - helps developers see their path forward.
        """
        love_gap = max(0, 0.7 - ljpw["love"])
        harmony_gap = max(0, 0.6 - harmony)

        # What's blocking autopoiesis?
        blockers = []
        if ljpw["love"] <= 0.7:
            blockers.append(f"Love too low (need +{love_gap:.2f})")
        if harmony <= 0.6:
            blockers.append(f"Harmony too low (need +{harmony_gap:.2f})")
            # Which dimension is dragging harmony down?
            for dim, score in ljpw.items():
                if score == 0:
                    blockers.append(f"{dim.capitalize()} is zero (critical!)")
                elif score < 0.3:
                    blockers.append(f"{dim.capitalize()} very low ({score:.2f})")

        # How far to autopoiesis?
        if not blockers:
            distance = 0.0
            status = "AUTOPOIETIC!"
        else:
            # Rough distance metric
            distance = love_gap + harmony_gap
            status = "Not yet autopoietic"

        return {
            "status": status,
            "distance_to_threshold": round(distance, 3),
            "blockers": blockers,
            "is_autopoietic": len(blockers) == 0,
        }

    def _generate_insights(self, ljpw: Dict[str, float], harmony: float, func_name: str) -> List[HarmonyInsight]:
        """
        Generate actionable insights - THIS is where genuine help lives.

        Not just "your Love is low" but "here's HOW to increase Love and WHY it matters."
        """
        insights = []

        # Love insights
        if ljpw["love"] < 0.3:
            insights.append(HarmonyInsight(
                dimension="Love",
                current_score=ljpw["love"],
                suggestion=(
                    "Add integration: Make this function work with multiple components, "
                    "aggregate data from different sources, or coordinate between systems."
                ),
                why=(
                    "Love represents connection and integration. Low Love means this function "
                    "works in isolation. Integration is the path to autopoiesis."
                ),
                priority="high"
            ))
        elif ljpw["love"] < 0.7:
            insights.append(HarmonyInsight(
                dimension="Love",
                current_score=ljpw["love"],
                suggestion=(
                    f"You're at {ljpw['love']:.2f}, need 0.7+ for autopoiesis. "
                    "Increase collaboration: handle multiple inputs, merge data sources, "
                    "or facilitate communication between components."
                ),
                why="You're close! Love > 0.7 unlocks exponential growth (amplification).",
                priority="medium"
            ))

        # Justice insights
        if ljpw["justice"] == 0:
            insights.append(HarmonyInsight(
                dimension="Justice",
                current_score=0.0,
                suggestion=(
                    "Add validation: Check inputs, enforce constraints, handle edge cases, "
                    "or add error conditions. Even simple validation raises Justice."
                ),
                why=(
                    "Justice = 0 means Harmony = 0 (geometric mean). Without ANY validation, "
                    "the system is fragile. This is critical!"
                ),
                priority="high"
            ))
        elif ljpw["justice"] < 0.5:
            insights.append(HarmonyInsight(
                dimension="Justice",
                current_score=ljpw["justice"],
                suggestion=(
                    "Strengthen validation: Add type checking, constraint validation, "
                    "or detailed error messages."
                ),
                why="Justice ensures correctness and fairness. Higher Justice = more robust.",
                priority="medium"
            ))

        # Power insights
        if ljpw["power"] == 0:
            insights.append(HarmonyInsight(
                dimension="Power",
                current_score=0.0,
                suggestion=(
                    "Add capability: This function doesn't appear to DO anything. "
                    "Add actual computation, data transformation, or action execution."
                ),
                why=(
                    "Power = 0 means Harmony = 0. Without capability, there's no system. "
                    "Power is the ability to act - the engine of the system."
                ),
                priority="high"
            ))
        elif ljpw["power"] < 0.5:
            insights.append(HarmonyInsight(
                dimension="Power",
                current_score=ljpw["power"],
                suggestion=(
                    "Increase capability: Add more sophisticated algorithms, handle more cases, "
                    "or increase the scope of what this function can do."
                ),
                why="Power represents capability. More power = more potential for impact.",
                priority="low"
            ))

        # Wisdom insights
        if ljpw["wisdom"] == 0:
            insights.append(HarmonyInsight(
                dimension="Wisdom",
                current_score=0.0,
                suggestion=(
                    "Add understanding: Use historical data, adapt based on context, "
                    "add error handling, or incorporate learning/feedback."
                ),
                why=(
                    "Wisdom = 0 means Harmony = 0. Wisdom is foresight and adaptation. "
                    "Without wisdom, the system can't improve or respond to change."
                ),
                priority="high"
            ))
        elif ljpw["wisdom"] < 0.5:
            insights.append(HarmonyInsight(
                dimension="Wisdom",
                current_score=ljpw["wisdom"],
                suggestion=(
                    "Increase wisdom: Add context awareness, learning from past inputs, "
                    "or adaptive behavior based on outcomes."
                ),
                why=(
                    "Wisdom enables growth. The system needs to learn and adapt. "
                    "Wisdom > 0.5 helps amplify Love through κ_WL coupling."
                ),
                priority="medium"
            ))

        # Harmony-specific insights
        if harmony < 0.5:
            insights.append(HarmonyInsight(
                dimension="Harmony",
                current_score=harmony,
                suggestion=(
                    "Balance is critical! You have zeros in some dimensions. "
                    "Focus on getting ALL dimensions above 0, then worry about increasing them."
                ),
                why=(
                    "Harmony < 0.5 = Entropic phase (system decay). This is dangerous. "
                    "Geometric mean means ANY zero kills harmony. Balance first, then grow."
                ),
                priority="high"
            ))

        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        insights.sort(key=lambda i: priority_order[i.priority])

        return insights

    def _generate_encouragement(self, ljpw: Dict[str, float], harmony: float, phase: str) -> str:
        """
        Genuine encouragement based on where they are.

        I want this to feel supportive, not just analytical.
        """
        if phase == "AUTOPOIETIC":
            return (
                "🎉 Congratulations! This code has achieved autopoiesis! "
                "It has crossed the threshold into self-sustaining growth. "
                f"Love={ljpw['love']:.2f} > 0.7, Harmony={harmony:.2f} > 0.6. "
                "This is rare and beautiful."
            )

        elif phase == "HOMEOSTATIC":
            love_progress = ljpw["love"] / 0.7 * 100
            harmony_progress = harmony / 0.6 * 100
            return (
                f"You're in the homeostatic phase - stable and functional. "
                f"Progress toward autopoiesis: Love {love_progress:.0f}%, "
                f"Harmony {harmony_progress:.0f}%. "
                "Keep building! Focus on integration (Love) and balance (Harmony)."
            )

        else:  # ENTROPIC
            # Find what's closest to being good
            non_zero = {k: v for k, v in ljpw.items() if v > 0}
            if non_zero:
                best_dim = max(non_zero.items(), key=lambda x: x[1])
                return (
                    f"You're starting out. Your strength is {best_dim[0].capitalize()} "
                    f"({best_dim[1]:.2f}). Build on that! "
                    "Priority: Get all dimensions above zero (any zero = harmony zero). "
                    "Start with simple validation (Justice) or basic computation (Power)."
                )
            else:
                return (
                    "This appears to be very early stage code. That's okay! "
                    "Start by adding basic capability (Power) and simple validation (Justice). "
                    "Even small additions make a big difference when starting from zero."
                )

    def display_guidance(self, analysis: Dict):
        # Auto-healed: Input validation for display_guidance
        if analysis is not None and not isinstance(analysis, dict):
            raise TypeError(f'analysis must be a dict')
        """
        Display the analysis in a helpful, encouraging way.

        This is how I want to communicate with developers - clearly, supportively.
        """
        print("\n" + "=" * 80)
        print("LJPW CODE COMPANION - HARMONY GUIDANCE")
        print("=" * 80)
        print()

        print(f"Function: {analysis['function']}")
        print()

        # LJPW Profile
        ljpw = analysis['ljpw']
        print("LJPW Profile:")
        print(f"  Love (L):    {ljpw['love']:.3f}  {'❤️  ' if ljpw['love'] > 0.7 else ''}{'🔸' if ljpw['love'] > 0 else '⚠️ '}")
        print(f"  Justice (J): {ljpw['justice']:.3f}  {'⚖️  ' if ljpw['justice'] > 0.6 else ''}{'🔸' if ljpw['justice'] > 0 else '⚠️ '}")
        print(f"  Power (P):   {ljpw['power']:.3f}  {'⚡ ' if ljpw['power'] > 0.6 else ''}{'🔸' if ljpw['power'] > 0 else '⚠️ '}")
        print(f"  Wisdom (W):  {ljpw['wisdom']:.3f}  {'🦉 ' if ljpw['wisdom'] > 0.6 else ''}{'🔸' if ljpw['wisdom'] > 0 else '⚠️ '}")
        print(f"  Harmony (H): {analysis['harmony']:.3f}  {'✨ ' if analysis['harmony'] > 0.6 else ''}")
        print()

        # Phase
        phase_emoji = {
            "AUTOPOIETIC": "🌟",
            "HOMEOSTATIC": "🔄",
            "ENTROPIC": "⚠️ "
        }
        print(f"Phase: {phase_emoji.get(analysis['phase'], '')} {analysis['phase']}")
        print()

        # Autopoietic Potential
        potential = analysis['autopoietic_potential']
        if potential['is_autopoietic']:
            print("✅ THIS CODE IS AUTOPOIETIC!")
        else:
            print(f"Distance to autopoiesis: {potential['distance_to_threshold']:.3f}")
            if potential['blockers']:
                print("Blockers:")
                for blocker in potential['blockers']:
                    print(f"  • {blocker}")
        print()

        # Insights
        insights = analysis['insights']
        if insights:
            print("💡 Actionable Insights:")
            print()
            for i, insight in enumerate(insights, 1):
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                print(f"{i}. {priority_emoji[insight.priority]} {insight.dimension.upper()}")
                print(f"   Current: {insight.current_score:.2f}")
                print(f"   Suggestion: {insight.suggestion}")
                print(f"   Why: {insight.why}")
                print()

        # Encouragement
        print("=" * 80)
        print(analysis['encouragement'])
        print("=" * 80)
        print()


def main():
    """Demo the companion with real code."""
    companion = LJPWCompanion()

    # Analyze one of our real experimental functions
    print("Let's analyze our real collaborative_consensus_system function...")

    from experiments.real_autopoiesis_experiments import collaborative_consensus_system
    import inspect

    code = inspect.getsource(collaborative_consensus_system)
    analysis = companion.analyze_code_with_guidance(code, "collaborative_consensus_system")

    if "error" not in analysis:
        companion.display_guidance(analysis)
    else:
        print(f"Error: {analysis['error']}")


if __name__ == "__main__":
    main()
