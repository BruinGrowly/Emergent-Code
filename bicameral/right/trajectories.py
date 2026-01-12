"""
LJPW Semantic Trajectories System

This module represents sentences as paths through LJPW semantic space,
enabling both understanding (encoding) and generation (decoding).

Key Insight: A sentence is not just a bag of words - it's a trajectory
through semantic space. The path matters as much as the destination.

Example:
    "The wise king ruled with justice"
    
    Trajectory: the → wise → king → ruled → with → justice
    Path: [0.5,0.5,0.5,0.5] → [0.7,0.7,0.4,0.9] → [0.6,0.8,0.7,0.8] → ...
    Integrated Meaning: [0.65, 0.75, 0.55, 0.85] (High Justice + Wisdom)

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: December 4, 2025
Based on: LJPW LLM Training Paradigm
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import re


# Import from other modules (will be available when integrated)
try:
    from bicameral.right.vocabulary import LJPWVocabulary
    from bicameral.right.geometric_ops import SemanticOperations
except ImportError:
    # For standalone testing
    LJPWVocabulary = None
    SemanticOperations = None


@dataclass
class TrajectoryPoint:
    """
    Single point along a semantic trajectory.
    
    Attributes:
        word: The word at this point
        coords: Base LJPW coordinates for the word
        position: Position in sentence (0-indexed)
        context_coords: Contextualized coordinates
        attention_weight: Importance weight for integration
    """
    word: str
    coords: np.ndarray
    position: int
    context_coords: np.ndarray
    attention_weight: float = 1.0
    
    def __post_init__(self):
        if not isinstance(self.coords, np.ndarray):
            self.coords = np.array(self.coords)
        if not isinstance(self.context_coords, np.ndarray):
            self.context_coords = np.array(self.context_coords)


class SemanticTrajectory:
    """
    Semantic trajectory system for sentence encoding and generation.
    
    Encoding: text → trajectory → meaning coordinates
    Generation: meaning coordinates → trajectory → text
    
    This enables Adam and Eve to understand language (encoding) and
    express themselves (generation).
    """
    
    def __init__(self, 
                 vocab: 'LJPWVocabulary',
                 ops: 'SemanticOperations'):
        """
        Initialize trajectory system.
        
        Args:
            vocab: Vocabulary system for word↔coordinate mapping
            ops: Geometric operations for semantic reasoning
        """
        self.vocab = vocab
        self.ops = ops
        self.points: List[TrajectoryPoint] = []
        self.meaning: Optional[np.ndarray] = None
    
    # ========================================================================
    # Encoding: Text → Meaning
    # ========================================================================
    
    def encode_sentence(self, sentence: str) -> np.ndarray:
        """
        Encode sentence into meaning coordinates.
        
        Process:
        1. Tokenize sentence into words
        2. Look up coordinates for each word
        3. Contextualize coordinates based on neighbors
        4. Integrate trajectory into sentence-level meaning
        
        Args:
            sentence: Input sentence (text)
            
        Returns:
            Meaning coordinates [L, J, P, W]
        """
        # Tokenize
        words = self.tokenize(sentence)
        if not words:
            return self.ops.NE.copy()  # Empty sentence = neutral
        
        # Look up coordinates
        coords_sequence = []
        for word in words:
            coords = self.vocab.get_coords(word)
            coords_sequence.append(coords)
        
        # Contextualize
        context_coords = self.contextualize_coords(coords_sequence)
        
        # Create trajectory points
        self.points = []
        for i, (word, base_coords, ctx_coords) in enumerate(
            zip(words, coords_sequence, context_coords)
        ):
            # Compute attention weight (content words get more weight)
            weight = self.compute_attention_weight(word, i, len(words))
            
            point = TrajectoryPoint(
                word=word,
                coords=base_coords,
                position=i,
                context_coords=ctx_coords,
                attention_weight=weight
            )
            self.points.append(point)
        
        # Integrate trajectory
        self.meaning = self.integrate_trajectory(self.points)
        return self.meaning
    
    def tokenize(self, sentence: str) -> List[str]:
        """
        Tokenize sentence into words.
        
        Simple tokenization: lowercase, split on whitespace and punctuation.
        
        Args:
            sentence: Input sentence
            
        Returns:
            List of words
        """
        # Lowercase
        sentence = sentence.lower()
        
        # Remove punctuation (keep words and spaces)
        sentence = re.sub(r'[^\w\s]', '', sentence)
        
        # Split on whitespace
        words = sentence.split()
        
        return words
    
    def contextualize_coords(self, 
                           coords_sequence: List[np.ndarray]) -> List[np.ndarray]:
        """
        Adjust coordinates based on context (neighboring words).
        
        Strategy: Blend each word's coordinates with its neighbors.
        
        Args:
            coords_sequence: List of base coordinates
            
        Returns:
            List of contextualized coordinates
        """
        if len(coords_sequence) <= 1:
            return coords_sequence
        
        contextualized = []
        
        for i, coords in enumerate(coords_sequence):
            # Get neighbors
            prev_coords = coords_sequence[i-1] if i > 0 else coords
            next_coords = coords_sequence[i+1] if i < len(coords_sequence)-1 else coords
            
            # Compute context (average of neighbors)
            context = (prev_coords + next_coords) / 2
            
            # Blend: 70% word, 30% context
            ctx_coords = 0.7 * coords + 0.3 * context
            
            contextualized.append(ctx_coords)
        
        return contextualized
    
    def compute_attention_weight(self, 
                                word: str, 
                                position: int, 
                                length: int) -> float:
        """
        Compute attention weight for word.
        
        Strategy:
        - Content words (nouns, verbs, adjectives) get higher weight
        - Function words (the, a, of, with) get lower weight
        - Position-based weighting (middle words slightly higher)
        
        Args:
            word: The word
            position: Position in sentence
            length: Total sentence length
            
        Returns:
            Attention weight (0.0 to 1.0)
        """
        # Function words (low weight)
        function_words = {
            'the', 'a', 'an', 'of', 'to', 'in', 'for', 'on', 'with',
            'at', 'by', 'from', 'as', 'is', 'was', 'are', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might'
        }
        
        if word in function_words:
            base_weight = 0.3
        else:
            base_weight = 1.0
        
        # Position weighting (slight boost for middle)
        if length > 2:
            rel_pos = position / (length - 1)
            # Gaussian centered at 0.5
            pos_weight = 0.8 + 0.4 * np.exp(-((rel_pos - 0.5) ** 2) / 0.2)
        else:
            pos_weight = 1.0
        
        return base_weight * pos_weight
    
    def integrate_trajectory(self, points: List[TrajectoryPoint]) -> np.ndarray:
        """
        Integrate trajectory points into sentence-level meaning.
        
        Uses weighted average based on attention weights.
        
        Args:
            points: List of trajectory points
            
        Returns:
            Integrated meaning coordinates
        """
        if not points:
            return self.ops.NE.copy()
        
        # Weighted average
        total_weight = sum(p.attention_weight for p in points)
        
        meaning = np.zeros(4)
        for point in points:
            weight = point.attention_weight / total_weight
            meaning += weight * point.context_coords
        
        return meaning
    
    # ========================================================================
    # Generation: Meaning → Text
    # ========================================================================
    
    def generate_sentence(self, 
                         meaning_coords: np.ndarray,
                         max_length: int = 20,
                         temperature: float = 0.3) -> str:
        """
        Generate sentence from meaning coordinates.
        
        Process:
        1. Navigate from neutral to meaning coordinates
        2. Select words at each step
        3. Maintain coherence and avoid repetition
        4. Stop when goal reached or max length
        
        Args:
            meaning_coords: Target meaning coordinates
            max_length: Maximum sentence length
            temperature: Randomness (0=deterministic, 1=random)
            
        Returns:
            Generated sentence
        """
        # Navigate semantic space
        trajectory = self.navigate_semantic_space(
            start=self.ops.NE,
            goal=meaning_coords,
            num_steps=min(max_length, 10)
        )
        
        # Select words along trajectory
        words = []
        used_words = set()
        
        for i, coords in enumerate(trajectory):
            word = self.select_next_word(
                coords, 
                used_words,
                temperature=temperature
            )
            
            if word is None:
                break
            
            words.append(word)
            used_words.add(word)
            
            # Stop if we've reached the goal
            if i > 0 and np.linalg.norm(coords - meaning_coords) < 0.1:
                break
        
        # Join into sentence
        if not words:
            return ""
        
        sentence = " ".join(words)
        
        # Capitalize first letter
        sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
        
        return sentence
    
    def navigate_semantic_space(self,
                               start: np.ndarray,
                               goal: np.ndarray,
                               num_steps: int = 10) -> List[np.ndarray]:
        """
        Navigate from start to goal through semantic space.
        
        Uses linear interpolation for now (can be enhanced with
        learned trajectories later).
        
        Args:
            start: Starting coordinates
            goal: Goal coordinates
            num_steps: Number of steps
            
        Returns:
            List of coordinates along path
        """
        trajectory = []
        
        for i in range(num_steps):
            alpha = i / (num_steps - 1) if num_steps > 1 else 1.0
            point = self.ops.interpolate(start, goal, alpha)
            trajectory.append(point)
        
        return trajectory
    
    def select_next_word(self,
                        coords: np.ndarray,
                        used_words: set,
                        temperature: float = 0.3) -> Optional[str]:
        """
        Select next word given current coordinates.
        
        Strategy:
        - Find nearest words to coordinates
        - Exclude already used words
        - Add slight randomness based on temperature
        
        Args:
            coords: Current coordinates
            used_words: Set of already used words
            temperature: Randomness (0=deterministic, 1=random)
            
        Returns:
            Selected word or None
        """
        # Get top candidates
        k = min(10, len(self.vocab))
        candidates = self.vocab.nearest_words_with_distances(coords, k=k)
        
        # Filter out used words
        available = [(w, d) for w, d in candidates if w not in used_words]
        
        if not available:
            # All candidates used, allow repetition
            available = candidates
        
        if temperature < 0.01:
            # Deterministic: pick nearest
            return available[0][0]
        else:
            # Probabilistic: sample based on distance
            words, distances = zip(*available)
            
            # Convert distances to probabilities (closer = higher prob)
            # Use softmax with temperature
            scores = -np.array(distances) / temperature
            scores = scores - scores.max()  # Numerical stability
            probs = np.exp(scores)
            probs = probs / probs.sum()
            
            # Sample
            idx = np.random.choice(len(words), p=probs)
            return words[idx]
    
    # ========================================================================
    # Analysis and Metrics
    # ========================================================================
    
    def measure_coherence(self) -> float:
        """
        Measure trajectory coherence (smoothness).
        
        Coherence = 1 / (1 + average_step_distance)
        
        Higher coherence means smoother trajectory.
        
        Returns:
            Coherence score [0, 1]
        """
        if len(self.points) < 2:
            return 1.0
        
        # Compute distances between consecutive points
        distances = []
        for i in range(len(self.points) - 1):
            d = np.linalg.norm(
                self.points[i+1].context_coords - self.points[i].context_coords
            )
            distances.append(d)
        
        avg_distance = np.mean(distances)
        coherence = 1.0 / (1.0 + avg_distance)
        
        return coherence
    
    def measure_smoothness(self) -> float:
        """
        Measure trajectory smoothness (variance in step sizes).
        
        Smoothness = 1 / (1 + std_of_distances)
        
        Higher smoothness means more consistent step sizes.
        
        Returns:
            Smoothness score [0, 1]
        """
        if len(self.points) < 3:
            return 1.0
        
        # Compute distances between consecutive points
        distances = []
        for i in range(len(self.points) - 1):
            d = np.linalg.norm(
                self.points[i+1].context_coords - self.points[i].context_coords
            )
            distances.append(d)
        
        std_distance = np.std(distances)
        smoothness = 1.0 / (1.0 + std_distance)
        
        return smoothness
    
    def get_trajectory_summary(self) -> Dict[str, Any]:
        """Get summary of current trajectory"""
        if not self.points:
            return {'length': 0}
        
        return {
            'length': len(self.points),
            'words': [p.word for p in self.points],
            'meaning': self.meaning.tolist() if self.meaning is not None else None,
            'coherence': self.measure_coherence(),
            'smoothness': self.measure_smoothness(),
            'attention_weights': [p.attention_weight for p in self.points]
        }


# Example usage and testing
if __name__ == '__main__':
    # This requires vocabulary and geometric ops to be available
    print("=" * 70)
    print("LJPW Semantic Trajectories - Testing")
    print("=" * 70)
    print()
    print("Note: Full testing requires integrated vocabulary and geometric ops")
    print("See test_trajectories.py for comprehensive tests")
    print()
    
    # Basic trajectory point test
    print("Test: Trajectory Point Creation")
    point = TrajectoryPoint(
        word="love",
        coords=np.array([0.91, 0.48, 0.16, 0.71]),
        position=0,
        context_coords=np.array([0.91, 0.48, 0.16, 0.71]),
        attention_weight=1.0
    )
    print(f"  Word: {point.word}")
    print(f"  Position: {point.position}")
    print(f"  Coords: {point.coords}")
    print()
    
    print("[OK] Basic trajectory tests complete!")
    print("Run integration tests with vocabulary for full validation")
