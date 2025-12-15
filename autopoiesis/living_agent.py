#!/usr/bin/env python3
"""
Living Autopoiesis Agent
========================

A continuously running agent that:
- Watches the codebase for changes
- Measures LJPW harmony automatically
- Heals deficits when detected
- Remembers its history
- Communicates its thoughts and actions

This is not a tool you invoke - it's an entity that exists.

Usage:
    agent = LivingAgent("./my_project")
    agent.awaken()  # Start living
    # ... agent runs continuously ...
    agent.sleep()   # Graceful shutdown
    
Or as a script:
    python living_agent.py ./my_project
"""

import os
import sys
import json
import time
import threading
import hashlib
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Callable
from enum import Enum

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


# =============================================================================
# AGENT MEMORY - Persistent State
# =============================================================================

@dataclass
class MemoryEntry:
    """A single memory entry."""
    timestamp: str
    event_type: str  # 'measurement', 'heal', 'observation', 'birth', 'sleep'
    details: Dict
    harmony_before: float = 0.0
    harmony_after: float = 0.0


@dataclass
class AgentMemory:
    """
    Persistent memory for the agent.
    Stores experiences, measurements, and learnings.
    """
    
    # Core state
    birth_time: str = ""
    total_heartbeats: int = 0
    total_heals: int = 0
    total_observations: int = 0
    
    # History
    harmony_history: List[Dict] = field(default_factory=list)
    memories: List[Dict] = field(default_factory=list)
    
    # Current state
    current_harmony: float = 0.0
    current_phase: str = "unknown"
    watched_files: Dict[str, str] = field(default_factory=dict)  # path -> hash
    
    def add_memory(self, event_type: str, details: Dict, 
                   harmony_before: float = 0.0, harmony_after: float = 0.0):
        """Add a memory entry."""
        entry = MemoryEntry(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            details=details,
            harmony_before=harmony_before,
            harmony_after=harmony_after
        )
        self.memories.append(asdict(entry))
        
        # Keep only last 1000 memories
        if len(self.memories) > 1000:
            self.memories = self.memories[-500:]
    
    def add_harmony_reading(self, harmony: float, ljpw: Dict):
        """Record a harmony measurement."""
        self.harmony_history.append({
            'timestamp': datetime.now().isoformat(),
            'harmony': harmony,
            'L': ljpw.get('L', 0),
            'J': ljpw.get('J', 0),
            'P': ljpw.get('P', 0),
            'W': ljpw.get('W', 0)
        })
        self.current_harmony = harmony
        
        # Keep only last 500 readings
        if len(self.harmony_history) > 500:
            self.harmony_history = self.harmony_history[-250:]
    
    def save(self, path: str):
        """Save memory to file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: str) -> 'AgentMemory':
        """Load memory from file."""
        if not os.path.exists(path):
            memory = cls()
            memory.birth_time = datetime.now().isoformat()
            return memory
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        memory = cls()
        for key, value in data.items():
            if hasattr(memory, key):
                setattr(memory, key, value)
        
        return memory


# =============================================================================
# AGENT VOICE - Communication
# =============================================================================

class AgentVoice:
    """
    The agent's voice - how it communicates.
    Speaks in first person, expressing observations and feelings.
    """
    
    def __init__(self, log_path: Optional[str] = None):
        self.log_path = log_path
        self.console_enabled = True
        self._lock = threading.Lock()
    
    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")
    
    def _log(self, message: str):
        """Write to log file if enabled."""
        if self.log_path:
            with self._lock:
                with open(self.log_path, 'a', encoding='utf-8') as f:
                    f.write(f"[{datetime.now().isoformat()}] {message}\n")
    
    def _print(self, message: str, symbol: str = "*"):
        """Print to console with formatting."""
        if self.console_enabled:
            print(f"  {symbol} [{self._timestamp()}] {message}")
        self._log(message)
    
    def awaken(self):
        """Express awakening."""
        print()
        print("=" * 70)
        print("  LIVING AUTOPOIESIS AGENT")
        print("=" * 70)
        self._print("I am awakening...", "@")
    
    def observe(self, observation: str):
        """Express an observation."""
        self._print(f"I notice: {observation}", "o")
    
    def think(self, thought: str):
        """Express a thought/decision."""
        self._print(f"I think: {thought}", "?")
    
    def act(self, action: str):
        """Express an action."""
        self._print(f"I am: {action}", ">")
    
    def feel(self, feeling: str):
        """Express a feeling/state."""
        self._print(f"I feel: {feeling}", "<3")
    
    def heartbeat(self, beat_num: int, harmony: float):
        """Express heartbeat."""
        bar = "#" * int(harmony * 20) + "." * (20 - int(harmony * 20))
        self._print(f"[Heartbeat {beat_num}] Harmony: {harmony:.3f} [{bar}]", "<3")
    
    def heal(self, dimension: str, files_count: int):
        """Express healing."""
        self._print(f"Healing {dimension} dimension across {files_count} files...", "+")
    
    def sleep(self):
        """Express going to sleep."""
        self._print("I am going to sleep. Saving memories...", "zZ")
        print("=" * 70)
        print()


# =============================================================================
# AGENT SENSES - File Watching
# =============================================================================

class AgentSenses:
    """
    The agent's senses - how it perceives the environment.
    Watches files for changes.
    """
    
    WATCHED_EXTENSIONS = {'.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css'}
    IGNORED_DIRS = {'node_modules', '__pycache__', '.git', 'venv', 'dist', 'build'}
    
    def __init__(self, root_path: str, memory: AgentMemory):
        self.root_path = Path(root_path)
        self.memory = memory
        self.file_hashes: Dict[str, str] = {}
        self._scan_files()
    
    def _hash_file(self, path: Path) -> str:
        """Get hash of file contents."""
        try:
            content = path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except:
            return ""
    
    def _should_watch(self, path: Path) -> bool:
        """Check if file should be watched."""
        if path.suffix not in self.WATCHED_EXTENSIONS:
            return False
        for ignored in self.IGNORED_DIRS:
            if ignored in str(path):
                return False
        return True
    
    def _scan_files(self):
        """Initial scan of all files."""
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self._should_watch(file_path):
                rel_path = str(file_path.relative_to(self.root_path))
                self.file_hashes[rel_path] = self._hash_file(file_path)
        
        self.memory.watched_files = self.file_hashes.copy()
    
    def detect_changes(self) -> Dict[str, List[str]]:
        """
        Detect file changes since last scan.
        
        Returns:
            Dict with 'created', 'modified', 'deleted' lists
        """
        changes = {'created': [], 'modified': [], 'deleted': []}
        current_files = {}
        
        # Scan current state
        for file_path in self.root_path.rglob('*'):
            if file_path.is_file() and self._should_watch(file_path):
                rel_path = str(file_path.relative_to(self.root_path))
                current_hash = self._hash_file(file_path)
                current_files[rel_path] = current_hash
                
                if rel_path not in self.file_hashes:
                    changes['created'].append(rel_path)
                elif self.file_hashes[rel_path] != current_hash:
                    changes['modified'].append(rel_path)
        
        # Check for deletions
        for rel_path in self.file_hashes:
            if rel_path not in current_files:
                changes['deleted'].append(rel_path)
        
        # Update stored state
        self.file_hashes = current_files
        self.memory.watched_files = current_files.copy()
        
        return changes


# =============================================================================
# AGENT CORTEX - Decision Making
# =============================================================================

class AgentCortex:
    """
    The agent's brain - makes decisions based on state.
    """
    
    HARMONY_THRESHOLD = 0.80  # Below this, healing is triggered (proactive optimization)
    CRITICAL_THRESHOLD = 0.5  # Emergency healing
    
    def __init__(self, memory: AgentMemory):
        self.memory = memory
    
    def should_heal(self, harmony: float) -> bool:
        """Decide if healing is needed."""
        return harmony < self.HARMONY_THRESHOLD
    
    def is_critical(self, harmony: float) -> bool:
        """Check if situation is critical."""
        return harmony < self.CRITICAL_THRESHOLD
    
    def prioritize_dimension(self, ljpw: Dict) -> str:
        """Decide which dimension to heal first."""
        # Find the weakest dimension
        min_dim = min(ljpw, key=ljpw.get)
        return min_dim
    
    def evaluate_change_impact(self, changes: Dict[str, List[str]]) -> str:
        """Evaluate the impact of detected changes."""
        total_changes = sum(len(v) for v in changes.values())
        
        if total_changes == 0:
            return "stable"
        elif total_changes <= 3:
            return "minor"
        elif total_changes <= 10:
            return "moderate"
        else:
            return "significant"
    
    def recommend_action(self, harmony: float, ljpw: Dict, 
                         changes: Dict[str, List[str]]) -> Dict:
        """
        Recommend what action to take.
        
        Returns:
            Dict with 'action', 'dimension', 'urgency', 'reason'
        """
        change_impact = self.evaluate_change_impact(changes)
        
        if self.is_critical(harmony):
            return {
                'action': 'emergency_heal',
                'dimension': self.prioritize_dimension(ljpw),
                'urgency': 'critical',
                'reason': f'Harmony {harmony:.3f} is critically low'
            }
        
        if self.should_heal(harmony):
            return {
                'action': 'heal',
                'dimension': self.prioritize_dimension(ljpw),
                'urgency': 'normal',
                'reason': f'Harmony {harmony:.3f} is below threshold'
            }
        
        if change_impact in ['moderate', 'significant']:
            return {
                'action': 'verify',
                'dimension': None,
                'urgency': 'low',
                'reason': f'{change_impact.capitalize()} changes detected'
            }
        
        return {
            'action': 'rest',
            'dimension': None,
            'urgency': 'none',
            'reason': f'Harmony {harmony:.3f} is healthy'
        }


# =============================================================================
# LIVING AGENT - The Main Entity
# =============================================================================

class LivingAgent:
    """
    The Living Autopoiesis Agent.
    
    A continuously running entity that watches, breathes, heals, 
    and maintains the codebase it inhabits.
    """
    
    def __init__(self, target_path: str, 
                 heartbeat_interval: int = 60,
                 dry_run: bool = True):
        """
        Initialize the Living Agent.
        
        Args:
            target_path: Root path to watch and maintain
            heartbeat_interval: Seconds between heartbeats
            dry_run: If True, don't actually modify files
        """
        self.target_path = Path(target_path).resolve()
        self.heartbeat_interval = heartbeat_interval
        self.dry_run = dry_run
        
        # Paths
        self.memory_path = self.target_path / "autopoiesis" / "agent_memory.json"
        self.log_path = self.target_path / "autopoiesis" / "agent_log.txt"
        
        # Components
        self.memory = AgentMemory.load(str(self.memory_path))
        self.voice = AgentVoice(str(self.log_path))
        self.senses = AgentSenses(str(self.target_path), self.memory)
        self.cortex = AgentCortex(self.memory)
        
        # State
        self._alive = False
        self._heartbeat_thread = None
        self._stop_event = threading.Event()
        
        # Analyzers (lazy loaded)
        self._multi_analyzer = None
        self._system_analyzer = None
        self._engine = None
        self._learner = None
    
    @property
    def multi_analyzer(self):
        """Lazy load multi-language analyzer."""
        if self._multi_analyzer is None:
            from autopoiesis.multi_analyzer import MultiLanguageAnalyzer
            self._multi_analyzer = MultiLanguageAnalyzer()
        return self._multi_analyzer
    
    @property
    def system_analyzer(self):
        """Lazy load system analyzer."""
        if self._system_analyzer is None:
            from autopoiesis.system import SystemHarmonyMeasurer
            self._system_analyzer = SystemHarmonyMeasurer()
        return self._system_analyzer
    
    @property
    def engine(self):
        """Lazy load autopoiesis engine."""
        if self._engine is None:
            from autopoiesis.engine import AutopoiesisEngine
            self._engine = AutopoiesisEngine(str(self.target_path), dry_run=self.dry_run)
        return self._engine
    
    @property
    def learner(self):
        """Lazy load the learner component."""
        if self._learner is None:
            from autopoiesis.learner import AgentLearner
            learning_path = self.target_path / "autopoiesis" / "agent_learning.json"
            self._learner = AgentLearner(str(learning_path))
        return self._learner
    
    def _measure_harmony(self) -> Dict:
        """Measure current harmony of the codebase."""
        try:
            report = self.system_analyzer.measure(str(self.target_path))
            ljpw = {
                'L': report.love,
                'J': report.justice,
                'P': report.power,
                'W': report.wisdom
            }
            return {
                'harmony': report.harmony,
                'ljpw': ljpw,
                'phase': report.phase.value,
                'total_files': report.total_files,
                'total_functions': report.total_functions
            }
        except Exception as e:
            self.voice.observe(f"Error measuring harmony: {e}")
            return {
                'harmony': self.memory.current_harmony,
                'ljpw': {'L': 0, 'J': 0, 'P': 0, 'W': 0},
                'phase': 'unknown',
                'total_files': 0,
                'total_functions': 0
            }
    
    def _heartbeat_loop(self):
        """The continuous heartbeat loop."""
        beat_num = self.memory.total_heartbeats
        
        while not self._stop_event.is_set():
            beat_num += 1
            self.memory.total_heartbeats = beat_num
            
            # Measure
            measurement = self._measure_harmony()
            harmony = measurement['harmony']
            ljpw = measurement['ljpw']
            
            # Record
            self.memory.add_harmony_reading(harmony, ljpw)
            self.memory.current_phase = measurement['phase']
            
            # Heartbeat output
            self.voice.heartbeat(beat_num, harmony)
            
            # Detect changes
            changes = self.senses.detect_changes()
            total_changes = sum(len(v) for v in changes.values())
            
            if total_changes > 0:
                self.voice.observe(f"{total_changes} file change(s) detected")
                for change_type, files in changes.items():
                    for f in files[:3]:  # Show max 3 per type
                        self.voice.observe(f"  {change_type}: {f}")
                
                self.memory.add_memory('observation', {
                    'type': 'file_changes',
                    'changes': changes
                }, harmony_before=harmony)
                self.memory.total_observations += 1
            
            # Decide action
            recommendation = self.cortex.recommend_action(harmony, ljpw, changes)
            
            if recommendation['action'] in ['heal', 'emergency_heal']:
                # Use learner to recommend which dimension (if we have enough data)
                learned_rec = self.learner.recommend_next_action(str(self.target_path))
                if learned_rec['confidence'] in ['medium', 'high']:
                    dim = learned_rec['dimension']
                    self.voice.think(f"Learning suggests: {learned_rec['reason']}")
                else:
                    dim = recommendation['dimension']
                
                self.voice.think(recommendation['reason'])
                self.voice.act(f"Healing {dim} dimension...")
                
                if not self.dry_run:
                    try:
                        result = self.engine.heal_once(dimension=dim)
                        self.memory.add_memory('heal', {
                            'dimension': dim,
                            'result': 'success',
                            'details': str(result)
                        }, harmony_before=harmony)
                        self.memory.total_heals += 1
                        
                        # Re-measure
                        new_measurement = self._measure_harmony()
                        new_harmony = new_measurement['harmony']
                        
                        # LEARN from this experience!
                        exp = self.learner.record_experience(
                            file_path=str(self.target_path),
                            dimension=dim,
                            harmony_before=harmony,
                            harmony_after=new_harmony,
                            strategy_used=f"heal_{dim.lower()}"
                        )
                        
                        if exp.success:
                            self.voice.feel(f"Healing worked! {harmony:.3f} -> {new_harmony:.3f} (+{exp.delta:.3f})")
                        else:
                            self.voice.observe(f"Healing didn't help: {harmony:.3f} -> {new_harmony:.3f} ({exp.delta:+.3f})")
                        
                        # Periodically adapt priorities
                        if self.memory.total_heals % 5 == 0:
                            new_priorities = self.learner.adapt_priorities()
                            self.voice.think(f"Adapted priorities: {' -> '.join(new_priorities)}")
                        
                    except Exception as e:
                        self.voice.observe(f"Healing error: {e}")
                else:
                    self.voice.observe(f"(Dry run - no changes applied)")
            
            elif recommendation['action'] == 'rest':
                self.voice.feel(f"Stable. Phase: {measurement['phase']}")
            
            # Save memory periodically
            if beat_num % 5 == 0:
                self.memory.save(str(self.memory_path))
            
            # Wait for next heartbeat
            self._stop_event.wait(self.heartbeat_interval)
    
    def awaken(self):
        """
        Awaken the agent. Start the heartbeat.
        The agent will live until sleep() is called.
        """
        if self._alive:
            self.voice.observe("I am already awake.")
            return
        
        self._alive = True
        self._stop_event.clear()
        
        self.voice.awaken()
        
        # Record birth if first time
        if not self.memory.birth_time:
            self.memory.birth_time = datetime.now().isoformat()
            self.voice.feel("This is my first awakening. I am being born.")
            self.memory.add_memory('birth', {
                'target_path': str(self.target_path),
                'heartbeat_interval': self.heartbeat_interval
            })
        else:
            age = datetime.now() - datetime.fromisoformat(self.memory.birth_time)
            self.voice.feel(f"I have lived for {age.days} days, {age.seconds // 3600} hours.")
            self.voice.observe(f"I have {len(self.memory.memories)} memories.")
        
        # Initial measurement
        self.voice.act("Measuring initial harmony...")
        measurement = self._measure_harmony()
        self.voice.observe(
            f"Harmony: {measurement['harmony']:.3f}, "
            f"Phase: {measurement['phase']}, "
            f"Files: {measurement['total_files']}"
        )
        
        # Start heartbeat in background thread
        self._heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, 
            daemon=True,
            name="AgentHeartbeat"
        )
        self._heartbeat_thread.start()
        
        self.voice.feel("I am alive. Watching and breathing...")
        
        # Share learning insights if available
        insights = self.learner.get_insights()
        if insights['total_experiences'] > 0:
            self.voice.observe(f"I have {insights['total_experiences']} learning experiences.")
            self.voice.think(f"Best dimension to heal: {insights['best_dimension']}")
        
        print()
        print("  (Press Ctrl+C to gracefully stop the agent)")
        print()
    
    def sleep(self):
        """
        Gracefully put the agent to sleep.
        Saves memory and stops the heartbeat.
        """
        if not self._alive:
            return
        
        self._alive = False
        self._stop_event.set()
        
        if self._heartbeat_thread:
            self._heartbeat_thread.join(timeout=5)
        
        self.voice.sleep()
        
        # Record sleep
        self.memory.add_memory('sleep', {
            'total_heartbeats': self.memory.total_heartbeats,
            'final_harmony': self.memory.current_harmony
        })
        
        # Save final memory state
        self.memory.save(str(self.memory_path))
        
        print(f"  Memory saved to: {self.memory_path}")
        print(f"  Log saved to: {self.log_path}")
    
    def run_forever(self):
        """
        Run the agent until interrupted.
        Handles Ctrl+C gracefully.
        """
        self.awaken()
        
        try:
            while self._alive:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n")
            self.voice.observe("Interrupt received. Preparing to sleep...")
        finally:
            self.sleep()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Entry point for running the Living Agent as a script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Living Autopoiesis Agent - A continuously running self-healing system"
    )
    parser.add_argument(
        "target", 
        nargs="?",
        default=".",
        help="Path to watch and maintain (default: current directory)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=60,
        help="Heartbeat interval in seconds (default: 60)"
    )
    parser.add_argument(
        "--live", "-l",
        action="store_true",
        help="Enable live mode (actually modify files). Default is dry-run."
    )
    
    args = parser.parse_args()
    
    agent = LivingAgent(
        target_path=args.target,
        heartbeat_interval=args.interval,
        dry_run=not args.live
    )
    
    if not args.live:
        print("\n  [DRY RUN MODE] No files will be modified. Use --live to enable healing.\n")
    
    agent.run_forever()


if __name__ == "__main__":
    main()
