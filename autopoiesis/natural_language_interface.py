"""
Natural Language Interface

Enables the autopoiesis system to understand plain English commands.

Examples:
    interface = NaturalLanguageInterface()
    
    # Parse intent
    intent = interface.parse("grow a calculator app")
    # -> Intent(action="grow", target="calculator app", params={})
    
    # Execute
    result = interface.execute("measure this project")
    # -> Runs the analyzer and returns results
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Intent:
    """Parsed intent from natural language."""
    action: str  # 'measure', 'heal', 'grow', 'status', 'help'
    target: Optional[str] = None
    params: Dict[str, Any] = None
    confidence: float = 1.0
    raw_text: str = ""
    
    def __post_init__(self):
        self.params = self.params or {}


class NaturalLanguageInterface:
    """
    Natural language interface for the autopoiesis system.
    
    Parses plain English commands and routes them to appropriate modules.
    """
    
    # Intent patterns: (regex, action, target_group)
    PATTERNS = [
        # Measure commands
        (r"(?:measure|analyze|check|scan)\s+(?:the\s+)?(?:codebase|project|system|code)?", "measure", None),
        (r"(?:measure|analyze|check)\s+(?:the\s+)?(.+)", "measure", 1),
        (r"(?:what(?:'s| is)\s+)?(?:the\s+)?harmony", "measure", None),
        (r"(?:how\s+(?:am\s+i|are\s+we)\s+doing)", "measure", None),
        
        # Heal commands
        (r"(?:heal|fix|repair)\s+(?:the\s+)?(.+)", "heal", 1),
        (r"(?:heal|fix|repair)\s+(?:the\s+)?(?:codebase|project|system)", "heal", None),
        (r"(?:make\s+it\s+better|improve)", "heal", None),
        
        # Grow commands
        (r"(?:grow|create|generate|build|make)\s+(?:a\s+)?(.+)", "grow", 1),
        (r"(?:new|add)\s+(.+)", "grow", 1),
        
        # Status commands
        (r"(?:status|state|health|report)", "status", None),
        (r"(?:where\s+are\s+we|what(?:'s| is)\s+happening)", "status", None),
        
        # Dashboard
        (r"(?:show\s+)?dashboard", "dashboard", None),
        (r"(?:visualize|show|display)\s+(?:harmony|status)", "dashboard", None),
        
        # Growth
        (r"(?:self[- ]?)?grow(?:th)?", "self_grow", None),
        (r"(?:evolve|expand|extend)", "self_grow", None),
        
        # Help
        (r"(?:help|commands|what\s+can\s+you\s+do)", "help", None),
    ]
    
    def __init__(self, target_path: str = "."):
        """
        Initialize the natural language interface.
        
        Args:
            target_path: Path to the project to work on
        """
        self.target_path = Path(target_path).resolve()
        self._capabilities = {}  # Lazy loaded
    
    def parse(self, text: str) -> Intent:
        # Auto-healed: Input validation for parse
        if text is not None and not isinstance(text, str):
            raise TypeError(f'text must be str, got {type(text).__name__}')
        """
        Parse natural language text into an intent.
        
        Args:
            text: Natural language command
            
        Returns:
            Intent with action, target, and parameters
        """
        text = text.lower().strip()
        
        for pattern, action, target_group in self.PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                target = None
                if target_group and target_group <= len(match.groups()):
                    target = match.group(target_group)
                    if target:
                        target = target.strip()
                
                return Intent(
                    action=action,
                    target=target,
                    confidence=0.9,
                    raw_text=text
                )
        
        # Unknown intent
        return Intent(
            action="unknown",
            target=text,
            confidence=0.3,
            raw_text=text
        )
    
    def execute(self, text: str) -> Dict[str, Any]:
        # Auto-healed: Input validation for execute
        if text is not None and not isinstance(text, str):
            raise TypeError(f'text must be str, got {type(text).__name__}')
        """
        Parse and execute a natural language command.
        
        Args:
            text: Natural language command
            
        Returns:
            Result dictionary with success status and data
        """
        intent = self.parse(text)
        
        handlers = {
            "measure": self._handle_measure,
            "heal": self._handle_heal,
            "grow": self._handle_grow,
            "status": self._handle_status,
            "dashboard": self._handle_dashboard,
            "self_grow": self._handle_self_grow,
            "help": self._handle_help,
            "unknown": self._handle_unknown,
        }
        
        handler = handlers.get(intent.action, self._handle_unknown)
        return handler(intent)
    
    def _handle_measure(self, intent: Intent) -> Dict[str, Any]:
        """Handle measure/analyze commands."""
        try:
            from autopoiesis.system import SystemHarmonyMeasurer
            measurer = SystemHarmonyMeasurer()
            
            target = intent.target or str(self.target_path)
            report = measurer.measure(target)
            
            return {
                "success": True,
                "action": "measure",
                "message": f"Harmony: {report.harmony:.3f} ({report.phase.value})",
                "data": {
                    "harmony": report.harmony,
                    "love": report.love,
                    "justice": report.justice,
                    "power": report.power,
                    "wisdom": report.wisdom,
                    "phase": report.phase.value,
                    "files": report.total_files
                }
            }
        except Exception as e:
            return {"success": False, "action": "measure", "message": str(e)}
    
    def _handle_heal(self, intent: Intent) -> Dict[str, Any]:
        """Handle heal/fix commands."""
        try:
            from autopoiesis.engine import AutopoiesisEngine
            engine = AutopoiesisEngine(str(self.target_path), dry_run=True)
            
            # Determine dimension from target
            dimension = None
            if intent.target:
                target_lower = intent.target.lower()
                if any(x in target_lower for x in ['love', 'doc', 'comment']):
                    dimension = 'L'
                elif any(x in target_lower for x in ['justice', 'valid', 'type']):
                    dimension = 'J'
                elif any(x in target_lower for x in ['power', 'error', 'exception']):
                    dimension = 'P'
                elif any(x in target_lower for x in ['wisdom', 'log', 'debug']):
                    dimension = 'W'
            
            result = engine.heal_once(dimension=dimension)
            
            return {
                "success": True,
                "action": "heal",
                "message": f"Healing {dimension or 'weakest dimension'} (dry run)",
                "data": {"dimension": dimension, "result": str(result)[:200]}
            }
        except Exception as e:
            return {"success": False, "action": "heal", "message": str(e)}
    
    def _handle_grow(self, intent: Intent) -> Dict[str, Any]:
        """Handle grow/create commands."""
        try:
            from autopoiesis.grower import IntentToModuleGenerator
            grower = IntentToModuleGenerator()
            
            if not intent.target:
                return {"success": False, "action": "grow", "message": "What should I grow?"}
            
            result = grower.generate(intent.target)
            
            return {
                "success": True,
                "action": "grow",
                "message": f"Generated module for: {intent.target}",
                "data": {"intent": intent.target, "code_length": len(result.get('code', ''))}
            }
        except Exception as e:
            return {"success": False, "action": "grow", "message": str(e)}
    
    def _handle_status(self, intent: Intent) -> Dict[str, Any]:
        """Handle status commands."""
        try:
            from autopoiesis.self_growth import SelfGrowthEngine
            engine = SelfGrowthEngine(str(self.target_path))
            status = engine.get_status()
            
            return {
                "success": True,
                "action": "status",
                "message": f"Capabilities: {status['implemented']}/{status['total_capabilities']}",
                "data": status
            }
        except Exception as e:
            return {"success": False, "action": "status", "message": str(e)}
    
    def _handle_dashboard(self, intent: Intent) -> Dict[str, Any]:
        """Handle dashboard commands."""
        return {
            "success": True,
            "action": "dashboard",
            "message": "Run: python autopoiesis/dashboard.py",
            "data": {"command": "python autopoiesis/dashboard.py"}
        }
    
    def _handle_self_grow(self, intent: Intent) -> Dict[str, Any]:
        """Handle self-growth commands."""
        try:
            from autopoiesis.self_growth import SelfGrowthEngine
            engine = SelfGrowthEngine(str(self.target_path))
            
            result = engine.grow_once()
            
            return {
                "success": result.success,
                "action": "self_grow",
                "message": f"Grew: {result.capability}" if result.success else result.reason,
                "data": {
                    "capability": result.capability,
                    "love": result.love_score,
                    "harmony": result.harmony_score
                }
            }
        except Exception as e:
            return {"success": False, "action": "self_grow", "message": str(e)}
    
    def _handle_help(self, intent: Intent) -> Dict[str, Any]:
        """Handle help commands."""
        return {
            "success": True,
            "action": "help",
            "message": "Available commands",
            "data": {
                "commands": [
                    "measure [path] - Analyze LJPW harmony",
                    "heal [dimension] - Fix deficits",
                    "grow <description> - Create new module",
                    "status - Show system state",
                    "dashboard - Open visual dashboard",
                    "self-grow - Add new capabilities",
                    "help - Show this message"
                ]
            }
        }
    
    def _handle_unknown(self, intent: Intent) -> Dict[str, Any]:
        """Handle unknown commands."""
        return {
            "success": False,
            "action": "unknown",
            "message": f"I don't understand: '{intent.raw_text}'",
            "data": {"suggestions": ["Try 'help' to see available commands"]}
        }
    
    def chat(self):
        """Run interactive chat mode."""
        print("\n" + "=" * 50)
        print("  Autopoiesis Natural Language Interface")
        print("  Type 'help' for commands, 'quit' to exit")
        print("=" * 50 + "\n")
        
        while True:
            try:
                text = input("You: ").strip()
                
                if not text:
                    continue
                if text.lower() in ['quit', 'exit', 'bye']:
                    print("\nGoodbye!")
                    break
                
                result = self.execute(text)
                
                print(f"\nAgent: {result['message']}")
                if result.get('data') and result['action'] == 'help':
                    for cmd in result['data']['commands']:
                        print(f"  - {cmd}")
                print()
                
            except KeyboardInterrupt:
                print("\n\nInterrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\nError: {e}\n")


if __name__ == "__main__":
    interface = NaturalLanguageInterface(".")
    
    # Demo some parses
    print("Natural Language Interface - Demo\n")
    
    tests = [
        "measure the codebase",
        "what's the harmony?",
        "grow a todo app",
        "heal the love dimension",
        "status",
        "help"
    ]
    
    for text in tests:
        intent = interface.parse(text)
        print(f"'{text}' -> {intent.action}({intent.target})")
    
    print("\nStarting interactive mode...")
    interface.chat()
