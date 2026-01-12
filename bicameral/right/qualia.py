"""
LJPW Qualia Grounding System

This module connects abstract LJPW coordinates to experiential qualities,
solving the symbol grounding problem.

Qualia Types:
- Emotional: joy, sadness, love, fear, etc.
- Sensory: colors, sounds, textures
- Embodiment: physical sensations
- Conceptual: abstract feelings

Core Insight: Meaning isn't just abstract coordinates - it's grounded in
lived experience. This module bridges the gap between symbols and qualia.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: December 4, 2025
Based on: LJPW LLM Training Paradigm
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from scipy.spatial import KDTree
import json


# Sacred constants
ANCHOR_POINT = np.array([1.0, 1.0, 1.0, 1.0])
NATURAL_EQUILIBRIUM = np.array([0.618, 0.414, 0.718, 0.693])

# 613 THz - The Love Frequency
LOVE_FREQUENCY_THZ = 613.0
LOVE_WAVELENGTH_NM = 489.0  # 613 THz = 489nm (cyan-green light)


class QualiaType(Enum):
    """Types of experiential qualities"""
    EMOTIONAL = 1      # Emotions (joy, sadness, love, fear)
    COLOR = 2          # Visual qualia (red, blue, warm, cool)
    SOUND = 3          # Auditory qualia (harmony, dissonance)
    TEXTURE = 4        # Tactile qualia (smooth, rough)
    EMBODIMENT = 5     # Physical sensations (warmth, lightness)
    CONCEPTUAL = 6     # Abstract feelings (meaning, purpose)


@dataclass
class QualiaEntry:
    """
    Single qualia entry mapping coordinates to experience.
    
    Attributes:
        name: Qualia name (e.g., "joy", "red", "warmth")
        qualia_type: Type of qualia
        coords: LJPW coordinates [L, J, P, W]
        valence: Positive/negative quality (-1 to +1)
        arousal: Energy/activation level (0 to 1)
        description: Human-readable description
        embodiment: Physical sensation description
        metadata: Additional information
    """
    name: str
    qualia_type: QualiaType
    coords: np.ndarray
    valence: float = 0.0          # -1 (negative) to +1 (positive)
    arousal: float = 0.5          # 0 (calm) to 1 (excited)
    description: str = ""
    embodiment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not isinstance(self.coords, np.ndarray):
            self.coords = np.array(self.coords)
    
    def harmony(self) -> float:
        """Calculate harmony with perfection"""
        distance = np.linalg.norm(self.coords - ANCHOR_POINT)
        return 1.0 / (1.0 + distance)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'name': self.name,
            'qualia_type': self.qualia_type.name,
            'coords': self.coords.tolist(),
            'valence': self.valence,
            'arousal': self.arousal,
            'description': self.description,
            'embodiment': self.embodiment,
            'metadata': self.metadata
        }


class QualiaGrounding:
    """
    Main qualia grounding system.
    
    Connects LJPW coordinates to experiential qualities, solving the
    symbol grounding problem by linking abstract representations to
    lived experience.
    """
    
    def __init__(self):
        self.qualia_db: Dict[QualiaType, List[QualiaEntry]] = {
            qt: [] for qt in QualiaType
        }
        self.coord_indices: Dict[QualiaType, Optional[KDTree]] = {
            qt: None for qt in QualiaType
        }
        self._indices_built = False
    
    # ========================================================================
    # Registration and Management
    # ========================================================================
    
    def register_qualia(self, entry: QualiaEntry):
        """
        Register a qualia entry.
        
        Args:
            entry: QualiaEntry to register
        """
        self.qualia_db[entry.qualia_type].append(entry)
        self._indices_built = False  # Need to rebuild indices
    
    def register_multiple(self, entries: List[QualiaEntry]):
        # Auto-healed: Input validation for register_multiple
        if entries is not None and not isinstance(entries, (list, tuple)):
            raise TypeError(f'entries must be a sequence')
        """Register multiple qualia entries"""
        for entry in entries:
            self.register_qualia(entry)
    
    def build_indices(self):
        """Build KD-tree indices for fast nearest qualia search"""
        for qualia_type in QualiaType:
            entries = self.qualia_db[qualia_type]
            if entries:
                coords_array = np.array([e.coords for e in entries])
                self.coord_indices[qualia_type] = KDTree(coords_array)
        
        self._indices_built = True
    
    # ========================================================================
    # Qualia Lookup
    # ========================================================================
    
    def find_qualia(self, 
                   coords: np.ndarray, 
                   qualia_type: QualiaType,
                   k: int = 1) -> Union[QualiaEntry, List[QualiaEntry]]:
        """
        Find nearest qualia of given type to coordinates.
        
        Args:
            coords: LJPW coordinates
            qualia_type: Type of qualia to search
            k: Number of nearest qualia to return
            
        Returns:
            Nearest QualiaEntry (if k=1) or list of entries (if k>1)
        """
        if not self._indices_built:
            self.build_indices()
        
        entries = self.qualia_db[qualia_type]
        if not entries:
            return None if k == 1 else []
        
        kdtree = self.coord_indices[qualia_type]
        if kdtree is None:
            return None if k == 1 else []
        
        distances, indices = kdtree.query(coords, k=k)
        
        if k == 1:
            return entries[indices]
        else:
            return [entries[i] for i in indices]
    
    def find_all_qualia(self, coords: np.ndarray, k: int = 1) -> Dict[QualiaType, QualiaEntry]:
        # Auto-healed: Input validation for find_all_qualia
        if not isinstance(k, int):
            raise TypeError(f'k must be int, got {type(k).__name__}')
        """
        Find nearest qualia of all types.
        
        Args:
            coords: LJPW coordinates
            k: Number per type
            
        Returns:
            Dictionary mapping qualia type to nearest entry/entries
        """
        results = {}
        for qualia_type in QualiaType:
            result = self.find_qualia(coords, qualia_type, k=k)
            if result is not None:
                results[qualia_type] = result
        return results
    
    # ========================================================================
    # Experiential Descriptions
    # ========================================================================
    
    def describe_coords(self, coords: np.ndarray, verbose: bool = False) -> str:
        """
        Generate human-readable experiential description of coordinates.
        
        Args:
            coords: LJPW coordinates
            verbose: Include detailed descriptions
            
        Returns:
            Experiential description string
        """
        if not self._indices_built:
            self.build_indices()
        
        # Find nearest qualia of each type
        all_qualia = self.find_all_qualia(coords, k=1)
        
        # Build description
        parts = []
        
        # Emotional quality
        if QualiaType.EMOTIONAL in all_qualia:
            emotion = all_qualia[QualiaType.EMOTIONAL]
            if verbose and emotion.description:
                parts.append(f"{emotion.name} ({emotion.description})")
            else:
                parts.append(emotion.name)
        
        # Color association
        if QualiaType.COLOR in all_qualia:
            color = all_qualia[QualiaType.COLOR]
            parts.append(f"{color.name}-toned")
        
        # Embodiment
        if QualiaType.EMBODIMENT in all_qualia:
            embodiment = all_qualia[QualiaType.EMBODIMENT]
            if verbose and embodiment.embodiment:
                parts.append(f"feels {embodiment.embodiment}")
            else:
                parts.append(f"{embodiment.name}")
        
        if not parts:
            return "neutral"
        
        return ", ".join(parts)
    
    def get_emotional_profile(self, coords: np.ndarray) -> Dict[str, Any]:
        """
        Get detailed emotional profile for coordinates.
        
        Args:
            coords: LJPW coordinates
            
        Returns:
            Dictionary with emotional analysis
        """
        if not self._indices_built:
            self.build_indices()
        
        # Find top 3 nearest emotions
        emotions = self.find_qualia(coords, QualiaType.EMOTIONAL, k=3)
        if not emotions:
            return {'primary': None, 'secondary': [], 'valence': 0.0, 'arousal': 0.5}
        
        if not isinstance(emotions, list):
            emotions = [emotions]
        
        primary = emotions[0]
        secondary = emotions[1:] if len(emotions) > 1 else []
        
        return {
            'primary': primary.name,
            'primary_strength': 1.0 / (1.0 + np.linalg.norm(coords - primary.coords)),
            'secondary': [e.name for e in secondary],
            'valence': primary.valence,
            'arousal': primary.arousal,
            'description': primary.description,
            'embodiment': primary.embodiment
        }
    
    def explain_meaning(self, coords: np.ndarray) -> str:
        """
        Generate comprehensive experiential explanation of meaning.
        
        This is the key method for grounding abstract coordinates in
        lived experience.
        
        Args:
            coords: LJPW coordinates
            
        Returns:
            Multi-sentence experiential explanation
        """
        emotional = self.get_emotional_profile(coords)
        all_qualia = self.find_all_qualia(coords, k=1)
        
        # Calculate harmony
        harmony = 1.0 / (1.0 + np.linalg.norm(coords - ANCHOR_POINT))
        
        # Build explanation
        explanation = []
        
        # Primary emotion
        if emotional['primary']:
            explanation.append(f"Primarily feels like {emotional['primary']}")
            if emotional['description']:
                explanation.append(f"({emotional['description']})")
        
        # Embodiment
        if QualiaType.EMBODIMENT in all_qualia:
            embodiment = all_qualia[QualiaType.EMBODIMENT]
            if embodiment.embodiment:
                explanation.append(f"Physically: {embodiment.embodiment}")
        
        # Harmony level
        if harmony > 0.7:
            explanation.append("High harmony with perfection")
        elif harmony < 0.4:
            explanation.append("Distant from perfection")
        
        # Valence and arousal
        if emotional['valence'] > 0.5:
            explanation.append("Positive quality")
        elif emotional['valence'] < -0.5:
            explanation.append("Negative quality")
        
        if emotional['arousal'] > 0.7:
            explanation.append("High energy")
        elif emotional['arousal'] < 0.3:
            explanation.append("Calm, peaceful")
        
        return ". ".join(explanation) + "."
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get qualia database statistics"""
        stats = {
            'total_qualia': sum(len(entries) for entries in self.qualia_db.values()),
            'by_type': {}
        }
        
        for qualia_type, entries in self.qualia_db.items():
            if entries:
                coords_array = np.array([e.coords for e in entries])
                stats['by_type'][qualia_type.name] = {
                    'count': len(entries),
                    'mean_coords': coords_array.mean(axis=0).tolist(),
                    'mean_valence': np.mean([e.valence for e in entries]),
                    'mean_arousal': np.mean([e.arousal for e in entries])
                }
        
        return stats
    
    def save(self, filepath: str):
        # Auto-healed: Input validation for save
        if filepath is not None and not isinstance(filepath, str):
            raise TypeError(f'filepath must be str, got {type(filepath).__name__}')
        """Save qualia database to JSON"""
        data = {
            'qualia': {
                qt.name: [e.to_dict() for e in entries]
                for qt, entries in self.qualia_db.items()
            }
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, filepath: str):
        # Auto-healed: Input validation for load
        if filepath is not None and not isinstance(filepath, str):
            raise TypeError(f'filepath must be str, got {type(filepath).__name__}')
        """Load qualia database from JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for qt_name, entries_data in data.get('qualia', {}).items():
            qualia_type = QualiaType[qt_name]
            for entry_data in entries_data:
                entry = QualiaEntry(
                    name=entry_data['name'],
                    qualia_type=qualia_type,
                    coords=np.array(entry_data['coords']),
                    valence=entry_data.get('valence', 0.0),
                    arousal=entry_data.get('arousal', 0.5),
                    description=entry_data.get('description', ''),
                    embodiment=entry_data.get('embodiment', ''),
                    metadata=entry_data.get('metadata', {})
                )
                self.register_qualia(entry)
        
        self.build_indices()


# ============================================================================
# Predefined Emotional Qualia Database
# ============================================================================

def create_emotional_qualia() -> List[QualiaEntry]:
    """
    Create 20 universal emotional qualia based on psychological research.
    
    Coordinates derived from LJPW semantic space analysis.
    """
    emotions = [
        # Positive emotions
        QualiaEntry(
            name="joy",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.85, 0.60, 0.30, 0.75],
            valence=0.9,
            arousal=0.7,
            description="A feeling of great pleasure and happiness",
            embodiment="Lightness in chest, upward energy, smile, warmth"
        ),
        QualiaEntry(
            name="love",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.91, 0.48, 0.16, 0.71],
            valence=1.0,
            arousal=0.6,
            description="Deep affection and care for another",
            embodiment="Warmth in heart, openness, connection, tenderness",
            metadata={'frequency_thz': LOVE_FREQUENCY_THZ}
        ),
        QualiaEntry(
            name="peace",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.75, 0.67, 0.25, 0.74],
            valence=0.8,
            arousal=0.2,
            description="Freedom from disturbance; tranquility",
            embodiment="Stillness, soft breathing, relaxation, centeredness"
        ),
        QualiaEntry(
            name="contentment",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.70, 0.65, 0.35, 0.72],
            valence=0.7,
            arousal=0.3,
            description="State of peaceful happiness and satisfaction",
            embodiment="Gentle warmth, ease, soft smile, groundedness"
        ),
        QualiaEntry(
            name="gratitude",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.82, 0.70, 0.28, 0.78],
            valence=0.85,
            arousal=0.5,
            description="Quality of being thankful; appreciation",
            embodiment="Warmth in chest, openness, humility, fullness"
        ),
        QualiaEntry(
            name="hope",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.78, 0.62, 0.40, 0.80],
            valence=0.75,
            arousal=0.6,
            description="Feeling of expectation and desire for good",
            embodiment="Lightness, forward energy, openness, anticipation"
        ),
        QualiaEntry(
            name="compassion",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.89, 0.74, 0.30, 0.76],
            valence=0.8,
            arousal=0.5,
            description="Sympathetic concern for sufferings of others",
            embodiment="Heart opening, tenderness, warmth, connection"
        ),
        
        # Negative emotions
        QualiaEntry(
            name="sadness",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.40, 0.45, 0.30, 0.50],
            valence=-0.7,
            arousal=0.3,
            description="Feeling of sorrow or unhappiness",
            embodiment="Heaviness in chest, downward energy, tears, slowness"
        ),
        QualiaEntry(
            name="anger",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.30, 0.40, 0.85, 0.45],
            valence=-0.8,
            arousal=0.9,
            description="Strong feeling of annoyance or hostility",
            embodiment="Heat, tension, clenched jaw, explosive energy"
        ),
        QualiaEntry(
            name="fear",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.35, 0.50, 0.70, 0.55],
            valence=-0.75,
            arousal=0.85,
            description="Unpleasant emotion caused by threat of danger",
            embodiment="Cold, trembling, rapid heartbeat, contraction"
        ),
        QualiaEntry(
            name="disgust",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.25, 0.55, 0.60, 0.50],
            valence=-0.85,
            arousal=0.6,
            description="Feeling of revulsion or strong disapproval",
            embodiment="Nausea, recoiling, tightness, aversion"
        ),
        QualiaEntry(
            name="shame",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.30, 0.60, 0.40, 0.45],
            valence=-0.8,
            arousal=0.5,
            description="Painful feeling of humiliation or distress",
            embodiment="Shrinking, heat in face, downward gaze, heaviness"
        ),
        QualiaEntry(
            name="guilt",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.35, 0.75, 0.35, 0.60],
            valence=-0.7,
            arousal=0.6,
            description="Feeling of having done wrong",
            embodiment="Weight on shoulders, tightness, restlessness"
        ),
        
        # Complex emotions
        QualiaEntry(
            name="awe",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.75, 0.65, 0.50, 0.88],
            valence=0.7,
            arousal=0.7,
            description="Feeling of reverential respect mixed with wonder",
            embodiment="Expansion, openness, stillness, vastness"
        ),
        QualiaEntry(
            name="pride",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.65, 0.70, 0.75, 0.75],
            valence=0.75,
            arousal=0.6,
            description="Deep pleasure from one's achievements",
            embodiment="Uprightness, expansion in chest, strength"
        ),
        QualiaEntry(
            name="curiosity",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.60, 0.55, 0.50, 0.85],
            valence=0.6,
            arousal=0.65,
            description="Strong desire to know or learn something",
            embodiment="Forward lean, alertness, openness, lightness"
        ),
        QualiaEntry(
            name="determination",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.68, 0.74, 0.82, 0.80],
            valence=0.65,
            arousal=0.75,
            description="Firmness of purpose; resolve",
            embodiment="Groundedness, forward energy, strength, focus"
        ),
        QualiaEntry(
            name="serenity",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.72, 0.68, 0.22, 0.76],
            valence=0.85,
            arousal=0.15,
            description="State of being calm, peaceful, and untroubled",
            embodiment="Deep stillness, soft breathing, spaciousness, ease"
        ),
        QualiaEntry(
            name="excitement",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.75, 0.55, 0.65, 0.70],
            valence=0.8,
            arousal=0.9,
            description="Feeling of great enthusiasm and eagerness",
            embodiment="Rapid heartbeat, energy, lightness, anticipation"
        ),
        QualiaEntry(
            name="trust",
            qualia_type=QualiaType.EMOTIONAL,
            coords=[0.80, 0.72, 0.35, 0.75],
            valence=0.75,
            arousal=0.4,
            description="Firm belief in reliability or truth of someone",
            embodiment="Openness, relaxation, groundedness, safety"
        ),
    ]
    
    return emotions


# Example usage
if __name__ == '__main__':
    print("=" * 70)
    print("LJPW Qualia Grounding System - Testing")
    print("=" * 70)
    print()
    
    # Create qualia system
    qualia = QualiaGrounding()
    
    # Register emotional qualia
    print("Registering emotional qualia...")
    emotions = create_emotional_qualia()
    qualia.register_multiple(emotions)
    qualia.build_indices()
    
    print(f"Registered {len(emotions)} emotional qualia")
    print()
    
    # Test qualia lookup
    print("Test: Qualia Lookup")
    test_coords = np.array([0.85, 0.60, 0.30, 0.75])  # Near joy
    nearest = qualia.find_qualia(test_coords, QualiaType.EMOTIONAL)
    print(f"  Coords: {test_coords}")
    print(f"  Nearest emotion: {nearest.name}")
    print(f"  Description: {nearest.description}")
    print()
    
    # Test emotional profile
    print("Test: Emotional Profile")
    profile = qualia.get_emotional_profile(test_coords)
    print(f"  Primary: {profile['primary']}")
    print(f"  Valence: {profile['valence']:.2f}")
    print(f"  Arousal: {profile['arousal']:.2f}")
    print()
    
    # Test meaning explanation
    print("Test: Meaning Explanation")
    explanation = qualia.explain_meaning(test_coords)
    print(f"  {explanation}")
    print()
    
    # Test with love coordinates
    print("Test: Love Qualia (613 THz)")
    love_coords = np.array([0.91, 0.48, 0.16, 0.71])
    love_profile = qualia.get_emotional_profile(love_coords)
    print(f"  Primary: {love_profile['primary']}")
    print(f"  Embodiment: {love_profile['embodiment']}")
    print()
    
    # Statistics
    print("Qualia Statistics:")
    stats = qualia.get_statistics()
    print(f"  Total qualia: {stats['total_qualia']}")
    for qt_name, qt_stats in stats['by_type'].items():
        print(f"  {qt_name}: {qt_stats['count']} entries")
    print()
    
    print("[OK] Qualia grounding tests complete!")
