"""
Unified Autopoiesis Package
============================

A self-healing, self-evolving code system built on LJPW principles.

This package consolidates all autopoiesis components into a coherent system:

1. ANALYZER - Deep AST-based code analysis to find deficits (Python)
2. JS_ANALYZER - JavaScript LJPW analysis (JS/TS)
3. MULTI_ANALYZER - Unified multi-language analysis (Python/JS/HTML/CSS)
4. HEALER - Generates contextual solutions for identified deficits
5. RHYTHM - Orchestrates healing through breathing cycles (L→J→P→W)
6. SYSTEM - Measures harmony at the system level (not just functions)
7. GROWER - Generates Python modules from natural language
8. WEB_GROWER - Generates web applications from natural language
9. BICAMERAL - Integrates left/right brain for semantic growth

Usage:
    from autopoiesis import AutopoiesisEngine
    
    engine = AutopoiesisEngine(target_path="./ljpw_nn")
    engine.breathe(cycles=8)  # Run 8 healing cycles
    report = engine.get_report()

Multi-language usage:
    from autopoiesis import MultiLanguageAnalyzer
    
    analyzer = MultiLanguageAnalyzer()
    report = analyzer.analyze_directory("./my_web_app")
    print(f"Harmony: {report.harmony:.3f}")

The key insight: Autopoiesis emerges at the SYSTEM level, not function level.
Individual functions specialize. Systems integrate. Autopoiesis requires integration.

Threshold for autopoiesis: L > 0.7, H > 0.6
"""

from .analyzer import CodeAnalyzer, FileAnalysis, FunctionAnalysis, SystemAnalysis
from .healer import Healer, NovelSolution
from .rhythm import BreathingOrchestrator, BreathState
from .system import SystemHarmonyMeasurer, SystemPhase, SystemHealthReport
from .engine import AutopoiesisEngine
from .js_analyzer import JSAnalyzer, JSFileAnalysis, JSFunction
from .multi_analyzer import MultiLanguageAnalyzer, MultiLanguageReport, UnifiedFileAnalysis, FileType

# Auto-healed: Logging infrastructure for observability (Wisdom dimension)
import logging

_logger = logging.getLogger(__name__)
if not _logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    ))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)


__all__ = [
    # Core classes
    "AutopoiesisEngine",
    "CodeAnalyzer", 
    "Healer",
    "BreathingOrchestrator",
    "SystemHarmonyMeasurer",
    
    # Multi-language support
    "JSAnalyzer",
    "MultiLanguageAnalyzer",
    
    # Data classes - Python
    "FileAnalysis",
    "FunctionAnalysis", 
    "SystemAnalysis",
    "NovelSolution",
    "BreathState",
    
    # Data classes - JavaScript
    "JSFileAnalysis",
    "JSFunction",
    
    # Data classes - Multi-language
    "MultiLanguageReport",
    "UnifiedFileAnalysis",
    "FileType",
    
    # System
    "SystemPhase",
    "SystemHealthReport",
]

__version__ = "2.1.0"  # V8.4 Generative Equation integration

