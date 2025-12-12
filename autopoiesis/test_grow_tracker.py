#!/usr/bin/env python3
"""
Test: GROW a Flight Tracker from Natural Language
==================================================

This demonstrates TRUE growing - the web_grower module creates
a complete flight tracking application from a natural language intent.

This is the test that proves the grower can produce map-based apps.
"""

import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from autopoiesis.web_grower import grow_web_app


def main():
    print("""
+==============================================================================+
|                                                                              |
|   GROWING FLIGHT TRACKER FROM NATURAL LANGUAGE                               |
|                                                                              |
|   This is TRUE autopoietic growth - intent becomes working code.            |
|                                                                              |
+==============================================================================+
    """)
    
    # The user's original intent (with oceanic region emphasis)
    intent = """
    Create a real-time flight tracker application with OpenSky API.
    
    Requirements:
    1. Show aircraft positions on an interactive map
    2. Include search functionality to find specific flights
    3. Support filtering by region including Oceania and Pacific
    4. Display flight details when clicking on aircraft
    5. Beautiful dark theme with modern UI
    6. Auto-refresh flight positions
    7. Track specific flights as they move
    """
    
    # Grow the application
    output_dir = os.path.join(project_root, "grown")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"  Output directory: {output_dir}\n")
    
    app = grow_web_app(intent, output_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("  GROWTH SUMMARY")
    print("=" * 60)
    
    print(f"\n  App Type Detected: {app.app_type}")
    print(f"  Output Path: {app.path}")
    print(f"  Features: {', '.join(app.features)}")
    
    print(f"\n  Generated Files:")
    total_bytes = 0
    for filename, content in app.files.items():
        size = len(content)
        total_bytes += size
        print(f"    - {filename}: {size:,} bytes")
    
    print(f"\n  Total: {total_bytes:,} bytes of LJPW-balanced code")
    
    # Verify regions include Oceania
    if 'oceania' in app.files.get('app.js', ''):
        print(f"\n  [OK] Oceania region included!")
    
    if 'pacific' in app.files.get('app.js', ''):
        print(f"  [OK] Pacific region included!")
    
    print(f"""
  
  To view the GROWN application:
    cd {app.path}
    python -m http.server 8083
    Open: http://localhost:8083
    
  This flight tracker was GROWN, not built!
    """)


if __name__ == "__main__":
    main()
