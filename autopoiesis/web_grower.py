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
}

# Keywords to detect app type
APP_TYPE_KEYWORDS = {
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
        else:
            files = self._generate_generic_app(parsed)
        
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
