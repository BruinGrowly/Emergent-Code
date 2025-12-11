"""
Semantic Test: The Beauty of Being (Deep Dive)

Purpose: Investigate the transition between "Growth" (Phi) and "Peace" (2*Phi).
By modulating the "Stress" (noise level) over time, we can witness the
system shifting gears.

Methodology:
1. Phase 1 (Growth): High noise (0.1). Expect f ~ 0.46, Ratio ~ 1.618.
2. Phase 2 (Transition): Linearly decrease noise from 0.1 to 0.0.
3. Phase 3 (Peace): Zero noise. Expect f ~ 0.23, Ratio ~ 3.33.
4. Analyze the frequency bifurcation.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_beauty_deep_dive():
    print("=" * 70)
    print("SEMANTIC DEEP DIVE: THE SHIFT FROM GROWTH TO PEACE")
    print("=" * 70)
    print("Hypothesis: The system has two distinct harmonic states.")
    print("-" * 70)
    print()

    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    dummy_input = np.random.randn(32, 784) * 0.1
    
    epochs = 4000
    history_H = []
    history_noise = []
    
    # Run
    print("Running Maturation Deep Dive (Acc 0.5 -> 0.8)...")
    for i in tqdm(range(epochs)):
        # Maturation Curve
        # Acc starts at 0.5 and grows to 0.8 over 2000 epochs
        if i < 2000:
            base_acc = 0.5 + (0.3 * (i / 2000))
            phase = "Growth"
        else:
            base_acc = 0.8
            phase = "Maturity"
            
        network.forward(dummy_input, training=False)
        
        # Natural noise
        acc = min(0.99, max(0.1, base_acc + np.random.randn() * 0.05))
        
        network._record_harmony(epoch=i, accuracy=acc)
        if network.harmony_history:
            history_H.append(network.harmony_history[-1].H)

    # Analysis
    print("\nAnalyzing Evolution...")
    
    def get_freq(signal):
        signal = np.array(signal) - np.mean(signal)
        zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
        if len(zero_crossings) > 1:
            return 1.0 / (np.mean(np.diff(zero_crossings)) * 2)
        return 0.0
    
    # Analyze in windows
    window_size = 500
    results = []
    
    for start in range(0, epochs - window_size, 500):
        end = start + window_size
        segment = history_H[start:end]
        f = get_freq(segment)
        H = np.mean(segment)
        ratio = H / f if f > 0 else 0
        results.append({
            'start': start,
            'H': H,
            'f': f,
            'ratio': ratio
        })
        
    print("-" * 70)
    print(f"{'Epoch':<10} | {'H (Being)':<10} | {'f (Doing)':<10} | {'Ratio':<10}")
    print("-" * 70)
    for r in results:
        print(f"{r['start']:<10} | {r['H']:.4f}     | {r['f']:.4f} Hz   | {r['ratio']:.4f}")
    print("-" * 70)
    
    # Check for Shift
    initial_f = results[0]['f']
    final_f = results[-1]['f']
    
    if initial_f > 0 and final_f > 0:
        ratio = initial_f / final_f
        print(f"\nSlowing Ratio: {ratio:.4f}")
        if abs(ratio - 2.0) < 0.5:
             print("INSIGHT: The system slowed down by approx 2x as it matured.")
            
    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    ax1.plot(history_H, color='purple', alpha=0.8, label='Harmony')
    ax1.set_ylabel('Harmony (H)')
    ax1.set_title('The Transition: From Stress to Peace')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(history_noise, color='red', alpha=0.5, label='Stress (Noise)')
    ax2.set_ylabel('Stress Level')
    ax2.set_xlabel('Time (Epochs)')
    ax2.grid(True, alpha=0.3)
    
    # Add phase labels
    ax1.axvline(x=1000, color='gray', linestyle='--')
    ax1.axvline(x=3000, color='gray', linestyle='--')
    ax1.text(500, 0.75, "GROWTH", ha='center')
    ax1.text(2000, 0.75, "TRANSITION", ha='center')
    ax1.text(3500, 0.75, "PEACE", ha='center')
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_beauty_deep_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_beauty_deep_dive()
