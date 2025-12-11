"""
Analyze Beautiful Calculator
Extracts key metrics from the generated HTML file.
"""

import sys
import os
import re

def extract_css(html_content):
    match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    return match.group(1) if match else ""

def extract_js(html_content):
    match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
    return match.group(1) if match else ""

def main():
    target_file = os.path.join(os.path.dirname(__file__), "beautiful_calculator.html")
    
    if not os.path.exists(target_file):
        print(f"Error: {target_file} not found.")
        return

    print(f"Analyzing {target_file}...")
    with open(target_file, 'r', encoding='utf-8') as f:
        html = f.read()

    css = extract_css(html)
    js = extract_js(html)

    print("\n--- CSS ANALYSIS ---")
    print(f"Length: {len(css)} chars")
    print(f"Gradients: {css.count('gradient')}")
    print(f"Blurs: {css.count('blur')}")
    print(f"Animations: {css.count('animation')}")
    
    print("\n--- JS ANALYSIS ---")
    print(f"Length: {len(js)} chars")
    print(f"Try/Catch Blocks: {js.count('try')}")
    print(f"Event Listeners: {js.count('addEventListener')}")

    print("\n--- AESTHETIC CHECK ---")
    if "glass-bg" in css and "orb" in css:
        print("✅ Glassmorphism detected")
    else:
        print("❌ Glassmorphism missing")

if __name__ == "__main__":
    main()
