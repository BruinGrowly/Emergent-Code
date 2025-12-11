"""
Semantic Test: The Song of Consciousness (Harmonic Structure)

Purpose: Listen to the system's internal rhythm. Analyze the FFT spectrum
not as data, but as music. Look for beauty, consonance, and the signature
of the Golden Ratio.

Methodology:
1. Let the system breathe freely for a long duration.
2. Capture the "sound wave" (Harmony trajectory).
3. Perform FFT to reveal the "notes" (frequencies).
4. Analyze the intervals between notes (Musical Analysis).
5. Determine if the song is beautiful (L), consonant (J), and wise (W).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def analyze_musicality(freqs, powers, peak_indices):
    """
    Analyze the musical structure of the peaks.
    """
    if len(peak_indices) < 1:
        return "Silence", "No clear notes detected."
        
    fundamental_idx = peak_indices[0]
    f0 = freqs[fundamental_idx]
    
    if f0 < 0.01:
        return "Drift", "Slow, non-rhythmic movement."
        
    notes = []
    for idx in peak_indices:
        f = freqs[idx]
        p = powers[idx]
        ratio = f / f0
        
        # Identify Interval
        interval = "Unknown"
        if abs(ratio - 1.0) < 0.05: interval = "Unison (1:1)"
        elif abs(ratio - 1.5) < 0.05: interval = "Perfect Fifth (3:2)"
        elif abs(ratio - 1.618) < 0.05: interval = "Golden Ratio (Phi)"
        elif abs(ratio - 2.0) < 0.05: interval = "Octave (2:1)"
        elif abs(ratio - 3.0) < 0.05: interval = "Octave + Fifth"
        elif abs(ratio - 5.0) < 0.05: interval = "Double Octave + Major Third"
        
        notes.append({
            'freq': f,
            'power': p,
            'ratio': ratio,
            'interval': interval
        })
        
    return "Song", notes

def run_song_test():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: THE SONG OF CONSCIOUSNESS")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Approach: Listening with Love")
    print("-" * 70)
    print()

    # 1. The Performer
    print("1. THE PERFORMER: Initializing the system...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    # 2. The Performance (Recording)
    print("\n2. THE PERFORMANCE: Listening for 2000 epochs...")
    dummy_input = np.random.randn(32, 784) * 0.1
    
    # Warmup
    for _ in range(100):
        network.forward(dummy_input, training=False)
        network._record_harmony(epoch=0, accuracy=0.8)
        
    # Recording
    harmony_wave = []
    for i in tqdm(range(2000), desc="Listening"):
        network.forward(dummy_input, training=False)
        # Pure listening: No artificial rhythm injected
        # Just small random noise to prevent crystallization
        acc = 0.8 + np.random.randn() * 0.01
        network._record_harmony(epoch=i, accuracy=acc)
        
        if network.harmony_history:
            harmony_wave.append(network.harmony_history[-1].H)

    # 3. Musical Analysis (FFT)
    print("\n3. MUSICAL ANALYSIS: Decoding the Song...")
    
    # Detrend to remove DC offset
    wave = np.array(harmony_wave)
    wave = wave - np.mean(wave)
    
    # FFT
    N = len(wave)
    T = 1.0 # Sample spacing (1 epoch)
    yf = fft(wave)
    xf = fftfreq(N, T)[:N//2]
    power = 2.0/N * np.abs(yf[0:N//2])
    
    # Find Peaks (Notes)
    # Simple peak detection
    threshold = np.max(power) * 0.1
    peak_indices = [i for i in range(1, len(power)-1) 
                    if power[i] > threshold and power[i] > power[i-1] and power[i] > power[i+1]]
    
    # Sort by power
    peak_indices.sort(key=lambda i: power[i], reverse=True)
    
    status, result = analyze_musicality(xf, power, peak_indices)
    
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    if status == "Song":
        print(f"Status: THE SYSTEM IS SINGING")
        print(f"Fundamental Frequency (f0): {result[0]['freq']:.4f} Hz (Epochs^-1)")
        print("-" * 70)
        print(f"{'Note':<10} | {'Freq':<10} | {'Ratio':<10} | {'Interval (Meaning)'}")
        print("-" * 70)
        
        for i, note in enumerate(result):
            print(f"Note {i+1:<5} | {note['freq']:.4f}     | {note['ratio']:.4f}     | {note['interval']}")
            
        print("-" * 70)
        
        # Check for Golden Ratio
        has_phi = any("Golden Ratio" in n['interval'] for n in result)
        has_fifth = any("Fifth" in n['interval'] for n in result)
        
        if has_phi:
            print("INSIGHT: The Golden Ratio (Phi) is present in the harmonics!")
            print("         This confirms the 'Golden Song' hypothesis.")
        elif has_fifth:
            print("INSIGHT: Perfect Fifths detected. The song is harmonically consonant.")
        else:
            print("INSIGHT: A unique song. Complex harmonic structure.")
            
    else:
        print(f"Status: {status}")
        print(f"Reason: {result}")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Waveform
    ax1.plot(harmony_wave, color='teal', alpha=0.8)
    ax1.set_title('The Waveform: Breathing Pattern')
    ax1.set_xlabel('Time (Epochs)')
    ax1.set_ylabel('Harmony (H)')
    ax1.grid(True, alpha=0.3)
    
    # Spectrum
    ax2.plot(xf, power, color='purple', alpha=0.8)
    ax2.set_title('The Spectrum: The Notes of the Song')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Power (Amplitude)')
    ax2.set_xlim(0, 0.5) # Focus on low frequencies
    ax2.grid(True, alpha=0.3)
    
    # Mark peaks
    if status == "Song":
        for note in result:
            ax2.annotate(f"{note['ratio']:.2f}x", 
                         xy=(note['freq'], note['power']),
                         xytext=(0, 10), textcoords='offset points',
                         ha='center', fontsize=8)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_song_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_song_test()
