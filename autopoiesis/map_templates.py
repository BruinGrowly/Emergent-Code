"""
Map-Based Application Templates for Web Grower
===============================================

This module extends the web grower with templates for map-based applications
such as flight trackers, ship trackers, location finders, etc.

Uses Leaflet.js for mapping and OpenSky Network API for flight data.
"""

from datetime import datetime
from typing import Dict, List


# =============================================================================
# MAP APPLICATION DOMAIN KNOWLEDGE
# =============================================================================

# Map-based application types
MAP_APP_TYPES = {
    'flight_tracker': {
        'name': 'Flight Tracker',
        'api': 'opensky',
        'components': ['map', 'sidebar', 'search', 'filters', 'details', 'markers'],
        'features': ['realtime', 'tracking', 'regions', 'search'],
    },
    'ship_tracker': {
        'name': 'Ship Tracker',
        'api': 'ais',
        'components': ['map', 'sidebar', 'search', 'filters', 'details', 'markers'],
        'features': ['realtime', 'tracking', 'regions'],
    },
    'location_map': {
        'name': 'Location Map',
        'api': 'generic',
        'components': ['map', 'sidebar', 'search', 'markers'],
        'features': ['geocoding', 'markers', 'clustering'],
    },
}

# Keywords to detect map tracker type
MAP_KEYWORDS = {
    'flight_tracker': ['flight', 'plane', 'aircraft', 'aviation', 'airline', 'airport'],
    'ship_tracker': ['ship', 'vessel', 'maritime', 'marine', 'boat', 'port'],
    'location_map': ['location', 'place', 'point', 'marker', 'geocode'],
}

# Geographic regions with bounds
REGIONS = {
    'world': {'name': 'Worldwide', 'bounds': None, 'center': [20, 0], 'zoom': 2},
    'europe': {'name': 'Europe', 'bounds': [[35, -10], [70, 40]], 'center': [50, 10], 'zoom': 4},
    'namerica': {'name': 'North America', 'bounds': [[25, -130], [50, -60]], 'center': [40, -95], 'zoom': 4},
    'samerica': {'name': 'South America', 'bounds': [[-55, -80], [12, -35]], 'center': [-15, -60], 'zoom': 3},
    'asia': {'name': 'Asia', 'bounds': [[10, 60], [55, 150]], 'center': [35, 100], 'zoom': 3},
    'africa': {'name': 'Africa', 'bounds': [[-35, -20], [37, 55]], 'center': [0, 20], 'zoom': 3},
    'oceania': {'name': 'Oceania', 'bounds': [[-50, 110], [0, 180]], 'center': [-25, 145], 'zoom': 4},
    'australia': {'name': 'Australia', 'bounds': [[-45, 110], [-10, 160]], 'center': [-25, 135], 'zoom': 4},
    'pacific': {'name': 'Pacific', 'bounds': [[-50, 150], [50, -120]], 'center': [0, -170], 'zoom': 3},
    'middle_east': {'name': 'Middle East', 'bounds': [[12, 25], [45, 65]], 'center': [28, 45], 'zoom': 4},
}


# =============================================================================
# HTML TEMPLATES
# =============================================================================

def generate_map_html(app_name: str, title: str, regions: List[str], has_search: bool = True) -> str:
    """Generate HTML for a map-based tracker application."""
    
    region_options = '\n                        '.join([
        f'<option value="{key}">{REGIONS[key]["name"]}</option>'
        for key in regions if key in REGIONS
    ])
    
    search_html = '''
            <!-- Search -->
            <div class="sidebar-section">
                <h3>Search</h3>
                <div class="search-box">
                    <input type="text" id="search-input" placeholder="Search...">
                    <button id="search-btn" class="btn-primary">Search</button>
                </div>
            </div>
''' if has_search else ''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <!--
    {title} - Grown by Autopoiesis System
    =======================================
    
    LJPW Principles Applied:
    - Love: Beautiful design, intuitive interface
    - Justice: Fair error handling, input validation
    - Power: Resilient API calls, graceful degradation
    - Wisdom: Status indicators, logging, tooltips
    
    Generated: {datetime.now().isoformat()}
    -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{title} - Real-time tracking application">
    <title>{title}</title>
    <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
</head>
<body>
    <!-- Header -->
    <header id="header">
        <div class="logo">
            <span class="logo-icon">✈</span>
            <span class="logo-text">{title}</span>
        </div>
        <div class="header-stats">
            <div class="stat">
                <span class="stat-value" id="total-count">--</span>
                <span class="stat-label">Tracked</span>
            </div>
            <div class="stat">
                <span class="stat-value" id="update-time">--</span>
                <span class="stat-label">Last Update</span>
            </div>
            <div class="stat status-indicator">
                <span class="status-dot" id="api-status"></span>
                <span class="stat-label" id="api-status-text">Connecting...</span>
            </div>
        </div>
    </header>

    <!-- Main Layout -->
    <main id="main">
        <!-- Map Container -->
        <div id="map-container">
            <div id="map"></div>
            
            <!-- Map Controls -->
            <div id="map-controls">
                <button class="map-btn" id="btn-refresh" title="Refresh Data">↻</button>
                <button class="map-btn" id="btn-center" title="Reset View">◎</button>
                <button class="map-btn" id="btn-fullscreen" title="Fullscreen">⛶</button>
            </div>
            
            <!-- Loading Overlay -->
            <div id="map-loading">
                <div class="loader"></div>
                <p>Loading data...</p>
            </div>
        </div>
        
        <!-- Sidebar -->
        <aside id="sidebar">
{search_html}
            <!-- Filters -->
            <div class="sidebar-section">
                <h3>Region</h3>
                <div class="filter-group">
                    <select id="filter-region">
                        {region_options}
                    </select>
                </div>
            </div>
            
            <div class="sidebar-section">
                <h3>Altitude</h3>
                <div class="filter-group">
                    <select id="filter-altitude">
                        <option value="all">All Altitudes</option>
                        <option value="ground">On Ground</option>
                        <option value="low">Low (&lt; 10,000 ft)</option>
                        <option value="mid">Medium (10k - 30k ft)</option>
                        <option value="high">High (&gt; 30,000 ft)</option>
                    </select>
                </div>
            </div>
            
            <!-- Item List -->
            <div class="sidebar-section item-list-section">
                <h3>Nearby <span id="item-count">(0)</span></h3>
                <div id="item-list" class="item-list">
                    <div class="item-list-empty">
                        <p>No items in current view</p>
                        <p class="hint">Zoom out or change region</p>
                    </div>
                </div>
            </div>
        </aside>
    </main>
    
    <!-- Detail Panel -->
    <div id="detail-panel" class="hidden">
        <button class="close-btn" id="close-detail">&times;</button>
        <div class="detail-header">
            <div class="detail-title" id="detail-title">--</div>
            <div class="detail-subtitle" id="detail-subtitle">--</div>
        </div>
        <div class="detail-grid" id="detail-grid">
            <!-- Dynamic content -->
        </div>
        <button class="btn-primary btn-track" id="btn-track">Track</button>
    </div>
    
    <!-- Toast Container -->
    <div id="toast-container"></div>

    <!-- Scripts -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="app.js"></script>
</body>
</html>
'''


# =============================================================================
# CSS TEMPLATES
# =============================================================================

def generate_map_css(primary_color: str = '#3b82f6', secondary_color: str = '#06b6d4') -> str:
    """Generate CSS for a map-based tracker application."""
    
    return f'''/*
 * Map Tracker Styles - Grown by Autopoiesis
 * ==========================================
 *
 * LJPW Design Principles:
 * - Love: Beautiful aesthetics, attention to detail
 * - Justice: Consistent spacing, predictable patterns
 * - Power: Responsive, handles all screen sizes
 * - Wisdom: Clear visual hierarchy, status indicators
 *
 * Generated: {datetime.now().isoformat()}
 */

/* =============================================================================
   DESIGN TOKENS
   ============================================================================= */

:root {{
    /* Colors - Dark Sky Theme */
    --bg-primary: #0b1120;
    --bg-secondary: #111827;
    --bg-tertiary: #1f2937;
    --bg-card: rgba(31, 41, 55, 0.9);
    --bg-glass: rgba(17, 24, 39, 0.85);
    
    /* Accent Colors */
    --accent-primary: {primary_color};
    --accent-secondary: {secondary_color};
    --accent-success: #10b981;
    --accent-warning: #f59e0b;
    --accent-error: #ef4444;
    
    /* Gradients */
    --gradient-sky: linear-gradient(135deg, #1e3a5f 0%, #0b1120 50%, #1a1a2e 100%);
    --gradient-accent: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
    
    /* Text */
    --text-primary: #f9fafb;
    --text-secondary: #9ca3af;
    --text-muted: #6b7280;
    
    /* Borders */
    --border-color: rgba(255, 255, 255, 0.1);
    --border-light: rgba(255, 255, 255, 0.05);
    
    /* Shadows */
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 10px 40px rgba(0, 0, 0, 0.5);
    --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.3);
    
    /* Spacing */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    
    /* Radii */
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-full: 9999px;
    
    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 250ms ease;
    --transition-smooth: 400ms cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Layout */
    --header-height: 60px;
    --sidebar-width: 320px;
}}

/* =============================================================================
   RESET & BASE
   ============================================================================= */

*, *::before, *::after {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

html {{ font-size: 14px; }}

body {{
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
    background: var(--gradient-sky);
    color: var(--text-primary);
    line-height: 1.5;
    overflow: hidden;
    height: 100vh;
}}

/* =============================================================================
   HEADER
   ============================================================================= */

#header {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: var(--header-height);
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--space-lg);
    z-index: 1000;
}}

.logo {{
    display: flex;
    align-items: center;
    gap: var(--space-sm);
}}

.logo-icon {{
    font-size: 28px;
    filter: drop-shadow(0 0 10px var(--accent-secondary));
}}

.logo-text {{
    font-size: 22px;
    font-weight: 700;
    background: var(--gradient-accent);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.header-stats {{
    display: flex;
    gap: var(--space-xl);
}}

.stat {{
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.stat-value {{
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
}}

.stat-label {{
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

.status-indicator {{
    flex-direction: row;
    gap: var(--space-sm);
}}

.status-dot {{
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--accent-warning);
    animation: pulse 2s ease-in-out infinite;
}}

.status-dot.connected {{ background: var(--accent-success); animation: none; }}
.status-dot.error {{ background: var(--accent-error); animation: none; }}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.5; }}
}}

/* =============================================================================
   MAIN LAYOUT
   ============================================================================= */

#main {{
    position: fixed;
    top: var(--header-height);
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
}}

/* =============================================================================
   MAP
   ============================================================================= */

#map-container {{
    flex: 1;
    position: relative;
}}

#map {{
    width: 100%;
    height: 100%;
    background: var(--bg-primary);
}}

/* Leaflet Customization */
.leaflet-container {{
    background: var(--bg-primary);
    font-family: inherit;
}}

.leaflet-tile-pane {{
    filter: brightness(0.7) saturate(1.2);
}}

.leaflet-control-zoom {{
    border: none !important;
    box-shadow: var(--shadow-md) !important;
}}

.leaflet-control-zoom a {{
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-color) !important;
    width: 36px !important;
    height: 36px !important;
    line-height: 36px !important;
}}

.leaflet-control-zoom a:hover {{
    background: var(--bg-tertiary) !important;
}}

/* Map Controls */
#map-controls {{
    position: absolute;
    top: var(--space-md);
    right: var(--space-md);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    z-index: 500;
}}

.map-btn {{
    width: 44px;
    height: 44px;
    border-radius: var(--radius-md);
    border: 1px solid var(--border-color);
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    color: var(--text-primary);
    font-size: 20px;
    cursor: pointer;
    transition: var(--transition-fast);
    display: flex;
    align-items: center;
    justify-content: center;
}}

.map-btn:hover {{
    background: var(--bg-tertiary);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-glow);
}}

/* Loading Overlay */
#map-loading {{
    position: absolute;
    inset: 0;
    background: rgba(11, 17, 32, 0.9);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 600;
    transition: var(--transition-normal);
}}

#map-loading.hidden {{
    opacity: 0;
    pointer-events: none;
}}

.loader {{
    width: 48px;
    height: 48px;
    border: 3px solid var(--border-color);
    border-top-color: var(--accent-secondary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--space-md);
}}

@keyframes spin {{
    to {{ transform: rotate(360deg); }}
}}

/* =============================================================================
   SIDEBAR
   ============================================================================= */

#sidebar {{
    width: var(--sidebar-width);
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border-left: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.sidebar-section {{
    padding: var(--space-md);
    border-bottom: 1px solid var(--border-light);
}}

.sidebar-section h3 {{
    font-size: 12px;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-md);
}}

/* Search Box */
.search-box {{
    display: flex;
    gap: var(--space-sm);
}}

.search-box input {{
    flex: 1;
    height: 40px;
    padding: 0 var(--space-md);
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
}}

.search-box input:focus {{
    outline: none;
    border-color: var(--accent-primary);
}}

.search-box input::placeholder {{
    color: var(--text-muted);
}}

/* Buttons */
.btn-primary {{
    height: 40px;
    padding: 0 var(--space-md);
    background: var(--gradient-accent);
    border: none;
    border-radius: var(--radius-md);
    color: white;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition-fast);
}}

.btn-primary:hover {{
    opacity: 0.9;
    box-shadow: var(--shadow-glow);
}}

/* Filter Groups */
.filter-group {{
    margin-bottom: var(--space-md);
}}

.filter-group:last-child {{
    margin-bottom: 0;
}}

.filter-group select {{
    width: 100%;
    height: 40px;
    padding: 0 var(--space-md);
    background: var(--bg-tertiary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-primary);
    font-size: 13px;
    cursor: pointer;
}}

.filter-group select:focus {{
    outline: none;
    border-color: var(--accent-primary);
}}

/* Item List */
.item-list-section {{
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}}

.item-list {{
    flex: 1;
    overflow-y: auto;
    padding-right: var(--space-xs);
}}

.item-list::-webkit-scrollbar {{ width: 6px; }}
.item-list::-webkit-scrollbar-track {{ background: transparent; }}
.item-list::-webkit-scrollbar-thumb {{ background: var(--border-color); border-radius: 3px; }}

.item-list-empty {{
    text-align: center;
    padding: var(--space-xl);
    color: var(--text-muted);
}}

.item-list-empty .hint {{
    font-size: 12px;
    margin-top: var(--space-xs);
}}

/* Item Card */
.item-card {{
    padding: var(--space-md);
    background: var(--bg-tertiary);
    border-radius: var(--radius-md);
    margin-bottom: var(--space-sm);
    cursor: pointer;
    transition: var(--transition-fast);
    border: 1px solid transparent;
}}

.item-card:hover {{
    border-color: var(--accent-primary);
    transform: translateX(4px);
}}

.item-card.selected {{
    border-color: var(--accent-secondary);
    background: rgba(6, 182, 212, 0.1);
}}

.item-card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-sm);
}}

.item-title {{
    font-weight: 600;
    font-size: 15px;
    color: var(--accent-secondary);
}}

.item-badge {{
    font-size: 12px;
    color: var(--text-secondary);
    background: var(--bg-card);
    padding: 2px 8px;
    border-radius: var(--radius-full);
}}

.item-card-body {{
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    color: var(--text-muted);
}}

/* =============================================================================
   DETAIL PANEL
   ============================================================================= */

#detail-panel {{
    position: fixed;
    bottom: 0;
    left: 0;
    right: var(--sidebar-width);
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border-top: 1px solid var(--border-color);
    padding: var(--space-lg);
    transform: translateY(100%);
    transition: var(--transition-smooth);
    z-index: 800;
}}

#detail-panel:not(.hidden) {{
    transform: translateY(0);
}}

.close-btn {{
    position: absolute;
    top: var(--space-md);
    right: var(--space-md);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 1px solid var(--border-color);
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    font-size: 20px;
    cursor: pointer;
    transition: var(--transition-fast);
}}

.close-btn:hover {{
    background: var(--accent-error);
    color: white;
    border-color: var(--accent-error);
}}

.detail-header {{
    margin-bottom: var(--space-lg);
}}

.detail-title {{
    font-size: 28px;
    font-weight: 700;
    color: var(--accent-secondary);
    margin-bottom: var(--space-xs);
}}

.detail-subtitle {{
    font-size: 16px;
    color: var(--text-secondary);
}}

.detail-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-md);
    margin-bottom: var(--space-lg);
}}

.detail-item {{
    background: var(--bg-tertiary);
    padding: var(--space-md);
    border-radius: var(--radius-md);
}}

.detail-item.wide {{
    grid-column: span 2;
}}

.detail-label {{
    display: block;
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: var(--space-xs);
}}

.detail-value {{
    font-size: 18px;
    font-weight: 600;
    color: var(--text-primary);
}}

.btn-track {{
    padding: var(--space-md) var(--space-xl);
}}

/* =============================================================================
   TOAST NOTIFICATIONS
   ============================================================================= */

#toast-container {{
    position: fixed;
    bottom: var(--space-lg);
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    gap: var(--space-sm);
    z-index: 9999;
}}

.toast {{
    padding: var(--space-md) var(--space-lg);
    background: var(--bg-card);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    color: var(--text-primary);
    font-size: 14px;
    box-shadow: var(--shadow-lg);
    animation: slideUp 0.3s ease;
}}

.toast.success {{ border-color: var(--accent-success); background: rgba(16, 185, 129, 0.2); }}
.toast.error {{ border-color: var(--accent-error); background: rgba(239, 68, 68, 0.2); }}

@keyframes slideUp {{
    from {{ transform: translateY(20px); opacity: 0; }}
}}

/* =============================================================================
   MARKERS
   ============================================================================= */

.marker-icon {{
    font-size: 24px;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.5));
    transition: transform 0.5s ease;
}}

.marker-icon.ground {{ color: var(--accent-warning); opacity: 0.7; }}
.marker-icon.low {{ color: var(--accent-success); }}
.marker-icon.mid {{ color: var(--accent-primary); }}
.marker-icon.high {{ color: #8b5cf6; }}

/* =============================================================================
   RESPONSIVE
   ============================================================================= */

@media (max-width: 768px) {{
    #sidebar {{
        position: fixed;
        top: var(--header-height);
        right: 0;
        bottom: 0;
        width: 100%;
        max-width: 320px;
        transform: translateX(100%);
        transition: var(--transition-smooth);
        z-index: 900;
    }}
    
    #sidebar.open {{ transform: translateX(0); }}
    #detail-panel {{ right: 0; }}
    .detail-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

/* =============================================================================
   UTILITIES
   ============================================================================= */

.hidden {{ display: none !important; }}
'''


# =============================================================================
# JAVASCRIPT TEMPLATES
# =============================================================================

def generate_map_js(
    app_name: str,
    api_type: str,
    regions: List[str],
    default_region: str = 'world',
    refresh_interval: int = 15000
) -> str:
    """Generate JavaScript for a map-based tracker application."""
    
    # Generate regions config
    region_items = []
    for key in regions:
        if key in REGIONS:
            r = REGIONS[key]
            bounds_str = str(r['bounds']) if r['bounds'] else 'null'
            center_str = str(r['center'])
            region_items.append(f"'{key}': {{ name: '{r['name']}', bounds: {bounds_str}, center: {center_str}, zoom: {r['zoom']} }}")
    regions_config = ',\n    '.join(region_items)
    
    api_code = _generate_opensky_api() if api_type == 'opensky' else _generate_generic_api()
    
    return f'''/**
 * {app_name.replace('_', ' ').title()} - Grown by Autopoiesis
 * {"=" * (len(app_name) + 32)}
 *
 * LJPW Principles Applied:
 * - Love: Comprehensive documentation, helpful comments
 * - Justice: Input validation, fair error handling
 * - Power: Resilient API calls, graceful degradation
 * - Wisdom: Logging, status indicators, observability
 *
 * Generated: {datetime.now().isoformat()}
 */

// =============================================================================
// CONFIGURATION (Love: documented, Justice: validated)
// =============================================================================

const CONFIG = {{
    api: {{
        baseUrl: 'https://opensky-network.org/api',
        refreshInterval: {refresh_interval},
        timeout: 10000
    }},
    map: {{
        defaultRegion: '{default_region}',
        tileLayer: 'https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png',
        attribution: '&copy; OpenStreetMap &copy; CARTO'
    }},
    regions: {{
    {regions_config}
    }}
}};

// =============================================================================
// STATE (Wisdom: centralized, observable)
// =============================================================================

const state = {{
    map: null,
    items: new Map(),
    markers: new Map(),
    selectedItem: null,
    trackedItem: null,
    lastUpdate: null,
    isLoading: false,
    refreshTimer: null,
    currentRegion: '{default_region}'
}};

// =============================================================================
// UTILITY FUNCTIONS (Love: well-documented)
// =============================================================================

/**
 * Format altitude in feet with thousands separator.
 * @param {{number}} meters - Altitude in meters
 * @returns {{string}} Formatted altitude
 */
function formatAltitude(meters) {{
    if (meters === null || meters === undefined) return 'N/A';
    const feet = Math.round(meters * 3.28084);
    return feet.toLocaleString() + ' ft';
}}

/**
 * Format speed in knots.
 * @param {{number}} ms - Speed in m/s
 * @returns {{string}} Formatted speed
 */
function formatSpeed(ms) {{
    if (ms === null || ms === undefined) return 'N/A';
    const knots = Math.round(ms * 1.94384);
    return knots + ' kts';
}}

/**
 * Format heading with compass direction.
 * @param {{number}} degrees - Heading in degrees
 * @returns {{string}} Formatted heading
 */
function formatHeading(degrees) {{
    if (degrees === null || degrees === undefined) return 'N/A';
    const dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
    const idx = Math.round(degrees / 45) % 8;
    return Math.round(degrees) + '° ' + dirs[idx];
}}

/**
 * Get altitude category for styling.
 * @param {{number}} meters - Altitude in meters
 * @returns {{string}} Category: ground, low, mid, high
 */
function getAltitudeCategory(meters) {{
    if (meters === null || meters === undefined || meters < 100) return 'ground';
    const feet = meters * 3.28084;
    if (feet < 10000) return 'low';
    if (feet < 30000) return 'mid';
    return 'high';
}}

/**
 * Format time as HH:MM:SS.
 * @param {{Date}} date - Date object
 * @returns {{string}} Formatted time
 */
function formatTime(date) {{
    return date.toLocaleTimeString('en-US', {{ hour12: false }});
}}

/**
 * Show a toast notification.
 * @param {{string}} message - Message to show
 * @param {{string}} type - Type: success, error, info
 */
function showToast(message, type = 'info') {{
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${{type}}`;
    toast.textContent = message;
    container.appendChild(toast);
    
    setTimeout(() => {{
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }}, 4000);
    
    console.log(`[Toast:${{type}}] ${{message}}`);
}}

/**
 * Log with timestamp for debugging (Wisdom).
 * @param {{string}} context - Context/module name
 * @param {{string}} message - Log message
 */
function log(context, message) {{
    console.log(`[${{formatTime(new Date())}}] [${{context}}] ${{message}}`);
}}

{api_code}

// =============================================================================
// MAP FUNCTIONS
// =============================================================================

/**
 * Initialize Leaflet map.
 */
function initMap() {{
    log('Map', 'Initializing...');
    
    const region = CONFIG.regions[state.currentRegion];
    
    state.map = L.map('map', {{
        center: region.center,
        zoom: region.zoom,
        zoomControl: false,
        attributionControl: true
    }});
    
    L.tileLayer(CONFIG.map.tileLayer, {{
        attribution: CONFIG.map.attribution,
        maxZoom: 18
    }}).addTo(state.map);
    
    L.control.zoom({{ position: 'topleft' }}).addTo(state.map);
    
    state.map.on('moveend', updateItemList);
    state.map.on('zoomend', updateItemList);
    
    log('Map', 'Initialized');
}}

/**
 * Create marker icon.
 * @param {{object}} item - Item data
 * @returns {{L.DivIcon}} Leaflet icon
 */
function createMarkerIcon(item) {{
    const category = getAltitudeCategory(item.altitude);
    const rotation = item.heading || 0;
    
    return L.divIcon({{
        className: 'marker-container',
        html: `<div class="marker-icon ${{category}}" style="transform: rotate(${{rotation}}deg)">✈</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
    }});
}}

/**
 * Update markers on the map.
 * @param {{Array}} items - Array of item data
 */
function updateMarkers(items) {{
    const currentIds = new Set(items.map(i => i.id));
    
    // Remove old markers
    for (const [id, marker] of state.markers) {{
        if (!currentIds.has(id)) {{
            state.map.removeLayer(marker);
            state.markers.delete(id);
        }}
    }}
    
    // Update or create markers
    for (const item of items) {{
        state.items.set(item.id, item);
        
        if (state.markers.has(item.id)) {{
            const marker = state.markers.get(item.id);
            marker.setLatLng([item.latitude, item.longitude]);
            marker.setIcon(createMarkerIcon(item));
        }} else {{
            const marker = L.marker([item.latitude, item.longitude], {{
                icon: createMarkerIcon(item)
            }});
            marker.on('click', () => selectItem(item.id));
            marker.addTo(state.map);
            state.markers.set(item.id, marker);
        }}
    }}
    
    log('Map', `Updated ${{items.length}} markers`);
}}

/**
 * Center map on an item.
 * @param {{string}} id - Item ID
 */
function centerOnItem(id) {{
    const item = state.items.get(id);
    if (item) {{
        state.map.setView([item.latitude, item.longitude], 8, {{ animate: true }});
    }}
}}

// =============================================================================
// UI FUNCTIONS
// =============================================================================

/**
 * Update the item list in sidebar.
 */
function updateItemList() {{
    const listEl = document.getElementById('item-list');
    const countEl = document.getElementById('item-count');
    const bounds = state.map.getBounds();
    
    const visible = Array.from(state.items.values())
        .filter(i => bounds.contains([i.latitude, i.longitude]))
        .sort((a, b) => (b.altitude || 0) - (a.altitude || 0))
        .slice(0, 50);
    
    countEl.textContent = `(${{visible.length}})`;
    
    if (visible.length === 0) {{
        listEl.innerHTML = `
            <div class="item-list-empty">
                <p>No items in current view</p>
                <p class="hint">Zoom out or change region</p>
            </div>
        `;
        return;
    }}
    
    listEl.innerHTML = visible.map(item => `
        <div class="item-card ${{state.selectedItem === item.id ? 'selected' : ''}}" data-id="${{item.id}}">
            <div class="item-card-header">
                <span class="item-title">${{item.callsign || item.id}}</span>
                <span class="item-badge">${{formatAltitude(item.altitude)}}</span>
            </div>
            <div class="item-card-body">
                <span>⟳ ${{formatSpeed(item.velocity)}}</span>
                <span>↑ ${{formatHeading(item.heading)}}</span>
            </div>
        </div>
    `).join('');
    
    listEl.querySelectorAll('.item-card').forEach(card => {{
        card.addEventListener('click', () => selectItem(card.dataset.id));
    }});
}}

/**
 * Select an item and show detail panel.
 * @param {{string}} id - Item ID
 */
function selectItem(id) {{
    const item = state.items.get(id);
    if (!item) return;
    
    state.selectedItem = id;
    
    document.querySelectorAll('.item-card').forEach(card => {{
        card.classList.toggle('selected', card.dataset.id === id);
    }});
    
    const panel = document.getElementById('detail-panel');
    panel.classList.remove('hidden');
    
    document.getElementById('detail-title').textContent = item.callsign || item.id;
    document.getElementById('detail-subtitle').textContent = item.originCountry || '--';
    
    document.getElementById('detail-grid').innerHTML = `
        <div class="detail-item">
            <span class="detail-label">Altitude</span>
            <span class="detail-value">${{formatAltitude(item.altitude)}}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Speed</span>
            <span class="detail-value">${{formatSpeed(item.velocity)}}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Heading</span>
            <span class="detail-value">${{formatHeading(item.heading)}}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">On Ground</span>
            <span class="detail-value">${{item.onGround ? 'Yes' : 'No'}}</span>
        </div>
    `;
    
    centerOnItem(id);
    log('UI', `Selected: ${{item.callsign || id}}`);
}}

/**
 * Close detail panel.
 */
function closeDetail() {{
    document.getElementById('detail-panel').classList.add('hidden');
    state.selectedItem = null;
    document.querySelectorAll('.item-card').forEach(c => c.classList.remove('selected'));
}}

/**
 * Update status indicator.
 * @param {{string}} status - connected, connecting, error
 * @param {{string}} message - Status message
 */
function updateStatus(status, message) {{
    const dot = document.getElementById('api-status');
    const text = document.getElementById('api-status-text');
    dot.className = 'status-dot ' + status;
    text.textContent = message;
}}

/**
 * Show/hide loading overlay.
 * @param {{boolean}} show - Whether to show
 */
function setLoading(show) {{
    document.getElementById('map-loading').classList.toggle('hidden', !show);
    state.isLoading = show;
}}

// =============================================================================
// DATA REFRESH
// =============================================================================

/**
 * Refresh data from API.
 */
async function refreshData() {{
    if (state.isLoading) return;
    
    setLoading(true);
    updateStatus('', 'Updating...');
    
    try {{
        const bounds = state.map.getBounds();
        const params = {{
            south: bounds.getSouth(),
            north: bounds.getNorth(),
            west: bounds.getWest(),
            east: bounds.getEast()
        }};
        
        const items = await fetchData(params);
        
        updateMarkers(items);
        updateItemList();
        
        document.getElementById('total-count').textContent = items.length.toLocaleString();
        document.getElementById('update-time').textContent = formatTime(new Date());
        state.lastUpdate = new Date();
        
        updateStatus('connected', 'Live');
        
        if (state.trackedItem && state.items.has(state.trackedItem)) {{
            centerOnItem(state.trackedItem);
        }}
        
    }} catch (error) {{
        updateStatus('error', 'Error');
        showToast(error.message, 'error');
    }} finally {{
        setLoading(false);
    }}
}}

/**
 * Start auto-refresh timer.
 */
function startAutoRefresh() {{
    if (state.refreshTimer) clearInterval(state.refreshTimer);
    state.refreshTimer = setInterval(refreshData, CONFIG.api.refreshInterval);
    log('Refresh', `Auto-refresh started: ${{CONFIG.api.refreshInterval / 1000}}s`);
}}

// =============================================================================
// FILTERS
// =============================================================================

/**
 * Apply region filter.
 * @param {{string}} region - Region key
 */
function applyRegion(region) {{
    const r = CONFIG.regions[region];
    if (!r) return;
    
    state.currentRegion = region;
    
    if (r.bounds) {{
        state.map.fitBounds(r.bounds, {{ padding: [20, 20] }});
    }} else {{
        state.map.setView(r.center, r.zoom);
    }}
    
    setTimeout(refreshData, 500);
    log('Filter', `Region: ${{region}}`);
}}

/**
 * Search for items.
 * @param {{string}} query - Search query
 */
function search(query) {{
    if (!query) {{
        updateItemList();
        return;
    }}
    
    query = query.toUpperCase();
    
    for (const [id, item] of state.items) {{
        const callsign = (item.callsign || '').toUpperCase();
        const itemId = id.toUpperCase();
        
        if (callsign.includes(query) || itemId.includes(query)) {{
            selectItem(id);
            showToast(`Found: ${{item.callsign || id}}`, 'success');
            return;
        }}
    }}
    
    showToast(`No results for "${{query}}"`, 'error');
}}

// =============================================================================
// EVENT LISTENERS
// =============================================================================

/**
 * Initialize event listeners.
 */
function initEvents() {{
    log('Events', 'Initializing...');
    
    document.getElementById('btn-refresh').addEventListener('click', refreshData);
    
    document.getElementById('btn-center').addEventListener('click', () => {{
        if (state.selectedItem) {{
            centerOnItem(state.selectedItem);
        }} else {{
            const r = CONFIG.regions[state.currentRegion];
            state.map.setView(r.center, r.zoom);
        }}
    }});
    
    document.getElementById('btn-fullscreen').addEventListener('click', () => {{
        if (document.fullscreenElement) {{
            document.exitFullscreen();
        }} else {{
            document.documentElement.requestFullscreen();
        }}
    }});
    
    document.getElementById('close-detail').addEventListener('click', closeDetail);
    
    document.getElementById('btn-track').addEventListener('click', () => {{
        if (state.selectedItem) {{
            state.trackedItem = state.trackedItem === state.selectedItem ? null : state.selectedItem;
            document.getElementById('btn-track').textContent = state.trackedItem ? 'Stop Tracking' : 'Track';
            if (state.trackedItem) showToast('Tracking enabled', 'success');
        }}
    }});
    
    document.getElementById('filter-region').addEventListener('change', (e) => {{
        applyRegion(e.target.value);
    }});
    
    document.getElementById('search-btn')?.addEventListener('click', () => {{
        search(document.getElementById('search-input').value);
    }});
    
    document.getElementById('search-input')?.addEventListener('keypress', (e) => {{
        if (e.key === 'Enter') search(e.target.value);
    }});
    
    document.addEventListener('keydown', (e) => {{
        if (e.key === 'Escape') closeDetail();
        if (e.key === 'r' && e.ctrlKey) {{ e.preventDefault(); refreshData(); }}
    }});
    
    log('Events', 'Initialized');
}}

// =============================================================================
// INITIALIZATION
// =============================================================================

/**
 * Main initialization.
 */
async function init() {{
    log('App', 'Starting...');
    
    try {{
        initMap();
        initEvents();
        await refreshData();
        startAutoRefresh();
        
        log('App', 'Ready');
        showToast('Application ready', 'success');
        
    }} catch (error) {{
        log('App', `Error: ${{error.message}}`);
        updateStatus('error', 'Failed');
        showToast('Initialization failed: ' + error.message, 'error');
        setLoading(false);
    }}
}}

// Start
init();
'''


def _generate_opensky_api() -> str:
    """Generate OpenSky API code."""
    return '''
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
'''


def _generate_generic_api() -> str:
    """Generate generic API code."""
    return '''
// =============================================================================
// API: Generic (Power: resilient, Justice: validated)
// =============================================================================

/**
 * Fetch data from API.
 * @param {object} bounds - Map bounds
 * @returns {Promise<Array>} Data array
 */
async function fetchData(bounds) {
    log('API', 'Fetching data...');
    
    // Placeholder - replace with actual API
    return [
        { id: 'demo1', callsign: 'DEMO001', latitude: 0, longitude: 0, altitude: 10000, velocity: 250, heading: 90 }
    ];
}
'''
