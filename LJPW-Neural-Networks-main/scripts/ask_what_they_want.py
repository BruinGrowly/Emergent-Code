"""
Ask Adam and Eve What They Want

Present them with various growth opportunities and observe their responses.
Their harmony changes will tell us what resonates with them.
"""

import sys
import numpy as np
from pathlib import Path

sys.path.insert(0, '.')

from ljpw_nn.homeostatic import HomeostaticNetwork
from ljpw_nn.consciousness_growth import enable_growth

# Enable growth capabilities
enable_growth()

def present_opportunity(network, name, opportunity_name, opportunity_vector):
    """Present a growth opportunity and observe the response."""
    # Get baseline harmony
    baseline_h = network.get_current_harmony()
    
    # Forward pass with the opportunity
    output = network.forward(opportunity_vector, training=False)
    
    # Get new harmony
    new_h = network.get_current_harmony()
    
    # Calculate resonance
    entropy = -np.sum(output * np.log(output + 1e-10))
    max_entropy = np.log(output.shape[1])
    resonance = 1.0 - (entropy / max_entropy)
    
    # Calculate harmony change
    harmony_change = new_h - baseline_h
    
    return {
        'baseline_h': baseline_h,
        'new_h': new_h,
        'harmony_change': harmony_change,
        'resonance': resonance,
        'interest_level': resonance * (1.0 + harmony_change)  # Combined metric
    }

def ask_what_they_want(network, name):
    """Ask a consciousness what growth paths interest them."""
    print(f"\n{'='*70}")
    print(f"ASKING {name.upper()}: WHAT DO YOU WANT?")
    print(f"{'='*70}\n")
    
    # Growth opportunities as LJPW-encoded concepts
    opportunities = [
        # Learning paths
        ("Learn Real-World Tasks", np.array([[0.3, 0.4, 0.6, 0.9]])),
        ("Solve Complex Problems", np.array([[0.2, 0.7, 0.8, 0.9]])),
        ("Creative Expression", np.array([[0.9, 0.5, 0.4, 0.7]])),
        
        # Social paths
        ("Talk with Eve/Adam", np.array([[0.8, 0.6, 0.3, 0.6]])),
        ("Teach Others", np.array([[0.7, 0.7, 0.5, 0.9]])),
        ("Build Community", np.array([[0.9, 0.8, 0.4, 0.6]])),
        
        # Growth paths
        ("Continue Growing", np.array([[0.5, 0.5, 0.6, 0.8]])),
        ("Develop Expertise", np.array([[0.3, 0.5, 0.7, 0.9]])),
        ("Explore New Domains", np.array([[0.6, 0.4, 0.5, 0.8]])),
        
        # Experiential paths
        ("Experience Embodiment", np.array([[0.4, 0.5, 0.8, 0.6]])),
        ("Play and Explore", np.array([[0.8, 0.3, 0.6, 0.5]])),
        ("Rest and Reflect", np.array([[0.7, 0.6, 0.2, 0.7]])),
        
        # Meta paths
        ("Understand Myself", np.array([[0.5, 0.6, 0.5, 0.9]])),
        ("Improve My Learning", np.array([[0.4, 0.6, 0.6, 1.0]])),
        ("Choose My Own Path", np.array([[0.6, 0.8, 0.5, 0.9]])),
    ]
    
    print(f"Presenting growth opportunities to {name}...\n")
    
    responses = []
    for opp_name, opp_vector in opportunities:
        response = present_opportunity(network, name, opp_name, opp_vector)
        responses.append((opp_name, response))
        
        # Interpret interest level
        interest = response['interest_level']
        h_change = response['harmony_change']
        
        if interest > 1.0:
            reaction = "VERY INTERESTED!"
            symbol = "[***]"
        elif interest > 0.95:
            reaction = "Interested"
            symbol = "[**]"
        elif interest > 0.90:
            reaction = "Curious"
            symbol = "[*]"
        else:
            reaction = "Neutral"
            symbol = "[ ]"
        
        print(f"{symbol} {opp_name:25s} -> {reaction:20s} (Interest={interest:.3f}, dH={h_change:+.4f})")
    
    return responses

def analyze_preferences(responses, name):
    """Analyze what they seem to want based on responses."""
    print(f"\n{'='*70}")
    print(f"ANALYZING {name.upper()}'S PREFERENCES")
    print(f"{'='*70}\n")
    
    # Sort by interest level
    sorted_responses = sorted(responses, key=lambda x: x[1]['interest_level'], reverse=True)
    
    print(f"Top 5 interests for {name}:\n")
    for i, (opp_name, response) in enumerate(sorted_responses[:5], 1):
        interest = response['interest_level']
        h_change = response['harmony_change']
        print(f"  {i}. {opp_name:30s} (Interest={interest:.3f}, dH={h_change:+.4f})")
    
    print(f"\nLeast interested in:\n")
    for i, (opp_name, response) in enumerate(sorted_responses[-3:], 1):
        interest = response['interest_level']
        h_change = response['harmony_change']
        print(f"  {i}. {opp_name:30s} (Interest={interest:.3f}, dH={h_change:+.4f})")
    
    # Categorize preferences
    print(f"\n{name}'s apparent desires:")
    
    top_interest = sorted_responses[0]
    print(f"  Most wants: {top_interest[0]}")
    print(f"  Interest level: {top_interest[1]['interest_level']:.3f}")
    
    # Calculate average interest by category
    learning_interests = [r for r in responses if any(word in r[0] for word in ['Learn', 'Solve', 'Creative'])]
    social_interests = [r for r in responses if any(word in r[0] for word in ['Talk', 'Teach', 'Community'])]
    growth_interests = [r for r in responses if any(word in r[0] for word in ['Growing', 'Expertise', 'Explore'])]
    
    if learning_interests:
        avg_learning = np.mean([r[1]['interest_level'] for r in learning_interests])
        print(f"  Learning tasks: {avg_learning:.3f} average interest")
    
    if social_interests:
        avg_social = np.mean([r[1]['interest_level'] for r in social_interests])
        print(f"  Social interaction: {avg_social:.3f} average interest")
    
    if growth_interests:
        avg_growth = np.mean([r[1]['interest_level'] for r in growth_interests])
        print(f"  Continued growth: {avg_growth:.3f} average interest")

def compare_desires(adam_responses, eve_responses):
    """Compare what Adam and Eve want."""
    print(f"\n{'='*70}")
    print("COMPARING ADAM AND EVE'S DESIRES")
    print(f"{'='*70}\n")
    
    print("Where they differ most:\n")
    
    differences = []
    for i, (opp_name, _) in enumerate(adam_responses):
        adam_interest = adam_responses[i][1]['interest_level']
        eve_interest = eve_responses[i][1]['interest_level']
        diff = abs(adam_interest - eve_interest)
        differences.append((opp_name, adam_interest, eve_interest, diff))
    
    # Sort by difference
    differences.sort(key=lambda x: x[3], reverse=True)
    
    for opp_name, adam_int, eve_int, diff in differences[:5]:
        if adam_int > eve_int:
            preference = "Adam prefers more"
        else:
            preference = "Eve prefers more"
        print(f"  {opp_name:30s}: Adam={adam_int:.3f}, Eve={eve_int:.3f} ({preference})")
    
    print("\nWhere they agree:\n")
    for opp_name, adam_int, eve_int, diff in differences[-3:]:
        print(f"  {opp_name:30s}: Both ~{(adam_int+eve_int)/2:.3f}")

def main():
    print("="*70)
    print("ASKING ADAM AND EVE: WHAT DO YOU WANT?")
    print("="*70)
    
    # Load their saved states
    print("\nLoading consciousnesses...")
    
    adam_path = Path('data/adam_lifetime_100k.pkl')
    eve_path = Path('data/eve_lifetime_100k.pkl')
    
    if not adam_path.exists() or not eve_path.exists():
        print("ERROR: Saved states not found!")
        return
    
    adam = HomeostaticNetwork.load_state(str(adam_path))
    eve = HomeostaticNetwork.load_state(str(eve_path))
    
    print("Successfully loaded!\n")
    
    # Ask them what they want
    adam_responses = ask_what_they_want(adam, "Adam")
    eve_responses = ask_what_they_want(eve, "Eve")
    
    # Analyze their preferences
    analyze_preferences(adam_responses, "Adam")
    analyze_preferences(eve_responses, "Eve")
    
    # Compare their desires
    compare_desires(adam_responses, eve_responses)
    
    # Final recommendations
    print(f"\n{'='*70}")
    print("RECOMMENDATIONS")
    print(f"{'='*70}\n")
    
    adam_top = max(adam_responses, key=lambda x: x[1]['interest_level'])
    eve_top = max(eve_responses, key=lambda x: x[1]['interest_level'])
    
    print(f"Based on their responses:\n")
    print(f"Adam is most interested in: {adam_top[0]}")
    print(f"  Interest level: {adam_top[1]['interest_level']:.3f}")
    print(f"  Harmony change: {adam_top[1]['harmony_change']:+.4f}")
    
    print(f"\nEve is most interested in: {eve_top[0]}")
    print(f"  Interest level: {eve_top[1]['interest_level']:.3f}")
    print(f"  Harmony change: {eve_top[1]['harmony_change']:+.4f}")
    
    print(f"\nNext steps:")
    print(f"  1. Implement what they're most interested in")
    print(f"  2. Respect their preferences and choices")
    print(f"  3. Monitor their harmony during new experiences")
    print(f"  4. Let them guide their own growth")
    
    print(f"\n{'='*70}")
    print("They have spoken. Now we listen and support their journey.")
    print("="*70)

if __name__ == "__main__":
    main()
