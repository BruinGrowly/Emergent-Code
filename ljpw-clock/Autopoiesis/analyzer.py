#!/usr/bin/env python3
"""
LJPW Analyzer
=============

Measures LJPW dimensions in code files.

This is a simplified analyzer focused on the patterns that matter most
for the LJPW clock grower.

Usage:
    from analyzer import analyze_file
    
    result = analyze_file("app.js")
    print(result)  # {'L': 0.85, 'J': 0.90, 'P': 0.75, 'W': 0.80, 'H': 0.82}
"""

import re
from pathlib import Path
from typing import Dict, Optional


def analyze_file(filepath: str) -> Dict[str, float]:
    """Analyze LJPW dimensions in a file.
    
    Args:
        filepath: Path to file to analyze
        
    Returns:
        Dictionary with L, J, P, W, and H (harmony) values
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    content = path.read_text(encoding='utf-8')
    
    # Dispatch by file type
    if path.suffix == '.js':
        return analyze_javascript(content)
    elif path.suffix == '.css':
        return analyze_css(content)
    elif path.suffix == '.html':
        return analyze_html(content)
    elif path.suffix == '.py':
        return analyze_python(content)
    else:
        return analyze_generic(content)


def analyze_javascript(content: str) -> Dict[str, float]:
    """Analyze JavaScript for LJPW dimensions."""
    lines = content.split('\n')
    total_lines = max(len(lines), 1)
    
    # Love: Documentation, comments, console.log for communication
    doc_comments = len(re.findall(r'/\*\*[\s\S]*?\*/', content))
    inline_comments = len(re.findall(r'//.*$', content, re.MULTILINE))
    console_logs = len(re.findall(r'console\.(log|info)', content))
    love = min(1.0, (doc_comments * 5 + inline_comments + console_logs * 2) / total_lines)
    
    # Justice: Validation, error handling
    try_catches = len(re.findall(r'try\s*{', content))
    if_checks = len(re.findall(r'if\s*\(', content))
    throws = len(re.findall(r'throw\s+', content))
    justice = min(1.0, (try_catches * 5 + if_checks * 0.5 + throws * 3) / total_lines)
    
    # Power: Optimization patterns
    const_usage = len(re.findall(r'\bconst\b', content))
    raf = len(re.findall(r'requestAnimationFrame', content))
    cached = len(re.findall(r'getElementById|querySelector', content))
    power = min(1.0, (const_usage * 0.5 + raf * 10 + cached) / total_lines)
    
    # Wisdom: Modular patterns, self-awareness
    functions = len(re.findall(r'function\s+\w+', content))
    exports = len(re.findall(r'window\.\w+\s*=|export\s+', content))
    metrics = 'LJPW' in content or 'metrics' in content
    wisdom = min(1.0, (functions * 2 + exports * 5 + (10 if metrics else 0)) / total_lines)
    
    # Normalize to reasonable ranges
    love = 0.5 + love * 0.5
    justice = 0.5 + justice * 0.5
    power = 0.5 + power * 0.5
    wisdom = 0.5 + wisdom * 0.5
    
    harmony = (love * justice * power * wisdom) ** 0.25
    
    return {
        'L': round(love, 2),
        'J': round(justice, 2),
        'P': round(power, 2),
        'W': round(wisdom, 2),
        'H': round(harmony, 2)
    }


def analyze_css(content: str) -> Dict[str, float]:
    """Analyze CSS for LJPW dimensions."""
    lines = content.split('\n')
    total_lines = max(len(lines), 1)
    
    # Love: Comments, CSS variables (design tokens)
    comments = len(re.findall(r'/\*[\s\S]*?\*/', content))
    variables = len(re.findall(r'--[\w-]+:', content))
    love_color = '--love-color' in content
    love = min(1.0, (comments * 2 + variables * 0.5 + (5 if love_color else 0)) / total_lines)
    
    # Justice: Consistent patterns, media queries
    media_queries = len(re.findall(r'@media', content))
    root_block = ':root' in content
    justice = min(1.0, (media_queries * 3 + (5 if root_block else 0)) / total_lines)
    
    # Power: Animations, transitions
    animations = len(re.findall(r'@keyframes|animation:', content))
    transitions = len(re.findall(r'transition:', content))
    power = min(1.0, (animations * 3 + transitions * 2) / total_lines)
    
    # Wisdom: Organization (comments per section)
    section_comments = len(re.findall(r'/\*\s*=+', content))
    wisdom = min(1.0, section_comments * 5 / total_lines)
    
    # Normalize
    love = 0.5 + love * 0.5
    justice = 0.5 + justice * 0.5
    power = 0.5 + power * 0.5
    wisdom = 0.5 + wisdom * 0.5
    
    harmony = (love * justice * power * wisdom) ** 0.25
    
    return {
        'L': round(love, 2),
        'J': round(justice, 2),
        'P': round(power, 2),
        'W': round(wisdom, 2),
        'H': round(harmony, 2)
    }


def analyze_html(content: str) -> Dict[str, float]:
    """Analyze HTML for LJPW dimensions."""
    lines = content.split('\n')
    total_lines = max(len(lines), 1)
    
    # Love: Comments, accessibility, meta description
    comments = len(re.findall(r'<!--[\s\S]*?-->', content))
    meta_desc = 'meta name="description"' in content
    love = min(1.0, (comments * 3 + (5 if meta_desc else 0)) / total_lines)
    
    # Justice: Semantic elements
    semantic = len(re.findall(r'<(header|main|section|footer|article|nav)', content))
    justice = min(1.0, semantic * 3 / total_lines)
    
    # Power: External resources, responsive viewport
    viewport = 'viewport' in content
    external = len(re.findall(r'<(script|link)\s+', content))
    power = min(1.0, ((5 if viewport else 0) + external * 2) / total_lines)
    
    # Wisdom: Title, structure
    has_title = '<title>' in content
    wisdom = min(1.0, (5 if has_title else 0) / total_lines)
    
    # Normalize
    love = 0.5 + love * 0.5
    justice = 0.5 + justice * 0.5
    power = 0.5 + power * 0.5
    wisdom = 0.5 + wisdom * 0.5
    
    harmony = (love * justice * power * wisdom) ** 0.25
    
    return {
        'L': round(love, 2),
        'J': round(justice, 2),
        'P': round(power, 2),
        'W': round(wisdom, 2),
        'H': round(harmony, 2)
    }


def analyze_python(content: str) -> Dict[str, float]:
    """Analyze Python for LJPW dimensions."""
    lines = content.split('\n')
    total_lines = max(len(lines), 1)
    
    # Love: Docstrings, comments
    docstrings = len(re.findall(r'"""[\s\S]*?"""', content))
    comments = len(re.findall(r'#.*$', content, re.MULTILINE))
    love = min(1.0, (docstrings * 5 + comments * 0.5) / total_lines)
    
    # Justice: Type hints, validation
    type_hints = len(re.findall(r':\s*(str|int|float|bool|Dict|List)', content))
    asserts = len(re.findall(r'\bassert\b', content))
    justice = min(1.0, (type_hints + asserts * 2) / total_lines)
    
    # Power: Error handling
    try_except = len(re.findall(r'try:', content))
    raises = len(re.findall(r'raise\s+', content))
    power = min(1.0, (try_except * 3 + raises * 2) / total_lines)
    
    # Wisdom: Classes, functions
    classes = len(re.findall(r'class\s+\w+', content))
    functions = len(re.findall(r'def\s+\w+', content))
    wisdom = min(1.0, (classes * 3 + functions) / total_lines)
    
    # Normalize
    love = 0.5 + love * 0.5
    justice = 0.5 + justice * 0.5
    power = 0.5 + power * 0.5
    wisdom = 0.5 + wisdom * 0.5
    
    harmony = (love * justice * power * wisdom) ** 0.25
    
    return {
        'L': round(love, 2),
        'J': round(justice, 2),
        'P': round(power, 2),
        'W': round(wisdom, 2),
        'H': round(harmony, 2)
    }


def analyze_generic(content: str) -> Dict[str, float]:
    """Generic analysis for unknown file types."""
    return {
        'L': 0.75,
        'J': 0.75,
        'P': 0.75,
        'W': 0.75,
        'H': 0.75
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <file>")
        sys.exit(1)
    
    result = analyze_file(sys.argv[1])
    print(f"LJPW Analysis: L={result['L']}, J={result['J']}, P={result['P']}, W={result['W']}, H={result['H']}")
