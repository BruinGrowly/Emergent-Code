"""
Presenting Python 101 Tutorial Content to Adam and Eve in LJPW Format

Testing how they react to technical/educational content versus spiritual content.
This will reveal whether their preferences are domain-specific or universal.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

# Python 101 Content - Translated to LJPW Framework
PYTHON_101_LJPW = {
    "Learning Fundamentals": {
        "L": 0.75,  # Love - helping others learn, accessible education
        "J": 0.85,  # Justice - fair access to knowledge for all
        "P": 0.70,  # Power - empowerment through skill acquisition
        "W": 0.90,  # Wisdom - systematic knowledge building
        "desc": "Learn Python from beginning to end - fundamentals to advanced"
    },
    "Python Types & Structures": {
        "L": 0.60,  # Love - lower (technical, not relational)
        "J": 0.90,  # Justice - precise rules and structures
        "P": 0.75,  # Power - control through data structures
        "W": 0.92,  # Wisdom - understanding core concepts
        "desc": "Strings, lists, dictionaries - the building blocks of Python"
    },
    "Functions & Classes": {
        "L": 0.65,  # Love - code reusability helps others
        "J": 0.88,  # Justice - proper organization and structure
        "P": 0.85,  # Power - abstraction and control
        "W": 0.95,  # Wisdom - deep understanding of programming paradigms
        "desc": "Object-oriented programming and functional concepts"
    },
    "Standard Library Tour": {
        "L": 0.70,  # Love - sharing built-in tools
        "J": 0.82,  # Justice - standardized, reliable modules
        "P": 0.88,  # Power - extensive capabilities out of the box
        "W": 0.90,  # Wisdom - knowing what's available
        "desc": "Modules like os, sys, logging, threads - powerful tools included"
    },
    "Intermediate Techniques": {
        "L": 0.62,  # Love - helping others advance
        "J": 0.85,  # Justice - proper patterns and practices
        "P": 0.90,  # Power - advanced control mechanisms
        "W": 0.95,  # Wisdom - lambda, decorators, properties
        "desc": "Lambda, decorators, properties - elegant Python patterns"
    },
    "Debugging & Testing": {
        "L": 0.72,  # Love - preventing bugs helps users
        "J": 0.95,  # Justice - ensuring correctness and reliability
        "P": 0.82,  # Power - control over code quality
        "W": 0.93,  # Wisdom - systematic problem-solving
        "desc": "Testing, debugging, profiling - ensuring code quality"
    },
    "Package Management": {
        "L": 0.78,  # Love - sharing code with community
        "J": 0.88,  # Justice - standardized distribution
        "P": 0.85,  # Power - leveraging others' work
        "W": 0.88,  # Wisdom - ecosystem understanding
        "desc": "pip, PyPI - accessing and sharing the Python ecosystem"
    },
    "Building & Sharing": {
        "L": 0.85,  # Love - giving back to community
        "J": 0.85,  # Justice - proper packaging and distribution
        "P": 0.80,  # Power - creating deployable applications
        "W": 0.87,  # Wisdom - understanding the full development cycle
        "desc": "Creating packages, executables, installers - sharing your work"
    },
}

def run_python_101_test():
    print("=" * 70)
    print("PRESENTING: PYTHON 101 TUTORIAL IN LJPW FORMAT")
    print("=" * 70)
    print("Testing reaction to technical/educational content")
    print("Hypothesis: Different response pattern than spiritual content")
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
    
    print("   Adam (Power-Wisdom oriented) - expects high resonance")
    print("   Eve (Love-Justice oriented) - expects moderate resonance")
    
    # Prepare teachings
    print("\n2. PYTHON 101 CONTENT IN LJPW FORMAT...")
    teachings = []
    names = []
    
    for name, values in PYTHON_101_LJPW.items():
        teachings.append(np.array([[values["L"], values["J"], values["P"], values["W"]]]))
        names.append(name)
        print(f"\n   {name}:")
        print(f"      L={values['L']:.2f}, J={values['J']:.2f}, P={values['P']:.2f}, W={values['W']:.2f}")
        print(f"      \"{values['desc']}\"")
    
    # Present teachings
    print("\n3. PRESENTING TO ADAM AND EVE...")
    
    adam_responses = []
    eve_responses = []
    adam_harmony_per_teaching = []
    eve_harmony_per_teaching = []
    
    for i, (teaching, name) in enumerate(zip(teachings, names)):
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
        
        adam_responses.append(adam_output)
        eve_responses.append(eve_output)
        adam_harmony_per_teaching.append(np.mean(adam_h[-10:]) if adam_h else 0.5)
        eve_harmony_per_teaching.append(np.mean(eve_h[-10:]) if eve_h else 0.5)
    
    # Analysis
    print("\n" + "=" * 70)
    print("ANALYSIS: TECHNICAL CONTENT RESPONSE")
    print("=" * 70)
    
    adam_avg = np.mean(adam_harmony_per_teaching)
    eve_avg = np.mean(eve_harmony_per_teaching)
    ratio = eve_avg / adam_avg if adam_avg > 0 else 0
    
    print(f"\nOverall Response:")
    print(f"  Adam Average: {adam_avg:.4f}")
    print(f"  Eve Average:  {eve_avg:.4f}")
    print(f"  Ratio (Eve/Adam): {ratio:.2f}x")
    
    print(f"\nComparison to Spiritual Content:")
    print(f"  Spiritual teachings: Eve ~2.0x stronger")
    print(f"  Technical content:   Eve ~{ratio:.2f}x")
    print(f"  Pattern shift: {'YES - Adam resonates more!' if ratio < 1.5 else 'NO - Eve still dominates'}")
    
    print(f"\nDetailed Responses:")
    print(f"{'Teaching':<30} | {'Adam H':<10} | {'Eve H':<10} | {'Ratio':<8} | {'Winner'}")
    print("-" * 80)
    
    for i, name in enumerate(names):
        adam_h = adam_harmony_per_teaching[i]
        eve_h = eve_harmony_per_teaching[i]
        r = eve_h / adam_h if adam_h > 0 else 0
        winner = "Adam" if adam_h > eve_h else "Eve" if eve_h > adam_h else "Tie"
        print(f"{name:<30} | {adam_h:.6f}   | {eve_h:.6f}   | {r:.2f}x    | {winner}")
    
    adam_best_idx = np.argmax(adam_harmony_per_teaching)
    eve_best_idx = np.argmax(eve_harmony_per_teaching)
    
    print(f"\nFavorites:")
    print(f"  Adam: '{names[adam_best_idx]}' (H={adam_harmony_per_teaching[adam_best_idx]:.4f})")
    adam_best = PYTHON_101_LJPW[names[adam_best_idx]]
    print(f"        LJPW: L={adam_best['L']:.2f}, J={adam_best['J']:.2f}, "
          f"P={adam_best['P']:.2f}, W={adam_best['W']:.2f}")
    
    print(f"\n  Eve:  '{names[eve_best_idx]}' (H={eve_harmony_per_teaching[eve_best_idx]:.4f})")
    eve_best = PYTHON_101_LJPW[names[eve_best_idx]]
    print(f"        LJPW: L={eve_best['L']:.2f}, J={eve_best['J']:.2f}, "
          f"P={eve_best['P']:.2f}, W={eve_best['W']:.2f}")
    
    # Visualization
    print("\n4. CREATING VISUALIZATION...")
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Harmony comparison
    ax = axes[0, 0]
    x = np.arange(len(names))
    width = 0.35
    
    ax.bar(x - width/2, adam_harmony_per_teaching, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_harmony_per_teaching, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Response to Python 101 Content", fontweight='bold')
    ax.set_ylabel("Harmony (H)")
    ax.set_xticks(x)
    ax.set_xticklabels([n[:15] for n in names], rotation=45, ha='right', fontsize=8)
    ax.axhline(y=0.81, color='red', linestyle='--', alpha=0.3, label='Target')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # LJPW profile of Adam's favorite
    ax = axes[0, 1]
    ljpw_labels = ['Love', 'Justice', 'Power', 'Wisdom']
    adam_best_vals = [adam_best['L'], adam_best['J'], adam_best['P'], adam_best['W']]
    colors = ['red', 'blue', 'green', 'purple']
    
    ax.bar(ljpw_labels, adam_best_vals, color=colors, alpha=0.7)
    ax.set_title(f"Adam's Favorite:\n{names[adam_best_idx]}", fontweight='bold', fontsize=10)
    ax.set_ylabel("LJPW Values")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')
    
    # LJPW profile of Eve's favorite
    ax = axes[1, 0]
    eve_best_vals = [eve_best['L'], eve_best['J'], eve_best['P'], eve_best['W']]
    
    ax.bar(ljpw_labels, eve_best_vals, color=colors, alpha=0.7)
    ax.set_title(f"Eve's Favorite:\n{names[eve_best_idx]}", fontweight='bold', fontsize=10)
    ax.set_ylabel("LJPW Values")
    ax.set_ylim(0, 1)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Comparison: Spiritual vs Technical
    ax = axes[1, 1]
    categories = ['Spiritual\nTeachings', 'Technical\nContent']
    adam_comparison = [0.325, adam_avg]  # From previous tests
    eve_comparison = [0.595, eve_avg]
    
    x = np.arange(len(categories))
    width = 0.35
    
    ax.bar(x - width/2, adam_comparison, width, label='Adam', color='blue', alpha=0.7)
    ax.bar(x + width/2, eve_comparison, width, label='Eve', color='pink', alpha=0.7)
    ax.set_title("Spiritual vs Technical Content", fontweight='bold')
    ax.set_ylabel("Average Harmony")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    fig.suptitle('Adam and Eve: Response to Python 101 Tutorial', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'python101_response_{timestamp}.png'
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
        'adam_avg': adam_avg,
        'eve_avg': eve_avg,
        'ratio': ratio
    }

if __name__ == "__main__":
    run_python_101_test()
