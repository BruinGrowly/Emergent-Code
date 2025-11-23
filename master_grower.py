"""
SPDX-License-Identifier: MIT
Master Grower - Growing Code from a Real-World Blueprint (v5 - Final)

This script uses a 'minimum_profile' constraint and a robust assembly
process to intelligently construct a Python script based on a high-level
semantic blueprint.
"""

import math
import time
import sys
import os
import json
from typing import Dict, List, Optional, Tuple, Any

# Add the 'harmonizer_repo' directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
# Support both directory names for flexibility
harmonizer_path = os.path.join(project_root, 'Python-Code-Harmonizer')
if not os.path.exists(harmonizer_path):
    harmonizer_path = os.path.join(project_root, 'Python-Code-Harmonizer-main')

if harmonizer_path not in sys.path:
    sys.path.insert(0, harmonizer_path)

try:
    from harmonizer.main import PythonCodeHarmonizer
    
    # Subclass to add string analysis capability to the real Harmonizer
    class StringHarmonizer(PythonCodeHarmonizer):
        def analyze_file_content(self, content: str) -> dict:
            # Use internal methods to analyze string content directly
            tree = self._parse_code_to_ast(content, "string")
            if tree is None: return {}
            return self._analyze_all_functions(tree)
            
    print("[OK] Real Harmonizer loaded successfully.")
except ImportError:
    print("Warning: Harmonizer not found. Using Mock Harmonizer.")
    from mock_harmonizer import PythonCodeHarmonizer as StringHarmonizer

from calculator_components import SOURCES

# ==============================================================================
#  Gene Pool Profile Loading
# ==============================================================================

GENE_POOL_DIR = os.path.join(project_root, 'master_gene_pool')

def load_profile_from_gene_pool(file_path_suffix: str) -> Dict[str, float]:
    """
    Scans the gene pool analysis files to find the profile for a specific file.
    """
    analysis_files = [
        os.path.join(GENE_POOL_DIR, 'django_analysis.json'),
        os.path.join(GENE_POOL_DIR, 'lodash/lodash_analysis.json'),
        os.path.join(GENE_POOL_DIR, 'requests_analysis.json'),
        os.path.join(GENE_POOL_DIR, 'black_analysis.json'),
    ]
    
    target_path_normalized = file_path_suffix.replace('/', os.sep).replace('\\', os.sep)

    for fpath in analysis_files:
        if not os.path.exists(fpath):
            continue
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
                for entry in data:
                    # Handle different formats
                    entry_file = entry.get('file') or entry.get('file_path')
                    if not entry_file: continue
                    
                    entry_file_normalized = entry_file.replace('/', os.sep).replace('\\', os.sep)
                    
                    if entry_file_normalized.endswith(target_path_normalized):
                        # Found it! Extract profile.
                        if 'coords' in entry:
                            return {'L': entry['coords'][0], 'J': entry['coords'][1], 'P': entry['coords'][2], 'W': entry['coords'][3]}
                        else:
                            return {'L': entry.get('L', 0), 'J': entry.get('J', 0), 'P': entry.get('P', 0), 'W': entry.get('W', 0)}
        except Exception as e:
            print(f"Warning: Error reading {fpath}: {e}")
            
    print(f"Warning: Could not find profile for {file_path_suffix} in gene pool.")
    return {'L': 0, 'J': 0, 'P': 0, 'W': 0} # Default fallback

# ==============================================================================
# The Gene Hunter v1 (Dynamic Archetype Discovery)
# ==============================================================================

class GeneHunter:
    def __init__(self):
        self.gene_pool_data = {}
        self._load_gene_pool()

    def _load_gene_pool(self):
        # Load Django Analysis
        try:
            with open('master_gene_pool/django_analysis.json', 'r') as f:
                django_data = json.load(f)
                self.gene_pool_data['django'] = self._normalize_django(django_data)
        except FileNotFoundError:
            print("[WARNING] Django gene pool not found.")

        # Load Lodash Analysis
        try:
            with open('master_gene_pool/lodash/lodash_analysis.json', 'r') as f:
                lodash_data = json.load(f)
                self.gene_pool_data['lodash'] = self._normalize_lodash(lodash_data)
        except FileNotFoundError:
            print("[WARNING] Lodash gene pool not found.")

        # Load Requests Analysis (Mock)
        try:
            with open('master_gene_pool/requests_analysis.json', 'r') as f:
                requests_data = json.load(f)
                self.gene_pool_data['requests'] = self._normalize_django(requests_data) # Re-use Django normalizer as format is same
        except FileNotFoundError:
            print("[WARNING] Requests gene pool not found.")

        # Load Black Analysis (Mock)
        try:
            with open('master_gene_pool/black_analysis.json', 'r') as f:
                black_data = json.load(f)
                self.gene_pool_data['black'] = self._normalize_django(black_data) # Re-use Django normalizer
        except FileNotFoundError:
            print("[WARNING] Black gene pool not found.")

    def _normalize_django(self, data):
        normalized = []
        for entry in data:
            # Django uses 'coords': [L, J, P, W]
            coords = entry.get('coords', [0, 0, 0, 0])
            normalized.append({
                'file': entry['file'],
                'profile': {'L': coords[0], 'J': coords[1], 'P': coords[2], 'W': coords[3]}
            })
        return normalized

    def _normalize_lodash(self, data):
        normalized = []
        for entry in data:
            # Lodash uses explicit keys
            normalized.append({
                'file': entry.get('file_path', 'unknown'),
                'profile': {
                    'L': entry.get('L', 0),
                    'J': entry.get('J', 0),
                    'P': entry.get('P', 0),
                    'W': entry.get('W', 0)
                }
            })
        return normalized

    def find_archetype(self, query):
        source = query.get('source')
        criteria = query.get('criteria')
        
        if source not in self.gene_pool_data:
            return None

        candidates = self.gene_pool_data[source]
        
        if criteria == 'max_power':
            best = max(candidates, key=lambda x: x['profile']['P'])
        elif criteria == 'max_justice':
            best = max(candidates, key=lambda x: x['profile']['J'])
        elif criteria == 'max_wisdom':
            best = max(candidates, key=lambda x: x['profile']['W'])
        elif criteria == 'max_love':
            best = max(candidates, key=lambda x: x['profile']['L'])
        else:
            return None
            
        return best['file']


def load_dna_from_file(filename: str) -> Dict[str, Any]:
    with open(filename, 'r') as f:
        dna = json.load(f)
    return dna

# ==============================================================================
# The Stability Validator v1 (Structural Enforcement)
# ==============================================================================

class StabilityValidator:
    def validate(self, component_name, source_code):
        issues = []
        
        # Check for docstrings (Wisdom)
        if '"""' not in source_code and "'''" not in source_code:
            issues.append("Missing docstring")
            
        # Check for error handling (Justice) - simplistic check
        if "try:" not in source_code and "raise " not in source_code:
            # Only strictly enforce for 'robust' components
            if "robust" in component_name:
                issues.append("Missing error handling in robust component")

        if issues:
            print(f"      [STABILITY FAIL] {component_name}: {', '.join(issues)}")
            return False
        
        print(f"      [STABILITY PASS] {component_name} is structurally sound.")
        return True

# ==============================================================================
# The Component Composer v2 (Fractal Growth with AST-based parsing)
# ==============================================================================

class ComponentComposer:
    def compose(self, name: str, recipe: Dict[str, str], sources: Dict[str, str]) -> Optional[str]:
        """
        Compose a new function from atomic components using AST parsing.
        
        Args:
            name: Name of the composed function
            recipe: Dictionary with 'core', optional 'guard', 'observer'
            sources: Dictionary mapping component names to source code
            
        Returns:
            Generated source code or None if composition fails
        """
        import ast
        
        core_name = recipe['core']
        guard_name = recipe.get('guard')
        observer_name = recipe.get('observer')
        
        core_source = sources[core_name]
        
        # Parse the core function to extract its operation
        try:
            tree = ast.parse(core_source)
            func_def = None
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_def = node
                    break
            
            if not func_def:
                return None
            
            # Extract the return expression
            operation = None
            for stmt in func_def.body:
                if isinstance(stmt, ast.Return) and stmt.value:
                    operation = ast.unparse(stmt.value)
                    break
            
            if not operation:
                return None
                
        except (SyntaxError, ValueError):
            # Fallback to simple extraction if AST parsing fails
            import re
            body_match = re.search(r"return\s+(.+)", core_source)
            if not body_match:
                return None
            operation = body_match.group(1).strip()
        
        # Generate new function
        code = f"def {name}(a, b):\n"
        code += f'    """\n    Fractally composed function: {name}\n'
        code += f'    Core: {core_name} (Power)\n'
        if guard_name: code += f'    Guard: {guard_name} (Justice)\n'
        if observer_name: code += f'    Observer: {observer_name} (Love)\n'
        code += f'    """\n'
        
        # 1. Justice Layer (Guard)
        if guard_name:
            code += f"    {guard_name}(a, b)\n"
            
        # 2. Power Layer (Core)
        code += f"    result = {operation}\n"
        
        # 3. Love Layer (Observer)
        if observer_name:
            code += f"    {observer_name}('{name}', a, b, result)\n"
            
        code += "    return result\n"
        return code

class MasterGrower:
    def __init__(self, dna_file):
        self.dna = load_dna_from_file(dna_file)
        self.archetype_queries = self.dna.get('archetype_queries', {})
        self.gene_hunter = GeneHunter()
        self.validator = StabilityValidator()
        self.composer = ComponentComposer()
        
        self.harmonizer = StringHarmonizer(quiet=True)
        self.component_context = self._analyze_gene_pool()

    # ... (rest of methods) ...

    def grow(self):
        print(f"\n[GROWTH] Starting growth process from DNA: {self.dna['filename']}...")
        
        selected_components = {}
        missing_components = []
        composed_sources = {}

        for comp_name, details in self.dna['required_components'].items():
            print(f"\n[SELECTION] Selecting optimal '{comp_name}'...")
            
            # FRACTAL COMPOSITION PATH
            if 'composition' in details:
                print(f"    - Detected Fractal Composition recipe.")
                recipe = details['composition']
                # Verify atomic parts exist
                sources = SOURCES['functions']
                if recipe['core'] in sources:
                    print(f"    - Composing '{comp_name}' from atoms: {recipe}")
                    new_source = self.composer.compose(comp_name, recipe, sources)
                    if new_source:
                        composed_sources[comp_name] = new_source
                        selected_components[comp_name] = comp_name # Self-reference
                        print(f"      [SUCCESS] Fractally grown '{comp_name}'.")
                        continue
                
                print(f"      [FAILURE] Could not compose '{comp_name}'. Missing atoms.")
                missing_components.append(comp_name)
                continue

            # STANDARD SELECTION PATH
            component_pool = self.component_context['functions']
            if comp_name == 'main':
                component_pool = self.component_context['main_blocks']

            best_name, distance = self._find_best_match(details, component_pool)
            
            if best_name:
                print(f"    - Best semantic match: '{best_name}' (Distance: {distance:.2f})")
                selected_components[comp_name] = best_name
            else:
                print(f"    [GAP] Could not find a suitable component for '{comp_name}'.")
                missing_components.append(comp_name)

        if missing_components:
            print(f"\n[ADAPTATION REQUIRED] The following components are missing or do not meet quality standards:")
            for gap in missing_components:
                print(f"  - {gap}: Needs implementation matching archetype '{self.dna['required_components'][gap].get('archetype', 'composed')}'")
            print("\n[HALT] Growth halted due to genetic gaps. Please adapt components to match DNA and re-run.")
            return

        filename = self.dna["filename"]
        print(f"\n[ASSEMBLY] Assembling final organism in '{filename}'...")
        
        with open(filename, 'w') as f:
            f.write(self.dna.get("docstring", '"""Grown Calculator"""') + "\n\n")
            f.write("import argparse\nimport sys\n\n")
            
            f.write("# --- Atomic Components (Fractal Building Blocks) ---\n")
            for name in ['validate_numeric', 'log_operation']:
                if name in SOURCES['functions']:
                    f.write(SOURCES['functions'][name] + "\n")

            f.write("# --- Component Gene Pool (Semantically Selected) ---\n")
            for comp_name, selected_name in selected_components.items():
                if comp_name == 'main': continue
                
                if comp_name in composed_sources:
                    f.write(f"\n# Fractally Grown: {comp_name}\n")
                    f.write(composed_sources[comp_name] + "\n")
                else:
                    f.write(SOURCES['functions'][selected_name] + "\n\n")
            
            # Write selected main block
            main_name = selected_components['main']
            main_source = SOURCES['main_blocks'][main_name]
            
            if "def main_simple():" in main_source:
                main_source_renamed = main_source.replace("def main_simple():", "def main():", 1)
            elif "def main_robust():" in main_source:
                main_source_renamed = main_source.replace("def main_robust():", "def main():", 1)
            else:
                main_source_renamed = main_source # Fallback

            # NEURAL WIRING: Connect main brain to selected limbs
            import re
            ops_pattern = r"ops\s*=\s*\{[^}]+\}"
            
            # Construct the correct ops dictionary string
            new_ops = "ops = {"
            # Handle dynamic keys based on what was selected/composed
            for key in selected_components:
                if key == 'main': continue
                
                # Intelligent Wiring: Map complex names to standard slots
                wired_key = key
                if key == 'secure_add': wired_key = 'add'
                elif 'add' in key: wired_key = 'add'
                elif 'subtract' in key: wired_key = 'subtract'
                elif 'multiply' in key: wired_key = 'multiply'
                elif 'divide' in key: wired_key = 'divide'
                
                new_ops += f"'{wired_key}': {selected_components[key]}, "
            
            new_ops += "}"
            
            main_source_wired = re.sub(ops_pattern, new_ops, main_source_renamed)

            f.write("# --- Semantically Selected Main Block (guided by Master Gene Pool Archetypes) ---\n")
            f.write(main_source_wired)
            f.write("\nif __name__ == '__main__':\n    main()\n")

        print(f"\n[COMPLETE] Growth complete!")

    def _analyze_gene_pool(self):
        print("[GENE POOL] Analyzing available components with Harmonizer...")
        context = {'functions': {}, 'main_blocks': {}}
        
        # Analyze functions
        for name, source in SOURCES['functions'].items():
            print(f"  - Analyzing function '{name}'...")
            report = self.harmonizer.analyze_file_content(source)
            if report:
                func_name = list(report.keys())[0]
                coords = report[func_name]['ice_result']['ice_components']['intent'].coordinates
                context['functions'][name] = {'L': coords.love, 'J': coords.justice, 'P': coords.power, 'W': coords.wisdom}
        
        # Analyze main blocks
        for name, source in SOURCES['main_blocks'].items():
            print(f"  - Analyzing main block '{name}'...")
            report = self.harmonizer.analyze_file_content(source)
            if report:
                func_name = list(report.keys())[0]
                coords = report[func_name]['ice_result']['ice_components']['intent'].coordinates
                context['main_blocks'][name] = {'L': coords.love, 'J': coords.justice, 'P': coords.power, 'W': coords.wisdom}
                
        return context

    def _find_best_match(self, details, component_pool):
        # DYNAMICALLY RESOLVE ARCHETYPE
        archetype_key = details['archetype']
        query = self.archetype_queries.get(archetype_key)
        
        if query:
            print(f"    - Resolving dynamic archetype query for '{archetype_key}'...")
            archetype_file = self.gene_hunter.find_archetype(query)
            if not archetype_file:
                print(f"      [WARNING] Could not resolve query for '{archetype_key}'. Using fallback.")
                return None, float('inf')
        else:
            # Fallback for legacy DNA
            archetype_file = archetype_key

        print(f"    - Loading target profile from archetype: {archetype_file}")
        target_profile = load_profile_from_gene_pool(archetype_file)
        print(f"      -> Target Profile: L={target_profile['L']:.3f}, J={target_profile['J']:.3f}, P={target_profile['P']:.3f}, W={target_profile['W']:.3f}")

        candidate_names = details['candidates']
        minimum_profile = details.get('minimum_profile', {})

        qualified_candidates = []
        print("    - Filtering candidates by minimum profile and stability...")
        for name in candidate_names:
            candidate_profile = component_pool.get(name)
            if not candidate_profile: continue
            
            # 1. Profile Check
            is_qualified = all(candidate_profile.get(dim, 0) >= min_score for dim, min_score in minimum_profile.items())
            
            if not is_qualified:
                print(f"      - Discarding '{name}': Fails minimum profile.")
                continue

            # 2. Stability Check (Dynamic Stability)
            source_code = SOURCES['functions'].get(name) or SOURCES['main_blocks'].get(name)
            if not self.validator.validate(name, source_code):
                print(f"      - Discarding '{name}': Fails stability validation.")
                continue

            print(f"      - Qualifying '{name}': Meets all standards.")
            qualified_candidates.append(name)
        
        if not qualified_candidates:
            return None, float('inf')

        best_match_name = None
        min_distance = float('inf')
        for name in qualified_candidates:
            candidate_profile = component_pool.get(name)
            dist = math.sqrt(sum([(target_profile[dim] - candidate_profile[dim])**2 for dim in ['L', 'J', 'P', 'W']]))
            if dist < min_distance:
                min_distance = dist
                best_match_name = name
        
        return best_match_name, min_distance


if __name__ == '__main__':
    dna_file = 'calculator_dna.json'
    if len(sys.argv) > 1:
        dna_file = sys.argv[1]
    
    print(f"Growing organism from DNA: {dna_file}")
    grower = MasterGrower(dna_file)
    grower.grow()
