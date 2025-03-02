#!/usr/bin/env python3
"""
Script to check database connection for Django application.
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
    print("Django setup successful")
except Exception as e:
    print(f"Django setup error: {str(e)}")
    sys.exit(1)

def check_database_connection():
    """Test the database connection and return status code"""
    from django.db import connections
    from django.db.utils import OperationalError
    
    try:
        db_conn = connections['default']
        db_conn.cursor()
        print("Database connection successful")
        return 0
    except OperationalError as e:
        print(f"Database connection failed: {str(e)}")
        return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(check_database_connection())
