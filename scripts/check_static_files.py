#!/usr/bin/env python3
"""
Check that static files exist and are accessible.
"""
import os
from pathlib import Path

static_dir = Path('/home/esolathomas/ws/sola_thomas_website/staticfiles')

print(f"Checking static directory: {static_dir}")
print(f"Directory exists: {os.path.exists(static_dir)}")
print(f"Directory is readable: {os.access(static_dir, os.R_OK)}")

if os.path.exists(static_dir):
    print("\nListing files in static directory:")
    for root, dirs, files in os.walk(static_dir):
        for file in files:
            full_path = os.path.join(root, file)
            if 'css' in full_path or 'js' in full_path or 'svg' in full_path:
                print(f"  {os.path.relpath(full_path, static_dir)} - "
                     f"Readable: {os.access(full_path, os.R_OK)}")

    # Check for specific files that should exist
    key_files = [
        'css/theme.css',
        'svg/moon.svg',
        'svg/sun.svg',
        'js/theme.js',
    ]
    
    print("\nChecking for key static files:")
    for file in key_files:
        file_path = static_dir / file
        exists = os.path.exists(file_path)
        print(f"  {file} - Exists: {exists}, "
             f"Readable: {os.access(file_path, os.R_OK) if exists else 'N/A'}")
