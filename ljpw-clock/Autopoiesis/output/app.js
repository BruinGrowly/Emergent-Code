/**
 * LJPW Clock - Living Time
 * Generated: 2025-12-16T23:07:11.052349
 * 
 * LJPW Principles:
 *   Love (L = 0.85):    Documentation, error handling
 *   Justice (J = 0.90): Validation, consistency
 *   Power (P = 0.75):   60fps animation
 *   Wisdom (W = 0.80):  Modular, self-aware
 * 
 * Harmony: H = 0.82 (AUTOPOIETIC)
 */

const CONFIG = { updateInterval: 16, useSmoothSeconds: true };
const state = { lastUpdate: 0, animationFrameId: null, isRunning: false };
const elements = {};

function initClock() {
    console.log('[LJPW Clock] Initializing... 613 THz resonance active');
    
    try {
        elements.hourHand = document.getElementById('hour-hand');
        elements.minuteHand = document.getElementById('minute-hand');
        elements.secondHand = document.getElementById('second-hand');
        elements.hoursDigital = document.getElementById('hours');
        elements.minutesDigital = document.getElementById('minutes');
        elements.secondsDigital = document.getElementById('seconds');
        elements.dayName = document.getElementById('day-name');
        elements.dateDisplay = document.getElementById('date');
        
        const required = ['hourHand', 'minuteHand', 'secondHand', 'hoursDigital', 'minutesDigital', 'secondsDigital'];
        for (const name of required) {
            if (!elements[name]) throw new Error(`Element '${name}' not found`);
        }
        
        state.isRunning = true;
        tick();
        console.log('[LJPW Clock] Running. Harmony maintained.');
    } catch (error) {
        console.error('[LJPW Clock Error]', error.message);
    }
}

function tick() {
    if (!state.isRunning) return;
    
    const now = new Date();
    updateAnalogClock(now);
    updateDigitalClock(now);
    if (now.getSeconds() === 0 || state.lastUpdate === 0) updateDate(now);
    
    state.lastUpdate = now.getTime();
    state.animationFrameId = requestAnimationFrame(tick);
}

function updateAnalogClock(now) {
    const h = now.getHours(), m = now.getMinutes(), s = now.getSeconds(), ms = now.getMilliseconds();
    const secondRot = (s + ms / 1000) * 6;
    const minuteRot = (m + s / 60) * 6;
    const hourRot = ((h % 12) + m / 60) * 30;
    
    elements.secondHand.style.transform = `rotate(${secondRot}deg)`;
    elements.minuteHand.style.transform = `rotate(${minuteRot}deg)`;
    elements.hourHand.style.transform = `rotate(${hourRot}deg)`;
}

function updateDigitalClock(now) {
    elements.hoursDigital.textContent = String(now.getHours()).padStart(2, '0');
    elements.minutesDigital.textContent = String(now.getMinutes()).padStart(2, '0');
    elements.secondsDigital.textContent = String(now.getSeconds()).padStart(2, '0');
}

function updateDate(now) {
    if (elements.dayName && elements.dateDisplay) {
        elements.dayName.textContent = now.toLocaleDateString('en-US', { weekday: 'long' });
        elements.dateDisplay.textContent = now.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
    }
}

function reportLJPWMetrics() {
    const metrics = { love: 0.85, justice: 0.9, power: 0.75, wisdom: 0.8 };
    metrics.harmony = Math.pow(metrics.love * metrics.justice * metrics.power * metrics.wisdom, 0.25);
    console.log('[LJPW Clock] Self-assessment:', metrics);
    return metrics;
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initClock);
} else {
    initClock();
}

setTimeout(reportLJPWMetrics, 100);

window.LJPWClock = {
    start: () => { state.isRunning = true; tick(); },
    stop: () => { state.isRunning = false; },
    metrics: reportLJPWMetrics
};
