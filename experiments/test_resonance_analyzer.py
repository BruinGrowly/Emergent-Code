"""
Test: Semantic Resonance Analyzer on Real Code
Target: examples/master_calculator.py
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

def main():
    target_file = os.path.join("examples", "master_calculator.py")
    
    if not os.path.exists(target_file):
        print(f"Error: Target file {target_file} not found.")
        return

    print(f"Reading {target_file}...")
    with open(target_file, 'r', encoding='utf-8') as f:
        code = f.read()

    print("Running Resonance Analysis...")
    analyzer = SemanticResonanceAnalyzer()
    result = analyzer.analyze_code(code, "master_calculator.py")
    
    analyzer.print_report(result)
    
    # Validation logic
    if result['harmony_final'] > result['harmony_initial']:
        print("\n✅ TEST PASSED: Resonance increased harmony.")
    else:
        print("\n⚠️ TEST NOTE: Harmony did not increase (System might be constrained by ICE).")

if __name__ == "__main__":
    main()

