#!/usr/bin/env python3
"""
SPDX-License-Identifier: MIT
LJPW Semantic Capabilities Module

This module extends the LJPW framework with advanced semantic analysis capabilities
for analyzing complex systems through the lens of Love, Justice, Power, and Wisdom.

New concepts introduced:
- Semantic Mass & Density: Weight and substance of entities
- Semantic Drift: Movement through LJPW space over time
- Service Archetypes: Predefined personality profiles
- Semantic Relationships: Interaction physics (gravity, friction, resonance)
- Dimensional Combinations: Secondary/derived metrics
- Fractal Profiling: Multi-scale LJPW analysis

Version: 1.0.0
Date: 2025-11-29
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum


# =============================================================================
# CORE DATA STRUCTURES
# =============================================================================

@dataclass
class LJPWVector:
    """A point in 4-dimensional LJPW semantic space."""
    L: float  # Love: Connectivity, openness, integration
    J: float  # Justice: Security, rules, boundaries, fairness
    P: float  # Power: Performance, capacity, throughput
    W: float  # Wisdom: Observability, logging, insight
    
    def __post_init__(self):
        """Ensure values are normalized to [0, 1] range."""
        self.L = max(0.0, min(1.0, self.L))
        self.J = max(0.0, min(1.0, self.J))
        self.P = max(0.0, min(1.0, self.P))
        self.W = max(0.0, min(1.0, self.W))
    
    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.L, self.J, self.P, self.W)
    
    def volume(self) -> float:
        """Average of all dimensions - represents functional footprint."""
        return (self.L + self.J + self.P + self.W) / 4.0
    
    def dominant_dimension(self) -> str:
        """Returns the name of the highest dimension."""
        dims = {'L': self.L, 'J': self.J, 'P': self.P, 'W': self.W}
        return max(dims, key=dims.get)


@dataclass
class SemanticEntity:
    """An entity with semantic properties in LJPW space."""
    name: str
    coordinates: LJPWVector
    concept_count: int = 1
    semantic_clarity: float = 0.5
    timestamp: Optional[float] = None
    metadata: Dict = field(default_factory=dict)


# =============================================================================
# REFERENCE POINTS
# =============================================================================

# The Source - Divine Perfection
ANCHOR_POINT = LJPWVector(L=1.0, J=1.0, P=1.0, W=1.0)

# Natural Equilibrium - Achievable Optimal Balance
NATURAL_EQUILIBRIUM = LJPWVector(
    L=0.618034,  # φ⁻¹ = (√5 - 1)/2 - Golden Ratio
    J=0.414214,  # √2 - 1 - Pythagorean
    P=0.718282,  # e - 2 - Exponential
    W=0.693147   # ln(2) - Information Unit
)


# =============================================================================
# 1. HARMONY & CLARITY (Core Metrics)
# =============================================================================

def harmony_index(coords: LJPWVector, anchor: LJPWVector = ANCHOR_POINT) -> float:
    """
    Harmony Score: How well balanced the entity is relative to an anchor.
    
    Formula: H = 1.0 / (1.0 + distance_to_anchor)
    
    Higher harmony indicates better alignment with the ideal state.
    """
    d = math.sqrt(
        (anchor.L - coords.L) ** 2 +
        (anchor.J - coords.J) ** 2 +
        (anchor.P - coords.P) ** 2 +
        (anchor.W - coords.W) ** 2
    )
    return 1.0 / (1.0 + d)


def semantic_clarity(entity: SemanticEntity) -> float:
    """
    Semantic Clarity: How distinct and unambiguous the entity's purpose is.
    
    High clarity: A dedicated, focused system (e.g., a pure database server)
    Low clarity: A system running many unrelated services
    
    Measured by:
    - Dominance of primary dimension
    - Consistency of supporting dimensions
    """
    coords = entity.coordinates
    dims = [coords.L, coords.J, coords.P, coords.W]
    
    # Primary dimension dominance
    max_dim = max(dims)
    mean_dim = sum(dims) / 4.0
    dominance = max_dim / mean_dim if mean_dim > 0 else 1.0
    
    # Variance (lower is clearer when dominated)
    variance = sum((d - mean_dim) ** 2 for d in dims) / 4.0
    
    # Clarity increases with dominance and decreases with ambiguity
    base_clarity = entity.semantic_clarity
    adjusted_clarity = base_clarity * (0.5 + 0.5 * (dominance - 1.0))
    
    return max(0.0, min(1.0, adjusted_clarity))


# =============================================================================
# 2. SEMANTIC MASS & DENSITY
# =============================================================================

def semantic_mass(entity: SemanticEntity) -> float:
    """
    Semantic Mass: The significance or "gravity" of an entity.
    
    Formula: Mass = (ConceptCount × SemanticClarity) × (1 + HarmonyScore)
    
    A complex, well-defined, and harmonious system has high mass.
    High mass entities exert more influence on their semantic neighbors.
    """
    clarity = semantic_clarity(entity)
    harmony = harmony_index(entity.coordinates)
    
    return (entity.concept_count * clarity) * (1.0 + harmony)


def semantic_density(entity: SemanticEntity) -> float:
    """
    Semantic Density: Mass per unit volume.
    
    Formula: Density = Mass / Volume
    
    Where Volume is the average of LJPW dimensions (functional footprint).
    
    High density indicates a highly potent system packed into a small
    functional footprint (e.g., a critical authentication server).
    """
    mass = semantic_mass(entity)
    volume = entity.coordinates.volume()
    
    # Avoid division by zero
    if volume < 0.01:
        return mass / 0.01
    
    return mass / volume


def semantic_influence(entity: SemanticEntity) -> float:
    """
    Semantic Influence: How much this entity affects its neighbors.
    
    Formula: Influence = Mass × Clarity
    
    High influence entities shape the semantic landscape around them.
    """
    mass = semantic_mass(entity)
    clarity = semantic_clarity(entity)
    
    return mass * clarity


# =============================================================================
# 3. SEMANTIC DRIFT (Temporal Analysis)
# =============================================================================

@dataclass
class SemanticDrift:
    """Represents movement through LJPW space over time."""
    delta_L: float
    delta_J: float
    delta_P: float
    delta_W: float
    time_delta: float
    
    @property
    def magnitude(self) -> float:
        """Total distance moved in semantic space."""
        return math.sqrt(
            self.delta_L ** 2 +
            self.delta_J ** 2 +
            self.delta_P ** 2 +
            self.delta_W ** 2
        )
    
    @property
    def velocity(self) -> float:
        """Rate of change (magnitude per time unit)."""
        if self.time_delta <= 0:
            return 0.0
        return self.magnitude / self.time_delta
    
    @property
    def direction(self) -> Dict[str, float]:
        """Normalized direction vector."""
        mag = self.magnitude
        if mag == 0:
            return {'L': 0, 'J': 0, 'P': 0, 'W': 0}
        return {
            'L': self.delta_L / mag,
            'J': self.delta_J / mag,
            'P': self.delta_P / mag,
            'W': self.delta_W / mag
        }


def calculate_drift(
    entity_t0: SemanticEntity,
    entity_t1: SemanticEntity
) -> SemanticDrift:
    """
    Calculate semantic drift between two states of an entity.
    
    Use cases:
    - Detecting "entropy" (decay of Justice/Wisdom)
    - Detecting "hardening" (increase in Justice)
    - Tracking active development (high velocity)
    - Predicting future state based on trajectory
    """
    c0, c1 = entity_t0.coordinates, entity_t1.coordinates
    
    time_delta = 1.0  # Default time unit
    if entity_t0.timestamp and entity_t1.timestamp:
        time_delta = max(0.001, entity_t1.timestamp - entity_t0.timestamp)
    
    return SemanticDrift(
        delta_L=c1.L - c0.L,
        delta_J=c1.J - c0.J,
        delta_P=c1.P - c0.P,
        delta_W=c1.W - c0.W,
        time_delta=time_delta
    )


def predict_future_state(
    entity: SemanticEntity,
    drift: SemanticDrift,
    time_forward: float
) -> LJPWVector:
    """
    Predict future LJPW coordinates based on current trajectory.
    
    Simple linear extrapolation - assumes constant velocity.
    """
    velocity_factor = time_forward / drift.time_delta if drift.time_delta > 0 else 0
    
    return LJPWVector(
        L=entity.coordinates.L + drift.delta_L * velocity_factor,
        J=entity.coordinates.J + drift.delta_J * velocity_factor,
        P=entity.coordinates.P + drift.delta_P * velocity_factor,
        W=entity.coordinates.W + drift.delta_W * velocity_factor
    )


def drift_interpretation(drift: SemanticDrift) -> str:
    """
    Interpret the meaning of a semantic drift.
    """
    interpretations = []
    
    # Love drift
    if drift.delta_L > 0.1:
        interpretations.append("Opening up (increased connectivity)")
    elif drift.delta_L < -0.1:
        interpretations.append("Closing down (decreased connectivity)")
    
    # Justice drift
    if drift.delta_J > 0.1:
        interpretations.append("Hardening (increased security/rules)")
    elif drift.delta_J < -0.1:
        interpretations.append("Entropy (decaying structure)")
    
    # Power drift
    if drift.delta_P > 0.1:
        interpretations.append("Empowering (increased capacity)")
    elif drift.delta_P < -0.1:
        interpretations.append("Depleting (decreased capacity)")
    
    # Wisdom drift
    if drift.delta_W > 0.1:
        interpretations.append("Enlightening (increased observability)")
    elif drift.delta_W < -0.1:
        interpretations.append("Obscuring (decreased insight)")
    
    # Velocity interpretation
    if drift.velocity > 0.5:
        interpretations.append("⚠️ High velocity - instability or active development")
    
    return "; ".join(interpretations) if interpretations else "Stable (minimal drift)"


# =============================================================================
# 4. SERVICE ARCHETYPES
# =============================================================================

class Archetype(Enum):
    """Predefined personality profiles defined by LJPW signature ranges."""
    
    # Network/Infrastructure Archetypes
    PUBLIC_GATEWAY = "public_gateway"      # High Love, Moderate Justice
    SECURITY_SENTINEL = "security_sentinel"  # High Justice, Low Love
    DATA_VAULT = "data_vault"              # High Power, Moderate Justice
    MONITORING_HUB = "monitoring_hub"      # High Wisdom
    
    # Software Component Archetypes
    API_ENDPOINT = "api_endpoint"          # High Love, High Power
    VALIDATOR = "validator"                # High Justice
    TRANSFORMER = "transformer"            # High Power, Moderate Wisdom
    LOGGER = "logger"                      # High Wisdom, Moderate Love
    
    # System Archetypes
    BALANCED_SYSTEM = "balanced_system"    # All dimensions moderate-high
    CHAOTIC_SYSTEM = "chaotic_system"      # Low harmony, high variance
    FORTRESS = "fortress"                  # Very high Justice, low Love


# Archetype signature definitions
ARCHETYPE_SIGNATURES: Dict[Archetype, Dict[str, Tuple[float, float]]] = {
    Archetype.PUBLIC_GATEWAY: {
        'L': (0.7, 1.0), 'J': (0.4, 0.7), 'P': (0.5, 0.8), 'W': (0.4, 0.7)
    },
    Archetype.SECURITY_SENTINEL: {
        'L': (0.1, 0.4), 'J': (0.8, 1.0), 'P': (0.3, 0.6), 'W': (0.5, 0.8)
    },
    Archetype.DATA_VAULT: {
        'L': (0.3, 0.6), 'J': (0.5, 0.8), 'P': (0.7, 1.0), 'W': (0.4, 0.7)
    },
    Archetype.MONITORING_HUB: {
        'L': (0.5, 0.8), 'J': (0.4, 0.7), 'P': (0.4, 0.7), 'W': (0.8, 1.0)
    },
    Archetype.API_ENDPOINT: {
        'L': (0.7, 1.0), 'J': (0.4, 0.7), 'P': (0.7, 1.0), 'W': (0.4, 0.7)
    },
    Archetype.VALIDATOR: {
        'L': (0.3, 0.6), 'J': (0.8, 1.0), 'P': (0.3, 0.6), 'W': (0.5, 0.8)
    },
    Archetype.TRANSFORMER: {
        'L': (0.4, 0.7), 'J': (0.4, 0.7), 'P': (0.7, 1.0), 'W': (0.5, 0.8)
    },
    Archetype.LOGGER: {
        'L': (0.5, 0.8), 'J': (0.3, 0.6), 'P': (0.3, 0.6), 'W': (0.8, 1.0)
    },
    Archetype.BALANCED_SYSTEM: {
        'L': (0.5, 0.8), 'J': (0.5, 0.8), 'P': (0.5, 0.8), 'W': (0.5, 0.8)
    },
    Archetype.CHAOTIC_SYSTEM: {
        'L': (0.0, 1.0), 'J': (0.0, 1.0), 'P': (0.0, 1.0), 'W': (0.0, 1.0)
    },
    Archetype.FORTRESS: {
        'L': (0.0, 0.3), 'J': (0.9, 1.0), 'P': (0.4, 0.7), 'W': (0.5, 0.8)
    },
}


def match_archetype(coords: LJPWVector) -> Tuple[Archetype, float]:
    """
    Match an entity's coordinates against the library of archetypes.
    
    Returns the best matching archetype and a confidence score (0-1).
    """
    best_match = None
    best_score = -1.0
    
    for archetype, signature in ARCHETYPE_SIGNATURES.items():
        score = _archetype_match_score(coords, signature)
        if score > best_score:
            best_score = score
            best_match = archetype
    
    return (best_match, best_score)


def _archetype_match_score(
    coords: LJPWVector,
    signature: Dict[str, Tuple[float, float]]
) -> float:
    """Calculate how well coordinates match an archetype signature."""
    scores = []
    
    # Calculate specificity bonus - narrower ranges are more specific
    total_range = sum(high - low for low, high in signature.values())
    specificity_bonus = 1.0 - (total_range / 4.0)  # Max range is 4.0 (1.0 per dim)
    
    for dim, (low, high) in signature.items():
        value = getattr(coords, dim)
        if low <= value <= high:
            # Perfect match - score based on distance to center
            center = (low + high) / 2
            range_size = (high - low) / 2
            if range_size > 0:
                distance = abs(value - center) / range_size
                scores.append(1.0 - distance * 0.5)  # 0.5 to 1.0
            else:
                scores.append(1.0)
        else:
            # Outside range - penalize by distance
            if value < low:
                penalty = (low - value) / max(low, 0.1)
            else:
                penalty = (value - high) / max(1.0 - high, 0.1)
            scores.append(max(0.0, 1.0 - penalty))
    
    base_score = sum(scores) / len(scores) if scores else 0.0
    # Apply specificity bonus to prefer more specific archetypes
    return base_score * (0.7 + 0.3 * specificity_bonus)


def describe_archetype(archetype: Archetype) -> str:
    """Get a human-readable description of an archetype."""
    descriptions = {
        Archetype.PUBLIC_GATEWAY: "The Public Gateway: Open, welcoming, but with reasonable security. E.g., Web Server, API Gateway.",
        Archetype.SECURITY_SENTINEL: "The Security Sentinel: Strict, protective, defensive. E.g., Firewall, Authentication Service.",
        Archetype.DATA_VAULT: "The Data Vault: Powerful, structured storage. E.g., Database, Cache Server.",
        Archetype.MONITORING_HUB: "The Monitoring Hub: Observant, insightful, watchful. E.g., Splunk, Prometheus, Log Aggregator.",
        Archetype.API_ENDPOINT: "The API Endpoint: Open and powerful, serving many users efficiently.",
        Archetype.VALIDATOR: "The Validator: Ensures correctness and compliance with rules.",
        Archetype.TRANSFORMER: "The Transformer: Processes and transforms data efficiently.",
        Archetype.LOGGER: "The Logger: Records and illuminates system behavior.",
        Archetype.BALANCED_SYSTEM: "The Balanced System: Well-rounded, harmonious across all dimensions.",
        Archetype.CHAOTIC_SYSTEM: "The Chaotic System: Unpredictable, lacking clear purpose or structure.",
        Archetype.FORTRESS: "The Fortress: Maximum security, minimal accessibility.",
    }
    return descriptions.get(archetype, "Unknown archetype")


# =============================================================================
# 5. SEMANTIC RELATIONSHIPS (Interaction Physics)
# =============================================================================

def semantic_gravity(
    entity1: SemanticEntity,
    entity2: SemanticEntity,
    G: float = 1.0
) -> float:
    """
    Semantic Gravity: Attraction between entities based on mass.
    
    Formula: F = G × (m1 × m2) / r²
    
    Where r is the semantic distance between entities.
    
    High mass entities "pull" other entities towards them
    (e.g., a central dependency attracts many modules).
    """
    m1 = semantic_mass(entity1)
    m2 = semantic_mass(entity2)
    
    c1, c2 = entity1.coordinates, entity2.coordinates
    r = math.sqrt(
        (c1.L - c2.L) ** 2 +
        (c1.J - c2.J) ** 2 +
        (c1.P - c2.P) ** 2 +
        (c1.W - c2.W) ** 2
    )
    
    # Avoid division by zero (entities at same position)
    r = max(r, 0.01)
    
    return G * (m1 * m2) / (r ** 2)


def semantic_friction(
    entity1: SemanticEntity,
    entity2: SemanticEntity
) -> float:
    """
    Semantic Friction: Resistance generated when entities with opposing values interact.
    
    High friction occurs when:
    - A High Love system tries to talk to a High Justice firewall
    - A High Power system lacks the Wisdom to handle a Wise system
    
    Returns a friction coefficient (0 = smooth, 1 = maximum resistance).
    """
    c1, c2 = entity1.coordinates, entity2.coordinates
    
    # Calculate opposition on each axis
    # Friction is highest when one is high and the other is low
    friction_scores = []
    
    for dim in ['L', 'J', 'P', 'W']:
        v1 = getattr(c1, dim)
        v2 = getattr(c2, dim)
        
        # Opposition: high when one high, one low
        opposition = abs(v1 - v2)
        
        # Weight by the importance of the dimension for interaction
        # L-J opposition is particularly friction-generating
        if dim in ['L', 'J']:
            friction_scores.append(opposition * 1.2)
        else:
            friction_scores.append(opposition)
    
    return min(1.0, sum(friction_scores) / len(friction_scores))


def semantic_resonance(
    entity1: SemanticEntity,
    entity2: SemanticEntity
) -> float:
    """
    Semantic Resonance: Amplification that occurs when entities share similar frequencies.
    
    Resonance occurs when entities have similar dominant dimensions and
    comparable values across all dimensions.
    
    Returns a resonance score (0 = no resonance, 1 = perfect resonance).
    """
    c1, c2 = entity1.coordinates, entity2.coordinates
    
    # Check if dominant dimensions match
    dom1 = c1.dominant_dimension()
    dom2 = c2.dominant_dimension()
    
    # Base resonance from dimension alignment
    if dom1 == dom2:
        dominant_match = 0.3
    else:
        dominant_match = 0.0
    
    # Similarity across all dimensions
    similarity_scores = []
    for dim in ['L', 'J', 'P', 'W']:
        v1 = getattr(c1, dim)
        v2 = getattr(c2, dim)
        similarity = 1.0 - abs(v1 - v2)
        similarity_scores.append(similarity)
    
    avg_similarity = sum(similarity_scores) / len(similarity_scores)
    
    # Combined resonance
    return min(1.0, dominant_match + avg_similarity * 0.7)


# =============================================================================
# 6. DIMENSIONAL COMBINATIONS (Secondary Metrics)
# =============================================================================

def secure_connectivity(coords: LJPWVector) -> float:
    """
    Secure Connectivity: L + J
    
    Can we connect safely? Balances openness with security.
    """
    return (coords.L + coords.J) / 2.0


def service_capacity(coords: LJPWVector) -> float:
    """
    Service Capacity: L + P
    
    Can we serve many users? Balances connectivity with power.
    """
    return (coords.L + coords.P) / 2.0


def operational_excellence(coords: LJPWVector) -> float:
    """
    Operational Excellence: L + J + P (The "Golden Triangle" of ops)
    
    Full operational capability without the meta-awareness of Wisdom.
    """
    return (coords.L + coords.J + coords.P) / 3.0


def security_intelligence(coords: LJPWVector) -> float:
    """
    Security Intelligence: J + W
    
    Do we know when we are being attacked? Combines defense with insight.
    """
    return (coords.J + coords.W) / 2.0


def wise_power(coords: LJPWVector) -> float:
    """
    Wise Power: P + W
    
    Power guided by insight and awareness.
    """
    return (coords.P + coords.W) / 2.0


def loving_wisdom(coords: LJPWVector) -> float:
    """
    Loving Wisdom: L + W
    
    Insight combined with connectivity and care.
    """
    return (coords.L + coords.W) / 2.0


def all_secondary_metrics(coords: LJPWVector) -> Dict[str, float]:
    """Calculate all secondary/combined metrics."""
    return {
        'secure_connectivity': secure_connectivity(coords),
        'service_capacity': service_capacity(coords),
        'operational_excellence': operational_excellence(coords),
        'security_intelligence': security_intelligence(coords),
        'wise_power': wise_power(coords),
        'loving_wisdom': loving_wisdom(coords),
    }


# =============================================================================
# 7. FRACTAL PROFILING (Multi-Scale Analysis)
# =============================================================================

class FractalScale(Enum):
    """Scales for fractal LJPW analysis."""
    ATOMIC = "atomic"        # Port/Service level
    ENTITY = "entity"        # Host/Component level
    CLUSTER = "cluster"      # Subnet/Group level
    SYSTEM = "system"        # Network/Application level
    PLATFORM = "platform"    # Multi-system platform level


@dataclass
class FractalProfile:
    """LJPW profile with scale context."""
    scale: FractalScale
    coordinates: LJPWVector
    children: List['FractalProfile'] = field(default_factory=list)
    name: str = ""


def aggregate_profiles(
    children: List[FractalProfile],
    weights: Optional[List[float]] = None
) -> LJPWVector:
    """
    Aggregate child profiles into a parent profile.
    
    Uses weighted averaging by default, with optional custom weights.
    """
    if not children:
        return NATURAL_EQUILIBRIUM
    
    if weights is None:
        weights = [1.0] * len(children)
    
    total_weight = sum(weights)
    if total_weight == 0:
        return NATURAL_EQUILIBRIUM
    
    L = sum(c.coordinates.L * w for c, w in zip(children, weights)) / total_weight
    J = sum(c.coordinates.J * w for c, w in zip(children, weights)) / total_weight
    P = sum(c.coordinates.P * w for c, w in zip(children, weights)) / total_weight
    W = sum(c.coordinates.W * w for c, w in zip(children, weights)) / total_weight
    
    return LJPWVector(L=L, J=J, P=P, W=W)


def build_fractal_tree(
    components: List[SemanticEntity],
    groupings: Dict[str, List[str]],
    top_level_name: str = "System"
) -> FractalProfile:
    """
    Build a fractal profile tree from components and groupings.
    
    Args:
        components: List of atomic-level entities
        groupings: Dict mapping group names to component names
        top_level_name: Name for the root profile
    
    Returns:
        A FractalProfile tree with aggregated coordinates at each level
    """
    # Create atomic profiles
    atomic_profiles = {
        c.name: FractalProfile(
            scale=FractalScale.ATOMIC,
            coordinates=c.coordinates,
            name=c.name
        )
        for c in components
    }
    
    # Create cluster profiles
    cluster_profiles = []
    for group_name, member_names in groupings.items():
        members = [atomic_profiles[n] for n in member_names if n in atomic_profiles]
        if members:
            cluster_coords = aggregate_profiles(members)
            cluster_profiles.append(FractalProfile(
                scale=FractalScale.CLUSTER,
                coordinates=cluster_coords,
                children=members,
                name=group_name
            ))
    
    # Create system-level profile
    system_coords = aggregate_profiles(cluster_profiles)
    return FractalProfile(
        scale=FractalScale.SYSTEM,
        coordinates=system_coords,
        children=cluster_profiles,
        name=top_level_name
    )


# =============================================================================
# COMPREHENSIVE DIAGNOSTIC
# =============================================================================

def full_semantic_diagnostic(entity: SemanticEntity) -> Dict:
    """
    Generate a comprehensive semantic diagnostic for an entity.
    
    Includes all metrics: mass, density, influence, clarity, harmony,
    archetype matching, and secondary metrics.
    """
    coords = entity.coordinates
    archetype, archetype_confidence = match_archetype(coords)
    
    return {
        'name': entity.name,
        'coordinates': {
            'L': coords.L,
            'J': coords.J,
            'P': coords.P,
            'W': coords.W,
        },
        'primary_metrics': {
            'harmony_index': harmony_index(coords),
            'semantic_clarity': semantic_clarity(entity),
            'semantic_mass': semantic_mass(entity),
            'semantic_density': semantic_density(entity),
            'semantic_influence': semantic_influence(entity),
        },
        'archetype': {
            'match': archetype.value if archetype else None,
            'confidence': archetype_confidence,
            'description': describe_archetype(archetype) if archetype else None,
        },
        'secondary_metrics': all_secondary_metrics(coords),
        'dominant_dimension': coords.dominant_dimension(),
        'volume': coords.volume(),
    }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LJPW SEMANTIC CAPABILITIES DEMONSTRATION")
    print("=" * 70)
    
    # Create example entities
    web_server = SemanticEntity(
        name="web_server",
        coordinates=LJPWVector(L=0.8, J=0.5, P=0.7, W=0.5),
        concept_count=15,
        semantic_clarity=0.7
    )
    
    firewall = SemanticEntity(
        name="firewall",
        coordinates=LJPWVector(L=0.2, J=0.9, P=0.4, W=0.6),
        concept_count=8,
        semantic_clarity=0.9
    )
    
    database = SemanticEntity(
        name="database",
        coordinates=LJPWVector(L=0.4, J=0.6, P=0.9, W=0.5),
        concept_count=25,
        semantic_clarity=0.8
    )
    
    # Full diagnostic
    print("\n--- Full Diagnostic: Web Server ---")
    diag = full_semantic_diagnostic(web_server)
    for section, values in diag.items():
        if isinstance(values, dict):
            print(f"\n{section}:")
            for k, v in values.items():
                if isinstance(v, float):
                    print(f"  {k}: {v:.4f}")
                else:
                    print(f"  {k}: {v}")
        else:
            print(f"{section}: {values}")
    
    # Interaction physics
    print("\n--- Interaction Physics ---")
    gravity = semantic_gravity(web_server, firewall)
    friction = semantic_friction(web_server, firewall)
    resonance = semantic_resonance(web_server, database)
    
    print(f"Web Server <-> Firewall Gravity: {gravity:.4f}")
    print(f"Web Server <-> Firewall Friction: {friction:.4f}")
    print(f"Web Server <-> Database Resonance: {resonance:.4f}")
    
    # Drift analysis
    print("\n--- Drift Analysis ---")
    web_server_t1 = SemanticEntity(
        name="web_server",
        coordinates=LJPWVector(L=0.75, J=0.6, P=0.7, W=0.55),
        concept_count=18,
        semantic_clarity=0.7,
        timestamp=1.0
    )
    web_server.timestamp = 0.0
    
    drift = calculate_drift(web_server, web_server_t1)
    print(f"Drift Magnitude: {drift.magnitude:.4f}")
    print(f"Drift Velocity: {drift.velocity:.4f}")
    print(f"Interpretation: {drift_interpretation(drift)}")
    
    print("\n" + "=" * 70)
