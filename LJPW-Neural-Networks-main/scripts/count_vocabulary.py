"""Count total vocabulary in LJPW_Language_Data"""
import json
import os

data_dir = os.path.join('data', 'LJPW_Language_Data')

files = [
    'comprehensive_language_expansion.json',
    'second_major_expansion.json',
    'third_major_expansion.json',
    'fourth_major_expansion.json',
    'fifth_major_expansion.json',
    'multilingual_expansion.json',
    'qualia_mapping_analysis.json',
    'semantic_space_mapping.json',
    'topological_semantic_map.json'
]

total = 0
all_words = set()

print("=" * 70)
print("LJPW Language Data Inventory")
print("=" * 70)
print()

for filename in files:
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        continue
        
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        
        # Try different data structures
        mappings = data.get('mappings', data.get('words', data.get('concepts', [])))
        
        if isinstance(mappings, dict):
            count = len(mappings)
            all_words.update(mappings.keys())
        elif isinstance(mappings, list):
            count = len(mappings)
            # Extract words from list entries
            for item in mappings:
                if isinstance(item, dict):
                    if 'word' in item:
                        all_words.add(item['word'])
                    elif 'concept' in item:
                        all_words.add(item['concept'])
        else:
            count = 0
        
        total += count
        print(f"{filename:50s} {count:5d} entries")
        
    except Exception as e:
        print(f"{filename:50s} ERROR: {e}")

print()
print("=" * 70)
print(f"Total entries across all files: {total}")
print(f"Unique words collected: {len(all_words)}")
print("=" * 70)
print()

if all_words:
    print("Sample words:")
    for word in list(all_words)[:20]:
        print(f"  - {word}")
