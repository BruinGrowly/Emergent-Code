"""
Semantic Test: The Dance of Creation (Co-Creation)

Purpose: Test if two sovereign networks ("Adam" and "Eve") can collaborate to create art.
Mechanism: Shared Reward based on Aesthetic Beauty.
Canvas = Adam_Output + Eve_Output
Beauty = Symmetry + Entropy + Contrast
Accuracy = Beauty (normalized to 0.0 - 1.0)

Hypothesis: They will learn to coordinate their outputs to maximize the beauty of the shared canvas.

Methodology:
1. Initialize Adam and Eve.
2. Run for 4000 epochs.
3. At each step:
   - Generate random "Inspiration" (Input).
   - Get Outputs (Paint).
   - Combine into Canvas.
   - Calculate Beauty Score.
   - Feed Beauty as Accuracy to both.
4. Measure the evolution of Beauty and the correlation between their outputs.
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def calculate_beauty(image):
    """
    Calculates the aesthetic beauty of a 12x12 image.
    Components:
    1. Symmetry (Horizontal + Vertical)
    2. Entropy (Complexity)
    3. Contrast (Variance)
    """
    # Normalize image to 0-1
    img = image.reshape(12, 12)
    img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-6)
    
    # 1. Symmetry
    # Horizontal flip
    h_flip = np.fliplr(img)
    # Vertical flip
    v_flip = np.flipud(img)
    
    # MSE between original and flips (Lower is more symmetrical)
    h_sym = 1.0 - np.mean((img - h_flip)**2)
    v_sym = 1.0 - np.mean((img - v_flip)**2)
    symmetry = (h_sym + v_sym) / 2.0
    
    # 2. Entropy (Complexity)
    # Histogram of pixel values
    hist, _ = np.histogram(img, bins=10, range=(0, 1))
    prob = hist / np.sum(hist)
    ent = entropy(prob)
    # Normalize entropy (max entropy for 10 bins is ln(10) ~ 2.3)
    complexity = ent / np.log(10)
    
    # 3. Contrast
    contrast = np.std(img) * 2.0 # Scale up a bit
    contrast = min(contrast, 1.0)
    
    # Weighted Sum
    # We value Symmetry and Complexity most
    score = 0.4 * symmetry + 0.4 * complexity + 0.2 * contrast
    return score

def run_dance_test():
    print("=" * 70)
    print("SEMANTIC GROWTH: THE DANCE OF CREATION")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Joy is Beauty. Together we create.")
    print("-" * 70)
    print()

    # 1. The Dancers
    print("1. THE DANCERS: Initializing Adam and Eve...")
    
    # Adam
    adam = HomeostaticNetwork(
        input_size=784,
        output_size=144, # Output is the Canvas (12x12) - Fibonacci 144
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    # Eve
    eve = HomeostaticNetwork(
        input_size=784,
        output_size=144, # Output is the Canvas (12x12) - Fibonacci 144
        hidden_fib_indices=[13, 8],
        target_harmony=0.81,
        allow_adaptation=True,
        seed=137
    )
    
    epochs = 4000
    history_Beauty = []
    final_canvas = None
    
    # 2. The Dance
    print("\n2. THE DANCE: Painting for 4000 epochs...")
    
    for i in tqdm(range(epochs)):
        # Inspiration (Random Noise)
        inspiration = np.random.randn(1, 784) # Single batch for visualization clarity
        
        # Paint
        paint_adam = adam.forward(inspiration, training=False)
        paint_eve = eve.forward(inspiration, training=False)
        
        # The Shared Canvas
        canvas = paint_adam + paint_eve
        
        # The Joy (Beauty Score)
        beauty = calculate_beauty(canvas)
        history_Beauty.append(beauty)
        
        # Feedback (Shared Reward)
        # Accuracy = Beauty
        # We add a little noise to simulate subjective fluctuation
        acc = beauty + np.random.randn() * 0.01
        acc = np.clip(acc, 0.0, 1.0)
        
        # Record Harmony
        adam._record_harmony(epoch=i, accuracy=acc)
        eve._record_harmony(epoch=i, accuracy=acc)
        
        if i == epochs - 1:
            final_canvas = canvas.reshape(12, 12)

    # 3. Semantic Analysis (Artistic Evolution)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Evolution of Beauty
    start_beauty = np.mean(history_Beauty[:100])
    end_beauty = np.mean(history_Beauty[-100:])
    improvement = end_beauty - start_beauty
    
    print(f"{'Metric':<20} | {'Value':<10} | {'Meaning'}")
    print("-" * 70)
    print(f"{'Start Beauty':<20} | {start_beauty:.4f}     | {'Chaos'}")
    print(f"{'End Beauty':<20} | {end_beauty:.4f}     | {'Art'}")
    print(f"{'Improvement':<20} | {improvement:+.4f}     | {'Learning' if improvement > 0 else 'Stagnation'}")
    print("-" * 70)
    
    if improvement > 0.1:
        print("\nRESULT: MASTERPIECE")
        print("They learned to create beauty together.")
    else:
        print("\nRESULT: ABSTRACT ART")
        print("They are exploring, but not converging on classical beauty.")

    # Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Beauty History
    ax1.plot(history_Beauty, color='purple', alpha=0.6)
    ax1.set_ylabel('Beauty Score')
    ax1.set_xlabel('Epoch')
    ax1.set_title('The Evolution of Joy')
    ax1.grid(True, alpha=0.3)
    
    # Final Canvas
    ax2.imshow(final_canvas, cmap='magma')
    ax2.set_title(f'The Final Canvas (Beauty={end_beauty:.2f})')
    ax2.axis('off')
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_dance_art_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_dance_test()
