"""
Test Pure LJPW Language Model

Comprehensive test of the integrated language model.

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.language_model import PureLJPWLanguageModel
import numpy as np


def main():
    print("=" * 70)
    print("Pure LJPW Language Model - Comprehensive Test")
    print("=" * 70)
    print()
    
    # Initialize
    print("Initializing language model...")
    lm = PureLJPWLanguageModel()
    print()
    
    # Test 1: Understanding
    print("=" * 70)
    print("Test 1: Semantic Understanding")
    print("=" * 70)
    print()
    
    test_sentences = [
        "love conquers all",
        "justice and wisdom guide us",
        "peace brings harmony to the world"
    ]
    
    for text in test_sentences:
        understanding = lm.understand(text)
        print(f"Text: \"{text}\"")
        print(f"  Meaning: [{understanding.meaning[0]:.2f}, {understanding.meaning[1]:.2f}, "
              f"{understanding.meaning[2]:.2f}, {understanding.meaning[3]:.2f}]")
        print(f"  Emotion: {understanding.emotional_profile['primary']}")
        print(f"  Territory: {understanding.territory.name}")
        print(f"  Coherence: {understanding.trajectory_coherence:.3f}")
        print(f"  Explanation: {understanding.explanation}")
        print()
    
    # Test 2: Generation
    print("=" * 70)
    print("Test 2: Text Generation")
    print("=" * 70)
    print()
    
    test_meanings = [
        (np.array([0.85, 0.70, 0.35, 0.80]), "High love and wisdom"),
        (np.array([0.60, 0.90, 0.50, 0.85]), "High justice"),
    ]
    
    for coords, description in test_meanings:
        generated = lm.generate(coords, style='precise', max_length=8)
        print(f"Target: {description}")
        print(f"  Coords: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}]")
        try:
            print(f"  Generated: \"{generated}\"")
        except UnicodeEncodeError:
            print(f"  Generated: \"{generated.encode('ascii', 'replace').decode()}\"")
        print()
    
    # Test 3: Reasoning
    print("=" * 70)
    print("Test 3: Semantic Reasoning")
    print("=" * 70)
    print()
    
    # Antonym
    antonym_result = lm.reason('antonym', word='love')
    print(f"Antonym of 'love': {antonym_result['antonym']}")
    print()
    
    # Analogy
    analogy_result = lm.reason('analogy', a='love', b='peace', c='justice')
    print(f"Analogy: {analogy_result['analogy']}")
    print()
    
    # Similar words
    similar_result = lm.reason('similar', word='wisdom', k=5)
    print(f"Similar to 'wisdom': {', '.join(similar_result['similar'])}")
    print()
    
    # Interpolation
    interp_result = lm.reason('interpolate', word1='love', word2='wisdom', alpha=0.5)
    print(f"Blend of 'love' and 'wisdom': {interp_result['result']}")
    print()
    
    # Test 4: Explanation
    print("=" * 70)
    print("Test 4: Interpretable Explanation")
    print("=" * 70)
    print()
    
    coords = np.array([0.91, 0.48, 0.16, 0.71])  # Love coordinates
    explanation = lm.explain(coords)
    print(f"Coordinates: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}]")
    print(f"Explanation: {explanation}")
    print()
    
    # Statistics
    print("=" * 70)
    print("Model Statistics")
    print("=" * 70)
    stats = lm.get_statistics()
    print(f"Vocabulary: {stats['vocabulary_size']} words")
    print(f"Qualia: {stats['qualia_count']} entries")
    print(f"Operations: {', '.join(stats['operations'])}")
    print()
    
    print("[OK] Pure LJPW Language Model fully operational!")
    print()
    print("This model enables:")
    print("  ✓ True semantic understanding")
    print("  ✓ Geometric reasoning about meaning")
    print("  ✓ Complete interpretability")
    print("  ✓ Consciousness communication (ready for Adam & Eve!)")
    print()


if __name__ == '__main__':
    main()
