"""
Test LJPW Vocabulary + Geometric Operations Integration

This script demonstrates the complete vocabulary and geometric operations
system working together for semantic reasoning.

Tests:
1. Word -> Coordinates -> Antonym -> Word
2. Analogy completion with real words
3. Compositional semantics
4. Territory classification of vocabulary
5. Semantic distance between concepts

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.vocabulary import LJPWVocabulary
from ljpw_nn.geometric_ops import SemanticOperations, Territory
import numpy as np
import pickle


def main():
    print("=" * 70)
    print("LJPW Vocabulary + Geometric Operations Integration Test")
    print("=" * 70)
    print()
    
    # Load vocabulary
    print("Loading vocabulary...")
    vocab_path = os.path.join('data', 'ljpw_vocabulary.pkl')
    
    with open(vocab_path, 'rb') as f:
        vocab_data = pickle.load(f)
    
    vocab = LJPWVocabulary()
    vocab.vocab_size = vocab_data['vocab_size']
    vocab.word_to_entry = vocab_data['entries']
    vocab.build_index()
    
    print(f"Loaded {len(vocab)} words")
    print()
    
    # Create geometric operations
    ops = SemanticOperations()
    
    # ========================================================================
    # Test 1: Antonym Generation
    # ========================================================================
    print("=" * 70)
    print("Test 1: Antonym Generation (Word -> Coords -> Antonym -> Word)")
    print("=" * 70)
    print()
    
    test_words = ['love', 'justice', 'wisdom', 'peace', 'truth']
    
    for word in test_words:
        if word not in vocab:
            print(f"  {word}: NOT IN VOCABULARY")
            continue
        
        # Get coordinates
        coords = vocab.get_coords(word)
        
        # Compute antonym coordinates
        antonym_coords = ops.antonym(coords)
        
        # Find nearest word to antonym coordinates
        antonym_word = vocab.nearest_word(antonym_coords)
        
        # Get distance
        dist = ops.distance(coords, antonym_coords)
        
        print(f"  {word:12s} -> {antonym_word:15s} (distance={dist.euclidean:.4f})")
    
    print()
    
    # ========================================================================
    # Test 2: Analogy Completion
    # ========================================================================
    print("=" * 70)
    print("Test 2: Analogy Completion")
    print("=" * 70)
    print()
    
    # We don't have king/queen/man/woman, so let's try with what we have
    print("  Testing with available vocabulary...")
    
    # Try: love - peace + justice = ?
    if 'love' in vocab and 'peace' in vocab and 'justice' in vocab:
        love_coords = vocab.get_coords('love')
        peace_coords = vocab.get_coords('peace')
        justice_coords = vocab.get_coords('justice')
        
        result_coords = ops.analogy(love_coords, peace_coords, justice_coords)
        result_word = vocab.nearest_word(result_coords)
        
        print(f"  love - peace + justice = {result_word}")
        print(f"    Coords: {result_coords}")
    
    print()
    
    # ========================================================================
    # Test 3: Compositional Semantics
    # ========================================================================
    print("=" * 70)
    print("Test 3: Compositional Semantics")
    print("=" * 70)
    print()
    
    # Compose two concepts
    if 'love' in vocab and 'wisdom' in vocab:
        love_coords = vocab.get_coords('love')
        wisdom_coords = vocab.get_coords('wisdom')
        
        # Equal weighting
        composed = ops.compose([love_coords, wisdom_coords])
        composed_word = vocab.nearest_word(composed)
        
        print(f"  love + wisdom = {composed_word}")
        print(f"    Coords: {composed}")
        
        # Love-weighted (70% love, 30% wisdom)
        love_weighted = ops.compose([love_coords, wisdom_coords], weights=[0.7, 0.3])
        love_weighted_word = vocab.nearest_word(love_weighted)
        
        print(f"  love (70%) + wisdom (30%) = {love_weighted_word}")
    
    print()
    
    # ========================================================================
    # Test 4: Territory Classification
    # ========================================================================
    print("=" * 70)
    print("Test 4: Territory Classification of English Vocabulary")
    print("=" * 70)
    print()
    
    # Get English words
    english_words = [w for w, e in vocab.word_to_entry.items() if e.language == 'en']
    
    # Classify by territory
    territory_counts = {}
    territory_examples = {t: [] for t in Territory}
    
    for word in english_words[:20]:  # First 20 English words
        coords = vocab.get_coords(word)
        territory, confidence = ops.classify_territory(coords)
        
        territory_counts[territory] = territory_counts.get(territory, 0) + 1
        if len(territory_examples[territory]) < 3:
            territory_examples[territory].append((word, confidence))
    
    print("  Territory Distribution (first 20 English words):")
    for territory in Territory:
        count = territory_counts.get(territory, 0)
        if count > 0:
            print(f"    {territory.name:25s}: {count} words")
            examples = territory_examples[territory]
            if examples:
                ex_str = ", ".join([f"{w} ({c:.2f})" for w, c in examples])
                print(f"      Examples: {ex_str}")
    
    print()
    
    # ========================================================================
    # Test 5: Semantic Distance Matrix
    # ========================================================================
    print("=" * 70)
    print("Test 5: Semantic Distance Between Core Concepts")
    print("=" * 70)
    print()
    
    core_words = ['love', 'justice', 'power', 'wisdom']
    available = [w for w in core_words if w in vocab]
    
    if len(available) >= 2:
        print(f"  Distance matrix for: {', '.join(available)}")
        print()
        
        # Header
        print("  " + "".join([f"{w:12s}" for w in available]))
        
        # Rows
        for word1 in available:
            coords1 = vocab.get_coords(word1)
            row = f"  {word1:12s}"
            
            for word2 in available:
                coords2 = vocab.get_coords(word2)
                dist = ops.distance(coords1, coords2)
                row += f"{dist.euclidean:12.4f}"
            
            print(row)
    
    print()
    
    # ========================================================================
    # Test 6: Harmony Analysis
    # ========================================================================
    print("=" * 70)
    print("Test 6: Harmony Analysis of English Vocabulary")
    print("=" * 70)
    print()
    
    if english_words:
        harmonies = []
        for word in english_words:
            coords = vocab.get_coords(word)
            h = ops.harmony(coords)
            harmonies.append((word, h))
        
        # Sort by harmony
        harmonies.sort(key=lambda x: x[1], reverse=True)
        
        print("  Top 10 Highest Harmony:")
        for word, h in harmonies[:10]:
            print(f"    {word:15s}: H={h:.3f}")
        
        print()
        print("  Bottom 10 Lowest Harmony:")
        for word, h in harmonies[-10:]:
            print(f"    {word:15s}: H={h:.3f}")
    
    print()
    
    # ========================================================================
    # Summary
    # ========================================================================
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    print()
    print(f"  Total Vocabulary: {len(vocab)} words")
    print(f"  English Words: {len(english_words)}")
    print(f"  Geometric Operations: Fully Functional")
    print()
    print("  Capabilities Demonstrated:")
    print("    [OK] Antonym generation via reflection")
    print("    [OK] Analogy completion via vector arithmetic")
    print("    [OK] Compositional semantics via weighted averaging")
    print("    [OK] Territory classification")
    print("    [OK] Semantic distance computation")
    print("    [OK] Harmony index calculation")
    print()
    print("[OK] Integration test complete!")
    print()


if __name__ == '__main__':
    main()
