"""
Load LJPW Language Data into Vocabulary System

This script loads all existing coordinate databases from data/LJPW_Language_Data/
and creates a unified LJPW vocabulary with 1,435+ words.

Files loaded:
- comprehensive_language_expansion.json (234 words)
- second_major_expansion.json (292 words)
- third_major_expansion.json (400 words)
- fourth_major_expansion.json (400 words)
- fifth_major_expansion.json (180 words)

Total: ~1,435 unique words with LJPW coordinates

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.vocabulary import LJPWVocabulary, VocabularyLoader
import numpy as np


def main():
    print("=" * 70)
    print("Loading LJPW Language Data")
    print("=" * 70)
    print()
    
    # Define data directory and files
    data_dir = os.path.join('data', 'LJPW_Language_Data')
    
    expansion_files = [
        'comprehensive_language_expansion.json',
        'second_major_expansion.json',
        'third_major_expansion.json',
        'fourth_major_expansion.json',
        'fifth_major_expansion.json'
    ]
    
    print(f"Data directory: {data_dir}")
    print(f"Files to load: {len(expansion_files)}")
    print()
    
    # Load all files
    print("Loading coordinate databases...")
    print("-" * 70)
    
    vocab = VocabularyLoader.load_multiple_files(expansion_files, data_dir)
    
    print("-" * 70)
    print()
    
    # Build index
    print("Building KD-tree spatial index...")
    vocab.build_index()
    print()
    
    # Display statistics
    print("=" * 70)
    print("Vocabulary Statistics")
    print("=" * 70)
    
    stats = vocab.get_statistics()
    
    print(f"\nTotal Words: {stats['size']}")
    print(f"\nLanguage Distribution:")
    for lang, count in sorted(stats['languages'].items()):
        # Handle unicode in language names
        try:
            print(f"  {lang}: {count} words")
        except UnicodeEncodeError:
            print(f"  {lang.encode('ascii', 'replace').decode()}: {count} words")
    
    print(f"\nSource Distribution:")
    for source, count in sorted(stats['sources'].items()):
        print(f"  {source}: {count} words")
    
    print(f"\nCoordinate Statistics:")
    print(f"  Mean: L={stats['coord_stats']['mean'][0]:.3f}, "
          f"J={stats['coord_stats']['mean'][1]:.3f}, "
          f"P={stats['coord_stats']['mean'][2]:.3f}, "
          f"W={stats['coord_stats']['mean'][3]:.3f}")
    print(f"  Std:  L={stats['coord_stats']['std'][0]:.3f}, "
          f"J={stats['coord_stats']['std'][1]:.3f}, "
          f"P={stats['coord_stats']['std'][2]:.3f}, "
          f"W={stats['coord_stats']['std'][3]:.3f}")
    
    print(f"\nHarmony Statistics:")
    print(f"  Mean: {stats['harmony_stats']['mean']:.3f}")
    print(f"  Std:  {stats['harmony_stats']['std']:.3f}")
    print(f"  Min:  {stats['harmony_stats']['min']:.3f}")
    print(f"  Max:  {stats['harmony_stats']['max']:.3f}")
    
    # Test some lookups
    print("\n" + "=" * 70)
    print("Testing Vocabulary Lookups")
    print("=" * 70)
    
    test_words = ['love', 'justice', 'power', 'wisdom', 'courage', 'compassion']
    
    print("\nWord -> Coordinates:")
    for word in test_words:
        if word in vocab:
            entry = vocab.get_entry(word)
            coords = entry.coords
            harmony = entry.harmony()
            print(f"  {word:12s}: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}] "
                  f"(H={harmony:.3f})")
        else:
            print(f"  {word:12s}: NOT FOUND")
    
    print("\nCoordinates -> Word (Nearest Neighbor):")
    test_coords_list = [
        ([0.90, 0.45, 0.20, 0.70], "High Love, Low Power"),
        ([0.50, 0.90, 0.50, 0.80], "High Justice, High Wisdom"),
        ([0.40, 0.40, 0.90, 0.60], "High Power"),
        ([0.70, 0.70, 0.70, 0.90], "High Wisdom, Balanced")
    ]
    
    for coords, description in test_coords_list:
        coords_array = np.array(coords)
        nearest = vocab.nearest_word(coords_array)
        nearest_3 = vocab.nearest_words_with_distances(coords_array, k=3)
        
        print(f"\n  {description}:")
        print(f"    Coords: [{coords[0]:.2f}, {coords[1]:.2f}, {coords[2]:.2f}, {coords[3]:.2f}]")
        
        # Handle unicode in word output
        try:
            print(f"    Nearest: {nearest}")
        except UnicodeEncodeError:
            print(f"    Nearest: {nearest.encode('ascii', 'replace').decode()}")
        
        print(f"    Top 3:")
        for word, dist in nearest_3:
            try:
                print(f"      {word:15s} (distance={dist:.4f})")
            except UnicodeEncodeError:
                safe_word = word.encode('ascii', 'replace').decode()
                print(f"      {safe_word:15s} (distance={dist:.4f})")
    
    # Save vocabulary
    print("\n" + "=" * 70)
    print("Saving Vocabulary")
    print("=" * 70)
    
    save_path = os.path.join('data', 'ljpw_vocabulary.pkl')
    vocab.save(save_path)
    print(f"\nVocabulary saved to: {save_path}")
    
    # Also save as JSON for inspection
    json_path = os.path.join('data', 'ljpw_vocabulary_stats.json')
    import json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"Statistics saved to: {json_path}")
    
    print("\n" + "=" * 70)
    print("[OK] LJPW Language Data Loading Complete!")
    print("=" * 70)
    print(f"\nLoaded {stats['size']} words with LJPW coordinates")
    print("Vocabulary ready for Pure LJPW Language Model")
    print()


if __name__ == '__main__':
    main()
