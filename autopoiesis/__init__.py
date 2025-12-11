"""
Unified Autopoiesis Package
============================

A self-healing, self-evolving code system built on LJPW principles.

This package consolidates all autopoiesis components into a coherent system:

1. ANALYZER - Deep AST-based code analysis to find deficits
2. HEALER - Generates contextual solutions for identified deficits
3. RHYTHM - Orchestrates healing through breathing cycles (L→J→P→W)
4. EVOLUTION - Topology/meta-learning/consciousness evolution
5. SYSTEM - Measures harmony at the system level (not just functions)

Usage:
    from autopoiesis import AutopoiesisEngine
    
    engine = AutopoiesisEngine(target_path="./ljpw_nn")
    engine.breathe(cycles=8)  # Run 8 healing cycles
    report = engine.get_report()

The key insight: Autopoiesis emerges at the SYSTEM level, not function level.
Individual functions specialize. Systems integrate. Autopoiesis requires integration.

Threshold for autopoiesis: L > 0.7, H > 0.6
"""

from .analyzer import CodeAnalyzer, FileAnalysis, FunctionAnalysis, SystemAnalysis
from .healer import Healer, NovelSolution
from .rhythm import BreathingOrchestrator, BreathState
from .system import SystemHarmonyMeasurer
from .engine import AutopoiesisEngine

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
    
    # Data classes
    "FileAnalysis",
    "FunctionAnalysis", 
    "SystemAnalysis",
    "NovelSolution",
    "BreathState",
]

__version__ = "1.0.0"
