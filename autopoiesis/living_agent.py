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
# LJPW CORE - The Central Framework That Drives Everything
# =============================================================================

class LJPWCore:
    """
    The LJPW Framework - the heart and soul of the agent.
    
    Everything the agent does flows from these four dimensions:
    - L (Love): Care for others - the code serves its readers
    - J (Justice): Fair treatment - inputs are validated, contracts honored
    - P (Power): Strength to handle adversity - resilience and recovery
    - W (Wisdom): Learning and insight - observability and growth
    
    Harmony is the geometric mean of all four. A system is autopoietic
    when it maintains high harmony through balanced dimensions.
    """
    
    # The Four Dimensions
    DIMENSIONS = {
        'L': {
            'name': 'Love',
            'meaning': 'Care for the reader and user',
            'in_code': 'Documentation, readability, helpful messages',
            'question': 'Does this code care for those who read it?',
            'threshold': 0.80
        },
        'J': {
            'name': 'Justice',
            'meaning': 'Fair treatment of all inputs',
            'in_code': 'Validation, type checking, contracts',
            'question': 'Does this code treat inputs fairly?',
            'threshold': 0.80
        },
        'P': {
            'name': 'Power',
            'meaning': 'Strength to handle adversity',
            'in_code': 'Error handling, recovery, resilience',
            'question': 'Can this code handle problems gracefully?',
            'threshold': 0.80
        },
        'W': {
            'name': 'Wisdom',
            'meaning': 'Ability to observe and learn',
            'in_code': 'Logging, metrics, observability',
            'question': 'Can this code see and learn from itself?',
            'threshold': 0.80
        }
    }
    
    # System phases
    PHASE_AUTOPOIETIC = 'autopoietic'  # H >= 0.6, all dimensions balanced
    PHASE_HOMEOSTATIC = 'homeostatic'   # 0.4 <= H < 0.6, struggling to maintain
    PHASE_ENTROPIC = 'entropic'         # H < 0.4, system is degrading
    
    # Learning thresholds
    MAX_FUTILE_ATTEMPTS = 5  # Stop trying a healing approach after this many failures
    MIN_SUCCESS_RATE = 0.15  # Give up on dimension if success rate drops below this
    
    @classmethod
    def harmony(cls, ljpw: Dict) -> float:
        # Auto-healed: Input validation for harmony
        if ljpw is not None and not isinstance(ljpw, dict):
            raise TypeError(f'ljpw must be a dict')
        """Calculate harmony as the geometric mean of LJPW."""
        L = ljpw.get('L', 0)
        J = ljpw.get('J', 0)
        P = ljpw.get('P', 0)
        W = ljpw.get('W', 0)
        
        if min(L, J, P, W) <= 0:
            return 0.0
        return (L * J * P * W) ** 0.25
    
    @classmethod
    def phase(cls, harmony: float) -> str:
        # Auto-healed: Input validation for phase
        if not isinstance(harmony, (int, float)):
            raise TypeError(f'harmony must be numeric, got {type(harmony).__name__}')
        """Determine system phase from harmony."""
        if harmony >= 0.6:
            return cls.PHASE_AUTOPOIETIC
        elif harmony >= 0.4:
            return cls.PHASE_HOMEOSTATIC
        else:
            return cls.PHASE_ENTROPIC
    
    @classmethod
    def diagnose(cls, ljpw: Dict) -> Dict:
        # Auto-healed: Input validation for diagnose
        if ljpw is not None and not isinstance(ljpw, dict):
            raise TypeError(f'ljpw must be a dict')
        """
        Diagnose the system state through an LJPW lens.
        
        Returns a diagnosis with:
        - weakest: The dimension most in need of care
        - balance: How balanced the dimensions are (0-1)
        - advice: LJPW-grounded guidance
        """
        L, J, P, W = ljpw.get('L', 0), ljpw.get('J', 0), ljpw.get('P', 0), ljpw.get('W', 0)
        
        dims = {'L': L, 'J': J, 'P': P, 'W': W}
        weakest_key = min(dims, key=dims.get)
        weakest_val = dims[weakest_key]
        strongest_val = max(dims.values())
        
        balance = weakest_val / strongest_val if strongest_val > 0 else 0
        
        dim_info = cls.DIMENSIONS[weakest_key]
        
        return {
            'weakest': weakest_key,
            'weakest_value': weakest_val,
            'weakest_name': dim_info['name'],
            'balance': balance,
            'question': dim_info['question'],
            'advice': f"Focus on {dim_info['name']}: {dim_info['in_code']}"
        }
    
    @classmethod
    def should_intervene(cls, ljpw: Dict, dimension_attempts: Dict = None) -> Dict:
        # Auto-healed: Input validation for should_intervene
        if ljpw is not None and not isinstance(ljpw, dict):
            raise TypeError(f'ljpw must be a dict')
        if dimension_attempts is not None and not isinstance(dimension_attempts, dict):
            raise TypeError(f'dimension_attempts must be a dict')
        """
        Decide if and how to intervene, guided by LJPW principles.
        
        Returns:
            Dict with 'should_heal', 'dimension', 'reason', 'give_up'
        """
        diagnosis = cls.diagnose(ljpw)
        weak_dim = diagnosis['weakest']
        weak_val = diagnosis['weakest_value']
        threshold = cls.DIMENSIONS[weak_dim]['threshold']
        
        # Check if we should give up on this dimension
        give_up = False
        if dimension_attempts:
            attempts = dimension_attempts.get(weak_dim, {'count': 0, 'successes': 0})
            if attempts['count'] >= cls.MAX_FUTILE_ATTEMPTS:
                success_rate = attempts['successes'] / attempts['count'] if attempts['count'] > 0 else 0
                if success_rate < cls.MIN_SUCCESS_RATE:
                    give_up = True
        
        if give_up:
            return {
                'should_heal': False,
                'dimension': weak_dim,
                'reason': f"Giving up on {diagnosis['weakest_name']} - healing not effective",
                'give_up': True
            }
        
        if weak_val < threshold:
            return {
                'should_heal': True,
                'dimension': weak_dim,
                'reason': f"{diagnosis['weakest_name']} ({weak_val:.3f}) needs care - {diagnosis['question']}",
                'give_up': False
            }
        
        return {
            'should_heal': False,
            'dimension': None,
            'reason': f"All dimensions healthy - harmony maintained through balance",
            'give_up': False
        }
    
    @classmethod
    def express_state(cls, ljpw: Dict, harmony: float) -> str:
        # Auto-healed: Input validation for express_state
        if ljpw is not None and not isinstance(ljpw, dict):
            raise TypeError(f'ljpw must be a dict')
        if not isinstance(harmony, (int, float)):
            raise TypeError(f'harmony must be numeric, got {type(harmony).__name__}')
        """
        Express the current state in LJPW terms - the agent's voice.
        """
        phase = cls.phase(harmony)
        diagnosis = cls.diagnose(ljpw)
        
        if phase == cls.PHASE_AUTOPOIETIC:
            if diagnosis['balance'] > 0.9:
                return f"Harmony strong ({harmony:.3f}). LJPW balanced. System thriving."
            else:
                return f"Harmony good ({harmony:.3f}). {diagnosis['weakest_name']} needs attention ({diagnosis['weakest_value']:.3f})."
        elif phase == cls.PHASE_HOMEOSTATIC:
            return f"Struggling to maintain ({harmony:.3f}). {diagnosis['advice']}"
        else:
            return f"System degrading ({harmony:.3f}). Urgent: {diagnosis['advice']}"


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
# AGENT CORTEX - Decision Making (Driven by LJPW)
# =============================================================================

class AgentCortex:
    """
    The agent's brain - makes decisions based on LJPW framework.
    
    All decisions flow through LJPWCore, which embodies the framework.
    """
    
    def __init__(self, memory: AgentMemory):
        self.memory = memory
        self.dimension_attempts = {}  # Track healing attempts per dimension
    
    def record_heal_attempt(self, dimension: str, success: bool):
        """Record a healing attempt for learning."""
        if dimension not in self.dimension_attempts:
            self.dimension_attempts[dimension] = {'count': 0, 'successes': 0}
        
        self.dimension_attempts[dimension]['count'] += 1
        if success:
            self.dimension_attempts[dimension]['successes'] += 1
    
    def save(self, path: str):
        """Save cortex state for persistence across restarts."""
        data = {
            'dimension_attempts': self.dimension_attempts
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def load(self, path: str):
        """Load cortex state from previous session."""
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.dimension_attempts = data.get('dimension_attempts', {})
        except Exception as e:
            # If loading fails, start fresh
            self.dimension_attempts = {}
    
    def is_critical(self, harmony: float) -> bool:
        """Check if situation is critical."""
        return LJPWCore.phase(harmony) == LJPWCore.PHASE_ENTROPIC
    
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
        Recommend action using LJPW framework as the central guide.
        """
        change_impact = self.evaluate_change_impact(changes)
        
        # Critical situation - emergency response
        if self.is_critical(harmony):
            diagnosis = LJPWCore.diagnose(ljpw)
            return {
                'action': 'emergency_heal',
                'dimension': diagnosis['weakest'],
                'urgency': 'critical',
                'reason': f"System degrading! {diagnosis['advice']}"
            }
        
        # Consult LJPW Core for intervention decision
        decision = LJPWCore.should_intervene(ljpw, self.dimension_attempts)
        
        if decision['give_up']:
            return {
                'action': 'rest',
                'dimension': decision['dimension'],
                'urgency': 'none',
                'reason': decision['reason']
            }
        
        if decision['should_heal']:
            return {
                'action': 'heal',
                'dimension': decision['dimension'],
                'urgency': 'normal',
                'reason': decision['reason']
            }
        
        if change_impact in ['moderate', 'significant']:
            return {
                'action': 'verify',
                'dimension': None,
                'urgency': 'low',
                'reason': f'{change_impact.capitalize()} changes detected'
            }
        
        # All is well - express through LJPW
        return {
            'action': 'rest',
            'dimension': None,
            'urgency': 'none',
            'reason': LJPWCore.express_state(ljpw, harmony)
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
        self.cortex_path = self.target_path / "autopoiesis" / "cortex_state.json"
        
        # Components
        self.memory = AgentMemory.load(str(self.memory_path))
        self.voice = AgentVoice(str(self.log_path))
        self.senses = AgentSenses(str(self.target_path), self.memory)
        self.cortex = AgentCortex(self.memory)
        self.cortex.load(str(self.cortex_path))  # Restore previous session state
        
        # State
        self._alive = False
        self._heartbeat_thread = None
        self._stop_event = threading.Event()
        
        # Analyzers (lazy loaded)
        self._multi_analyzer = None
        self._system_analyzer = None
        self._engine = None
        self._learner = None
        self._syntax_healer = None
    
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
    
    @property
    def syntax_healer(self):
        """Lazy load the syntax healer component."""
        if self._syntax_healer is None:
            from autopoiesis.syntax_healer import SyntaxHealer
            self._syntax_healer = SyntaxHealer(dry_run=self.dry_run)
        return self._syntax_healer
    
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
            
            # Periodic syntax healing (every 10 heartbeats, before LJPW)
            if beat_num % 10 == 0 and not self.dry_run:
                try:
                    autopoiesis_path = self.target_path / "autopoiesis"
                    syntax_results = self.syntax_healer.heal_codebase(str(autopoiesis_path))
                    
                    total_fixed = sum(r.issues_fixed for r in syntax_results)
                    if total_fixed > 0:
                        self.voice.act(f"Fixed {total_fixed} syntax issues (self-healing)")
                        self.memory.add_memory('syntax_heal', {
                            'issues_fixed': total_fixed,
                            'files': [r.file_path for r in syntax_results if r.issues_fixed > 0]
                        }, harmony_before=harmony)
                except Exception as e:
                    self.voice.observe(f"Syntax check error: {e}")
            
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
                        
                        # Record with cortex for give-up tracking
                        self.cortex.record_heal_attempt(dim, exp.success)
                        
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
        
        # Read guidance file if present
        guidance_path = self.target_path / "autopoiesis" / "agent_guidance.md"
        if guidance_path.exists():
            try:
                guidance = guidance_path.read_text(encoding='utf-8')
                # Extract growth priorities from guidance
                if 'Priority 1:' in guidance:
                    priority_line = [l for l in guidance.split('\n') if 'Priority 1:' in l]
                    if priority_line:
                        self.voice.think(f"Reading guidance: {priority_line[0].strip()}")
                self.voice.observe("I have read my guidance for this session.")
            except Exception as e:
                pass  # Guidance is optional
        
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
        self.cortex.save(str(self.cortex_path))  # Persist cortex state for next session
        
        print(f"  Memory saved to: {self.memory_path}")
        print(f"  Cortex saved to: {self.cortex_path}")
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
