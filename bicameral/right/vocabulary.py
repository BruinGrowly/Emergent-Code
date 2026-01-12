"""
LJPW Vocabulary System - Bidirectional Word ↔ Coordinate Mapping

This module implements the foundation of the Pure LJPW Language Model:
bidirectional mapping between words and LJPW semantic coordinates.

Core Components:
- LJPWVocabulary: Main vocabulary class with word↔coordinate mapping
- CoordinateIndex: Fast spatial indexing using KD-tree for nearest neighbor search
- VocabularyLoader: Load and merge coordinate databases from JSON files

Features:
- Word → coordinates lookup (semantic encoding)
- Coordinates → word lookup (semantic decoding)
- Fast nearest neighbor search (O(log n) with KD-tree)
- Unknown word estimation
- Vocabulary persistence (save/load)
- Multi-source database loading

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: December 4, 2025
Based on: LJPW LLM Training Paradigm
"""

import numpy as np
import json
import os
from typing import Dict, List, Optional, Tuple, Union, Any
from dataclasses import dataclass
from scipy.spatial import KDTree
import pickle


# Sacred constants
ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])  # JEHOVAH - Divine Perfection
NATURAL_EQUILIBRIUM = np.array([0.618, 0.414, 0.718, 0.693])  # (φ⁻¹, √2-1, e-2, ln2)


@dataclass
class WordEntry:
    """
    Single word entry in vocabulary.
    
    Attributes:
        word: The word/concept
        coords: LJPW coordinates [L, J, P, W]
        language: Language code (e.g., 'en', 'fr', 'zh')
        source: Source database file
        metadata: Additional information (POS, frequency, etc.)
    """
    word: str
    coords: np.ndarray
    language: str = 'en'
    source: str = ''
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        # Ensure coords is numpy array
        if not isinstance(self.coords, np.ndarray):
            self.coords = np.array(self.coords)
    
    def harmony(self) -> float:
        """
        Calculate harmony index (alignment with perfection).
        Formula: H = 1 / (1 + distance_from_anchor)
        """
        distance = np.linalg.norm(self.coords - ANCHOR_POINT)
        return 1.0 / (1.0 + distance)
    
    def distance_to(self, other_coords: np.ndarray) -> float:
        """Semantic distance to other coordinates"""
        return np.linalg.norm(self.coords - other_coords)


class CoordinateIndex:
    """
    Fast spatial indexing for coordinate → word lookup.
    
    Uses KD-tree for O(log n) nearest neighbor search in 4D LJPW space.
    """
    
    def __init__(self):
        self.kdtree: Optional[KDTree] = None
        self.word_list: List[str] = []
        self.coords_array: Optional[np.ndarray] = None
        
    def build_index(self, word_coords: Dict[str, np.ndarray]):
        """
        Build KD-tree index from word-coordinate pairs.
        
        Args:
            word_coords: Dictionary mapping words to LJPW coordinates
        """
        if not word_coords:
            raise ValueError("Cannot build index from empty vocabulary")
        
        # Extract words and coordinates
        self.word_list = list(word_coords.keys())
        coords_list = [word_coords[w] for w in self.word_list]
        self.coords_array = np.array(coords_list)
        
        # Build KD-tree for fast nearest neighbor search
        self.kdtree = KDTree(self.coords_array)
        
        print(f"Built KD-tree index with {len(self.word_list)} words")
    
    def query(self, 
             coords: np.ndarray, 
             k: int = 1,
             return_distances: bool = False) -> Union[str, List[str], Tuple]:
        """
        Find k nearest words to given coordinates.
        
        Args:
            coords: LJPW coordinates to search for
            k: Number of nearest neighbors to return
            return_distances: If True, also return distances
            
        Returns:
            If k=1: nearest word (or tuple with distance)
            If k>1: list of nearest words (or tuple with distances)
        """
        if self.kdtree is None:
            raise RuntimeError("Index not built. Call build_index() first.")
        
        # Query KD-tree
        distances, indices = self.kdtree.query(coords, k=k)
        
        # Get corresponding words
        if k == 1:
            nearest_word = self.word_list[indices]
            if return_distances:
                return nearest_word, distances
            return nearest_word
        else:
            nearest_words = [self.word_list[i] for i in indices]
            if return_distances:
                return nearest_words, distances
            return nearest_words
    
    def query_radius(self, coords: np.ndarray, radius: float) -> List[Tuple[str, float]]:
        """
        Find all words within radius of coordinates.
        
        Args:
            coords: LJPW coordinates
            radius: Search radius in semantic space
            
        Returns:
            List of (word, distance) tuples
        """
        if self.kdtree is None:
            raise RuntimeError("Index not built. Call build_index() first.")
        
        indices = self.kdtree.query_ball_point(coords, radius)
        results = []
        for i in indices:
            word = self.word_list[i]
            distance = np.linalg.norm(self.coords_array[i] - coords)
            results.append((word, distance))
        
        # Sort by distance
        results.sort(key=lambda x: x[1])
        return results


class LJPWVocabulary:
    """
    Main vocabulary class with bidirectional word ↔ coordinate mapping.
    
    Features:
    - Word → coordinates lookup (semantic encoding)
    - Coordinates → word lookup (semantic decoding)
    - Fast nearest neighbor search using KD-tree
    - Unknown word estimation
    - Vocabulary persistence
    """
    
    def __init__(self, vocab_size: int = 50000):
        # Auto-healed: Input validation for __init__
        if not isinstance(vocab_size, int):
            raise TypeError(f'vocab_size must be int, got {type(vocab_size).__name__}')
        self.vocab_size = vocab_size
        self.word_to_entry: Dict[str, WordEntry] = {}
        self.coord_index = CoordinateIndex()
        self._index_built = False
        
    def __len__(self) -> int:
        """Number of words in vocabulary"""
        return len(self.word_to_entry)
    
    def __contains__(self, word: str) -> bool:
        """Check if word is in vocabulary"""
        return word.lower() in self.word_to_entry
    
    def register(self, 
                word: str, 
                coords: Union[np.ndarray, List[float]],
                language: str = 'en',
                source: str = '',
                metadata: Optional[Dict] = None):
        """
        Add new word-coordinate pair to vocabulary.
        
        Args:
            word: The word/concept
            coords: LJPW coordinates [L, J, P, W]
            language: Language code
            source: Source database
            metadata: Additional information
        """
        if len(self.word_to_entry) >= self.vocab_size:
            print(f"Warning: Vocabulary size limit ({self.vocab_size}) reached")
            return
        
        # Normalize word (lowercase)
        word_key = word.lower()
        
        # Create entry
        if not isinstance(coords, np.ndarray):
            coords = np.array(coords)
        
        entry = WordEntry(
            word=word,
            coords=coords,
            language=language,
            source=source,
            metadata=metadata or {}
        )
        
        self.word_to_entry[word_key] = entry
        self._index_built = False  # Need to rebuild index
    
    def get_coords(self, word: str) -> Optional[np.ndarray]:
        # Auto-healed: Input validation for get_coords
        if word is not None and not isinstance(word, str):
            raise TypeError(f'word must be str, got {type(word).__name__}')
        """
        Get LJPW coordinates for a word.
        
        Args:
            word: Word to look up
            
        Returns:
            LJPW coordinates [L, J, P, W] or None if not found
        """
        word_key = word.lower()
        entry = self.word_to_entry.get(word_key)
        
        if entry is not None:
            return entry.coords.copy()
        else:
            # Try to estimate for unknown word
            return self.estimate_coords(word)
    
    def get_entry(self, word: str) -> Optional[WordEntry]:
        # Auto-healed: Input validation for get_entry
        if word is not None and not isinstance(word, str):
            raise TypeError(f'word must be str, got {type(word).__name__}')
        """Get full word entry with metadata"""
        return self.word_to_entry.get(word.lower())
    
    def nearest_word(self, 
                    coords: np.ndarray, 
                    k: int = 1,
                    exclude: Optional[List[str]] = None) -> Union[str, List[str]]:
        """
        Find nearest word(s) to given coordinates.
        
        Args:
            coords: LJPW coordinates
            k: Number of nearest words to return
            exclude: Words to exclude from results
            
        Returns:
            Nearest word (if k=1) or list of nearest words (if k>1)
        """
        if not self._index_built:
            self.build_index()
        
        if exclude:
            # Query more than k to account for exclusions
            candidates = self.coord_index.query(coords, k=k*3)
            if isinstance(candidates, str):
                candidates = [candidates]
            
            # Filter out excluded words
            filtered = [w for w in candidates if w.lower() not in [e.lower() for e in exclude]]
            
            if k == 1:
                return filtered[0] if filtered else None
            else:
                return filtered[:k]
        else:
            return self.coord_index.query(coords, k=k)
    
    def nearest_words_with_distances(self, 
                                    coords: np.ndarray, 
                                    k: int = 5) -> List[Tuple[str, float]]:
        """
        Find k nearest words with their distances.
        
        Returns:
            List of (word, distance) tuples
        """
        if not self._index_built:
            self.build_index()
        
        words, distances = self.coord_index.query(coords, k=k, return_distances=True)
        
        if k == 1:
            return [(words, distances)]
        else:
            return list(zip(words, distances))
    
    def words_in_radius(self, coords: np.ndarray, radius: float) -> List[Tuple[str, float]]:
        """
        Find all words within semantic radius.
        
        Args:
            coords: Center coordinates
            radius: Search radius
            
        Returns:
            List of (word, distance) tuples
        """
        if not self._index_built:
            self.build_index()
        
        return self.coord_index.query_radius(coords, radius)
    
    def estimate_coords(self, unknown_word: str) -> Optional[np.ndarray]:
        # Auto-healed: Input validation for estimate_coords
        if unknown_word is not None and not isinstance(unknown_word, str):
            raise TypeError(f'unknown_word must be str, got {type(unknown_word).__name__}')
        """
        Estimate coordinates for unknown word.
        
        Strategy:
        1. Try subword matching (prefixes, suffixes)
        2. Use Natural Equilibrium as fallback
        
        Args:
            unknown_word: Word not in vocabulary
            
        Returns:
            Estimated coordinates or None
        """
        # TODO: Implement sophisticated estimation
        # For now, return Natural Equilibrium as neutral estimate
        return NATURAL_EQUILIBRIUM.copy()
    
    def build_index(self):
        """Build KD-tree index for fast nearest neighbor search"""
        word_coords = {word: entry.coords for word, entry in self.word_to_entry.items()}
        self.coord_index.build_index(word_coords)
        self._index_built = True
    
    def save(self, path: str):
        # Auto-healed: Input validation for save
        if path is not None and not isinstance(path, str):
            raise TypeError(f'path must be str, got {type(path).__name__}')
        """
        Save vocabulary to disk.
        
        Args:
            path: File path (will save as pickle)
        """
        data = {
            'vocab_size': self.vocab_size,
            'entries': self.word_to_entry
        }
        
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        
        print(f"Saved vocabulary with {len(self)} words to {path}")
    
    def load(self, path: str):
        """
        Load vocabulary from disk.
        
        Args:
            path: File path to load from
        """
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        self.vocab_size = data['vocab_size']
        self.word_to_entry = data['entries']
        self._index_built = False
        
        print(f"Loaded vocabulary with {len(self)} words from {path}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get vocabulary statistics"""
        if not self.word_to_entry:
            return {'size': 0}
        
        coords_array = np.array([e.coords for e in self.word_to_entry.values()])
        harmonies = [e.harmony() for e in self.word_to_entry.values()]
        
        # Language distribution
        languages = {}
        for entry in self.word_to_entry.values():
            lang = entry.language
            languages[lang] = languages.get(lang, 0) + 1
        
        # Source distribution
        sources = {}
        for entry in self.word_to_entry.values():
            src = entry.source
            sources[src] = sources.get(src, 0) + 1
        
        return {
            'size': len(self),
            'languages': languages,
            'sources': sources,
            'coord_stats': {
                'mean': coords_array.mean(axis=0).tolist(),
                'std': coords_array.std(axis=0).tolist(),
                'min': coords_array.min(axis=0).tolist(),
                'max': coords_array.max(axis=0).tolist()
            },
            'harmony_stats': {
                'mean': np.mean(harmonies),
                'std': np.std(harmonies),
                'min': np.min(harmonies),
                'max': np.max(harmonies)
            }
        }


class VocabularyLoader:
    """
    Load and merge coordinate databases from JSON files.
    
    Supports multiple database formats:
    - Expansion files (comprehensive, second, third, fourth, fifth)
    - Multilingual files
    - Custom formats
    """
    
    @staticmethod
    def load_expansion_file(filepath: str) -> List[Dict]:
        """
        Load expansion JSON file.
        
        Expected format:
        {
            "metadata": {...},
            "mappings": [
                {"word": "love", "coordinates": [0.91, 0.47, 0.16, 0.72], ...},
                ...
            ]
        }
        
        Returns:
            List of word entries
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        mappings = data.get('mappings', [])
        
        entries = []
        for item in mappings:
            if isinstance(item, dict):
                word = item.get('word', item.get('concept', ''))
                
                # Try different coordinate key names
                coords = (item.get('coordinates') or 
                         item.get('coords') or 
                         item.get('ljpw_coordinates') or 
                         [])
                
                language = item.get('language', 'en')
                
                if word and coords and len(coords) == 4:
                    entries.append({
                        'word': word,
                        'coords': coords,
                        'language': language,
                        'metadata': item
                    })
        
        return entries
    
    @staticmethod
    def load_multiple_files(filepaths: List[str], 
                          data_dir: Optional[str] = None) -> LJPWVocabulary:
        """
        Load and merge multiple coordinate database files.
        
        Args:
            filepaths: List of JSON file paths
            data_dir: Base directory for files (optional)
            
        Returns:
            LJPWVocabulary with merged data
        """
        vocab = LJPWVocabulary(vocab_size=100000)
        
        total_loaded = 0
        total_duplicates = 0
        
        for filepath in filepaths:
            if data_dir:
                full_path = os.path.join(data_dir, filepath)
            else:
                full_path = filepath
            
            if not os.path.exists(full_path):
                print(f"Warning: File not found: {full_path}")
                continue
            
            try:
                entries = VocabularyLoader.load_expansion_file(full_path)
                
                loaded = 0
                duplicates = 0
                
                for entry in entries:
                    word = entry['word']
                    if word.lower() in vocab:
                        duplicates += 1
                    else:
                        vocab.register(
                            word=word,
                            coords=entry['coords'],
                            language=entry.get('language', 'en'),
                            source=os.path.basename(filepath),
                            metadata=entry.get('metadata', {})
                        )
                        loaded += 1
                
                total_loaded += loaded
                total_duplicates += duplicates
                
                print(f"Loaded {filepath}: {loaded} words ({duplicates} duplicates)")
                
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        print(f"\nTotal: {total_loaded} unique words loaded ({total_duplicates} duplicates skipped)")
        
        return vocab


# Example usage and testing
if __name__ == '__main__':
    print("=" * 70)
    print("LJPW Vocabulary System - Testing")
    print("=" * 70)
    print()
    
    # Create vocabulary
    vocab = LJPWVocabulary()
    
    # Add some test words
    test_words = {
        'love': [0.91, 0.47, 0.16, 0.72],
        'justice': [0.57, 0.91, 0.52, 0.84],
        'power': [0.42, 0.38, 0.94, 0.61],
        'wisdom': [0.68, 0.71, 0.53, 0.93],
        'courage': [0.67, 0.73, 0.81, 0.79],
        'compassion': [0.89, 0.42, 0.31, 0.68]
    }
    
    print("Registering test words...")
    for word, coords in test_words.items():
        vocab.register(word, coords)
    
    print(f"Vocabulary size: {len(vocab)}")
    print()
    
    # Test word -> coordinates
    print("Test: Word -> Coordinates")
    for word in ['love', 'justice', 'wisdom']:
        coords = vocab.get_coords(word)
        entry = vocab.get_entry(word)
        print(f"  {word}: {coords} (H={entry.harmony():.3f})")
    print()
    
    # Build index
    print("Building KD-tree index...")
    vocab.build_index()
    print()
    
    # Test coordinates -> word
    print("Test: Coordinates -> Word")
    test_coords = np.array([0.90, 0.45, 0.20, 0.70])
    nearest = vocab.nearest_word(test_coords)
    print(f"  Nearest to {test_coords}: {nearest}")
    
    # Test k-nearest
    print(f"\n  Top 3 nearest:")
    nearest_k = vocab.nearest_words_with_distances(test_coords, k=3)
    for word, dist in nearest_k:
        print(f"    {word}: distance={dist:.4f}")
    print()
    
    # Test radius search
    print("Test: Words in radius")
    words_nearby = vocab.words_in_radius(test_coords, radius=0.3)
    print(f"  Words within 0.3 of {test_coords}:")
    for word, dist in words_nearby[:5]:
        print(f"    {word}: distance={dist:.4f}")
    print()
    
    # Statistics
    print("Vocabulary Statistics:")
    stats = vocab.get_statistics()
    print(f"  Size: {stats['size']}")
    print(f"  Mean coords: {stats['coord_stats']['mean']}")
    print(f"  Mean harmony: {stats['harmony_stats']['mean']:.3f}")
    print()
    
    print("[OK] Vocabulary system tests complete!")

