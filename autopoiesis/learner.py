"""
Agent Learner - Learning from Healing Outcomes
==============================================

Enables the autopoiesis agent to learn from its healing experiences:
- Track which heals actually improve harmony
- Remember what works for each file/pattern
- Adapt healing strategies based on success rates

This transforms the agent from a "healing machine" into a "learning organism."

Usage:
    learner = AgentLearner()
    
    # Record an experience
    learner.record_experience(
        file_path="app.js",
        dimension="L",
        harmony_before=0.3,
        harmony_after=0.8,
        strategy_used="add_jsdoc"
    )
    
    # Get insights
    insights = learner.get_insights()
    print(f"Best dimension to heal: {insights['best_dimension']}")
    
    # Get recommendation
    rec = learner.recommend_next_action("app.js")
    print(f"Recommended: {rec}")
"""

import os
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
import statistics


@dataclass
class HealingExperience:
    """A single healing experience record."""
    file_path: str
    dimension: str  # L, J, P, W
    harmony_before: float
    harmony_after: float
    timestamp: str
    strategy_used: str  # e.g., "add_jsdoc", "add_validation"
    
    @property
    def delta(self) -> float:
        """Change in harmony."""
        return self.harmony_after - self.harmony_before
    
    @property
    def success(self) -> bool:
        """Was this healing successful?"""
        return self.delta > 0
    
    @property
    def improvement_percent(self) -> float:
        """Percent improvement."""
        if self.harmony_before == 0:
            return self.harmony_after * 100
        return (self.delta / self.harmony_before) * 100


@dataclass
class LearningInsight:
    """Aggregated learning about a pattern."""
    pattern: str  # e.g., "dimension:L", "file:app.js", "strategy:add_jsdoc"
    total_attempts: int = 0
    successful_attempts: int = 0
    total_improvement: float = 0.0
    best_delta: float = 0.0
    worst_delta: float = 0.0
    
    @property
    def success_rate(self) -> float:
        """Success rate as 0.0 to 1.0."""
        if self.total_attempts == 0:
            return 0.0
        return self.successful_attempts / self.total_attempts
    
    @property
    def avg_improvement(self) -> float:
        """Average harmony improvement."""
        if self.total_attempts == 0:
            return 0.0
        return self.total_improvement / self.total_attempts


@dataclass
class LearnerState:
    """Persistent state for the learner."""
    experiences: List[Dict] = field(default_factory=list)
    dimension_priorities: List[str] = field(default_factory=lambda: ['L', 'J', 'P', 'W'])
    total_heals: int = 0
    total_successful_heals: int = 0
    creation_time: str = ""
    last_updated: str = ""


class AgentLearner:
    """
    The learning component of the autopoiesis agent.
    
    Tracks healing experiences, derives insights, and adapts strategy.
    """
    
    DEFAULT_PATH = "agent_learning.json"
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        Initialize the learner.
        
        Args:
            storage_path: Path to persist learning data
        """
        self.storage_path = storage_path or self.DEFAULT_PATH
        self.state = self._load_state()
        
        # Derived insights (computed on demand)
        self._insights_cache: Dict[str, LearningInsight] = {}
        self._insights_dirty = True
    
    def _load_state(self) -> LearnerState:
        """Load state from file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                state = LearnerState()
                for key, value in data.items():
                    if hasattr(state, key):
                        setattr(state, key, value)
                return state
            except Exception:
                pass
        
        state = LearnerState()
        state.creation_time = datetime.now().isoformat()
        return state
    
    def _save_state(self):
        """Save state to file."""
        self.state.last_updated = datetime.now().isoformat()
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.state), f, indent=2)
    
    def record_experience(self, 
                          file_path: str,
                          dimension: str,
                          harmony_before: float,
                          harmony_after: float,
                          strategy_used: str = "unknown") -> HealingExperience:
        """
        Record a healing experience.
        
        Args:
            file_path: File that was healed
            dimension: Dimension healed (L, J, P, W)
            harmony_before: Harmony before healing
            harmony_after: Harmony after healing
            strategy_used: What strategy was applied
            
        Returns:
            The recorded experience
        """
        exp = HealingExperience(
            file_path=file_path,
            dimension=dimension,
            harmony_before=harmony_before,
            harmony_after=harmony_after,
            timestamp=datetime.now().isoformat(),
            strategy_used=strategy_used
        )
        
        # Add to state
        self.state.experiences.append(asdict(exp))
        self.state.total_heals += 1
        if exp.success:
            self.state.total_successful_heals += 1
        
        # Mark insights as dirty
        self._insights_dirty = True
        
        # Limit experience history
        if len(self.state.experiences) > 1000:
            self.state.experiences = self.state.experiences[-500:]
        
        # Save
        self._save_state()
        
        return exp
    
    def _compute_insights(self):
        """Compute insights from experiences."""
        if not self._insights_dirty:
            return
        
        self._insights_cache = {}
        
        # Group by various patterns
        patterns = defaultdict(lambda: LearningInsight(pattern=""))
        
        for exp_dict in self.state.experiences:
            exp = HealingExperience(**exp_dict)
            delta = exp.delta
            success = exp.success
            
            # By dimension
            dim_key = f"dimension:{exp.dimension}"
            if dim_key not in patterns:
                patterns[dim_key] = LearningInsight(pattern=dim_key)
            patterns[dim_key].total_attempts += 1
            patterns[dim_key].total_improvement += delta
            patterns[dim_key].best_delta = max(patterns[dim_key].best_delta, delta)
            patterns[dim_key].worst_delta = min(patterns[dim_key].worst_delta, delta)
            if success:
                patterns[dim_key].successful_attempts += 1
            
            # By strategy
            strat_key = f"strategy:{exp.strategy_used}"
            if strat_key not in patterns:
                patterns[strat_key] = LearningInsight(pattern=strat_key)
            patterns[strat_key].total_attempts += 1
            patterns[strat_key].total_improvement += delta
            patterns[strat_key].best_delta = max(patterns[strat_key].best_delta, delta)
            patterns[strat_key].worst_delta = min(patterns[strat_key].worst_delta, delta)
            if success:
                patterns[strat_key].successful_attempts += 1
            
            # By file extension
            ext = Path(exp.file_path).suffix
            ext_key = f"extension:{ext}"
            if ext_key not in patterns:
                patterns[ext_key] = LearningInsight(pattern=ext_key)
            patterns[ext_key].total_attempts += 1
            patterns[ext_key].total_improvement += delta
            if success:
                patterns[ext_key].successful_attempts += 1
        
        self._insights_cache = dict(patterns)
        self._insights_dirty = False
    
    def get_insights(self) -> Dict:
        """
        Get aggregated insights from all experiences.
        
        Returns:
            Dict with insights about dimensions, strategies, etc.
        """
        self._compute_insights()
        
        # Extract dimension insights
        dimension_insights = {}
        for dim in ['L', 'J', 'P', 'W']:
            key = f"dimension:{dim}"
            if key in self._insights_cache:
                insight = self._insights_cache[key]
                dimension_insights[dim] = {
                    'success_rate': insight.success_rate,
                    'avg_improvement': insight.avg_improvement,
                    'attempts': insight.total_attempts,
                    'best_delta': insight.best_delta
                }
            else:
                dimension_insights[dim] = {
                    'success_rate': 0.0,
                    'avg_improvement': 0.0,
                    'attempts': 0,
                    'best_delta': 0.0
                }
        
        # Find best dimension
        best_dim = max(dimension_insights.keys(), 
                       key=lambda d: dimension_insights[d]['avg_improvement'])
        
        # Strategy insights
        strategy_insights = {}
        for key, insight in self._insights_cache.items():
            if key.startswith("strategy:"):
                strat = key.replace("strategy:", "")
                strategy_insights[strat] = {
                    'success_rate': insight.success_rate,
                    'avg_improvement': insight.avg_improvement,
                    'attempts': insight.total_attempts
                }
        
        # Find best strategy
        best_strategy = None
        if strategy_insights:
            best_strategy = max(strategy_insights.keys(),
                               key=lambda s: strategy_insights[s]['avg_improvement'])
        
        return {
            'total_experiences': len(self.state.experiences),
            'overall_success_rate': (self.state.total_successful_heals / 
                                    max(self.state.total_heals, 1)),
            'best_dimension': best_dim,
            'best_strategy': best_strategy,
            'dimension_insights': dimension_insights,
            'strategy_insights': strategy_insights,
            'current_priorities': self.state.dimension_priorities
        }
    
    def recommend_next_action(self, file_path: str) -> Dict:
        """
        Recommend the next healing action based on learning.
        
        Args:
            file_path: File to potentially heal
            
        Returns:
            Dict with 'dimension', 'strategy', 'confidence', 'reason'
        """
        insights = self.get_insights()
        dim_insights = insights['dimension_insights']
        
        # Find dimension with best improvement rate
        best_dim = max(dim_insights.keys(), 
                       key=lambda d: dim_insights[d]['avg_improvement'])
        
        # Get extension-specific insights
        ext = Path(file_path).suffix
        ext_key = f"extension:{ext}"
        
        # Calculate confidence based on sample size
        attempts = dim_insights[best_dim]['attempts']
        if attempts >= 20:
            confidence = 'high'
        elif attempts >= 5:
            confidence = 'medium'
        else:
            confidence = 'low'
        
        # Build reason
        success_rate = dim_insights[best_dim]['success_rate']
        avg_imp = dim_insights[best_dim]['avg_improvement']
        
        if attempts > 0:
            reason = (f"Dimension {best_dim} has {success_rate:.0%} success rate "
                     f"with avg improvement of {avg_imp:+.3f} over {attempts} attempts")
        else:
            reason = f"No data yet - starting with {best_dim} (default priority)"
        
        return {
            'dimension': best_dim,
            'strategy': insights.get('best_strategy'),
            'confidence': confidence,
            'reason': reason
        }
    
    def adapt_priorities(self) -> List[str]:
        """
        Adapt dimension priorities based on learning.
        
        Reorders dimensions by their average improvement.
        
        Returns:
            New priority order
        """
        insights = self.get_insights()
        dim_insights = insights['dimension_insights']
        
        # Sort by average improvement
        new_order = sorted(
            ['L', 'J', 'P', 'W'],
            key=lambda d: dim_insights[d]['avg_improvement'],
            reverse=True
        )
        
        self.state.dimension_priorities = new_order
        self._save_state()
        
        return new_order
    
    def get_summary(self) -> str:
        """Get a human-readable summary of learnings."""
        insights = self.get_insights()
        
        lines = [
            "=== Learning Summary ===",
            f"Total experiences: {insights['total_experiences']}",
            f"Overall success rate: {insights['overall_success_rate']:.0%}",
            "",
            "Dimension Performance:",
        ]
        
        for dim in ['L', 'J', 'P', 'W']:
            d = insights['dimension_insights'][dim]
            if d['attempts'] > 0:
                lines.append(
                    f"  {dim}: {d['success_rate']:.0%} success, "
                    f"avg +{d['avg_improvement']:.3f}, "
                    f"{d['attempts']} attempts"
                )
            else:
                lines.append(f"  {dim}: No data yet")
        
        lines.append("")
        lines.append(f"Best dimension: {insights['best_dimension']}")
        lines.append(f"Current priorities: {' -> '.join(insights['current_priorities'])}")
        
        return '\n'.join(lines)
    
    def reflect(self) -> str:
        """
        Generate a reflection on what has been learned.
        
        Returns:
            A first-person reflection from the agent's perspective
        """
        insights = self.get_insights()
        
        if insights['total_experiences'] == 0:
            return "I haven't healed anything yet. I have no experiences to learn from."
        
        lines = []
        
        # Overall reflection
        success_rate = insights['overall_success_rate']
        if success_rate >= 0.8:
            lines.append("I feel confident in my healing abilities.")
        elif success_rate >= 0.5:
            lines.append("I'm learning. Some of my heals work, some don't.")
        else:
            lines.append("I'm still struggling. Many of my heals don't improve harmony.")
        
        # Dimension reflection
        best_dim = insights['best_dimension']
        dim_names = {'L': 'Love', 'J': 'Justice', 'P': 'Power', 'W': 'Wisdom'}
        lines.append(f"I'm best at healing {dim_names[best_dim]} ({best_dim}).")
        
        # Strategy reflection
        if insights['best_strategy']:
            lines.append(f"My most effective strategy is: {insights['best_strategy']}")
        
        # Adaptation
        lines.append("")
        lines.append(f"Based on my experiences, I now prioritize: " +
                    " -> ".join(insights['current_priorities']))
        
        return '\n'.join(lines)


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_learner(storage_path: Optional[str] = None) -> AgentLearner:
    """Create a learner instance."""
    return AgentLearner(storage_path)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("""
+==============================================================================+
|                                                                              |
|   AGENT LEARNER - Learning from Healing Outcomes                             |
|                                                                              |
+==============================================================================+
    """)
    
    # Create learner with temp storage
    import tempfile
    temp_path = os.path.join(tempfile.gettempdir(), "test_learner.json")
    learner = AgentLearner(temp_path)
    
    print("  Simulating healing experiences...")
    print("-" * 60)
    
    # Simulate some experiences
    test_experiences = [
        # Love heals tend to work well
        ("app.js", "L", 0.1, 0.8, "add_jsdoc"),
        ("utils.js", "L", 0.2, 0.7, "add_jsdoc"),
        ("main.js", "L", 0.0, 0.6, "add_jsdoc"),
        
        # Justice heals are moderate
        ("app.js", "J", 0.3, 0.5, "add_validation"),
        ("api.js", "J", 0.2, 0.4, "add_validation"),
        
        # Power heals are mixed
        ("app.js", "P", 0.5, 0.6, "add_try_catch"),
        ("api.js", "P", 0.4, 0.3, "add_try_catch"),  # This one failed!
        
        # Wisdom heals work okay
        ("app.js", "W", 0.3, 0.5, "add_logging"),
        ("utils.js", "W", 0.2, 0.6, "add_logging"),
    ]
    
    for file_path, dim, before, after, strategy in test_experiences:
        exp = learner.record_experience(file_path, dim, before, after, strategy)
        status = "OK" if exp.success else "FAIL"
        print(f"  [{status}] {dim} on {file_path}: {before:.2f} -> {after:.2f} ({exp.delta:+.2f})")
    
    print()
    print("  Deriving insights...")
    print("-" * 60)
    
    insights = learner.get_insights()
    print(f"  Total experiences: {insights['total_experiences']}")
    print(f"  Overall success rate: {insights['overall_success_rate']:.0%}")
    print(f"  Best dimension: {insights['best_dimension']}")
    print(f"  Best strategy: {insights['best_strategy']}")
    
    print()
    print("  Dimension breakdown:")
    for dim in ['L', 'J', 'P', 'W']:
        d = insights['dimension_insights'][dim]
        if d['attempts'] > 0:
            print(f"    {dim}: {d['success_rate']:.0%} success, avg +{d['avg_improvement']:.3f}")
    
    print()
    print("  Adapting priorities...")
    new_order = learner.adapt_priorities()
    print(f"    New order: {' -> '.join(new_order)}")
    
    print()
    print("  Agent reflection:")
    print("-" * 60)
    reflection = learner.reflect()
    for line in reflection.split('\n'):
        print(f"    {line}")
    
    print()
    print("  Recommendation for 'test.js':")
    rec = learner.recommend_next_action("test.js")
    print(f"    Dimension: {rec['dimension']}")
    print(f"    Confidence: {rec['confidence']}")
    print(f"    Reason: {rec['reason']}")
    
    print()
    print(f"  Learning data saved to: {temp_path}")
