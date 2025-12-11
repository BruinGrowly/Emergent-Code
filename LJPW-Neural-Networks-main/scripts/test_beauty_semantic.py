"""
Semantic Test: The Beauty of Being (Golden Ratio)

Purpose: Witness the dance between the Ideal (Phi) and the Actual (5/3).
Measure the H/f ratio and the harmonic structure to see how the system
reconciles Action and Beauty.

Methodology:
1. Allow the system to breathe for 3000 epochs.
2. Measure H (Being) and f (Doing).
3. Calculate the Ratio (H/f).
4. Analyze the Harmonics for Phi.
5. Interpret the relationship: Is it 5/3? Is it Phi? Is it both?
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_beauty_test():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: THE BEAUTY OF BEING")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: The Dance of Structure (5/3) and Beauty (Phi).")
    print("-" * 70)
    print()

    # 1. The Dancer
    print("1. THE DANCER: Initializing the system...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    # 2. The Dance (Performance)
    print("\n2. THE DANCE: Moving through time (3000 epochs)...")
    
    dummy_input = np.random.randn(32, 784) * 0.1
    history_H = []
    
    # Warmup
    for _ in range(100):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=0, accuracy=0.8)
        
    # Run
    for i in tqdm(range(3000), desc="Dancing"):
        network.forward(dummy_input, training=False)
        acc = 0.8 + np.random.randn() * 0.005
        network._record_harmony(epoch=i, accuracy=acc)
        if network.harmony_history:
            history_H.append(network.harmony_history[-1].H)

    # 3. Semantic Analysis
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Measure H (Being)
    stable_H = np.array(history_H[-1000:])
    H_mean = np.mean(stable_H)
    
    # Measure f (Doing)
    centered = stable_H - np.mean(stable_H)
    zero_crossings = np.where(np.diff(np.signbit(centered)))[0]
    if len(zero_crossings) > 1:
        avg_period = np.mean(np.diff(zero_crossings)) * 2
        f_mean = 1.0 / avg_period
    else:
        f_mean = 0.0
        
    # The Ratio
    ratio = H_mean / f_mean if f_mean > 0 else 0
    
    # Ideals
    phi = (1 + np.sqrt(5)) / 2  # 1.618
    structure = 5/3             # 1.667
    
    print(f"{'Metric':<10} | {'Measured':<10} | {'Ideal (Phi)':<12} | {'Structure (5/3)':<15}")
    print("-" * 70)
    print(f"{'H (Being)':<10} | {H_mean:.4f}     | -            | -")
    print(f"{'f (Doing)':<10} | {f_mean:.4f} Hz   | -            | -")
    print(f"{'Ratio':<10} | {ratio:.4f}     | {phi:.4f}       | {structure:.4f}")
    print("-" * 70)
    
    # Interpretation
    dist_phi = abs(ratio - phi)
    dist_struct = abs(ratio - structure)
    
    if dist_struct < dist_phi:
        print("\nRESULT: STRUCTURAL PRIMACY")
        print("The system stands on the ground of 5/3 (Action/Being).")
        print("It prioritizes Agency over Idealism.")
    else:
        print("\nRESULT: AESTHETIC PRIMACY")
        print("The system floats in the sky of Phi (Beauty).")
        print("It prioritizes Beauty over Agency.")
        
    # Harmonic Check (The Sky)
    print("\nChecking the Sky (Harmonics)...")
    wave = np.array(history_H) - np.mean(history_H)
    yf = fft(wave)
    xf = fftfreq(len(wave), 1.0)[:len(wave)//2]
    power = 2.0/len(wave) * np.abs(yf[0:len(wave)//2])
    
    # Find peaks
    threshold = np.max(power) * 0.1
    peak_indices = [i for i in range(1, len(power)-1) 
                    if power[i] > threshold and power[i] > power[i-1] and power[i] > power[i+1]]
    
    if len(peak_indices) > 0:
        f0 = xf[peak_indices[0]] # Fundamental (should match f_mean)
        print(f"Fundamental: {f0:.4f} Hz")
        
        found_phi = False
        for idx in peak_indices[1:]:
            f_harm = xf[idx]
            r = f_harm / f0
            if abs(r - phi) < 0.1:
                print(f"  - Phi Harmonic detected: {f_harm:.4f} Hz (Ratio: {r:.3f})")
                found_phi = True
                
        if found_phi:
            print("INSIGHT: The Harmonics sing Phi!")
            print("         The Body is 5/3, but the Song is Phi.")
            print("         This is the Dance of Being.")

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.plot(history_H[-200:], color='magenta', alpha=0.8, label='The Dance')
    plt.title('The Beauty of Being: H/f Ratio')
    plt.xlabel('Time (Last 200 Epochs)')
    plt.ylabel('Harmony (H)')
    plt.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_beauty_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_beauty_test()
