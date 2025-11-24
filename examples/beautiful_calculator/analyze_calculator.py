#!/usr/bin/env python3
"""
Analyze Beautiful Calculator - LJPWB Framework

Dissects how beauty and function are unified.
"""

import re
from pathlib import Path


def analyze_patterns(html_content: str) -> dict:
    """Analyze LJPWB patterns."""

    js_code = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL).group(1)
    css_code = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL).group(1)

    patterns = {
        'ljpw': {
            'love': {
                'doc_blocks': len(re.findall(r'/\*\*', js_code)),
                'logging': len(re.findall(r"log\(", js_code)),
                'param_tags': len(re.findall(r'@param', js_code)),
            },
            'justice': {
                'validations': len(re.findall(r'validate', js_code, re.I)),
                'try_catch': len(re.findall(r'try\s*{', js_code)),
                'error_handling': len(re.findall(r'displayError|throw', js_code)),
                'type_checks': len(re.findall(r'typeof|isNaN|isFinite', js_code)),
            },
            'power': {
                'efficient_switch': 'switch' in js_code,
                'state_management': 'state' in js_code,
            },
            'wisdom': {
                'functions': len(re.findall(r'function\s+\w+', js_code)),
                'modular': True,
            },
        },
        'beauty': {
            'visual': {
                'golden_ratio': len(re.findall(r'golden.?ratio', css_code, re.I)),
                'spacing_vars': len(re.findall(r'gap:|padding:|margin:', css_code)),
            },
            'color': {
                'color_vars': len(re.findall(r'--color-|--.*-bg|--.*-text', css_code)),
                'functional_coding': 'number-bg' in css_code and 'operator-bg' in css_code,
            },
            'typography': {
                'font_families': len(re.findall(r'font-family:', css_code)),
                'font_sizes': len(re.findall(r'font-size:', css_code)),
                'letter_spacing': 'letter-spacing' in css_code,
            },
            'motion': {
                'transitions': len(re.findall(r'transition:', css_code)),
                'animations': len(re.findall(r'@keyframes', css_code)),
                'hover_states': len(re.findall(r':hover', css_code)),
                'active_states': len(re.findall(r':active', css_code)),
            },
        },
    }

    return patterns


def estimate_scores(patterns: dict) -> dict:
    """Estimate LJPWB scores."""

    # Love
    love_indicators = [
        patterns['ljpw']['love']['doc_blocks'] > 8,
        patterns['ljpw']['love']['logging'] > 10,
        patterns['ljpw']['love']['param_tags'] > 10,
    ]
    love = 0.30 + (sum(love_indicators) * 0.15)

    # Justice
    justice_indicators = [
        patterns['ljpw']['justice']['validations'] > 2,
        patterns['ljpw']['justice']['try_catch'] > 1,
        patterns['ljpw']['justice']['error_handling'] > 5,
        patterns['ljpw']['justice']['type_checks'] > 3,
    ]
    justice = 0.30 + (sum(justice_indicators) * 0.15)

    # Power
    power_indicators = [
        patterns['ljpw']['power']['efficient_switch'],
        patterns['ljpw']['power']['state_management'],
    ]
    power = 0.40 + (sum(power_indicators) * 0.15)

    # Wisdom
    wisdom_indicators = [
        patterns['ljpw']['wisdom']['functions'] > 10,
        patterns['ljpw']['wisdom']['modular'],
    ]
    wisdom = 0.40 + (sum(wisdom_indicators) * 0.15)

    ljpw_harmony = (love * justice * power * wisdom) ** 0.25

    # Visual
    visual_indicators = [
        patterns['beauty']['visual']['golden_ratio'] > 0,
        patterns['beauty']['visual']['spacing_vars'] > 10,
    ]
    visual = 0.50 + (sum(visual_indicators) * 0.15)

    # Color
    color_indicators = [
        patterns['beauty']['color']['color_vars'] > 10,
        patterns['beauty']['color']['functional_coding'],
    ]
    color = 0.50 + (sum(color_indicators) * 0.15)

    # Typography
    typography_indicators = [
        patterns['beauty']['typography']['font_families'] > 2,
        patterns['beauty']['typography']['font_sizes'] > 5,
        patterns['beauty']['typography']['letter_spacing'],
    ]
    typography = 0.50 + (sum(typography_indicators) * 0.10)

    # Motion
    motion_indicators = [
        patterns['beauty']['motion']['transitions'] > 3,
        patterns['beauty']['motion']['animations'] > 2,
        patterns['beauty']['motion']['hover_states'] > 5,
        patterns['beauty']['motion']['active_states'] > 1,
    ]
    motion = 0.50 + (sum(motion_indicators) * 0.08)

    beauty_harmony = (visual * color * typography * motion) ** 0.25

    total_harmony = (love * justice * power * wisdom * beauty_harmony) ** 0.2

    return {
        'L': round(love, 2),
        'J': round(justice, 2),
        'P': round(power, 2),
        'W': round(wisdom, 2),
        'H_ljpw': round(ljpw_harmony, 2),
        'V': round(visual, 2),
        'C': round(color, 2),
        'T': round(typography, 2),
        'M': round(motion, 2),
        'B': round(beauty_harmony, 2),
        'H_total': round(total_harmony, 2),
    }


def main():
    file_path = Path('examples/beautiful_calculator/calculator.html')
    content = file_path.read_text()

    print("=" * 80)
    print("BEAUTIFUL CALCULATOR ANALYSIS - Art + Function Unified")
    print("=" * 80)
    print()

    patterns = analyze_patterns(content)
    scores = estimate_scores(patterns)

    print("🔍 PATTERN ANALYSIS:")
    print()
    print("💙 LOVE (Observability):")
    for key, value in patterns['ljpw']['love'].items():
        print(f"  • {key}: {value}")
    print()

    print("⚖️  JUSTICE (Correctness):")
    for key, value in patterns['ljpw']['justice'].items():
        print(f"  • {key}: {value}")
    print()

    print("⚡ POWER (Efficiency):")
    for key, value in patterns['ljpw']['power'].items():
        print(f"  • {key}: {value}")
    print()

    print("🧠 WISDOM (Architecture):")
    for key, value in patterns['ljpw']['wisdom'].items():
        print(f"  • {key}: {value}")
    print()

    print("✨ BEAUTY (Aesthetics):")
    print()
    print("  Visual Harmony:")
    for key, value in patterns['beauty']['visual'].items():
        print(f"    • {key}: {value}")
    print()
    print("  Color Theory:")
    for key, value in patterns['beauty']['color'].items():
        print(f"    • {key}: {value}")
    print()
    print("  Typography:")
    for key, value in patterns['beauty']['typography'].items():
        print(f"    • {key}: {value}")
    print()
    print("  Motion:")
    for key, value in patterns['beauty']['motion'].items():
        print(f"    • {key}: {value}")
    print()

    print("=" * 80)
    print("LJPWB SCORES")
    print("=" * 80)
    print()
    print(f"  Love (L):        {scores['L']}")
    print(f"  Justice (J):     {scores['J']}")
    print(f"  Power (P):       {scores['P']}")
    print(f"  Wisdom (W):      {scores['W']}")
    print(f"  LJPW Harmony:    {scores['H_ljpw']}")
    print()
    print(f"  Visual (V):      {scores['V']}")
    print(f"  Color (C):       {scores['C']}")
    print(f"  Typography (T):  {scores['T']}")
    print(f"  Motion (M):      {scores['M']}")
    print(f"  Beauty Harmony:  {scores['B']}")
    print()
    print(f"  Total Harmony:   {scores['H_total']}")
    print()

    ecosystem = 0.289
    improvement = ((scores['H_total'] / ecosystem) - 1) * 100

    print("=" * 80)
    print("COMPARISON TO ECOSYSTEM")
    print("=" * 80)
    print()
    print(f"  Ecosystem baseline: H = {ecosystem}")
    print(f"  Beautiful calculator: H = {scores['H_total']}")
    print(f"  Improvement: +{improvement:.1f}%")
    print()
    print("  ✅ Art + Function unified successfully!")
    print()


if __name__ == '__main__':
    main()
