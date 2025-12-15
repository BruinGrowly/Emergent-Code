"""
Experiment: Grow a Beautiful World Clock (v6.0)
Target: High Love (Beauty) + High Justice (Accuracy) + PNG Focus
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_grower import ResonanceGrower
from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

class ClockMaterializer:
    """
    Translates Semantic Physics into a World Clock.
    """
    def __init__(self, profile):
        # Auto-healed: Input validation for __init__
        if profile is not None and not isinstance(profile, (str, bytes)):
            raise TypeError(f'profile must be a valid path')
        self.L = profile['L']
        self.J = profile['J']
        self.P = profile['P']
        self.W = profile['W']

    def materialize_css(self) -> str:
        """
        Love dictates Aesthetics.
        """
        radius = int(self.L * 25)
        glass_opacity = 0.15 if self.L > 0.8 else 0.3
        
        css = ""
        css += ":root {\n"
        css += "    --bg-gradient: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);\n"
        css += "    --glass: rgba(255, 255, 255, " + str(glass_opacity) + ");\n"
        css += "    --border: 1px solid rgba(255, 255, 255, 0.2);\n"
        css += "    --text-main: #f8fafc;\n"
        css += "    --text-dim: #94a3b8;\n"
        css += "    --accent: #f43f5e;\n"
        css += "}\n\n"

        css += "body {\n"
        css += "    margin: 0;\n"
        css += "    min-height: 100vh;\n"
        css += "    display: flex;\n"
        css += "    flex-direction: column;\n"
        css += "    align-items: center;\n"
        css += "    justify-content: center;\n"
        css += "    background: var(--bg-gradient);\n"
        css += "    font-family: 'Inter', system-ui, sans-serif;\n"
        css += "    color: var(--text-main);\n"
        css += "    overflow-x: hidden;\n"
        css += "}\n\n"

        css += "h1 {\n"
        css += "    font-weight: 300;\n"
        css += "    letter-spacing: 2px;\n"
        css += "    margin-bottom: 3rem;\n"
        css += "    text-transform: uppercase;\n"
        css += "    font-size: 1.5rem;\n"
        css += "    opacity: 0.8;\n"
        css += "}\n\n"

        css += ".clock-grid {\n"
        css += "    display: grid;\n"
        css += "    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));\n"
        css += "    gap: 2rem;\n"
        css += "    width: 90%;\n"
        css += "    max-width: 1200px;\n"
        css += "}\n\n"

        css += ".city-card {\n"
        css += "    background: var(--glass);\n"
        css += "    backdrop-filter: blur(" + str(int(self.L * 20)) + "px);\n"
        css += "    border: var(--border);\n"
        css += "    border-radius: " + str(radius) + "px;\n"
        css += "    padding: 2rem;\n"
        css += "    display: flex;\n"
        css += "    flex-direction: column;\n"
        css += "    justify-content: space-between;\n"
        css += "    position: relative;\n"
        css += "    overflow: hidden;\n"
        css += "    transition: transform 0.3s ease;\n"
        css += "}\n\n"

        css += ".city-card:hover {\n"
        css += "    transform: translateY(-5px);\n"
        css += "    background: rgba(255,255,255, " + str(glass_opacity + 0.05) + ");\n"
        css += "}\n\n"

        css += ".city-card.primary {\n"
        css += "    border-color: rgba(244, 63, 94, 0.5);\n"
        css += "    box-shadow: 0 0 30px rgba(244, 63, 94, 0.2);\n"
        css += "}\n\n"

        css += ".city-name {\n"
        css += "    font-size: 1.1rem;\n"
        css += "    color: var(--text-dim);\n"
        css += "    font-weight: 500;\n"
        css += "    letter-spacing: 1px;\n"
        css += "    margin-bottom: 0.5rem;\n"
        css += "}\n\n"

        css += ".time-display {\n"
        css += "    font-size: 3.5rem;\n"
        css += "    font-weight: 200;\n"
        css += "    font-variant-numeric: tabular-nums;\n"
        css += "    letter-spacing: -2px;\n"
        css += "}\n\n"

        css += ".date-display {\n"
        css += "    font-size: 0.9rem;\n"
        css += "    color: var(--text-dim);\n"
        css += "    margin-top: 0.5rem;\n"
        css += "}\n\n"

        css += ".analog-ring {\n"
        css += "    position: absolute;\n"
        css += "    top: -20px;\n"
        css += "    right: -20px;\n"
        css += "    width: 100px;\n"
        css += "    height: 100px;\n"
        css += "    border: 2px solid rgba(255,255,255,0.1);\n"
        css += "    border-radius: 50%;\n"
        css += "    pointer-events: none;\n"
        css += "}\n"
        return css

    def materialize_js(self) -> str:
        """
        Justice dictates Accuracy. Power dictates Efficiency.
        """
        
        update_mechanism = ""
        if self.P > 0.6:
            update_mechanism = "    function update() {\n"
            update_mechanism += "        updateClocks();\n"
            update_mechanism += "        requestAnimationFrame(update);\n"
            update_mechanism += "    }\n"
            update_mechanism += "    requestAnimationFrame(update);\n"
        else:
            update_mechanism = "    setInterval(updateClocks, 1000);\n"

        js = ""
        js += "const cities = [\n"
        js += "    { name: 'PORT MORESBY', tz: 'Pacific/Port_Moresby', primary: true },\n"
        js += "    { name: 'NEW YORK', tz: 'America/New_York' },\n"
        js += "    { name: 'LONDON', tz: 'Europe/London' },\n"
        js += "    { name: 'TOKYO', tz: 'Asia/Tokyo' },\n"
        js += "    { name: 'SYDNEY', tz: 'Australia/Sydney' }\n"
        js += " ];\n\n"

        js += "const container = document.querySelector('.clock-grid');\n\n"

        js += "cities.forEach(city => {\n"
        js += "    const card = document.createElement('div');\n"
        # Using string concat to avoid Python syntax confusion
        js += "    const primaryClass = city.primary ? 'primary' : '';\n"
        js += "    card.className = 'city-card ' + primaryClass;\n"
        js += "    card.innerHTML = `\n"
        js += "        <div class=\"analog-ring\"></div>\n"
        js += "        <div>\n"
        js += "            <div class=\"city-name\">${city.name}</div>\n"
        js += "            <div class=\"time-display\" id=\"time-${city.name}\">--:--</div>\n"
        js += "            <div class=\"date-display\" id=\"date-${city.name}\">Loading...</div>\n"
        js += "        </div>\n"
        js += "    `;\n"
        js += "    container.appendChild(card);\n"
        js += "});\n\n"

        js += "function updateClocks() {\n"
        js += "    const now = new Date();\n"
        js += "    cities.forEach(city => {\n"
        js += "        const options = { \n"
        js += "            timeZone: city.tz, \n"
        js += "            hour: '2-digit', \n"
        js += "            minute: '2-digit', \n"
        js += "            second: '2-digit',\n"
        js += "            hour12: false \n"
        js += "        };\n"
        js += "        const dateOptions = {\n"
        js += "            timeZone: city.tz,\n"
        js += "            weekday: 'short',\n"
        js += "            month: 'short',\n"
        js += "            day: 'numeric'\n"
        js += "        };\n"
        js += "        const timeStr = new Intl.DateTimeFormat('en-US', options).format(now);\n"
        js += "        const dateStr = new Intl.DateTimeFormat('en-US', dateOptions).format(now);\n"
        js += "        document.getElementById(`time-${city.name}`).textContent = timeStr;\n"
        js += "        document.getElementById(`date-${city.name}`).textContent = dateStr;\n"
        js += "    });\n"
        js += "}\n\n"
        js += update_mechanism
        
        return js

    def generate_html(self) -> str:
        css = self.materialize_css()
        js = self.materialize_js()
        
        html = "<!DOCTYPE html>\n"
        html += "<html>\n"
        html += "<head>\n"
        html += "    <title>Emergent World Clock</title>\n"
        html += "    <style>" + css + "    </style>\n"
        html += "</head>\n"
        html += "<body>\n"
        html += "    <h1>Global Resonance Time</h1>\n"
        html += "    <div class=\"clock-grid\"></div>\n"
        html += "    <script>" + js + "    </script>\n"
        html += "</body>\n"
        html += "</html>"
        return html

def main():
    print("🌱 GROWING WORLD CLOCK (Target: PNG)...")
    
    grower = ResonanceGrower()
    profile = grower.determine_target_profile(
        intent="Beautiful World Clock with Papua New Guinea focus",
        context="Global connectivity, high accuracy"
    )
    
    print("\n--- RESONANCE PROFILE ---")
    print(f"L: {profile['L']:.3f} (Beauty)")
    print(f"J: {profile['J']:.3f} (Accuracy)")
    print(f"P: {profile['P']:.3f} (Performance)")
    
    materializer = ClockMaterializer(profile)
    html_code = materializer.generate_html()
    
    output_path = os.path.join("examples", "auto_generated", "beautiful_world_clock.html")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_code)
        
    print(f"\n✅ Grown successfully: {output_path}")

    analyzer = SemanticResonanceAnalyzer()
    report = analyzer.analyze_code(html_code, "beautiful_world_clock.html")
    print(f"Harmony: {report['harmony_final']:.3f}")

if __name__ == "__main__":
    main()
