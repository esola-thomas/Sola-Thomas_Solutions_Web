#!/usr/bin/env python3
"""
Debug how static files are referenced in HTML templates
"""
import os
import sys
import re
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Get the HTML content from the site
def get_html():
    try:
        response = requests.get('http://localhost/')
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch HTML: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching HTML: {str(e)}")
        return None

# Extract static file references
def extract_static_refs(html_content):
    if not html_content:
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    static_refs = []
    
    # Check CSS files
    for link in soup.find_all('link', rel='stylesheet'):
        if link.get('href'):
            static_refs.append(('CSS', link.get('href')))
    
    # Check JS files
    for script in soup.find_all('script', src=True):
        static_refs.append(('JS', script.get('src')))
    
    # Check images
    for img in soup.find_all('img', src=True):
        static_refs.append(('IMG', img.get('src')))
    
    # Check SVG references
    for element in soup.find_all(attrs={'href': re.compile(r'.*\.svg.*')}):
        static_refs.append(('SVG', element.get('href')))
    
    return static_refs

# Verify if static files are accessible
def check_static_refs(static_refs):
    results = []
    for ref_type, ref_path in static_refs:
        if ref_path.startswith('/static/'):
            full_url = f"http://localhost{ref_path}"
            try:
                response = requests.get(full_url)
                status = response.status_code
            except Exception:
                status = "Error"
            
            # Check if file exists in staticfiles directory
            path_in_static = ref_path.replace('/static/', '')
            file_path = Path('/home/esolathomas/ws/sola_thomas_website/staticfiles') / path_in_static
            file_exists = os.path.exists(file_path)
            
            results.append({
                'type': ref_type,
                'path': ref_path,
                'url': full_url,
                'status': status,
                'exists_in_static': file_exists
            })
    
    return results

if __name__ == "__main__":
    print("Debugging static file references in HTML")
    html_content = get_html()
    if html_content:
        static_refs = extract_static_refs(html_content)
        print(f"\nFound {len(static_refs)} static file references:")
        for ref_type, ref_path in static_refs:
            print(f"  {ref_type}: {ref_path}")
        
        print("\nChecking accessibility of static files:")
        results = check_static_refs(static_refs)
        for result in results:
            print(f"  {result['type']}: {result['path']}")
            print(f"    URL: {result['url']}")
            print(f"    Status: {result['status']}")
            print(f"    Exists in staticfiles: {result['exists_in_static']}")
            print()
    else:
        print("Failed to get HTML content for analysis")
