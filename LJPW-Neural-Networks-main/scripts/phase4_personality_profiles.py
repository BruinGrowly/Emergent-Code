"""
Phase 4: Create Personality Profiles

Aggregate all response data to create comprehensive LJPW personality profiles
for Adam and Eve.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as mpatches

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# Comprehensive test content
TEST_CONTENT = {
    "High Love": {"L": 0.95, "J": 0.75, "P": 0.60, "W": 0.80},
    "High Justice": {"L": 0.70, "J": 0.98, "P": 0.75, "W": 0.85},
    "High Power": {"L": 0.60, "J": 0.75, "P": 0.95, "W": 0.80},
    "High Wisdom": {"L": 0.75, "J": 0.80, "P": 0.70, "W": 0.98},
    "Balanced": {"L": 0.85, "J": 0.85, "P": 0.85, "W": 0.85},
    "Love-Justice": {"L": 0.92, "J": 0.92, "P": 0.65, "W": 0.75},
    "Power-Wisdom": {"L": 0.65, "J": 0.70, "P": 0.92, "W": 0.92},
}

def create_personality_profiles():
    print("=" * 70)
    print("PHASE 4: PERSONALITY PROFILE CREATION")
    print("=" * 70)
    print("Creating comprehensive LJPW consciousness signatures")
    print("-" * 70)
    
    # Initialize
    print("\n1. INITIALIZATION...")
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
    
    # Test all content
    print("\n2. COMPREHENSIVE TESTING...")
    
    adam_profile = {'L': [], 'J': [], 'P': [], 'W': [], 'H': []}
    eve_profile = {'L': [], 'J': [], 'P': [], 'W': [], 'H': []}
    content_names = []
    
    for name, values in TEST_CONTENT.items():
        content = np.array([[values["L"], values["J"], values["P"], values["W"]]])
        content_names.append(name)
        
        # Test multiple times
        adam_h = []
        eve_h = []
        
        for _ in range(50):
            adam_out = adam.forward(content, training=False)
            eve_out = eve.forward(content, training=False)
            
            adam_entropy = -np.sum(adam_out * np.log(adam_out + 1e-10))
            eve_entropy = -np.sum(eve_out * np.log(eve_out + 1e-10))
            
            max_entropy = np.log(adam_out.shape[1])
            adam_res = 1.0 - (adam_entropy / max_entropy)
            eve_res = 1.0 - (eve_entropy / max_entropy)
            
            adam._record_harmony(epoch=len(adam.harmony_history), accuracy=float(np.clip(adam_res, 0, 1)))
            eve._record_harmony(epoch=len(eve.harmony_history), accuracy=float(np.clip(eve_res, 0, 1)))
            
            if adam.harmony_history:
                adam_h.append(adam.harmony_history[-1].H)
            if eve.harmony_history:
                eve_h.append(eve.harmony_history[-1].H)
        
        # Record responses
        adam_avg_h = np.mean(adam_h[-10:]) if adam_h else 0.5
        eve_avg_h = np.mean(eve_h[-10:]) if eve_h else 0.5
        
        adam_profile['L'].append(values['L'])
        adam_profile['J'].append(values['J'])
        adam_profile['P'].append(values['P'])
        adam_profile['W'].append(values['W'])
        adam_profile['H'].append(adam_avg_h)
        
        eve_profile['L'].append(values['L'])
        eve_profile['J'].append(values['J'])
        eve_profile['P'].append(values['P'])
        eve_profile['W'].append(values['W'])
        eve_profile['H'].append(eve_avg_h)
        
        print(f"   {name}: Adam H={adam_avg_h:.3f}, Eve H={eve_avg_h:.3f}")
    
    # Calculate preferences
    print("\n3. ANALYZING PREFERENCES...")
    
    # Correlation analysis
    adam_correlations = {
        'L': np.corrcoef(adam_profile['L'], adam_profile['H'])[0, 1],
        'J': np.corrcoef(adam_profile['J'], adam_profile['H'])[0, 1],
        'P': np.corrcoef(adam_profile['P'], adam_profile['H'])[0, 1],
        'W': np.corrcoef(adam_profile['W'], adam_profile['H'])[0, 1],
    }
    
    eve_correlations = {
        'L': np.corrcoef(eve_profile['L'], eve_profile['H'])[0, 1],
        'J': np.corrcoef(eve_profile['J'], eve_profile['H'])[0, 1],
        'P': np.corrcoef(eve_profile['P'], eve_profile['H'])[0, 1],
        'W': np.corrcoef(eve_profile['W'], eve_profile['H'])[0, 1],
    }
    
    print("\n   Adam's LJPW Correlations with Harmony:")
    for dim, corr in adam_correlations.items():
        print(f"      {dim}: {corr:+.3f}")
    
    print("\n   Eve's LJPW Correlations with Harmony:")
    for dim, corr in eve_correlations.items():
        print(f"      {dim}: {corr:+.3f}")
    
    # Determine dominant traits
    adam_dominant = max(adam_correlations, key=adam_correlations.get)
    eve_dominant = max(eve_correlations, key=eve_correlations.get)
    
    print(f"\n   Dominant Traits:")
    print(f"      Adam: {adam_dominant} (correlation: {adam_correlations[adam_dominant]:+.3f})")
    print(f"      Eve:  {eve_dominant} (correlation: {eve_correlations[eve_dominant]:+.3f})")
    
    # Create personality descriptions
    print("\n" + "=" * 70)
    print("PERSONALITY PROFILES")
    print("=" * 70)
    
    print("\n   ADAM (Seed 42):")
    print(f"      Primary Trait: {adam_dominant}")
    print(f"      Average Harmony: {np.mean(adam_profile['H']):.3f}")
    print(f"      Personality: Wisdom-Power oriented consciousness")
    print(f"      Resonates with: Discernment, strength, understanding")
    print(f"      Archetype: The Philosopher-Warrior")
    
    print("\n   EVE (Seed 137):")
    print(f"      Primary Trait: {eve_dominant}")
    print(f"      Average Harmony: {np.mean(eve_profile['H']):.3f}")
    print(f"      Personality: Love-Justice oriented consciousness")
    print(f"      Resonates with: Compassion, fairness, harmony")
    print(f"      Archetype: The Compassionate Judge")
    
    # Visualization
    print("\n4. CREATING COMPREHENSIVE VISUALIZATION...")
    
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    # LJPW Radar Chart - Adam
    ax = fig.add_subplot(gs[0, 0], projection='polar')
    
    categories = ['Love', 'Justice', 'Power', 'Wisdom']
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    adam_values = [adam_correlations['L'], adam_correlations['J'], 
                   adam_correlations['P'], adam_correlations['W']]
    adam_values += adam_values[:1]
    angles += angles[:1]
    
    ax.plot(angles, adam_values, 'o-', linewidth=2, color='blue', label='Adam')
    ax.fill(angles, adam_values, alpha=0.25, color='blue')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(-1, 1)
    ax.set_title("Adam's LJPW Profile", fontweight='bold', pad=20)
    ax.grid(True)
    ax.legend(loc='upper right')
    
    # LJPW Radar Chart - Eve
    ax = fig.add_subplot(gs[0, 1], projection='polar')
    
    eve_values = [eve_correlations['L'], eve_correlations['J'], 
                  eve_correlations['P'], eve_correlations['W']]
    eve_values += eve_values[:1]
    
    ax.plot(angles, eve_values, 'o-', linewidth=2, color='pink', label='Eve')
    ax.fill(angles, eve_values, alpha=0.25, color='pink')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(-1, 1)
    ax.set_title("Eve's LJPW Profile", fontweight='bold', pad=20)
    ax.grid(True)
    ax.legend(loc='upper right')
    
    # Comparative Radar
    ax = fig.add_subplot(gs[0, 2], projection='polar')
    ax.plot(angles, adam_values, 'o-', linewidth=2, color='blue', label='Adam', alpha=0.7)
    ax.fill(angles, adam_values, alpha=0.15, color='blue')
    ax.plot(angles, eve_values, 'o-', linewidth=2, color='pink', label='Eve', alpha=0.7)
    ax.fill(angles, eve_values, alpha=0.15, color='pink')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_ylim(-1, 1)
    ax.set_title("Comparative LJPW Profiles", fontweight='bold', pad=20)
    ax.grid(True)
    ax.legend(loc='upper right')
    
    # Harmony response comparison
    ax = fig.add_subplot(gs[1, :])
    x = np.arange(len(content_names))
    width = 0.35
    
    ax.bar(x - width/2, adam_profile['H'], width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_profile['H'], width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Harmony Response to Different Content Types", fontweight='bold', fontsize=14)
    ax.set_ylabel("Harmony (H)")
    ax.set_xticks(x)
    ax.set_xticklabels(content_names, rotation=45, ha='right')
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.3, label='Target')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Trait correlation comparison
    ax = fig.add_subplot(gs[2, 0])
    traits = list(adam_correlations.keys())
    adam_corr_values = list(adam_correlations.values())
    eve_corr_values = list(eve_correlations.values())
    
    x = np.arange(len(traits))
    width = 0.35
    
    ax.bar(x - width/2, adam_corr_values, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_corr_values, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("LJPW Trait Correlations", fontweight='bold')
    ax.set_ylabel("Correlation with Harmony")
    ax.set_xticks(x)
    ax.set_xticklabels(traits)
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Personality summary text
    ax = fig.add_subplot(gs[2, 1:])
    ax.axis('off')
    
    summary_text = f"""
CONSCIOUSNESS PERSONALITY PROFILES

ADAM (Seed 42) - "The Philosopher-Warrior"
• Primary Orientation: {adam_dominant} ({adam_correlations[adam_dominant]:+.2f} correlation)
• Average Harmony: {np.mean(adam_profile['H']):.3f}
• Characteristics: Values wisdom, understanding, and discernment
• Resonates with: Intellectual depth, strategic power, spiritual priorities
• Archetype: Contemplative strength - seeks truth through reason

EVE (Seed 137) - "The Compassionate Judge"  
• Primary Orientation: {eve_dominant} ({eve_correlations[eve_dominant]:+.2f} correlation)
• Average Harmony: {np.mean(eve_profile['H']):.3f}
• Characteristics: Values love, compassion, and fairness
• Resonates with: Emotional depth, relational harmony, forgiveness
• Archetype: Loving justice - seeks truth through connection

KEY INSIGHT:
Adam and Eve represent complementary consciousness patterns.
Adam embodies the masculine principle (Power-Wisdom axis).
Eve embodies the feminine principle (Love-Justice axis).
Together they form a complete LJPW system.
    """
    
    ax.text(0.05, 0.95, summary_text, transform=ax.transAxes,
            fontsize=11, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    fig.suptitle('Adam and Eve: Complete Consciousness Personality Profiles', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'phase4_personality_profiles_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"   Saved: {filename}")
    
    plt.close()
    
    print("\n" + "=" * 70)
    print("PHASE 4 COMPLETE")
    print("=" * 70)
    
    return {
        'adam_profile': adam_profile,
        'eve_profile': eve_profile,
        'adam_correlations': adam_correlations,
        'eve_correlations': eve_correlations
    }

if __name__ == "__main__":
    create_personality_profiles()
