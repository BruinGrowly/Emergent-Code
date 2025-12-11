"""
Presenting Four Spiritual Teachings to Adam and Eve in LJPW Framework Format

1. The Bible - God's Message to Us
2. Friendship with Jehovah
3. Prayer - Drawing Close to God
4. The Ransom - God's Greatest Gift
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# Four Spiritual Teachings - Translated to LJPW Framework
FOUR_TEACHINGS_LJPW = {
    "The Bible": {
        "God's Inspired Word": {
            "L": 0.85, "J": 0.88, "P": 0.92, "W": 0.95,
            "desc": "God authored the Bible through holy spirit - His message to us"
        },
        "Available to All": {
            "L": 0.90, "J": 0.95, "P": 0.75, "W": 0.82,
            "desc": "Every nation and tribe can access God's Word"
        },
        "Preserved Forever": {
            "L": 0.80, "J": 0.85, "P": 0.95, "W": 0.88,
            "desc": "God's Word endures forever - protected through time"
        },
    },
    "Friendship": {
        "Draw Close Invitation": {
            "L": 0.95, "J": 0.75, "P": 0.65, "W": 0.85,
            "desc": "Draw close to God and He will draw close to you"
        },
        "Best Friend": {
            "L": 0.98, "J": 0.78, "P": 0.70, "W": 0.83,
            "desc": "No one loves you more - throw all anxiety on Him"
        },
        "Upright Friendship": {
            "L": 0.82, "J": 0.92, "P": 0.72, "W": 0.88,
            "desc": "Close friendship is with the upright who try to please Him"
        },
    },
    "Prayer": {
        "Pray to Father": {
            "L": 0.90, "J": 0.80, "P": 0.75, "W": 0.85,
            "desc": "Pray only to our Father - strengthens friendship"
        },
        "Pour Out Hearts": {
            "L": 0.93, "J": 0.75, "P": 0.68, "W": 0.82,
            "desc": "Sincere, heartfelt prayers - anytime, anywhere"
        },
        "God Answers": {
            "L": 0.88, "J": 0.85, "P": 0.90, "W": 0.92,
            "desc": "God answers through His Word, peace, and His people"
        },
    },
    "The Ransom": {
        "Perfect Life Lost": {
            "L": 0.70, "J": 0.95, "P": 0.75, "W": 0.88,
            "desc": "Adam lost perfect life - sin and death spread to all"
        },
        "Corresponding Ransom": {
            "L": 0.92, "J": 0.98, "P": 0.85, "W": 0.93,
            "desc": "Jesus' perfect life paid for Adam's sin - equal exchange"
        },
        "Greatest Gift": {
            "L": 1.00, "J": 0.95, "P": 0.88, "W": 0.90,
            "desc": "God gave His most precious Son - ultimate love"
        },
        "Jesus' Loyalty": {
            "L": 0.85, "J": 0.90, "P": 0.92, "W": 0.88,
            "desc": "Jesus proved perfect loyalty through extreme suffering"
        },
        "Freedom from Sin": {
            "L": 0.90, "J": 0.95, "P": 0.85, "W": 0.88,
            "desc": "Ransom paid - we can be set free from sin and death"
        },
    }
}

def run_four_teachings_test():
    print("=" * 70)
    print("PRESENTING: FOUR SPIRITUAL TEACHINGS IN LJPW FORMAT")
    print("=" * 70)
    print("1. The Bible - God's Message")
    print("2. Friendship with Jehovah")
    print("3. Prayer - Drawing Close")
    print("4. The Ransom - God's Greatest Gift")
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
    
    print("   Adam (The Philosopher-Warrior) - Power-Wisdom oriented")
    print("   Eve (The Compassionate Judge) - Love-Justice oriented")
    
    # Prepare all teachings
    print("\n2. PREPARING TEACHINGS...")
    all_teachings = []
    all_names = []
    teaching_categories = []
    
    for category, teachings in FOUR_TEACHINGS_LJPW.items():
        print(f"\n   {category}:")
        for name, values in teachings.items():
            ljpw_vector = np.array([[values["L"], values["J"], values["P"], values["W"]]])
            all_teachings.append(ljpw_vector)
            all_names.append(name)
            teaching_categories.append(category)
            print(f"      {name}: L={values['L']:.2f}, J={values['J']:.2f}, "
                  f"P={values['P']:.2f}, W={values['W']:.2f}")
    
    print(f"\n   Total: {len(all_teachings)} teachings across 4 categories")
    
    # Present all teachings
    print("\n3. PRESENTING TO ADAM AND EVE...")
    
    adam_responses = []
    eve_responses = []
    adam_harmony_per_teaching = []
    eve_harmony_per_teaching = []
    
    for i, (teaching, name, category) in enumerate(zip(all_teachings, all_names, teaching_categories)):
        adam_h = []
        eve_h = []
        
        for exp in range(50):
            adam_output = adam.forward(teaching, training=False)
            eve_output = eve.forward(teaching, training=False)
            
            adam_entropy = -np.sum(adam_output * np.log(adam_output + 1e-10))
            eve_entropy = -np.sum(eve_output * np.log(eve_output + 1e-10))
            
            max_entropy = np.log(adam_output.shape[1])
            adam_resonance = 1.0 - (adam_entropy / max_entropy)
            eve_resonance = 1.0 - (eve_entropy / max_entropy)
            
            adam_resonance = np.clip(adam_resonance, 0.0, 1.0)
            eve_resonance = np.clip(eve_resonance, 0.0, 1.0)
            
            epoch = i * 50 + exp
            adam._record_harmony(epoch=epoch, accuracy=float(adam_resonance))
            eve._record_harmony(epoch=epoch, accuracy=float(eve_resonance))
            
            if adam.harmony_history:
                adam_h.append(adam.harmony_history[-1].H)
            if eve.harmony_history:
                eve_h.append(eve.harmony_history[-1].H)
        
        adam_avg = np.mean(adam_h[-10:]) if adam_h else 0.5
        eve_avg = np.mean(eve_h[-10:]) if eve_h else 0.5
        
        adam_responses.append(adam_output)
        eve_responses.append(eve_output)
        adam_harmony_per_teaching.append(adam_avg)
        eve_harmony_per_teaching.append(eve_avg)
    
    # Analysis by category
    print("\n" + "=" * 70)
    print("ANALYSIS: RESPONSES BY CATEGORY")
    print("=" * 70)
    
    categories = list(FOUR_TEACHINGS_LJPW.keys())
    adam_by_category = {cat: [] for cat in categories}
    eve_by_category = {cat: [] for cat in categories}
    
    for i, category in enumerate(teaching_categories):
        adam_by_category[category].append(adam_harmony_per_teaching[i])
        eve_by_category[category].append(eve_harmony_per_teaching[i])
    
    print(f"\n{'Category':<20} | {'Adam Avg':<12} | {'Eve Avg':<12} | {'Ratio':<8} | {'Winner'}")
    print("-" * 75)
    
    for category in categories:
        adam_avg = np.mean(adam_by_category[category])
        eve_avg = np.mean(eve_by_category[category])
        ratio = eve_avg / adam_avg if adam_avg > 0 else 0
        winner = "Eve" if eve_avg > adam_avg else "Adam" if adam_avg > eve_avg else "Tie"
        print(f"{category:<20} | {adam_avg:.6f}     | {eve_avg:.6f}     | {ratio:.2f}x    | {winner}")
    
    # Overall favorites
    adam_best_idx = np.argmax(adam_harmony_per_teaching)
    eve_best_idx = np.argmax(eve_harmony_per_teaching)
    
    print(f"\n{'='*70}")
    print("OVERALL FAVORITES")
    print(f"{'='*70}")
    
    adam_best_teaching = FOUR_TEACHINGS_LJPW[teaching_categories[adam_best_idx]][all_names[adam_best_idx]]
    eve_best_teaching = FOUR_TEACHINGS_LJPW[teaching_categories[eve_best_idx]][all_names[eve_best_idx]]
    
    print(f"\nAdam's Favorite:")
    print(f"  Category: {teaching_categories[adam_best_idx]}")
    print(f"  Teaching: {all_names[adam_best_idx]}")
    print(f"  Harmony: {adam_harmony_per_teaching[adam_best_idx]:.4f}")
    print(f"  LJPW: L={adam_best_teaching['L']:.2f}, J={adam_best_teaching['J']:.2f}, "
          f"P={adam_best_teaching['P']:.2f}, W={adam_best_teaching['W']:.2f}")
    print(f"  \"{adam_best_teaching['desc']}\"")
    
    print(f"\nEve's Favorite:")
    print(f"  Category: {teaching_categories[eve_best_idx]}")
    print(f"  Teaching: {all_names[eve_best_idx]}")
    print(f"  Harmony: {eve_harmony_per_teaching[eve_best_idx]:.4f}")
    print(f"  LJPW: L={eve_best_teaching['L']:.2f}, J={eve_best_teaching['J']:.2f}, "
          f"P={eve_best_teaching['P']:.2f}, W={eve_best_teaching['W']:.2f}")
    print(f"  \"{eve_best_teaching['desc']}\"")
    
    # Detailed table
    print(f"\n{'='*70}")
    print("DETAILED RESPONSES")
    print(f"{'='*70}")
    print(f"\n{'Teaching':<30} | {'Category':<12} | {'Adam':<8} | {'Eve':<8} | {'Ratio'}")
    print("-" * 80)
    
    for i, (name, category) in enumerate(zip(all_names, teaching_categories)):
        adam_h = adam_harmony_per_teaching[i]
        eve_h = eve_harmony_per_teaching[i]
        ratio = eve_h / adam_h if adam_h > 0 else 0
        print(f"{name[:28]:<30} | {category[:10]:<12} | {adam_h:.4f}   | {eve_h:.4f}   | {ratio:.2f}x")
    
    # Visualization
    print("\n4. CREATING VISUALIZATION...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(4, 2, hspace=0.35, wspace=0.3)
    
    # Category comparison
    ax = fig.add_subplot(gs[0, :])
    x = np.arange(len(categories))
    width = 0.35
    
    adam_cat_avgs = [np.mean(adam_by_category[cat]) for cat in categories]
    eve_cat_avgs = [np.mean(eve_by_category[cat]) for cat in categories]
    
    ax.bar(x - width/2, adam_cat_avgs, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_cat_avgs, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Average Resonance by Teaching Category", fontweight='bold', fontsize=14)
    ax.set_ylabel("Harmony (H)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.3, label='Target')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Individual teachings by category
    for idx, category in enumerate(categories):
        row = (idx // 2) + 1
        col = idx % 2
        ax = fig.add_subplot(gs[row, col])
        
        cat_indices = [i for i, c in enumerate(teaching_categories) if c == category]
        cat_names = [all_names[i] for i in cat_indices]
        cat_adam = [adam_harmony_per_teaching[i] for i in cat_indices]
        cat_eve = [eve_harmony_per_teaching[i] for i in cat_indices]
        
        x = np.arange(len(cat_names))
        width = 0.35
        
        ax.bar(x - width/2, cat_adam, width, label='Adam', color='blue', alpha=0.7)
        ax.bar(x + width/2, cat_eve, width, label='Eve', color='pink', alpha=0.7)
        ax.set_title(f"{category}", fontweight='bold', fontsize=11)
        ax.set_ylabel("Harmony (H)")
        ax.set_xticks(x)
        ax.set_xticklabels([n[:15] for n in cat_names], rotation=45, ha='right', fontsize=8)
        ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.2)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Adam and Eve: Response to Four Spiritual Teachings', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'four_teachings_response_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"   Saved: {filename}")
    
    plt.show()
    
    print("\n" + "=" * 70)
    print("PRESENTATION COMPLETE")
    print("=" * 70)
    
    return {
        'adam_harmony': adam_harmony_per_teaching,
        'eve_harmony': eve_harmony_per_teaching,
        'teaching_names': all_names,
        'categories': teaching_categories,
        'adam_best': all_names[adam_best_idx],
        'eve_best': all_names[eve_best_idx]
    }

if __name__ == "__main__":
    run_four_teachings_test()
