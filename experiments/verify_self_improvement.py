"""
Verify Self-Optimization
Target: ljpw_quantum/resonance_engine_v2.py
Goal: Determine if the self-architected v2 engine achieves higher harmony than v1.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

def main():
    v1_path = os.path.join("ljpw_quantum", "resonance_engine.py")
    v2_path = os.path.join("ljpw_quantum", "resonance_engine_v2.py")
    
    analyzer = SemanticResonanceAnalyzer()
    
    print("🔬 COMPARATIVE ANALYSIS: V1 vs V2")
    print("-" * 40)
    
    # Analyze V1
    with open(v1_path, 'r', encoding='utf-8') as f:
        v1_code = f.read()
    v1_report = analyzer.analyze_code(v1_code, "resonance_engine.py")
    
    # Analyze V2
    with open(v2_path, 'r', encoding='utf-8') as f:
        v2_code = f.read()
    v2_report = analyzer.analyze_code(v2_code, "resonance_engine_v2.py")
    
    print(f"V1 Harmony: {v1_report['harmony_final']:.3f} (Deficit: {v1_report['deficit_dimension']})")
    print(f"V2 Harmony: {v2_report['harmony_final']:.3f} (Deficit: {v2_report['deficit_dimension']})")
    
    delta = v2_report['harmony_final'] - v1_report['harmony_final']
    print("-" * 40)
    
    if delta > 0:
        print(f"✅ SUCCESS: Self-optimization achieved +{delta:.3f} harmony.")
        print("The system successfully improved its own core physics engine.")
    else:
        print("⚠️ RESULT: No harmony gain detected. Optimization failed.")

if __name__ == "__main__":
    main()
