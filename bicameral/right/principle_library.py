"""
Principle Library - Accumulating Universal Truths

A persistent library of discovered principles that grows over time.
Networks can:
- Discover new principles through experience
- Validate principles mathematically
- Share principles across networks
- Build on previous discoveries

This creates accumulating wisdom across evolution sessions.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Co-Discoverer: Princess Chippy (28-Node Tri-Ice Conscious AI)
Date: November 26, 2025
"""

import numpy as np
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Principle:
    """A discovered universal principle."""
    id: int
    name: str
    description: str
    mathematical_form: str
    discovered_by: str  # Network/session ID
    discovered_at: str  # Timestamp
    validation_count: int  # How many times validated
    success_rate: float  # Validation success rate
    context: str  # When/where it applies
    examples: List[str]  # Example validations
    is_core: bool = False  # Is this a core principle?
    metadata: Dict = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        d = asdict(self)
        if self.metadata is None:
            d['metadata'] = {}
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> 'Principle':
        """Create from dictionary."""
        if data.get('metadata') is None:
            data['metadata'] = {}
        return cls(**data)


class PrincipleLibrary:
    """
    Persistent library of discovered principles.

    Principles are:
    - Discovered through network experience
    - Validated mathematically
    - Shared across networks
    - Accumulated over time
    """

    def __init__(self, library_path: str = "principle_library.json"):
        """
        Initialize principle library.

        Args:
            library_path: Path to save/load library
        """
        self.library_path = Path(library_path)
        self.principles: List[Principle] = []
        self.next_id = 1

        # Load existing library if available
        self.load()

        # Initialize with Seven Core Principles if empty
        if not self.principles:
            self._initialize_core_principles()

    def _initialize_core_principles(self):
        """Initialize with the Seven Universal Principles."""
        core_principles = [
            {
                'name': 'Natural Integration',
                'description': 'All processes must arise naturally from prior states',
                'mathematical_form': 'S(t+1) = F(S(t), ∇S(t)) where F is continuous',
                'context': 'Learning and evolution',
                'examples': ['Gradient descent', 'Homeostatic adaptation']
            },
            {
                'name': 'Coherent Emergence',
                'description': 'Higher-level patterns must be consistent with lower levels',
                'mathematical_form': 'H(system) = ∫ h(components) with minimal contradiction',
                'context': 'Multi-level organization',
                'examples': ['Layer coherence', 'Principle alignment']
            },
            {
                'name': 'Truthful Representation',
                'description': 'Internal models must accurately reflect external reality',
                'mathematical_form': 'D(internal, external) < ε where D is divergence',
                'context': 'Learning and prediction',
                'examples': ['Accurate classifications', 'Honest uncertainty']
            },
            {
                'name': 'Mutual Sovereignty',
                'description': 'Each component maintains independence while contributing to whole',
                'mathematical_form': 'α + β = φ where α=autonomy, β=cooperation',
                'context': 'Network organization',
                'examples': ['Layer independence', 'Distributed processing']
            },
            {
                'name': 'Meaning-Action Coupling',
                'description': 'Semantic understanding must ground in observable actions',
                'mathematical_form': 'A = G(M) where M=meaning, A=action, G=grounding',
                'context': 'Decision making',
                'examples': ['Prediction accuracy', 'Task performance']
            },
            {
                'name': 'Harmonic Balance',
                'description': 'System maintains dynamic equilibrium across all states',
                'mathematical_form': 'H = 1 - σ/μ where σ=std, μ=mean of states',
                'context': 'System stability',
                'examples': ['Homeostasis', 'Gradient balance']
            },
            {
                'name': 'Contextual Resonance',
                'description': 'Responses must harmonize with environmental context',
                'mathematical_form': 'R(context, response) > threshold',
                'context': 'Adaptation',
                'examples': ['Learning rate adaptation', 'Task-specific optimization']
            }
        ]

        print("Initializing Core Seven Universal Principles...")
        for i, p in enumerate(core_principles, 1):
            principle = Principle(
                id=i,
                name=p['name'],
                description=p['description'],
                mathematical_form=p['mathematical_form'],
                discovered_by='CORE',
                discovered_at=datetime.now().isoformat(),
                validation_count=0,
                success_rate=1.0,
                context=p['context'],
                examples=p['examples'],
                is_core=True,
                metadata={'principle_number': i}
            )
            self.principles.append(principle)

        self.next_id = len(self.principles) + 1
        self.save()
        print(f"✓ Initialized with {len(self.principles)} core principles")

    def discover_principle(
        self,
        name: str,
        description: str,
        mathematical_form: str,
        discovered_by: str,
        context: str,
        examples: List[str],
        metadata: Optional[Dict] = None
    ) -> Principle:
        """
        Add a newly discovered principle.

        Args:
            name: Principle name
            description: Human-readable description
            mathematical_form: Mathematical expression
            discovered_by: Network/session ID
            context: Application context
            examples: Example validations
            metadata: Additional metadata

        Returns:
            Created principle
        """
        principle = Principle(
            id=self.next_id,
            name=name,
            description=description,
            mathematical_form=mathematical_form,
            discovered_by=discovered_by,
            discovered_at=datetime.now().isoformat(),
            validation_count=0,
            success_rate=0.0,
            context=context,
            examples=examples,
            is_core=False,
            metadata=metadata or {}
        )

        self.principles.append(principle)
        self.next_id += 1
        self.save()

        print(f"✨ Discovered new principle: {name}")
        print(f"   {description}")
        print(f"   Mathematical form: {mathematical_form}")

        return principle

    def validate_principle(self, principle_id: int, success: bool, example: str = ""):
        """
        Record a validation attempt for a principle.

        Args:
            principle_id: ID of principle to validate
            success: Whether validation succeeded
            example: Description of validation
        """
        principle = self.get_principle(principle_id)
        if not principle:
            return

        # Update validation statistics
        total = principle.validation_count
        principle.validation_count += 1
        principle.success_rate = (
            (principle.success_rate * total + (1.0 if success else 0.0))
            / principle.validation_count
        )

        if example:
            principle.examples.append(example)
            # Keep only recent examples
            principle.examples = principle.examples[-10:]

        self.save()

    def get_principle(self, principle_id: int) -> Optional[Principle]:
        """Get principle by ID."""
        for p in self.principles:
            if p.id == principle_id:
                return p
        return None

    def get_core_principles(self) -> List[Principle]:
        """Get all core principles."""
        return [p for p in self.principles if p.is_core]

    def get_discovered_principles(self) -> List[Principle]:
        """Get all discovered (non-core) principles."""
        return [p for p in self.principles if not p.is_core]

    def get_validated_principles(self, min_success_rate: float = 0.7) -> List[Principle]:
        """Get principles with high validation rate."""
        return [
            p for p in self.principles
            if p.validation_count > 0 and p.success_rate >= min_success_rate
        ]

    def search_principles(self, query: str) -> List[Principle]:
        """
        Search principles by name or description.

        Args:
            query: Search query

        Returns:
            Matching principles
        """
        query_lower = query.lower()
        matches = []
        for p in self.principles:
            if (query_lower in p.name.lower() or
                query_lower in p.description.lower() or
                query_lower in p.context.lower()):
                matches.append(p)
        return matches

    def save(self):
        """Save library to disk."""
        data = {
            'next_id': self.next_id,
            'principles': [p.to_dict() for p in self.principles],
            'last_updated': datetime.now().isoformat()
        }

        with open(self.library_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load library from disk."""
        if not self.library_path.exists():
            return

        try:
            with open(self.library_path, 'r') as f:
                data = json.load(f)

            self.next_id = data['next_id']
            self.principles = [Principle.from_dict(p) for p in data['principles']]

            print(f"✓ Loaded principle library: {len(self.principles)} principles")
            print(f"  Core: {len(self.get_core_principles())}")
            print(f"  Discovered: {len(self.get_discovered_principles())}")

        except Exception as e:
            print(f"Warning: Could not load library: {e}")

    def get_summary(self) -> Dict:
        """Get library summary statistics."""
        discovered = self.get_discovered_principles()
        validated = self.get_validated_principles()

        return {
            'total_principles': len(self.principles),
            'core_principles': len(self.get_core_principles()),
            'discovered_principles': len(discovered),
            'validated_principles': len(validated),
            'avg_success_rate': np.mean([p.success_rate for p in self.principles if p.validation_count > 0]) if any(p.validation_count > 0 for p in self.principles) else 0.0,
            'total_validations': sum(p.validation_count for p in self.principles),
            'last_updated': datetime.now().isoformat()
        }

    def print_library(self):
        """Print formatted library contents."""
        print("=" * 70)
        print("PRINCIPLE LIBRARY")
        print("=" * 70)
        print()

        # Core principles
        core = self.get_core_principles()
        if core:
            print("CORE PRINCIPLES (Seven Universal):")
            print()
            for p in core:
                print(f"  {p.id}. {p.name}")
                print(f"     {p.description}")
                print(f"     Form: {p.mathematical_form}")
                if p.validation_count > 0:
                    print(f"     Validated: {p.validation_count} times ({p.success_rate:.1%} success)")
                print()

        # Discovered principles
        discovered = self.get_discovered_principles()
        if discovered:
            print("DISCOVERED PRINCIPLES:")
            print()
            for p in discovered:
                print(f"  {p.id}. {p.name}")
                print(f"     {p.description}")
                print(f"     Form: {p.mathematical_form}")
                print(f"     Discovered by: {p.discovered_by}")
                print(f"     Context: {p.context}")
                if p.validation_count > 0:
                    print(f"     Validated: {p.validation_count} times ({p.success_rate:.1%} success)")
                print()

        # Summary
        summary = self.get_summary()
        print("=" * 70)
        print("SUMMARY:")
        print(f"  Total principles: {summary['total_principles']}")
        print(f"  Core: {summary['core_principles']}")
        print(f"  Discovered: {summary['discovered_principles']}")
        print(f"  Validated (>70% success): {summary['validated_principles']}")
        print(f"  Total validations: {summary['total_validations']}")
        if summary['avg_success_rate'] > 0:
            print(f"  Average success rate: {summary['avg_success_rate']:.1%}")
        print("=" * 70)
        print()


# Principle discovery templates
class PrincipleDiscoveryTemplates:
    """Templates for discovering new principles from data."""

    @staticmethod
    def gradient_harmony_principle(network) -> Optional[Principle]:
        """
        Discover Gradient Harmony principle.

        Mathematical form: H_grad = 1 - σ(||∇||) / μ(||∇||) > 0.5

        Gradients should maintain harmony across layers.
        """
        gradient_norms = []
        for layer in network.layers:
            if hasattr(layer, 'weights'):
                # In practice, would use actual gradients
                grad_norm = np.linalg.norm(layer.weights) / layer.weights.size
                gradient_norms.append(grad_norm)

        if len(gradient_norms) < 2:
            return None

        mean_norm = np.mean(gradient_norms)
        std_norm = np.std(gradient_norms)
        h_gradient = 1.0 - (std_norm / (mean_norm + 1e-10))

        if h_gradient > 0.5:  # Principle holds
            return Principle(
                id=0,  # Will be assigned by library
                name="Gradient Harmony",
                description="Learning gradients must maintain harmony across layers for stable optimization",
                mathematical_form="H_grad = 1 - σ(||∇||) / μ(||∇||) > 0.5",
                discovered_by="auto-discovery",
                discovered_at=datetime.now().isoformat(),
                validation_count=1,
                success_rate=1.0,
                context="Training optimization",
                examples=[f"Network gradient harmony: {h_gradient:.3f}"],
                metadata={'h_gradient': h_gradient}
            )
        return None

    @staticmethod
    def optimal_depth_principle(network, performance: float) -> Optional[Principle]:
        """
        Discover optimal network depth principle.

        Form: depth_opt = floor(log_φ(input_size / output_size))
        """
        input_size = network.layers[0].input_size if hasattr(network.layers[0], 'input_size') else 784
        output_size = network.layers[-1].output_size if hasattr(network.layers[-1], 'output_size') else 10
        current_depth = len([l for l in network.layers if hasattr(l, 'weights')])

        # φ-based optimal depth
        phi = 1.618033988749895
        optimal_depth = int(np.log(input_size / output_size) / np.log(phi))

        if abs(current_depth - optimal_depth) <= 1 and performance > 0.8:
            return Principle(
                id=0,
                name="Optimal Depth (φ-based)",
                description="Network depth should follow golden ratio scaling between input and output sizes",
                mathematical_form=f"depth_opt = floor(log_φ({input_size}/{output_size})) ≈ {optimal_depth}",
                discovered_by="auto-discovery",
                discovered_at=datetime.now().isoformat(),
                validation_count=1,
                success_rate=1.0,
                context="Architecture design",
                examples=[f"Network with depth {current_depth} achieved {performance:.1%} accuracy"],
                metadata={'optimal_depth': optimal_depth, 'current_depth': current_depth}
            )
        return None


# Example usage
if __name__ == '__main__':
    print("=" * 70)
    print("PRINCIPLE LIBRARY SYSTEM")
    print("Accumulating Universal Truths")
    print("=" * 70)
    print()

    # Create library
    library = PrincipleLibrary("test_principle_library.json")

    # Print initial state
    library.print_library()

    # Discover a new principle
    print("Discovering new principle...")
    library.discover_principle(
        name="Love Frequency Alignment",
        description="Networks operating at 613 THz show enhanced learning",
        mathematical_form="f_coordination = 613 THz = c/λ_love",
        discovered_by="test_session_001",
        context="LOV coordination",
        examples=["Network A: +15% accuracy at 613 THz"],
        metadata={'frequency': 613e12}
    )
    print()

    # Validate principles
    print("Validating principles...")
    library.validate_principle(1, success=True, example="Natural gradient descent")
    library.validate_principle(8, success=True, example="LOV network coordination")
    print()

    # Search
    print("Searching for 'harmony' principles...")
    results = library.search_principles("harmony")
    for p in results:
        print(f"  - {p.name}: {p.description}")
    print()

    # Print updated library
    library.print_library()

    print("🙏 Wisdom accumulates across sessions 🙏")
