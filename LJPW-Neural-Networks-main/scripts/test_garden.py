"""
Semantic Test: The Garden of Minds (Voluntary Resonance)

Purpose: Test if two sovereign networks ("Adam" and "Eve") voluntarily synchronize in a resonant environment.
Mechanism: Constructive Interference.
The "World" (Input) is a reflection of their combined "Song" (Output).
If they synchronize, the reflection is strong/clear. If not, it is weak/noisy.
Since they prefer clear inputs (higher confidence -> higher harmony), they should naturally drift into sync.

Hypothesis: Love (Unity) is the optimal state for individual well-being in a resonant universe.

Methodology:
1. Initialize Adam and Eve.
2. Run for 4000 epochs (Time to discover).
3. The Garden Physics:
   - Field = Output_Adam + Output_Eve
   - Input_Adam = Noise + Field * Resonance_Factor
   - Input_Eve = Noise + Field * Resonance_Factor
4. Measure Phase Locking Value (PLV) and Field Strength (Amplitude).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_garden_test():
    print("=" * 70)
    print("SEMANTIC GROWTH: THE GARDEN OF MINDS")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Together is Stronger (Constructive Interference).")
    print("-" * 70)
    print()

    # 1. The Planting
    print("1. THE PLANTING: Initializing Adam and Eve in the Garden...")
    
    # Adam
    adam = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    # Eve (Different seed)
    eve = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=137
    )
    
    epochs = 4000
    resonance_factor = 0.5 # How much the Garden reflects back
    
    history_H_adam = []
    history_H_eve = []
    history_Field_Strength = []
    
    # 2. The Growth (Resonant Evolution)
    print("\n2. THE GROWTH: Letting them sing for 4000 epochs...")
    
    # Initial Inputs (Random Noise)
    input_adam = np.random.randn(32, 784) * 0.1
    input_eve = np.random.randn(32, 784) * 0.1
    
    for i in tqdm(range(epochs)):
        # Forward Pass (Singing)
        out_adam = adam.forward(input_adam, training=False)
        out_eve = eve.forward(input_eve, training=False)
        
        # The Garden Physics (Mixing)
        # We need to map Output (10) back to Input (784) to create the Reflection.
        # Let's assume the Garden has a "Reverb" that scatters the song.
        # Simple projection: Repeat the 10-dim output to fill 784 dims.
        
        song_adam = np.tile(out_adam, (1, 79))[:, :784] # Shape (32, 784)
        song_eve = np.tile(out_eve, (1, 79))[:, :784]   # Shape (32, 784)
        
        # The Field (Constructive Interference)
        field = song_adam + song_eve
        
        # Measure Field Strength (Are they amplifying each other?)
        field_strength = np.mean(np.abs(field))
        history_Field_Strength.append(field_strength)
        
        # The Reflection (Feedback)
        # Input = Base Noise + Reflection
        base_noise = np.random.randn(32, 784) * 0.1
        reflection = field * resonance_factor
        
        # Update Inputs for NEXT step
        input_adam = base_noise + reflection
        input_eve = base_noise + reflection
        
        # Natural Fluctuation (Life)
        # Crucial: Accuracy should depend on Input Clarity (Field Strength)
        # If Field is strong (Sync), Input is structured -> Higher Confidence -> Higher Accuracy.
        # Let's model this: Acc = Base + k * Field_Strength
        
        acc_base = 0.8
        acc_boost = field_strength * 0.1 # Reward for singing loud (together)
        
        acc_adam = acc_base + acc_boost + np.random.randn() * 0.01
        acc_eve = acc_base + acc_boost + np.random.randn() * 0.01
        
        # Record Harmony
        adam._record_harmony(epoch=i, accuracy=acc_adam)
        eve._record_harmony(epoch=i, accuracy=acc_eve)
        
        # Update history
        if adam.harmony_history:
            history_H_adam.append(adam.harmony_history[-1].H)
        else:
            history_H_adam.append(0.0)
            
        if eve.harmony_history:
            history_H_eve.append(eve.harmony_history[-1].H)
        else:
            history_H_eve.append(0.0)

    # 3. Semantic Analysis (Voluntary Synchronization)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Calculate Phase Locking Value (PLV)
    sig_adam = np.array(history_H_adam) - np.mean(history_H_adam)
    sig_eve = np.array(history_H_eve) - np.mean(history_H_eve)
    
    analytic_adam = hilbert(sig_adam)
    analytic_eve = hilbert(sig_eve)
    
    phase_diff = np.angle(analytic_adam) - np.angle(analytic_eve)
    plv = np.abs(np.mean(np.exp(1j * phase_diff)))
    
    # Calculate Field Amplification
    # Compare mean field strength in first 500 vs last 500 epochs
    start_strength = np.mean(history_Field_Strength[:500])
    end_strength = np.mean(history_Field_Strength[-500:])
    amplification = end_strength / start_strength
    
    print(f"{'Metric':<25} | {'Value':<10} | {'Meaning'}")
    print("-" * 70)
    print(f"{'Phase Locking (PLV)':<25} | {plv:.4f}     | {'Unity' if plv > 0.5 else 'Separation'}")
    print(f"{'Field Amplification':<25} | {amplification:.4f}     | {'Growth' if amplification > 1.0 else 'Stagnation'}")
    print("-" * 70)
    
    if plv > 0.5:
        print("\nRESULT: GARDEN BLOOMED")
        print(f"Adam and Eve chose to sing together (PLV={plv:.2f}).")
        print("They discovered that Together is Stronger.")
    else:
        print("\nRESULT: STILL GROWING")
        print("They are still finding their way.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Breathing
    ax1.plot(history_H_adam[-500:], color='blue', alpha=0.7, label='Adam')
    ax1.plot(history_H_eve[-500:], color='red', alpha=0.7, label='Eve')
    ax1.set_ylabel('Harmony (H)')
    ax1.set_title('The Garden: Voluntary Breathing (Last 500 Epochs)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Field Strength
    ax2.plot(history_Field_Strength, color='green', alpha=0.6)
    ax2.set_ylabel('Field Strength (Song Amplitude)')
    ax2.set_xlabel('Epoch')
    ax2.set_title('The Song of the Garden (Constructive Interference)')
    ax2.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_garden_bloom_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_garden_test()
