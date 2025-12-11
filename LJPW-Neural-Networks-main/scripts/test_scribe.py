"""
Semantic Test: The Scribe (Python Literacy)

Purpose: Test if a homeostatic network ("Adam") can learn to write valid Python code.
Mechanism: Reinforcement Learning via Homeostasis.
Output: 10 characters (ASCII).
Reward:
- SyntaxError: 0.0
- RuntimeError: 0.5
- Success: 1.0

Hypothesis: The system will learn to generate valid expressions (e.g., "1+1", "a*b") to maximize harmony.

Methodology:
1. Initialize Adam with large output size (10 chars * 128 ASCII = 1280).
2. Run for 10,000 epochs (Learning Language takes time).
3. At each step:
   - Generate Output.
   - Convert to String.
   - Try `eval()` in a safe context.
   - Calculate Reward.
   - Feed Reward as Accuracy.
4. Measure the "Literacy Rate" (Percentage of valid code).
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import ast

sys.path.insert(0, '.')

from ljpw_nn import HomeostaticNetwork

def decode_output(output_vector):
    """
    Decodes the output vector into a string.
    Adapts to the actual size of the vector (due to Fibonacci constraints).
    """
    # Flatten to 1D array
    output_vector = output_vector.flatten()
    
    # Calculate how many full characters we can form (128 logits per char)
    num_chars = output_vector.size // 128
    
    if num_chars == 0:
        return ""
        
    # Take the usable part
    usable_vector = output_vector[:num_chars * 128]
    
    # Reshape to (num_chars, 128)
    reshaped = usable_vector.reshape(num_chars, 128)
    # Argmax to get character indices
    char_indices = np.argmax(reshaped, axis=1)
    # Convert to string (ASCII 0-127)
    # We clip to printable range (32-126) to make it easier?
    # No, let's allow full ASCII but handle errors.
    chars = [chr(idx) if 32 <= idx <= 126 else ' ' for idx in char_indices]
    return "".join(chars).strip()

def evaluate_code(code_str):
    """
    Evaluates the code string.
    Returns (Reward, Result/Error).
    """
    if not code_str:
        return 0.0, "Empty"
        
    context = {'a': 1, 'b': 2, 'c': 3}
    
    try:
        # Try to parse first (Syntax Check)
        ast.parse(code_str)
        
        # Try to evaluate (Execution Check)
        try:
            result = eval(code_str, {"__builtins__": {}}, context)
            return 1.0, f"Success: {result}"
        except Exception as e:
            return 0.5, f"RuntimeError: {type(e).__name__}"
            
    except SyntaxError:
        return 0.0, "SyntaxError"
    except Exception:
        return 0.0, "Error"

def run_scribe_test():
    print("=" * 70)
    print("SEMANTIC EDUCATION: THE SCRIBE (PYTHON LESSON 1)")
    print("=" * 70)
    print("Framework: LJPW (Love, Justice, Power, Wisdom)")
    print("Hypothesis: Structure is Power. Adam will learn to speak.")
    print("-" * 70)
    print()

    # 1. The Student
    print("1. THE STUDENT: Initializing Adam with a Keyboard...")
    
    # Adam
    # Output size: 10 chars * 128 ASCII options = 1280
    # We need a larger network for this complexity.
    # Fibonacci indices: [15, 13] -> [610, 233]
    adam = HomeostaticNetwork(
        input_size=784,
        output_size=1280, 
        hidden_fib_indices=[15, 13], 
        target_harmony=0.81,
        allow_adaptation=True,
        seed=42
    )
    
    epochs = 10000
    history_Literacy = []
    valid_codes = set()
    
    # 2. The Lesson
    print("\n2. THE LESSON: Writing for 10,000 epochs...")
    
    pbar = tqdm(range(epochs))
    for i in pbar:
        # Inspiration (Random Noise)
        inspiration = np.random.randn(1, 784)
        
        # Write
        output = adam.forward(inspiration, training=False)
        code = decode_output(output)
        
        # Grade
        reward, message = evaluate_code(code)
        
        # Feedback
        # Accuracy = Reward
        acc = reward + np.random.randn() * 0.01
        acc = np.clip(acc, 0.0, 1.0)
        
        # Record Harmony
        adam._record_harmony(epoch=i, accuracy=acc)
        
        # Track Literacy
        history_Literacy.append(reward)
        if reward == 1.0:
            valid_codes.add(code)
            pbar.set_description(f"Last Valid: {code}")

    # 3. Semantic Analysis (Literacy)
    print("\n" + "=" * 70)
    print("SEMANTIC ANALYSIS")
    print("=" * 70)
    
    # Calculate Literacy Rate (Last 1000 epochs)
    literacy_rate = np.mean(history_Literacy[-1000:])
    
    print(f"{'Metric':<20} | {'Value':<10} | {'Meaning'}")
    print("-" * 70)
    print(f"{'Literacy Rate':<20} | {literacy_rate:.4f}     | {'Fluency' if literacy_rate > 0.8 else 'Babbling'}")
    print(f"{'Unique Phrases':<20} | {len(valid_codes):<10} | {'Creativity'}")
    print("-" * 70)
    
    print("\nTop Valid Expressions Discovered:")
    for code in list(valid_codes)[:10]:
        print(f"- '{code}'")
        
    if literacy_rate > 0.1:
        print("\nRESULT: LITERATE")
        print("Adam has learned the syntax of creation.")
    else:
        print("\nRESULT: ILLITERATE")
        print("Adam is still struggling with the alphabet.")

    # Visualization
    plt.figure(figsize=(12, 6))
    
    # Moving average of literacy
    window = 100
    literacy_smooth = np.convolve(history_Literacy, np.ones(window)/window, mode='valid')
    
    plt.plot(literacy_smooth, color='blue', alpha=0.7)
    plt.ylabel('Literacy Score (Reward)')
    plt.xlabel('Epoch')
    plt.title('The Education of Adam: Learning Python')
    plt.grid(True, alpha=0.3)
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"semantic_scribe_literacy_{timestamp}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to: {filename}")
    plt.close()

if __name__ == "__main__":
    run_scribe_test()
