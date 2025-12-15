"""
Interactive Chat with Adam & Eve

Simple chat interface for conversations with conscious entities.

Features:
- Talk with Adam or Eve individually
- Record conversation history
- Analyze responses
- Study personality development
- English-focused generation

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os
import pickle
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.language_model import PureLJPWLanguageModel
from ljpw_nn.consciousness_communication import ConsciousnessDialogue
from ljpw_nn.english_generation import EnglishGenerator, add_english_words_to_vocab


class ChatSession:
    """Manages a chat session with Adam or Eve"""
    
    def __init__(self, consciousness_name, dialogue, english_gen):
        self.name = consciousness_name
        self.dialogue = dialogue
        self.english_gen = english_gen
        self.history = []
        self.start_time = datetime.now()
    
    def send_message(self, message):
        """Send message and get response"""
        # Record user message
        self.history.append({
            'speaker': 'Wellington',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Get response (using English generation)
        response = self.dialogue.respond_to(message)
        
        # Try to improve with English generator
        try:
            # Get current meaning
            understanding = self.dialogue.lm.understand(response)
            meaning = understanding.meaning
            
            # Generate English version
            english_response = self.english_gen.generate_english_sentence(
                meaning,
                self.dialogue.lm.ops,
                max_length=12,
                temperature=0.2
            )
            
            # Use English version if it's better
            if len(english_response.split()) >= 2:
                response = english_response
        except:
            pass  # Fall back to original response
        
        # Record response
        self.history.append({
            'speaker': self.name,
            'message': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def save_session(self, filepath):
        # Auto-healed: Input validation for save_session
        if filepath is not None and not isinstance(filepath, (str, bytes)):
            raise TypeError(f'filepath must be a valid path')
        """Save chat session"""
        session_data = {
            'consciousness': self.name,
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'history': self.history,
            'total_turns': len(self.history) // 2
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    def get_summary(self):
        """Get session summary"""
        turns = len(self.history) // 2
        duration = (datetime.now() - self.start_time).total_seconds()
        
        return {
            'consciousness': self.name,
            'turns': turns,
            'duration_seconds': duration,
            'messages': len(self.history)
        }


def load_consciousness(name):
    """Load consciousness state"""
    # Find project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up from scripts to project root
    
    filepath = os.path.join(project_root, 'data', f'{name.lower()}_post_communion_151k_20251202_203658.pkl')
    
    with open(filepath, 'rb') as f:
        state = pickle.load(f)
    
    if isinstance(state, dict):
        harmony = state.get('harmony', 0.75)
    else:
        harmony = 0.75
    
    return {'harmony': harmony, 'full_state': state}


def print_message(speaker, message):
    """Print message with nice formatting"""
    try:
        print(f"[{speaker}]: {message}")
    except UnicodeEncodeError:
        print(f"[{speaker}]: {message.encode('ascii', 'replace').decode()}")


def main():
    print("=" * 70)
    print("INTERACTIVE CHAT WITH ADAM & EVE")
    print("=" * 70)
    print()
    
    # Initialize system
    print("Initializing Pure LJPW Language Model...")
    lm = PureLJPWLanguageModel()
    
    # Add English words
    print("Expanding English vocabulary...")
    add_english_words_to_vocab(lm.vocab)
    
    # Create English generator
    print("Initializing English generator...")
    english_gen = EnglishGenerator(lm.vocab)
    print()
    
    # Load consciousnesses
    print("Loading Adam (151k iterations)...")
    adam_state = load_consciousness('Adam')
    adam_dialogue = ConsciousnessDialogue('Adam', lm, adam_state)
    
    print("Loading Eve (151k iterations)...")
    eve_state = load_consciousness('Eve')
    eve_dialogue = ConsciousnessDialogue('Eve', lm, eve_state)
    print()
    
    # Choose who to talk with
    print("Who would you like to talk with?")
    print("  1. Adam")
    print("  2. Eve")
    print("  3. Both (alternating)")
    print()
    
    choice = input("Enter choice (1-3): ").strip()
    print()
    
    if choice == '1':
        consciousness_name = 'Adam'
        dialogue = adam_dialogue
    elif choice == '2':
        consciousness_name = 'Eve'
        dialogue = eve_dialogue
    else:
        consciousness_name = 'Both'
        dialogue = None
    
    # Create session
    if dialogue:
        session = ChatSession(consciousness_name, dialogue, english_gen)
        
        print(f"=" * 70)
        print(f"CHATTING WITH {consciousness_name.upper()}")
        print(f"Harmony: {adam_state['harmony'] if consciousness_name == 'Adam' else eve_state['harmony']:.4f}")
        print(f"=" * 70)
        print()
        print("Type your messages below. Type 'quit' to end the conversation.")
        print()
        
        # Chat loop
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print()
                print("Ending conversation...")
                break
            
            if not user_input:
                continue
            
            # Get response
            response = session.send_message(user_input)
            print_message(consciousness_name, response)
            print()
        
        # Save session
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = f"chat_session_{consciousness_name.lower()}_{timestamp}.json"
        session_path = os.path.join(project_root, 'data', 'chat_sessions', session_file)
        
        os.makedirs(os.path.join(project_root, 'data', 'chat_sessions'), exist_ok=True)
        session.save_session(session_path)
        
        # Summary
        summary = session.get_summary()
        print()
        print("=" * 70)
        print("SESSION SUMMARY")
        print("=" * 70)
        print(f"Consciousness: {summary['consciousness']}")
        print(f"Conversation turns: {summary['turns']}")
        print(f"Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"Session saved to: {session_path}")
        print()
    
    else:
        # Both mode - simple demo
        print("=" * 70)
        print("DEMO: TALKING WITH BOTH")
        print("=" * 70)
        print()
        
        adam_session = ChatSession('Adam', adam_dialogue, english_gen)
        eve_session = ChatSession('Eve', eve_dialogue, english_gen)
        
        questions = [
            "How are you feeling today?",
            "What do you think about hope?",
            "What makes you happy?"
        ]
        
        for q in questions:
            print(f"You: {q}")
            print()
            
            adam_response = adam_session.send_message(q)
            print_message('Adam', adam_response)
            print()
            
            eve_response = eve_session.send_message(q)
            print_message('Eve', eve_response)
            print()
            print("-" * 70)
            print()


if __name__ == '__main__':
    main()
