#!/usr/bin/env python3
"""
Script to verify migrations have been applied correctly.
"""
import os
import sys
import django

# Add the Django project directory to Python path
project_path = '/home/esolathomas/ws/sola_thomas_website'
sys.path.append(project_path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sola_thomas_website.settings')
os.environ['DEPLOYMENT'] = 'True'

# Initialize Django
try:
    django.setup()
except Exception as e:
    print(f"Django setup error: {str(e)}")
    sys.exit(1)

def check_migrations():
    """Check if migrations have been applied correctly"""
    try:
        from django.db import connection
        
        # Get list of all tables in the database
        tables = connection.introspection.table_names()
        
        # Check for essential tables
        required_tables = ['auth_user', 'django_content_type', 'django_migrations']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"Missing required tables: {', '.join(missing_tables)}")
            print("Migrations have not been completely applied!")
            return 1
        else:
            print("All required tables exist. Migrations appear to be successful.")
            return 0
    except Exception as e:
        print(f"Error checking migrations: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(check_migrations())
