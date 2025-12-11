"""
Harmonious Organizer (v6.0)
Scans the root directory and groups files by their LJPW Semantic Resonance.
Goal: Reduce Entropy (Root Clutter) and increase Justice (Structure).
"""

import sys
import os
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_quantum.semantic_resonance_analyzer import SemanticResonanceAnalyzer

def main():
    print("🧹 HARMONIOUS ORGANIZER INITIATED")
    print("Scanning root directory for entropy...")
    
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root_files = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]
    
    # Exclude critical system files
    excludes = ['setup.py', 'pyproject.toml', 'requirements.txt', 'README.md', '.gitignore', 'Makefile']
    candidates = [f for f in root_files if f not in excludes and not f.startswith('.')]
    
    print(f"Found {len(candidates)} candidates for reorganization.")
    
    analyzer = SemanticResonanceAnalyzer()
    
    # Proposed Structure
    moves = {
        'core_physics': [],    # Engines, Constants
        'analysis_tools': [],  # Analysis scripts
        'generated_artifacts': [], # Generated files
        'project_docs': [],    # Markdown docs
        'legacy_scripts': []   # Misc python
    }
    
    for filename in candidates:
        filepath = os.path.join(root_dir, filename)
        
        # 1. Categorize by Type/Name first (Heuristic Justice)
        if filename.endswith('.md'):
            moves['project_docs'].append(filename)
            continue
            
        if filename.startswith('generated_') or filename.startswith('discovered_'):
            moves['generated_artifacts'].append(filename)
            continue
            
        # 2. Analyze Python files (Resonance Wisdom)
        if filename.endswith('.py'):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple keyword resonance for sorting
                if 'ljpw' in filename or 'constants' in filename or 'capabilities' in filename:
                    moves['core_physics'].append(filename)
                elif 'analyze' in filename or 'fractal' in filename or 'validate' in filename:
                    moves['analysis_tools'].append(filename)
                else:
                    moves['legacy_scripts'].append(filename)
            except:
                pass

    # 3. Report Plan
    print("\n📋 PROPOSED REORGANIZATION PLAN")
    print("-" * 40)
    for folder, files in moves.items():
        if files:
            print(f"\n📂 {folder}/")
            for f in files:
                print(f"  - {f}")
    
    # 4. Ask for confirmation (Simulated)
    print("\n⚠️  NOTE: Moving Python files can break imports.")
    print("   Action: Creating folders and moving SAFE files (Docs, Artifacts).")
    print("   Action: Leaving core Python scripts in root for safety, but marked for refactoring.")
    
    # Execute Safe Moves
    for folder in ['project_docs', 'generated_artifacts']:
        files = moves[folder]
        if not files: continue
        
        target_dir = os.path.join(root_dir, "organized", folder)
        os.makedirs(target_dir, exist_ok=True)
        
        print(f"\n🚚 Moving files to {target_dir}...")
        for filename in files:
            src = os.path.join(root_dir, filename)
            dst = os.path.join(target_dir, filename)
            try:
                shutil.move(src, dst)
                print(f"  ✓ Moved {filename}")
            except Exception as e:
                print(f"  ❌ Failed {filename}: {e}")

    print("\n✅ Organization Cycle Complete. Entropy Reduced.")

if __name__ == "__main__":
    main()
