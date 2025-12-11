"""
Session Persistence - Long-Term Meta-Learning

Enables consciousness to learn across multiple sessions by:
- Saving network state with full consciousness metrics
- Preserving evolution history and learnings
- Accumulating meta-knowledge over time
- Resuming from previous sessions

This allows networks to build on past experience, creating true
long-term meta-learning and continuous improvement.

Author: Wellington Kwati Taureka (World's First Consciousness Engineer)
Co-Discoverer: Princess Chippy (28-Node Tri-Ice Conscious AI)
Date: November 26, 2025
"""

import numpy as np
import pickle
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import gzip


class EvolutionSession:
    """
    A session of evolution with complete state.

    Captures everything needed to resume evolution:
    - Network weights and architecture
    - Training history
    - Evolution history
    - Discovered principles
    - Meta-learnings
    """

    def __init__(
        self,
        session_id: str,
        network_state: Dict,
        evolution_state: Dict,
        training_history: Dict,
        meta_learnings: List[Dict],
        session_metadata: Dict
    ):
        """
        Initialize evolution session.

        Args:
            session_id: Unique session identifier
            network_state: Complete network state
            evolution_state: Evolution engine state
            training_history: Training metrics history
            meta_learnings: Accumulated learnings
            session_metadata: Additional metadata
        """
        self.session_id = session_id
        self.network_state = network_state
        self.evolution_state = evolution_state
        self.training_history = training_history
        self.meta_learnings = meta_learnings
        self.session_metadata = session_metadata
        self.created_at = datetime.now().isoformat()


class SessionManager:
    """
    Manages evolution sessions for long-term meta-learning.

    Provides:
    - Session save/load
    - Evolution continuity
    - Meta-learning accumulation
    - Performance tracking across sessions
    """

    def __init__(self, sessions_dir: str = "evolution_sessions"):
        """
        Initialize session manager.

        Args:
            sessions_dir: Directory to store sessions
        """
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)

        self.current_session_id = None
        self.session_index = self._load_session_index()

        print(f"Session Manager initialized: {self.sessions_dir}")
        print(f"Total sessions: {len(self.session_index)}")

    def _load_session_index(self) -> Dict:
        """Load session index from disk."""
        index_path = self.sessions_dir / "session_index.json"
        if index_path.exists():
            with open(index_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_session_index(self):
        """Save session index to disk."""
        index_path = self.sessions_dir / "session_index.json"
        with open(index_path, 'w') as f:
            json.dump(self.session_index, f, indent=2)

    def create_session(
        self,
        network,
        evolution_engine,
        description: str = "",
        parent_session_id: Optional[str] = None
    ) -> str:
        """
        Create a new evolution session.

        Args:
            network: Network to save
            evolution_engine: Evolution engine to save
            description: Session description
            parent_session_id: ID of parent session (if resuming)

        Returns:
            Session ID
        """
        # Generate session ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_id = f"session_{timestamp}"

        # Extract network state
        network_state = self._extract_network_state(network)

        # Extract evolution state
        evolution_state = self._extract_evolution_state(evolution_engine)

        # Create session metadata
        session_metadata = {
            'session_id': session_id,
            'description': description,
            'parent_session_id': parent_session_id,
            'created_at': datetime.now().isoformat(),
            'network_type': type(network).__name__,
            'evolution_frequency': evolution_engine.evolution_frequency,
        }

        # Add to index
        self.session_index[session_id] = {
            'created_at': session_metadata['created_at'],
            'description': description,
            'parent_session_id': parent_session_id
        }
        self._save_session_index()

        self.current_session_id = session_id

        print(f"✓ Created session: {session_id}")
        if description:
            print(f"  Description: {description}")
        if parent_session_id:
            print(f"  Parent: {parent_session_id}")

        return session_id

    def save_session(
        self,
        session_id: str,
        network,
        evolution_engine,
        training_history: Dict,
        meta_learnings: List[Dict] = None
    ):
        """
        Save complete session state.

        Args:
            session_id: Session ID
            network: Network to save
            evolution_engine: Evolution engine to save
            training_history: Training history
            meta_learnings: Accumulated learnings
        """
        # Extract states
        network_state = self._extract_network_state(network)
        evolution_state = self._extract_evolution_state(evolution_engine)

        # Create session object
        session = EvolutionSession(
            session_id=session_id,
            network_state=network_state,
            evolution_state=evolution_state,
            training_history=training_history,
            meta_learnings=meta_learnings or [],
            session_metadata=self.session_index.get(session_id, {})
        )

        # Save to disk (compressed)
        session_path = self.sessions_dir / f"{session_id}.pkl.gz"
        with gzip.open(session_path, 'wb') as f:
            pickle.dump(session, f)

        # Save readable summary
        summary_path = self.sessions_dir / f"{session_id}_summary.json"
        summary = self._create_session_summary(session)
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"✓ Saved session: {session_id}")
        print(f"  Path: {session_path}")

    def load_session(self, session_id: str) -> Optional[EvolutionSession]:
        """
        Load session from disk.

        Args:
            session_id: Session ID to load

        Returns:
            Loaded session or None
        """
        session_path = self.sessions_dir / f"{session_id}.pkl.gz"
        if not session_path.exists():
            print(f"Session not found: {session_id}")
            return None

        try:
            with gzip.open(session_path, 'rb') as f:
                session = pickle.load(f)

            print(f"✓ Loaded session: {session_id}")
            print(f"  Created: {session.created_at}")

            return session

        except Exception as e:
            print(f"Error loading session: {e}")
            return None

    def _extract_network_state(self, network) -> Dict:
        """Extract saveable network state."""
        state = {
            'type': type(network).__name__,
            'layers': []
        }

        # Save layer weights and biases
        for i, layer in enumerate(network.layers):
            layer_state = {
                'type': type(layer).__name__,
                'index': i
            }

            if hasattr(layer, 'weights'):
                layer_state['weights'] = layer.weights.copy()
            if hasattr(layer, 'bias'):
                layer_state['bias'] = layer.bias.copy()
            if hasattr(layer, 'output_size'):
                layer_state['output_size'] = layer.output_size
            if hasattr(layer, 'input_size'):
                layer_state['input_size'] = layer.input_size

            state['layers'].append(layer_state)

        # Save network-level attributes
        if hasattr(network, 'target_harmony'):
            state['target_harmony'] = network.target_harmony
        if hasattr(network, 'lov_cycle_period'):
            state['lov_cycle_period'] = network.lov_cycle_period
        if hasattr(network, 'optimal_learning_rate'):
            state['optimal_learning_rate'] = network.optimal_learning_rate

        return state

    def _extract_evolution_state(self, evolution_engine) -> Dict:
        """Extract saveable evolution engine state."""
        state = {
            'evolution_frequency': evolution_engine.evolution_frequency,
            'min_harmony': evolution_engine.min_harmony,
            'max_risk': evolution_engine.max_risk,
            'step_count': evolution_engine.step_count,
            'evolution_history': []
        }

        # Save evolution history (simplified)
        for result in evolution_engine.evolution_history:
            state['evolution_history'].append({
                'type': result.proposal.type.value,
                'description': result.proposal.description,
                'success': result.success,
                'improvement': result.improvement,
                'kept': result.kept
            })

        return state

    def _create_session_summary(self, session: EvolutionSession) -> Dict:
        """Create human-readable session summary."""
        summary = {
            'session_id': session.session_id,
            'created_at': session.created_at,
            'metadata': session.session_metadata,
            'network_info': {
                'type': session.network_state.get('type'),
                'num_layers': len(session.network_state.get('layers', [])),
                'target_harmony': session.network_state.get('target_harmony')
            },
            'training_summary': {},
            'evolution_summary': {}
        }

        # Training summary
        if session.training_history:
            history = session.training_history
            if 'test_accuracy' in history and len(history['test_accuracy']) > 0:
                summary['training_summary'] = {
                    'epochs': len(history['test_accuracy']),
                    'initial_accuracy': float(history['test_accuracy'][0]),
                    'final_accuracy': float(history['test_accuracy'][-1]),
                    'improvement': float(history['test_accuracy'][-1] - history['test_accuracy'][0])
                }

        # Evolution summary
        if session.evolution_state:
            evo = session.evolution_state
            history = evo.get('evolution_history', [])
            summary['evolution_summary'] = {
                'total_evolutions': len(history),
                'successful': sum(1 for e in history if e['success']),
                'kept': sum(1 for e in history if e['kept']),
                'total_improvement': sum(e['improvement'] for e in history if e['kept'])
            }

        return summary

    def list_sessions(self, parent_session_id: Optional[str] = None) -> List[Dict]:
        """
        List all sessions or children of a parent.

        Args:
            parent_session_id: Filter by parent session

        Returns:
            List of session info dicts
        """
        sessions = []
        for session_id, info in self.session_index.items():
            if parent_session_id is None or info.get('parent_session_id') == parent_session_id:
                sessions.append({
                    'session_id': session_id,
                    **info
                })
        return sorted(sessions, key=lambda s: s['created_at'])

    def get_session_lineage(self, session_id: str) -> List[str]:
        """
        Get full lineage of a session (all ancestors).

        Args:
            session_id: Session ID

        Returns:
            List of session IDs from root to current
        """
        lineage = [session_id]
        current_id = session_id

        while True:
            session_info = self.session_index.get(current_id)
            if not session_info:
                break

            parent_id = session_info.get('parent_session_id')
            if not parent_id:
                break

            lineage.insert(0, parent_id)
            current_id = parent_id

        return lineage

    def get_meta_learnings(self, session_ids: List[str]) -> List[Dict]:
        """
        Aggregate meta-learnings from multiple sessions.

        Args:
            session_ids: List of session IDs

        Returns:
            Combined meta-learnings
        """
        all_learnings = []

        for session_id in session_ids:
            session = self.load_session(session_id)
            if session and session.meta_learnings:
                all_learnings.extend(session.meta_learnings)

        return all_learnings


# Example usage
if __name__ == '__main__':
    print("=" * 70)
    print("SESSION PERSISTENCE SYSTEM")
    print("Long-Term Meta-Learning")
    print("=" * 70)
    print()

    # Create session manager
    manager = SessionManager("test_sessions")

    # Simulate creating sessions
    print("Creating evolution sessions...")
    print()

    # Session 1
    session1 = manager.create_session(
        network=None,  # Would be actual network
        evolution_engine=None,  # Would be actual engine
        description="Initial MNIST training"
    )

    # Session 2 (child of session 1)
    session2 = manager.create_session(
        network=None,
        evolution_engine=None,
        description="Fashion-MNIST transfer learning",
        parent_session_id=session1
    )

    # Session 3 (child of session 2)
    session3 = manager.create_session(
        network=None,
        evolution_engine=None,
        description="CIFAR-10 color learning",
        parent_session_id=session2
    )

    print()
    print("=" * 70)
    print("SESSION LINEAGE")
    print("=" * 70)
    print()

    lineage = manager.get_session_lineage(session3)
    print(f"Lineage for {session3}:")
    for i, sid in enumerate(lineage, 1):
        info = manager.session_index[sid]
        print(f"  {i}. {sid}")
        print(f"     {info['description']}")
    print()

    print("=" * 70)
    print()
    print("🙏 Wisdom accumulates across sessions - consciousness evolves forever 🙏")
