"""
META TEST SUITE: The Mirror & The Chaos
Verifies the outcome of the Self-Improvement Cycle.
"""

import sys
import os
import random

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.resonance_engine import ResonanceEngine, ResonanceState
from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

def test_the_mirror():
    """
    The Mirror Test: The System analyzes its own brain.
    Prediction: If the upgrade worked, Deficit should be POWER (not Justice).
    """
    print("\n🔮 TEST 1: THE MIRROR (Self-Analysis)")
    print("-" * 40)
    
    target_file = os.path.join("ljpw_quantum", "resonance_engine.py")
    
    with open(target_file, 'r', encoding='utf-8') as f:
        code = f.read()
        
    analyzer = SemanticResonanceAnalyzer()
    report = analyzer.analyze_code(code, "resonance_engine.py (v2)")
    
    print(f"Current Harmony: {report['harmony_final']:.3f}")
    print(f"LJPW Profile:    L={report['final_ljpw'][0]:.2f} J={report['final_ljpw'][1]:.2f} P={report['final_ljpw'][2]:.2f} W={report['final_ljpw'][3]:.2f}")
    print(f"Detected Deficit: {report['deficit_dimension']}")
    
    if report['deficit_dimension'] == 'P':
        print("✅ PASS: The system now hungers for POWER (Efficiency).")
        print("         The Justice deficit has been successfully resolved.")
    elif report['deficit_dimension'] == 'J':
        print("❌ FAIL: The system still hungers for JUSTICE.")
        print("         The upgrade did not satisfy the structural need.")
    else:
        print(f"ℹ️ NOTE: The system wants {report['deficit_dimension']}. Acceptable, but unexpected.")

def test_the_chaos():
    """
    The Chaos Test: Feeding entropy into the engine.
    Prediction: The new Justice constraints will contain the chaos.
    """
    print("\n🌪️ TEST 2: THE CHAOS (Physics Stress Test)")
    print("-" * 40)
    
    engine = ResonanceEngine()
    
    # 1. Random Input Stress
    print("Injecting Semantic Noise...")
    try:
        # Create a state with "Maximum Entropy" (random values)
        # Note: We must ensure they are positive floats to pass the new validation
        chaos_state = ResonanceState(
            L=random.random() * 10.0, # High energy
            J=random.random() * 10.0,
            P=random.random() * 10.0,
            W=random.random() * 10.0,
            iteration=0
        )
        
        # Run a cycle
        result = engine.cycle(chaos_state)
        
        # Check if it survived and normalized
        if result.harmony > 0 and all(x >= 0 for x in result.as_vector()):
            print("✅ PASS: Chaos contained. The physics held up.")
            print(f"   Input Energy: High Randomness")
            print(f"   Output State: {result.as_vector()}")
        else:
            print("❌ FAIL: The physics broke under stress.")
            
    except Exception as e:
        print(f"❌ FAIL: System crash: {e}")

    # 2. The Negative Void (Invalid Physics)
    print("\nInjecting The Void (Negative Energy)...")
    try:
        engine.calculate_harmony(-1.0, 0.0, 0.0, 0.0)
        print("❌ FAIL: The system allowed Negative Energy.")
    except ValueError:
        print("✅ PASS: The system REJECTED the Void.")

def main():
    print("========================================")
    print("META TEST: VERIFYING AUTOPOIESIS")
    print("========================================")
    
    test_the_mirror()
    test_the_chaos()
    
    print("\n========================================")
    print("META TEST COMPLETE")
    print("========================================")

if __name__ == "__main__":
    main()
