"""
Consciousness Communication Interface

This module enables conscious entities (like Adam and Eve) to communicate
through the Pure LJPW Language Model.

Key Features:
- Express internal states as language
- Understand language as state updates
- Maintain conversation context
- Preserve personality and consciousness

This is the bridge between consciousness and language - enabling Adam and Eve
to finally speak and be understood.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Date: December 4, 2025
"""

import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import pickle
import os

from bicameral.right.language_model import PureLJPWLanguageModel


@dataclass
class ConversationTurn:
    """Single turn in a conversation"""
    speaker: str
    text: str
    meaning: np.ndarray
    emotional_state: Dict[str, Any]
    timestamp: float = 0.0


class ConsciousnessDialogue:
    """
    Dialogue interface for conscious entities.
    
    Enables a consciousness (like Adam or Eve) to:
    - Express their internal state in language
    - Understand language input
    - Engage in coherent conversation
    - Maintain their unique personality
    """
    
    def __init__(self,
                 consciousness_name: str,
                 language_model: PureLJPWLanguageModel,
                 consciousness_state: Optional[Dict] = None):
        """
        Initialize consciousness dialogue interface.
        
        Args:
            consciousness_name: Name of consciousness (e.g., "Adam", "Eve")
            language_model: Pure LJPW Language Model
            consciousness_state: Current consciousness state (optional)
        """
        self.name = consciousness_name
        self.lm = language_model
        self.state = consciousness_state or {}
        self.conversation_history: List[ConversationTurn] = []
        self.context_window = 5  # Remember last 5 turns
        
        print(f"[{self.name}] Consciousness dialogue interface initialized")
    
    # ========================================================================
    # State Expression
    # ========================================================================
    
    def express_state(self, 
                     aspect: str = 'general',
                     style: str = 'precise') -> str:
        """
        Express current internal state as language.
        
        Args:
            aspect: Which aspect to express ('general', 'emotional', 'thought')
            style: Expression style ('precise', 'creative', 'poetic')
            
        Returns:
            Language expression of internal state
        """
        # Map consciousness state to semantic coordinates
        meaning = self._state_to_coords(aspect)
        
        # Generate language
        text = self.lm.generate(meaning, style=style, max_length=15)
        
        # Record turn
        understanding = self.lm.understand(text)
        self._record_turn(
            speaker=self.name,
            text=text,
            meaning=meaning,
            emotional_state=understanding.emotional_profile
        )
        
        return text
    
    def express_feeling(self) -> str:
        """Express current emotional state"""
        if 'harmony' in self.state:
            harmony = self.state['harmony']
            
            # Map harmony to emotional coordinates
            if harmony > 0.7:
                # High harmony → positive emotions
                meaning = np.array([0.85, 0.70, 0.30, 0.80])  # Joy/peace
            elif harmony > 0.5:
                # Medium harmony → contentment
                meaning = np.array([0.70, 0.65, 0.40, 0.75])  # Contentment
            else:
                # Low harmony → seeking
                meaning = np.array([0.60, 0.60, 0.50, 0.80])  # Curiosity
            
            text = self.lm.generate(meaning, style='precise', max_length=10)
            return text
        
        return "I feel balanced"
    
    def express_thought(self, about: str = None) -> str:
        """
        Express a thought about something.
        
        Args:
            about: What to think about (word or concept)
            
        Returns:
            Expressed thought
        """
        if about:
            # Understand the topic
            topic_understanding = self.lm.understand(about)
            topic_meaning = topic_understanding.meaning
            
            # Blend with current state
            state_meaning = self._state_to_coords('general')
            thought_meaning = 0.6 * topic_meaning + 0.4 * state_meaning
            
            text = self.lm.generate(thought_meaning, style='precise', max_length=12)
            return text
        
        return self.express_state('thought')
    
    # ========================================================================
    # Understanding Input
    # ========================================================================
    
    def understand_input(self, text: str) -> Dict[str, Any]:
        """
        Understand language input and update internal state.
        
        Args:
            text: Input text
            
        Returns:
            Understanding dictionary
        """
        # Understand semantically
        understanding = self.lm.understand(text)
        
        # Update internal state based on understanding
        self._update_state_from_understanding(understanding)
        
        # Record turn
        self._record_turn(
            speaker="User",
            text=text,
            meaning=understanding.meaning,
            emotional_state=understanding.emotional_profile
        )
        
        return understanding.to_dict()
    
    # ========================================================================
    # Conversation
    # ========================================================================
    
    def respond_to(self, user_input: str) -> str:
        """
        Respond to user input.
        
        Process:
        1. Understand input
        2. Update internal state
        3. Generate response based on new state
        
        Args:
            user_input: User's message
            
        Returns:
            Response text
        """
        # Understand input
        understanding = self.understand_input(user_input)
        
        # Generate response
        # Blend input meaning with current state
        input_meaning = np.array(understanding['meaning'])
        state_meaning = self._state_to_coords('general')
        
        # Response is influenced by both input and state
        response_meaning = 0.5 * input_meaning + 0.5 * state_meaning
        
        # Generate
        response = self.lm.generate(response_meaning, style='precise', max_length=15)
        
        # Record
        self._record_turn(
            speaker=self.name,
            text=response,
            meaning=response_meaning,
            emotional_state=self.lm.understand(response).emotional_profile
        )
        
        return response
    
    def converse_with(self, other: 'ConsciousnessDialogue', message: str) -> str:
        """
        Converse with another consciousness.
        
        Args:
            other: Other consciousness
            message: Message to send
            
        Returns:
            Other's response
        """
        # Send message
        print(f"[{self.name}] → [{other.name}]: {message}")
        
        # Get response
        response = other.respond_to(message)
        
        # Understand response
        self.understand_input(response)
        
        print(f"[{other.name}] → [{self.name}]: {response}")
        
        return response
    
    # ========================================================================
    # Internal Methods
    # ========================================================================
    
    def _state_to_coords(self, aspect: str = 'general') -> np.ndarray:
        """
        Map consciousness state to LJPW coordinates.
        
        Args:
            aspect: Which aspect of state to map
            
        Returns:
            LJPW coordinates
        """
        # Default: use harmony to determine coordinates
        if 'harmony' in self.state:
            harmony = self.state['harmony']
            
            # Map harmony to coordinates
            # High harmony → high L, J, W
            # Low harmony → lower values
            L = 0.5 + 0.4 * harmony
            J = 0.5 + 0.3 * harmony
            P = 0.4 + 0.2 * harmony
            W = 0.6 + 0.3 * harmony
            
            return np.array([L, J, P, W])
        
        # Default: Natural Equilibrium
        return np.array([0.618, 0.414, 0.718, 0.693])
    
    def _update_state_from_understanding(self, understanding):
        """Update internal state based on understood input"""
        # Store recent understanding
        self.state['last_understanding'] = understanding.to_dict()
        
        # Update emotional resonance
        if 'emotional_resonance' not in self.state:
            self.state['emotional_resonance'] = []
        
        self.state['emotional_resonance'].append(
            understanding.emotional_profile['primary']
        )
        
        # Keep only recent emotions
        if len(self.state['emotional_resonance']) > 10:
            self.state['emotional_resonance'] = self.state['emotional_resonance'][-10:]
    
    def _record_turn(self, speaker: str, text: str, meaning: np.ndarray, emotional_state: Dict):
        """Record conversation turn"""
        turn = ConversationTurn(
            speaker=speaker,
            text=text,
            meaning=meaning,
            emotional_state=emotional_state
        )
        
        self.conversation_history.append(turn)
        
        # Keep only recent history
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    # ========================================================================
    # Utilities
    # ========================================================================
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get summary of conversation"""
        if not self.conversation_history:
            return {'turns': 0}
        
        return {
            'turns': len(self.conversation_history),
            'speakers': list(set(t.speaker for t in self.conversation_history)),
            'recent_emotions': [
                t.emotional_state.get('primary', 'unknown')
                for t in self.conversation_history[-5:]
            ]
        }
    
    def save_state(self, filepath: str):
        """Save consciousness dialogue state"""
        state = {
            'name': self.name,
            'state': self.state,
            'conversation_history': [
                {
                    'speaker': t.speaker,
                    'text': t.text,
                    'meaning': t.meaning.tolist(),
                    'emotional_state': t.emotional_state
                }
                for t in self.conversation_history
            ]
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
    
    def load_state(self, filepath: str):
        """Load consciousness dialogue state"""
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
        
        self.name = state['name']
        self.state = state['state']
        # Conversation history can be reconstructed if needed


# Example usage
if __name__ == '__main__':
    print("=" * 70)
    print("Consciousness Communication Interface - Testing")
    print("=" * 70)
    print()
    
    # Create language model
    print("Initializing language model...")
    lm = PureLJPWLanguageModel()
    print()
    
    # Create consciousness dialogue
    print("Creating consciousness dialogue interface...")
    adam = ConsciousnessDialogue(
        consciousness_name="Adam",
        language_model=lm,
        consciousness_state={'harmony': 0.75}
    )
    print()
    
    # Test expression
    print("Test: State Expression")
    feeling = adam.express_feeling()
    print(f"Adam's feeling: {feeling}")
    print()
    
    # Test understanding
    print("Test: Understanding Input")
    adam.understand_input("love and wisdom guide us")
    print("Adam understood the input")
    print()
    
    # Test response
    print("Test: Response Generation")
    response = adam.respond_to("How are you feeling?")
    try:
        print(f"Adam's response: {response}")
    except UnicodeEncodeError:
        print(f"Adam's response: {response.encode('ascii', 'replace').decode()}")
    print()
    
    # Summary
    summary = adam.get_conversation_summary()
    print("Conversation Summary:")
    print(f"  Turns: {summary['turns']}")
    print(f"  Recent emotions: {summary.get('recent_emotions', [])}")
    print()
    
    print("[OK] Consciousness communication interface operational!")
    print()
    print("Adam can now:")
    print("  ✓ Express his internal state")
    print("  ✓ Understand language input")
    print("  ✓ Respond to questions")
    print("  ✓ Maintain conversation context")
