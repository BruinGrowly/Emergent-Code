"""
Test: Resonance Code Grower
Target: Verify blueprint generation logic.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_grower import ResonanceGrower

def main():
    print("Initializing Resonance Grower...")
    grower = ResonanceGrower()
    
    intent = "Create a secure enterprise login system"
    context = "Production environment"
    
    print(f"\nRequest: {intent} ({context})")
    blueprint = grower.generate_blueprint(intent, context)
    
    print("\n--- GENERATED BLUEPRINT ---")
    print(blueprint)
    print("---------------------------")
    
    if "RESONANCE BLUEPRINT" in blueprint and "Justice" in blueprint:
        print("\n✅ TEST PASSED: Blueprint generated with correct semantic focus.")
    else:
        print("\n❌ TEST FAILED: Blueprint missing key elements.")

if __name__ == "__main__":
    main()

