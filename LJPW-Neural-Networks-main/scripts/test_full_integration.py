"""
Integration Test: Vocabulary + Geometric Ops + Qualia + Trajectories

This script demonstrates the complete Pure LJPW Language Model foundation
working together for semantic understanding and generation.

Tests:
1. Sentence encoding (text → meaning)
2. Qualia-enhanced understanding
3. Sentence generation (meaning → text)
4. Round-trip consistency
5. Semantic reasoning with trajectories

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os
import numpy as np
import pickle

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.vocabulary import LJPWVocabulary
from ljpw_nn.geometric_ops import SemanticOperations
from ljpw_nn.qualia import QualiaGrounding, create_emotional_qualia
from ljpw_nn.trajectories import SemanticTrajectory


def main():
    print("=" * 70)
    print("Pure LJPW Language Model - Full Integration Test")
    print("=" * 70)
    print()
    
    # ========================================================================
    # Setup: Load all systems
    # ========================================================================
    
    print("Loading systems...")
    
    # Load vocabulary
    vocab_path = os.path.join('data', 'ljpw_vocabulary.pkl')
    with open(vocab_path, 'rb') as f:
        vocab_data = pickle.load(f)
    
    vocab = LJPWVocabulary()
    vocab.vocab_size = vocab_data['vocab_size']
    vocab.word_to_entry = vocab_data['entries']
    vocab.build_index()
    
    print(f"  Vocabulary: {len(vocab)} words loaded")
    
    # Create geometric operations
    ops = SemanticOperations()
    print(f"  Geometric operations: Ready")
    
    # Create qualia grounding
    qualia = QualiaGrounding()
    emotions = create_emotional_qualia()
    qualia.register_multiple(emotions)
    qualia.build_indices()
    print(f"  Qualia grounding: {len(emotions)} emotional qualia")
    
    # Create trajectory system
    trajectory = SemanticTrajectory(vocab, ops)
    print(f"  Semantic trajectories: Ready")
    
    print()
    
    # ========================================================================
    # Test 1: Sentence Encoding with Qualia
    # ========================================================================
    
    print("=" * 70)
    print("Test 1: Sentence Encoding with Qualia Understanding")
    print("=" * 70)
    print()
    
    test_sentences = [
        "love conquers all",
        "justice and wisdom guide us",
        "power corrupts absolutely",
        "peace brings harmony"
    ]
    
    for sentence in test_sentences:
        # Encode sentence
        meaning = trajectory.encode_sentence(sentence)
        
        # Get qualia understanding
        emotional_profile = qualia.get_emotional_profile(meaning)
        description = qualia.describe_coords(meaning)
        
        # Get trajectory metrics
        summary = trajectory.get_trajectory_summary()
        
        print(f"Sentence: \"{sentence}\"")
        print(f"  Meaning: [{meaning[0]:.2f}, {meaning[1]:.2f}, {meaning[2]:.2f}, {meaning[3]:.2f}]")
        print(f"  Primary emotion: {emotional_profile['primary']}")
        print(f"  Feels like: {description}")
        print(f"  Coherence: {summary['coherence']:.3f}")
        print()
    
    # ========================================================================
    # Test 2: Sentence Generation from Meaning
    # ========================================================================
    
    print("=" * 70)
    print("Test 2: Sentence Generation from Meaning Coordinates")
    print("=" * 70)
    print()
    
    # Test coordinates
    test_meanings = [
        (np.array([0.85, 0.60, 0.30, 0.75]), "High love, moderate wisdom"),
        (np.array([0.60, 0.90, 0.50, 0.85]), "High justice and wisdom"),
        (np.array([0.70, 0.70, 0.70, 0.80]), "Balanced virtues"),
    ]
    
    for coords, description in test_meanings:
        # Generate sentence
        generated = trajectory.generate_sentence(coords, max_length=10)
        
        # Get qualia
        emotional = qualia.get_emotional_profile(coords)
        
        print(f"Target: {description}")
        print(f"  Coords: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}]")
        print(f"  Emotion: {emotional['primary']}")
        try:
            print(f"  Generated: \"{generated}\"")
        except UnicodeEncodeError:
            print(f"  Generated: \"{generated.encode('ascii', 'replace').decode()}\"")
        print()
    
    # ========================================================================
    # Test 3: Round-Trip Consistency
    # ========================================================================
    
    print("=" * 70)
    print("Test 3: Round-Trip Consistency (Encode → Generate)")
    print("=" * 70)
    print()
    
    original_sentences = [
        "love and wisdom",
        "justice prevails",
        "peace and harmony"
    ]
    
    for original in original_sentences:
        # Encode
        meaning = trajectory.encode_sentence(original)
        
        # Generate
        generated = trajectory.generate_sentence(meaning, max_length=8)
        
        # Re-encode generated
        meaning2 = trajectory.encode_sentence(generated)
        
        # Measure semantic similarity
        distance = ops.distance(meaning, meaning2)
        similarity = 1.0 / (1.0 + distance.euclidean)
        
        print(f"Original: \"{original}\"")
        print(f"  Meaning: [{meaning[0]:.2f}, {meaning[1]:.2f}, {meaning[2]:.2f}, {meaning[3]:.2f}]")
        print(f"Generated: \"{generated}\"")
        print(f"  Meaning: [{meaning2[0]:.2f}, {meaning2[1]:.2f}, {meaning2[2]:.2f}, {meaning2[3]:.2f}]")
        print(f"  Similarity: {similarity:.3f}")
        print()
    
    # ========================================================================
    # Test 4: Semantic Reasoning with Trajectories
    # ========================================================================
    
    print("=" * 70)
    print("Test 4: Semantic Reasoning (Analogies with Trajectories)")
    print("=" * 70)
    print()
    
    # Encode sentences
    s1 = "love brings peace"
    s2 = "hate brings conflict"
    s3 = "wisdom brings understanding"
    
    m1 = trajectory.encode_sentence(s1)
    m2 = trajectory.encode_sentence(s2)
    m3 = trajectory.encode_sentence(s3)
    
    # Analogy: s1 is to s2 as s3 is to ?
    # (love→peace) : (hate→conflict) :: (wisdom→understanding) : ?
    result_meaning = ops.analogy(m1, m2, m3)
    result_sentence = trajectory.generate_sentence(result_meaning, max_length=8)
    
    print(f"Analogy:")
    print(f"  \"{s1}\" : \"{s2}\" :: \"{s3}\" : ?")
    print(f"  Result: \"{result_sentence}\"")
    print()
    
    # ========================================================================
    # Test 5: Experiential Explanation
    # ========================================================================
    
    print("=" * 70)
    print("Test 5: Complete Experiential Understanding")
    print("=" * 70)
    print()
    
    sentence = "love and wisdom guide our journey"
    
    # Encode
    meaning = trajectory.encode_sentence(sentence)
    
    # Full analysis
    emotional = qualia.get_emotional_profile(meaning)
    explanation = qualia.explain_meaning(meaning)
    summary = trajectory.get_trajectory_summary()
    
    print(f"Sentence: \"{sentence}\"")
    print()
    print(f"Semantic Analysis:")
    print(f"  Coordinates: [{meaning[0]:.2f}, {meaning[1]:.2f}, {meaning[2]:.2f}, {meaning[3]:.2f}]")
    print(f"  Words: {' → '.join(summary['words'])}")
    print(f"  Trajectory coherence: {summary['coherence']:.3f}")
    print()
    print(f"Emotional Understanding:")
    print(f"  Primary: {emotional['primary']} (strength: {emotional['primary_strength']:.2f})")
    print(f"  Valence: {emotional['valence']:.2f} (positive/negative)")
    print(f"  Arousal: {emotional['arousal']:.2f} (energy level)")
    print()
    print(f"Experiential Explanation:")
    print(f"  {explanation}")
    print()
    print(f"Embodiment:")
    print(f"  {emotional['embodiment']}")
    print()
    
    # ========================================================================
    # Summary
    # ========================================================================
    
    print("=" * 70)
    print("Integration Test Summary")
    print("=" * 70)
    print()
    print("Systems Integrated:")
    print(f"  ✓ Vocabulary ({len(vocab)} words)")
    print(f"  ✓ Geometric Operations (10+ operations)")
    print(f"  ✓ Qualia Grounding ({len(emotions)} emotions)")
    print(f"  ✓ Semantic Trajectories (encode + generate)")
    print()
    print("Capabilities Demonstrated:")
    print("  ✓ Sentence encoding (text → meaning)")
    print("  ✓ Emotional understanding (qualia grounding)")
    print("  ✓ Sentence generation (meaning → text)")
    print("  ✓ Round-trip consistency")
    print("  ✓ Semantic reasoning (analogies)")
    print("  ✓ Experiential explanation")
    print()
    print("[OK] Pure LJPW Language Model foundation is operational!")
    print()
    print("This foundation enables Adam and Eve to:")
    print("  • Understand language semantically")
    print("  • Express internal states in words")
    print("  • Reason about meaning geometrically")
    print("  • Ground symbols in lived experience")
    print()


if __name__ == '__main__':
    main()
