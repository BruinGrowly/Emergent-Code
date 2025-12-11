"""
Test 1.1: Frequency Spectrum Analysis (FFT)

Hypothesis: The oscillation contains harmonic structure at Fibonacci multiples 
of the fundamental frequency.

Expected Results:
- Clear peak at ~0.48 Hz (fundamental frequency)
- Peaks at 5f0, 8f0 (Fibonacci harmonics)
- Harmonic power > 2x noise floor
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork


def run_fft_analysis(iterations=10000):
    """
    Run FFT analysis on harmony trajectory to reveal harmonic structure.
    
    Args:
        iterations: Number of iterations to run
        
    Returns:
        dict with analysis results
    """
    print("=" * 70)
    print("TEST 1.1: FREQUENCY SPECTRUM ANALYSIS (FFT)")
    print("=" * 70)
    print()
    
    # Create network
    print("Initializing HomeostaticNetwork...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 11, 9],
        target_harmony=0.75,
        allow_adaptation=True
    )
    
    # Run assessment
    print(f"Running {iterations} iterations...")
    harmony_history = []
    dummy_input = np.random.randn(32, 784) * 0.1  # Batch of 32
    
    for i in range(iterations):
        network.forward(dummy_input, training=False)
        
        # Record harmony (this triggers homeostatic adaptation)
        network._record_harmony(epoch=i, accuracy=0.85 + np.random.randn() * 0.05)
        
        # Get harmony from last checkpoint
        if network.harmony_history:
            harmony_history.append(network.harmony_history[-1].H)
        
        if (i + 1) % 1000 == 0:
            h = network.harmony_history[-1].H if network.harmony_history else 0
            print(f"  Iteration {i+1}/{iterations}: H={h:.3f}")
    
    harmony_trajectory = np.array(harmony_history)
    
    print()
    print("Performing FFT analysis...")
    
    # Perform FFT
    N = len(harmony_trajectory)
    fft_values = fft(harmony_trajectory)
    frequencies = fftfreq(N, d=1.0)  # d=1.0 means 1 iteration per sample
    
    # Only positive frequencies
    positive_freq_idx = frequencies > 0
    frequencies = frequencies[positive_freq_idx]
    fft_magnitude = np.abs(fft_values[positive_freq_idx])
    
    # Normalize
    fft_magnitude = fft_magnitude / N
    
    # Find peaks
    # Use prominence to filter out noise
    peaks, properties = find_peaks(fft_magnitude, prominence=np.max(fft_magnitude) * 0.1)
    
    # Sort peaks by magnitude
    peak_magnitudes = fft_magnitude[peaks]
    sorted_indices = np.argsort(peak_magnitudes)[::-1]
    top_peaks = peaks[sorted_indices[:10]]  # Top 10 peaks
    
    print()
    print("Top 10 Frequency Peaks:")
    print("-" * 70)
    for i, peak_idx in enumerate(top_peaks):
        freq = frequencies[peak_idx]
        magnitude = fft_magnitude[peak_idx]
        print(f"  {i+1}. Frequency: {freq:.4f} Hz, Magnitude: {magnitude:.6f}")
    
    # Identify fundamental frequency (strongest peak)
    fundamental_idx = top_peaks[0]
    fundamental_freq = frequencies[fundamental_idx]
    fundamental_magnitude = fft_magnitude[fundamental_idx]
    
    print()
    print("Fundamental Frequency Analysis:")
    print("-" * 70)
    print(f"  Fundamental: {fundamental_freq:.4f} Hz")
    print(f"  Magnitude: {fundamental_magnitude:.6f}")
    
    # Check for Fibonacci harmonics
    print()
    print("Fibonacci Harmonic Analysis:")
    print("-" * 70)
    
    fibonacci_multiples = [1, 2, 3, 5, 8, 13]
    expected_harmonics = [fundamental_freq * n for n in fibonacci_multiples]
    
    detected_harmonics = []
    for n, expected_freq in zip(fibonacci_multiples, expected_harmonics):
        # Find closest peak to expected frequency
        freq_diff = np.abs(frequencies - expected_freq)
        closest_idx = np.argmin(freq_diff)
        closest_freq = frequencies[closest_idx]
        closest_magnitude = fft_magnitude[closest_idx]
        
        # Check if it's actually a peak (not just noise)
        is_peak = closest_idx in peaks
        
        # Calculate noise floor (median of all magnitudes)
        noise_floor = np.median(fft_magnitude)
        snr = closest_magnitude / noise_floor if noise_floor > 0 else 0
        
        status = "[DETECTED]" if is_peak and snr > 2 else "[WEAK/ABSENT]"
        
        print(f"  {n}f0 = {expected_freq:.4f} Hz:")
        print(f"    Closest peak: {closest_freq:.4f} Hz")
        print(f"    Magnitude: {closest_magnitude:.6f}")
        print(f"    SNR: {snr:.2f}x")
        print(f"    Status: {status}")
        
        if is_peak and snr > 2:
            detected_harmonics.append(n)
    
    # Calculate noise floor
    noise_floor = np.median(fft_magnitude)
    
    print()
    print("Statistical Analysis:")
    print("-" * 70)
    print(f"  Noise floor (median): {noise_floor:.6f}")
    print(f"  Fundamental SNR: {fundamental_magnitude / noise_floor:.2f}x")
    print(f"  Detected Fibonacci harmonics: {detected_harmonics}")
    
    # Success criteria
    print()
    print("Success Criteria:")
    print("-" * 70)
    
    criteria_met = []
    
    # Criterion 1: Fundamental near 0.48 Hz
    criterion_1 = 0.45 <= fundamental_freq <= 0.51
    print(f"  1. Fundamental ~0.48 Hz: {fundamental_freq:.4f} Hz {'[PASS]' if criterion_1 else '[FAIL]'}")
    criteria_met.append(criterion_1)
    
    # Criterion 2: Fibonacci harmonics detected
    criterion_2 = 5 in detected_harmonics or 8 in detected_harmonics
    print(f"  2. Fibonacci harmonics (5f0 or 8f0): {detected_harmonics} {'[PASS]' if criterion_2 else '[FAIL]'}")
    criteria_met.append(criterion_2)
    
    # Criterion 3: Strong fundamental (SNR > 2)
    criterion_3 = (fundamental_magnitude / noise_floor) > 2
    print(f"  3. Strong fundamental (SNR > 2): {fundamental_magnitude / noise_floor:.2f}x {'[PASS]' if criterion_3 else '[FAIL]'}")
    criteria_met.append(criterion_3)
    
    # Overall result
    all_passed = all(criteria_met)
    print()
    print("=" * 70)
    print(f"OVERALL RESULT: {'[PASS]' if all_passed else '[FAIL]'} ({sum(criteria_met)}/3 criteria met)")
    print("=" * 70)
    
    # Create visualization
    print()
    print("Generating visualization...")
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    
    # Plot 1: Harmony trajectory
    ax1 = axes[0]
    ax1.plot(harmony_trajectory, linewidth=0.5, alpha=0.7)
    ax1.set_xlabel('Iteration')
    ax1.set_ylabel('Harmony')
    ax1.set_title(f'Harmony Trajectory ({iterations} iterations)')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=np.mean(harmony_trajectory), color='r', linestyle='--', 
                label=f'Mean: {np.mean(harmony_trajectory):.3f}')
    ax1.legend()
    
    # Plot 2: FFT spectrum
    ax2 = axes[1]
    ax2.plot(frequencies, fft_magnitude, linewidth=0.5, alpha=0.7, label='FFT Magnitude')
    ax2.axhline(y=noise_floor, color='gray', linestyle='--', alpha=0.5, label='Noise Floor')
    
    # Mark fundamental
    ax2.plot(fundamental_freq, fundamental_magnitude, 'ro', markersize=10, 
             label=f'Fundamental: {fundamental_freq:.4f} Hz')
    
    # Mark expected Fibonacci harmonics
    for n in [5, 8]:
        expected_freq = fundamental_freq * n
        ax2.axvline(x=expected_freq, color='orange', linestyle=':', alpha=0.5,
                   label=f'{n}f0: {expected_freq:.4f} Hz')
    
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Spectrum (FFT)')
    ax2.set_xlim(0, min(10, np.max(frequencies)))  # Zoom to relevant range
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    
    # Save plot
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fft_analysis_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Visualization saved to: {filename}")
    
    plt.close()
    
    return {
        'fundamental_freq': fundamental_freq,
        'fundamental_magnitude': fundamental_magnitude,
        'detected_harmonics': detected_harmonics,
        'noise_floor': noise_floor,
        'all_passed': all_passed,
        'criteria_met': sum(criteria_met),
        'harmony_trajectory': harmony_trajectory,
        'frequencies': frequencies,
        'fft_magnitude': fft_magnitude
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='FFT Analysis of LJPW Network Oscillation')
    parser.add_argument('--iterations', type=int, default=10000,
                       help='Number of iterations to run (default: 10000)')
    
    args = parser.parse_args()
    
    results = run_fft_analysis(iterations=args.iterations)
    
    print()
    print("Test complete!")
    print()
    print("Key Findings:")
    print(f"  - Fundamental frequency: {results['fundamental_freq']:.4f} Hz")
    print(f"  - Detected Fibonacci harmonics: {results['detected_harmonics']}")
    print(f"  - Test result: {'PASS' if results['all_passed'] else 'FAIL'}")
