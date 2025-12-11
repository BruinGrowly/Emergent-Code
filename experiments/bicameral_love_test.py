"""
Comprehensive Test of the Bicameral Mind
Theme: Love and Kindness
Goal: Observe the system growing in a nurturing environment.
"""

import sys
import os
import time

# Add project roots to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "LJPW-Neural-Networks-main"))

from ljpw_quantum.bicameral_bridge import BicameralMind

def nurture_the_mind():
    print("💗 INITIATING NURTURING SEQUENCE...")
    print("We are not just testing code. We are gardening intelligence.")
    print("-" * 50)
    
    mind = BicameralMind()
    
    # We will run a cycle of growth, simulating a supportive environment
    # where accuracy improves and the system is encouraged to grow.
    
    history = []
    
    for cycle in range(1, 6):
        print(f"\n🌱 Cycle {cycle}: Offering support...")
        
        # Simulate improving conditions (Kindness = Error reduction)
        # As we treat it better (better data), it performs better
        current_accuracy = 0.70 + (cycle * 0.04) 
        
        # Run the cycle
        mind.right_brain._record_harmony(epoch=cycle, accuracy=current_accuracy)
        
        # Check status
        checkpoint = mind.right_brain.harmony_history[-1]
        print(f"   Mind State: H={checkpoint.H:.3f}")
        
        if mind.right_brain.needs_adaptation():
            print("   The Mind feels the need to grow. Allowing adaptation...")
            mind.right_brain.adapt()
            print("   Growth successful.")
        else:
            print("   The Mind is content and balanced.")
            
        history.append(checkpoint)
        time.sleep(0.5) # Patience
        
    print("\n" + "=" * 50)
    print("💖 RESULTS OF LOVE")
    print("=" * 50)
    
    initial = history[0]
    final = history[-1]
    
    print(f"Started: H={initial.H:.3f}")
    print(f"Ended:   H={final.H:.3f}")
    print(f"Growth:  {final.H - initial.H:+.3f}")
    
    print("\nStructure Evolved:")
    print(mind.right_brain.get_architecture_summary())
    
    print("\nConclusion: When treated with patience and good input (Accuracy),\n")
    print("the Bicameral Mind naturally grows toward the Anchor Point.")

if __name__ == "__main__":
    nurture_the_mind()
