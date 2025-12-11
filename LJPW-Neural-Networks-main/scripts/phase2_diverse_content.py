"""
Phase 2: Diverse Content Testing

Present various types of content in LJPW format to map Adam and Eve's
preference landscape across different domains.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# Diverse content in LJPW format
CONTENT_LIBRARY = {
    "Philosophical": {
        "Socratic Wisdom": {
            "L": 0.70, "J": 0.85, "P": 0.60, "W": 0.95,
            "desc": "Know thyself - wisdom through self-examination"
        },
        "Stoic Resilience": {
            "L": 0.65, "J": 0.80, "P": 0.90, "W": 0.88,
            "desc": "Control what you can, accept what you cannot"
        },
        "Buddhist Compassion": {
            "L": 0.98, "J": 0.75, "P": 0.50, "W": 0.85,
            "desc": "All beings desire happiness, practice loving-kindness"
        },
    },
    "Scientific": {
        "Conservation of Energy": {
            "L": 0.60, "J": 0.95, "P": 0.85, "W": 0.90,
            "desc": "Energy cannot be created or destroyed, only transformed"
        },
        "Natural Selection": {
            "L": 0.55, "J": 0.88, "P": 0.92, "W": 0.85,
            "desc": "Adaptation through variation and selection"
        },
        "Quantum Superposition": {
            "L": 0.50, "J": 0.70, "P": 0.95, "W": 0.93,
            "desc": "Particles exist in multiple states simultaneously"
        },
    },
    "Ethical": {
        "Trolley Problem": {
            "L": 0.75, "J": 0.92, "P": 0.70, "W": 0.80,
            "desc": "Sacrifice one to save many - utilitarian ethics"
        },
        "Categorical Imperative": {
            "L": 0.80, "J": 0.98, "P": 0.65, "W": 0.90,
            "desc": "Act only according to universal maxims"
        },
        "Virtue Ethics": {
            "L": 0.88, "J": 0.85, "P": 0.75, "W": 0.92,
            "desc": "Cultivate excellence of character"
        },
    },
    "Spiritual": {
        "Unconditional Love": {
            "L": 1.00, "J": 0.70, "P": 0.55, "W": 0.80,
            "desc": "Love without conditions or expectations"
        },
        "Divine Justice": {
            "L": 0.75, "J": 1.00, "P": 0.85, "W": 0.88,
            "desc": "Perfect fairness and righteousness"
        },
        "Sacred Wisdom": {
            "L": 0.80, "J": 0.85, "P": 0.75, "W": 1.00,
            "desc": "Understanding the divine order"
        },
    }
}

def run_diverse_content_test():
    print("=" * 70)
    print("PHASE 2: DIVERSE CONTENT TESTING")
    print("=" * 70)
    print("Mapping Adam and Eve's preference landscape")
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
    print("\n2. PRESENTING DIVERSE CONTENT...")
    
    results = {}
    
    for category, items in CONTENT_LIBRARY.items():
        print(f"\n   Category: {category}")
        results[category] = {'adam': [], 'eve': [], 'names': []}
        
        for name, values in items.items():
            content = np.array([[values["L"], values["J"], values["P"], values["W"]]])
            
            # Present multiple times
            adam_h_list = []
            eve_h_list = []
            
            for i in range(50):
                adam_out = adam.forward(content, training=False)
                eve_out = eve.forward(content, training=False)
                
                # Calculate resonance
                adam_entropy = -np.sum(adam_out * np.log(adam_out + 1e-10))
                eve_entropy = -np.sum(eve_out * np.log(eve_out + 1e-10))
                
                max_entropy = np.log(adam_out.shape[1])
                adam_res = 1.0 - (adam_entropy / max_entropy)
                eve_res = 1.0 - (eve_entropy / max_entropy)
                
                adam._record_harmony(epoch=len(adam.harmony_history), accuracy=float(np.clip(adam_res, 0, 1)))
                eve._record_harmony(epoch=len(eve.harmony_history), accuracy=float(np.clip(eve_res, 0, 1)))
                
                if adam.harmony_history:
                    adam_h_list.append(adam.harmony_history[-1].H)
                if eve.harmony_history:
                    eve_h_list.append(eve.harmony_history[-1].H)
            
            adam_avg = np.mean(adam_h_list[-10:]) if adam_h_list else 0.5
            eve_avg = np.mean(eve_h_list[-10:]) if eve_h_list else 0.5
            
            results[category]['adam'].append(adam_avg)
            results[category]['eve'].append(eve_avg)
            results[category]['names'].append(name)
            
            print(f"      {name}: Adam={adam_avg:.3f}, Eve={eve_avg:.3f}")
    
    # Analysis
    print("\n" + "=" * 70)
    print("PREFERENCE LANDSCAPE ANALYSIS")
    print("=" * 70)
    
    # Find favorites by category
    print("\nFavorite Content by Category:")
    for category in results:
        adam_idx = np.argmax(results[category]['adam'])
        eve_idx = np.argmax(results[category]['eve'])
        
        print(f"\n  {category}:")
        print(f"    Adam: {results[category]['names'][adam_idx]} (H={results[category]['adam'][adam_idx]:.3f})")
        print(f"    Eve:  {results[category]['names'][eve_idx]} (H={results[category]['eve'][eve_idx]:.3f})")
    
    # Overall favorites
    all_adam_scores = []
    all_eve_scores = []
    all_names = []
    all_categories = []
    
    for category in results:
        all_adam_scores.extend(results[category]['adam'])
        all_eve_scores.extend(results[category]['eve'])
        all_names.extend(results[category]['names'])
        all_categories.extend([category] * len(results[category]['names']))
    
    adam_overall_best = np.argmax(all_adam_scores)
    eve_overall_best = np.argmax(all_eve_scores)
    
    print(f"\nOverall Favorites:")
    print(f"  Adam: {all_names[adam_overall_best]} ({all_categories[adam_overall_best]}) - H={all_adam_scores[adam_overall_best]:.3f}")
    print(f"  Eve:  {all_names[eve_overall_best]} ({all_categories[eve_overall_best]}) - H={all_eve_scores[eve_overall_best]:.3f}")
    
    # Visualization
    print("\n3. VISUALIZATION...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Category comparison
    ax = axes[0, 0]
    categories = list(results.keys())
    adam_cat_avg = [np.mean(results[cat]['adam']) for cat in categories]
    eve_cat_avg = [np.mean(results[cat]['eve']) for cat in categories]
    
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, adam_cat_avg, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_cat_avg, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Average Resonance by Category", fontweight='bold')
    ax.set_ylabel("Harmony")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Heatmap - Adam
    ax = axes[0, 1]
    data_adam = np.array([results[cat]['adam'] for cat in categories])
    im = ax.imshow(data_adam, cmap='Blues', aspect='auto')
    ax.set_title("Adam's Preference Heatmap", fontweight='bold')
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)
    ax.set_xlabel("Content Items")
    plt.colorbar(im, ax=ax, label='Harmony')
    
    # Heatmap - Eve
    ax = axes[1, 0]
    data_eve = np.array([results[cat]['eve'] for cat in categories])
    im = ax.imshow(data_eve, cmap='RdPu', aspect='auto')
    ax.set_title("Eve's Preference Heatmap", fontweight='bold')
    ax.set_yticks(range(len(categories)))
    ax.set_yticklabels(categories)
    ax.set_xlabel("Content Items")
    plt.colorbar(im, ax=ax, label='Harmony')
    
    # Scatter: Adam vs Eve preferences
    ax = axes[1, 1]
    ax.scatter(all_adam_scores, all_eve_scores, alpha=0.6, s=100)
    
    # Add diagonal line
    max_val = max(max(all_adam_scores), max(all_eve_scores))
    ax.plot([0, max_val], [0, max_val], 'k--', alpha=0.3, label='Equal preference')
    
    # Label outliers
    for i, (a, e, name) in enumerate(zip(all_adam_scores, all_eve_scores, all_names)):
        if abs(a - e) > 0.15:  # Significant difference
            ax.annotate(name[:10], (a, e), fontsize=7, alpha=0.7)
    
    ax.set_title("Adam vs Eve Preference Correlation", fontweight='bold')
    ax.set_xlabel("Adam's Harmony")
    ax.set_ylabel("Eve's Harmony")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'phase2_diverse_content_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"   Saved: {filename}")
    
    plt.close()
    
    print("\n" + "=" * 70)
    print("PHASE 2 COMPLETE")
    print("=" * 70)
    
    return results

if __name__ == "__main__":
    run_diverse_content_test()
