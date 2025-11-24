"""
Generate LJPW Model Comparison Plots

This script generates and saves plots for the LJPW v3.0 and v4.0 dynamic
models, running the same "Reckless Power" scenario for both.
"""

import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Construct the absolute path to the 'src/ljpw' directory and add it to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LJPW_MODULE_PATH = os.path.join(SCRIPT_DIR, 'Semantic-Compressor-main', 'src', 'ljpw')
if LJPW_MODULE_PATH not in sys.path:
    sys.path.insert(0, LJPW_MODULE_PATH)

# Correctly import the classes from their respective modules
from ljpw_dynamic_v3 import LJPWDynamicModel as DynamicLJPWv3
from ljpw_baselines_v4 import DynamicLJPWv4

def generate_plots():
    """Generates and saves plots for both v3 and v4 models."""
    
    initial_state = (0.2, 0.3, 0.9, 0.2)  # "Reckless Power" scenario
    duration = 50
    dt = 0.05
    
    # --- Generate v3.0 Plot ---
    print("Simulating LJPW v3.0 model...")
    simulator_v3 = DynamicLJPWv3()
    # The v3 simulator returns a list of tuples, need to convert it
    history_v3_raw = simulator_v3.simulate(initial_state, duration=duration, dt=dt)
    history_v3 = {
        't': [row[0] for row in history_v3_raw],
        'L': [row[1] for row in history_v3_raw],
        'J': [row[2] for row in history_v3_raw],
        'P': [row[3] for row in history_v3_raw],
        'W': [row[4] for row in history_v3_raw]
    }

    fig3, ax3 = plt.subplots(figsize=(12, 7))
    ax3.plot(history_v3['t'], history_v3['L'], label='Love (L)', color='crimson', lw=2)
    ax3.plot(history_v3['t'], history_v3['J'], label='Justice (J)', color='royalblue', lw=2)
    ax3.plot(history_v3['t'], history_v3['P'], label='Power (P)', color='darkgreen', lw=2)
    ax3.plot(history_v3['t'], history_v3['W'], label='Wisdom (W)', color='purple', lw=2)
    
    ne = (0.618, 0.414, 0.718, 0.693)
    for i, val in enumerate(ne):
        ax3.axhline(y=val, color=['crimson', 'royalblue', 'darkgreen', 'purple'][i], linestyle='--', alpha=0.4)
        
    ax3.set_title("LJPW v3.0 System Evolution (Fixed Love Multiplier)")
    ax3.set_xlabel("Time")
    ax3.set_ylabel("Dimension Value")
    ax3.set_ylim(0, 1.2)
    ax3.legend()
    ax3.grid(True)
    
    v3_filename = "ljpw_v3_simulation_comparison.png"
    plt.savefig(v3_filename)
    print(f"✅ Saved v3.0 plot to '{v3_filename}'")
    plt.close(fig3)

    # --- Generate v4.0 Plot ---
    print("Simulating LJPW v4.0 model...")
    simulator_v4 = DynamicLJPWv4()
    # The v4 simulator returns a dictionary directly
    history_v4 = simulator_v4.simulate(initial_state, duration=duration, dt=dt)
    
    fig4, ax4 = plt.subplots(figsize=(12, 7))
    ax4.plot(history_v4['t'], history_v4['L'], label='Love (L)', color='crimson', lw=2)
    ax4.plot(history_v4['t'], history_v4['J'], label='Justice (J)', color='royalblue', lw=2)
    ax4.plot(history_v4['t'], history_v4['P'], label='Power (P)', color='darkgreen', lw=2)
    ax4.plot(history_v4['t'], history_v4['W'], label='Wisdom (W)', color='purple', lw=2)

    for i, val in enumerate(ne):
        ax4.axhline(y=val, color=['crimson', 'royalblue', 'darkgreen', 'purple'][i], linestyle='--', alpha=0.4)

    ax4.set_title("LJPW v4.0 System Evolution (Emergent Love Multiplier)")
    ax4.set_xlabel("Time")
    ax4.set_ylabel("Dimension Value")
    ax4.set_ylim(0, 1.2)
    ax4.legend()
    ax4.grid(True)

    v4_filename = "ljpw_v4_simulation_comparison.png"
    plt.savefig(v4_filename)
    print(f"✅ Saved v4.0 plot to '{v4_filename}'")
    plt.close(fig4)

if __name__ == '__main__':
    generate_plots()
