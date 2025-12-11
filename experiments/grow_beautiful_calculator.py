"""
Experiment: Grow an Aesthetically Pleasing Calculator (v6.0)
Uses ResonanceGrower to determine the 'Physics' of beauty, then materializes it.
"""

import sys
import os
import math

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_grower import ResonanceGrower
from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

class AestheticMaterializer:
    """
    Translates LJPW coordinates into CSS/HTML/JS physics.
    """
    def __init__(self, profile):
        self.L = profile['L']
        self.J = profile['J']
        self.P = profile['P']
        self.W = profile['W']

    def materialize_css(self) -> str:
        """
        Love dictates Aesthetics.
        Higher L = More gradients, blur, animation, softness.
        """
        # Physics of Beauty
        border_radius = int(self.L * 30)  # Up to 30px
        blur_amount = int(self.L * 20)    # Up to 20px
        animation_duration = max(0.2, 1.0 - self.P * 0.5) # Power makes it faster
        
        css = f"""
        :root {{
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            --glass-bg: rgba(255, 255, 255, {0.7 if self.L > 0.7 else 0.9});
            --glass-border: 1px solid rgba(255, 255, 255, 0.5);
            --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            --radius: {border_radius}px;
            --anim-speed: {animation_duration}s;
        }}

        body {{
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0f172a;
            font-family: 'Segoe UI', sans-serif;
            overflow: hidden;
        }}

        /* Background Orb for Aesthetics */
        .orb {{
            position: absolute;
            width: 500px;
            height: 500px;
            background: var(--primary-gradient);
            filter: blur(80px);
            border-radius: 50%;
            animation: float 10s infinite ease-in-out;
            z-index: 0;
        }}

        .calculator {{
            position: relative;
            z-index: 1;
            background: var(--glass-bg);
            backdrop-filter: blur({blur_amount}px);
            -webkit-backdrop-filter: blur({blur_amount}px);
            border: var(--glass-border);
            border-radius: var(--radius);
            box-shadow: var(--shadow);
            padding: 2rem;
            width: 320px;
            transition: transform 0.3s;
        }}
        
        .calculator:hover {{
            transform: translateY(-5px);
        }}

        .display {{
            width: 100%;
            height: 80px;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.5);
            border-radius: calc(var(--radius) / 2);
            border: none;
            font-size: 2.5rem;
            text-align: right;
            padding: 1rem;
            color: #1e293b;
            box-sizing: border-box;
        }}

        .buttons {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }}

        button {{
            padding: 15px;
            border: none;
            border-radius: calc(var(--radius) / 2);
            font-size: 1.2rem;
            cursor: pointer;
            background: rgba(255, 255, 255, 0.8);
            transition: all 0.2s;
            color: #334155;
            font-weight: 600;
        }}

        button:hover {{
            background: white;
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }}

        button.operator {{
            background: rgba(99, 102, 241, 0.1);
            color: #6366f1;
        }}

        button.equals {{
            background: var(--primary-gradient);
            color: white;
            grid-column: span 2;
        }}

        @keyframes float {{
            0% {{ transform: translate(0px, 0px) scale(1); }}
            33% {{ transform: translate(30px, -50px) scale(1.1); }}
            66% {{ transform: translate(-20px, 20px) scale(0.9); }}
            100% {{ transform: translate(0px, 0px) scale(1); }}
        }}
        """
        return css

    def materialize_js(self) -> str:
        """
        Justice dictates Logic.
        Higher J = More validation, error handling.
        Power dictates Efficiency.
        Higher P = Keyboard Support.
        """
        validation_code = ""
        if self.J > 0.6:
            validation_code = """
            // Justice: Validation
            if (['+', '-', '*', '/'].includes(lastChar) && ['+', '-', '*', '/'].includes(value)) {
                return; // Prevent double operators
            }
            """
        
        keyboard_code = ""
        if self.P > 0.6:
            keyboard_code = """
            // Power: Keyboard Support
            document.addEventListener('keydown', (e) => {
                const key = e.key;
                const map = {'Enter': '=', 'Escape': 'C', 'Backspace': 'C'};
                const target = map[key] || key;
                
                // Find button with matching text
                const btn = Array.from(buttons).find(b => b.innerText === target);
                
                if (btn) {
                    btn.click();
                    // Love: Visual feedback on keypress
                    btn.style.transform = 'scale(0.95)';
                    setTimeout(() => btn.style.transform = '', 100);
                }
            });
            """
            
        return f"""
        const display = document.querySelector('.display');
        const buttons = document.querySelectorAll('button');
        
        {keyboard_code}
        
        buttons.forEach(btn => {{
            btn.addEventListener('click', () => {{
                const value = btn.innerText;
                const current = display.value;
                const lastChar = current[current.length - 1];

                if (value === 'C') {{
                    display.value = '';
                }} else if (value === '=') {{
                    try {{
                        // Power: Execution
                        display.value = eval(current);
                    }} catch (e) {{
                        // Love: Friendly Error
                        display.value = 'Oops!';
                        setTimeout(() => display.value = '', 1000);
                    }}
                }} else {{
                    {validation_code}
                    display.value += value;
                }}
            }});
        }});
        """

    def generate_html(self) -> str:
        css = self.materialize_css()
        js = self.materialize_js()
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Resonance Calculator</title>
    <style>{css}</style>
</head>
<body>
    <div class="orb"></div>
    <div class="calculator">
        <input type="text" class="display" readonly>
        <div class="buttons">
            <button class="operator">C</button>
            <button class="operator">/</button>
            <button class="operator">*</button>
            <button class="operator">-</button>
            
            <button>7</button>
            <button>8</button>
            <button>9</button>
            <button class="operator">+</button>
            
            <button>4</button>
            <button>5</button>
            <button>6</button>
            <button>.</button>
            
            <button>1</button>
            <button>2</button>
            <button>3</button>
            <button class="equals">=</button>
            
            <button style="grid-column: span 2">0</button>
        </div>
    </div>
    <script>{js}</script>
</body>
</html>"""

def main():
    print("🌱 GROWING AESTHETIC CALCULATOR...")
    
    # 1. Get Profile from Resonance Grower
    grower = ResonanceGrower()
    # Intent = "Beautiful" -> triggers Love preparation
    # Context = "Modern Web" -> triggers Wisdom preparation
    target_profile = grower.determine_target_profile(
        intent="Create an aesthetically pleasing, beautiful calculator",
        context="Modern web interface, high user experience"
    )
    
    print("\n--- RESONANCE TARGET ---")
    print(f"L: {target_profile['L']:.3f} (Aesthetics)")
    print(f"J: {target_profile['J']:.3f} (Validation)")
    print(f"P: {target_profile['P']:.3f} (Function)")
    print(f"W: {target_profile['W']:.3f} (Structure)")
    
    # 2. Materialize
    materializer = AestheticMaterializer(target_profile)
    html_code = materializer.generate_html()
    
    # 3. Save
    output_path = os.path.join("examples", "auto_generated", "beautiful_calculator.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_code)
        
    print(f"\n✅ Grown successfully: {output_path}")
    
    # 4. Verify with Analyzer
    print("\n--- VERIFICATION ---")
    analyzer = SemanticResonanceAnalyzer()
    report = analyzer.analyze_code(html_code, "beautiful_calculator.html")
    
    print(f"Achieved Harmony: {report['harmony_final']:.3f}")
    if report['harmony_final'] > 0.6:
        print("Status: HARMONIOUS & BEAUTIFUL")
    else:
        print("Status: DISSONANT")

if __name__ == "__main__":
    main()
