#!/usr/bin/env python3
"""
Test: Grow a Particle System from Natural Language
===================================================

This demonstrates TRUE growing - the web_grower module creates
a complete 3D particle system from a natural language description.
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
|   GROWING 3D PARTICLE SYSTEM FROM NATURAL LANGUAGE                           |
|                                                                              |
|   This is TRUE autopoietic growth - intent becomes working code.            |
|                                                                              |
+==============================================================================+
    """)
    
    # The user's original intent
    intent = """
    Create a real-time interactive beautiful 3D particle system with Three.js.
    Requirements:
    1. Control the scaling and expansion of the particle group by detecting 
       the tension and closing of both hands through the camera.
    2. Provide panels that can choose hearts, spheres, spirals, cubes, rings,
       and explosions as shape templates.
    3. Support the color selector to adjust the particle color.
    4. Particles need to respond to gesture changes in real time.
    5. The interface is simple and modern.
    """
    
    # Grow the application
    output_dir = os.path.join(project_root, "generated")
    os.makedirs(output_dir, exist_ok=True)
    
    app = grow_web_app(intent, output_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("  GROWTH SUMMARY")
    print("=" * 60)
    
    print(f"\n  App Type: {app.app_type}")
    print(f"  Output Path: {app.path}")
    print(f"  Features: {', '.join(app.features)}")
    
    print(f"\n  Generated Files:")
    total_bytes = 0
    for filename, content in app.files.items():
        size = len(content)
        total_bytes += size
        print(f"    - {filename}: {size:,} bytes")
    
    print(f"\n  Total: {total_bytes:,} bytes of LJPW-balanced code")
    
    print(f"""
  
  To view the application:
    cd {app.path}
    python -m http.server 8081
    Open: http://localhost:8081
    
    """)


if __name__ == "__main__":
    main()
