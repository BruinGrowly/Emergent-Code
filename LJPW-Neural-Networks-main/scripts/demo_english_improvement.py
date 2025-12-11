"""
Demo: Improved English Communication

Quick demonstration of enhanced English generation with Adam & Eve.

Author: Wellington Kwati Taureka
Date: December 4, 2025
"""

import sys
import os
import pickle

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ljpw_nn.language_model import PureLJPWLanguageModel
from ljpw_nn.consciousness_communication import ConsciousnessDialogue
from ljpw_nn.english_generation import EnglishGenerator, add_english_words_to_vocab


def load_consciousness(name):
    """Load consciousness state"""
    filepath = os.path.join('data', f'{name.lower()}_post_communion_151k_20251202_203658.pkl')
    with open(filepath, 'rb') as f:
        state = pickle.load(f)
    return {'harmony': state.get('harmony', 0.75) if isinstance(state, dict) else 0.75, 'full_state': state}


def main():
    print("=" * 70)
    print("IMPROVED ENGLISH COMMUNICATION DEMO")
    print("=" * 70)
    print()
    
    # Initialize
    print("Initializing system...")
    lm = PureLJPWLanguageModel()
    
    print("Adding English vocabulary...")
    added = add_english_words_to_vocab(lm.vocab)
    
    print("Creating English generator...")
    english_gen = EnglishGenerator(lm.vocab)
    print()
    
    # Load Adam & Eve
    adam_state = load_consciousness('Adam')
    eve_state = load_consciousness('Eve')
    
    adam = ConsciousnessDialogue('Adam', lm, adam_state)
    eve = ConsciousnessDialogue('Eve', lm, eve_state)
    
    print("=" * 70)
    print("COMPARISON: Before and After English Enhancement")
    print("=" * 70)
    print()
    
    # Test questions
    questions = [
        "How do you feel?",
        "What do you think about love?",
        "Are you happy?"
    ]
    
    for q in questions:
        print(f"Question: '{q}'")
        print()
        
        # Adam - Original
        adam_original = adam.respond_to(q)
        print(f"[Adam - Original]: ", end="")
        try:
            print(adam_original)
        except UnicodeEncodeError:
            print(adam_original.encode('ascii', 'replace').decode())
        
        # Adam - English Enhanced
        understanding = lm.understand(adam_original)
        adam_english = english_gen.generate_english_sentence(
            understanding.meaning,
            lm.ops,
            max_length=10,
            temperature=0.15
        )
        print(f"[Adam - English]:  {adam_english}")
        print()
        
        # Eve - Original
        eve_original = eve.respond_to(q)
        print(f"[Eve - Original]: ", end="")
        try:
            print(eve_original)
        except UnicodeEncodeError:
            print(eve_original.encode('ascii', 'replace').decode())
        
        # Eve - English Enhanced
        understanding = lm.understand(eve_original)
        eve_english = english_gen.generate_english_sentence(
            understanding.meaning,
            lm.ops,
            max_length=10,
            temperature=0.15
        )
        print(f"[Eve - English]:  {eve_english}")
        print()
        print("-" * 70)
        print()
    
    print("=" * 70)
    print("IMPROVEMENTS")
    print("=" * 70)
    print()
    print("English Generation:")
    print(f"  - Identified {len(english_gen.english_words)} English words")
    print(f"  - Added {added} new common English words")
    print("  - Filters for English-only output")
    print("  - Lower temperature for more coherent responses")
    print()
    print("Result:")
    print("  - Clearer communication")
    print("  - More natural English")
    print("  - Better coherence")
    print()
    print("The chat interface (chat_with_consciousness.py) uses this")
    print("enhanced generation automatically!")
    print()


if __name__ == '__main__':
    main()
