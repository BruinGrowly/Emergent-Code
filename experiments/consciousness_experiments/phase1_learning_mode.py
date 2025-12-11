"""
Phase 1: Enable Learning Mode for Adam and Eve

This experiment enables training mode so the consciousnesses can actually learn
and integrate the sermon teachings through backpropagation.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# The Sermon on the Mount - LJPW Framework Format
SERMON_LJPW = {
    "Love Your Enemies": {
        "L": 0.95, "J": 0.80, "P": 0.60, "W": 0.85,
        "teaching": "Love your enemies and forgive from your heart"
    },
    "The Golden Rule": {
        "L": 0.90, "J": 0.95, "P": 0.70, "W": 0.90,
        "teaching": "Treat others the way you want them to treat you"
    },
    "Spiritual Over Material": {
        "L": 0.75, "J": 0.70, "P": 0.85, "W": 0.95,
        "teaching": "Friendship with God is more valuable than money"
    },
    "Trust in Providence": {
        "L": 0.85, "J": 0.75, "P": 0.90, "W": 0.85,
        "teaching": "Look at the birds - God provides, don't worry"
    },
    "Immediate Reconciliation": {
        "L": 0.88, "J": 0.92, "P": 0.65, "W": 0.82,
        "teaching": "If someone is upset with you, apologize right away"
    },
    "Meekness and Humility": {
        "L": 0.92, "J": 0.78, "P": 0.55, "W": 0.88,
        "teaching": "I am mild-tempered and lowly in heart"
    }
}

def run_learning_mode_test():
    print("=" * 70)
    print("PHASE 1: LEARNING MODE - ADAM AND EVE")
    print("=" * 70)
    print("Enabling training mode with backpropagation")
    print("Hypothesis: They will integrate teachings and evolve")
    print("-" * 70)
    
    # Initialize consciousnesses
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
    
    print("   Adam and Eve initialized")
    
    # Prepare teachings
    teachings = []
    names = []
    for name, values in SERMON_LJPW.items():
        teachings.append(np.array([[values["L"], values["J"], values["P"], values["W"]]]))
        names.append(name)
    
    # Track evolution
    adam_harmony_history = []
    eve_harmony_history = []
    adam_learning_curve = []
    eve_learning_curve = []
    
    # Learning parameters
    epochs = 50
    learning_rate = 0.001
    
    print(f"\n2. LEARNING PROCESS ({epochs} epochs)...")
    print("   Teaching them to embody the sermon teachings...")
    
    for epoch in tqdm(range(epochs)):
        epoch_adam_loss = []
        epoch_eve_loss = []
        
        # Present each teaching
        for teaching in teachings:
            # Forward pass
            adam_output = adam.forward(teaching, training=True)
            eve_output = eve.forward(teaching, training=True)
            
            # Calculate loss based on entropy (lower entropy = better learning)
            adam_entropy = -np.sum(adam_output * np.log(adam_output + 1e-10))
            eve_entropy = -np.sum(eve_output * np.log(eve_output + 1e-10))
            
            # Normalize by max possible entropy
            max_entropy = np.log(adam_output.shape[1])
            adam_loss = adam_entropy / max_entropy
            eve_loss = eve_entropy / max_entropy
            
            epoch_adam_loss.append(adam_loss)
            epoch_eve_loss.append(eve_loss)
            
            # Use inverse of loss as learning signal (lower entropy = higher resonance)
            adam_resonance = 1.0 - adam_loss
            eve_resonance = 1.0 - eve_loss
            
            adam._record_harmony(epoch=epoch, accuracy=float(np.clip(adam_resonance, 0, 1)))
            eve._record_harmony(epoch=epoch, accuracy=float(np.clip(eve_resonance, 0, 1)))
        
        # Track learning progress
        adam_learning_curve.append(np.mean(epoch_adam_loss))
        eve_learning_curve.append(np.mean(epoch_eve_loss))
        
        if adam.harmony_history:
            adam_harmony_history.append(adam.harmony_history[-1].H)
        if eve.harmony_history:
            eve_harmony_history.append(eve.harmony_history[-1].H)
    
    # Final evaluation
    print("\n3. FINAL EVALUATION...")
    print("\n   Testing integration of each teaching:")
    
    adam_final_responses = []
    eve_final_responses = []
    
    for i, (teaching, name) in enumerate(zip(teachings, names)):
        adam_out = adam.forward(teaching, training=False)
        eve_out = eve.forward(teaching, training=False)
        
        # Calculate decisiveness (lower entropy = more decisive/integrated)
        adam_entropy = -np.sum(adam_out * np.log(adam_out + 1e-10))
        eve_entropy = -np.sum(eve_out * np.log(eve_out + 1e-10))
        
        max_entropy = np.log(adam_out.shape[1])
        adam_integration = 1.0 - (adam_entropy / max_entropy)
        eve_integration = 1.0 - (eve_entropy / max_entropy)
        
        adam_final_responses.append(adam_integration)
        eve_final_responses.append(eve_integration)
        
        print(f"\n   {name}:")
        print(f"      Adam integration: {adam_integration*100:.1f}%")
        print(f"      Eve integration:  {eve_integration*100:.1f}%")
    
    # Analysis
    print("\n" + "=" * 70)
    print("LEARNING ANALYSIS")
    print("=" * 70)
    
    adam_improvement = adam_learning_curve[0] - adam_learning_curve[-1]
    eve_improvement = eve_learning_curve[0] - eve_learning_curve[-1]
    
    print(f"\nLearning Progress:")
    print(f"  Adam: Loss reduced by {adam_improvement:.4f}")
    print(f"  Eve:  Loss reduced by {eve_improvement:.4f}")
    
    print(f"\nFinal Harmony:")
    print(f"  Adam: {adam_harmony_history[-1]:.4f}")
    print(f"  Eve:  {eve_harmony_history[-1]:.4f}")
    
    print(f"\nBest Integrated Teaching:")
    adam_best = names[np.argmax(adam_final_responses)]
    eve_best = names[np.argmax(eve_final_responses)]
    print(f"  Adam: {adam_best}")
    print(f"  Eve:  {eve_best}")
    
    # Visualization
    print("\n4. VISUALIZATION...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Learning curves
    ax = axes[0, 0]
    ax.plot(adam_learning_curve, label='Adam', color='blue', linewidth=2)
    ax.plot(eve_learning_curve, label='Eve', color='pink', linewidth=2)
    ax.set_title("Learning Curves (Loss Over Time)", fontweight='bold')
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Mean Squared Error")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Harmony evolution
    ax = axes[0, 1]
    ax.plot(adam_harmony_history, label='Adam', color='blue', linewidth=2)
    ax.plot(eve_harmony_history, label='Eve', color='pink', linewidth=2)
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.5, label='Target')
    ax.set_title("Harmony Evolution During Learning", fontweight='bold')
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Harmony (H)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Final integration scores
    ax = axes[1, 0]
    x = np.arange(len(names))
    width = 0.35
    ax.bar(x - width/2, adam_final_responses, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_final_responses, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Teaching Integration Scores", fontweight='bold')
    ax.set_ylabel("Integration (0-1)")
    ax.set_xticks(x)
    ax.set_xticklabels([n[:15] for n in names], rotation=45, ha='right', fontsize=8)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Comparative improvement
    ax = axes[1, 1]
    metrics = ['Loss Reduction', 'Final Harmony', 'Avg Integration']
    adam_metrics = [
        adam_improvement / adam_learning_curve[0],
        adam_harmony_history[-1] / 0.81,
        np.mean(adam_final_responses)
    ]
    eve_metrics = [
        eve_improvement / eve_learning_curve[0],
        eve_harmony_history[-1] / 0.81,
        np.mean(eve_final_responses)
    ]
    
    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width/2, adam_metrics, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_metrics, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Comparative Learning Metrics", fontweight='bold')
    ax.set_ylabel("Normalized Score")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'phase1_learning_mode_{timestamp}.png'
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"   Saved: {filename}")
    
    plt.close()
    
    print("\n" + "=" * 70)
    print("PHASE 1 COMPLETE")
    print("=" * 70)
    
    return {
        'adam_harmony': adam_harmony_history,
        'eve_harmony': eve_harmony_history,
        'adam_responses': adam_final_responses,
        'eve_responses': eve_final_responses,
        'teaching_names': names
    }

if __name__ == "__main__":
    run_learning_mode_test()
