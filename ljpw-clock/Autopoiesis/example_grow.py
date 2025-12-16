#!/usr/bin/env python3
"""
Example: Growing a Clock
========================

This example demonstrates how to use the LJPW Clock Grower
to generate a clock from natural language intent.

Run:
    python example_grow.py
"""

import os
from clock_grower import ClockGrower


def main():
    print("""
+===============================================================+
|                                                               |
|   LJPW CLOCK GROWER - EXAMPLE                                 |
|                                                               |
|   This example grows a clock from natural language intent.    |
|                                                               |
+===============================================================+
    """)
    
    # ==========================================================================
    # STEP 1: Define your intent
    # ==========================================================================
    
    intent = "Create a beautiful digital and analog clock with LJPW Visual Art Semantics"
    
    # You can use simpler intents too:
    # intent = "Make me a clock"
    # intent = "I want a timepiece with a smooth second hand"
    # intent = "Build a minimal clock app"
    
    # ==========================================================================
    # STEP 2: Create the grower
    # ==========================================================================
    
    grower = ClockGrower()
    
    # ==========================================================================
    # STEP 3: Grow the clock
    # ==========================================================================
    
    files = grower.grow(intent)
    
    # ==========================================================================
    # STEP 4: Verify it meets autopoietic threshold
    # ==========================================================================
    
    print()
    is_autopoietic = grower.verify()
    
    # ==========================================================================
    # STEP 5: Save to output folder
    # ==========================================================================
    
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    
    print()
    print(f"[Saving to {output_dir}]")
    grower.save_to(output_dir)
    
    # ==========================================================================
    # DONE!
    # ==========================================================================
    
    print("""
+===============================================================+
|   GROWTH COMPLETE                                             |
|                                                               |
|   Your clock has been grown in the 'output/' folder.          |
|                                                               |
|   To view:                                                    |
|     cd output                                                 |
|     python -m http.server 8080                                |
|     Open http://localhost:8080                                |
|                                                               |
|   Grown, not coded. Happy to be.                              |
+===============================================================+
    """)


if __name__ == "__main__":
    main()
