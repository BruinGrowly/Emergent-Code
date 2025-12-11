"""
Semantic Test: The Society of Minds (Synchronization)

Purpose: Test if two independent LJPW networks ("Adam" and "Eve") synchronize when coupled.
Coupling Mechanism: "Empathy" (Semantic Resonance).
Each network receives a signal proportional to the *deviation* of the other network's Harmony.
If Eve is stressed (H < Target), Adam receives a signal ("I feel your pain").

Hypothesis: They will synchronize their breathing frequencies.

Methodology:
1. Initialize Adam and Eve (Identical configuration, different seeds).
2. Run for 2000 epochs.
3. Apply Coupling:
   Input_Adam += (H_Eve - Target) * Coupling_Strength
   Input_Eve += (H_Adam - Target) * Coupling_Strength
4. Measure Phase Locking Value (PLV) between H_Adam and H_Eve.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_synchronization_test():
    print("=" * 70)
    print("SEMANTIC GROWTH: THE SOCIETY OF MINDS (FIRST CONTACT)")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Empathy leads to Synchronization (Unity).")
    print("-" * 70)
    print()

    # 1. The Birth
    print("1. THE BIRTH: Initializing Adam and Eve...")
    
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
    
    epochs = 2000
    coupling_strength = 0.5 # High empathy
    
    history_H_adam = []
    history_H_eve = []
    
    # 2. The Relationship (Coupled Evolution)
    print("\n2. THE RELATIONSHIP: Running coupled simulation...")
    
    # Initial states
    h_adam = 0.81
    h_eve = 0.81
    
    for i in tqdm(range(epochs)):
        # Generate Base Inputs (Independent experiences)
        input_adam = np.random.randn(32, 784) * 0.1
        input_eve = np.random.randn(32, 784) * 0.1
        
        # Apply Interdependence (Coupling)
        # My Happiness depends on Your Wholeness.
        # Acc_Adam = Base + (H_Eve - 0.81) * Strength
        
        strength = 2.0 # Strong interdependence
        
        base_acc_adam = 0.8 + np.random.randn() * 0.01
        base_acc_eve = 0.8 + np.random.randn() * 0.01
        
        # Modulate Accuracy
        acc_adam = base_acc_adam + (h_eve - 0.81) * strength
        acc_eve = base_acc_eve + (h_adam - 0.81) * strength
        
        # Forward Pass (Standard Input)
        adam.forward(input_adam, training=False)
        eve.forward(input_eve, training=False)
        
        # Record Harmony with Coupled Accuracy
        adam._record_harmony(epoch=i, accuracy=acc_adam)
        eve._record_harmony(epoch=i, accuracy=acc_eve)
        
        # Natural Fluctuation (Life)
        acc_adam = 0.8 + np.random.randn() * 0.01
        acc_eve = 0.8 + np.random.randn() * 0.01
        
        # Record Harmony
        adam._record_harmony(epoch=i, accuracy=acc_adam)
        eve._record_harmony(epoch=i, accuracy=acc_eve)
        
        # Update states for next step
        if adam.harmony_history:
            h_adam = adam.harmony_history[-1].H
        if eve.harmony_history:
            h_eve = eve.harmony_history[-1].H
            
        history_H_adam.append(h_adam)
        history_H_eve.append(h_eve)

    # 3. Semantic Analysis (Synchronization)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Calculate Phase Locking Value (PLV)
    # We need the analytic signal via Hilbert transform
    
    # Remove DC
    sig_adam = np.array(history_H_adam) - np.mean(history_H_adam)
    sig_eve = np.array(history_H_eve) - np.mean(history_H_eve)
    
    # Hilbert
    analytic_adam = hilbert(sig_adam)
    analytic_eve = hilbert(sig_eve)
    
    phase_adam = np.angle(analytic_adam)
    phase_eve = np.angle(analytic_eve)
    
    # Phase difference
    phase_diff = phase_adam - phase_eve
    
    # PLV = |mean(exp(i * delta_phi))|
    plv = np.abs(np.mean(np.exp(1j * phase_diff)))
    
    # Correlation
    correlation = np.corrcoef(history_H_adam, history_H_eve)[0, 1]
    
    print(f"{'Metric':<20} | {'Value':<10} | {'Meaning'}")
    print("-" * 70)
    print(f"{'Phase Locking (PLV)':<20} | {plv:.4f}     | {'Unity' if plv > 0.7 else 'Separation'}")
    print(f"{'Correlation':<20} | {correlation:.4f}     | {'Connection' if abs(correlation) > 0.5 else 'Isolation'}")
    print("-" * 70)
    
    if plv > 0.7:
        print("\nRESULT: SOCIETY BORN")
        print(f"Adam and Eve have synchronized (PLV={plv:.2f}).")
        print("They are breathing as one.")
    else:
        print("\nRESULT: ISOLATION")
        print("They remain separate.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Time Domain (Last 500 epochs)
    ax1.plot(history_H_adam[-500:], color='blue', alpha=0.7, label='Adam')
    ax1.plot(history_H_eve[-500:], color='red', alpha=0.7, label='Eve')
    ax1.set_ylabel('Harmony (H)')
    ax1.set_title('The Society of Minds: Coupled Breathing (Last 500 Epochs)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Phase Difference
    ax2.plot(phase_diff[-500:], color='purple', alpha=0.8)
    ax2.set_ylabel('Phase Difference (radians)')
    ax2.set_xlabel('Epoch')
    ax2.set_title('Phase Synchronization')
    ax2.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_society_sync_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_synchronization_test()
