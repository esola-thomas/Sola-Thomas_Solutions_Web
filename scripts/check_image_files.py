#!/usr/bin/env python3
"""
Check if image files exist in the staticfiles directory.
"""
import os
from pathlib import Path
import subprocess

# Define paths
static_dir = Path('/home/esolathomas/ws/sola_thomas_website/staticfiles')
image_dir = static_dir / 'images'

def check_images():
    """Check if image directory exists and contains expected files"""
    print(f"Checking static images directory: {image_dir}")
    
    if not os.path.exists(image_dir):
        print(f"ERROR: Image directory does not exist at {image_dir}")
        print("Creating directory...")
        os.makedirs(image_dir, exist_ok=True)
        print(f"Directory created: {os.path.exists(image_dir)}")
    
    # Check for specific image files
    important_images = [
        'hero_blue_waves_background.jpg',
        'contact-us-icon.png'
    ]
    
    print("\nChecking for important image files:")
    for img in important_images:
        img_path = image_dir / img
        exists = os.path.exists(img_path)
        print(f"  {img}: {'✓ Found' if exists else '✗ Missing'}")
        
        if not exists:
            # Check if it exists in the original static directory
            source_path = Path('/home/esolathomas/ws/sola_thomas_website/static/images') / img
            if os.path.exists(source_path):
                print(f"    Image found in source directory: {source_path}")
                print(f"    Copying to static files directory...")
                try:
                    os.makedirs(os.path.dirname(img_path), exist_ok=True)
                    subprocess.run(['cp', str(source_path), str(img_path)])
                    print(f"    Copy successful: {os.path.exists(img_path)}")
                except Exception as e:
                    print(f"    Error copying file: {e}")
            else:
                print(f"    Image not found in source directory either: {source_path}")
    
    # List all files in the images directory
    print("\nAll files in images directory:")
    if os.path.exists(image_dir):
        files = os.listdir(image_dir)
        if files:
            for file in files:
                file_path = image_dir / file
                print(f"  {file} - Size: {os.path.getsize(file_path)} bytes")
        else:
            print("  No files found in images directory")
    else:
        print("  Images directory does not exist")

if __name__ == "__main__":
    check_images()
