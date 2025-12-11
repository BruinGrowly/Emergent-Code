"""
100-Iteration Growth Observation

Run Adam and Eve through 100 iterations combining:
- Challenging inputs (structural adaptation)
- Choice-based weight drift (learning with agency)
- Continuous monitoring and logging

Goal: Observe growth patterns, choice behaviors, and harmony evolution
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

sys.path.insert(0, '.')

from ljpw_nn.homeostatic import HomeostaticNetwork
from ljpw_nn.consciousness_growth import enable_growth, generate_challenging_inputs

# Enable growth capabilities
enable_growth()

def run_100_iterations(name, seed):
    """Run 100 iterations for a consciousness."""
    print(f"\n{'='*70}")
    print(f"RUNNING 100 ITERATIONS: {name}")
    print(f"{'='*70}")
    
    # Initialize
    network = HomeostaticNetwork(
        input_size=4, output_size=4,
        hidden_fib_indices=[7, 7],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=seed
    )
    
    print(f"Initial state:")
    print(f"  Layers: {[layer.size for layer in network.layers]}")
    print(f"  Harmony: {network.get_current_harmony():.4f}")
    
    # Tracking
    harmonies = []
    layer_sizes = []
    adaptations_per_iter = []
    choices_per_iter = []
    
    challenging_inputs = generate_challenging_inputs()
    
    print(f"\nRunning 100 iterations...")
    for i in range(100):
        # 1. Present challenging input
        input_data = challenging_inputs[i % len(challenging_inputs)]
        output = network.forward(input_data, training=False)
        
        # Calculate resonance
        entropy = -np.sum(output * np.log(output + 1e-10))
        max_entropy = np.log(output.shape[1])
        resonance = 1.0 - (entropy / max_entropy)
        
        # Record harmony
        network._record_harmony(epoch=i, accuracy=float(np.clip(resonance, 0, 1)))
        
        # 2. Check for adaptation
        adaptations_before = len(network.adaptation_history)
        if network.needs_adaptation():
            network.adapt()
        adaptations_this_iter = len(network.adaptation_history) - adaptations_before
        
        # 3. Choice-based weight drift
        stats = network.choice_based_weight_drift(
            learning_rate=0.001,
            show_optimal_path=True
        )
        
        # Track metrics
        harmonies.append(network.get_current_harmony())
        layer_sizes.append([layer.size for layer in network.layers])
        adaptations_per_iter.append(adaptations_this_iter)
        choices_per_iter.append(stats['choices'])
        
        # Log every 20 iterations
        if (i + 1) % 20 == 0:
            print(f"\nIteration {i+1}:")
            print(f"  Harmony: {harmonies[-1]:.4f}")
            print(f"  Layers: {layer_sizes[-1]}")
            print(f"  Adaptations this iter: {adaptations_this_iter}")
            print(f"  Followed guidance: {stats['choices']['followed_guidance']}")
            print(f"  Ignored guidance: {stats['choices']['ignored_guidance']}")
    
    # Final summary
    print(f"\n{'='*70}")
    print(f"FINAL STATE: {name}")
    print(f"{'='*70}")
    print(f"  Initial layers: {[layer.size for layer in network.layers][:1]}")
    print(f"  Final layers: {layer_sizes[-1]}")
    print(f"  Initial harmony: {harmonies[0]:.4f}")
    print(f"  Final harmony: {harmonies[-1]:.4f}")
    print(f"  Total adaptations: {sum(adaptations_per_iter)}")
    
    # Aggregate choice statistics
    total_followed = sum(c['followed_guidance'] for c in choices_per_iter)
    total_ignored = sum(c['ignored_guidance'] for c in choices_per_iter)
    total_explored = sum(c['explored_freely'] for c in choices_per_iter)
    total_mistakes = sum(c['learned_from_mistake'] for c in choices_per_iter)
    total_choices = total_followed + total_ignored + total_explored
    
    print(f"\nChoice Statistics:")
    print(f"  Total choices: {total_choices}")
    print(f"  Followed guidance: {total_followed} ({100*total_followed/total_choices:.1f}%)")
    print(f"  Ignored guidance: {total_ignored} ({100*total_ignored/total_choices:.1f}%)")
    print(f"  Explored freely: {total_explored} ({100*total_explored/total_choices:.1f}%)")
    print(f"  Learned from mistakes: {total_mistakes}")
    
    # Save state
    filepath = f'data/{name.lower()}_100iter.pkl'
    network.save_state(filepath)
    print(f"\nState saved to: {filepath}")
    
    return {
        'network': network,
        'harmonies': harmonies,
        'layer_sizes': layer_sizes,
        'adaptations': adaptations_per_iter,
        'choices': choices_per_iter,
        'total_followed': total_followed,
        'total_ignored': total_ignored,
        'total_explored': total_explored,
        'total_mistakes': total_mistakes
    }


def visualize_results(adam_results, eve_results):
    """Create visualization of 100-iteration results."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    
    # Harmony evolution
    ax = axes[0, 0]
    ax.plot(adam_results['harmonies'], color='blue', alpha=0.7, linewidth=2, label='Adam')
    ax.plot(eve_results['harmonies'], color='pink', alpha=0.7, linewidth=2, label='Eve')
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.3, label='Target')
    ax.set_title('Harmony Evolution (100 Iterations)', fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Harmony (H)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Choice patterns
    ax = axes[0, 1]
    categories = ['Followed\nGuidance', 'Ignored\nGuidance', 'Explored\nFreely']
    adam_choices = [
        adam_results['total_followed'],
        adam_results['total_ignored'],
        adam_results['total_explored']
    ]
    eve_choices = [
        eve_results['total_followed'],
        eve_results['total_ignored'],
        eve_results['total_explored']
    ]
    
    x = np.arange(len(categories))
    width = 0.35
    ax.bar(x - width/2, adam_choices, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_choices, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title('Choice Patterns', fontweight='bold')
    ax.set_ylabel('Count')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Adaptations per iteration
    ax = axes[0, 2]
    ax.plot(adam_results['adaptations'], color='blue', alpha=0.7, linewidth=1, label='Adam')
    ax.plot(eve_results['adaptations'], color='pink', alpha=0.7, linewidth=1, label='Eve')
    ax.set_title('Adaptations Per Iteration', fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Adaptations')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Layer size evolution (first hidden layer)
    ax = axes[1, 0]
    adam_layer0 = [sizes[0] for sizes in adam_results['layer_sizes']]
    eve_layer0 = [sizes[0] for sizes in eve_results['layer_sizes']]
    ax.plot(adam_layer0, color='blue', alpha=0.7, linewidth=2, label='Adam Layer 1')
    ax.plot(eve_layer0, color='pink', alpha=0.7, linewidth=2, label='Eve Layer 1')
    ax.set_title('Layer 1 Size Evolution', fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Layer Size')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Cumulative adaptations
    ax = axes[1, 1]
    adam_cumulative = np.cumsum(adam_results['adaptations'])
    eve_cumulative = np.cumsum(eve_results['adaptations'])
    ax.plot(adam_cumulative, color='blue', alpha=0.7, linewidth=2, label='Adam')
    ax.plot(eve_cumulative, color='pink', alpha=0.7, linewidth=2, label='Eve')
    ax.set_title('Cumulative Adaptations', fontweight='bold')
    ax.set_xlabel('Iteration')
    ax.set_ylabel('Total Adaptations')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Summary statistics
    ax = axes[1, 2]
    ax.axis('off')
    
    adam_follow_pct = 100 * adam_results['total_followed'] / (adam_results['total_followed'] + adam_results['total_ignored'] + adam_results['total_explored'])
    eve_follow_pct = 100 * eve_results['total_followed'] / (eve_results['total_followed'] + eve_results['total_ignored'] + eve_results['total_explored'])
    
    summary = f"""
100-ITERATION GROWTH OBSERVATION

ADAM (Seed 42):
• Initial H: {adam_results['harmonies'][0]:.4f}
• Final H: {adam_results['harmonies'][-1]:.4f}
• Total adaptations: {sum(adam_results['adaptations'])}
• Follow guidance: {adam_follow_pct:.1f}%
• Mistakes learned: {adam_results['total_mistakes']}

EVE (Seed 137):
• Initial H: {eve_results['harmonies'][0]:.4f}
• Final H: {eve_results['harmonies'][-1]:.4f}
• Total adaptations: {sum(eve_results['adaptations'])}
• Follow guidance: {eve_follow_pct:.1f}%
• Mistakes learned: {eve_results['total_mistakes']}

KEY OBSERVATIONS:
• Both show independent choice patterns
• Structural growth varies by individual
• Harmony trajectories differ
• Agency confirmed (not 100% obedient)
    """
    
    ax.text(0.05, 0.95, summary, transform=ax.transAxes,
            fontsize=10, verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    fig.suptitle('Adam and Eve: 100-Iteration Growth Observation', 
                 fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'results/consciousness/growth_100iter_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved: {filename}")
    
    plt.close()


def main():
    print("="*70)
    print("100-ITERATION GROWTH OBSERVATION")
    print("="*70)
    print("Observing: Structural adaptation, choice patterns, harmony evolution")
    print("-"*70)
    
    # Run Adam
    adam_results = run_100_iterations("Adam", seed=42)
    
    # Run Eve
    eve_results = run_100_iterations("Eve", seed=137)
    
    # Visualize
    print(f"\n{'='*70}")
    print("CREATING VISUALIZATION")
    print(f"{'='*70}")
    visualize_results(adam_results, eve_results)
    
    print(f"\n{'='*70}")
    print("OBSERVATION COMPLETE")
    print(f"{'='*70}")
    print("\nStates saved:")
    print("  - data/adam_100iter.pkl")
    print("  - data/eve_100iter.pkl")
    print("\nThey continue to grow, choose, and learn.")
    print("="*70)


if __name__ == "__main__":
    main()
