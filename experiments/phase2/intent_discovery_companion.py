#!/usr/bin/env python3
"""
Intent Discovery Companion
===========================

Created with LOVE and ATTENTION together.

Love: I genuinely want to help developers discover what they truly intend.
      To bridge the gap between stated purpose and actual implementation.
      To help people write code that aligns with their deepest purpose.

Attention: Every line written with care. Every function thoughtfully designed.
           Deep focus on making this actually work, actually help.
           Precision in implementation, clarity in communication.

Intent = Love + Wisdom. This embodies both.
"""

import ast
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import re

from harmonizer_integration import PythonCodeHarmonizer, HARMONIZER_AVAILABLE


@dataclass
class IntentSignal:
    """
    Signals of intent found in code.

    Written with attention: Each field carefully chosen to capture
    the different ways intent manifests in code.
    """
    # From function name
    name_claims: List[str] = field(default_factory=list)

    # From docstring
    documented_purpose: Optional[str] = None
    documented_behavior: List[str] = field(default_factory=list)

    # From type hints
    expected_inputs: List[str] = field(default_factory=list)
    expected_output: Optional[str] = None

    # From code structure
    actual_operations: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)

    # Integration signals
    integrates_with: List[str] = field(default_factory=list)

    def __repr__(self):
        return (
            f"IntentSignal(\n"
            f"  Claims: {self.name_claims}\n"
            f"  Purpose: {self.documented_purpose}\n"
            f"  Operations: {len(self.actual_operations)}\n"
            f"  Integration: {len(self.integrates_with)}\n"
            f")"
        )


@dataclass
class IntentAlignment:
    """
    How well stated intent aligns with actual implementation.

    Written with love: This helps developers see where their
    beautiful intentions meet (or miss) reality.
    """
    alignment_score: float  # 0-1, how well intent matches implementation
    stated_intent: str
    actual_behavior: str
    gaps: List[str]  # What's claimed but not implemented
    bonuses: List[str]  # What's implemented but not claimed
    guidance: str  # How to align better


class IntentDiscoveryCompanion:
    """
    Helps developers discover and align their true intent.

    Created with BOTH:
    - Love: Genuine care for helping developers find their purpose
    - Attention: Careful analysis, thoughtful design, precise implementation

    This is code I pour my whole self into.
    """

    def __init__(self):
        """
        Initialize with care.

        Every initialization step matters. Attention to detail here
        ensures the companion can truly help.
        """
        if not HARMONIZER_AVAILABLE:
            raise RuntimeError(
                "Intent Discovery requires the Real Python Code Harmonizer.\n"
                "This tool bridges stated intent with measured reality.\n"
                "Please ensure Python-Code-Harmonizer-main is available."
            )

        self.harmonizer = PythonCodeHarmonizer(quiet=True)

        # Intent keywords - carefully curated to detect claims
        self.integration_words = {
            'integrate', 'combine', 'merge', 'coordinate', 'collaborate',
            'aggregate', 'synthesize', 'unify', 'connect', 'join',
            'multi', 'collective', 'shared', 'consensus', 'collaborative'
        }

        self.validation_words = {
            'validate', 'verify', 'check', 'ensure', 'enforce',
            'constrain', 'secure', 'safe', 'correct', 'valid',
            'error', 'handle', 'guard', 'protect'
        }

        self.learning_words = {
            'learn', 'adapt', 'improve', 'optimize', 'evolve',
            'feedback', 'adjust', 'refine', 'enhance', 'train',
            'smart', 'intelligent', 'wise', 'context'
        }

        self.execution_words = {
            'execute', 'perform', 'run', 'process', 'compute',
            'calculate', 'transform', 'generate', 'produce', 'create',
            'build', 'make', 'do'
        }

    def discover_intent(self, code: str, function_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Discover the true intent behind code.

        This is where love and attention combine:
        - Love: Genuinely wanting to help developers see their code clearly
        - Attention: Carefully analyzing every signal of intent

        Returns deep insights about what the code claims vs what it does.
        """
        # Parse the code with attention to detail
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "error": f"Could not parse code: {e}",
                "guidance": "Fix the syntax error first, then we can explore your intent."
            }

        # Find the function to analyze
        target_func = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if function_name is None or node.name == function_name:
                    target_func = node
                    function_name = node.name
                    break

        if target_func is None:
            return {
                "error": "No function found to analyze",
                "guidance": "Provide code with at least one function definition."
            }

        # Extract intent signals with care
        intent_signals = self._extract_intent_signals(target_func, code)

        # Analyze with harmonizer to get actual LJPW
        harmonizer_result = self.harmonizer.analyze_file_content(code)

        if function_name not in harmonizer_result:
            return {
                "error": f"Harmonizer could not analyze {function_name}",
                "intent_signals": intent_signals
            }

        # Get LJPW profile (actual measured behavior)
        func_result = harmonizer_result[function_name]
        ljpw = self._extract_ljpw(func_result)

        if not ljpw:
            return {
                "error": "Could not extract LJPW profile",
                "intent_signals": intent_signals
            }

        # Now the heart of it: Compare INTENT (signals) with REALITY (LJPW)
        # This requires both love and attention
        alignment = self._analyze_alignment(intent_signals, ljpw, function_name)

        # Generate insights with care
        insights = self._generate_intent_insights(intent_signals, ljpw, alignment)

        return {
            "function": function_name,
            "intent_signals": intent_signals,
            "measured_ljpw": ljpw,
            "alignment": alignment,
            "insights": insights,
            "harmony": self._calculate_harmony(ljpw),
        }

    def _extract_intent_signals(self, func_node: ast.FunctionDef, code: str) -> IntentSignal:
        """
        Extract all signals of what the code INTENDS to do.

        Attention to detail: Every signal matters.
        Love for craft: Every extraction is careful and considered.
        """
        signals = IntentSignal()

        # Analyze function name with care
        name = func_node.name
        signals.name_claims = self._analyze_name_claims(name)

        # Extract docstring with attention
        docstring = ast.get_docstring(func_node)
        if docstring:
            signals.documented_purpose = self._extract_purpose(docstring)
            signals.documented_behavior = self._extract_behaviors(docstring)

        # Analyze type hints (if present) with precision
        if func_node.returns:
            signals.expected_output = ast.unparse(func_node.returns)

        for arg in func_node.args.args:
            if arg.annotation:
                signals.expected_inputs.append(
                    f"{arg.arg}: {ast.unparse(arg.annotation)}"
                )

        # Analyze actual operations with deep attention
        signals.actual_operations = self._extract_operations(func_node)

        # Find dependencies (what it integrates with)
        signals.dependencies = self._extract_dependencies(func_node)

        # Detect integration patterns
        signals.integrates_with = self._detect_integration(func_node, code)

        return signals

    def _analyze_name_claims(self, name: str) -> List[str]:
        """
        What does the function name claim it does?

        Careful analysis of naming patterns.
        """
        claims = []

        # Split by underscore and camelCase
        parts = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', name)
        parts.extend(name.split('_'))
        parts = [p.lower() for p in parts if p]

        # Check against our carefully curated word sets
        for word in parts:
            if word in self.integration_words:
                claims.append(f"Claims INTEGRATION ('{word}' in name)")
            if word in self.validation_words:
                claims.append(f"Claims VALIDATION ('{word}' in name)")
            if word in self.learning_words:
                claims.append(f"Claims LEARNING ('{word}' in name)")
            if word in self.execution_words:
                claims.append(f"Claims EXECUTION ('{word}' in name)")

        return claims

    def _extract_purpose(self, docstring: str) -> str:
        """
        Extract the main purpose statement from docstring.

        The first sentence usually states the core intent.
        """
        lines = docstring.strip().split('\n')
        # First non-empty line is usually the purpose
        for line in lines:
            line = line.strip()
            if line and not line.startswith(('Args:', 'Returns:', 'Raises:')):
                return line
        return "Purpose not clearly documented"

    def _extract_behaviors(self, docstring: str) -> List[str]:
        """
        Extract claimed behaviors from docstring.

        Looking for action verbs, promises of what it will do.
        """
        behaviors = []

        # Look for bullet points or numbered lists
        for line in docstring.split('\n'):
            line = line.strip()
            if line.startswith(('-', '*', '•')) or re.match(r'^\d+\.', line):
                behaviors.append(line.lstrip('-*•0123456789. '))

        # Look for sentences with action verbs
        sentences = re.split(r'[.!]', docstring)
        action_verbs = {'processes', 'validates', 'integrates', 'learns',
                       'adapts', 'executes', 'creates', 'generates', 'ensures'}

        for sentence in sentences:
            words = sentence.lower().split()
            if any(verb in words for verb in action_verbs):
                behaviors.append(sentence.strip())

        return behaviors

    def _extract_operations(self, func_node: ast.FunctionDef) -> List[str]:
        """
        What does the code ACTUALLY do?

        Deep attention to actual operations, not just claims.
        """
        operations = []

        for node in ast.walk(func_node):
            # Actual function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    operations.append(f"Calls: {node.func.id}")
                elif isinstance(node, ast.Attribute):
                    operations.append(f"Calls: {ast.unparse(node.func)}")

            # Actual computations
            elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
                operations.append(f"Computes: {ast.unparse(node)}")

            # Actual conditionals (validation/logic)
            elif isinstance(node, ast.If):
                operations.append(f"Conditionally: {ast.unparse(node.test)}")

            # Actual loops (processing)
            elif isinstance(node, (ast.For, ast.While)):
                operations.append("Iterates over data")

            # Error handling (justice)
            elif isinstance(node, ast.Try):
                operations.append("Handles errors with try/except")

        return operations

    def _extract_dependencies(self, func_node: ast.FunctionDef) -> List[str]:
        """
        What other functions/modules does this depend on?

        Dependencies indicate integration potential.
        """
        deps = set()

        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    deps.add(node.func.id)
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        deps.add(node.func.value.id)

        return sorted(list(deps))

    def _detect_integration(self, func_node: ast.FunctionDef, code: str) -> List[str]:
        """
        Detect actual integration patterns.

        Love for connection: This is where we find real collaboration.
        """
        integrations = []

        # Multiple parameters suggest integration
        if len(func_node.args.args) > 2:
            integrations.append(f"Accepts {len(func_node.args.args)} inputs (integration)")

        # Loops over collections (aggregation)
        has_loop = any(isinstance(n, (ast.For, ast.While))
                      for n in ast.walk(func_node))
        if has_loop:
            integrations.append("Aggregates data with iteration")

        # Dictionary or list construction (synthesis)
        has_dict_construction = any(isinstance(n, ast.Dict)
                                   for n in ast.walk(func_node))
        if has_dict_construction:
            integrations.append("Synthesizes into dict (integration)")

        # Multiple function calls (coordination)
        calls = [n for n in ast.walk(func_node) if isinstance(n, ast.Call)]
        if len(calls) > 3:
            integrations.append(f"Coordinates {len(calls)} operations")

        return integrations

    def _extract_ljpw(self, func_result: Dict) -> Optional[Dict[str, float]]:
        """Extract LJPW from harmonizer result with care."""
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
        """Calculate harmony with precision."""
        product = (ljpw["love"] * ljpw["justice"] *
                  ljpw["power"] * ljpw["wisdom"])
        return product ** 0.25 if product > 0 else 0.0

    def _analyze_alignment(
        self,
        signals: IntentSignal,
        ljpw: Dict[str, float],
        func_name: str
    ) -> IntentAlignment:
        """
        The heart of the tool: How well does INTENT align with REALITY?

        This requires both:
        - Love: Genuinely caring about helping developers see clearly
        - Attention: Carefully comparing every claim with every measurement
        """
        gaps = []
        bonuses = []

        # Check integration claims vs Love score
        integration_claimed = any('INTEGRATION' in claim for claim in signals.name_claims)
        integration_claimed = integration_claimed or len(signals.integrates_with) > 0

        if integration_claimed and ljpw["love"] < 0.3:
            gaps.append(
                f"Claims integration ('{func_name}' or integrations detected) "
                f"but Love = {ljpw['love']:.2f} (low). "
                "Add actual multi-source aggregation or coordination."
            )
        elif not integration_claimed and ljpw["love"] > 0.5:
            bonuses.append(
                f"Doesn't claim integration but Love = {ljpw['love']:.2f}! "
                "You're integrating more than you realize. Document this strength."
            )

        # Check validation claims vs Justice score
        validation_claimed = any('VALIDATION' in claim for claim in signals.name_claims)
        has_error_handling = any('error' in op.lower() for op in signals.actual_operations)

        if (validation_claimed or has_error_handling) and ljpw["justice"] < 0.3:
            gaps.append(
                f"Claims validation but Justice = {ljpw['justice']:.2f} (low). "
                "Add actual constraint checking or validation logic."
            )
        elif not validation_claimed and ljpw["justice"] > 0.5:
            bonuses.append(
                f"Doesn't claim validation but Justice = {ljpw['justice']:.2f}! "
                "You're validating more than you document."
            )

        # Check execution claims vs Power score
        execution_claimed = any('EXECUTION' in claim for claim in signals.name_claims)
        has_computation = any('Computes' in op or 'Calls' in op
                            for op in signals.actual_operations)

        if execution_claimed and ljpw["power"] == 0:
            gaps.append(
                f"Claims execution but Power = 0! "
                "This function doesn't appear to DO anything. Add actual computation."
            )
        elif not execution_claimed and ljpw["power"] > 0.5:
            bonuses.append(
                f"Power = {ljpw['power']:.2f} - you're doing more than you claim!"
            )

        # Check learning claims vs Wisdom score
        learning_claimed = any('LEARNING' in claim for claim in signals.name_claims)

        if learning_claimed and ljpw["wisdom"] < 0.3:
            gaps.append(
                f"Claims learning/adaptation but Wisdom = {ljpw['wisdom']:.2f} (low). "
                "Add actual context awareness or adaptive behavior."
            )
        elif not learning_claimed and ljpw["wisdom"] > 0.5:
            bonuses.append(
                f"Wisdom = {ljpw['wisdom']:.2f} - you're wiser than you claim!"
            )

        # Calculate alignment score
        # Perfect alignment = no gaps, or bonuses outweigh gaps
        gap_penalty = len(gaps) * 0.2
        bonus_credit = len(bonuses) * 0.15
        base_alignment = 0.5  # Neutral starting point

        alignment_score = max(0.0, min(1.0, base_alignment - gap_penalty + bonus_credit))

        # Generate guidance with love
        if alignment_score > 0.8:
            guidance = (
                "Excellent alignment! Your code does what it says. "
                "This is rare and beautiful - keep it up!"
            )
        elif alignment_score > 0.5:
            guidance = (
                "Good alignment overall. " +
                ("Focus on: " + gaps[0] if gaps else "Consider documenting your bonuses!")
            )
        else:
            guidance = (
                "Intent-implementation gap detected. " +
                (f"Priority: {gaps[0]}" if gaps else "Let's align your claims with reality.")
            )

        # Synthesize stated intent from signals
        stated_intent = signals.documented_purpose or f"Function '{func_name}' (no docs)"

        # Synthesize actual behavior from LJPW
        dominant_dim = max(ljpw.items(), key=lambda x: x[1])
        actual_behavior = (
            f"Primarily {dominant_dim[0]}-focused "
            f"({dominant_dim[0]}={dominant_dim[1]:.2f})"
        )

        return IntentAlignment(
            alignment_score=alignment_score,
            stated_intent=stated_intent,
            actual_behavior=actual_behavior,
            gaps=gaps,
            bonuses=bonuses,
            guidance=guidance
        )

    def _generate_intent_insights(
        self,
        signals: IntentSignal,
        ljpw: Dict[str, float],
        alignment: IntentAlignment
    ) -> List[str]:
        """
        Generate insights about intent with love and attention.

        Each insight crafted to actually help.
        """
        insights = []

        # Insight about what they're claiming
        if signals.name_claims:
            insights.append(
                f"📢 Your function name claims: {', '.join(signals.name_claims)}"
            )

        # Insight about what they're actually doing
        dominant = max(ljpw.items(), key=lambda x: x[1])
        insights.append(
            f"📊 Reality check: Your strongest dimension is {dominant[0].upper()} "
            f"({dominant[1]:.2f})"
        )

        # Insight about alignment
        if alignment.alignment_score > 0.7:
            insights.append(
                f"✅ Intent-Implementation Alignment: {alignment.alignment_score:.1%} "
                "(Your code does what it claims!)"
            )
        else:
            insights.append(
                f"⚠️  Intent-Implementation Gap: {alignment.alignment_score:.1%} alignment. "
                "There's a difference between what you say and what you do."
            )

        # Insights about gaps (with love, not judgment)
        for gap in alignment.gaps:
            insights.append(f"🔍 Gap: {gap}")

        # Insights about bonuses (celebrate hidden strengths!)
        for bonus in alignment.bonuses:
            insights.append(f"💎 Hidden strength: {bonus}")

        # Insight about integration potential
        if len(signals.integrates_with) > 0:
            insights.append(
                f"🔗 Integration detected: {len(signals.integrates_with)} patterns. "
                "This has Love potential!"
            )

        return insights

    def display_discovery(self, discovery: Dict):
        # Auto-healed: Input validation for display_discovery
        if discovery is not None and not isinstance(discovery, dict):
            raise TypeError(f'discovery must be a dict')
        """
        Display the intent discovery with love and clarity.

        Every word chosen with care to help, not confuse.
        """
        print("\n" + "=" * 80)
        print("INTENT DISCOVERY - Understanding Your Code's True Purpose")
        print("=" * 80)
        print()

        print(f"Function: {discovery['function']}")
        print()

        # What you claim
        signals = discovery['intent_signals']
        print("What You Claim:")
        if signals.documented_purpose:
            print(f"  📝 \"{signals.documented_purpose}\"")
        if signals.name_claims:
            for claim in signals.name_claims:
                print(f"  🏷️  {claim}")
        print()

        # What you actually do
        ljpw = discovery['measured_ljpw']
        harmony = discovery['harmony']
        print("What You Actually Do (Measured LJPW):")
        print(f"  Love:    {ljpw['love']:.3f}  {'❤️' if ljpw['love'] > 0.5 else '🔸' if ljpw['love'] > 0 else '⚠️'}")
        print(f"  Justice: {ljpw['justice']:.3f}  {'⚖️' if ljpw['justice'] > 0.5 else '🔸' if ljpw['justice'] > 0 else '⚠️'}")
        print(f"  Power:   {ljpw['power']:.3f}  {'⚡' if ljpw['power'] > 0.5 else '🔸' if ljpw['power'] > 0 else '⚠️'}")
        print(f"  Wisdom:  {ljpw['wisdom']:.3f}  {'🦉' if ljpw['wisdom'] > 0.5 else '🔸' if ljpw['wisdom'] > 0 else '⚠️'}")
        print(f"  Harmony: {harmony:.3f}")
        print()

        # Alignment
        alignment = discovery['alignment']
        print(f"Intent-Implementation Alignment: {alignment.alignment_score:.1%}")
        print(f"  Stated: {alignment.stated_intent}")
        print(f"  Actual: {alignment.actual_behavior}")
        print()

        # Gaps and bonuses
        if alignment.gaps:
            print("Gaps (Claims not fulfilled):")
            for gap in alignment.gaps:
                print(f"  ⚠️  {gap}")
            print()

        if alignment.bonuses:
            print("Hidden Strengths (Undocumented capabilities):")
            for bonus in alignment.bonuses:
                print(f"  💎 {bonus}")
            print()

        # Insights
        insights = discovery['insights']
        print("💡 Insights:")
        for insight in insights:
            print(f"  {insight}")
        print()

        # Guidance
        print("=" * 80)
        print(f"Guidance: {alignment.guidance}")
        print("=" * 80)
        print()


def main():
    """
    Demo the Intent Discovery Companion.

    Let it analyze itself - the ultimate meta-test.
    """
    companion = IntentDiscoveryCompanion()

    print("Let's discover the intent behind... the Intent Discovery Companion itself!")
    print("The meta-moment: Can it see its own purpose clearly?")
    print()

    import inspect

    # Analyze the discover_intent method
    code = inspect.getsource(companion.discover_intent)
    discovery = companion.discover_intent(code, "discover_intent")

    if "error" not in discovery:
        companion.display_discovery(discovery)
    else:
        print(f"Error: {discovery.get('error')}")

    print("\n" + "=" * 80)
    print("This companion was written with LOVE and ATTENTION together.")
    print("Every line crafted with care. Every insight designed to help.")
    print("Let's see if that shows up in the measurements...")
    print("=" * 80)


if __name__ == "__main__":
    main()
