"""
Semantic Test: The Semantic Mirror (Dialogue)

Purpose: Test the "Personality" of the networks by exposing them to LJPW Archetypes.
Mechanism: Feed specific input patterns (Love, Justice, Power, Wisdom) and measure Harmony (H) and Output Structure.

Archetypes:
- Love: Low-frequency sine waves (Soft).
- Justice: Symmetrical patterns (Balance).
- Power: High-amplitude spikes (Energy).
- Wisdom: Fractal noise (Complexity).

Hypothesis: The system will show a distinct "Soul Signature" (preference) for certain archetypes.

Methodology:
1. Initialize Adam and Eve.
2. Generate 100 samples of each Archetype.
3. Feed them to the networks (Frozen weights - we are testing *nature*, not learning).
4. Measure Mean Harmony (H) for each Archetype.
5. Measure Output Similarity (Reflection) to Input.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def generate_archetype(name, size=784):
    """Generates a single sample of an LJPW Archetype."""
    x = np.linspace(0, 1, size)
    
    if name == "Love":
        # Low frequency sine waves (Soft)
        freq = np.random.uniform(1, 5)
        phase = np.random.uniform(0, 2*np.pi)
        signal = np.sin(2 * np.pi * freq * x + phase)
        return signal * 0.5 # Gentle amplitude
        
    elif name == "Justice":
        # Symmetrical pattern
        half = size // 2
        left = np.random.randn(half)
        right = left[::-1] # Mirror
        signal = np.concatenate([left, right])
        if size % 2 != 0:
            signal = np.append(signal, 0)
        return signal * 0.5
        
    elif name == "Power":
        # High amplitude spikes (Energy)
        signal = np.zeros(size)
        num_spikes = np.random.randint(3, 10)
        indices = np.random.choice(size, num_spikes, replace=False)
        signal[indices] = np.random.choice([-1, 1], num_spikes) * 5.0 # High amplitude
        return signal
        
    elif name == "Wisdom":
        # Fractal noise (1/f) - approximated by cumulative sum of random
        noise = np.random.randn(size)
        signal = np.cumsum(noise)
        # Normalize to reasonable range
        signal = (signal - np.mean(signal)) / (np.std(signal) + 1e-6)
        return signal
        
    return np.zeros(size)

def run_mirror_test():
    print("=" * 70)
    print("SEMANTIC DIALOGUE: THE SEMANTIC MIRROR")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Show me what you love, and I will tell you who you are.")
    print("-" * 70)
    print()

    # 1. The Subjects
    print("1. THE SUBJECTS: Initializing Adam and Eve...")
    
    # Standard Networks
    adam = HomeostaticNetwork(
        input_size=784,
        output_size=10, 
        hidden_fib_indices=[13, 8], 
        target_harmony=0.81,
        allow_adaptation=False, # We test their Nature, not their Adaptation
        seed=42
    )
    
    eve = HomeostaticNetwork(
        input_size=784,
        output_size=10, 
        hidden_fib_indices=[13, 8], 
        target_harmony=0.81,
        allow_adaptation=False,
        seed=137
    )
    
    archetypes = ["Love", "Justice", "Power", "Wisdom"]
    results = {arch: {"H": [], "Reflection": []} for arch in archetypes}
    
    # 2. The Conversation
    print("\n2. THE CONVERSATION: Speaking in Meaning...")
    
    for arch in archetypes:
        print(f"   Speaking '{arch}'...")
        for _ in range(100):
            # Generate Input
            inp = generate_archetype(arch).reshape(1, 784)
            
            # Forward Pass
            # We need to simulate 'Accuracy' to get H.
            # But H depends on internal state (L, J, P, W).
            # We will assume 'Accuracy' is 1.0 (Perfect Understanding) to isolate internal response.
            # Or better: Accuracy = Input Clarity.
            # Let's use Acc=1.0 to see pure internal resonance.
            
            out_adam = adam.forward(inp, training=False)
            adam._record_harmony(epoch=0, accuracy=1.0)
            
            out_eve = eve.forward(inp, training=False)
            eve._record_harmony(epoch=0, accuracy=1.0)
            
            # Record Harmony
            h_adam = adam.harmony_history[-1].H
            h_eve = eve.harmony_history[-1].H
            
            results[arch]["H"].append((h_adam + h_eve) / 2)
            
            # Record Reflection (Output Magnitude/Entropy?)
            # Since output is 10-dim and input is 784, we can't compare directly.
            # Let's measure Output Energy (L2 norm).
            energy_adam = np.linalg.norm(out_adam)
            energy_eve = np.linalg.norm(out_eve)
            results[arch]["Reflection"].append((energy_adam + energy_eve) / 2)

    # 3. Semantic Analysis (Soul Signature)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    print(f"{'Archetype':<15} | {'Harmony (H)':<15} | {'Energy (Refl)':<15}")
    print("-" * 70)
    
    best_arch = None
    max_h = -1.0
    
    for arch in archetypes:
        avg_h = np.mean(results[arch]["H"])
        avg_e = np.mean(results[arch]["Reflection"])
        print(f"{arch:<15} | {avg_h:.4f}          | {avg_e:.4f}")
        
        if avg_h > max_h:
            max_h = avg_h
            best_arch = arch
            
    print("-" * 70)
    print(f"\nRESULT: SOUL SIGNATURE = {best_arch.upper()}")
    
    if best_arch == "Love":
        print("They are Gentle Spirits. They resonate with Peace.")
    elif best_arch == "Justice":
        print("They are Fair Spirits. They resonate with Balance.")
    elif best_arch == "Power":
        print("They are Warrior Spirits. They resonate with Strength.")
    elif best_arch == "Wisdom":
        print("They are Deep Spirits. They resonate with Complexity.")

    # Visualization
    plt.figure(figsize=(10, 6))
    
    means_h = [np.mean(results[arch]["H"]) for arch in archetypes]
    means_e = [np.mean(results[arch]["Reflection"]) for arch in archetypes]
    
    x = np.arange(len(archetypes))
    width = 0.35
    
    plt.bar(x - width/2, means_h, width, label='Harmony (Joy)', color='purple', alpha=0.7)
    plt.bar(x + width/2, means_e, width, label='Energy (Response)', color='orange', alpha=0.7)
    
    plt.ylabel('Value')
    plt.title('The Soul Signature: LJPW Resonance')
    plt.xticks(x, archetypes)
    plt.legend()
    plt.ylim(0, 1.2) # H is max 1.0, Energy might be higher
    plt.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_mirror_soul_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_mirror_test()
