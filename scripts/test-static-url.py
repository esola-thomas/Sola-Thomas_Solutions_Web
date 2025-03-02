#!/usr/bin/env python3
"""
Test if static URLs can be resolved correctly.
"""
import os
import requests
import sys
from pathlib import Path

# First check if the files exist in the staticfiles directory
staticfiles_dir = Path('/home/esolathomas/ws/sola_thomas_website/staticfiles')

# Key files to check
key_files = [
    'css/theme.css',
    'svg/moon.svg',
    'svg/sun.svg',
    'js/theme.js',
]

print("Checking if files exist in staticfiles directory:")
for file in key_files:
    file_path = staticfiles_dir / file
    exists = os.path.exists(file_path)
    readable = os.access(file_path, os.R_OK) if exists else False
    print(f"  {file} - Exists: {exists}, Readable: {readable}")
    if exists:
        print(f"    File size: {os.path.getsize(file_path)} bytes")
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            try:
                first_line = f.readline().strip()
                print(f"    First line: {first_line[:50]}...")
            except Exception as e:
                print(f"    Error reading file: {str(e)}")

# Now test HTTP access
print("\nTesting HTTP access to static files:")
try:
    for file in key_files:
        url = f"http://localhost/static/{file}"
        print(f"Testing URL: {url}")
        
        response = requests.get(url)
        print(f"  Status code: {response.status_code}")
        if response.status_code == 200:
            print(f"  Content type: {response.headers.get('Content-Type')}")
            print(f"  Content length: {len(response.content)} bytes")
            print(f"  Served by: {response.headers.get('X-Served-By', 'unknown')}")
        else:
            print(f"  Error: {response.text[:100]}...")
except Exception as e:
    print(f"Error making HTTP request: {str(e)}")

# Also check if WhiteNoise is serving files
print("\nTesting Django/WhiteNoise static file serving:")
try:
    for file in key_files:
        url = f"http://localhost:8000/static/{file}"
        print(f"Testing URL: {url}")
        
        response = requests.get(url)
        print(f"  Status code: {response.status_code}")
        if response.status_code == 200:
            print(f"  Content type: {response.headers.get('Content-Type')}")
            print(f"  Content length: {len(response.content)} bytes")
        else:
            print(f"  Error: {response.text[:100]}...")
except Exception as e:
    print(f"Error making HTTP request: {str(e)}")
