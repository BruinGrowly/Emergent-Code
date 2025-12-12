/**
 * SkyView Flight Tracker - Application
 * =====================================
 * 
 * A beautiful, real-time flight tracking application using OpenSky Network API.
 * 
 * Features:
 * - Real-time aircraft positions on interactive map
 * - Search and filter flights
 * - Detailed flight information
 * - Status indicators and notifications
 * - Auto-refresh with configurable interval
 * 
 * LJPW Principles Applied:
 * - Love: Intuitive UI, helpful tooltips, beautiful design
 * - Justice: Fair error handling, reliable data validation
 * - Power: Resilient API calls, graceful degradation
 * - Wisdom: Logging, status indicators, informative displays
 * 
 * API: OpenSky Network (https://opensky-network.org/api)
 * Free tier: 100 requests/day for anonymous users
 */

// =============================================================================
// CONFIGURATION
// =============================================================================

const CONFIG = {
    api: {
        baseUrl: 'https://opensky-network.org/api',
        refreshInterval: 15000,  // 15 seconds (respect rate limits)
        timeout: 10000
    },
    map: {
        defaultCenter: [20, 0],  // World center
        defaultZoom: 3,
        tileLayer: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attribution: '© OpenStreetMap contributors © CARTO'
    },
    regions: {
        world: { bounds: null },
        europe: { bounds: [[35, -10], [70, 40]] },
        namerica: { bounds: [[25, -130], [50, -60]] },
        asia: { bounds: [[10, 60], [55, 150]] },
        australia: { bounds: [[-45, 110], [-10, 160]] }
    }
};

// =============================================================================
// STATE
// =============================================================================

const state = {
    map: null,
    flights: new Map(),
    markers: new Map(),
    selectedFlight: null,
    trackedFlight: null,
    lastUpdate: null,
    isLoading: false,
    refreshTimer: null
};

// =============================================================================
// UTILITY FUNCTIONS
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
 * Format heading as compass direction.
 * @param {number} degrees - Heading in degrees
 * @returns {string} Formatted heading
 */
function formatHeading(degrees) {
    if (degrees === null || degrees === undefined) return 'N/A';
    const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const index = Math.round(degrees / 45) % 8;
    return Math.round(degrees) + '° ' + directions[index];
}

/**
 * Format vertical rate.
 * @param {number} rate - Vertical rate in m/s
 * @returns {string} Formatted rate
 */
function formatVerticalRate(rate) {
    if (rate === null || rate === undefined) return 'N/A';
    const fpm = Math.round(rate * 196.85);
    if (fpm > 100) return '+' + fpm + ' fpm ↑';
    if (fpm < -100) return fpm + ' fpm ↓';
    return 'Level';
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
 * Log with timestamp for debugging.
 * @param {string} context - Context/module name
 * @param {string} message - Log message
 */
function log(context, message) {
    console.log(`[${formatTime(new Date())}] [${context}] ${message}`);
}

// =============================================================================
// API FUNCTIONS
// =============================================================================

/**
 * Fetch flights from OpenSky Network API.
 * @param {object} bounds - Map bounds { south, north, west, east }
 * @returns {Promise<Array>} Array of flight data
 */
async function fetchFlights(bounds = null) {
    log('API', 'Fetching flights...');

    let url = `${CONFIG.api.baseUrl}/states/all`;

    if (bounds) {
        const { south, north, west, east } = bounds;
        url += `?lamin=${south}&lomin=${west}&lamax=${north}&lomax=${east}`;
    }

    try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), CONFIG.api.timeout);

        const response = await fetch(url, {
            signal: controller.signal,
            headers: {
                'Accept': 'application/json'
            }
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error(`API returned ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (!data || !data.states) {
            log('API', 'No flight data in response');
            return [];
        }

        // Parse the states array into flight objects
        const flights = data.states.map(state => ({
            icao24: state[0],
            callsign: state[1]?.trim() || 'Unknown',
            originCountry: state[2],
            longitude: state[5],
            latitude: state[6],
            altitude: state[7] || state[13],  // baro or geo altitude
            onGround: state[8],
            velocity: state[9],
            heading: state[10],
            verticalRate: state[11],
            sensors: state[12],
            lastContact: state[4],
            squawk: state[14]
        })).filter(f => f.longitude && f.latitude);

        log('API', `Received ${flights.length} flights`);
        return flights;

    } catch (error) {
        if (error.name === 'AbortError') {
            log('API', 'Request timed out');
            throw new Error('Request timed out. Try again.');
        }
        log('API', `Error: ${error.message}`);
        throw error;
    }
}

// =============================================================================
// MAP FUNCTIONS
// =============================================================================

/**
 * Initialize the Leaflet map.
 */
function initMap() {
    log('Map', 'Initializing...');

    state.map = L.map('map', {
        center: CONFIG.map.defaultCenter,
        zoom: CONFIG.map.defaultZoom,
        zoomControl: false,
        attributionControl: true
    });

    // Add tile layer
    L.tileLayer(CONFIG.map.tileLayer, {
        attribution: CONFIG.map.attribution,
        maxZoom: 18
    }).addTo(state.map);

    // Add zoom control to top-left
    L.control.zoom({ position: 'topleft' }).addTo(state.map);

    // Listen for map movement to update flight list
    state.map.on('moveend', updateFlightList);
    state.map.on('zoomend', updateFlightList);

    log('Map', 'Initialized');
}

/**
 * Create aircraft marker icon.
 * @param {object} flight - Flight data
 * @returns {L.DivIcon} Leaflet icon
 */
function createAircraftIcon(flight) {
    const category = getAltitudeCategory(flight.altitude);
    const rotation = flight.heading || 0;

    return L.divIcon({
        className: 'aircraft-marker',
        html: `<div class="aircraft-icon ${category}" style="transform: rotate(${rotation}deg)">✈</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    });
}

/**
 * Update aircraft markers on the map.
 * @param {Array} flights - Array of flight data
 */
function updateMarkers(flights) {
    const currentIcaos = new Set(flights.map(f => f.icao24));

    // Remove markers for flights that are no longer visible
    for (const [icao, marker] of state.markers) {
        if (!currentIcaos.has(icao)) {
            state.map.removeLayer(marker);
            state.markers.delete(icao);
        }
    }

    // Update or create markers
    for (const flight of flights) {
        state.flights.set(flight.icao24, flight);

        if (state.markers.has(flight.icao24)) {
            // Update existing marker
            const marker = state.markers.get(flight.icao24);
            marker.setLatLng([flight.latitude, flight.longitude]);
            marker.setIcon(createAircraftIcon(flight));
        } else {
            // Create new marker
            const marker = L.marker([flight.latitude, flight.longitude], {
                icon: createAircraftIcon(flight)
            });

            marker.on('click', () => selectFlight(flight.icao24));
            marker.addTo(state.map);
            state.markers.set(flight.icao24, marker);
        }
    }

    log('Map', `Updated ${flights.length} markers`);
}

/**
 * Center map on a specific flight.
 * @param {string} icao24 - Aircraft ICAO24 code
 */
function centerOnFlight(icao24) {
    const flight = state.flights.get(icao24);
    if (flight) {
        state.map.setView([flight.latitude, flight.longitude], 8, {
            animate: true
        });
    }
}

// =============================================================================
// UI FUNCTIONS
// =============================================================================

/**
 * Update the flight list in the sidebar.
 */
function updateFlightList() {
    const listEl = document.getElementById('flight-list');
    const countEl = document.getElementById('flight-count');
    const bounds = state.map.getBounds();

    // Get flights in current view
    const visibleFlights = Array.from(state.flights.values())
        .filter(f => bounds.contains([f.latitude, f.longitude]))
        .sort((a, b) => (b.altitude || 0) - (a.altitude || 0))
        .slice(0, 50);  // Limit to 50 for performance

    countEl.textContent = `(${visibleFlights.length})`;

    if (visibleFlights.length === 0) {
        listEl.innerHTML = `
            <div class="flight-list-empty">
                <p>No flights in current view</p>
                <p class="hint">Zoom out or change region</p>
            </div>
        `;
        return;
    }

    listEl.innerHTML = visibleFlights.map(flight => `
        <div class="flight-card ${state.selectedFlight === flight.icao24 ? 'selected' : ''}" 
             data-icao="${flight.icao24}">
            <div class="flight-card-header">
                <span class="flight-callsign">${flight.callsign}</span>
                <span class="flight-altitude">${formatAltitude(flight.altitude)}</span>
            </div>
            <div class="flight-card-body">
                <span class="flight-speed">⟳ ${formatSpeed(flight.velocity)}</span>
                <span class="flight-heading">↑ ${formatHeading(flight.heading)}</span>
            </div>
        </div>
    `).join('');

    // Add click handlers
    listEl.querySelectorAll('.flight-card').forEach(card => {
        card.addEventListener('click', () => {
            selectFlight(card.dataset.icao);
        });
    });
}

/**
 * Select a flight and show detail panel.
 * @param {string} icao24 - Aircraft ICAO24 code
 */
function selectFlight(icao24) {
    const flight = state.flights.get(icao24);
    if (!flight) return;

    state.selectedFlight = icao24;

    // Update flight list selection
    document.querySelectorAll('.flight-card').forEach(card => {
        card.classList.toggle('selected', card.dataset.icao === icao24);
    });

    // Update detail panel
    const detailPanel = document.getElementById('flight-detail');
    detailPanel.classList.remove('hidden');

    document.getElementById('detail-callsign').textContent = flight.callsign;
    document.getElementById('detail-route').textContent = `${flight.originCountry} → ...`;
    document.getElementById('detail-altitude').textContent = formatAltitude(flight.altitude);
    document.getElementById('detail-speed').textContent = formatSpeed(flight.velocity);
    document.getElementById('detail-heading').textContent = formatHeading(flight.heading);
    document.getElementById('detail-vrate').textContent = formatVerticalRate(flight.verticalRate);
    document.getElementById('detail-aircraft').textContent = 'Loading...';
    document.getElementById('detail-registration').textContent = flight.icao24.toUpperCase();

    // Center map on this flight
    centerOnFlight(icao24);

    log('UI', `Selected flight: ${flight.callsign}`);
}

/**
 * Close the flight detail panel.
 */
function closeFlightDetail() {
    document.getElementById('flight-detail').classList.add('hidden');
    state.selectedFlight = null;

    document.querySelectorAll('.flight-card').forEach(card => {
        card.classList.remove('selected');
    });
}

/**
 * Update the status indicator.
 * @param {string} status - Status: connected, connecting, error
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
    const overlay = document.getElementById('map-loading');
    overlay.classList.toggle('hidden', !show);
    state.isLoading = show;
}

// =============================================================================
// DATA REFRESH
// =============================================================================

/**
 * Refresh flight data.
 */
async function refreshFlights() {
    if (state.isLoading) return;

    setLoading(true);
    updateStatus('connecting', 'Updating...');

    try {
        // Get current map bounds
        const bounds = state.map.getBounds();
        const apiParams = {
            south: bounds.getSouth(),
            north: bounds.getNorth(),
            west: bounds.getWest(),
            east: bounds.getEast()
        };

        // Fetch flights
        const flights = await fetchFlights(apiParams);

        // Update markers
        updateMarkers(flights);

        // Update flight list
        updateFlightList();

        // Update stats
        document.getElementById('total-flights').textContent = flights.length.toLocaleString();
        document.getElementById('update-time').textContent = formatTime(new Date());
        state.lastUpdate = new Date();

        // Update status
        updateStatus('connected', 'Live');

        // If tracking a flight, center on it
        if (state.trackedFlight && state.flights.has(state.trackedFlight)) {
            centerOnFlight(state.trackedFlight);
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
    if (state.refreshTimer) {
        clearInterval(state.refreshTimer);
    }

    state.refreshTimer = setInterval(refreshFlights, CONFIG.api.refreshInterval);
    log('Refresh', `Started auto-refresh every ${CONFIG.api.refreshInterval / 1000}s`);
}

// =============================================================================
// FILTERS
// =============================================================================

/**
 * Apply region filter.
 * @param {string} region - Region key
 */
function applyRegionFilter(region) {
    const regionConfig = CONFIG.regions[region];

    if (region === 'custom') {
        // Use current view, just refresh
        refreshFlights();
    } else if (regionConfig && regionConfig.bounds) {
        state.map.fitBounds(regionConfig.bounds, { padding: [20, 20] });
        setTimeout(refreshFlights, 500);  // Wait for map to settle
    } else {
        // World view
        state.map.setView(CONFIG.map.defaultCenter, CONFIG.map.defaultZoom);
        setTimeout(refreshFlights, 500);
    }

    log('Filter', `Applied region: ${region}`);
}

/**
 * Apply altitude filter.
 * @param {string} filter - Altitude filter key
 */
function applyAltitudeFilter(filter) {
    // This would filter the displayed flights
    // For now, just update the flight list
    updateFlightList();
    log('Filter', `Applied altitude: ${filter}`);
}

/**
 * Search for flights.
 * @param {string} query - Search query
 */
function searchFlights(query) {
    if (!query) {
        updateFlightList();
        return;
    }

    query = query.toUpperCase();

    // Find matching flight
    for (const [icao, flight] of state.flights) {
        if (flight.callsign.toUpperCase().includes(query) ||
            icao.toUpperCase().includes(query)) {
            selectFlight(icao);
            showToast(`Found: ${flight.callsign}`, 'success');
            return;
        }
    }

    showToast(`No flights matching "${query}"`, 'error');
}

// =============================================================================
// EVENT LISTENERS
// =============================================================================

/**
 * Initialize all event listeners.
 */
function initEventListeners() {
    // Refresh button
    document.getElementById('btn-refresh').addEventListener('click', () => {
        refreshFlights();
    });

    // Center button
    document.getElementById('btn-center').addEventListener('click', () => {
        if (state.selectedFlight) {
            centerOnFlight(state.selectedFlight);
        } else {
            state.map.setView(CONFIG.map.defaultCenter, CONFIG.map.defaultZoom);
        }
    });

    // Fullscreen button
    document.getElementById('btn-fullscreen').addEventListener('click', () => {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            document.documentElement.requestFullscreen();
        }
    });

    // Close detail panel
    document.getElementById('close-detail').addEventListener('click', closeFlightDetail);

    // Track flight button
    document.getElementById('btn-track').addEventListener('click', () => {
        if (state.selectedFlight) {
            state.trackedFlight = state.trackedFlight === state.selectedFlight
                ? null
                : state.selectedFlight;

            const btn = document.getElementById('btn-track');
            btn.textContent = state.trackedFlight ? 'Stop Tracking' : 'Track This Flight';

            if (state.trackedFlight) {
                showToast('Tracking flight', 'success');
            }
        }
    });

    // Region filter
    document.getElementById('filter-region').addEventListener('change', (e) => {
        applyRegionFilter(e.target.value);
    });

    // Altitude filter
    document.getElementById('filter-altitude').addEventListener('change', (e) => {
        applyAltitudeFilter(e.target.value);
    });

    // Search
    document.getElementById('search-btn').addEventListener('click', () => {
        const query = document.getElementById('search-input').value;
        searchFlights(query);
    });

    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchFlights(e.target.value);
        }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeFlightDetail();
        } else if (e.key === 'r' && e.ctrlKey) {
            e.preventDefault();
            refreshFlights();
        }
    });

    log('Events', 'All event listeners initialized');
}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Main initialization function.
 */
async function init() {
    log('App', 'Starting SkyView Flight Tracker...');

    try {
        // Initialize map
        initMap();

        // Initialize event listeners
        initEventListeners();

        // Initial data fetch
        await refreshFlights();

        // Start auto-refresh
        startAutoRefresh();

        log('App', 'Initialization complete');
        showToast('SkyView initialized', 'success');

    } catch (error) {
        log('App', `Initialization error: ${error.message}`);
        updateStatus('error', 'Failed');
        showToast('Failed to initialize: ' + error.message, 'error');
        setLoading(false);
    }
}

// Start the application
init();
