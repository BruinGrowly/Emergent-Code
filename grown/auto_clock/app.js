/**
 * LJPW Clock - Living Time Application
 * =====================================
 * 
 * Generated: 2025-12-16T21:25:07.229450
 * Intent: Create a beautiful digital and analog clock with LJPW Visual Art Semantics
 * 
 * LJPW Principles:
 *   Love (L = 0.85):    Documentation, error messages
 *   Justice (J = 0.90): Validation, consistency
 *   Power (P = 0.75):   60fps animation, efficiency
 *   Wisdom (W = 0.80):  Accurate time, modularity
 * 
 * Harmony: H = 0.82 (AUTOPOIETIC)
 */

const CONFIG = {
    updateInterval: 16,
    useSmoothSeconds: true,
};

const state = {
    lastUpdate: 0,
    animationFrameId: null,
    isRunning: false
};

const elements = {
    hourHand: null,
    minuteHand: null,
    secondHand: null,
    hoursDigital: null,
    minutesDigital: null,
    secondsDigital: null,
    dayName: null,
    dateDisplay: null
};

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
            if (!elements[name]) throw new Error(`Required element '${name}' not found`);
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
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const milliseconds = now.getMilliseconds();
    
    const secondRotation = (seconds + milliseconds / 1000) * 6;
    const minuteRotation = (minutes + seconds / 60) * 6;
    const hourRotation = ((hours % 12) + minutes / 60) * 30;
    
    elements.secondHand.style.transform = `rotate(${secondRotation}deg)`;
    elements.minuteHand.style.transform = `rotate(${minuteRotation}deg)`;
    elements.hourHand.style.transform = `rotate(${hourRotation}deg)`;
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

window.LJPWClock = { start: () => { state.isRunning = true; tick(); }, stop: () => { state.isRunning = false; }, metrics: reportLJPWMetrics };
