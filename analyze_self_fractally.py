#!/usr/bin/env python3
"""
Fractal Self-Analysis: Applying LJPW Semantic Capabilities to This Repository

This script analyzes the repository that created it, using the very concepts
it contains. A meta-exercise in semantic self-reflection.

We run 5 iterations, each time going deeper and discovering emergent patterns.
"""

import os
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# Import our own semantic capabilities
from ljpw_semantic_capabilities import (
    LJPWVector, SemanticEntity, SemanticDrift,
    Archetype, FractalScale, FractalProfile,
    harmony_index, semantic_mass, semantic_density, semantic_influence,
    semantic_clarity, calculate_drift, drift_interpretation,
    match_archetype, describe_archetype,
    semantic_gravity, semantic_friction, semantic_resonance,
    all_secondary_metrics, aggregate_profiles, build_fractal_tree,
    full_semantic_diagnostic, ANCHOR_POINT, NATURAL_EQUILIBRIUM
)


# =============================================================================
# PHASE 1: MAP THE REPOSITORY STRUCTURE
# =============================================================================

def estimate_ljpw_from_file(filepath: str) -> LJPWVector:
    """
    Estimate LJPW coordinates for a file based on its characteristics.
    
    This is a heuristic based on file patterns - in production you'd use
    the actual LJPW analyzer.
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except:
        return LJPWVector(L=0.3, J=0.3, P=0.3, W=0.3)
    
    total_lines = len(lines)
    if total_lines == 0:
        return LJPWVector(L=0.3, J=0.3, P=0.3, W=0.3)
    
    # Estimate Love (connectivity, documentation, openness)
    docstrings = content.count('"""') + content.count("'''")
    comments = sum(1 for line in lines if line.strip().startswith('#'))
    imports = sum(1 for line in lines if 'import' in line)
    love = min(1.0, 0.3 + (docstrings * 0.05) + (comments / total_lines) + (imports * 0.02))
    
    # Estimate Justice (validation, error handling, structure)
    try_blocks = content.count('try:')
    asserts = content.count('assert ')
    validates = content.lower().count('valid')
    raises = content.count('raise ')
    justice = min(1.0, 0.2 + (try_blocks * 0.08) + (asserts * 0.03) + (validates * 0.05) + (raises * 0.04))
    
    # Estimate Power (functionality, computation)
    functions = content.count('def ')
    classes = content.count('class ')
    returns = content.count('return ')
    power = min(1.0, 0.3 + (functions * 0.03) + (classes * 0.05) + (returns * 0.02))
    
    # Estimate Wisdom (logging, metrics, self-awareness)
    logs = content.lower().count('log')
    prints = content.count('print(')
    metrics = content.lower().count('metric')
    wisdom = min(1.0, 0.2 + (logs * 0.04) + (prints * 0.02) + (metrics * 0.05))
    
    return LJPWVector(L=love, J=justice, P=power, W=wisdom)


def count_concepts(filepath: str) -> int:
    """Count the number of concepts (functions, classes) in a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return content.count('def ') + content.count('class ') + 1
    except:
        return 1


def scan_repository(root_path: str) -> List[SemanticEntity]:
    """Scan the repository and create semantic entities for each Python file."""
    entities = []
    
    for dirpath, dirnames, filenames in os.walk(root_path):
        # Skip hidden and generated directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.') and d != '__pycache__' and d != 'generated']
        
        for filename in filenames:
            if filename.endswith('.py') and not filename.startswith('__'):
                filepath = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(filepath, root_path)
                
                coords = estimate_ljpw_from_file(filepath)
                concepts = count_concepts(filepath)
                
                # Clarity based on file focus (shorter name = more focused)
                clarity = min(1.0, 0.5 + (1.0 / (1 + len(filename) / 20)))
                
                entities.append(SemanticEntity(
                    name=rel_path,
                    coordinates=coords,
                    concept_count=concepts,
                    semantic_clarity=clarity,
                    metadata={'full_path': filepath}
                ))
    
    return entities


# =============================================================================
# PHASE 2: BUILD FRACTAL STRUCTURE
# =============================================================================

def group_by_directory(entities: List[SemanticEntity]) -> Dict[str, List[str]]:
    """Group entities by their parent directory."""
    groups = defaultdict(list)
    for entity in entities:
        parts = entity.name.split(os.sep)
        if len(parts) > 1:
            group = parts[0]
        else:
            group = '_root'
        groups[group].append(entity.name)
    return dict(groups)


# =============================================================================
# PHASE 3: ANALYSIS FUNCTIONS
# =============================================================================

def find_gravitational_centers(entities: List[SemanticEntity], top_n: int = 5) -> List[Tuple[str, float]]:
    """Find entities with highest gravitational pull."""
    masses = [(e.name, semantic_mass(e)) for e in entities]
    return sorted(masses, key=lambda x: x[1], reverse=True)[:top_n]


def find_friction_pairs(entities: List[SemanticEntity], top_n: int = 5) -> List[Tuple[str, str, float]]:
    """Find entity pairs with highest friction."""
    pairs = []
    for i, e1 in enumerate(entities):
        for e2 in entities[i+1:]:
            friction = semantic_friction(e1, e2)
            pairs.append((e1.name, e2.name, friction))
    return sorted(pairs, key=lambda x: x[2], reverse=True)[:top_n]


def find_resonant_pairs(entities: List[SemanticEntity], top_n: int = 5) -> List[Tuple[str, str, float]]:
    """Find entity pairs with highest resonance."""
    pairs = []
    for i, e1 in enumerate(entities):
        for e2 in entities[i+1:]:
            res = semantic_resonance(e1, e2)
            pairs.append((e1.name, e2.name, res))
    return sorted(pairs, key=lambda x: x[2], reverse=True)[:top_n]


def analyze_archetypes(entities: List[SemanticEntity]) -> Dict[str, List[str]]:
    """Group entities by their matched archetype."""
    archetype_groups = defaultdict(list)
    for entity in entities:
        archetype, confidence = match_archetype(entity.coordinates)
        if confidence > 0.5:
            archetype_groups[archetype.value].append(entity.name)
    return dict(archetype_groups)


def calculate_system_health(entities: List[SemanticEntity]) -> Dict[str, float]:
    """Calculate overall system health metrics."""
    if not entities:
        return {}
    
    # Aggregate coordinates
    avg_L = sum(e.coordinates.L for e in entities) / len(entities)
    avg_J = sum(e.coordinates.J for e in entities) / len(entities)
    avg_P = sum(e.coordinates.P for e in entities) / len(entities)
    avg_W = sum(e.coordinates.W for e in entities) / len(entities)
    
    system_coords = LJPWVector(L=avg_L, J=avg_J, P=avg_P, W=avg_W)
    
    return {
        'system_harmony': harmony_index(system_coords),
        'system_L': avg_L,
        'system_J': avg_J,
        'system_P': avg_P,
        'system_W': avg_W,
        'total_mass': sum(semantic_mass(e) for e in entities),
        'avg_density': sum(semantic_density(e) for e in entities) / len(entities),
        'entity_count': len(entities),
        **all_secondary_metrics(system_coords)
    }


# =============================================================================
# PHASE 4: ITERATION AND EMERGENCE
# =============================================================================

def run_iteration(entities: List[SemanticEntity], iteration: int) -> Dict:
    """Run a single analysis iteration and return insights."""
    
    print(f"\n{'='*70}")
    print(f"ITERATION {iteration}: {'ATOMIC' if iteration == 1 else 'EMERGENT'} ANALYSIS")
    print(f"{'='*70}")
    
    results = {
        'iteration': iteration,
        'insights': [],
        'metrics': {},
        'emergent_patterns': []
    }
    
    # System Health
    health = calculate_system_health(entities)
    results['metrics'] = health
    
    print(f"\n📊 SYSTEM HEALTH (Iteration {iteration})")
    print(f"   Harmony Index: {health['system_harmony']:.4f}")
    print(f"   LJPW Vector: L={health['system_L']:.3f}, J={health['system_J']:.3f}, P={health['system_P']:.3f}, W={health['system_W']:.3f}")
    print(f"   Total Semantic Mass: {health['total_mass']:.2f}")
    print(f"   Average Density: {health['avg_density']:.2f}")
    print(f"   Entity Count: {health['entity_count']}")
    
    # Gravitational Centers
    print(f"\n🌟 GRAVITATIONAL CENTERS (Highest Mass)")
    centers = find_gravitational_centers(entities)
    for name, mass in centers:
        print(f"   {mass:8.2f} | {name}")
        results['insights'].append(f"High mass entity: {name} ({mass:.2f})")
    
    # Archetype Distribution
    print(f"\n🎭 ARCHETYPE DISTRIBUTION")
    archetypes = analyze_archetypes(entities)
    for archetype, members in sorted(archetypes.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {archetype:20s}: {len(members)} entities")
        if len(members) <= 3:
            for m in members:
                print(f"      - {m}")
    
    # Friction Analysis (potential integration problems)
    print(f"\n⚡ HIGHEST FRICTION PAIRS (Integration Difficulty)")
    friction_pairs = find_friction_pairs(entities)
    for e1, e2, friction in friction_pairs:
        print(f"   {friction:.3f} | {os.path.basename(e1)} ↔ {os.path.basename(e2)}")
        if friction > 0.4:
            results['emergent_patterns'].append(f"High friction: {e1} vs {e2}")
    
    # Resonance Analysis (natural collaborations)
    print(f"\n🎵 HIGHEST RESONANCE PAIRS (Natural Collaboration)")
    resonant_pairs = find_resonant_pairs(entities)
    for e1, e2, resonance in resonant_pairs:
        print(f"   {resonance:.3f} | {os.path.basename(e1)} ↔ {os.path.basename(e2)}")
        if resonance > 0.8:
            results['emergent_patterns'].append(f"High resonance: {e1} + {e2}")
    
    # Secondary Metrics
    print(f"\n📈 DERIVED METRICS")
    print(f"   Secure Connectivity (L+J): {health['secure_connectivity']:.3f}")
    print(f"   Service Capacity (L+P):    {health['service_capacity']:.3f}")
    print(f"   Operational Excellence:    {health['operational_excellence']:.3f}")
    print(f"   Security Intelligence:     {health['security_intelligence']:.3f}")
    
    return results


def run_fractal_iteration(entities: List[SemanticEntity], groups: Dict[str, List[str]], iteration: int) -> Dict:
    """Run analysis at the cluster/module level."""
    
    print(f"\n{'='*70}")
    print(f"FRACTAL ITERATION {iteration}: CLUSTER-LEVEL EMERGENCE")
    print(f"{'='*70}")
    
    # Create entity lookup
    entity_map = {e.name: e for e in entities}
    
    # Build cluster profiles
    cluster_profiles = []
    for group_name, member_names in groups.items():
        members = [entity_map[n] for n in member_names if n in entity_map]
        if members:
            # Aggregate
            avg_L = sum(m.coordinates.L for m in members) / len(members)
            avg_J = sum(m.coordinates.J for m in members) / len(members)
            avg_P = sum(m.coordinates.P for m in members) / len(members)
            avg_W = sum(m.coordinates.W for m in members) / len(members)
            
            cluster_entity = SemanticEntity(
                name=group_name,
                coordinates=LJPWVector(L=avg_L, J=avg_J, P=avg_P, W=avg_W),
                concept_count=sum(m.concept_count for m in members),
                semantic_clarity=sum(m.semantic_clarity for m in members) / len(members)
            )
            cluster_profiles.append(cluster_entity)
            
            archetype, confidence = match_archetype(cluster_entity.coordinates)
            print(f"\n📦 CLUSTER: {group_name}")
            print(f"   Members: {len(members)}")
            print(f"   LJPW: L={avg_L:.3f}, J={avg_J:.3f}, P={avg_P:.3f}, W={avg_W:.3f}")
            print(f"   Harmony: {harmony_index(cluster_entity.coordinates):.4f}")
            print(f"   Archetype: {archetype.value} ({confidence:.2f})")
            print(f"   Mass: {semantic_mass(cluster_entity):.2f}")
    
    # Cluster-level interactions
    if len(cluster_profiles) > 1:
        print(f"\n🔗 CLUSTER INTERACTIONS")
        for i, c1 in enumerate(cluster_profiles):
            for c2 in cluster_profiles[i+1:]:
                gravity = semantic_gravity(c1, c2)
                friction = semantic_friction(c1, c2)
                resonance = semantic_resonance(c1, c2)
                
                if gravity > 100 or friction > 0.3 or resonance > 0.7:
                    print(f"   {c1.name} ↔ {c2.name}:")
                    print(f"      Gravity: {gravity:.1f}, Friction: {friction:.3f}, Resonance: {resonance:.3f}")
    
    return {'clusters': [c.name for c in cluster_profiles]}


def detect_emergent_patterns(all_results: List[Dict]) -> List[str]:
    """Analyze results across iterations to find emergent patterns."""
    patterns = []
    
    # Track harmony trend
    harmonies = [r['metrics']['system_harmony'] for r in all_results if r.get('metrics', {}).get('system_harmony')]
    if len(harmonies) > 1:
        trend = harmonies[-1] - harmonies[0]
        if abs(trend) > 0.01:
            direction = "increasing" if trend > 0 else "decreasing"
            patterns.append(f"Harmony is {direction} across iterations (Δ={trend:.4f})")
    
    # Find recurring high-mass entities
    mass_mentions = defaultdict(int)
    for r in all_results:
        for insight in r.get('insights', []):
            if 'High mass' in insight:
                mass_mentions[insight] += 1
    
    for insight, count in mass_mentions.items():
        if count > 1:
            patterns.append(f"Persistent gravitational center: {insight}")
    
    # Collect all emergent patterns from iterations
    for r in all_results:
        patterns.extend(r.get('emergent_patterns', []))
    
    return list(set(patterns))


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║   FRACTAL SELF-ANALYSIS: THE REPOSITORY EXAMINES ITSELF                  ║
║                                                                          ║
║   "The tool that measures meaning, measuring its own meaning"            ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Scan the repository
    root_path = os.path.dirname(os.path.abspath(__file__))
    print(f"📂 Scanning repository: {root_path}")
    
    entities = scan_repository(root_path)
    print(f"   Found {len(entities)} Python files")
    
    # Group by directory for fractal analysis
    groups = group_by_directory(entities)
    print(f"   Organized into {len(groups)} clusters")
    
    all_results = []
    
    # =========================================================================
    # 5 ITERATIONS OF ANALYSIS
    # =========================================================================
    
    # Iteration 1: Raw atomic analysis
    results1 = run_iteration(entities, 1)
    all_results.append(results1)
    
    # Iteration 2: Fractal (cluster) analysis
    results2 = run_fractal_iteration(entities, groups, 2)
    all_results.append({'iteration': 2, 'metrics': {}, 'insights': [], 'emergent_patterns': [], **results2})
    
    # Iteration 3: Focus on experiments directory
    print(f"\n{'='*70}")
    print(f"ITERATION 3: DEEP DIVE - EXPERIMENTS CLUSTER")
    print(f"{'='*70}")
    
    exp_entities = [e for e in entities if e.name.startswith('experiments')]
    if exp_entities:
        results3 = run_iteration(exp_entities, 3)
        all_results.append(results3)
    
    # Iteration 4: Focus on documentation (docs as semantic entities)
    print(f"\n{'='*70}")
    print(f"ITERATION 4: DOCUMENTATION AS SEMANTIC ENTITY")
    print(f"{'='*70}")
    
    # Analyze docs directory
    doc_path = os.path.join(root_path, 'docs')
    if os.path.exists(doc_path):
        doc_files = [f for f in os.listdir(doc_path) if f.endswith('.md')]
        print(f"   Found {len(doc_files)} documentation files")
        
        # Estimate doc "health" based on size and structure
        total_doc_lines = 0
        for doc_file in doc_files:
            try:
                with open(os.path.join(doc_path, doc_file), 'r') as f:
                    total_doc_lines += len(f.readlines())
            except:
                pass
        
        doc_ratio = total_doc_lines / max(1, sum(e.concept_count for e in entities))
        print(f"   Documentation ratio: {doc_ratio:.2f} lines per concept")
        
        if doc_ratio > 5:
            print(f"   ✅ Well-documented (ratio > 5)")
        elif doc_ratio > 2:
            print(f"   ⚠️ Moderately documented (ratio 2-5)")
        else:
            print(f"   ❌ Under-documented (ratio < 2)")
        
        all_results.append({
            'iteration': 4,
            'metrics': {'doc_ratio': doc_ratio},
            'insights': [f"Documentation ratio: {doc_ratio:.2f}"],
            'emergent_patterns': []
        })
    
    # Iteration 5: System-level synthesis
    print(f"\n{'='*70}")
    print(f"ITERATION 5: SYSTEM SYNTHESIS - WHAT HAS EMERGED?")
    print(f"{'='*70}")
    
    # Final system health
    final_health = calculate_system_health(entities)
    
    # Match system archetype
    system_coords = LJPWVector(
        L=final_health['system_L'],
        J=final_health['system_J'],
        P=final_health['system_P'],
        W=final_health['system_W']
    )
    system_archetype, confidence = match_archetype(system_coords)
    
    print(f"\n🌐 SYSTEM-LEVEL PROFILE")
    print(f"   The repository as a whole is a: {system_archetype.value.upper()}")
    print(f"   Confidence: {confidence:.2f}")
    print(f"   {describe_archetype(system_archetype)}")
    
    # Distance from ideals
    dist_to_anchor = math.sqrt(
        (1 - system_coords.L)**2 + (1 - system_coords.J)**2 +
        (1 - system_coords.P)**2 + (1 - system_coords.W)**2
    )
    dist_to_ne = math.sqrt(
        (NATURAL_EQUILIBRIUM.L - system_coords.L)**2 +
        (NATURAL_EQUILIBRIUM.J - system_coords.J)**2 +
        (NATURAL_EQUILIBRIUM.P - system_coords.P)**2 +
        (NATURAL_EQUILIBRIUM.W - system_coords.W)**2
    )
    
    print(f"\n📍 DISTANCE FROM IDEALS")
    print(f"   Distance to Anchor (1,1,1,1): {dist_to_anchor:.4f}")
    print(f"   Distance to Natural Equilibrium: {dist_to_ne:.4f}")
    
    if dist_to_ne < dist_to_anchor * 0.5:
        print(f"   ✅ Closer to Natural Equilibrium than Anchor - realistic, achievable state")
    
    # Emergent Patterns
    print(f"\n🌱 EMERGENT PATTERNS ACROSS ALL ITERATIONS")
    patterns = detect_emergent_patterns(all_results)
    if patterns:
        for p in patterns:
            print(f"   • {p}")
    else:
        print(f"   No strong emergent patterns detected")
    
    # Final Reflection
    print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                         FINAL REFLECTION                                  ║
╚══════════════════════════════════════════════════════════════════════════╝

The repository has examined itself through {len(all_results)} fractal iterations.

WHAT WE LEARNED:
  • System Harmony: {final_health['system_harmony']:.4f}
  • Dominant Character: {system_archetype.value}
  • Total Semantic Mass: {final_health['total_mass']:.2f}
  • Entity Count: {final_health['entity_count']}

THE META-INSIGHT:
  This repository contains the tools to analyze itself.
  The analysis reveals the repository's own character.
  That character shaped the tools that performed the analysis.
  
  This is semantic autopoiesis - the system that produces itself.

""")
    
    all_results.append({
        'iteration': 5,
        'metrics': final_health,
        'insights': [f"System archetype: {system_archetype.value}"],
        'emergent_patterns': patterns
    })
    
    return all_results


if __name__ == "__main__":
    results = main()
