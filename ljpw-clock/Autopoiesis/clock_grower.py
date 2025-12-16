#!/usr/bin/env python3
"""
LJPW Clock Grower
=================

A self-contained clock grower that generates LJPW-balanced clocks from intent.

Usage:
    from clock_grower import ClockGrower
    
    grower = ClockGrower()
    files = grower.grow("Create a beautiful clock")
    grower.save_to("output/")

LJPW Principles:
    Love (L):    Documentation, helpful feedback
    Justice (J): Validation, consistent behavior
    Power (P):   Efficient generation
    Wisdom (W):  Modular, self-aware code
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

from templates import ClockTemplates


# =============================================================================
# CONFIGURATION
# =============================================================================

# App types the grower knows about
APP_TYPES = {
    'clock': {
        'name': 'LJPW Clock',
        'components': ['analog', 'digital', 'harmony_indicator'],
        'features': ['smooth_seconds', 'date_display', 'ljpw_metrics'],
    },
}

# Keywords to detect app type from intent
APP_TYPE_KEYWORDS = {
    'clock': ['clock', 'time', 'watch', 'timer', 'analog', 'digital clock', 'timepiece'],
}

# Target LJPW profile
LJPW_PROFILE = {
    'L': 0.85,  # Love
    'J': 0.90,  # Justice
    'P': 0.75,  # Power
    'W': 0.80,  # Wisdom
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class ParsedIntent:
    """Parsed representation of user intent."""
    raw_intent: str
    app_type: str
    components: List[str]
    features: List[str]
    app_name: str
    description: str


# =============================================================================
# CLOCK GROWER
# =============================================================================

class ClockGrower:
    """Grows LJPW-balanced clocks from natural language intent."""
    
    def __init__(self):
        self.profile = LJPW_PROFILE
        self.harmony = self._calculate_harmony()
        self.templates = ClockTemplates()
        self._generated_files: Dict[str, str] = {}
    
    def _calculate_harmony(self) -> float:
        """Calculate harmony as geometric mean of LJPW dimensions."""
        p = self.profile
        return (p['L'] * p['J'] * p['P'] * p['W']) ** 0.25
    
    def parse(self, intent: str) -> ParsedIntent:
        """Parse natural language intent.
        
        Args:
            intent: Natural language description of desired app
            
        Returns:
            ParsedIntent with extracted information
        """
        intent_lower = intent.lower()
        
        # Detect app type
        app_type = 'clock'  # Default
        for atype, keywords in APP_TYPE_KEYWORDS.items():
            if any(kw in intent_lower for kw in keywords):
                app_type = atype
                break
        
        # Get components and features for this type
        app_info = APP_TYPES.get(app_type, APP_TYPES['clock'])
        
        return ParsedIntent(
            raw_intent=intent,
            app_type=app_type,
            components=app_info['components'],
            features=app_info['features'],
            app_name=f"ljpw_{app_type}",
            description=f"A {app_info['name']} generated from: {intent}"
        )
    
    def grow(self, intent: str) -> Dict[str, str]:
        """Grow a clock from natural language intent.
        
        Args:
            intent: Natural language description
            
        Returns:
            Dictionary of filename -> content
        """
        print(f"[LJPW Clock Grower]")
        print(f"  Intent: {intent}")
        print(f"  Target: L={self.profile['L']}, J={self.profile['J']}, P={self.profile['P']}, W={self.profile['W']}")
        print(f"  Harmony: H={self.harmony:.2f}")
        print()
        
        # Parse intent
        parsed = self.parse(intent)
        print(f"[Parsing]")
        print(f"  App Type: {parsed.app_type}")
        print(f"  Components: {parsed.components}")
        print(f"  Features: {parsed.features}")
        print()
        
        # Generate files
        print(f"[Growing]")
        files = self._generate_clock(parsed)
        
        for filename, content in files.items():
            print(f"  Generated: {filename} ({len(content):,} bytes)")
        
        self._generated_files = files
        
        print()
        print(f"[Complete]")
        print(f"  Total: {sum(len(c) for c in files.values()):,} bytes")
        print(f"  Status: {'AUTOPOIETIC' if self.harmony > 0.6 and self.profile['L'] > 0.7 else 'HOMEOSTATIC'}")
        
        return files
    
    def _generate_clock(self, parsed: ParsedIntent) -> Dict[str, str]:
        """Generate clock files from parsed intent."""
        timestamp = datetime.now().isoformat()
        
        return {
            'index.html': self.templates.html(parsed, self.profile, self.harmony, timestamp),
            'styles.css': self.templates.css(parsed, self.profile, self.harmony, timestamp),
            'app.js': self.templates.js(parsed, self.profile, self.harmony, timestamp),
        }
    
    def save_to(self, output_dir: str) -> None:
        """Save generated files to a directory.
        
        Args:
            output_dir: Path to output directory
        """
        if not self._generated_files:
            raise ValueError("No files generated yet. Call grow() first.")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for filename, content in self._generated_files.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Saved: {filepath}")
    
    def verify(self) -> bool:
        """Verify the clock meets autopoietic threshold."""
        is_autopoietic = self.harmony > 0.6 and self.profile['L'] > 0.7
        
        print(f"[Verification]")
        print(f"  Harmony: {self.harmony:.2f} {'>' if self.harmony > 0.6 else '<='} 0.6")
        print(f"  Love: {self.profile['L']:.2f} {'>' if self.profile['L'] > 0.7 else '<='} 0.7")
        print(f"  Result: {'AUTOPOIETIC (OK)' if is_autopoietic else 'HOMEOSTATIC'}")
        
        return is_autopoietic


# =============================================================================
# MAIN (for testing)
# =============================================================================

if __name__ == "__main__":
    grower = ClockGrower()
    grower.grow("Create a beautiful digital and analog clock")
    grower.verify()
