#!/usr/bin/env python
"""
Manual superuser creation script for troubleshooting.
Run this if the automatic superuser creation fails.
"""

import os
import sys
import django

# Add the Django project to the Python path
sys.path.insert(0, '/opt/render/project/src/mysite')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

django.setup()

from django.contrib.auth.models import User

def create_superuser():
    # Get credentials from environment or use defaults
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@chatapp.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123!')
    
    # Check if superuser already exists
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser already exists.")
        existing_superuser = User.objects.filter(is_superuser=True).first()
        print(f"   Username: {existing_superuser.username}")
        print(f"   Email: {existing_superuser.email}")
        return True
    
    # Create superuser
    try:
        superuser = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print("⚠️  Please change the password after first login!")
        return True
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

if __name__ == '__main__':
    create_superuser()
