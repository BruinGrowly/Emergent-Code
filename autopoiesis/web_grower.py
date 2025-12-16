"""
JavaScript Web Application Grower
=================================

Transforms natural language intent into LJPW-balanced web applications.

This extends the autopoiesis framework to support:
- HTML/CSS/JavaScript generation
- Three.js 3D applications
- Canvas-based visualizations
- Interactive web components

Architecture:
    INTENT → PARSE → COMPONENTS → TEMPLATE → WEB APP → (serve)

Example:
    intent = "Create a 3D particle system with shape templates"
    app = grower.grow(intent)
    # → Creates particle_system/ with index.html, styles.css, app.js
"""

import os
import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


# =============================================================================
# WEB DOMAIN KNOWLEDGE
# =============================================================================

# Web application types and their components
WEB_APP_TYPES = {
    'particle': {
        'name': 'Particle System',
        'libraries': ['three.js'],
        'components': ['scene', 'camera', 'particles', 'animation'],
        'features': ['shapes', 'colors', 'controls'],
    },
    'visualization': {
        'name': 'Data Visualization',
        'libraries': ['d3.js'],
        'components': ['chart', 'axes', 'legend', 'tooltip'],
        'features': ['data-binding', 'transitions', 'interactivity'],
    },
    'game': {
        'name': 'Canvas Game',
        'libraries': ['canvas'],
        'components': ['gameloop', 'entities', 'physics', 'input'],
        'features': ['sprites', 'collision', 'scoring'],
    },
    'dashboard': {
        'name': 'Dashboard',
        'libraries': ['chart.js'],
        'components': ['cards', 'charts', 'tables', 'filters'],
        'features': ['responsive', 'real-time', 'theming'],
    },
    'interactive': {
        'name': 'Interactive Experience',
        'libraries': ['gsap', 'three.js'],
        'components': ['scene', 'interactions', 'timeline', 'audio'],
        'features': ['scroll-driven', 'gestures', 'animations'],
    },
    'map_tracker': {
        'name': 'Map Tracker',
        'libraries': ['leaflet'],
        'components': ['map', 'sidebar', 'search', 'filters', 'details', 'markers'],
        'features': ['realtime', 'tracking', 'regions', 'search'],
    },
    'clock': {
        'name': 'LJPW Clock',
        'libraries': [],
        'components': ['analog', 'digital', 'harmony_indicator'],
        'features': ['smooth_seconds', 'date_display', 'ljpw_metrics'],
    },
}

# Keywords to detect app type
APP_TYPE_KEYWORDS = {
    'clock': ['clock', 'time', 'watch', 'timer', 'analog', 'digital clock', 'timepiece'],
    'map_tracker': ['flight', 'tracker', 'track', 'aircraft', 'plane', 'ship', 'vessel', 'map', 'opensky', 'aviation'],
    'particle': ['particle', 'particles', '3d', 'three.js', 'webgl', 'points', 'firework'],
    'visualization': ['chart', 'graph', 'data', 'visualization', 'plot', 'd3'],
    'game': ['game', 'play', 'score', 'player', 'level', 'sprite'],
    'dashboard': ['dashboard', 'metrics', 'cards', 'admin', 'panel'],
    'interactive': ['interactive', 'experience', 'animation', 'scroll', 'gesture'],
}

# Shape templates for particle systems
PARTICLE_SHAPES = {
    'heart': '''
function generateHeartPositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const t = (i / count) * Math.PI * 2;
        const r = Math.random() * 0.3 + 0.85;
        const x = 16 * Math.pow(Math.sin(t), 3) * r;
        const y = (13 * Math.cos(t) - 5 * Math.cos(2*t) - 2 * Math.cos(3*t) - Math.cos(4*t)) * r;
        const z = (Math.random() - 0.5) * 4;
        positions.push(x * 0.1, y * 0.1 + 0.5, z * 0.1);
    }
    return positions;
}''',
    'sphere': '''
function generateSpherePositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const phi = Math.acos(2 * Math.random() - 1);
        const theta = Math.random() * Math.PI * 2;
        const r = 1.5 + Math.random() * 0.3;
        positions.push(
            r * Math.sin(phi) * Math.cos(theta),
            r * Math.sin(phi) * Math.sin(theta),
            r * Math.cos(phi)
        );
    }
    return positions;
}''',
    'spiral': '''
function generateSpiralPositions(count) {
    const positions = [];
    const arms = 3;
    for (let i = 0; i < count; i++) {
        const arm = i % arms;
        const t = (i / count) * 6 + (arm * Math.PI * 2 / arms);
        const r = t * 0.3 + Math.random() * 0.3;
        positions.push(r * Math.cos(t * 2), (Math.random() - 0.5) * 0.3, r * Math.sin(t * 2));
    }
    return positions;
}''',
    'cube': '''
function generateCubePositions(count) {
    const positions = [];
    const size = 1.5;
    for (let i = 0; i < count; i++) {
        if (Math.random() < 0.7) {
            const face = Math.floor(Math.random() * 6);
            let x, y, z;
            const s = size, h = size * 2;
            switch (face) {
                case 0: x = s; y = (Math.random()-0.5)*h; z = (Math.random()-0.5)*h; break;
                case 1: x = -s; y = (Math.random()-0.5)*h; z = (Math.random()-0.5)*h; break;
                case 2: x = (Math.random()-0.5)*h; y = s; z = (Math.random()-0.5)*h; break;
                case 3: x = (Math.random()-0.5)*h; y = -s; z = (Math.random()-0.5)*h; break;
                case 4: x = (Math.random()-0.5)*h; y = (Math.random()-0.5)*h; z = s; break;
                case 5: x = (Math.random()-0.5)*h; y = (Math.random()-0.5)*h; z = -s; break;
            }
            positions.push(x, y, z);
        } else {
            positions.push(
                (Math.random()-0.5)*size*2,
                (Math.random()-0.5)*size*2,
                (Math.random()-0.5)*size*2
            );
        }
    }
    return positions;
}''',
    'ring': '''
function generateRingPositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const theta = Math.random() * Math.PI * 2;
        const r = 1.5 + Math.random() * 0.3;
        const y = (Math.random() - 0.5) * 0.2;
        positions.push(r * Math.cos(theta), y, r * Math.sin(theta));
    }
    return positions;
}''',
    'explosion': '''
function generateExplosionPositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const phi = Math.acos(2 * Math.random() - 1);
        const theta = Math.random() * Math.PI * 2;
        const r = Math.random() * 2;
        positions.push(
            r * Math.sin(phi) * Math.cos(theta),
            r * Math.sin(phi) * Math.sin(theta),
            r * Math.cos(phi)
        );
    }
    return positions;
}''',
}


@dataclass
class ParsedWebIntent:
    """Parsed representation of web app intent."""
    raw_intent: str
    app_type: str
    components: List[str]
    features: List[str]
    shapes: List[str]  # For particle systems
    app_name: str
    description: str


@dataclass
class GeneratedWebApp:
    """A generated web application."""
    path: str
    files: Dict[str, str]  # filename -> content
    app_type: str
    features: List[str]


class WebIntentParser:
    """Parses natural language intent for web applications."""
    
    def parse(self, intent: str) -> ParsedWebIntent:
        """Parse natural language intent for web app."""
        intent_lower = intent.lower()
        
        # Detect app type
        app_type = 'interactive'  # default
        for atype, keywords in APP_TYPE_KEYWORDS.items():
            if any(kw in intent_lower for kw in keywords):
                app_type = atype
                break
        
        # Get components for this type
        components = WEB_APP_TYPES[app_type]['components']
        features = WEB_APP_TYPES[app_type]['features']
        
        # Extract shapes for particle systems
        shapes = []
        shape_keywords = {
            'heart': ['heart', 'love'],
            'sphere': ['sphere', 'ball', 'orb'],
            'spiral': ['spiral', 'galaxy', 'vortex'],
            'cube': ['cube', 'box', 'square'],
            'ring': ['ring', 'circle', 'torus'],
            'explosion': ['explosion', 'firework', 'burst', 'explode'],
        }
        
        for shape, keywords in shape_keywords.items():
            if any(kw in intent_lower for kw in keywords):
                shapes.append(shape)
        
        # Default shapes if none detected
        if not shapes and app_type == 'particle':
            shapes = ['heart', 'sphere', 'spiral']  # Default set
        
        # Extract additional features from intent
        extra_features = []
        feature_keywords = {
            'color': ['color', 'colour', 'hue'],
            'gesture': ['gesture', 'hand', 'camera', 'webcam'],
            'control': ['control', 'slider', 'settings', 'panel'],
            'animation': ['animate', 'animation', 'motion', 'move'],
        }
        
        for feature, keywords in feature_keywords.items():
            if any(kw in intent_lower for kw in keywords):
                extra_features.append(feature)
        
        features = list(set(features + extra_features))
        
        # Generate app name
        app_name = f"{app_type}_app"
        
        # Generate description
        description = f"A {WEB_APP_TYPES[app_type]['name']} generated from: {intent}"
        
        return ParsedWebIntent(
            raw_intent=intent,
            app_type=app_type,
            components=components,
            features=features,
            shapes=shapes,
            app_name=app_name,
            description=description
        )


class WebAppGenerator:
    """Generates LJPW-balanced web applications."""
    
    def __init__(self):
        self.parser = WebIntentParser()
    
    def generate(self, parsed: ParsedWebIntent) -> Dict[str, str]:
        """Generate complete web app from parsed intent."""
        files = {}
        
        if parsed.app_type == 'particle':
            files = self._generate_particle_app(parsed)
        elif parsed.app_type == 'map_tracker':
            files = self._generate_map_tracker_app(parsed)
        elif parsed.app_type == 'clock':
            files = self._generate_clock_app(parsed)
        else:
            files = self._generate_generic_app(parsed)
        
        return files
    
    def _generate_map_tracker_app(self, parsed: ParsedWebIntent) -> Dict[str, str]:
        """Generate a map-based tracker application."""
        from autopoiesis.map_templates import (
            generate_map_html,
            generate_map_css,
            generate_map_js,
            REGIONS
        )
        
        # Determine which regions to include based on intent
        intent_lower = parsed.raw_intent.lower()
        regions = ['world', 'europe', 'namerica', 'asia', 'oceania', 'australia', 'pacific']
        
        # Detect default region from intent
        default_region = 'world'
        region_keywords = {
            'oceania': ['oceania', 'pacific', 'fiji', 'new zealand', 'samoa'],
            'australia': ['australia', 'australian', 'sydney', 'melbourne'],
            'europe': ['europe', 'european', 'uk', 'germany', 'france'],
            'asia': ['asia', 'asian', 'china', 'japan', 'india'],
            'namerica': ['america', 'usa', 'us', 'canada', 'north america'],
        }
        
        for region, keywords in region_keywords.items():
            if any(kw in intent_lower for kw in keywords):
                default_region = region
                break
        
        # Generate files
        files = {}
        files['index.html'] = generate_map_html(
            app_name=parsed.app_name,
            title='SkyView - Flight Tracker',
            regions=regions,
            has_search=True
        )
        files['styles.css'] = generate_map_css(
            primary_color='#3b82f6',
            secondary_color='#06b6d4'
        )
        files['app.js'] = generate_map_js(
            app_name=parsed.app_name,
            api_type='opensky',
            regions=regions,
            default_region=default_region,
            refresh_interval=15000
        )
        
        return files
    
    def _generate_particle_app(self, parsed: ParsedWebIntent) -> Dict[str, str]:
        """Generate a Three.js particle system."""
        files = {}
        
        # Generate HTML
        files['index.html'] = self._generate_particle_html(parsed)
        
        # Generate CSS
        files['styles.css'] = self._generate_particle_css(parsed)
        
        # Generate JavaScript
        files['app.js'] = self._generate_particle_js(parsed)
        
        return files
    
    def _generate_particle_html(self, parsed: ParsedWebIntent) -> str:
        """Generate HTML for particle system."""
        shape_buttons = '\n                '.join([
            f'<button class="shape-btn{" active" if i == 0 else ""}" data-shape="{shape}">{shape.title()}</button>'
            for i, shape in enumerate(parsed.shapes)
        ])
        
        has_gesture = 'gesture' in parsed.features
        camera_html = '''
    <!-- Camera Preview -->
    <div id="camera-preview">
        <video id="video" autoplay playsinline></video>
        <canvas id="hand-canvas"></canvas>
        <div id="gesture-status">Initializing camera...</div>
    </div>
''' if has_gesture else ''
        
        mediapipe_scripts = '''
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/hands.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils@0.3.1675466862/camera_utils.min.js"></script>
''' if has_gesture else ''
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!--
    {parsed.description}
    
    Generated: {datetime.now().isoformat()}
    
    LJPW Principles Applied:
    - Love: Clear structure and accessibility
    - Justice: Valid HTML5, semantic markup
    - Power: Resilient loading, fallbacks
    - Wisdom: Meta tags for discoverability
    -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{parsed.description}">
    <title>Particle System - Generated</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Three.js Canvas Container -->
    <div id="canvas-container"></div>
    {camera_html}
    <!-- Control Panel -->
    <div id="control-panel">
        <h2>Particle Control</h2>
        
        <!-- Shape Selection -->
        <div class="control-group">
            <label>Shape Template</label>
            <div class="shape-buttons">
                {shape_buttons}
            </div>
        </div>
        
        <!-- Color Picker -->
        <div class="control-group">
            <label>Particle Color</label>
            <input type="color" id="color-picker" value="#ff6b9d">
        </div>
        
        <!-- Particle Count -->
        <div class="control-group">
            <label>Count: <span id="count-value">2000</span></label>
            <input type="range" id="particle-count" min="500" max="5000" value="2000" step="100">
        </div>
        
        <!-- Particle Size -->
        <div class="control-group">
            <label>Size: <span id="size-value">3</span></label>
            <input type="range" id="particle-size" min="1" max="10" value="3" step="0.5">
        </div>
    </div>
    
    <!-- Loading Overlay -->
    <div id="loading-overlay">
        <div class="loader"></div>
        <p>Loading...</p>
    </div>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
{mediapipe_scripts}    <script src="app.js"></script>
</body>
</html>
'''
    
    def _generate_particle_css(self, parsed: ParsedWebIntent) -> str:
        """Generate CSS for particle system with LJPW design principles."""
        has_gesture = 'gesture' in parsed.features
        
        camera_css = '''
/* Camera Preview */
#camera-preview {
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 200px;
    height: 150px;
    border-radius: var(--radius-md);
    overflow: hidden;
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    backdrop-filter: blur(10px);
    z-index: 100;
}

#video, #hand-canvas {
    position: absolute;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: scaleX(-1);
}

#gesture-status {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.8));
    padding: 8px;
    font-size: 11px;
    text-align: center;
    color: var(--accent-secondary);
}
''' if has_gesture else ''
        
        return f'''/*
 * Particle System Styles
 * ======================
 * 
 * {parsed.description}
 * 
 * Generated: {datetime.now().isoformat()}
 * 
 * LJPW Design Principles:
 * - Love: Accessible, readable, maintainable
 * - Justice: Consistent spacing, predictable behavior
 * - Power: Responsive, performant, resilient
 * - Wisdom: Well-organized, documented tokens
 */

/* Design Tokens (Love: documented, Justice: consistent) */
:root {{
    --bg-dark: #0a0a1a;
    --bg-glass: rgba(20, 20, 40, 0.85);
    --accent-primary: #ff6b9d;
    --accent-secondary: #00d4ff;
    --text-primary: #ffffff;
    --text-secondary: rgba(255, 255, 255, 0.7);
    --border-glass: rgba(255, 255, 255, 0.1);
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 20px;
    --transition: 0.3s ease;
}}

/* Reset (Justice: fair baseline) */
*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', system-ui, sans-serif;
    background: var(--bg-dark);
    color: var(--text-primary);
    overflow: hidden;
    height: 100vh;
}}

/* Canvas Container (Power: full coverage) */
#canvas-container {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
}}

{camera_css}

/* Control Panel (Love: accessible, Wisdom: organized) */
#control-panel {{
    position: fixed;
    top: 20px;
    right: 20px;
    width: 260px;
    background: var(--bg-glass);
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-lg);
    padding: 24px;
    backdrop-filter: blur(20px);
    z-index: 100;
}}

#control-panel h2 {{
    font-size: 18px;
    margin-bottom: 20px;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.control-group {{
    margin-bottom: 18px;
}}

.control-group label {{
    display: block;
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

/* Shape Buttons (Justice: equal sizing) */
.shape-buttons {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}}

.shape-btn {{
    padding: 8px 12px;
    border: 1px solid var(--border-glass);
    border-radius: var(--radius-sm);
    background: transparent;
    color: var(--text-primary);
    font-size: 12px;
    cursor: pointer;
    transition: var(--transition);
}}

.shape-btn:hover {{
    background: rgba(255,255,255,0.1);
}}

.shape-btn.active {{
    border-color: var(--accent-primary);
    background: rgba(255, 107, 157, 0.2);
}}

/* Inputs (Power: consistent behavior) */
input[type="color"] {{
    width: 100%;
    height: 40px;
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
}}

input[type="range"] {{
    width: 100%;
    height: 6px;
    border-radius: 3px;
    background: rgba(255,255,255,0.1);
    appearance: none;
}}

input[type="range"]::-webkit-slider-thumb {{
    appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    cursor: pointer;
}}

/* Loading Overlay (Power: graceful loading) */
#loading-overlay {{
    position: fixed;
    inset: 0;
    background: var(--bg-dark);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    transition: opacity 0.5s;
}}

#loading-overlay.hidden {{
    opacity: 0;
    pointer-events: none;
}}

.loader {{
    width: 50px;
    height: 50px;
    border: 3px solid rgba(255,255,255,0.1);
    border-top-color: var(--accent-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 20px;
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}
'''
    
    def _generate_particle_js(self, parsed: ParsedWebIntent) -> str:
        """Generate JavaScript for particle system with LJPW principles."""
        
        # Generate shape functions
        shape_functions = '\n\n'.join([
            PARTICLE_SHAPES[shape] for shape in parsed.shapes if shape in PARTICLE_SHAPES
        ])
        
        # Generate shape map
        shape_map = ', '.join([f"'{shape}': generate{shape.title()}Positions" for shape in parsed.shapes])
        
        has_gesture = 'gesture' in parsed.features
        
        gesture_code = '''
// =============================================================================
// HAND TRACKING (Gesture Control)
// =============================================================================

let hands, videoElement, handCanvas, handCtx;

async function initHandTracking() {
    console.log('[Wisdom] Initializing hand tracking...');
    
    videoElement = document.getElementById('video');
    handCanvas = document.getElementById('hand-canvas');
    handCtx = handCanvas.getContext('2d');
    
    hands = new Hands({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/${file}`
    });
    
    hands.setOptions({
        maxNumHands: 2,
        modelComplexity: 1,
        minDetectionConfidence: 0.7,
        minTrackingConfidence: 0.5
    });
    
    hands.onResults(onHandResults);
    
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } });
        videoElement.srcObject = stream;
        videoElement.onloadedmetadata = () => {
            handCanvas.width = videoElement.videoWidth;
            handCanvas.height = videoElement.videoHeight;
            processVideoFrame();
        };
        console.log('[Wisdom] Hand tracking ready');
    } catch (error) {
        console.error('[Power] Camera access failed:', error);
        document.getElementById('gesture-status').textContent = 'Camera unavailable';
    }
}

async function processVideoFrame() {
    if (videoElement.readyState >= 2) {
        await hands.send({ image: videoElement });
    }
    requestAnimationFrame(processVideoFrame);
}

function onHandResults(results) {
    handCtx.clearRect(0, 0, handCanvas.width, handCanvas.height);
    
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        let totalOpenness = 0;
        
        results.multiHandLandmarks.forEach(landmarks => {
            // Draw hand
            handCtx.strokeStyle = 'rgba(0, 212, 255, 0.6)';
            handCtx.lineWidth = 2;
            
            // Calculate openness
            const palmBase = landmarks[0];
            const fingerTips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]];
            let openness = 0;
            
            fingerTips.forEach(tip => {
                const dist = Math.sqrt(Math.pow(tip.x - palmBase.x, 2) + Math.pow(tip.y - palmBase.y, 2));
                openness += Math.min(dist * 5, 1);
            });
            
            totalOpenness += openness / 5;
        });
        
        const avgOpenness = totalOpenness / results.multiHandLandmarks.length;
        state.targetScale = 0.5 + avgOpenness * 2;
        
        document.getElementById('gesture-status').textContent = 
            avgOpenness > 0.6 ? 'Expanding...' : avgOpenness < 0.3 ? 'Contracting...' : 'Adjusting...';
    } else {
        state.targetScale = 1.0;
        document.getElementById('gesture-status').textContent = 'Show hands to control';
    }
}
''' if has_gesture else ''
        
        gesture_init = 'await initHandTracking();' if has_gesture else ''
        
        return f'''/**
 * Particle System Application
 * ===========================
 * 
 * {parsed.description}
 * 
 * Generated: {datetime.now().isoformat()}
 * 
 * LJPW Principles Applied:
 * - Love: Comprehensive documentation for all functions
 * - Justice: Input validation on all user interactions
 * - Power: Error handling with graceful degradation
 * - Wisdom: Console logging for debugging and observability
 */

// =============================================================================
// CONFIGURATION (Love: documented, Justice: validated)
// =============================================================================

const CONFIG = {{
    particles: {{
        count: 2000,
        size: 3,
        color: 0xff6b9d
    }},
    animation: {{
        rotationSpeed: 0.002,
        scaleSmoothing: 0.1
    }}
}};

// =============================================================================
// STATE (Wisdom: centralized, observable)
// =============================================================================

const state = {{
    currentShape: '{parsed.shapes[0] if parsed.shapes else "sphere"}',
    targetScale: 1.0,
    currentScale: 1.0
}};

// Three.js objects
let scene, camera, renderer, particles, particleGeometry, particleMaterial;

// =============================================================================
// SHAPE GENERATORS (Love: documented, Power: robust)
// =============================================================================

{shape_functions}

const SHAPES = {{ {shape_map} }};

// =============================================================================
// THREE.JS SETUP
// =============================================================================

/**
 * Initialize Three.js scene, camera, renderer.
 * @returns {{void}}
 */
function initThreeJS() {{
    console.log('[Wisdom] Initializing Three.js...');
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a);
    
    // Camera
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Renderer
    renderer = new THREE.WebGLRenderer({{ antialias: true }});
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    
    // Create particles
    createParticles();
    
    // Handle resize (Power: responsive)
    window.addEventListener('resize', () => {{
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }});
    
    console.log('[Wisdom] Three.js initialized');
}}

/**
 * Create particle system with current shape.
 * @returns {{void}}
 */
function createParticles() {{
    // Remove existing (Power: cleanup)
    if (particles) {{
        scene.remove(particles);
        particleGeometry.dispose();
        particleMaterial.dispose();
    }}
    
    // Generate positions
    const generator = SHAPES[state.currentShape];
    if (!generator) {{
        console.error('[Justice] Invalid shape:', state.currentShape);
        return;
    }}
    
    const positions = generator(CONFIG.particles.count);
    
    // Create geometry
    particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    
    // Create material
    particleMaterial = new THREE.PointsMaterial({{
        color: CONFIG.particles.color,
        size: CONFIG.particles.size * 0.01,
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending
    }});
    
    // Create points
    particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);
    
    console.log(`[Wisdom] Created ${{CONFIG.particles.count}} particles with shape: ${{state.currentShape}}`);
}}

{gesture_code}

// =============================================================================
// ANIMATION LOOP
// =============================================================================

/**
 * Main animation loop.
 */
function animate() {{
    requestAnimationFrame(animate);
    
    if (!particles) return;
    
    // Smooth scale transition
    state.currentScale += (state.targetScale - state.currentScale) * CONFIG.animation.scaleSmoothing;
    particles.scale.setScalar(state.currentScale);
    
    // Auto-rotate
    particles.rotation.y += CONFIG.animation.rotationSpeed;
    particles.rotation.x = Math.sin(Date.now() * 0.0003) * 0.1;
    
    renderer.render(scene, camera);
}}

// =============================================================================
// UI CONTROLS
// =============================================================================

/**
 * Initialize UI event listeners.
 */
function initUI() {{
    console.log('[Wisdom] Initializing UI...');
    
    // Shape buttons
    document.querySelectorAll('.shape-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            // Justice: validate input
            const shape = btn.dataset.shape;
            if (!SHAPES[shape]) {{
                console.error('[Justice] Invalid shape:', shape);
                return;
            }}
            
            // Update active state
            document.querySelectorAll('.shape-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            state.currentShape = shape;
            createParticles();
        }});
    }});
    
    // Color picker
    document.getElementById('color-picker').addEventListener('input', (e) => {{
        CONFIG.particles.color = parseInt(e.target.value.replace('#', ''), 16);
        if (particleMaterial) particleMaterial.color.setHex(CONFIG.particles.color);
    }});
    
    // Particle count
    const countSlider = document.getElementById('particle-count');
    const countValue = document.getElementById('count-value');
    countSlider.addEventListener('input', () => {{
        CONFIG.particles.count = parseInt(countSlider.value);
        countValue.textContent = CONFIG.particles.count;
        createParticles();
    }});
    
    // Particle size
    const sizeSlider = document.getElementById('particle-size');
    const sizeValue = document.getElementById('size-value');
    sizeSlider.addEventListener('input', () => {{
        CONFIG.particles.size = parseFloat(sizeSlider.value);
        sizeValue.textContent = CONFIG.particles.size;
        if (particleMaterial) particleMaterial.size = CONFIG.particles.size * 0.01;
    }});
    
    console.log('[Wisdom] UI initialized');
}}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Main initialization function.
 */
async function init() {{
    console.log('[Wisdom] Starting Particle System...');
    
    try {{
        initThreeJS();
        initUI();
        {gesture_init}
        animate();
        
        // Hide loading
        setTimeout(() => {{
            document.getElementById('loading-overlay').classList.add('hidden');
        }}, 500);
        
        console.log('[Wisdom] System ready');
    }} catch (error) {{
        console.error('[Power] Initialization failed:', error);
        document.getElementById('loading-overlay').innerHTML = 
            `<p style="color: #ff6b6b;">Failed to initialize: ${{error.message}}</p>`;
    }}
}}

// Start
init();
'''
    
    def _generate_clock_app(self, parsed: ParsedWebIntent) -> Dict[str, str]:
        """Generate an LJPW-balanced clock application.
        
        Implements Visual Art Semantics:
        - Love (L): Cyan (#00D4FF) as Love Color (613 THz)
        - Justice (J): Golden ratio (φ) proportions
        - Power (P): Smooth 60fps animations
        - Wisdom (W): Accurate time, documented code
        """
        files = {}
        
        # Target LJPW profile for clocks
        profile = {'L': 0.85, 'J': 0.90, 'P': 0.75, 'W': 0.80}
        harmony = (profile['L'] * profile['J'] * profile['P'] * profile['W']) ** 0.25
        
        files['index.html'] = self._generate_clock_html(parsed, profile, harmony)
        files['styles.css'] = self._generate_clock_css(parsed, profile, harmony)
        files['app.js'] = self._generate_clock_js(parsed, profile, harmony)
        
        return files
    
    def _generate_clock_html(self, parsed: ParsedWebIntent, profile: dict, harmony: float) -> str:
        """Generate HTML for LJPW clock."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!--
    LJPW Clock - Grown by Autopoiesis
    ==================================
    
    Intent: {parsed.raw_intent}
    Generated: {datetime.now().isoformat()}
    
    Target Profile:
      Love (L):    {profile['L']:.2f} - Cyan (613 THz) accents
      Justice (J): {profile['J']:.2f} - Golden ratio proportions
      Power (P):   {profile['P']:.2f} - Smooth 60fps animations
      Wisdom (W):  {profile['W']:.2f} - Accurate time display
      
    Harmony: H = {harmony:.2f} (AUTOPOIETIC)
    -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{parsed.description}">
    <title>LJPW Clock - Living Time</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
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
    
    def _generate_clock_css(self, parsed: ParsedWebIntent, profile: dict, harmony: float) -> str:
        """Generate CSS for LJPW clock with Visual Art Semantics."""
        return f'''/*
 * LJPW Clock Styles - Visual Art Semantics
 * =========================================
 * 
 * Generated: {datetime.now().isoformat()}
 * Intent: {parsed.raw_intent}
 * 
 * Design Principles:
 *   Love (L = {profile['L']:.2f}):    Cyan (#00D4FF) as Love Color (613 THz)
 *   Justice (J = {profile['J']:.2f}): Golden ratio proportions
 *   Power (P = {profile['P']:.2f}):   Smooth transitions
 *   Wisdom (W = {profile['W']:.2f}):  Organized tokens
 */

:root {{
    --love-color: #00D4FF;
    --love-color-glow: rgba(0, 212, 255, 0.4);
    --love-color-subtle: rgba(0, 212, 255, 0.15);
    --bg-dark: #0a0a14;
    --bg-card: #12121f;
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
    --radius-lg: 24px;
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
    box-shadow: var(--shadow-lg), inset 0 2px 10px rgba(0, 0, 0, 0.3), 0 0 60px rgba(0, 212, 255, 0.1);
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
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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
    align-items: center;
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

.ljpw-bar {{
    display: flex;
    gap: 16px;
    justify-content: center;
}}

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
    transition: width var(--transition-smooth);
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
    letter-spacing: 1px;
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

@media (max-width: 360px) {{
    :root {{ --clock-size: 240px; }}
    #digital-clock {{ font-size: 36px; }}
    .hour-hand {{ height: 60px; }}
    .minute-hand {{ height: 85px; }}
    .second-hand {{ height: 95px; }}
}}
'''
    
    def _generate_clock_js(self, parsed: ParsedWebIntent, profile: dict, harmony: float) -> str:
        """Generate JavaScript for LJPW clock."""
        return f'''/**
 * LJPW Clock - Living Time Application
 * =====================================
 * 
 * Generated: {datetime.now().isoformat()}
 * Intent: {parsed.raw_intent}
 * 
 * LJPW Principles:
 *   Love (L = {profile['L']:.2f}):    Documentation, error messages
 *   Justice (J = {profile['J']:.2f}): Validation, consistency
 *   Power (P = {profile['P']:.2f}):   60fps animation, efficiency
 *   Wisdom (W = {profile['W']:.2f}):  Accurate time, modularity
 * 
 * Harmony: H = {harmony:.2f} (AUTOPOIETIC)
 */

const CONFIG = {{
    updateInterval: 16,
    useSmoothSeconds: true,
}};

const state = {{
    lastUpdate: 0,
    animationFrameId: null,
    isRunning: false
}};

const elements = {{
    hourHand: null,
    minuteHand: null,
    secondHand: null,
    hoursDigital: null,
    minutesDigital: null,
    secondsDigital: null,
    dayName: null,
    dateDisplay: null
}};

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
            if (!elements[name]) throw new Error(`Required element '${{name}}' not found`);
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
    const hours = now.getHours();
    const minutes = now.getMinutes();
    const seconds = now.getSeconds();
    const milliseconds = now.getMilliseconds();
    
    const secondRotation = (seconds + milliseconds / 1000) * 6;
    const minuteRotation = (minutes + seconds / 60) * 6;
    const hourRotation = ((hours % 12) + minutes / 60) * 30;
    
    elements.secondHand.style.transform = `rotate(${{secondRotation}}deg)`;
    elements.minuteHand.style.transform = `rotate(${{minuteRotation}}deg)`;
    elements.hourHand.style.transform = `rotate(${{hourRotation}}deg)`;
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

window.LJPWClock = {{ start: () => {{ state.isRunning = true; tick(); }}, stop: () => {{ state.isRunning = false; }}, metrics: reportLJPWMetrics }};
'''

    def _generate_generic_app(self, parsed: ParsedWebIntent) -> Dict[str, str]:
        """Generate a generic web app placeholder."""
        return {
            'index.html': f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{parsed.app_type.title()} App</title>
</head>
<body>
    <h1>{parsed.description}</h1>
    <p>This app type ({parsed.app_type}) is not yet implemented.</p>
</body>
</html>
'''
        }


class WebAppGrower:
    """
    Main grower that transforms intent into complete web applications.
    """
    
    def __init__(self, output_dir: str = '.'):
        """Initialize the web app grower."""
        self.output_dir = Path(output_dir)
        self.parser = WebIntentParser()
        self.generator = WebAppGenerator()
    
    def grow(self, intent: str) -> GeneratedWebApp:
        """
        Grow a web application from natural language intent.
        
        Args:
            intent: Natural language description of the desired app
            
        Returns:
            GeneratedWebApp with all files
        """
        print(f"\n{'='*60}")
        print(f"  GROWING WEB APPLICATION FROM INTENT")
        print(f"{'='*60}")
        print(f"\n  Intent: \"{intent}\"")
        
        # Parse intent
        print(f"\n  Parsing intent...")
        parsed = self.parser.parse(intent)
        print(f"    App type: {parsed.app_type}")
        print(f"    Components: {parsed.components}")
        print(f"    Features: {parsed.features}")
        if parsed.shapes:
            print(f"    Shapes: {parsed.shapes}")
        
        # Create output directory
        app_dir = self.output_dir / parsed.app_name
        app_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n  Output directory: {app_dir}")
        
        # Generate files
        print(f"\n  Generating LJPW-balanced web application...")
        files = self.generator.generate(parsed)
        
        # Write files
        for filename, content in files.items():
            filepath = app_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    Created: {filename} ({len(content)} bytes)")
        
        # Create result
        result = GeneratedWebApp(
            path=str(app_dir),
            files=files,
            app_type=parsed.app_type,
            features=parsed.features
        )
        
        print(f"\n{'='*60}")
        print(f"  WEB APPLICATION GROWN SUCCESSFULLY")
        print(f"{'='*60}\n")
        
        return result


# Convenience function
def grow_web_app(intent: str, output_dir: str = '.') -> GeneratedWebApp:
    """
    Convenience function to grow a web app from intent.
    
    Example:
        >>> app = grow_web_app("Create a 3D particle system with heart shapes")
        >>> print(app.path)
        ./particle_app
    """
    grower = WebAppGrower(output_dir)
    return grower.grow(intent)
