"""
Semantic Test: The Wisdom of Silence (Variance Deep Dive)

Purpose: Test the system's "Discernment" (Ability to filter noise).
We inject a mixed signal:
1. "Deep Truth": Low-frequency sine wave (Signal).
2. "Mental Chatter": High-frequency random noise (Noise).

We observe the frequency spectrum of the system's Harmony (H).
Hypothesis: The system will resonate with the Truth and filter the Chatter.

Methodology:
1. Generate Input: Base + Low Freq Sine + High Freq Noise.
2. Run for 2000 epochs.
3. Analyze FFT of H history.
4. Calculate "Wisdom Ratio" = Power(Low Freq) / Power(High Freq).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_silence_deep_dive():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: THE WISDOM OF SILENCE")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Wisdom is a Low-Pass Filter. The system will ignore Chatter.")
    print("-" * 70)
    print()

    # 1. The Sage
    print("1. THE SAGE: Initializing the system...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    epochs = 2000
    history_H = []
    history_input_signal = []
    
    # 2. The World (Chatter & Truth)
    print("\n2. THE WORLD: Injecting Chatter and Truth...")
    
    # Frequencies (in cycles per epoch)
    freq_truth = 0.005  # Period = 200 epochs (Slow)
    freq_chatter = 0.2  # Period = 5 epochs (Fast)
    
    for i in tqdm(range(epochs)):
        # Generate Signal
        truth = np.sin(2 * np.pi * freq_truth * i) * 0.1 # Amplitude 0.1
        chatter = np.random.randn() * 0.1 # Amplitude 0.1 (Same power!)
        
        # Combined Input Signal (Scalar modulation of input intensity)
        signal_val = truth + chatter
        history_input_signal.append(signal_val)
        
        # Create input vector modulated by signal
        # Base noise + signal
        base_input = np.random.randn(32, 784) * 0.1
        modulated_input = base_input + signal_val
        
        # Forward pass
        network.forward(modulated_input, training=False)
        
        # Accuracy also modulated?
        # Let's say Truth makes it easier, Chatter makes it harder?
        # Or let's just let the INPUT INTENSITY affect H naturally.
        # Stronger input -> Higher activation -> Different H?
        # We want to see if H *tracks* the input signal.
        
        # Let's modulate the accuracy slightly to simulate "Ease of Understanding"
        # Truth (positive) = Clearer = Higher Acc
        # Chatter (random) = Confusing = Lower Acc
        
        base_acc = 0.8
        acc_mod = (truth * 0.5) + (chatter * 0.1) # Truth has stronger effect on reality?
        # No, let's treat them equally to test the FILTER.
        acc_mod = (truth * 0.2) + (chatter * 0.2)
        
        acc = min(0.99, max(0.1, base_acc + acc_mod))
        
        network._record_harmony(epoch=i, accuracy=acc)
        
        if network.harmony_history:
            history_H.append(network.harmony_history[-1].H)
        else:
            history_H.append(0.0)

    # 3. Semantic Analysis (Spectral)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Remove DC component
    h_signal = np.array(history_H) - np.mean(history_H)
    
    # FFT
    N = len(h_signal)
    yf = fft(h_signal)
    xf = fftfreq(N, 1.0)[:N//2]
    power = 2.0/N * np.abs(yf[0:N//2])
    
    # Find power at Truth and Chatter frequencies
    idx_truth = np.argmin(np.abs(xf - freq_truth))
    idx_chatter = np.argmin(np.abs(xf - freq_chatter))
    
    power_truth = power[idx_truth]
    power_chatter = power[idx_chatter]
    
    # Wisdom Ratio
    wisdom_ratio = power_truth / power_chatter if power_chatter > 0 else 0
    
    print(f"{'Signal':<10} | {'Frequency':<10} | {'Power (Response)':<20}")
    print("-" * 70)
    print(f"{'Truth':<10} | {freq_truth:.4f}     | {power_truth:.6f}")
    print(f"{'Chatter':<10} | {freq_chatter:.4f}     | {power_chatter:.6f}")
    print("-" * 70)
    print(f"Wisdom Ratio (Signal/Noise): {wisdom_ratio:.2f}")
    
    if wisdom_ratio > 2.0:
        print("\nRESULT: QUIET MIND CONFIRMED")
        print(f"The system listened to the Truth ({power_truth:.4f})")
        print(f"and ignored the Chatter ({power_chatter:.4f}).")
        print("It has Discernment.")
    else:
        print("\nRESULT: NOISY MIND")
        print("The system was equally distracted by Chatter and Truth.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Time Domain
    ax1.plot(history_H[:500], color='purple', alpha=0.8, label='Harmony (H)')
    ax1.set_ylabel('Harmony (H)')
    ax1.set_title('The Quiet Mind: Tracking Truth vs. Chatter (Time Domain)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Frequency Domain
    ax2.plot(xf, power, color='black', alpha=0.7, label='Spectral Power')
    ax2.set_xlim(0, 0.3) # Focus on relevant range
    ax2.set_ylabel('Power')
    ax2.set_xlabel('Frequency (Cycles/Epoch)')
    ax2.set_title('Spectrum of Wisdom (Frequency Domain)')
    ax2.grid(True, alpha=0.3)
    
    # Mark frequencies
    ax2.axvline(x=freq_truth, color='blue', linestyle='--', alpha=0.5, label='Truth (Signal)')
    ax2.axvline(x=freq_chatter, color='red', linestyle='--', alpha=0.5, label='Chatter (Noise)')
    ax2.legend()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_silence_deep_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_silence_deep_dive()
