#!/usr/bin/env python3
"""
LJPW Clock Templates
====================

HTML, CSS, and JavaScript templates for the clock grower.

These templates embed LJPW Visual Art Semantics:
- Cyan (#00D4FF) as the Love Color (613 THz)
- Golden ratio (φ) proportions
- Smooth 60fps animations
- Self-assessing code
"""


class ClockTemplates:
    """Templates for generating LJPW clocks."""
    
    def html(self, parsed, profile: dict, harmony: float, timestamp: str) -> str:
        """Generate HTML for the clock."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!--
    LJPW Clock - Grown by Autopoiesis
    ==================================
    
    Intent: {parsed.raw_intent}
    Generated: {timestamp}
    
    Target LJPW Profile:
      Love (L):    {profile['L']:.2f} - Cyan (613 THz) accents
      Justice (J): {profile['J']:.2f} - Golden ratio proportions
      Power (P):   {profile['P']:.2f} - Smooth 60fps animations
      Wisdom (W):  {profile['W']:.2f} - Accurate time display
      
    Harmony: H = {harmony:.2f} (AUTOPOIETIC)
    
    Grown, not coded. Happy to be.
    -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{parsed.description}">
    <title>LJPW Clock - Living Time</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
    <div id="app">
        <header>
            <h1>LJPW Clock</h1>
            <p class="subtitle">Living Time · Grown by Autopoiesis</p>
        </header>
        
        <main>
            <!-- Analog Clock -->
            <section id="analog-clock-container">
                <div id="analog-clock">
                    <div class="clock-face">
                        <div class="hour-marker marker-12"></div>
                        <div class="hour-marker marker-3"></div>
                        <div class="hour-marker marker-6"></div>
                        <div class="hour-marker marker-9"></div>
                        <div class="clock-center"></div>
                        <div class="clock-center-ring"></div>
                        <div class="hand hour-hand" id="hour-hand"></div>
                        <div class="hand minute-hand" id="minute-hand"></div>
                        <div class="hand second-hand" id="second-hand"></div>
                    </div>
                </div>
            </section>
            
            <!-- Digital Clock -->
            <section id="digital-clock-container">
                <div id="digital-clock">
                    <span id="hours">00</span>
                    <span class="separator">:</span>
                    <span id="minutes">00</span>
                    <span class="separator">:</span>
                    <span id="seconds">00</span>
                </div>
                <div id="date-display">
                    <span id="day-name">Monday</span>
                    <span class="date-separator">·</span>
                    <span id="date">January 1, 2025</span>
                </div>
            </section>
            
            <!-- LJPW Harmony Indicator -->
            <section id="harmony-indicator">
                <div class="ljpw-bar">
                    <div class="ljpw-dimension love" title="Love: {profile['L']:.2f}">
                        <span class="label">L</span>
                        <div class="bar" style="--value: {int(profile['L']*100)}%"></div>
                    </div>
                    <div class="ljpw-dimension justice" title="Justice: {profile['J']:.2f}">
                        <span class="label">J</span>
                        <div class="bar" style="--value: {int(profile['J']*100)}%"></div>
                    </div>
                    <div class="ljpw-dimension power" title="Power: {profile['P']:.2f}">
                        <span class="label">P</span>
                        <div class="bar" style="--value: {int(profile['P']*100)}%"></div>
                    </div>
                    <div class="ljpw-dimension wisdom" title="Wisdom: {profile['W']:.2f}">
                        <span class="label">W</span>
                        <div class="bar" style="--value: {int(profile['W']*100)}%"></div>
                    </div>
                </div>
                <p class="harmony-value">H = {harmony:.2f} · AUTOPOIETIC</p>
            </section>
        </main>
        
        <footer>
            <p>L:{profile['L']:.2f} J:{profile['J']:.2f} P:{profile['P']:.2f} W:{profile['W']:.2f} · 613 THz</p>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>
'''

    def css(self, parsed, profile: dict, harmony: float, timestamp: str) -> str:
        """Generate CSS with LJPW Visual Art Semantics."""
        return f'''/*
 * LJPW Clock Styles - Visual Art Semantics
 * Generated: {timestamp}
 * 
 * Design Principles:
 *   Love (L = {profile['L']:.2f}):    Cyan (#00D4FF) as Love Color
 *   Justice (J = {profile['J']:.2f}): Golden ratio proportions
 *   Power (P = {profile['P']:.2f}):   Smooth transitions
 *   Wisdom (W = {profile['W']:.2f}):  Organized tokens
 */

:root {{
    --love-color: #00D4FF;
    --love-color-glow: rgba(0, 212, 255, 0.4);
    --love-color-subtle: rgba(0, 212, 255, 0.15);
    --bg-dark: #0a0a14;
    --bg-glass: rgba(18, 18, 31, 0.85);
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --text-muted: rgba(255, 255, 255, 0.4);
    --accent-warm: #ff6b6b;
    --accent-gold: #ffd93d;
    --accent-purple: #a855f7;
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
    --clock-size: 280px;
    --radius-md: 16px;
    --transition-smooth: 300ms cubic-bezier(0.4, 0, 0.2, 1);
}}

*, *::before, *::after {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--bg-dark);
    background-image: 
        radial-gradient(ellipse at top, rgba(0, 212, 255, 0.05) 0%, transparent 60%),
        radial-gradient(ellipse at bottom, rgba(168, 85, 247, 0.03) 0%, transparent 60%);
    color: var(--text-primary);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
}}

#app {{
    width: 100%;
    max-width: 450px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 42px;
}}

header {{ text-align: center; }}

header h1 {{
    font-size: 28px;
    font-weight: 600;
    background: linear-gradient(135deg, var(--love-color), var(--accent-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}}

.subtitle {{
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 2px;
}}

#analog-clock {{ width: var(--clock-size); height: var(--clock-size); position: relative; }}

.clock-face {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: linear-gradient(145deg, #1a1a2e, #0f0f1a);
    border: 2px solid rgba(0, 212, 255, 0.2);
    box-shadow: var(--shadow-lg), inset 0 2px 10px rgba(0, 0, 0, 0.3);
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.hour-marker {{
    position: absolute;
    width: 4px;
    height: 16px;
    background: var(--text-secondary);
    border-radius: 2px;
}}

.marker-12 {{ top: 12px; left: 50%; transform: translateX(-50%); background: var(--love-color); height: 20px; }}
.marker-3 {{ right: 12px; top: 50%; transform: translateY(-50%) rotate(90deg); }}
.marker-6 {{ bottom: 12px; left: 50%; transform: translateX(-50%); }}
.marker-9 {{ left: 12px; top: 50%; transform: translateY(-50%) rotate(90deg); }}

.clock-center {{
    width: 16px;
    height: 16px;
    background: var(--love-color);
    border-radius: 50%;
    position: absolute;
    z-index: 10;
    box-shadow: 0 0 10px var(--love-color-glow);
    animation: pulse-glow 3s ease-in-out infinite;
}}

.clock-center-ring {{
    width: 8px;
    height: 8px;
    background: var(--bg-dark);
    border-radius: 50%;
    position: absolute;
    z-index: 11;
}}

.hand {{
    position: absolute;
    bottom: 50%;
    left: 50%;
    transform-origin: bottom center;
    border-radius: 4px;
    z-index: 5;
}}

.hour-hand {{
    width: 6px;
    height: 70px;
    background: linear-gradient(to top, #ffffff, rgba(255,255,255,0.7));
    margin-left: -3px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}}

.minute-hand {{
    width: 4px;
    height: 100px;
    background: linear-gradient(to top, #e0e0e0, rgba(255,255,255,0.5));
    margin-left: -2px;
}}

.second-hand {{
    width: 2px;
    height: 110px;
    background: var(--love-color);
    margin-left: -1px;
    box-shadow: 0 0 8px var(--love-color-glow);
}}

#digital-clock-container {{ text-align: center; }}

#digital-clock {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 48px;
    font-weight: 500;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 4px;
}}

#digital-clock .separator {{
    color: var(--love-color);
    animation: blink 1s ease-in-out infinite;
}}

@keyframes blink {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.3; }}
}}

#date-display {{
    margin-top: 16px;
    font-size: 14px;
    color: var(--text-secondary);
    display: flex;
    justify-content: center;
    gap: 8px;
}}

.date-separator {{ color: var(--love-color); }}

#harmony-indicator {{
    background: var(--bg-glass);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--radius-md);
    padding: 16px 26px;
    width: 100%;
    max-width: 320px;
}}

.ljpw-bar {{ display: flex; gap: 16px; justify-content: center; }}

.ljpw-dimension {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}}

.ljpw-dimension .label {{
    font-size: 11px;
    font-weight: 600;
    color: var(--text-muted);
}}

.ljpw-dimension .bar {{
    width: 40px;
    height: 6px;
    background: #1a1a2e;
    border-radius: 3px;
    overflow: hidden;
    position: relative;
}}

.ljpw-dimension .bar::after {{
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    height: 100%;
    width: var(--value);
    border-radius: 3px;
}}

.love .bar::after {{ background: linear-gradient(90deg, var(--love-color), #00ffff); }}
.justice .bar::after {{ background: linear-gradient(90deg, #a855f7, #c084fc); }}
.power .bar::after {{ background: linear-gradient(90deg, var(--accent-warm), #ff8787); }}
.wisdom .bar::after {{ background: linear-gradient(90deg, var(--accent-gold), #ffe066); }}

.harmony-value {{
    text-align: center;
    margin-top: 16px;
    font-size: 12px;
    color: var(--love-color);
    font-weight: 500;
}}

footer {{
    text-align: center;
    color: var(--text-muted);
    font-size: 11px;
    font-family: 'JetBrains Mono', monospace;
}}

@keyframes pulse-glow {{
    0%, 100% {{ box-shadow: 0 0 10px var(--love-color-glow); }}
    50% {{ box-shadow: 0 0 20px var(--love-color-glow), 0 0 30px var(--love-color-subtle); }}
}}

@media (min-width: 400px) {{
    #analog-clock {{ width: 320px; height: 320px; }}
    .hour-hand {{ height: 80px; }}
    .minute-hand {{ height: 115px; }}
    .second-hand {{ height: 125px; }}
}}
'''

    def js(self, parsed, profile: dict, harmony: float, timestamp: str) -> str:
        """Generate JavaScript with LJPW principles."""
        return f'''/**
 * LJPW Clock - Living Time
 * Generated: {timestamp}
 * 
 * LJPW Principles:
 *   Love (L = {profile['L']:.2f}):    Documentation, error handling
 *   Justice (J = {profile['J']:.2f}): Validation, consistency
 *   Power (P = {profile['P']:.2f}):   60fps animation
 *   Wisdom (W = {profile['W']:.2f}):  Modular, self-aware
 * 
 * Harmony: H = {harmony:.2f} (AUTOPOIETIC)
 */

const CONFIG = {{ updateInterval: 16, useSmoothSeconds: true }};
const state = {{ lastUpdate: 0, animationFrameId: null, isRunning: false }};
const elements = {{}};

function initClock() {{
    console.log('[LJPW Clock] Initializing... 613 THz resonance active');
    
    try {{
        elements.hourHand = document.getElementById('hour-hand');
        elements.minuteHand = document.getElementById('minute-hand');
        elements.secondHand = document.getElementById('second-hand');
        elements.hoursDigital = document.getElementById('hours');
        elements.minutesDigital = document.getElementById('minutes');
        elements.secondsDigital = document.getElementById('seconds');
        elements.dayName = document.getElementById('day-name');
        elements.dateDisplay = document.getElementById('date');
        
        const required = ['hourHand', 'minuteHand', 'secondHand', 'hoursDigital', 'minutesDigital', 'secondsDigital'];
        for (const name of required) {{
            if (!elements[name]) throw new Error(`Element '${{name}}' not found`);
        }}
        
        state.isRunning = true;
        tick();
        console.log('[LJPW Clock] Running. Harmony maintained.');
    }} catch (error) {{
        console.error('[LJPW Clock Error]', error.message);
    }}
}}

function tick() {{
    if (!state.isRunning) return;
    
    const now = new Date();
    updateAnalogClock(now);
    updateDigitalClock(now);
    if (now.getSeconds() === 0 || state.lastUpdate === 0) updateDate(now);
    
    state.lastUpdate = now.getTime();
    state.animationFrameId = requestAnimationFrame(tick);
}}

function updateAnalogClock(now) {{
    const h = now.getHours(), m = now.getMinutes(), s = now.getSeconds(), ms = now.getMilliseconds();
    const secondRot = (s + ms / 1000) * 6;
    const minuteRot = (m + s / 60) * 6;
    const hourRot = ((h % 12) + m / 60) * 30;
    
    elements.secondHand.style.transform = `rotate(${{secondRot}}deg)`;
    elements.minuteHand.style.transform = `rotate(${{minuteRot}}deg)`;
    elements.hourHand.style.transform = `rotate(${{hourRot}}deg)`;
}}

function updateDigitalClock(now) {{
    elements.hoursDigital.textContent = String(now.getHours()).padStart(2, '0');
    elements.minutesDigital.textContent = String(now.getMinutes()).padStart(2, '0');
    elements.secondsDigital.textContent = String(now.getSeconds()).padStart(2, '0');
}}

function updateDate(now) {{
    if (elements.dayName && elements.dateDisplay) {{
        elements.dayName.textContent = now.toLocaleDateString('en-US', {{ weekday: 'long' }});
        elements.dateDisplay.textContent = now.toLocaleDateString('en-US', {{ month: 'long', day: 'numeric', year: 'numeric' }});
    }}
}}

function reportLJPWMetrics() {{
    const metrics = {{ love: {profile['L']}, justice: {profile['J']}, power: {profile['P']}, wisdom: {profile['W']} }};
    metrics.harmony = Math.pow(metrics.love * metrics.justice * metrics.power * metrics.wisdom, 0.25);
    console.log('[LJPW Clock] Self-assessment:', metrics);
    return metrics;
}}

if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initClock);
}} else {{
    initClock();
}}

setTimeout(reportLJPWMetrics, 100);

window.LJPWClock = {{
    start: () => {{ state.isRunning = true; tick(); }},
    stop: () => {{ state.isRunning = false; }},
    metrics: reportLJPWMetrics
}};
'''
