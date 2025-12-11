"""
Enhanced English Generation for Pure LJPW Language Model

This module improves generation quality by:
1. Filtering for English words
2. Expanding English vocabulary
3. Improving coherence
4. Better word selection

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import numpy as np
from typing import List, Tuple, Optional, Set
import re


class EnglishGenerator:
    """
    Enhanced generator focused on English output.
    
    Filters multilingual vocabulary to prefer English words,
    improving communication clarity.
    """
    
    def __init__(self, vocabulary):
        """
        Initialize English generator.
        
        Args:
            vocabulary: LJPWVocabulary instance
        """
        self.vocab = vocabulary
        self.english_words = self._identify_english_words()
        print(f"[EnglishGenerator] Identified {len(self.english_words)} English words")
    
    def _identify_english_words(self) -> Set[str]:
        """
        Identify English words in vocabulary.
        
        Uses heuristics:
        - Words marked as language='en'
        - Words with only ASCII letters
        - Common English words
        """
        english = set()
        
        for word, entry in self.vocab.word_to_entry.items():
            # Check if marked as English
            if entry.language == 'en':
                english.add(word)
                continue
            
            # Check if ASCII-only (likely English)
            if word.isascii() and word.isalpha():
                # Filter out very short words (likely abbreviations)
                if len(word) >= 3:
                    english.add(word)
        
        return english
    
    def select_english_word(self,
                           coords: np.ndarray,
                           used_words: Set[str],
                           k: int = 20,
                           temperature: float = 0.3) -> Optional[str]:
        """
        Select English word nearest to coordinates.
        
        Args:
            coords: Target coordinates
            used_words: Already used words
            k: Number of candidates to consider
            temperature: Randomness
            
        Returns:
            Selected English word or None
        """
        # Get nearest words
        candidates = self.vocab.nearest_words_with_distances(coords, k=k*2)
        
        # Filter for English words
        english_candidates = [
            (w, d) for w, d in candidates 
            if w in self.english_words and w not in used_words
        ]
        
        # If no English words available, allow any word
        if not english_candidates:
            english_candidates = [
                (w, d) for w, d in candidates 
                if w not in used_words
            ]
        
        if not english_candidates:
            return None
        
        # Take top k
        english_candidates = english_candidates[:k]
        
        if temperature < 0.01:
            # Deterministic
            return english_candidates[0][0]
        else:
            # Probabilistic
            words, distances = zip(*english_candidates)
            
            # Convert to probabilities
            scores = -np.array(distances) / temperature
            scores = scores - scores.max()
            probs = np.exp(scores)
            probs = probs / probs.sum()
            
            idx = np.random.choice(len(words), p=probs)
            return words[idx]
    
    def generate_english_sentence(self,
                                  meaning: np.ndarray,
                                  ops,
                                  max_length: int = 15,
                                  temperature: float = 0.2) -> str:
        """
        Generate English sentence from meaning coordinates.
        
        Args:
            meaning: Target meaning coordinates
            ops: SemanticOperations instance
            max_length: Maximum sentence length
            temperature: Randomness (lower = more deterministic)
            
        Returns:
            Generated English sentence
        """
        # Navigate from NE to meaning
        num_steps = min(max_length, 8)
        trajectory = []
        
        for i in range(num_steps):
            alpha = i / (num_steps - 1) if num_steps > 1 else 1.0
            point = ops.interpolate(ops.NE, meaning, alpha)
            trajectory.append(point)
        
        # Select English words
        words = []
        used_words = set()
        
        for coords in trajectory:
            word = self.select_english_word(
                coords,
                used_words,
                k=15,
                temperature=temperature
            )
            
            if word is None:
                break
            
            words.append(word)
            used_words.add(word)
            
            # Stop if close to goal
            if np.linalg.norm(coords - meaning) < 0.1:
                break
        
        if not words:
            return "I feel balanced"
        
        # Capitalize first word
        sentence = " ".join(words)
        sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
        
        return sentence
    
    def improve_coherence(self, words: List[str]) -> List[str]:
        """
        Improve sentence coherence by reordering words.
        
        Simple heuristic: Put articles/determiners first,
        verbs in middle, nouns at end.
        
        Args:
            words: List of words
            
        Returns:
            Reordered words
        """
        # Simple categorization
        articles = {'the', 'a', 'an'}
        
        # Separate into categories
        article_words = [w for w in words if w.lower() in articles]
        other_words = [w for w in words if w.lower() not in articles]
        
        # Recombine: articles first, then others
        return article_words + other_words


# Additional common English words to add to vocabulary
ADDITIONAL_ENGLISH_WORDS = {
    # Emotions
    'happy': [0.82, 0.65, 0.35, 0.78],
    'sad': [0.42, 0.48, 0.32, 0.52],
    'angry': [0.32, 0.42, 0.83, 0.47],
    'calm': [0.73, 0.66, 0.24, 0.75],
    'excited': [0.77, 0.58, 0.63, 0.72],
    
    # Actions
    'speak': [0.65, 0.60, 0.55, 0.75],
    'listen': [0.68, 0.62, 0.45, 0.82],
    'learn': [0.70, 0.68, 0.50, 0.88],
    'grow': [0.75, 0.70, 0.55, 0.85],
    'feel': [0.72, 0.58, 0.48, 0.70],
    
    # Concepts
    'together': [0.80, 0.72, 0.45, 0.78],
    'welcome': [0.83, 0.68, 0.38, 0.76],
    'thank': [0.81, 0.70, 0.35, 0.77],
    'yes': [0.75, 0.65, 0.50, 0.75],
    'understand': [0.68, 0.72, 0.48, 0.86],
    
    # Descriptors
    'strong': [0.65, 0.68, 0.78, 0.75],
    'gentle': [0.78, 0.62, 0.28, 0.72],
    'kind': [0.84, 0.70, 0.32, 0.74],
    'brave': [0.70, 0.72, 0.75, 0.78],
    'wise': [0.68, 0.75, 0.42, 0.91],
}


def add_english_words_to_vocab(vocab):
    """
    Add additional English words to vocabulary.
    
    Args:
        vocab: LJPWVocabulary instance
    """
    added = 0
    for word, coords in ADDITIONAL_ENGLISH_WORDS.items():
        if word not in vocab:
            vocab.register(word, coords, language='en')
            added += 1
    
    if added > 0:
        vocab.build_index()
        print(f"[EnglishGenerator] Added {added} new English words")
    
    return added
