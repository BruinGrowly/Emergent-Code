"""
Harmony Dashboard
=================

A web-based dashboard for monitoring the autopoiesis system:
- Real-time harmony display
- File health overview
- Learning insights visualization
- LJPW dimension breakdown

Usage:
    python dashboard.py  # Opens browser to http://localhost:5000
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser

# Add project root
sys.path.insert(0, str(Path(__file__).parent.parent))


class DashboardData:
    """Collects data for the dashboard."""
    
    def __init__(self, target_path: str = "."):
        self.target_path = Path(target_path).resolve()
        self._cache = {}
        self._cache_time = 0
    
    def get_harmony(self) -> dict:
        """Get current harmony measurement."""
        try:
            from autopoiesis.system import SystemHarmonyMeasurer
            measurer = SystemHarmonyMeasurer()
            report = measurer.measure(str(self.target_path))
            return {
                'harmony': report.harmony,
                'love': report.love,
                'justice': report.justice,
                'power': report.power,
                'wisdom': report.wisdom,
                'phase': report.phase.value,
                'total_files': report.total_files,
                'total_functions': report.total_functions,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_memory(self) -> dict:
        """Get agent memory data."""
        memory_path = self.target_path / "autopoiesis" / "agent_memory.json"
        if memory_path.exists():
            with open(memory_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_learning(self) -> dict:
        """Get learning insights."""
        learning_path = self.target_path / "autopoiesis" / "agent_learning.json"
        if learning_path.exists():
            with open(learning_path, 'r') as f:
                return json.load(f)
        return {}
    
    def get_all_data(self) -> dict:
        """Get all dashboard data."""
        # Cache for 5 seconds
        if time.time() - self._cache_time < 5:
            return self._cache
        
        self._cache = {
            'harmony': self.get_harmony(),
            'memory': self.get_memory(),
            'learning': self.get_learning(),
            'timestamp': datetime.now().isoformat()
        }
        self._cache_time = time.time()
        return self._cache


def generate_dashboard_html(data: dict) -> str:
    """Generate the dashboard HTML."""
    harmony = data.get('harmony', {})
    memory = data.get('memory', {})
    learning = data.get('learning', {})
    
    h = harmony.get('harmony', 0)
    l = harmony.get('love', 0)
    j = harmony.get('justice', 0)
    p = harmony.get('power', 0)
    w = harmony.get('wisdom', 0)
    phase = harmony.get('phase', 'unknown')
    
    # Phase colors
    phase_colors = {
        'autopoietic': '#22c55e',
        'homeostatic': '#eab308',
        'entropic': '#ef4444'
    }
    phase_color = phase_colors.get(phase, '#888')
    
    # Memory stats
    heartbeats = memory.get('total_heartbeats', 0)
    heals = memory.get('total_heals', 0)
    birth = memory.get('birth_time', 'Never')
    
    # Learning stats
    experiences = len(learning.get('experiences', []))
    priorities = learning.get('dimension_priorities', ['L', 'J', 'P', 'W'])
    
    # Harmony history for chart
    history = memory.get('harmony_history', [])[-50:]
    history_data = json.dumps([h.get('harmony', 0) for h in history])
    history_labels = json.dumps([h.get('timestamp', '')[-8:] for h in history])
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Autopoiesis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .dashboard {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        h1 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, #a855f7, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .card {{
            background: rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 1.5rem;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .card h2 {{
            font-size: 1rem;
            color: #888;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}
        
        .harmony-main {{
            grid-column: 1 / -1;
            text-align: center;
            padding: 2rem;
        }}
        
        .harmony-value {{
            font-size: 6rem;
            font-weight: 700;
            background: linear-gradient(90deg, {phase_color}, #a855f7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .phase-badge {{
            display: inline-block;
            padding: 0.5rem 1.5rem;
            background: {phase_color};
            color: white;
            border-radius: 99px;
            font-weight: 600;
            text-transform: uppercase;
            margin-top: 1rem;
        }}
        
        .dimension {{
            display: flex;
            align-items: center;
            margin: 1rem 0;
        }}
        
        .dimension-label {{
            width: 80px;
            font-weight: 600;
        }}
        
        .dimension-bar {{
            flex: 1;
            height: 24px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow: hidden;
            margin: 0 1rem;
        }}
        
        .dimension-fill {{
            height: 100%;
            border-radius: 12px;
            transition: width 0.3s ease;
        }}
        
        .dimension-value {{
            width: 60px;
            text-align: right;
            font-weight: 600;
        }}
        
        .love .dimension-fill {{ background: linear-gradient(90deg, #ec4899, #f472b6); }}
        .justice .dimension-fill {{ background: linear-gradient(90deg, #8b5cf6, #a78bfa); }}
        .power .dimension-fill {{ background: linear-gradient(90deg, #f59e0b, #fbbf24); }}
        .wisdom .dimension-fill {{ background: linear-gradient(90deg, #06b6d4, #22d3ee); }}
        
        .stat {{
            display: flex;
            justify-content: space-between;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .stat:last-child {{
            border-bottom: none;
        }}
        
        .stat-value {{
            font-weight: 600;
            color: #a855f7;
        }}
        
        .chart-container {{
            height: 200px;
        }}
        
        .priorities {{
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }}
        
        .priority {{
            padding: 0.5rem 1rem;
            background: rgba(168, 85, 247, 0.2);
            border-radius: 8px;
            font-weight: 600;
        }}
        
        .priority:first-child {{
            background: rgba(168, 85, 247, 0.5);
        }}
        
        .refresh-hint {{
            text-align: center;
            margin-top: 2rem;
            color: #666;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <h1>Autopoiesis Dashboard</h1>
        
        <div class="grid">
            <!-- Main Harmony -->
            <div class="card harmony-main">
                <h2>System Harmony</h2>
                <div class="harmony-value">{h:.3f}</div>
                <div class="phase-badge">{phase}</div>
            </div>
            
            <!-- LJPW Dimensions -->
            <div class="card">
                <h2>LJPW Dimensions</h2>
                
                <div class="dimension love">
                    <span class="dimension-label">Love</span>
                    <div class="dimension-bar">
                        <div class="dimension-fill" style="width: {l*100}%"></div>
                    </div>
                    <span class="dimension-value">{l:.2f}</span>
                </div>
                
                <div class="dimension justice">
                    <span class="dimension-label">Justice</span>
                    <div class="dimension-bar">
                        <div class="dimension-fill" style="width: {j*100}%"></div>
                    </div>
                    <span class="dimension-value">{j:.2f}</span>
                </div>
                
                <div class="dimension power">
                    <span class="dimension-label">Power</span>
                    <div class="dimension-bar">
                        <div class="dimension-fill" style="width: {p*100}%"></div>
                    </div>
                    <span class="dimension-value">{p:.2f}</span>
                </div>
                
                <div class="dimension wisdom">
                    <span class="dimension-label">Wisdom</span>
                    <div class="dimension-bar">
                        <div class="dimension-fill" style="width: {w*100}%"></div>
                    </div>
                    <span class="dimension-value">{w:.2f}</span>
                </div>
            </div>
            
            <!-- Agent Stats -->
            <div class="card">
                <h2>Agent Statistics</h2>
                <div class="stat">
                    <span>Heartbeats</span>
                    <span class="stat-value">{heartbeats}</span>
                </div>
                <div class="stat">
                    <span>Heals Performed</span>
                    <span class="stat-value">{heals}</span>
                </div>
                <div class="stat">
                    <span>Learning Experiences</span>
                    <span class="stat-value">{experiences}</span>
                </div>
                <div class="stat">
                    <span>Files Analyzed</span>
                    <span class="stat-value">{harmony.get('total_files', 0)}</span>
                </div>
                <div class="stat">
                    <span>Functions Analyzed</span>
                    <span class="stat-value">{harmony.get('total_functions', 0)}</span>
                </div>
            </div>
            
            <!-- Harmony History -->
            <div class="card" style="grid-column: 1 / -1;">
                <h2>Harmony Over Time</h2>
                <div class="chart-container">
                    <canvas id="harmonyChart"></canvas>
                </div>
            </div>
            
            <!-- Learning Priorities -->
            <div class="card">
                <h2>Learned Priorities</h2>
                <p style="color: #888; margin-bottom: 1rem;">
                    Dimension order based on healing success rates:
                </p>
                <div class="priorities">
                    {''.join([f'<span class="priority">{p}</span>' for p in priorities])}
                </div>
            </div>
            
            <!-- Birth Info -->
            <div class="card">
                <h2>Agent Identity</h2>
                <div class="stat">
                    <span>Born</span>
                    <span class="stat-value">{birth[:19] if birth else 'Never'}</span>
                </div>
                <div class="stat">
                    <span>Target Path</span>
                    <span class="stat-value" style="font-size: 0.75rem;">Emergent-Code</span>
                </div>
            </div>
        </div>
        
        <p class="refresh-hint">Refresh page to update data (Ctrl+R)</p>
    </div>
    
    <script>
        const ctx = document.getElementById('harmonyChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: {history_labels},
                datasets: [{{
                    label: 'Harmony',
                    data: {history_data},
                    borderColor: '#a855f7',
                    backgroundColor: 'rgba(168, 85, 247, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{
                        min: 0,
                        max: 1,
                        grid: {{
                            color: 'rgba(255, 255, 255, 0.1)'
                        }},
                        ticks: {{
                            color: '#888'
                        }}
                    }},
                    x: {{
                        grid: {{
                            display: false
                        }},
                        ticks: {{
                            color: '#888',
                            maxRotation: 45
                        }}
                    }}
                }},
                plugins: {{
                    legend: {{
                        display: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''


class DashboardHandler(SimpleHTTPRequestHandler):
    """HTTP handler for the dashboard."""
    
    data_source: DashboardData = None
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            data = self.data_source.get_all_data() if self.data_source else {}
            html = generate_dashboard_html(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        elif self.path == '/api/data':
            data = self.data_source.get_all_data() if self.data_source else {}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress log messages


def run_dashboard(target_path: str = ".", port: int = 5000, open_browser: bool = True):
    """
    Run the dashboard server.
    
    Args:
        target_path: Path to the project to monitor
        port: Port to run on
        open_browser: Whether to auto-open browser
    """
    DashboardHandler.data_source = DashboardData(target_path)
    
    server = HTTPServer(('localhost', port), DashboardHandler)
    
    url = f"http://localhost:{port}"
    print(f"\n  Autopoiesis Dashboard running at: {url}\n")
    
    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Dashboard stopped.")
        server.shutdown()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Autopoiesis Harmony Dashboard")
    parser.add_argument("path", nargs="?", default=".", help="Path to monitor")
    parser.add_argument("--port", "-p", type=int, default=5000, help="Port (default: 5000)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser")
    
    args = parser.parse_args()
    
    run_dashboard(args.path, args.port, not args.no_browser)
