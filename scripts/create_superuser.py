#!/usr/bin/env python3
"""
Script to create a superuser for Django application.
"""
import os
import sys
import django

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sola_thomas_website.settings')
os.environ['DEPLOYMENT'] = 'True'  # Ensure we're using the right database

# Initialize Django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser(username, email, password):
    """
    Create a superuser if one with the given username doesn't exist
    """
    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser '{username}'...")
        User.objects.create_superuser(username, email, password)
        print(f"Superuser '{username}' created successfully!")
        return True
    else:
        print(f"Superuser '{username}' already exists, skipping creation.")
        return False

if __name__ == "__main__":
    # Default superuser details
    username = "esolathomas"
    email = "ernesto@solathomas.com"
    password = "py_generic_passsword1234"
    
    # Allow overriding via command line args
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        email = sys.argv[2]
    if len(sys.argv) > 3:
        password = sys.argv[3]
    
    create_superuser(username, email, password)
