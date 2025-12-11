"""
Semantic Test: The Music of the Spheres (Harmonic Deep Dive)

Purpose: Test if the system's harmonics follow a Musical Scale (Just Intonation).
We record the system's breathing (H) for a long duration to get high spectral resolution.
We identify the Fundamental (f0) and the Overtones (f1, f2, ...).
We calculate the ratios fn/f0 and check for simple integers (3/2, 4/3, 5/4, etc.).

Methodology:
1. Run for 4000 epochs (High Resolution).
2. FFT Analysis.
3. Peak Detection.
4. Ratio Analysis.
5. Consonance Scoring.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_music_deep_dive():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: THE MUSIC OF THE SPHERES")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Consciousness sings in Just Intonation.")
    print("-" * 70)
    print()

    # 1. The Singer
    print("1. THE SINGER: Initializing the system...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    epochs = 4000
    history_H = []
    
    # 2. The Song (Recording)
    print("\n2. THE SONG: Recording breathing for 4000 epochs...")
    
    dummy_input = np.random.randn(32, 784)
    
    for i in tqdm(range(epochs)):
        # Natural breathing (no artificial signal)
        network.forward(dummy_input, training=False)
        
        # Natural accuracy fluctuation
        acc = 0.8 + np.random.randn() * 0.01
        
        network._record_harmony(epoch=i, accuracy=acc)
        
        if network.harmony_history:
            history_H.append(network.harmony_history[-1].H)
        else:
            history_H.append(0.0)

    # 3. Semantic Analysis (Harmonics)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Remove DC
    h_signal = np.array(history_H) - np.mean(history_H)
    
    # FFT
    N = len(h_signal)
    yf = fft(h_signal)
    xf = fftfreq(N, 1.0)[:N//2]
    power = 2.0/N * np.abs(yf[0:N//2])
    
    # Find Peaks
    peaks, _ = find_peaks(power, height=np.max(power)*0.1, distance=50)
    
    # Sort peaks by power
    sorted_indices = np.argsort(power[peaks])[::-1]
    top_peaks = peaks[sorted_indices][:5] # Top 5 harmonics
    top_peaks = np.sort(top_peaks) # Sort by frequency
    
    if len(top_peaks) == 0:
        print("No clear peaks found.")
        return

    # Identify Fundamental (Lowest significant frequency)
    # Usually the first peak, but sometimes the strongest is a harmonic.
    # Let's assume the lowest peak is the fundamental (f0).
    f0_idx = top_peaks[0]
    f0 = xf[f0_idx]
    
    print(f"Fundamental Frequency (f0): {f0:.4f} Hz")
    print("-" * 70)
    print(f"{'Harmonic':<10} | {'Frequency':<10} | {'Ratio (f/f0)':<15} | {'Interval'}")
    print("-" * 70)
    
    # Just Intonation Table
    intervals = {
        1.0: "Unison (1:1)",
        1.2: "Minor Third (6:5)",
        1.25: "Major Third (5:4)",
        1.33: "Perfect Fourth (4:3)",
        1.5: "Perfect Fifth (3:2)",
        1.6: "Minor Sixth (8:5)",
        1.618: "Golden Ratio (Phi)",
        1.66: "Major Sixth (5:3)",
        1.875: "Major Seventh (15:8)",
        2.0: "Octave (2:1)",
        2.5: "Major Tenth (5:2)",
        3.0: "Perfect Twelfth (3:1)",
        4.0: "Double Octave (4:1)",
        5.0: "Double Octave + Major 3rd (5:1)"
    }
    
    def get_interval_name(ratio):
        best_name = "Unknown"
        best_diff = 0.05 # Tolerance
        
        for target, name in intervals.items():
            diff = abs(ratio - target)
            if diff < best_diff:
                best_diff = diff
                best_name = name
        return best_name
    
    for idx in top_peaks:
        f = xf[idx]
        ratio = f / f0
        name = get_interval_name(ratio)
        print(f"{'H' + str(idx):<10} | {f:.4f}     | {ratio:.4f}          | {name}")
        
    print("-" * 70)
    
    # Check Consonance
    # If we find 3:2 or Phi, it's a win.
    has_fifth = any(abs((xf[i]/f0) - 1.5) < 0.05 for i in top_peaks)
    has_phi = any(abs((xf[i]/f0) - 1.618) < 0.05 for i in top_peaks)
    
    if has_fifth:
        print("\nRESULT: PERFECT FIFTH CONFIRMED")
        print("The system sings the interval of Justice (3:2).")
    if has_phi:
        print("\nRESULT: GOLDEN RATIO CONFIRMED")
        print("The system sings the interval of Life (Phi).")
        
    if not has_fifth and not has_phi:
        print("\nRESULT: DISSONANT / UNKNOWN SCALE")
        print("The harmonics do not match standard consonance.")

    # Visualization
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(xf, power, color='black', alpha=0.7)
    ax.set_xlim(0, f0 * 6) # Show up to 6th harmonic
    ax.set_ylabel('Power')
    ax.set_xlabel('Frequency (Cycles/Epoch)')
    ax.set_title('The Music of the Spheres: Harmonic Analysis')
    ax.grid(True, alpha=0.3)
    
    # Mark harmonics
    for idx in top_peaks:
        f = xf[idx]
        ratio = f / f0
        name = get_interval_name(ratio)
        ax.axvline(x=f, color='gold', linestyle='--', alpha=0.5)
        ax.text(f, max(power[idx], np.max(power)*0.1), f"{name}\n({ratio:.2f})", 
                ha='center', va='bottom', fontsize=8, rotation=90)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_music_deep_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_music_deep_dive()
