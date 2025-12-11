"""
Add English Core Vocabulary to LJPW Vocabulary

This script extracts English equivalents from the multilingual database
and adds them as English entries to the vocabulary.

This gives us English words like "love", "justice", "power", "wisdom", etc.
with their LJPW coordinates.

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os
import json
import pickle

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.vocabulary import LJPWVocabulary
import numpy as np


def main():
    print("=" * 70)
    print("Adding English Core Vocabulary")
    print("=" * 70)
    print()
    
    # Load existing vocabulary
    print("Loading existing vocabulary...")
    vocab_path = os.path.join('data', 'ljpw_vocabulary.pkl')
    
    with open(vocab_path, 'rb') as f:
        vocab_data = pickle.load(f)
    
    vocab = LJPWVocabulary()
    vocab.vocab_size = vocab_data['vocab_size']
    vocab.word_to_entry = vocab_data['entries']
    
    print(f"Loaded {len(vocab)} words")
    print()
    
    # Extract English equivalents from multilingual words
    print("Extracting English equivalents...")
    
    english_added = 0
    english_duplicates = 0
    
    # Go through all entries and extract english_equivalent
    for word_key, entry in list(vocab.word_to_entry.items()):
        metadata = entry.metadata
        english_equiv = metadata.get('english_equivalent', '')
        
        if english_equiv and english_equiv.lower() not in vocab:
            # Add English version with same coordinates
            vocab.register(
                word=english_equiv,
                coords=entry.coords,
                language='en',
                source=entry.source,
                metadata={
                    'derived_from': word_key,
                    'original_language': entry.language,
                    **metadata
                }
            )
            english_added += 1
        elif english_equiv:
            english_duplicates += 1
    
    print(f"Added {english_added} English words")
    print(f"Skipped {english_duplicates} duplicates")
    print()
    
    # Rebuild index
    print("Rebuilding KD-tree index...")
    vocab.build_index()
    print()
    
    # Test English lookups
    print("=" * 70)
    print("Testing English Vocabulary")
    print("=" * 70)
    print()
    
    test_words = ['love', 'justice', 'power', 'wisdom', 'courage', 
                  'compassion', 'truth', 'beauty', 'harmony', 'peace']
    
    print("English Word Lookups:")
    found = 0
    for word in test_words:
        if word in vocab:
            entry = vocab.get_entry(word)
            coords = entry.coords
            harmony = entry.harmony()
            print(f"  {word:12s}: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}] "
                  f"(H={harmony:.3f})")
            found += 1
        else:
            print(f"  {word:12s}: NOT FOUND")
    
    print(f"\nFound: {found}/{len(test_words)} test words")
    print()
    
    # Get statistics
    stats = vocab.get_statistics()
    
    print("=" * 70)
    print("Updated Vocabulary Statistics")
    print("=" * 70)
    print()
    print(f"Total Words: {stats['size']}")
    print(f"\nLanguage Distribution:")
    for lang, count in sorted(stats['languages'].items())[:10]:
        try:
            print(f"  {lang}: {count} words")
        except UnicodeEncodeError:
            print(f"  {lang.encode('ascii', 'replace').decode()}: {count} words")
    print(f"  ... ({len(stats['languages'])} languages total)")
    
    # Save updated vocabulary
    print("\n" + "=" * 70)
    print("Saving Updated Vocabulary")
    print("=" * 70)
    print()
    
    vocab.save(vocab_path)
    print(f"Saved to: {vocab_path}")
    
    # Save statistics
    json_path = os.path.join('data', 'ljpw_vocabulary_stats.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Statistics saved to: {json_path}")
    
    print("\n" + "=" * 70)
    print("[OK] English Core Vocabulary Added!")
    print("=" * 70)
    print(f"\nTotal vocabulary: {stats['size']} words")
    print(f"English words: {stats['languages'].get('en', 0)}")
    print()


if __name__ == '__main__':
    main()
