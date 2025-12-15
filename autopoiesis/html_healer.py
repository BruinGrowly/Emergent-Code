"""
HTML Healer
===========

Automatically heals LJPW deficits in HTML code:
- Love (L): Adds semantic elements, alt text, aria labels
- Justice (J): Fixes structure, adds lang/charset
- Power (P): Adds noscript fallbacks, error handling
- Wisdom (W): Adds meta tags, structured data comments

Usage:
    healer = HTMLHealer()
    healer.heal_file("index.html", dimension="L")
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class HTMLHealingResult:
    """Result of HTML healing."""
    file_path: str
    dimension: str
    changes_made: List[str]
    success: bool


class HTMLHealer:
    """Heals HTML code by adding LJPW elements."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
    
    def heal_file(self, file_path: str, dimension: Optional[str] = None) -> List[HTMLHealingResult]:
        """Heal an HTML file."""
        path = Path(file_path)
        if not path.exists():
            return [HTMLHealingResult(file_path, dimension or "ALL", [], False)]
        
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
    
    def _heal_love(self, content: str, file_path: str) -> Tuple[str, HTMLHealingResult]:
        """Add accessibility and semantic elements."""
        changes = []
        
        # Add alt text to images without it
        img_pattern = r'<img\s+(?![^>]*alt=)[^>]*src=["\']([^"\']+)["\'][^>]*>'
        for match in re.finditer(img_pattern, content):
            src = match.group(1)
            filename = Path(src).stem.replace('-', ' ').replace('_', ' ')
            new_tag = match.group(0).replace('<img ', f'<img alt="{filename}" ')
            content = content.replace(match.group(0), new_tag)
            changes.append(f"Added alt text to image: {src}")
        
        # Add aria-label to buttons without text
        button_pattern = r'<button\s+(?![^>]*aria-label=)[^>]*></button>'
        content = re.sub(button_pattern, 
                        lambda m: m.group(0).replace('<button ', '<button aria-label="button" '),
                        content)
        if '<button aria-label="button"' in content:
            changes.append("Added aria-label to empty buttons")
        
        # Replace div with section/main/article where appropriate
        if '<div class="main"' in content or '<div id="main"' in content:
            content = re.sub(r'<div\s+(class|id)="main"', r'<main \1="main"', content)
            content = re.sub(r'</div>(\s*<!--\s*main\s*-->)', r'</main>\1', content)
            changes.append("Replaced div.main with <main>")
        
        return content, HTMLHealingResult(file_path, 'L', changes, True)
    
    def _heal_justice(self, content: str, file_path: str) -> Tuple[str, HTMLHealingResult]:
        """Fix structure and add required attributes."""
        changes = []
        
        # Add lang attribute to html tag
        if '<html' in content and 'lang=' not in content.split('<html')[1].split('>')[0]:
            content = content.replace('<html', '<html lang="en"', 1)
            changes.append("Added lang='en' to <html>")
        
        # Add charset meta if missing
        if '<head>' in content and '<meta charset' not in content:
            content = content.replace('<head>', '<head>\n    <meta charset="UTF-8">')
            changes.append("Added charset meta tag")
        
        # Add viewport meta if missing
        if '<head>' in content and 'viewport' not in content:
            head_end = content.find('</head>')
            if head_end > 0:
                viewport = '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
                content = content[:head_end] + viewport + content[head_end:]
                changes.append("Added viewport meta tag")
        
        # Add form validation attributes
        if 'type="email"' in content and 'required' not in content:
            content = re.sub(r'type="email"(?![^>]*required)', 'type="email" required', content)
            changes.append("Added required to email inputs")
        
        return content, HTMLHealingResult(file_path, 'J', changes, True)
    
    def _heal_power(self, content: str, file_path: str) -> Tuple[str, HTMLHealingResult]:
        """Add fallbacks and error handling."""
        changes = []
        
        # Add noscript fallback if scripts exist but no noscript
        if '<script' in content and '<noscript>' not in content:
            body_end = content.find('</body>')
            if body_end > 0:
                noscript = '\n    <noscript>\n        <p>This application requires JavaScript to function.</p>\n    </noscript>\n'
                content = content[:body_end] + noscript + content[body_end:]
                changes.append("Added <noscript> fallback")
        
        # Add onerror to images
        img_pattern = r'<img\s+(?![^>]*onerror=)[^>]*>'
        for match in re.finditer(img_pattern, content):
            if 'src=' in match.group(0):
                new_tag = match.group(0).replace('<img ', '<img onerror="this.style.display=\'none\'" ')
                content = content.replace(match.group(0), new_tag)
                changes.append("Added onerror handler to image")
                break  # Just one to avoid spam
        
        return content, HTMLHealingResult(file_path, 'P', changes, True)
    
    def _heal_wisdom(self, content: str, file_path: str) -> Tuple[str, HTMLHealingResult]:
        """Add meta tags and documentation."""
        changes = []
        
        # Add description meta if missing
        if '<head>' in content and '<meta name="description"' not in content:
            head_end = content.find('</head>')
            if head_end > 0:
                title_match = re.search(r'<title>([^<]+)</title>', content)
                desc = title_match.group(1) if title_match else "Application"
                meta = f'    <meta name="description" content="{desc}">\n'
                content = content[:head_end] + meta + content[head_end:]
                changes.append("Added description meta tag")
        
        # Add section comments if not present
        if '<!-- header -->' not in content.lower() and '<header>' in content:
            content = content.replace('<header>', '<!-- Header Section -->\n<header>')
            changes.append("Added section comment for header")
        
        if '<!-- footer -->' not in content.lower() and '<footer>' in content:
            content = content.replace('<footer>', '<!-- Footer Section -->\n<footer>')
            changes.append("Added section comment for footer")
        
        return content, HTMLHealingResult(file_path, 'W', changes, True)


if __name__ == "__main__":
    print("HTML Healer - Testing")
    print("-" * 40)
    
    # Test on flight-tracker
    test_path = Path(__file__).parent.parent / "flight-tracker" / "index.html"
    if test_path.exists():
        healer = HTMLHealer(dry_run=True)
        results = healer.heal_file(str(test_path))
        
        for r in results:
            print(f"\n[{r.dimension}] {len(r.changes_made)} changes:")
            for c in r.changes_made:
                print(f"  - {c}")
    else:
        print(f"Test file not found: {test_path}")
