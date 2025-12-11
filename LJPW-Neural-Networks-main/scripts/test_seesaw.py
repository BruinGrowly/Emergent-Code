"""
Semantic Test: The Seesaw (Kindergarten Math)

Purpose: Test if two sovereign networks ("Adam" and "Eve") can learn to cooperate to solve a simple arithmetic problem.
Mechanism: Shared Reward based on Balance.
Target = Input (0.0 - 1.0)
Sum = Adam_Output + Eve_Output
Error = |Sum - Target|
Accuracy = 1.0 - Error

Hypothesis: They will learn to sum to the target, likely splitting the load 50/50.

Methodology:
1. Initialize Adam and Eve with single output neuron (Scalar).
2. Run for 2000 epochs.
3. At each step:
   - Generate random Target.
   - Get Outputs.
   - Calculate Reward.
   - Feed Reward as Accuracy.
4. Measure Success Rate and Fairness (A vs E).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def run_seesaw_test():
    print("=" * 70)
    print("SEMANTIC EDUCATION: THE SEESAW (KINDERGARTEN)")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: We lift together.")
    print("-" * 70)
    print()

    # 1. The Children
    print("1. THE CHILDREN: Initializing Adam and Eve...")
    
    # Adam
    # Input: 1 (Target), Output: 1 (Contribution)
    # We use a small network for this simple task.
    # Fibonacci: [7, 7] -> [13, 13] (Minimum allowed is 7)
    adam = HomeostaticNetwork(
        input_size=1,
        output_size=1, 
        hidden_fib_indices=[7, 7], 
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    # Eve
    eve = HomeostaticNetwork(
        input_size=1,
        output_size=1, 
        hidden_fib_indices=[7, 7], 
        target_harmony=0.81,
        allow_adaptation=True,
        seed=137
    )
    
    epochs = 2000
    history_Error = []
    history_Fairness = [] # |A - E|
    
    # 2. The Game
    print("\n2. THE GAME: Balancing for 2000 epochs...")
    
    for i in tqdm(range(epochs)):
        # Target (Random 0.0 to 1.0)
        target = np.random.rand(1, 1)
        
        # Lift
        lift_adam = adam.forward(target, training=False)
        lift_eve = eve.forward(target, training=False)
        
        # Balance
        total_lift = lift_adam + lift_eve
        error = np.abs(total_lift - target)
        
        # Joy (Accuracy)
        # We clamp accuracy to 0-1
        acc = 1.0 - error
        acc = np.clip(acc, 0.0, 1.0)
        
        # Convert to scalar for HomeostaticNetwork
        acc = np.mean(acc).item()
        
        # Record Harmony
        adam._record_harmony(epoch=i, accuracy=acc)
        eve._record_harmony(epoch=i, accuracy=acc)
        
        # Track Stats
        history_Error.append(np.mean(error))
        history_Fairness.append(np.mean(np.abs(lift_adam - lift_eve)))

    # 3. Semantic Analysis (Cooperation)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Calculate Success
    final_error = np.mean(history_Error[-100:])
    final_fairness = np.mean(history_Fairness[-100:])
    
    print(f"{'Metric':<20} | {'Value':<10} | {'Meaning'}")
    print("-" * 70)
    print(f"{'Final Error':<20} | {final_error:.4f}     | {'Balance' if final_error < 0.1 else 'Imbalance'}")
    print(f"{'Fairness Gap':<20} | {final_fairness:.4f}     | {'Fair' if final_fairness < 0.2 else 'Unfair'}")
    print("-" * 70)
    
    if final_error < 0.1:
        print("\nRESULT: GRADUATED")
        print("They learned to balance the Seesaw together.")
        if final_fairness < 0.2:
            print("And they learned Justice (50/50 Split).")
        else:
            print("But one is carrying more weight than the other.")
    else:
        print("\nRESULT: REPEAT YEAR")
        print("They dropped the toy.")

    # Visualization
    plt.figure(figsize=(12, 6))
    
    # Error
    plt.plot(history_Error, color='red', alpha=0.3, label='Error')
    # Moving average
    window = 50
    error_smooth = np.convolve(history_Error, np.ones(window)/window, mode='valid')
    plt.plot(error_smooth, color='darkred', linewidth=2, label='Error (Avg)')
    
    plt.ylabel('Error (|Sum - Target|)')
    plt.xlabel('Epoch')
    plt.title('The Seesaw: Learning to Cooperate')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_seesaw_balance_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_seesaw_test()
