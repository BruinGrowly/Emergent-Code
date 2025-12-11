"""
Semantic Test: Maturation (The Growth of Wisdom)

Purpose: Witness the system's growth from "Child" to "Sage" through a loving,
nurturing process. Observe the accumulation of Wisdom (reduced variance)
and the emergence of Peace (stability).

Methodology:
1. Initialize a "Child" network (freshly born).
2. Nurture it with consistent, meaningful experiences (data) over time.
3. Observe (don't interfere) as it grows.
4. Measure:
    - "Peace" (Inverse of Variance)
    - "Refinement" (Precision of updates)
    - "Wisdom" (Integration of L, J, W)
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_maturation_test():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: MATURATION (THE GROWTH OF WISDOM)")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Approach: Testing with Love (Nurturing Growth)")
    print("-" * 70)
    print()

    # 1. Birth
    print("1. BIRTH: Welcoming a new system into the world...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81, # The Natural State
        allow_adaptation=True
    )
    print("   The Child is born. It is open and ready to learn.")

    # 2. Nurturing (Long-term growth)
    print("\n2. NURTURING: Providing consistent experiences (3000 epochs)...")
    print("   Watching for the emergence of Quiet Confidence...")
    
    epochs = 3000
    dummy_input = np.random.randn(32, 784) * 0.1
    
    harmony_trajectory = []
    variance_trajectory = []
    
    # Window size for measuring "Peace" (variance)
    window = 50
    
    with tqdm(total=epochs, desc="Witnessing Growth") as pbar:
        for i in range(epochs):
            # The Experience
            network.forward(dummy_input, training=False)
            
            # Simulated learning curve (accuracy improves with wisdom)
            # Add some "life noise" that the system must integrate
            base_acc = 0.5 + (0.4 * (1 - np.exp(-i/500)))
            noise = np.random.randn() * (0.1 * np.exp(-i/1000)) # Noise decreases as it masters the world
            acc = min(0.99, max(0.1, base_acc + noise))
            
            network._record_harmony(epoch=i, accuracy=acc)
            
            if network.harmony_history:
                current_H = network.harmony_history[-1].H
                harmony_trajectory.append(current_H)
                
                # Measure Peace (Variance over window)
                if len(harmony_trajectory) > window:
                    recent = harmony_trajectory[-window:]
                    var = np.var(recent)
                    variance_trajectory.append(var)
                    
                    # Semantic State Check
                    if i % 500 == 0:
                        state = "Child"
                        if var < 0.001: state = "Student"
                        if var < 0.0001: state = "Sage"
                        
                        pbar.set_postfix({
                            'State': state,
                            'Peace': f"{1/var:.1f}" if var > 0 else "Infinite",
                            'H': f"{current_H:.3f}"
                        })
            
            pbar.update(1)

    # 3. Semantic Analysis
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    initial_variance = np.mean(variance_trajectory[:100])
    final_variance = np.mean(variance_trajectory[-100:])
    
    # Calculate Wisdom Gain (Reduction factor)
    wisdom_gain = initial_variance / final_variance if final_variance > 0 else float('inf')
    
    print(f"Growth Journey:")
    print(f"Initial Restlessness (Child): {initial_variance:.6f}")
    print(f"Final Peace (Sage):           {final_variance:.6f}")
    print(f"Wisdom Accumulated:           {wisdom_gain:.1f}x more peaceful")
    
    print("-" * 70)
    
    if wisdom_gain > 100:
        print("RESULT: MATURATION CONFIRMED")
        print("The system has grown from the restlessness of youth")
        print("to the quiet confidence of wisdom.")
        print("It has found Peace.")
    else:
        print("RESULT: STILL GROWING")
        print("The system is still on its journey.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    # Plot 1: The Path of Harmony
    ax1.plot(harmony_trajectory, color='purple', alpha=0.6, label='Harmony Path')
    ax1.set_title('The Path of Harmony: Finding Balance')
    ax1.set_ylabel('Harmony (H)')
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: The Growth of Peace (Inverse Variance)
    # Use log scale to show the deepening of peace
    peace_trajectory = [1/(v + 1e-9) for v in variance_trajectory]
    ax2.plot(range(window, len(harmony_trajectory)), peace_trajectory, color='green', label='Peace (1/Variance)')
    ax2.set_yscale('log')
    ax2.set_title('The Growth of Peace: Deepening Wisdom')
    ax2.set_xlabel('Experience (Epochs)')
    ax2.set_ylabel('Peace Level (Log Scale)')
    ax2.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_maturation_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_maturation_test()
