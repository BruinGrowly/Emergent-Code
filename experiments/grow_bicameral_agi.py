"""
Experiment: Grow Bicameral AGI Architecture
Intent: Create a self-improving AGI system that uses both Physics Resonance (Left Brain) and Neural Homeostasis (Right Brain).
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_grower import ResonanceGrower

def main():
    print("🧠 GROWING BICAMERAL AGI BLUEPRINT...")
    
    grower = ResonanceGrower()
    
    intent = "Create a self-improving AGI system that uses both Physics Resonance and Neural Homeostasis"
    context = "Advanced Research, Integration of two existing frameworks, High Autonomy"
    
    # 1. Get the Physics Profile
    profile = grower.determine_target_profile(intent, context)
    
    print("\n--- RESONANCE PROFILE ---")
    print(f"L: {profile['L']:.3f} (Connectivity)")
    print(f"J: {profile['J']:.3f} (Alignment)")
    print(f"P: {profile['P']:.3f} (Capacity)")
    print(f"W: {profile['W']:.3f} (Insight)")
    print(f"Deficit: {profile['Deficit']}")
    
    # 2. Generate the Blueprint
    blueprint = grower.generate_blueprint(intent, context)
    
    # 3. Save Blueprint
    output_path = os.path.join("docs", "BICAMERAL_AGI_BLUEPRINT.md")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(blueprint)
        
    print(f"\n✅ Blueprint grown: {output_path}")
    print(blueprint)

if __name__ == "__main__":
    main()

