"""
Recursive Evolution Cycle (5 Steps)
The System improving its own components iteratively.
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer
from ljpw_quantum.resonance_grower import ResonanceGrower

def evolve_component(filename, iteration):
    print(f"\nEVOLUTION STEP {iteration}: Analyzing {filename}...")
    
    filepath = os.path.join("ljpw_quantum", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
        
    analyzer = SemanticResonanceAnalyzer()
    report = analyzer.analyze_code(code, filename)
    
    print(f"   Current State: H={report['harmony_final']:.3f} | Deficit: {report['deficit_dimension']}")
    
    # Generate Improvement
    grower = ResonanceGrower()
    intent = f"Evolve {filename} to fix {report['deficit_dimension']} deficit"
    blueprint = grower.generate_blueprint(intent, "Core System Evolution")
    
    # Save Evolution Artifact
    artifact_name = f"EVOLUTION_{iteration}_{filename.replace('.py', '')}_PLAN.md"
    artifact_path = os.path.join("organized", "project_docs", artifact_name)
    
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write(f"# Evolution Step {iteration}: {filename}\n\n")
        f.write(f"**Diagnosis:** Deficit in {report['deficit_dimension']}\n")
        f.write(f"**Harmony:** {report['harmony_initial']:.3f} -> {report['harmony_final']:.3f}\n\n")
        f.write(blueprint)
        
    print(f"   Evolution Plan Generated: {artifact_path}")

def main():
    print("INITIATING 5-STEP RECURSIVE EVOLUTION")
    print("=" * 50)
    
    targets = [
        "resonance_engine.py",
        "ice_container.py",
        "resonance_grower.py",
        "semantic_resonance_analyzer.py",
        "bicameral_bridge.py"
    ]
    
    for i, target in enumerate(targets, 1):
        evolve_component(target, i)
        time.sleep(0.5)
        
    print("\n" + "=" * 50)
    print("EVOLUTION COMPLETE")
    print("5 Components Analyzed. 5 Growth Plans Generated.")

if __name__ == "__main__":
    main()
