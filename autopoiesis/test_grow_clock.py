#!/usr/bin/env python3
"""
Test Auto-Growing a Clock
=========================

This script demonstrates TRUE autopoietic growth:
1. Parse natural language intent
2. Detect app type (should detect 'clock')
3. Generate LJPW-balanced files
4. Save to output directory

Run: python test_grow_clock.py
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from autopoiesis.web_grower import WebIntentParser, WebAppGenerator


def main():
    print("""
+==============================================================================+
|                                                                              |
|   AUTOPOIETIC CLOCK GROWTH TEST                                              |
|                                                                              |
|   Growing a clock from natural language intent...                            |
|                                                                              |
+==============================================================================+
    """)
    
    # The natural language intent
    intent = "Create a beautiful digital and analog clock with LJPW Visual Art Semantics"
    
    print(f"  Intent: {intent}")
    print()
    
    # Step 1: Parse the intent
    print("[STEP 1] Parsing intent...")
    parser = WebIntentParser()
    parsed = parser.parse(intent)
    
    print(f"  App Type Detected: {parsed.app_type}")
    print(f"  Components: {parsed.components}")
    print(f"  Features: {parsed.features}")
    print(f"  Description: {parsed.description}")
    print()
    
    # Step 2: Generate the app
    print("[STEP 2] Generating LJPW-balanced web app...")
    generator = WebAppGenerator()
    files = generator.generate(parsed)
    
    print(f"  Files generated: {list(files.keys())}")
    print()
    
    # Step 3: Save to output directory
    output_dir = os.path.join(project_root, "grown", "auto_clock")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"[STEP 3] Saving to {output_dir}...")
    
    total_bytes = 0
    for filename, content in files.items():
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        size = len(content)
        total_bytes += size
        print(f"  Saved: {filename} ({size:,} bytes)")
    
    print()
    print("=" * 60)
    print("  GROWTH COMPLETE")
    print("=" * 60)
    print(f"""
  Output: {output_dir}
  Total:  {total_bytes:,} bytes of LJPW-balanced code
  
  To view:
    cd {output_dir}
    python -m http.server 8087
    Open: http://localhost:8087
    """)
    
    return output_dir


if __name__ == "__main__":
    main()
