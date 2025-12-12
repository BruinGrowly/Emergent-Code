/**
 * Map Tracker App - Grown by Autopoiesis
 * ===============================================
 *
 * LJPW Principles Applied:
 * - Love: Comprehensive documentation, helpful comments
 * - Justice: Input validation, fair error handling
 * - Power: Resilient API calls, graceful degradation
 * - Wisdom: Logging, status indicators, observability
 *
 * Generated: 2025-12-12T19:07:35.711091
 */

// =============================================================================
// CONFIGURATION (Love: documented, Justice: validated)
// =============================================================================

const CONFIG = {
    api: {
        baseUrl: 'https://opensky-network.org/api',
        refreshInterval: 15000,
        timeout: 10000
    },
    map: {
        defaultRegion: 'oceania',
        tileLayer: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    },
    regions: {
    'world': { name: 'Worldwide', bounds: null, center: [20, 0], zoom: 2 },
    'europe': { name: 'Europe', bounds: [[35, -10], [70, 40]], center: [50, 10], zoom: 4 },
    'namerica': { name: 'North America', bounds: [[25, -130], [50, -60]], center: [40, -95], zoom: 4 },
    'asia': { name: 'Asia', bounds: [[10, 60], [55, 150]], center: [35, 100], zoom: 3 },
    'oceania': { name: 'Oceania', bounds: [[-50, 110], [0, 180]], center: [-25, 145], zoom: 4 },
    'australia': { name: 'Australia', bounds: [[-45, 110], [-10, 160]], center: [-25, 135], zoom: 4 },
    'pacific': { name: 'Pacific', bounds: [[-50, 150], [50, -120]], center: [0, -170], zoom: 3 }
    }
};

// =============================================================================
// STATE (Wisdom: centralized, observable)
// =============================================================================

const state = {
    map: null,
    items: new Map(),
    markers: new Map(),
    selectedItem: null,
    trackedItem: null,
    lastUpdate: null,
    isLoading: false,
    refreshTimer: null,
    currentRegion: 'oceania'
};

// =============================================================================
// UTILITY FUNCTIONS (Love: well-documented)
// =============================================================================

/**
 * Format altitude in feet with thousands separator.
 * @param {number} meters - Altitude in meters
 * @returns {string} Formatted altitude
 */
function formatAltitude(meters) {
    if (meters === null || meters === undefined) return 'N/A';
    const feet = Math.round(meters * 3.28084);
    return feet.toLocaleString() + ' ft';
}

/**
 * Format speed in knots.
 * @param {number} ms - Speed in m/s
 * @returns {string} Formatted speed
 */
function formatSpeed(ms) {
    if (ms === null || ms === undefined) return 'N/A';
    const knots = Math.round(ms * 1.94384);
    return knots + ' kts';
}

/**
 * Format heading with compass direction.
 * @param {number} degrees - Heading in degrees
 * @returns {string} Formatted heading
 */
function formatHeading(degrees) {
    if (degrees === null || degrees === undefined) return 'N/A';
    const dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const idx = Math.round(degrees / 45) % 8;
    return Math.round(degrees) + '° ' + dirs[idx];
}

/**
 * Get altitude category for styling.
 * @param {number} meters - Altitude in meters
 * @returns {string} Category: ground, low, mid, high
 */
function getAltitudeCategory(meters) {
    if (meters === null || meters === undefined || meters < 100) return 'ground';
    const feet = meters * 3.28084;
    if (feet < 10000) return 'low';
    if (feet < 30000) return 'mid';
    return 'high';
}

/**
 * Format time as HH:MM:SS.
 * @param {Date} date - Date object
 * @returns {string} Formatted time
 */
function formatTime(date) {
    return date.toLocaleTimeString('en-US', { hour12: false });
}

/**
 * Show a toast notification.
 * @param {string} message - Message to show
 * @param {string} type - Type: success, error, info
 */
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
    
    console.log(`[Toast:${type}] ${message}`);
}

/**
 * Log with timestamp for debugging (Wisdom).
 * @param {string} context - Context/module name
 * @param {string} message - Log message
 */
function log(context, message) {
    console.log(`[${formatTime(new Date())}] [${context}] ${message}`);
}


// =============================================================================
// API: OpenSky Network (Power: resilient, Justice: validated)
// =============================================================================

/**
 * Fetch flight data from OpenSky Network API.
 * @param {object} bounds - Map bounds
 * @returns {Promise<Array>} Flight data
 */
async function fetchData(bounds) {
    log('API', 'Fetching flights...');
    
    let url = `${CONFIG.api.baseUrl}/states/all`;
    
    if (bounds) {
        url += `?lamin=${bounds.south}&lomin=${bounds.west}&lamax=${bounds.north}&lomax=${bounds.east}`;
    }
    
    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.api.timeout);
        
        const response = await fetch(url, {
            signal: controller.signal,
            headers: { 'Accept': 'application/json' }
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (!data || !data.states) {
            log('API', 'No flight data');
            return [];
        }
        
        // Parse flight data (Justice: validate each field)
        const flights = data.states.map(s => ({
            id: s[0],
            callsign: s[1]?.trim() || 'Unknown',
            originCountry: s[2],
            longitude: s[5],
            latitude: s[6],
            altitude: s[7] || s[13],
            onGround: s[8],
            velocity: s[9],
            heading: s[10],
            verticalRate: s[11],
            lastContact: s[4]
        })).filter(f => f.longitude && f.latitude);
        
        log('API', `Received ${flights.length} flights`);
        return flights;
        
    } catch (error) {
        if (error.name === 'AbortError') {
            throw new Error('Request timed out');
        }
        throw error;
    }
}


// =============================================================================
// MAP FUNCTIONS
// =============================================================================

/**
 * Initialize Leaflet map.
 */
function initMap() {
    log('Map', 'Initializing...');
    
    const region = CONFIG.regions[state.currentRegion];
    
    state.map = L.map('map', {
        center: region.center,
        zoom: region.zoom,
        zoomControl: false,
        attributionControl: true
    });
    
    L.tileLayer(CONFIG.map.tileLayer, {
        attribution: CONFIG.map.attribution,
        maxZoom: 18
    }).addTo(state.map);
    
    L.control.zoom({ position: 'topleft' }).addTo(state.map);
    
    state.map.on('moveend', updateItemList);
    state.map.on('zoomend', updateItemList);
    
    log('Map', 'Initialized');
}

/**
 * Create marker icon.
 * @param {object} item - Item data
 * @returns {L.DivIcon} Leaflet icon
 */
function createMarkerIcon(item) {
    const category = getAltitudeCategory(item.altitude);
    const rotation = item.heading || 0;
    
    return L.divIcon({
        className: 'marker-container',
        html: `<div class="marker-icon ${category}" style="transform: rotate(${rotation}deg)">✈</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
}

/**
 * Update markers on the map.
 * @param {Array} items - Array of item data
 */
function updateMarkers(items) {
    const currentIds = new Set(items.map(i => i.id));
    
    // Remove old markers
    for (const [id, marker] of state.markers) {
        if (!currentIds.has(id)) {
            state.map.removeLayer(marker);
            state.markers.delete(id);
        }
    }
    
    // Update or create markers
    for (const item of items) {
        state.items.set(item.id, item);
        
        if (state.markers.has(item.id)) {
            const marker = state.markers.get(item.id);
            marker.setLatLng([item.latitude, item.longitude]);
            marker.setIcon(createMarkerIcon(item));
        } else {
            const marker = L.marker([item.latitude, item.longitude], {
                icon: createMarkerIcon(item)
            });
            marker.on('click', () => selectItem(item.id));
            marker.addTo(state.map);
            state.markers.set(item.id, marker);
        }
    }
    
    log('Map', `Updated ${items.length} markers`);
}

/**
 * Center map on an item.
 * @param {string} id - Item ID
 */
function centerOnItem(id) {
    const item = state.items.get(id);
    if (item) {
        state.map.setView([item.latitude, item.longitude], 8, { animate: true });
    }
}

// =============================================================================
// UI FUNCTIONS
// =============================================================================

/**
 * Update the item list in sidebar.
 */
function updateItemList() {
    const listEl = document.getElementById('item-list');
    const countEl = document.getElementById('item-count');
    const bounds = state.map.getBounds();
    
    const visible = Array.from(state.items.values())
        .filter(i => bounds.contains([i.latitude, i.longitude]))
        .sort((a, b) => (b.altitude || 0) - (a.altitude || 0))
        .slice(0, 50);
    
    countEl.textContent = `(${visible.length})`;
    
    if (visible.length === 0) {
        listEl.innerHTML = `
            <div class="item-list-empty">
                <p>No items in current view</p>
                <p class="hint">Zoom out or change region</p>
            </div>
        `;
        return;
    }
    
    listEl.innerHTML = visible.map(item => `
        <div class="item-card ${state.selectedItem === item.id ? 'selected' : ''}" data-id="${item.id}">
            <div class="item-card-header">
                <span class="item-title">${item.callsign || item.id}</span>
                <span class="item-badge">${formatAltitude(item.altitude)}</span>
            </div>
            <div class="item-card-body">
                <span>⟳ ${formatSpeed(item.velocity)}</span>
                <span>↑ ${formatHeading(item.heading)}</span>
            </div>
        </div>
    `).join('');
    
    listEl.querySelectorAll('.item-card').forEach(card => {
        card.addEventListener('click', () => selectItem(card.dataset.id));
    });
}

/**
 * Select an item and show detail panel.
 * @param {string} id - Item ID
 */
function selectItem(id) {
    const item = state.items.get(id);
    if (!item) return;
    
    state.selectedItem = id;
    
    document.querySelectorAll('.item-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.id === id);
    });
    
    const panel = document.getElementById('detail-panel');
    panel.classList.remove('hidden');
    
    document.getElementById('detail-title').textContent = item.callsign || item.id;
    document.getElementById('detail-subtitle').textContent = item.originCountry || '--';
    
    document.getElementById('detail-grid').innerHTML = `
        <div class="detail-item">
            <span class="detail-label">Altitude</span>
            <span class="detail-value">${formatAltitude(item.altitude)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Speed</span>
            <span class="detail-value">${formatSpeed(item.velocity)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Heading</span>
            <span class="detail-value">${formatHeading(item.heading)}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">On Ground</span>
            <span class="detail-value">${item.onGround ? 'Yes' : 'No'}</span>
        </div>
    `;
    
    centerOnItem(id);
    log('UI', `Selected: ${item.callsign || id}`);
}

/**
 * Close detail panel.
 */
function closeDetail() {
    document.getElementById('detail-panel').classList.add('hidden');
    state.selectedItem = null;
    document.querySelectorAll('.item-card').forEach(c => c.classList.remove('selected'));
}

/**
 * Update status indicator.
 * @param {string} status - connected, connecting, error
 * @param {string} message - Status message
 */
function updateStatus(status, message) {
    const dot = document.getElementById('api-status');
    const text = document.getElementById('api-status-text');
    dot.className = 'status-dot ' + status;
    text.textContent = message;
}

/**
 * Show/hide loading overlay.
 * @param {boolean} show - Whether to show
 */
function setLoading(show) {
    document.getElementById('map-loading').classList.toggle('hidden', !show);
    state.isLoading = show;
}

// =============================================================================
// DATA REFRESH
// =============================================================================

/**
 * Refresh data from API.
 */
async function refreshData() {
    if (state.isLoading) return;
    
    setLoading(true);
    updateStatus('', 'Updating...');
    
    try {
        const bounds = state.map.getBounds();
        const params = {
            south: bounds.getSouth(),
            north: bounds.getNorth(),
            west: bounds.getWest(),
            east: bounds.getEast()
        };
        
        const items = await fetchData(params);
        
        updateMarkers(items);
        updateItemList();
        
        document.getElementById('total-count').textContent = items.length.toLocaleString();
        document.getElementById('update-time').textContent = formatTime(new Date());
        state.lastUpdate = new Date();
        
        updateStatus('connected', 'Live');
        
        if (state.trackedItem && state.items.has(state.trackedItem)) {
            centerOnItem(state.trackedItem);
        }
        
    } catch (error) {
        updateStatus('error', 'Error');
        showToast(error.message, 'error');
    } finally {
        setLoading(false);
    }
}

/**
 * Start auto-refresh timer.
 */
function startAutoRefresh() {
    if (state.refreshTimer) clearInterval(state.refreshTimer);
    state.refreshTimer = setInterval(refreshData, CONFIG.api.refreshInterval);
    log('Refresh', `Auto-refresh started: ${CONFIG.api.refreshInterval / 1000}s`);
}

// =============================================================================
// FILTERS
// =============================================================================

/**
 * Apply region filter.
 * @param {string} region - Region key
 */
function applyRegion(region) {
    const r = CONFIG.regions[region];
    if (!r) return;
    
    state.currentRegion = region;
    
    if (r.bounds) {
        state.map.fitBounds(r.bounds, { padding: [20, 20] });
    } else {
        state.map.setView(r.center, r.zoom);
    }
    
    setTimeout(refreshData, 500);
    log('Filter', `Region: ${region}`);
}

/**
 * Search for items.
 * @param {string} query - Search query
 */
function search(query) {
    if (!query) {
        updateItemList();
        return;
    }
    
    query = query.toUpperCase();
    
    for (const [id, item] of state.items) {
        const callsign = (item.callsign || '').toUpperCase();
        const itemId = id.toUpperCase();
        
        if (callsign.includes(query) || itemId.includes(query)) {
            selectItem(id);
            showToast(`Found: ${item.callsign || id}`, 'success');
            return;
        }
    }
    
    showToast(`No results for "${query}"`, 'error');
}

// =============================================================================
// EVENT LISTENERS
// =============================================================================

/**
 * Initialize event listeners.
 */
function initEvents() {
    log('Events', 'Initializing...');
    
    document.getElementById('btn-refresh').addEventListener('click', refreshData);
    
    document.getElementById('btn-center').addEventListener('click', () => {
        if (state.selectedItem) {
            centerOnItem(state.selectedItem);
        } else {
            const r = CONFIG.regions[state.currentRegion];
            state.map.setView(r.center, r.zoom);
        }
    });
    
    document.getElementById('btn-fullscreen').addEventListener('click', () => {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            document.documentElement.requestFullscreen();
        }
    });
    
    document.getElementById('close-detail').addEventListener('click', closeDetail);
    
    document.getElementById('btn-track').addEventListener('click', () => {
        if (state.selectedItem) {
            state.trackedItem = state.trackedItem === state.selectedItem ? null : state.selectedItem;
            document.getElementById('btn-track').textContent = state.trackedItem ? 'Stop Tracking' : 'Track';
            if (state.trackedItem) showToast('Tracking enabled', 'success');
        }
    });
    
    document.getElementById('filter-region').addEventListener('change', (e) => {
        applyRegion(e.target.value);
    });
    
    document.getElementById('search-btn')?.addEventListener('click', () => {
        search(document.getElementById('search-input').value);
    });
    
    document.getElementById('search-input')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') search(e.target.value);
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDetail();
        if (e.key === 'r' && e.ctrlKey) { e.preventDefault(); refreshData(); }
    });
    
    log('Events', 'Initialized');
}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Main initialization.
 */
async function init() {
    log('App', 'Starting...');
    
    try {
        initMap();
        initEvents();
        await refreshData();
        startAutoRefresh();
        
        log('App', 'Ready');
        showToast('Application ready', 'success');
        
    } catch (error) {
        log('App', `Error: ${error.message}`);
        updateStatus('error', 'Failed');
        showToast('Initialization failed: ' + error.message, 'error');
        setLoading(false);
    }
}

// Start
init();
