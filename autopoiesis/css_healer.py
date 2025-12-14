"""
CSS Healer
==========

Automatically heals LJPW deficits in CSS code:
- Love (L): Adds comments, improves readability
- Justice (J): Adds design tokens, consistent naming
- Power (P): Adds fallbacks, vendor prefixes
- Wisdom (W): Adds media queries structure, organization

Usage:
    healer = CSSHealer()
    healer.heal_file("styles.css", dimension="L")
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class CSSHealingResult:
    """Result of CSS healing."""
    file_path: str
    dimension: str
    changes_made: List[str]
    success: bool


class CSSHealer:
    """Heals CSS code by adding LJPW elements."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
    
    def heal_file(self, file_path: str, dimension: Optional[str] = None) -> List[CSSHealingResult]:
        """Heal a CSS file."""
        path = Path(file_path)
        if not path.exists():
            return [CSSHealingResult(file_path, dimension or "ALL", [], False)]
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        original = content
        results = []
        
        dimensions = [dimension] if dimension else ['L', 'J', 'P', 'W']
        
        for dim in dimensions:
            if dim == 'L':
                content, result = self._heal_love(content, file_path)
            elif dim == 'J':
                content, result = self._heal_justice(content, file_path)
            elif dim == 'P':
                content, result = self._heal_power(content, file_path)
            elif dim == 'W':
                content, result = self._heal_wisdom(content, file_path)
            else:
                continue
            results.append(result)
        
        if content != original and not self.dry_run:
            path.write_text(content, encoding='utf-8')
        
        return results
    
    def _heal_love(self, content: str, file_path: str) -> Tuple[str, CSSHealingResult]:
        """Add comments and improve readability."""
        changes = []
        
        # Add file header if missing
        if not content.strip().startswith('/*'):
            filename = Path(file_path).stem
            header = f"""/**
 * {filename.replace('-', ' ').replace('_', ' ').title()} Styles
 * Auto-healed for readability
 */

"""
            content = header + content
            changes.append("Added file header comment")
        
        # Add section comments before major selectors
        major_selectors = ['body', 'header', 'main', 'footer', 'nav']
        for selector in major_selectors:
            # Check if selector exists and doesn't have comment before it
            selector_pattern = rf'\n({re.escape(selector)}\s*\{{)'
            section_comment = f'/* {selector.title()} Styles */'
            
            if re.search(selector_pattern, content) and section_comment.lower() not in content.lower():
                content = re.sub(selector_pattern, f'\n{section_comment}\n\\1', content, count=1)
                changes.append(f"Added section comment for {selector}")
        
        return content, CSSHealingResult(file_path, 'L', changes, True)
    
    def _heal_justice(self, content: str, file_path: str) -> Tuple[str, CSSHealingResult]:
        """Add design tokens and consistent naming."""
        changes = []
        
        # Extract colors and create CSS variables if :root doesn't exist
        if ':root' not in content:
            # Find hex colors
            colors = set(re.findall(r'#[0-9a-fA-F]{3,6}\b', content))
            
            if len(colors) >= 2:
                # Create :root block with color variables
                root_vars = [':root {']
                color_map = {}
                
                for i, color in enumerate(sorted(colors)[:8]):  # Max 8 colors
                    var_name = f'--color-{i + 1}'
                    root_vars.append(f'    {var_name}: {color};')
                    color_map[color] = f'var({var_name})'
                
                root_vars.append('}\n\n')
                
                # Insert at beginning (after header if exists)
                if content.startswith('/**'):
                    end_comment = content.find('*/') + 2
                    content = content[:end_comment] + '\n\n' + '\n'.join(root_vars) + content[end_comment:]
                else:
                    content = '\n'.join(root_vars) + content
                
                changes.append(f"Added :root with {len(colors)} color variables")
        
        return content, CSSHealingResult(file_path, 'J', changes, True)
    
    def _heal_power(self, content: str, file_path: str) -> Tuple[str, CSSHealingResult]:
        """Add fallbacks and vendor prefixes."""
        changes = []
        
        # Add fallback fonts
        if 'font-family' in content:
            # Add system font fallback if not present
            if 'sans-serif' not in content and 'serif' not in content:
                content = re.sub(
                    r"font-family:\s*(['\"][^'\"]+['\"])",
                    r"font-family: \1, system-ui, sans-serif",
                    content,
                    count=1
                )
                changes.append("Added font-family fallbacks")
        
        # Add vendor prefixes for common properties
        prefix_props = {
            'user-select': ['-webkit-user-select', '-moz-user-select'],
            'backdrop-filter': ['-webkit-backdrop-filter'],
            'appearance': ['-webkit-appearance', '-moz-appearance'],
        }
        
        for prop, prefixes in prefix_props.items():
            if prop in content and not any(p in content for p in prefixes):
                # Find lines with this property and add prefixes
                pattern = rf'(\s*)({prop}:\s*[^;]+;)'
                match = re.search(pattern, content)
                if match:
                    indent = match.group(1)
                    value = match.group(2).split(':')[1]
                    prefixed = '\n'.join([f'{indent}{p}:{value}' for p in prefixes])
                    content = content.replace(match.group(0), f'{prefixed}\n{match.group(0)}')
                    changes.append(f"Added vendor prefixes for {prop}")
        
        return content, CSSHealingResult(file_path, 'P', changes, True)
    
    def _heal_wisdom(self, content: str, file_path: str) -> Tuple[str, CSSHealingResult]:
        """Add media query structure and organization."""
        changes = []
        
        # Add responsive breakpoint comment if media queries exist
        if '@media' in content and '/* Responsive' not in content:
            # Find first media query and add comment
            content = re.sub(
                r'(@media\s*\([^)]+\)\s*\{)',
                r'/* Responsive Breakpoints */\n\1',
                content,
                count=1
            )
            changes.append("Added responsive section comment")
        
        # Add print styles if not present
        if '@media print' not in content and len(content) > 500:
            print_styles = """

/* Print Styles */
@media print {
    * {
        background: transparent !important;
        color: black !important;
    }
    
    nav, footer, .no-print {
        display: none !important;
    }
}
"""
            content = content.rstrip() + print_styles
            changes.append("Added print styles")
        
        return content, CSSHealingResult(file_path, 'W', changes, True)


if __name__ == "__main__":
    print("CSS Healer - Testing")
    print("-" * 40)
    
    # Test on flight-tracker
    test_path = Path(__file__).parent.parent / "flight-tracker" / "styles.css"
    if test_path.exists():
        healer = CSSHealer(dry_run=True)
        results = healer.heal_file(str(test_path))
        
        for r in results:
            print(f"\n[{r.dimension}] {len(r.changes_made)} changes:")
            for c in r.changes_made:
                print(f"  - {c}")
    else:
        print(f"Test file not found: {test_path}")
