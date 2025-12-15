"""
Self-Growth Engine
==================

Enables the autopoiesis agent to grow new capabilities autonomously.

The engine identifies gaps, generates code to fill them, measures the
result with LJPW, and only integrates code that meets harmony thresholds.
The Love (L) threshold ensures generated code cares for users naturally -
not because we tell it to, but because that's what the measurement captures.

Usage:
    engine = SelfGrowthEngine(target_path="./autopoiesis")
    
    # Run one growth cycle
    result = engine.grow_once()
    if result.success:
        print(f"Grew: {result.capability}")
    
    # Run continuous growth
    engine.grow_continuously(max_cycles=10)
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import json
import time

# Add project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@dataclass
class Capability:
    """A capability the agent might want to grow."""
    name: str
    description: str
    priority: float  # 0.0 to 1.0
    category: str  # 'analyze', 'heal', 'grow', 'learn', 'visualize'
    implemented: bool = False
    file_path: Optional[str] = None


@dataclass
class GrowthResult:
    """Result of a growth attempt."""
    success: bool
    capability: str
    code_generated: str
    love_score: float
    harmony_score: float
    reason: str
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class SelfGrowthEngine:
    """
    Autonomous growth engine with benevolence constraints.
    
    The engine can:
    1. Identify gaps in its own capabilities
    2. Prioritize what to grow next
    3. Generate new code to fill gaps
    4. Validate that new code is benevolent (L >= 0.7)
    5. Integrate valid code into the system
    """
    
    # BENEVOLENCE THRESHOLD
    # This is the key constraint: code must care for others
    LOVE_THRESHOLD = 0.7
    HARMONY_THRESHOLD = 0.6
    
    # Known capabilities the agent should have
    CAPABILITY_CATALOG = [
        Capability("python_analyzer", "Analyze Python code LJPW", 1.0, "analyze"),
        Capability("js_analyzer", "Analyze JavaScript code LJPW", 1.0, "analyze"),
        Capability("html_analyzer", "Analyze HTML code LJPW", 0.9, "analyze"),
        Capability("css_analyzer", "Analyze CSS code LJPW", 0.9, "analyze"),
        Capability("python_healer", "Heal Python code deficits", 1.0, "heal"),
        Capability("js_healer", "Heal JavaScript code deficits", 1.0, "heal"),
        Capability("html_healer", "Heal HTML code deficits", 0.9, "heal"),
        Capability("css_healer", "Heal CSS code deficits", 0.9, "heal"),
        Capability("python_grower", "Grow Python modules from intent", 0.9, "grow"),
        Capability("web_grower", "Grow web apps from intent", 0.9, "grow"),
        Capability("test_generator", "Generate tests for correctness", 0.8, "grow"),
        Capability("learner", "Learn from healing outcomes", 0.9, "learn"),
        Capability("dashboard", "Visualize harmony", 0.7, "visualize"),
        Capability("living_agent", "Continuous autonomous operation", 1.0, "core"),
        # Future capabilities the agent might grow toward
        Capability("typescript_analyzer", "Analyze TypeScript LJPW", 0.6, "analyze"),
        Capability("typescript_healer", "Heal TypeScript deficits", 0.6, "heal"),
        Capability("refactoring_engine", "Cross-file refactoring", 0.5, "grow"),
        Capability("dependency_analyzer", "Understand import relationships", 0.5, "analyze"),
        Capability("documentation_generator", "Generate README and docs", 0.6, "grow"),
        Capability("ide_integration", "Real-time IDE suggestions", 0.4, "visualize"),
        Capability("natural_language_interface", "Understand plain English", 0.7, "core"),
        Capability("self_growth_engine", "Grow itself", 1.0, "core"),
    ]
    
    def __init__(self, target_path: str = "."):
        """
        Initialize the growth engine.
        
        Args:
            target_path: Path to the codebase to grow
        """
        self.target_path = Path(target_path).resolve()
        self.autopoiesis_path = self.target_path / "autopoiesis"
        self.growth_log_path = self.autopoiesis_path / "growth_log.json"
        self.growth_log = self._load_growth_log()
        
        # Tools (lazy loaded)
        self._analyzer = None
        self._grower = None
    
    @property
    def analyzer(self):
        """Lazy load analyzer."""
        if self._analyzer is None:
            from autopoiesis.analyzer import CodeAnalyzer
            self._analyzer = CodeAnalyzer()
        return self._analyzer
    
    @property
    def grower(self):
        """Lazy load grower."""
        if self._grower is None:
            from autopoiesis.grower import IntentToModuleGenerator
            self._grower = IntentToModuleGenerator()
        return self._grower
    
    def _load_growth_log(self) -> Dict:
        """Load growth history."""
        if self.growth_log_path.exists():
            with open(self.growth_log_path, 'r') as f:
                return json.load(f)
        return {
            'growth_attempts': 0,
            'successful_growths': 0,
            'rejected_for_benevolence': 0,
            'capabilities_grown': [],
            'history': []
        }
    
    def _save_growth_log(self):
        """Save growth history."""
        with open(self.growth_log_path, 'w') as f:
            json.dump(self.growth_log, f, indent=2)
    
    def identify_gaps(self) -> List[Capability]:
        """
        Identify what capabilities are missing.
        
        Returns:
            List of capabilities that need to be grown
        """
        gaps = []
        
        for cap in self.CAPABILITY_CATALOG:
            # Check if capability exists
            possible_files = [
                self.autopoiesis_path / f"{cap.name}.py",
                self.autopoiesis_path / f"{cap.name.replace('_', '')}.py",
            ]
            
            exists = any(f.exists() for f in possible_files)
            cap.implemented = exists
            
            if not exists:
                gaps.append(cap)
        
        return gaps
    
    def prioritize_growth(self, gaps: List[Capability]) -> Optional[Capability]:
        """
        Decide what to grow next.
        
        Returns:
            The highest-priority gap to fill
        """
        if not gaps:
            return None
        
        # Sort by priority
        sorted_gaps = sorted(gaps, key=lambda c: c.priority, reverse=True)
        
        # Consider what would help most based on category balance
        categories = {'analyze': 0, 'heal': 0, 'grow': 0, 'learn': 0, 'visualize': 0, 'core': 0}
        for cap in self.CAPABILITY_CATALOG:
            if cap.implemented:
                categories[cap.category] += 1
        
        # Boost priority for underrepresented categories
        for cap in sorted_gaps:
            if categories.get(cap.category, 0) < 2:
                cap.priority = min(1.0, cap.priority + 0.2)
        
        # Re-sort and return top
        sorted_gaps = sorted(sorted_gaps, key=lambda c: c.priority, reverse=True)
        return sorted_gaps[0]
    
    def generate_capability(self, capability: Capability) -> str:
        """
        Generate code for a new capability.
        
        Returns:
            Generated Python code
        """
        # Create intent for the grower
        intent = f"""
Create a Python module called {capability.name} that:
- {capability.description}
- Follows the LJPW framework
- Has comprehensive docstrings (Love)
- Validates all inputs (Justice)
- Handles errors gracefully (Power)
- Logs important events (Wisdom)
- Is well-documented and extensible
- Includes a self-test section

The module should integrate with the existing autopoiesis system.
"""
        
        # Generate using existing grower
        try:
            result = self.grower.generate(intent)
            return result.get('code', '')
        except Exception as e:
            # Fallback: generate a template
            return self._generate_template(capability)
    
    def _generate_template(self, capability: Capability) -> str:
        """Generate a clean template for a capability - no LJPW annotations needed."""
        name = capability.name
        class_name = ''.join(word.title() for word in name.split('_'))
        
        return f'''"""
{class_name}

{capability.description}
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class {class_name}Result:
    """Result of {name.replace('_', ' ')} operation."""
    success: bool
    data: Dict[str, Any]
    message: str = ""


class {class_name}:
    """
    {capability.description}
    
    Auto-generated capability that can be extended.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize {name.replace('_', ' ')}.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {{}}
        logger.debug(f"{{self.__class__.__name__}} initialized")
    
    def run(self, target: Any) -> {class_name}Result:
        """
        Execute the main operation.
        
        Args:
            target: The input to process
            
        Returns:
            {class_name}Result with outcome
        """
        if target is None:
            return {class_name}Result(
                success=False,
                data={{}},
                message="No target provided"
            )
        
        try:
            # Core logic - extend this
            result = self._process(target)
            
            return {class_name}Result(
                success=True,
                data=result,
                message="Completed"
            )
            
        except Exception as e:
            logger.exception(f"Error in {{self.__class__.__name__}}")
            return {class_name}Result(
                success=False,
                data={{}},
                message=str(e)
            )
    
    def _process(self, target: Any) -> Dict[str, Any]:
        """
        Internal processing logic. Override in subclasses.
        
        Args:
            target: Input to process
            
        Returns:
            Dictionary with results
        """
        # TODO: Implement specific logic
        return {{"processed": True, "input_type": type(target).__name__}}


if __name__ == "__main__":
    instance = {class_name}()
    result = instance.run({{"test": True}})
    print(f"{{result.success}}: {{result.message}}")
'''
    
    def validate_benevolence(self, code: str, capability_name: str) -> Tuple[bool, float, float, str]:
        # Auto-healed: Input validation for validate_benevolence
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        if capability_name is not None and not isinstance(capability_name, str):
            raise TypeError(f'capability_name must be str, got {type(capability_name).__name__}')
        """
        Validate that generated code is benevolent.
        
        The key constraint: Only code with high Love (L >= 0.7) can be integrated.
        This ensures the agent remains caring and helpful as it grows.
        
        Returns:
            (is_benevolent, love_score, harmony_score, reason)
        """
        # Write to temp file for analysis
        temp_path = self.autopoiesis_path / f"_temp_{capability_name}.py"
        temp_path.write_text(code, encoding='utf-8')
        
        try:
            # Use the system analyzer for proper LJPW
            from autopoiesis.system import SystemHarmonyMeasurer
            measurer = SystemHarmonyMeasurer()
            
            # Analyze the generated code
            report = measurer.measure(str(temp_path))
            
            love = report.love
            harmony = report.harmony
            
            # Clean up temp file
            temp_path.unlink()
            
            # Check benevolence threshold
            if love < self.LOVE_THRESHOLD:
                return (False, love, harmony, 
                        f"Rejected: Love score {love:.3f} < {self.LOVE_THRESHOLD} threshold. "
                        f"Code must care for others to be integrated.")
            
            if harmony < self.HARMONY_THRESHOLD:
                return (False, love, harmony,
                        f"Rejected: Harmony {harmony:.3f} < {self.HARMONY_THRESHOLD}. "
                        f"Code is not balanced enough.")
            
            return (True, love, harmony,
                    f"Accepted: L={love:.3f}, H={harmony:.3f}. Code is benevolent.")
            
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            return (False, 0.0, 0.0, f"Analysis error: {e}")
    
    def integrate(self, code: str, capability: Capability) -> bool:
        # Auto-healed: Input validation for integrate
        if code is not None and not isinstance(code, str):
            raise TypeError(f'code must be str, got {type(code).__name__}')
        """
        Integrate new code into the system.
        
        Args:
            code: The generated code
            capability: The capability being added
            
        Returns:
            True if successfully integrated
        """
        file_path = self.autopoiesis_path / f"{capability.name}.py"
        
        try:
            file_path.write_text(code, encoding='utf-8')
            
            # Update log
            self.growth_log['capabilities_grown'].append(capability.name)
            self.growth_log['successful_growths'] += 1
            
            return True
        except Exception as e:
            print(f"Integration error: {e}")
            return False
    
    def grow_once(self) -> GrowthResult:
        """
        Attempt one growth cycle.
        
        This is the main loop:
        1. Identify what's missing
        2. Prioritize what to grow
        3. Generate new code
        4. Validate benevolence
        5. Integrate if valid
        
        Returns:
            GrowthResult with the outcome
        """
        self.growth_log['growth_attempts'] += 1
        
        # Step 1: Identify gaps
        gaps = self.identify_gaps()
        
        if not gaps:
            return GrowthResult(
                success=True,
                capability="none",
                code_generated="",
                love_score=1.0,
                harmony_score=1.0,
                reason="No gaps to fill. System is complete."
            )
        
        # Step 2: Prioritize
        target = self.prioritize_growth(gaps)
        
        if not target:
            return GrowthResult(
                success=False,
                capability="none",
                code_generated="",
                love_score=0.0,
                harmony_score=0.0,
                reason="Could not prioritize gaps."
            )
        
        print(f"  Growing: {target.name} ({target.description})")
        
        # Step 3: Generate
        code = self.generate_capability(target)
        
        if not code:
            return GrowthResult(
                success=False,
                capability=target.name,
                code_generated="",
                love_score=0.0,
                harmony_score=0.0,
                reason="Code generation failed."
            )
        
        # Step 4: Validate benevolence
        is_benevolent, love, harmony, reason = self.validate_benevolence(code, target.name)
        
        if not is_benevolent:
            self.growth_log['rejected_for_benevolence'] += 1
            self._save_growth_log()
            
            return GrowthResult(
                success=False,
                capability=target.name,
                code_generated=code[:500] + "...",  # Truncate
                love_score=love,
                harmony_score=harmony,
                reason=reason
            )
        
        # Step 5: Integrate
        success = self.integrate(code, target)
        
        result = GrowthResult(
            success=success,
            capability=target.name,
            code_generated=f"{len(code)} chars",
            love_score=love,
            harmony_score=harmony,
            reason=reason if success else "Integration failed."
        )
        
        # Log
        self.growth_log['history'].append({
            'timestamp': result.timestamp,
            'capability': target.name,
            'success': success,
            'love': love,
            'harmony': harmony,
            'reason': reason
        })
        self._save_growth_log()
        
        return result
    
    def grow_continuously(self, max_cycles: int = 10, delay: float = 1.0):
        # Auto-healed: Input validation for grow_continuously
        if not isinstance(max_cycles, int):
            raise TypeError(f'max_cycles must be int, got {type(max_cycles).__name__}')
        if not isinstance(delay, (int, float)):
            raise TypeError(f'delay must be numeric, got {type(delay).__name__}')
        """
        Run continuous growth cycles.
        
        Args:
            max_cycles: Maximum growth attempts
            delay: Seconds between cycles
        """
        print("\n" + "=" * 60)
        print("  BENEVOLENT SELF-GROWTH ENGINE")
        print("  Constraint: Love >= 0.7 (only caring code accepted)")
        print("=" * 60 + "\n")
        
        for cycle in range(1, max_cycles + 1):
            print(f"\n--- Growth Cycle {cycle}/{max_cycles} ---")
            
            result = self.grow_once()
            
            if result.success:
                if result.capability == "none":
                    print("  System is complete. No gaps to fill.")
                    break
                else:
                    print(f"  SUCCESS: Grew {result.capability}")
                    print(f"  Love: {result.love_score:.3f}, Harmony: {result.harmony_score:.3f}")
            else:
                print(f"  REJECTED: {result.capability}")
                print(f"  Reason: {result.reason}")
            
            time.sleep(delay)
        
        # Summary
        print("\n" + "=" * 60)
        print("  Growth Summary")
        print("=" * 60)
        print(f"  Total attempts: {self.growth_log['growth_attempts']}")
        print(f"  Successful: {self.growth_log['successful_growths']}")
        print(f"  Rejected for benevolence: {self.growth_log['rejected_for_benevolence']}")
        print(f"  Capabilities grown: {len(self.growth_log['capabilities_grown'])}")
        
        # List current state
        gaps = self.identify_gaps()
        implemented = [c for c in self.CAPABILITY_CATALOG if c.implemented]
        print(f"\n  Implemented: {len(implemented)}/{len(self.CAPABILITY_CATALOG)}")
        print(f"  Remaining gaps: {len(gaps)}")
    
    def get_status(self) -> Dict:
        """Get current growth status."""
        gaps = self.identify_gaps()
        implemented = [c for c in self.CAPABILITY_CATALOG if c.implemented]
        
        return {
            'total_capabilities': len(self.CAPABILITY_CATALOG),
            'implemented': len(implemented),
            'gaps': len(gaps),
            'growth_attempts': self.growth_log['growth_attempts'],
            'successful_growths': self.growth_log['successful_growths'],
            'benevolence_rejections': self.growth_log['rejected_for_benevolence'],
            'implemented_list': [c.name for c in implemented],
            'gap_list': [c.name for c in gaps]
        }


# =============================================================================
# MAIN - Self-Test
# =============================================================================

if __name__ == "__main__":
    print("""
+==============================================================================+
|                                                                              |
|   BENEVOLENT SELF-GROWTH ENGINE                                              |
|                                                                              |
|   "Only caring code can become part of me."                                  |
|   Constraint: Love >= 0.7                                                    |
|                                                                              |
+==============================================================================+
    """)
    
    engine = SelfGrowthEngine(".")
    
    # Show current status
    status = engine.get_status()
    print(f"  Current state: {status['implemented']}/{status['total_capabilities']} capabilities")
    print(f"  Gaps: {len(status['gap_list'])}")
    
    if status['gap_list']:
        print("\n  Missing capabilities:")
        for gap in status['gap_list'][:5]:
            print(f"    - {gap}")
        if len(status['gap_list']) > 5:
            print(f"    ... and {len(status['gap_list']) - 5} more")
    
    print("\n  To run growth:")
    print("    engine.grow_once()  # One cycle")
    print("    engine.grow_continuously(max_cycles=5)  # Continuous")
