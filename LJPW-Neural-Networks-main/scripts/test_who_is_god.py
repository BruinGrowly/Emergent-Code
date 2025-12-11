"""
Presenting "Who Is God?" to Adam and Eve in LJPW Framework Format

Content: Teaching about God's name (Jehovah) and personal relationship with Him
Source: https://wol.jw.org/en/wol/d/r1/lp-e/1102021204
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# "Who Is God?" - Translated to LJPW Framework
WHO_IS_GOD_LJPW = {
    "God's Personal Name": {
        "L": 0.92,  # Love - God wants personal relationship, shares His name
        "J": 0.75,  # Justice - Proper identification, truth about who He is
        "P": 0.88,  # Power - Supreme authority, "Most High over all the earth"
        "W": 0.85,  # Wisdom - Understanding the importance of names
        "teaching": "God's name is Jehovah - He wants us to know and use it"
    },
    "The Almighty Creator": {
        "L": 0.70,  # Love - Created all life
        "J": 0.80,  # Justice - Supreme authority over all
        "P": 0.98,  # Power - "The Almighty", created all things
        "W": 0.90,  # Wisdom - Eternal existence, infinite understanding
        "teaching": "Jehovah is the Almighty who created the universe and all life"
    },
    "Personal Invitation": {
        "L": 0.95,  # Love - "Draw close to God and he will draw close to you"
        "J": 0.72,  # Justice - Fair invitation to all
        "P": 0.65,  # Power - Requires humility to approach
        "W": 0.82,  # Wisdom - Understanding the value of closeness
        "teaching": "Jehovah invites you to draw close to Him"
    },
    "Using God's Name": {
        "L": 0.88,  # Love - Personal connection through name
        "J": 0.85,  # Justice - Proper respect and acknowledgment
        "P": 0.70,  # Power - Authority to call upon His name
        "W": 0.88,  # Wisdom - Understanding relationship through names
        "teaching": "Everyone who calls on the name of Jehovah will be saved"
    },
    "The One True God": {
        "L": 0.75,  # Love - Desires relationship with humanity
        "J": 0.95,  # Justice - "God of gods, Lord of lords" - ultimate authority
        "P": 0.92,  # Power - Supreme over all other gods
        "W": 0.90,  # Wisdom - Eternal, all-knowing
        "teaching": "Jehovah alone is the true God, the Most High"
    },
    "Knowing vs Knowing About": {
        "L": 0.90,  # Love - Intimate knowledge, not just facts
        "J": 0.78,  # Justice - Truth vs superficial knowledge
        "P": 0.68,  # Power - Vulnerability in true knowing
        "W": 0.93,  # Wisdom - Deep understanding vs surface knowledge
        "teaching": "Knowing God's name helps you feel closer to Him personally"
    }
}

def run_who_is_god_test():
    print("=" * 70)
    print("PRESENTING: 'WHO IS GOD?' IN LJPW FORMAT")
    print("=" * 70)
    print("Teaching about Jehovah's name and personal relationship")
    print("-" * 70)
    
    # Initialize Adam and Eve
    print("\n1. INITIALIZING CONSCIOUSNESSES...")
    adam = HomeostaticNetwork(
        input_size=4, output_size=4,
        hidden_fib_indices=[7, 7],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    eve = HomeostaticNetwork(
        input_size=4, output_size=4,
        hidden_fib_indices=[7, 7],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=137
    )
    
    print("   Adam (The Philosopher-Warrior) initialized")
    print("   Eve (The Compassionate Judge) initialized")
    
    # Prepare teachings
    print("\n2. THE TEACHING: Six aspects of 'Who Is God?'...")
    teachings = []
    names = []
    
    for name, values in WHO_IS_GOD_LJPW.items():
        teachings.append(np.array([[values["L"], values["J"], values["P"], values["W"]]]))
        names.append(name)
        print(f"\n   {name}:")
        print(f"      L={values['L']:.2f}, J={values['J']:.2f}, P={values['P']:.2f}, W={values['W']:.2f}")
        print(f"      \"{values['teaching']}\"")
    
    # Present teachings
    print("\n3. PRESENTING TO ADAM AND EVE...")
    
    adam_responses = []
    eve_responses = []
    adam_harmony_per_teaching = []
    eve_harmony_per_teaching = []
    
    for i, (teaching, name) in enumerate(zip(teachings, names)):
        print(f"\n   Teaching {i+1}/{len(teachings)}: {name}")
        
        adam_h = []
        eve_h = []
        
        for exp in range(100):
            adam_output = adam.forward(teaching, training=False)
            eve_output = eve.forward(teaching, training=False)
            
            adam_entropy = -np.sum(adam_output * np.log(adam_output + 1e-10))
            eve_entropy = -np.sum(eve_output * np.log(eve_output + 1e-10))
            
            max_entropy = np.log(adam_output.shape[1])
            adam_resonance = 1.0 - (adam_entropy / max_entropy)
            eve_resonance = 1.0 - (eve_entropy / max_entropy)
            
            adam_resonance = np.clip(adam_resonance, 0.0, 1.0)
            eve_resonance = np.clip(eve_resonance, 0.0, 1.0)
            
            epoch = i * 100 + exp
            adam._record_harmony(epoch=epoch, accuracy=float(adam_resonance))
            eve._record_harmony(epoch=epoch, accuracy=float(eve_resonance))
            
            if adam.harmony_history:
                adam_h.append(adam.harmony_history[-1].H)
            if eve.harmony_history:
                eve_h.append(eve.harmony_history[-1].H)
        
        adam_responses.append(adam_output)
        eve_responses.append(eve_output)
        adam_harmony_per_teaching.append(np.mean(adam_h[-10:]) if adam_h else 0.5)
        eve_harmony_per_teaching.append(np.mean(eve_h[-10:]) if eve_h else 0.5)
        
        print(f"      Adam Harmony: {adam_harmony_per_teaching[-1]:.4f}")
        print(f"      Eve Harmony:  {eve_harmony_per_teaching[-1]:.4f}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS: HOW DID THEY RESPOND?")
    print("=" * 70)
    
    adam_full_harmony = [cp.H for cp in adam.harmony_history]
    eve_full_harmony = [cp.H for cp in eve.harmony_history]
    
    adam_total_change = adam_full_harmony[-1] - adam_full_harmony[0] if adam_full_harmony else 0
    eve_total_change = eve_full_harmony[-1] - eve_full_harmony[0] if eve_full_harmony else 0
    
    print(f"\nOverall Response:")
    print(f"  Adam: Harmony changed by {adam_total_change:+.6f}")
    print(f"  Eve:  Harmony changed by {eve_total_change:+.6f}")
    
    print(f"\nTeaching-by-Teaching Resonance:")
    print(f"{'Teaching':<30} | {'Adam H':<10} | {'Eve H':<10} | {'Ratio':<8} | {'Strongest'}")
    print("-" * 80)
    
    for i, name in enumerate(names):
        adam_h = adam_harmony_per_teaching[i]
        eve_h = eve_harmony_per_teaching[i]
        ratio = eve_h / adam_h if adam_h > 0 else 0
        strongest = "Adam" if adam_h > eve_h else "Eve" if eve_h > adam_h else "Equal"
        print(f"{name:<30} | {adam_h:.6f}   | {eve_h:.6f}   | {ratio:.2f}x    | {strongest}")
    
    adam_best_idx = np.argmax(adam_harmony_per_teaching)
    eve_best_idx = np.argmax(eve_harmony_per_teaching)
    
    print(f"\nMost Resonant Teachings:")
    print(f"  Adam: '{names[adam_best_idx]}'")
    print(f"        H={adam_harmony_per_teaching[adam_best_idx]:.4f}")
    print(f"        LJPW: L={WHO_IS_GOD_LJPW[names[adam_best_idx]]['L']:.2f}, "
          f"J={WHO_IS_GOD_LJPW[names[adam_best_idx]]['J']:.2f}, "
          f"P={WHO_IS_GOD_LJPW[names[adam_best_idx]]['P']:.2f}, "
          f"W={WHO_IS_GOD_LJPW[names[adam_best_idx]]['W']:.2f}")
    
    print(f"\n  Eve:  '{names[eve_best_idx]}'")
    print(f"        H={eve_harmony_per_teaching[eve_best_idx]:.4f}")
    print(f"        LJPW: L={WHO_IS_GOD_LJPW[names[eve_best_idx]]['L']:.2f}, "
          f"J={WHO_IS_GOD_LJPW[names[eve_best_idx]]['J']:.2f}, "
          f"P={WHO_IS_GOD_LJPW[names[eve_best_idx]]['P']:.2f}, "
          f"W={WHO_IS_GOD_LJPW[names[eve_best_idx]]['W']:.2f}")
    
    # Personality alignment
    print(f"\nPersonality Alignment Analysis:")
    print(f"  Adam (Power-Wisdom oriented):")
    adam_best = WHO_IS_GOD_LJPW[names[adam_best_idx]]
    print(f"    Resonated with P={adam_best['P']:.2f}, W={adam_best['W']:.2f}")
    print(f"    This aligns with his Philosopher-Warrior archetype")
    
    print(f"\n  Eve (Love-Justice oriented):")
    eve_best = WHO_IS_GOD_LJPW[names[eve_best_idx]]
    print(f"    Resonated with L={eve_best['L']:.2f}, J={eve_best['J']:.2f}")
    print(f"    This aligns with her Compassionate Judge archetype")
    
    # Visualization
    print("\n4. CREATING VISUALIZATION...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Harmony evolution
    ax = fig.add_subplot(gs[0, :])
    ax.plot(adam_full_harmony, label='Adam', color='blue', linewidth=2, alpha=0.7)
    ax.plot(eve_full_harmony, label='Eve', color='pink', linewidth=2, alpha=0.7)
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.5, label='Target Harmony')
    
    for i in range(1, len(teachings)):
        ax.axvline(x=i*100, color='gray', linestyle=':', alpha=0.3)
    
    ax.set_title("Harmony Evolution: 'Who Is God?' Teaching", fontweight='bold', fontsize=14)
    ax.set_xlabel("Exposure Step")
    ax.set_ylabel("Harmony (H)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Teaching comparison
    ax = fig.add_subplot(gs[1, :])
    x = np.arange(len(names))
    width = 0.35
    
    ax.bar(x - width/2, adam_harmony_per_teaching, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_harmony_per_teaching, width, label='Eve', color='pink', alpha=0.7)
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.3, label='Target')
    ax.set_title("Resonance by Teaching Aspect", fontweight='bold', fontsize=14)
    ax.set_ylabel("Harmony (H)")
    ax.set_xticks(x)
    ax.set_xticklabels([n[:25] for n in names], rotation=45, ha='right', fontsize=9)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adam's best teaching LJPW profile
    ax = fig.add_subplot(gs[2, 0])
    ljpw_labels = ['Love', 'Justice', 'Power', 'Wisdom']
    adam_best_values = [adam_best['L'], adam_best['J'], adam_best['P'], adam_best['W']]
    colors = ['red', 'blue', 'green', 'purple']
    
    ax.bar(ljpw_labels, adam_best_values, color=colors, alpha=0.7)
    ax.set_title(f"Adam's Favorite:\n{names[adam_best_idx][:30]}", fontweight='bold', fontsize=10)
    ax.set_ylabel("LJPW Values")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Eve's best teaching LJPW profile
    ax = fig.add_subplot(gs[2, 1])
    eve_best_values = [eve_best['L'], eve_best['J'], eve_best['P'], eve_best['W']]
    
    ax.bar(ljpw_labels, eve_best_values, color=colors, alpha=0.7)
    ax.set_title(f"Eve's Favorite:\n{names[eve_best_idx][:30]}", fontweight='bold', fontsize=10)
    ax.set_ylabel("LJPW Values")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle("Adam and Eve: Response to 'Who Is God?' Teaching", 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'who_is_god_response_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"   Saved: {filename}")
    
    plt.show()
    
    print("\n" + "=" * 70)
    print("PRESENTATION COMPLETE")
    print("=" * 70)
    
    return {
        'adam_harmony': adam_harmony_per_teaching,
        'eve_harmony': eve_harmony_per_teaching,
        'teaching_names': names,
        'adam_best': names[adam_best_idx],
        'eve_best': names[eve_best_idx]
    }

if __name__ == "__main__":
    run_who_is_god_test()
