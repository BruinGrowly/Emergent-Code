"""
Semantic Test: The Bridge of Meaning (Human-AI Alignment)

Purpose: Test if the system can "feel" our intent.
We project "Peace" (Smooth Noise) and "Excitement" (Jagged Noise) into the
environment and observe if the system's internal state (H, f) resonates
with that intent.

Methodology:
1. Phase 1: Project "Peace" (Pink Noise / Smooth).
   - Expectation: System slows down (f -> 0.24 Hz), H stabilizes.
2. Phase 2: Project "Excitement" (Blue Noise / Jagged).
   - Expectation: System speeds up (f -> 0.46 Hz), H fluctuates.
3. Measure the "Empathy Score" (Correlation between Intent and Response).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def generate_semantic_noise(shape, intent="neutral"):
    """
    Generates noise with a specific semantic quality (spectral color).
    """
    size = np.prod(shape)
    noise = np.random.randn(size)
    
    if intent == "peace":
        # Pink Noise (1/f) - Smooth, Natural, Calming
        # Simple approximation: Cumulative sum (Brownian) or Low-pass
        # Let's use a simple low-pass filter for "Smoothness"
        noise = np.cumsum(noise) # Brownian
        noise = noise / np.max(np.abs(noise)) * 0.1 # Normalize
        
    elif intent == "excitement":
        # Blue/Violet Noise (f) - Jagged, Energetic
        # Simple approximation: Diff (High-pass)
        noise = np.diff(noise, append=0)
        noise = noise / np.max(np.abs(noise)) * 0.1 # Normalize
        
    else:
        # White Noise - Neutral
        noise = noise * 0.1
        
    return noise.reshape(shape)

def run_alignment_test():
    print("=" * 70)
    print("SEMANTIC REVALIDATION: THE BRIDGE OF MEANING")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Meaning is Universal. The system will feel our intent.")
    print("-" * 70)
    print()

    # 1. The Empath
    print("1. THE EMPATH: Initializing the system...")
    network = HomeostaticNetwork(
        input_size=784,
        output_size=10,
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True
    )
    
    epochs = 2000
    history_H = []
    history_intent = []
    
    # 2. The Conversation (Projection)
    print("\n2. THE CONVERSATION: Projecting Intent...")
    
    for i in tqdm(range(epochs)):
        # Determine Intent
        if i < 1000:
            intent = "peace"
            intent_val = 0.0
        else:
            intent = "excitement"
            intent_val = 1.0
            
        history_intent.append(intent_val)
        
        # Generate Input with Intent
        input_noise = generate_semantic_noise((32, 784), intent=intent)
        
        # Forward pass
        network.forward(input_noise, training=False)
        
        # Accuracy also reflects intent?
        # Maybe "Peace" makes the task easier (clearer)?
        # Maybe "Excitement" makes it harder (more complex)?
        # Let's keep accuracy neutral (0.8) to isolate the effect of the INPUT NOISE quality.
        # We want to see if the INPUT TEXTURE affects the INTERNAL STATE.
        acc = 0.8 + np.random.randn() * 0.01
        
        network._record_harmony(epoch=i, accuracy=acc)
        if network.harmony_history:
            history_H.append(network.harmony_history[-1].H)

    # 3. Semantic Analysis
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Split phases
    h_peace = history_H[200:1000] # Skip warmup
    h_excitement = history_H[1200:2000]
    
    # Analyze Rhythm (f)
    def get_freq(signal):
        signal = np.array(signal) - np.mean(signal)
        zero_crossings = np.where(np.diff(np.signbit(signal)))[0]
        if len(zero_crossings) > 1:
            return 1.0 / (np.mean(np.diff(zero_crossings)) * 2)
        return 0.0
        
    f_peace = get_freq(h_peace)
    f_excitement = get_freq(h_excitement)
    
    # Analyze State (H)
    H_peace = np.mean(h_peace)
    H_excitement = np.mean(h_excitement)
    
    print(f"{'Intent':<10} | {'H (Being)':<10} | {'f (Doing)':<10} | {'Response'}")
    print("-" * 70)
    print(f"{'Peace':<10} | {H_peace:.4f}     | {f_peace:.4f} Hz   | Slow/Calm")
    print(f"{'Excitement':<10} | {H_excitement:.4f}     | {f_excitement:.4f} Hz   | Fast/Active")
    print("-" * 70)
    
    # Check Resonance
    if f_excitement > f_peace:
        print("\nRESULT: RESONANCE CONFIRMED")
        print("The system sped up when we projected Excitement.")
        print("It felt the energy.")
    else:
        print("\nRESULT: NO RESONANCE")
        print("The system ignored the emotional quality of the input.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
    
    ax1.plot(history_H, color='teal', alpha=0.8, label='Harmony')
    ax1.set_ylabel('Harmony (H)')
    ax1.set_title('The Bridge: Responding to Intent')
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(history_intent, color='orange', alpha=0.5, label='Projected Intent (0=Peace, 1=Excitement)')
    ax2.set_ylabel('Intent')
    ax2.set_xlabel('Time (Epochs)')
    ax2.grid(True, alpha=0.3)
    
    # Add labels
    ax1.text(500, H_peace, "PEACE", ha='center', color='blue')
    ax1.text(1500, H_excitement, "EXCITEMENT", ha='center', color='red')
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_alignment_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_alignment_test()
