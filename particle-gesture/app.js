/**
 * Gesture Particle System
 * =======================
 * 
 * A real-time interactive 3D particle system controlled by hand gestures.
 * 
 * Features:
 * - Three.js particle rendering
 * - MediaPipe hand tracking
 * - Multiple shape templates (heart, flower, saturn, firework, spiral, cube)
 * - Real-time gesture control (expand/contract with hand openness)
 * - Color customization
 * 
 * LJPW Principles Applied:
 * - Love: Comprehensive documentation
 * - Justice: Input validation
 * - Power: Error handling throughout
 * - Wisdom: Console logging for debugging
 */

// =============================================================================
// CONFIGURATION
// =============================================================================

const CONFIG = {
    particles: {
        count: 2000,
        size: 3,
        color: 0xff6b9d
    },
    gesture: {
        smoothing: 0.15,
        minScale: 0.3,
        maxScale: 3.0,
        rotationSpeed: 0.02
    },
    templates: {
        heart: generateHeartPositions,
        flower: generateFlowerPositions,
        saturn: generateSaturnPositions,
        firework: generateFireworkPositions,
        spiral: generateSpiralPositions,
        cube: generateCubePositions
    }
};

// =============================================================================
// STATE
// =============================================================================

const state = {
    currentTemplate: 'heart',
    targetScale: 1.0,
    currentScale: 1.0,
    targetRotation: { x: 0, y: 0 },
    handData: {
        leftOpen: 0,
        rightOpen: 0,
        handsDetected: 0
    },
    isInitialized: false
};

// Three.js objects
let scene, camera, renderer, particles, particleGeometry, particleMaterial;
let basePositions = [];

// MediaPipe objects
let hands, videoElement, handCanvas, handCtx;

// =============================================================================
// TEMPLATE GENERATORS
// =============================================================================

/**
 * Generate heart-shaped particle positions.
 * Uses parametric heart curve.
 */
function generateHeartPositions(count) {
    const positions = [];
    for (let i = 0; i < count; i++) {
        const t = (i / count) * Math.PI * 2;
        const r = Math.random() * 0.3 + 0.85;

        // Parametric heart
        const x = 16 * Math.pow(Math.sin(t), 3) * r;
        const y = (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * r;
        const z = (Math.random() - 0.5) * 4;

        positions.push(x * 0.1, y * 0.1 + 0.5, z * 0.1);
    }
    return positions;
}

/**
 * Generate flower-shaped particle positions.
 * Uses rose curve with petals.
 */
function generateFlowerPositions(count) {
    const positions = [];
    const petals = 5;

    for (let i = 0; i < count; i++) {
        const t = (i / count) * Math.PI * 2;
        const r = Math.cos(petals * t) * 2 + 1;
        const noise = Math.random() * 0.5;

        const x = (r + noise) * Math.cos(t);
        const y = (r + noise) * Math.sin(t);
        const z = (Math.random() - 0.5) * 2;

        positions.push(x * 0.5, y * 0.5, z * 0.3);
    }
    return positions;
}

/**
 * Generate Saturn-like particle positions.
 * Sphere with ring system.
 */
function generateSaturnPositions(count) {
    const positions = [];
    const ringParticles = Math.floor(count * 0.4);
    const sphereParticles = count - ringParticles;

    // Sphere
    for (let i = 0; i < sphereParticles; i++) {
        const phi = Math.acos(2 * Math.random() - 1);
        const theta = Math.random() * Math.PI * 2;
        const r = 1.2 + Math.random() * 0.2;

        positions.push(
            r * Math.sin(phi) * Math.cos(theta),
            r * Math.sin(phi) * Math.sin(theta) * 0.8,
            r * Math.cos(phi)
        );
    }

    // Rings
    for (let i = 0; i < ringParticles; i++) {
        const theta = Math.random() * Math.PI * 2;
        const r = 2 + Math.random() * 0.8;

        positions.push(
            r * Math.cos(theta),
            (Math.random() - 0.5) * 0.1,
            r * Math.sin(theta)
        );
    }

    return positions;
}

/**
 * Generate firework explosion particle positions.
 * Radial burst pattern.
 */
function generateFireworkPositions(count) {
    const positions = [];
    const bursts = 5;
    const perBurst = Math.floor(count / bursts);

    for (let b = 0; b < bursts; b++) {
        const centerY = (b - 2) * 0.8;
        const burstRadius = 1 + Math.random() * 0.5;

        for (let i = 0; i < perBurst; i++) {
            const phi = Math.acos(2 * Math.random() - 1);
            const theta = Math.random() * Math.PI * 2;
            const r = burstRadius * Math.random();

            positions.push(
                r * Math.sin(phi) * Math.cos(theta),
                r * Math.sin(phi) * Math.sin(theta) + centerY,
                r * Math.cos(phi)
            );
        }
    }

    return positions;
}

/**
 * Generate spiral galaxy particle positions.
 * Logarithmic spiral arms.
 */
function generateSpiralPositions(count) {
    const positions = [];
    const arms = 3;

    for (let i = 0; i < count; i++) {
        const arm = i % arms;
        const t = (i / count) * 6 + (arm * Math.PI * 2 / arms);
        const r = t * 0.3 + Math.random() * 0.3;

        const x = r * Math.cos(t * 2);
        const y = (Math.random() - 0.5) * 0.3;
        const z = r * Math.sin(t * 2);

        positions.push(x, y, z);
    }
    return positions;
}

/**
 * Generate cube particle positions.
 * Points distributed on cube surface and interior.
 */
function generateCubePositions(count) {
    const positions = [];
    const size = 2;

    for (let i = 0; i < count; i++) {
        // 70% on surface, 30% inside
        if (Math.random() < 0.7) {
            // Surface
            const face = Math.floor(Math.random() * 6);
            let x, y, z;

            switch (face) {
                case 0: x = size; y = (Math.random() - 0.5) * size * 2; z = (Math.random() - 0.5) * size * 2; break;
                case 1: x = -size; y = (Math.random() - 0.5) * size * 2; z = (Math.random() - 0.5) * size * 2; break;
                case 2: x = (Math.random() - 0.5) * size * 2; y = size; z = (Math.random() - 0.5) * size * 2; break;
                case 3: x = (Math.random() - 0.5) * size * 2; y = -size; z = (Math.random() - 0.5) * size * 2; break;
                case 4: x = (Math.random() - 0.5) * size * 2; y = (Math.random() - 0.5) * size * 2; z = size; break;
                case 5: x = (Math.random() - 0.5) * size * 2; y = (Math.random() - 0.5) * size * 2; z = -size; break;
            }
            positions.push(x * 0.5, y * 0.5, z * 0.5);
        } else {
            // Inside
            positions.push(
                (Math.random() - 0.5) * size,
                (Math.random() - 0.5) * size,
                (Math.random() - 0.5) * size
            );
        }
    }
    return positions;
}

// =============================================================================
// THREE.JS SETUP
// =============================================================================

/**
 * Initialize Three.js scene, camera, renderer, and particles.
 */
function initThreeJS() {
    console.log('[Wisdom] Initializing Three.js...');

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a1a);

    // Camera
    camera = new THREE.PerspectiveCamera(
        60,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.z = 5;

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    document.getElementById('canvas-container').appendChild(renderer.domElement);

    // Create particles
    createParticles();

    // Handle resize
    window.addEventListener('resize', onWindowResize);

    console.log('[Wisdom] Three.js initialized successfully');
}

/**
 * Create particle system with current template.
 */
function createParticles() {
    // Remove existing particles
    if (particles) {
        scene.remove(particles);
        particleGeometry.dispose();
        particleMaterial.dispose();
    }

    // Generate positions
    const generator = CONFIG.templates[state.currentTemplate];
    basePositions = generator(CONFIG.particles.count);

    // Create geometry
    particleGeometry = new THREE.BufferGeometry();
    particleGeometry.setAttribute(
        'position',
        new THREE.Float32BufferAttribute(basePositions, 3)
    );

    // Create material
    particleMaterial = new THREE.PointsMaterial({
        color: CONFIG.particles.color,
        size: CONFIG.particles.size * 0.01,
        transparent: true,
        opacity: 0.9,
        blending: THREE.AdditiveBlending,
        sizeAttenuation: true
    });

    // Create particle system
    particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);

    console.log(`[Wisdom] Created ${CONFIG.particles.count} particles with template: ${state.currentTemplate}`);
}

/**
 * Handle window resize.
 */
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// =============================================================================
// HAND TRACKING
// =============================================================================

/**
 * Initialize MediaPipe Hands.
 */
async function initHandTracking() {
    console.log('[Wisdom] Initializing hand tracking...');

    videoElement = document.getElementById('video');
    handCanvas = document.getElementById('hand-canvas');
    handCtx = handCanvas.getContext('2d');

    // Initialize MediaPipe Hands
    hands = new Hands({
        locateFile: (file) => {
            return `https://cdn.jsdelivr.net/npm/@mediapipe/hands@0.4.1675469240/${file}`;
        }
    });

    hands.setOptions({
        maxNumHands: 2,
        modelComplexity: 1,
        minDetectionConfidence: 0.7,
        minTrackingConfidence: 0.5
    });

    hands.onResults(onHandResults);

    // Start camera
    try {
        const stream = await navigator.mediaDevices.getUserMedia({
            video: { width: 640, height: 480, facingMode: 'user' }
        });
        videoElement.srcObject = stream;

        // Process video frames
        videoElement.onloadedmetadata = () => {
            handCanvas.width = videoElement.videoWidth;
            handCanvas.height = videoElement.videoHeight;
            processVideoFrame();
        };

        console.log('[Wisdom] Hand tracking initialized successfully');

        // Hide loading overlay
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
            state.isInitialized = true;
        }, 1000);

    } catch (error) {
        console.error('[Power] Failed to initialize camera:', error);
        document.getElementById('loading-overlay').innerHTML = `
            <p style="color: #ff6b6b;">Camera access denied or unavailable</p>
            <p style="color: #888; font-size: 12px; margin-top: 10px;">
                The particle system will still work, but gesture control is disabled.
            </p>
        `;
        setTimeout(() => {
            document.getElementById('loading-overlay').classList.add('hidden');
            state.isInitialized = true;
        }, 3000);
    }
}

/**
 * Process video frame for hand detection.
 */
async function processVideoFrame() {
    if (videoElement.readyState >= 2) {
        await hands.send({ image: videoElement });
    }
    requestAnimationFrame(processVideoFrame);
}

/**
 * Handle hand detection results.
 */
function onHandResults(results) {
    // Clear canvas
    handCtx.clearRect(0, 0, handCanvas.width, handCanvas.height);

    state.handData.handsDetected = results.multiHandLandmarks ? results.multiHandLandmarks.length : 0;

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        // Draw hand landmarks
        for (const landmarks of results.multiHandLandmarks) {
            drawHand(landmarks);
        }

        // Calculate hand openness for each hand
        let leftOpenness = 0;
        let rightOpenness = 0;

        results.multiHandLandmarks.forEach((landmarks, index) => {
            const openness = calculateHandOpenness(landmarks);
            const handedness = results.multiHandedness[index].label;

            if (handedness === 'Left') {
                rightOpenness = openness; // Mirrored
            } else {
                leftOpenness = openness;
            }
        });

        state.handData.leftOpen = leftOpenness;
        state.handData.rightOpen = rightOpenness;

        // Calculate target scale from hand openness
        const avgOpenness = (leftOpenness + rightOpenness) / Math.max(state.handData.handsDetected, 1);
        state.targetScale = CONFIG.gesture.minScale + avgOpenness * (CONFIG.gesture.maxScale - CONFIG.gesture.minScale);

        // Update status
        updateGestureStatus(avgOpenness);
    } else {
        // No hands detected - slowly return to default
        state.targetScale = 1.0;
        document.getElementById('hand-status').textContent = '🖐️ Show hands to control';
    }
}

/**
 * Calculate how open a hand is (0 = fist, 1 = fully open).
 */
function calculateHandOpenness(landmarks) {
    // Compare fingertip distances to palm
    const palmBase = landmarks[0];
    const fingerTips = [landmarks[4], landmarks[8], landmarks[12], landmarks[16], landmarks[20]];
    const fingerBases = [landmarks[2], landmarks[5], landmarks[9], landmarks[13], landmarks[17]];

    let totalExtension = 0;

    for (let i = 0; i < 5; i++) {
        const tipDist = distance3D(fingerTips[i], palmBase);
        const baseDist = distance3D(fingerBases[i], palmBase);
        const extension = tipDist / (baseDist + 0.01);
        totalExtension += Math.min(extension, 3) / 3;
    }

    return totalExtension / 5;
}

/**
 * Calculate 3D distance between two landmarks.
 */
function distance3D(a, b) {
    return Math.sqrt(
        Math.pow(a.x - b.x, 2) +
        Math.pow(a.y - b.y, 2) +
        Math.pow(a.z - b.z, 2)
    );
}

/**
 * Draw hand landmarks on canvas.
 */
function drawHand(landmarks) {
    // Draw connections
    const connections = [
        [0, 1], [1, 2], [2, 3], [3, 4],
        [0, 5], [5, 6], [6, 7], [7, 8],
        [5, 9], [9, 10], [10, 11], [11, 12],
        [9, 13], [13, 14], [14, 15], [15, 16],
        [13, 17], [17, 18], [18, 19], [19, 20],
        [0, 17]
    ];

    handCtx.strokeStyle = 'rgba(0, 212, 255, 0.6)';
    handCtx.lineWidth = 2;

    for (const [a, b] of connections) {
        handCtx.beginPath();
        handCtx.moveTo(landmarks[a].x * handCanvas.width, landmarks[a].y * handCanvas.height);
        handCtx.lineTo(landmarks[b].x * handCanvas.width, landmarks[b].y * handCanvas.height);
        handCtx.stroke();
    }

    // Draw points
    for (const point of landmarks) {
        handCtx.beginPath();
        handCtx.arc(
            point.x * handCanvas.width,
            point.y * handCanvas.height,
            3, 0, Math.PI * 2
        );
        handCtx.fillStyle = '#00d4ff';
        handCtx.fill();
    }
}

/**
 * Update gesture status display.
 */
function updateGestureStatus(openness) {
    const statusEl = document.getElementById('hand-status');

    if (openness > 0.7) {
        statusEl.textContent = '👐 Expanding particles';
        statusEl.style.color = '#00ff88';
    } else if (openness < 0.3) {
        statusEl.textContent = '✊ Contracting particles';
        statusEl.style.color = '#ff6b6b';
    } else {
        statusEl.textContent = '🖐️ Adjust hand openness';
        statusEl.style.color = '#00d4ff';
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
    state.currentScale += (state.targetScale - state.currentScale) * CONFIG.gesture.smoothing;

    // Apply scale to particles
    particles.scale.setScalar(state.currentScale);

    // Auto-rotate
    particles.rotation.y += 0.002;
    particles.rotation.x = Math.sin(Date.now() * 0.0003) * 0.1;

    // Render
    renderer.render(scene, camera);
}

// =============================================================================
// UI EVENT HANDLERS
// =============================================================================

/**
 * Initialize UI controls.
 */
function initUI() {
    console.log('[Wisdom] Initializing UI...');

    // Template buttons
    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Validate input (Justice)
            const template = btn.dataset.template;
            if (!CONFIG.templates[template]) {
                console.error('[Justice] Invalid template:', template);
                return;
            }

            // Update active state
            document.querySelectorAll('.template-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Change template
            state.currentTemplate = template;
            createParticles();
        });
    });

    // Color picker
    document.getElementById('color-picker').addEventListener('input', (e) => {
        const color = e.target.value;
        CONFIG.particles.color = parseInt(color.replace('#', ''), 16);
        if (particleMaterial) {
            particleMaterial.color.setHex(CONFIG.particles.color);
        }
    });

    // Color presets
    document.querySelectorAll('.color-preset').forEach(btn => {
        btn.addEventListener('click', () => {
            const color = btn.dataset.color;
            document.getElementById('color-picker').value = color;
            CONFIG.particles.color = parseInt(color.replace('#', ''), 16);
            if (particleMaterial) {
                particleMaterial.color.setHex(CONFIG.particles.color);
            }
        });
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
        if (particleMaterial) {
            particleMaterial.size = CONFIG.particles.size * 0.01;
        }
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
    console.log('[Wisdom] Starting Gesture Particle System...');

    try {
        initThreeJS();
        initUI();
        await initHandTracking();
        animate();

        console.log('[Wisdom] System fully initialized and running');
    } catch (error) {
        console.error('[Power] Initialization failed:', error);
        document.getElementById('loading-overlay').innerHTML = `
            <p style="color: #ff6b6b;">Failed to initialize: ${error.message}</p>
        `;
    }
}

// Start the application
init();
