#!/usr/bin/env python3
"""
Fix static references in HTML templates
"""
import os
import re
from pathlib import Path

def fix_templates():
    templates_dir = Path('/home/esolathomas/ws/sola_thomas_website/templates')
    
    # Walk through all template files
    for root, _, files in os.walk(templates_dir):
        for file in files:
            if file.endswith(('.html', '.htm')):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}")
                
                # Read the file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Fix static references that don't start with a leading slash
                updated = re.sub(r'href=["\'](static/)', r'href="/static/', content)
                updated = re.sub(r'src=["\'](static/)', r'src="/static/', updated)
                
                # Write back the file if changed
                if updated != content:
                    print(f"  - Fixed references in {file}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(updated)

if __name__ == "__main__":
    fix_templates()
    print("Finished updating templates")
