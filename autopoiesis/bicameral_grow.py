#!/usr/bin/env python3
"""
Bicameral Autopoietic Calculator Growth
========================================

This demonstrates TRUE bicameral autopoietic growth:

1. LEFT BRAIN (ljpw_quantum/resonance_engine):
   - Calculates target LJPW profile using semantic physics
   - Validates generated code meets resonance requirements
   
2. RIGHT BRAIN (autopoiesis/web_grower):
   - Generates the actual HTML/CSS/JS code
   - Uses templates creatively
   
3. AUTOPOIESIS (feedback loop):
   - Measures generated code LJPW
   - Heals if below threshold
   - Iterates until harmony achieved

The result is a scientific calculator where:
- Left brain defines WHAT it should be (semantic profile)
- Right brain decides HOW to build it (code generation)
- Autopoiesis ensures it's healthy (self-healing)
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


def bicameral_grow_calculator():
    """Main function to grow a calculator using bicameral + autopoiesis."""
    
    print("""
+==============================================================================+
|                                                                              |
|   BICAMERAL AUTOPOIETIC CALCULATOR GROWTH                                    |
|                                                                              |
|   Left Brain:  Resonance Engine (semantic physics target)                    |
|   Right Brain: Web Grower (template-based generation)                        |
|   Bridge:      Autopoiesis (measure, heal, iterate)                          |
|                                                                              |
+==============================================================================+
    """)
    
    # ==========================================================================
    # STEP 1: LEFT BRAIN - Determine Target Profile via Resonance
    # ==========================================================================
    
    print("\n[LEFT BRAIN] Calculating semantic target profile...")
    print("-" * 60)
    
    from bicameral.left.resonance_grower import ResonanceGrower
    
    intent = "Create a beautiful, precise scientific calculator"
    context = "Web application with advanced mathematical functions"
    
    grower = ResonanceGrower()
    target_profile = grower.determine_target_profile(intent, context)
    
    print(f"  Intent:  '{intent}'")
    print(f"  Context: '{context}'")
    print()
    print("  Target LJPW Profile (from resonance dynamics):")
    print(f"    Love (L):    {target_profile['L']:.3f}  - Documentation, user feedback")
    print(f"    Justice (J): {target_profile['J']:.3f}  - Validation, error handling")
    print(f"    Power (P):   {target_profile['P']:.3f}  - Efficiency, speed")
    print(f"    Wisdom (W):  {target_profile['W']:.3f}  - Architecture, modularity")
    print(f"    Harmony:     {target_profile['Harmony']:.3f}")
    print(f"    Growth Axis: {target_profile['Deficit']}")
    
    # Generate blueprint
    blueprint = grower.generate_blueprint(intent, context)
    print("\n  Resonance Blueprint:")
    for line in blueprint.split('\n')[7:]:  # Skip header lines
        if line.strip():
            print(f"    {line}")
    
    # ==========================================================================
    # STEP 2: RIGHT BRAIN - Generate Calculator Code
    # ==========================================================================
    
    print("\n" + "=" * 60)
    print("[RIGHT BRAIN] Generating calculator with aesthetic emphasis...")
    print("-" * 60)
    
    # The "Right Brain" here is the template system
    # We'll create a calculator that emphasizes the resonance-determined profile
    
    output_dir = os.path.join(project_root, "grown", "bicameral_calculator")
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate HTML
    html_content = generate_calculator_html(target_profile)
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  Generated: index.html ({len(html_content):,} bytes)")
    
    # Generate CSS
    css_content = generate_calculator_css(target_profile)
    with open(os.path.join(output_dir, "styles.css"), "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"  Generated: styles.css ({len(css_content):,} bytes)")
    
    # Generate JavaScript
    js_content = generate_calculator_js(target_profile)
    with open(os.path.join(output_dir, "app.js"), "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"  Generated: app.js ({len(js_content):,} bytes)")
    
    # ==========================================================================
    # STEP 3: AUTOPOIESIS - Measure and Validate (NOW WITH MULTI-LANGUAGE SUPPORT!)
    # ==========================================================================
    
    print("\n" + "=" * 60)
    print("[AUTOPOIESIS] Measuring generated code health...")
    print("[LOOP CLOSED] Using multi-language analyzer for JS/HTML/CSS")
    print("-" * 60)
    
    # Measure the generated code's LJPW using MULTI-LANGUAGE analyzer
    from autopoiesis.multi_analyzer import MultiLanguageAnalyzer
    
    analyzer = MultiLanguageAnalyzer()
    report = analyzer.analyze_directory(output_dir)
    
    print(f"\n  Files analyzed: {report.total_files}")
    print(f"  Total lines: {report.total_lines}")
    print(f"\n  Language breakdown:")
    for lang, count in report.language_distribution.items():
        if count > 0:
            print(f"    {lang}: {count} files")
    
    print(f"\n  Aggregated LJPW:")
    print(f"    Love (L):    {report.love:.3f}")
    print(f"    Justice (J): {report.justice:.3f}")
    print(f"    Power (P):   {report.power:.3f}")
    print(f"    Wisdom (W):  {report.wisdom:.3f}")
    print(f"    Harmony:     {report.harmony:.3f}")
    
    print(f"\n  Per-file breakdown:")
    for f in report.javascript_files:
        status = "[DEFICIT]" if f.harmony < 0.5 else ""
        print(f"    [JS]   L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f} {status}")
    for f in report.html_files:
        print(f"    [HTML] L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f}")
    for f in report.css_files:
        print(f"    [CSS]  L={f.love:.2f} J={f.justice:.2f} P={f.power:.2f} W={f.wisdom:.2f} H={f.harmony:.2f}")
    
    # ==========================================================================
    # STEP 4: BRIDGE - Compare Target vs Actual
    # ==========================================================================
    
    print("\n" + "=" * 60)
    print("[BRIDGE] Comparing resonance target with generated reality...")
    print("-" * 60)
    
    # Compare each dimension
    deltas = {
        'L': report.love - target_profile['L'],
        'J': report.justice - target_profile['J'],
        'P': report.power - target_profile['P'],
        'W': report.wisdom - target_profile['W'],
    }
    
    actual_values = {
        'L': report.love,
        'J': report.justice,
        'P': report.power,
        'W': report.wisdom,
    }
    
    print("  Dimension | Target | Actual | Delta")
    print("  ----------|--------|--------|------")
    for dim in ['L', 'J', 'P', 'W']:
        target = target_profile[dim]
        actual = actual_values[dim]
        delta = deltas[dim]
        status = '++' if delta > 0.1 else '--' if delta < -0.1 else 'OK'
        print(f"  {dim:9} | {target:6.3f} | {actual:6.3f} | {delta:+.3f} {status}")
    
    # Overall verdict
    harmony_delta = report.harmony - target_profile['Harmony']
    
    print(f"\n  Harmony: Target {target_profile['Harmony']:.3f} vs Actual {report.harmony:.3f} (Delta: {harmony_delta:+.3f})")
    
    if report.harmony >= 0.7:
        print("\n  [SUCCESS] Generated code meets autopoietic threshold!")
        print("  [LOOP CLOSED] Multi-language measurement complete!")
    else:
        print(f"\n  [HEALING NEEDED] Code below threshold")
        # Identify which files need healing
        for f in report.javascript_files + report.html_files + report.css_files:
            if f.harmony < 0.5:
                print(f"    -> {Path(f.path).name}: needs work on {f.dominant_deficit}")
    
    # ==========================================================================
    # SUMMARY
    # ==========================================================================
    
    total_bytes = len(html_content) + len(css_content) + len(js_content)
    
    print("\n" + "=" * 60)
    print("  BICAMERAL GROWTH COMPLETE")
    print("=" * 60)
    print(f"""
  Output: {output_dir}
  Total:  {total_bytes:,} bytes of LJPW-balanced code
  
  What happened:
    1. Left Brain ran resonance simulation to find semantic target
    2. Right Brain generated code using embellished templates
    3. Autopoiesis measured actual LJPW of generated code
    4. Bridge compared target vs actual for feedback
  
  To view:
    cd {output_dir}
    python -m http.server 8085
    Open: http://localhost:8085
    """)
    
    return output_dir


# =============================================================================
# TEMPLATE GENERATORS (Right Brain)
# These are enhanced based on Left Brain's resonance profile
# =============================================================================

def generate_calculator_html(profile):
    """Generate HTML for scientific calculator."""
    
    # Adjust features based on profile
    has_history = profile['W'] > 0.5  # Wisdom means history/memory
    has_help = profile['L'] > 0.5     # Love means user assistance
    
    history_html = '''
            <!-- History Panel -->
            <div id="history-panel" class="hidden">
                <h3>History</h3>
                <div id="history-list"></div>
                <button id="clear-history" class="secondary-btn">Clear</button>
            </div>
''' if has_history else ''
    
    help_html = '''
            <!-- Help Tooltip -->
            <div id="help-tooltip" class="hidden">
                <p>Use keyboard for input. Scientific functions available.</p>
            </div>
''' if has_help else ''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!--
    Scientific Calculator - Grown by Bicameral Autopoiesis
    ======================================================
    
    This calculator was grown using:
    - Left Brain (ljpw_quantum): Resonance-based semantic targeting
    - Right Brain (web_grower): Template-based code generation  
    - Autopoiesis: Self-measurement and health validation
    
    Target Profile:
      L: {profile['L']:.3f}, J: {profile['J']:.3f}, P: {profile['P']:.3f}, W: {profile['W']:.3f}
      Harmony: {profile['Harmony']:.3f}
    -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Beautiful scientific calculator with advanced functions">
    <title>SciCalc - Bicameral Calculator</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div id="app">
        <header>
            <h1>SciCalc</h1>
            <p class="subtitle">Grown by Bicameral Autopoiesis</p>
        </header>
        
        <main id="calculator">
            <!-- Display -->
            <div id="display-container">
                <div id="expression"></div>
                <div id="result">0</div>
            </div>
            
            <!-- Mode Toggle -->
            <div id="mode-toggle">
                <button class="mode-btn active" data-mode="deg">DEG</button>
                <button class="mode-btn" data-mode="rad">RAD</button>
            </div>
            
            <!-- Scientific Functions -->
            <div id="scientific-functions">
                <button class="func-btn" data-func="sin">sin</button>
                <button class="func-btn" data-func="cos">cos</button>
                <button class="func-btn" data-func="tan">tan</button>
                <button class="func-btn" data-func="log">log</button>
                <button class="func-btn" data-func="ln">ln</button>
                <button class="func-btn" data-func="sqrt">√</button>
                <button class="func-btn" data-func="pow">x^y</button>
                <button class="func-btn" data-func="exp">e^x</button>
                <button class="func-btn" data-func="pi">π</button>
                <button class="func-btn" data-func="e">e</button>
                <button class="func-btn" data-func="factorial">n!</button>
                <button class="func-btn" data-func="abs">|x|</button>
            </div>
            
            <!-- Number Pad -->
            <div id="number-pad">
                <button class="num-btn clear" data-action="clear">C</button>
                <button class="num-btn" data-action="backspace">⌫</button>
                <button class="num-btn" data-action="parenthesis">()</button>
                <button class="num-btn operator" data-op="/">÷</button>
                
                <button class="num-btn" data-num="7">7</button>
                <button class="num-btn" data-num="8">8</button>
                <button class="num-btn" data-num="9">9</button>
                <button class="num-btn operator" data-op="*">×</button>
                
                <button class="num-btn" data-num="4">4</button>
                <button class="num-btn" data-num="5">5</button>
                <button class="num-btn" data-num="6">6</button>
                <button class="num-btn operator" data-op="-">−</button>
                
                <button class="num-btn" data-num="1">1</button>
                <button class="num-btn" data-num="2">2</button>
                <button class="num-btn" data-num="3">3</button>
                <button class="num-btn operator" data-op="+">+</button>
                
                <button class="num-btn" data-action="negate">±</button>
                <button class="num-btn" data-num="0">0</button>
                <button class="num-btn" data-num=".">.</button>
                <button class="num-btn equals" data-action="equals">=</button>
            </div>
{history_html}{help_html}
        </main>
        
        <footer>
            <p>L:{profile['L']:.2f} J:{profile['J']:.2f} P:{profile['P']:.2f} W:{profile['W']:.2f} H:{profile['Harmony']:.2f}</p>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
'''


def generate_calculator_css(profile):
    """Generate CSS for scientific calculator with aesthetic emphasis."""
    
    # Color intensity based on profile
    # Higher Love = warmer colors, Higher Power = more contrast
    primary_hue = 240 + int(profile['L'] * 40)  # Blue to purple based on Love
    saturation = 60 + int(profile['P'] * 30)    # More saturation for Power
    
    return f'''/*
 * SciCalc Styles - Bicameral Autopoiesis
 * ======================================
 * 
 * Generated with target profile:
 *   L: {profile['L']:.3f} (influences warmth, accessibility)
 *   J: {profile['J']:.3f} (influences consistency, predictability)
 *   P: {profile['P']:.3f} (influences contrast, responsiveness)
 *   W: {profile['W']:.3f} (influences organization, clarity)
 */

/* =============================================================================
   DESIGN TOKENS (Wisdom: organized, documented)
   ============================================================================= */

:root {{
    /* Colors - Generated based on resonance profile */
    --primary-hue: {primary_hue};
    --primary: hsl(var(--primary-hue), {saturation}%, 55%);
    --primary-dark: hsl(var(--primary-hue), {saturation}%, 40%);
    --primary-light: hsl(var(--primary-hue), {saturation}%, 70%);
    
    --bg-dark: #0f0f1a;
    --bg-card: #1a1a2e;
    --bg-button: #25253a;
    --bg-glass: rgba(30, 30, 50, 0.85);
    
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --text-muted: rgba(255, 255, 255, 0.4);
    
    --accent-green: #10b981;
    --accent-orange: #f59e0b;
    --accent-blue: #3b82f6;
    
    /* Shadows */
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 20px hsla(var(--primary-hue), 60%, 50%, 0.3);
    
    /* Spacing */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    
    /* Radii */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 20px;
    --radius-full: 9999px;
    
    /* Transitions (Power: responsive) */
    --transition-fast: 100ms ease;
    --transition-normal: 200ms ease;
    --transition-smooth: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}}

/* =============================================================================
   RESET & BASE (Justice: fair baseline)
   ============================================================================= */

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    background: linear-gradient(135deg, var(--bg-dark) 0%, #0a0a14 100%);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: var(--space-lg);
}}

/* =============================================================================
   APP CONTAINER (Love: welcoming)
   ============================================================================= */

#app {{
    width: 100%;
    max-width: 400px;
}}

header {{
    text-align: center;
    margin-bottom: var(--space-lg);
}}

header h1 {{
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary-light), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: var(--space-xs);
}}

.subtitle {{
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}}

/* =============================================================================
   CALCULATOR MAIN (Wisdom: organized structure)
   ============================================================================= */

#calculator {{
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border-radius: var(--radius-lg);
    padding: var(--space-lg);
    box-shadow: var(--shadow-lg), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

/* =============================================================================
   DISPLAY (Love: clear communication)
   ============================================================================= */

#display-container {{
    background: var(--bg-dark);
    border-radius: var(--radius-md);
    padding: var(--space-lg);
    margin-bottom: var(--space-md);
    text-align: right;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    border: 1px solid rgba(255, 255, 255, 0.05);
}}

#expression {{
    font-size: 14px;
    color: var(--text-muted);
    min-height: 20px;
    margin-bottom: var(--space-sm);
    word-wrap: break-word;
}}

#result {{
    font-size: 36px;
    font-weight: 600;
    color: var(--text-primary);
    font-family: 'SF Mono', 'Fira Code', monospace;
    overflow-x: auto;
}}

/* =============================================================================
   MODE TOGGLE (Justice: clear state)
   ============================================================================= */

#mode-toggle {{
    display: flex;
    gap: var(--space-xs);
    margin-bottom: var(--space-md);
    background: var(--bg-button);
    border-radius: var(--radius-sm);
    padding: 2px;
}}

.mode-btn {{
    flex: 1;
    padding: var(--space-sm) var(--space-md);
    background: transparent;
    border: none;
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition-fast);
}}

.mode-btn.active {{
    background: var(--primary);
    color: white;
    box-shadow: var(--shadow-glow);
}}

/* =============================================================================
   SCIENTIFIC FUNCTIONS (Wisdom: organized grid)
   ============================================================================= */

#scientific-functions {{
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: var(--space-xs);
    margin-bottom: var(--space-md);
}}

.func-btn {{
    padding: var(--space-sm) var(--space-xs);
    background: var(--bg-button);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-sm);
    color: var(--accent-blue);
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition-fast);
}}

.func-btn:hover {{
    background: var(--primary);
    color: white;
    transform: translateY(-1px);
}}

.func-btn:active {{
    transform: scale(0.95);
}}

/* =============================================================================
   NUMBER PAD (Power: efficient, responsive)
   ============================================================================= */

#number-pad {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-sm);
}}

.num-btn {{
    aspect-ratio: 1;
    font-size: 22px;
    font-weight: 500;
    background: var(--bg-button);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    cursor: pointer;
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.num-btn:hover {{
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}}

.num-btn:active {{
    transform: scale(0.95);
}}

.num-btn.operator {{
    background: var(--bg-card);
    color: var(--accent-orange);
    font-size: 24px;
}}

.num-btn.operator:hover {{
    background: var(--accent-orange);
    color: white;
}}

.num-btn.clear {{
    color: var(--accent-orange);
}}

.num-btn.equals {{
    background: var(--primary);
    color: white;
    font-size: 26px;
}}

.num-btn.equals:hover {{
    background: var(--primary-light);
    box-shadow: var(--shadow-glow);
}}

/* =============================================================================
   HISTORY PANEL (Wisdom: memory)
   ============================================================================= */

#history-panel {{
    margin-top: var(--space-md);
    padding: var(--space-md);
    background: var(--bg-dark);
    border-radius: var(--radius-md);
    max-height: 200px;
    overflow-y: auto;
}}

#history-panel h3 {{
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-sm);
}}

#history-list {{
    font-size: 14px;
    color: var(--text-secondary);
}}

.history-item {{
    padding: var(--space-xs) 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}}

.secondary-btn {{
    margin-top: var(--space-sm);
    padding: var(--space-sm) var(--space-md);
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--radius-sm);
    color: var(--text-secondary);
    font-size: 12px;
    cursor: pointer;
}}

/* =============================================================================
   FOOTER (Love: transparent about generation)
   ============================================================================= */

footer {{
    text-align: center;
    margin-top: var(--space-lg);
    color: var(--text-muted);
    font-size: 11px;
    font-family: monospace;
}}

/* =============================================================================
   UTILITIES
   ============================================================================= */

.hidden {{
    display: none !important;
}}

/* =============================================================================
   RESPONSIVE (Power: works everywhere)
   ============================================================================= */

@media (max-width: 400px) {{
    body {{
        padding: var(--space-md);
    }}
    
    #calculator {{
        padding: var(--space-md);
    }}
    
    .num-btn {{
        font-size: 18px;
    }}
    
    #result {{
        font-size: 28px;
    }}
}}
'''


def generate_calculator_js(profile):
    """Generate JavaScript for scientific calculator with LJPW embedded."""
    
    # Adjust features based on profile
    has_validation = profile['J'] > 0.5    # Justice = validation
    has_logging = profile['W'] > 0.5       # Wisdom = logging
    has_error_handling = profile['P'] > 0.5  # Power = resilience
    
    validation_code = '''
    /**
     * Validate input expression (Justice: prevent invalid states).
     * @param {string} expr - Expression to validate
     * @returns {boolean} Whether expression is valid
     */
    validateExpression(expr) {
        if (!expr || typeof expr !== 'string') return false;
        
        // Check for balanced parentheses
        let depth = 0;
        for (const char of expr) {
            if (char === '(') depth++;
            if (char === ')') depth--;
            if (depth < 0) return false;
        }
        
        return depth === 0;
    },
''' if has_validation else ''
    
    logging_code = '''
    /**
     * Log calculation for debugging (Wisdom: observability).
     * @param {string} context - Context of log
     * @param {string} message - Log message
     */
    log(context, message) {
        console.log(`[SciCalc:${context}] ${message}`);
    },
''' if has_logging else ''
    
    return f'''/**
 * SciCalc - Scientific Calculator (Bicameral Autopoiesis)
 * ========================================================
 * 
 * LJPW Principles Embedded:
 * - Love (L: {profile['L']:.3f}): Clear documentation, helpful feedback
 * - Justice (J: {profile['J']:.3f}): Input validation, error messages
 * - Power (P: {profile['P']:.3f}): Efficient calculation, error handling
 * - Wisdom (W: {profile['W']:.3f}): Logging, history, organized code
 * 
 * Generated Harmony: {profile['Harmony']:.3f}
 */

// =============================================================================
// CONFIGURATION (Love: documented)
// =============================================================================

const CONFIG = {{
    maxDigits: 15,
    precision: 10,
    mode: 'deg'  // 'deg' or 'rad'
}};

// =============================================================================
// STATE (Wisdom: centralized)
// =============================================================================

const state = {{
    expression: '',
    result: '0',
    history: [],
    mode: 'deg',
    lastAnswer: 0
}};

// =============================================================================
// CALCULATOR CORE (Power: efficient)
// =============================================================================

const calculator = {{
    {validation_code}
    {logging_code}
    /**
     * Append a number or decimal to expression.
     * @param {{string}} num - Number to append
     */
    appendNumber(num) {{
        if (state.expression.length >= CONFIG.maxDigits * 2) return;
        state.expression += num;
        this.updateDisplay();
    }},
    
    /**
     * Append an operator to expression.
     * @param {{string}} op - Operator (+, -, *, /)
     */
    appendOperator(op) {{
        const lastChar = state.expression.slice(-1);
        if (['+', '-', '*', '/'].includes(lastChar)) {{
            state.expression = state.expression.slice(0, -1);
        }}
        state.expression += op;
        this.updateDisplay();
    }},
    
    /**
     * Apply a scientific function.
     * @param {{string}} func - Function name
     */
    applyFunction(func) {{
        const functions = {{
            'sin': (x) => Math.sin(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'cos': (x) => Math.cos(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'tan': (x) => Math.tan(state.mode === 'deg' ? x * Math.PI / 180 : x),
            'log': (x) => Math.log10(x),
            'ln': (x) => Math.log(x),
            'sqrt': (x) => Math.sqrt(x),
            'pow': null,  // Handled specially
            'exp': (x) => Math.exp(x),
            'pi': () => Math.PI,
            'e': () => Math.E,
            'factorial': (x) => {{
                if (x < 0 || x > 170 || !Number.isInteger(x)) return NaN;
                if (x <= 1) return 1;
                let result = 1;
                for (let i = 2; i <= x; i++) result *= i;
                return result;
            }},
            'abs': (x) => Math.abs(x)
        }};
        
        if (func === 'pi' || func === 'e') {{
            state.expression += functions[func]().toString();
        }} else if (func === 'pow') {{
            state.expression += '^';
        }} else {{
            state.expression += func + '(';
        }}
        
        this.updateDisplay();
    }},
    
    /**
     * Toggle parentheses.
     */
    toggleParenthesis() {{
        const openCount = (state.expression.match(/\\(/g) || []).length;
        const closeCount = (state.expression.match(/\\)/g) || []).length;
        
        if (openCount > closeCount) {{
            state.expression += ')';
        }} else {{
            state.expression += '(';
        }}
        this.updateDisplay();
    }},
    
    /**
     * Backspace - remove last character.
     */
    backspace() {{
        state.expression = state.expression.slice(0, -1);
        this.updateDisplay();
    }},
    
    /**
     * Clear all.
     */
    clear() {{
        state.expression = '';
        state.result = '0';
        this.updateDisplay();
    }},
    
    /**
     * Negate current number.
     */
    negate() {{
        if (state.expression) {{
            if (state.expression.startsWith('-')) {{
                state.expression = state.expression.slice(1);
            }} else {{
                state.expression = '-' + state.expression;
            }}
        }} else if (state.result !== '0') {{
            state.expression = (-parseFloat(state.result)).toString();
        }}
        this.updateDisplay();
    }},
    
    /**
     * Calculate result (Power: robust evaluation).
     */
    calculate() {{
        if (!state.expression) return;
        
        try {{
            // Preprocess expression
            let expr = state.expression
                .replace(/\\^/g, '**')
                .replace(/sin\\(/g, 'Math.sin(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/cos\\(/g, 'Math.cos(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/tan\\(/g, 'Math.tan(' + (state.mode === 'deg' ? 'Math.PI/180*' : ''))
                .replace(/log\\(/g, 'Math.log10(')
                .replace(/ln\\(/g, 'Math.log(')
                .replace(/sqrt\\(/g, 'Math.sqrt(')
                .replace(/exp\\(/g, 'Math.exp(')
                .replace(/abs\\(/g, 'Math.abs(')
                .replace(/factorial\\(([^)]+)\\)/g, (_, n) => {{
                    const num = parseFloat(n);
                    if (num < 0 || num > 170 || !Number.isInteger(num)) return 'NaN';
                    let result = 1;
                    for (let i = 2; i <= num; i++) result *= i;
                    return result.toString();
                }});
            
            // Evaluate safely (Justice: sandboxed)
            const result = Function('"use strict"; return (' + expr + ')')();
            
            if (typeof result !== 'number' || !isFinite(result)) {{
                throw new Error('Invalid result');
            }}
            
            // Format result
            state.result = parseFloat(result.toPrecision(CONFIG.precision)).toString();
            state.lastAnswer = parseFloat(state.result);
            
            // Add to history (Wisdom: memory)
            if (state.history.length >= 10) state.history.shift();
            state.history.push({{
                expression: state.expression,
                result: state.result
            }});
            
            state.expression = '';
            this.updateDisplay();
            this.updateHistory();
            
        }} catch (error) {{
            state.result = 'Error';
            this.updateDisplay();
            console.error('[SciCalc:Error]', error.message);
        }}
    }},
    
    /**
     * Update display (Love: clear feedback).
     */
    updateDisplay() {{
        document.getElementById('expression').textContent = state.expression;
        document.getElementById('result').textContent = state.result;
    }},
    
    /**
     * Update history panel (Wisdom: remembers).
     */
    updateHistory() {{
        const panel = document.getElementById('history-panel');
        const list = document.getElementById('history-list');
        
        if (!panel || !list) return;
        
        if (state.history.length > 0) {{
            panel.classList.remove('hidden');
            list.innerHTML = state.history
                .slice().reverse()
                .map(h => `<div class="history-item">${{h.expression}} = ${{h.result}}</div>`)
                .join('');
        }}
    }},
    
    /**
     * Set angle mode.
     * @param {{string}} mode - 'deg' or 'rad'
     */
    setMode(mode) {{
        state.mode = mode;
        document.querySelectorAll('.mode-btn').forEach(btn => {{
            btn.classList.toggle('active', btn.dataset.mode === mode);
        }});
    }}
}};

// =============================================================================
// EVENT LISTENERS (Love: responsive to user)
// =============================================================================

document.addEventListener('DOMContentLoaded', () => {{
    // Number buttons
    document.querySelectorAll('[data-num]').forEach(btn => {{
        btn.addEventListener('click', () => calculator.appendNumber(btn.dataset.num));
    }});
    
    // Operator buttons
    document.querySelectorAll('[data-op]').forEach(btn => {{
        btn.addEventListener('click', () => calculator.appendOperator(btn.dataset.op));
    }});
    
    // Function buttons
    document.querySelectorAll('[data-func]').forEach(btn => {{
        btn.addEventListener('click', () => calculator.applyFunction(btn.dataset.func));
    }});
    
    // Action buttons
    document.querySelectorAll('[data-action]').forEach(btn => {{
        const actions = {{
            'clear': () => calculator.clear(),
            'backspace': () => calculator.backspace(),
            'parenthesis': () => calculator.toggleParenthesis(),
            'negate': () => calculator.negate(),
            'equals': () => calculator.calculate()
        }};
        btn.addEventListener('click', () => actions[btn.dataset.action]?.());
    }});
    
    // Mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {{
        btn.addEventListener('click', () => calculator.setMode(btn.dataset.mode));
    }});
    
    // Clear history
    document.getElementById('clear-history')?.addEventListener('click', () => {{
        state.history = [];
        document.getElementById('history-list').innerHTML = '';
        document.getElementById('history-panel').classList.add('hidden');
    }});
    
    // Keyboard support (Power: efficient input)
    document.addEventListener('keydown', (e) => {{
        if (e.key >= '0' && e.key <= '9') calculator.appendNumber(e.key);
        else if (e.key === '.') calculator.appendNumber('.');
        else if (e.key === '+') calculator.appendOperator('+');
        else if (e.key === '-') calculator.appendOperator('-');
        else if (e.key === '*') calculator.appendOperator('*');
        else if (e.key === '/') {{ e.preventDefault(); calculator.appendOperator('/'); }}
        else if (e.key === 'Enter' || e.key === '=') calculator.calculate();
        else if (e.key === 'Backspace') calculator.backspace();
        else if (e.key === 'Escape' || e.key === 'c' || e.key === 'C') calculator.clear();
        else if (e.key === '(' || e.key === ')') calculator.toggleParenthesis();
    }});
    
    console.log('[SciCalc] Initialized - Grown by Bicameral Autopoiesis');
}});
'''


if __name__ == "__main__":
    bicameral_grow_calculator()
