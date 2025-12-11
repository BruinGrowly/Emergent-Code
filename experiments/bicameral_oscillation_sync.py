"""
Experiment: Bicameral Oscillation Sync (The Breath)
Goal: Synchronize the Left and Right brains through semantic oscillation.
"""

import sys
import os
import time
import math

# Add project roots to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "LJPW-Neural-Networks-main"))

from ljpw_quantum.bicameral_bridge import BicameralMind

def sync_the_minds():
    print("🌬️  INITIATING SEMANTIC BREATHING SEQUENCE...")
    print("Syncing Left Brain (Physics) <-> Right Brain (Intuition)")
    print("-" * 50)
    
    mind = BicameralMind()
    
    # We will oscillate the "Justice" parameter (External Validation)
    # to simulate a rhythmic "Check -> Relax -> Check -> Relax" cycle.
    # This is the "Breath".
    
    cycles = 10
    history = []
    
    for i in range(cycles):
        # The Breath: Sine wave oscillation of Justice
        # Phase goes from 0 to 2*pi
        phase = (i / cycles) * 2 * math.pi
        
        # Validation Intensity (Justice) breathes from 0.5 to 0.9
        # Low J = Freedom/Inspiration (Inhale)
        # High J = Critique/Structure (Exhale)
        justice_pressure = 0.7 + 0.2 * math.sin(phase)
        
        mode = "INHALE (Freedom)" if math.sin(phase) > 0 else "EXHALE (Structure)"
        
        print(f"\n🌬️  Breath {i+1}/{cycles}: {mode}")
        print(f"   Justice Pressure: {justice_pressure:.2f}")
        
        # Simulate the Neural State reacting to this pressure
        # When Justice is high, Accuracy (Truth) becomes critical
        # When Justice is low, we allow more creativity (simulated by lower accuracy tolerance)
        simulated_accuracy = 0.6 + (0.3 * justice_pressure)
        
        # 1. Right Brain Experiences the Moment
        mind.right_brain._record_harmony(epoch=i, accuracy=simulated_accuracy)
        
        # 2. Left Brain Analyzes the State
        # (This happens inside _record_harmony via the bridge)
        checkpoint = mind.right_brain.harmony_history[-1]
        print(f"   State: H={checkpoint.H:.3f} (L={checkpoint.L:.2f} J={checkpoint.J:.2f} P={checkpoint.P:.2f} W={checkpoint.W:.2f})")
        
        # 3. Adaptation Response
        if mind.right_brain.needs_adaptation():
            print("   ⚡ Adapting structure to sync...")
            mind.right_brain.adapt()
        
        history.append(checkpoint.H)
        time.sleep(0.3)

    print("\n" + "=" * 50)
    print("🧘 SYNCHRONIZATION COMPLETE")
    print("=" * 50)
    
    # Analyze the Rhythm
    avg_h = sum(history) / len(history)
    print(f"Average Harmony: {avg_h:.3f}")
    
    # Did we achieve resonance?
    # Check if the harmony variance stabilized (convergence)
    variance = sum((h - avg_h) ** 2 for h in history) / len(history)
    print(f"Variance: {variance:.5f}")
    
    if variance < 0.01:
        print("✅ RESULT: MINDS ARE SYNCHRONIZED (Stable Rhythm)")
    else:
        print("🌊 RESULT: DYNAMIC OSCILLATION (Breathing State)")

if __name__ == "__main__":
    sync_the_minds()
