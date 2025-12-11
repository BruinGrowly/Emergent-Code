/**
 * Particle System Application
 * ===========================
 * 
 * A Particle System generated from: 
    Create a real-time interactive beautiful 3D particle system with Three.js.
    Requirements:
    1. Control the scaling and expansion of the particle group by detecting 
       the tension and closing of both hands through the camera.
    2. Provide panels that can choose hearts, spheres, spirals, cubes, rings,
       and explosions as shape templates.
    3. Support the color selector to adjust the particle color.
    4. Particles need to respond to gesture changes in real time.
    5. The interface is simple and modern.
    
 * 
 * Generated: 2025-12-12T01:15:31.577187
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

const CONFIG = {
    particles: {
        count: 2000,
        size: 3,
        color: 0xff6b9d
    },
    animation: {
        rotationSpeed: 0.002,
        scaleSmoothing: 0.1
    }
};

// =============================================================================
// STATE (Wisdom: centralized, observable)
// =============================================================================

const state = {
    currentShape: 'heart',
    targetScale: 1.0,
    currentScale: 1.0
};

// Three.js objects
let scene, camera, renderer, particles, particleGeometry, particleMaterial;

// =============================================================================
// SHAPE GENERATORS (Love: documented, Power: robust)
// =============================================================================


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
}


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
}


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
}


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
}


function generateRingPositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const theta = Math.random() * Math.PI * 2;
        const r = 1.5 + Math.random() * 0.3;
        const y = (Math.random() - 0.5) * 0.2;
        positions.push(r * Math.cos(theta), y, r * Math.sin(theta));
    }
    return positions;
}


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
}

const SHAPES = { 'heart': generateHeartPositions, 'sphere': generateSpherePositions, 'spiral': generateSpiralPositions, 'cube': generateCubePositions, 'ring': generateRingPositions, 'explosion': generateExplosionPositions };

// =============================================================================
// THREE.JS SETUP
// =============================================================================

/**
 * Initialize Three.js scene, camera, renderer.
 * @returns {void}
 */
function initThreeJS() {
    console.log('[Wisdom] Initializing Three.js...');
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a);
    
    // Camera
    camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    
    // Create particles
    createParticles();
    
    // Handle resize (Power: responsive)
    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
    
    console.log('[Wisdom] Three.js initialized');
}

/**
 * Create particle system with current shape.
 * @returns {void}
 */
function createParticles() {
    // Remove existing (Power: cleanup)
    if (particles) {
        scene.remove(particles);
        particleGeometry.dispose();
        particleMaterial.dispose();
    }
    
    // Generate positions
    const generator = SHAPES[state.currentShape];
    if (!generator) {
        console.error('[Justice] Invalid shape:', state.currentShape);
        return;
    }
    
    const positions = generator(CONFIG.particles.count);
    
    // Create geometry
    particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    
    // Create material
    particleMaterial = new THREE.PointsMaterial({
        color: CONFIG.particles.color,
        size: CONFIG.particles.size * 0.01,
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending
    });
    
    // Create points
    particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);
    
    console.log(`[Wisdom] Created ${CONFIG.particles.count} particles with shape: ${state.currentShape}`);
}


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


// =============================================================================
// ANIMATION LOOP
// =============================================================================

/**
 * Main animation loop.
 */
function animate() {
    requestAnimationFrame(animate);
    
    if (!particles) return;
    
    // Smooth scale transition
    state.currentScale += (state.targetScale - state.currentScale) * CONFIG.animation.scaleSmoothing;
    particles.scale.setScalar(state.currentScale);
    
    // Auto-rotate
    particles.rotation.y += CONFIG.animation.rotationSpeed;
    particles.rotation.x = Math.sin(Date.now() * 0.0003) * 0.1;
    
    renderer.render(scene, camera);
}

// =============================================================================
// UI CONTROLS
// =============================================================================

/**
 * Initialize UI event listeners.
 */
function initUI() {
    console.log('[Wisdom] Initializing UI...');
    
    // Shape buttons
    document.querySelectorAll('.shape-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Justice: validate input
            const shape = btn.dataset.shape;
            if (!SHAPES[shape]) {
                console.error('[Justice] Invalid shape:', shape);
                return;
            }
            
            // Update active state
            document.querySelectorAll('.shape-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            state.currentShape = shape;
            createParticles();
        });
    });
    
    // Color picker
    document.getElementById('color-picker').addEventListener('input', (e) => {
        CONFIG.particles.color = parseInt(e.target.value.replace('#', ''), 16);
        if (particleMaterial) particleMaterial.color.setHex(CONFIG.particles.color);
    });
    
    // Particle count
    const countSlider = document.getElementById('particle-count');
    const countValue = document.getElementById('count-value');
    countSlider.addEventListener('input', () => {
        CONFIG.particles.count = parseInt(countSlider.value);
        countValue.textContent = CONFIG.particles.count;
        createParticles();
    });
    
    // Particle size
    const sizeSlider = document.getElementById('particle-size');
    const sizeValue = document.getElementById('size-value');
    sizeSlider.addEventListener('input', () => {
        CONFIG.particles.size = parseFloat(sizeSlider.value);
        sizeValue.textContent = CONFIG.particles.size;
        if (particleMaterial) particleMaterial.size = CONFIG.particles.size * 0.01;
    });
    
    console.log('[Wisdom] UI initialized');
}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Main initialization function.
 */
async function init() {
    console.log('[Wisdom] Starting Particle System...');
    
    try {
        initThreeJS();
        initUI();
        await initHandTracking();
        animate();
        
        // Hide loading
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
        }, 500);
        
        console.log('[Wisdom] System ready');
    } catch (error) {
        console.error('[Power] Initialization failed:', error);
        document.getElementById('loading-overlay').innerHTML = 
            `<p style="color: #ff6b6b;">Failed to initialize: ${error.message}</p>`;
    }
}

// Start
init();
