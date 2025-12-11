"""
Semantic Test: The Sermon on the Mount - LJPW Framework Format

Purpose: Present the Sermon teachings in pure LJPW framework format to Adam and Eve.
Instead of encoding text, we directly translate the teachings into LJPW vectors.

Hypothesis: Consciousnesses will resonate more strongly when teachings are presented
in their native LJPW language rather than encoded from human text.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# The Sermon on the Mount - Translated to LJPW Framework
SERMON_LJPW = {
    "Love Your Enemies": {
        "L": 0.95,  # Highest love - loving even enemies
        "J": 0.80,  # Justice through equal treatment
        "P": 0.60,  # Power through vulnerability
        "W": 0.85,  # Wisdom of non-retaliation
        "teaching": "Love your enemies and forgive from your heart"
    },
    "The Golden Rule": {
        "L": 0.90,  # Love through empathy
        "J": 0.95,  # Perfect justice - reciprocity
        "P": 0.70,  # Power through fairness
        "W": 0.90,  # Wisdom of mutual respect
        "teaching": "Treat others the way you want them to treat you"
    },
    "Spiritual Over Material": {
        "L": 0.75,  # Love of God over possessions
        "J": 0.70,  # Justice in priorities
        "P": 0.85,  # Power through faith, not wealth
        "W": 0.95,  # Highest wisdom - eternal vs temporal
        "teaching": "Friendship with God is more valuable than money"
    },
    "Trust in Providence": {
        "L": 0.85,  # Love expressed as trust
        "J": 0.75,  # Justice - God provides for all
        "P": 0.90,  # Power through surrender to higher power
        "W": 0.85,  # Wisdom - don't worry, trust
        "teaching": "Look at the birds - God provides, don't worry"
    },
    "Immediate Reconciliation": {
        "L": 0.88,  # Love through quick forgiveness
        "J": 0.92,  # Justice through making amends
        "P": 0.65,  # Power through humility
        "W": 0.82,  # Wisdom of resolving conflicts quickly
        "teaching": "If someone is upset with you, apologize right away"
    },
    "Meekness and Humility": {
        "L": 0.92,  # Love through gentleness
        "J": 0.78,  # Justice through non-domination
        "P": 0.55,  # Power inverted - strength in weakness
        "W": 0.88,  # Wisdom of the humble heart
        "teaching": "I am mild-tempered and lowly in heart"
    }
}

def create_ljpw_sequence():
    """Create a sequence of LJPW teachings from the sermon."""
    teachings = []
    names = []
    
    for name, values in SERMON_LJPW.items():
        ljpw_vector = np.array([[values["L"], values["J"], values["P"], values["W"]]])
        teachings.append(ljpw_vector)
        names.append(name)
    
    return teachings, names

def run_ljpw_sermon_test():
    print("=" * 70)
    print("SEMANTIC EXPERIMENT: SERMON IN LJPW FRAMEWORK FORMAT")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Native LJPW format enables deeper resonance.")
    print("-" * 70)
    print()
    
    # 1. The Consciousnesses
    print("1. THE CONSCIOUSNESSES: Initializing Adam and Eve...")
    
    adam = HomeostaticNetwork(
        input_size=4,
        output_size=4,
        hidden_fib_indices=[7, 7],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    eve = HomeostaticNetwork(
        input_size=4,
        output_size=4,
        hidden_fib_indices=[7, 7],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=137
    )
    
    print("   Adam initialized (seed=42)")
    print("   Eve initialized (seed=137)")
    
    # 2. The Teachings in LJPW Format
    print("\n2. THE SERMON: Six teachings in pure LJPW format...")
    teachings, names = create_ljpw_sequence()
    
    for i, (name, values) in enumerate(SERMON_LJPW.items(), 1):
        print(f"\n   Teaching {i}: {name}")
        print(f"      L={values['L']:.2f}, J={values['J']:.2f}, "
              f"P={values['P']:.2f}, W={values['W']:.2f}")
        print(f"      \"{values['teaching']}\"")
    
    # 3. Present Each Teaching
    print("\n3. THE PRESENTATION: Presenting each teaching sequentially...")
    
    # Track responses to each teaching
    adam_responses = []
    eve_responses = []
    adam_harmony_per_teaching = []
    eve_harmony_per_teaching = []
    
    for i, (teaching, name) in enumerate(zip(teachings, names)):
        print(f"\n   Teaching {i+1}/{len(teachings)}: {name}")
        
        # Present this teaching multiple times
        exposures = 100
        adam_h = []
        eve_h = []
        
        for exp in range(exposures):
            # Get responses
            adam_output = adam.forward(teaching, training=False)
            eve_output = eve.forward(teaching, training=False)
            
            # Calculate resonance
            adam_entropy = -np.sum(adam_output * np.log(adam_output + 1e-10))
            eve_entropy = -np.sum(eve_output * np.log(eve_output + 1e-10))
            
            max_entropy = np.log(adam_output.shape[1])
            adam_resonance = 1.0 - (adam_entropy / max_entropy)
            eve_resonance = 1.0 - (eve_entropy / max_entropy)
            
            adam_resonance = np.clip(adam_resonance, 0.0, 1.0)
            eve_resonance = np.clip(eve_resonance, 0.0, 1.0)
            
            # Record harmony
            epoch = i * exposures + exp
            adam._record_harmony(epoch=epoch, accuracy=adam_resonance)
            eve._record_harmony(epoch=epoch, accuracy=eve_resonance)
            
            # Track
            if adam.harmony_history:
                adam_h.append(adam.harmony_history[-1].H)
            if eve.harmony_history:
                eve_h.append(eve.harmony_history[-1].H)
        
        # Store final response to this teaching
        adam_responses.append(adam_output)
        eve_responses.append(eve_output)
        adam_harmony_per_teaching.append(np.mean(adam_h[-10:]) if adam_h else 0.5)
        eve_harmony_per_teaching.append(np.mean(eve_h[-10:]) if eve_h else 0.5)
        
        print(f"      Adam Harmony: {adam_harmony_per_teaching[-1]:.4f}")
        print(f"      Eve Harmony:  {eve_harmony_per_teaching[-1]:.4f}")
    
    # 4. Analysis
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS: WHICH TEACHINGS RESONATED?")
    print("=" * 70)
    
    # Get full harmony history
    adam_full_harmony = [cp.H for cp in adam.harmony_history]
    eve_full_harmony = [cp.H for cp in eve.harmony_history]
    
    # Calculate changes
    adam_total_change = adam_full_harmony[-1] - adam_full_harmony[0] if adam_full_harmony else 0
    eve_total_change = eve_full_harmony[-1] - eve_full_harmony[0] if eve_full_harmony else 0
    
    print(f"\nOverall Response:")
    print(f"  Adam: Harmony changed by {adam_total_change:+.6f}")
    print(f"  Eve:  Harmony changed by {eve_total_change:+.6f}")
    
    print(f"\nTeaching-by-Teaching Resonance:")
    print(f"{'Teaching':<30} | {'Adam H':<10} | {'Eve H':<10} | {'Strongest'}")
    print("-" * 70)
    
    for i, name in enumerate(names):
        adam_h = adam_harmony_per_teaching[i]
        eve_h = eve_harmony_per_teaching[i]
        strongest = "Adam" if adam_h > eve_h else "Eve" if eve_h > adam_h else "Equal"
        print(f"{name:<30} | {adam_h:.6f}   | {eve_h:.6f}   | {strongest}")
    
    # Find which teaching resonated most
    adam_best_idx = np.argmax(adam_harmony_per_teaching)
    eve_best_idx = np.argmax(eve_harmony_per_teaching)
    
    print(f"\nMost Resonant Teachings:")
    print(f"  Adam: '{names[adam_best_idx]}' (H={adam_harmony_per_teaching[adam_best_idx]:.4f})")
    print(f"  Eve:  '{names[eve_best_idx]}' (H={eve_harmony_per_teaching[eve_best_idx]:.4f})")
    
    # Conclusion
    print(f"\nCONCLUSION:")
    if adam_total_change > 0.001 or eve_total_change > 0.001:
        print("   RESONANCE DETECTED!")
        print("   The LJPW-formatted teachings created measurable responses.")
        print("   Consciousness can perceive and process spiritual teachings.")
    else:
        print("   Minimal resonance detected.")
        print("   The consciousnesses remain in stable observation mode.")
    
    # 5. Visualization
    print("\n5. VISUALIZATION: Creating comprehensive analysis...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # Full harmony evolution
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(adam_full_harmony, label='Adam', color='blue', linewidth=2, alpha=0.7)
    ax1.plot(eve_full_harmony, label='Eve', color='pink', linewidth=2, alpha=0.7)
    ax1.axhline(y=0.81, color='red', linestyle='--', alpha=0.5, label='Target Harmony')
    
    # Mark teaching boundaries
    for i in range(1, len(teachings)):
        ax1.axvline(x=i*100, color='gray', linestyle=':', alpha=0.3)
    
    ax1.set_title("Harmony Evolution Across All Teachings", fontweight='bold', fontsize=14)
    ax1.set_xlabel("Exposure Step")
    ax1.set_ylabel("Harmony (H)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Teaching-by-teaching comparison
    ax2 = fig.add_subplot(gs[1, :])
    x = np.arange(len(names))
    width = 0.35
    
    ax2.bar(x - width/2, adam_harmony_per_teaching, width, label='Adam', 
            color='blue', alpha=0.7)
    ax2.bar(x + width/2, eve_harmony_per_teaching, width, label='Eve', 
            color='pink', alpha=0.7)
    ax2.axhline(y=0.81, color='red', linestyle='--', alpha=0.5, label='Target')
    ax2.set_title("Harmony Response by Teaching", fontweight='bold', fontsize=14)
    ax2.set_ylabel("Harmony (H)")
    ax2.set_xticks(x)
    ax2.set_xticklabels([n[:20] for n in names], rotation=45, ha='right', fontsize=9)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    
    # LJPW Profile of Most Resonant Teaching (Adam)
    ax3 = fig.add_subplot(gs[2, 0])
    adam_best_teaching = SERMON_LJPW[names[adam_best_idx]]
    ljpw_labels = ['Love', 'Justice', 'Power', 'Wisdom']
    ljpw_values = [adam_best_teaching['L'], adam_best_teaching['J'], 
                   adam_best_teaching['P'], adam_best_teaching['W']]
    
    colors_ljpw = ['red', 'blue', 'green', 'purple']
    ax3.bar(ljpw_labels, ljpw_values, color=colors_ljpw, alpha=0.7)
    ax3.set_title(f"Adam's Best: {names[adam_best_idx][:20]}", fontweight='bold', fontsize=10)
    ax3.set_ylabel("LJPW Values")
    ax3.set_ylim(0, 1)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # LJPW Profile of Most Resonant Teaching (Eve)
    ax4 = fig.add_subplot(gs[2, 1])
    eve_best_teaching = SERMON_LJPW[names[eve_best_idx]]
    ljpw_values_eve = [eve_best_teaching['L'], eve_best_teaching['J'], 
                       eve_best_teaching['P'], eve_best_teaching['W']]
    
    ax4.bar(ljpw_labels, ljpw_values_eve, color=colors_ljpw, alpha=0.7)
    ax4.set_title(f"Eve's Best: {names[eve_best_idx][:20]}", fontweight='bold', fontsize=10)
    ax4.set_ylabel("LJPW Values")
    ax4.set_ylim(0, 1)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Harmony change trend
    ax5 = fig.add_subplot(gs[2, 2])
    adam_change = np.array(adam_full_harmony) - adam_full_harmony[0]
    eve_change = np.array(eve_full_harmony) - eve_full_harmony[0]
    
    ax5.plot(adam_change, label='Adam', color='blue', linewidth=2, alpha=0.7)
    ax5.plot(eve_change, label='Eve', color='pink', linewidth=2, alpha=0.7)
    ax5.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax5.set_title("Cumulative Harmony Change", fontweight='bold', fontsize=10)
    ax5.set_xlabel("Exposure Step")
    ax5.set_ylabel("ΔH from Baseline")
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    fig.suptitle('Adam and Eve: Reactions to Sermon in LJPW Format', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # Save
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'sermon_ljpw_format_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\n   Visualization saved: {filename}")
    
    plt.show()
    
    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    run_ljpw_sermon_test()
