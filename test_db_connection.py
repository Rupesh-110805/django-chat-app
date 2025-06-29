#!/usr/bin/env python3
"""
Database connectivity test script for Render deployment
This helps debug PostgreSQL connection issues
"""

import os
import sys
import django
from django.conf import settings

# Add the project root to Python path
sys.path.insert(0, '/opt/render/project/src/mysite')

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

try:
    django.setup()
    print("✅ Django setup successful")
    
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Database connection successful: {result}")
        
    print("✅ All database tests passed!")
    
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    print(f"❌ Error type: {type(e).__name__}")
    
    # Try to provide more specific error information
    if "psycopg" in str(e).lower():
        print("🔧 PostgreSQL driver issue detected")
        print("   - Check psycopg/psycopg2 installation")
        print("   - Verify Python version compatibility")
    
    if "database" in str(e).lower():
        print("🔧 Database configuration issue detected")
        print("   - Check DATABASE_URL environment variable")
        print("   - Verify Neon PostgreSQL connection string")
    
    sys.exit(1)
