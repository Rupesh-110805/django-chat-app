"""
Database migration script to transfer data from SQLite to PostgreSQL
Run this script before switching to PostgreSQL in production
"""
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
mysite_dir = os.path.join(script_dir, 'mysite')
sys.path.insert(0, mysite_dir)

os.chdir(mysite_dir)

import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def backup_sqlite_data():
    """Create a JSON backup of all SQLite data"""
    print("🔄 Creating backup of SQLite data...")
    
    try:
        # Create fixtures backup with UTF-8 encoding
        with open('data_backup.json', 'w', encoding='utf-8') as f:
            call_command('dumpdata', 
                        '--exclude=contenttypes', 
                        '--exclude=auth.permission',
                        '--exclude=sessions.session',
                        '--exclude=admin.logentry',
                        '--indent=2',
                        stdout=f)
        print("✅ SQLite data backed up to 'data_backup.json'")
        return True
    except Exception as e:
        print(f"❌ Error backing up data: {e}")
        return False

def restore_data_to_postgres():
    """Restore data to PostgreSQL database"""
    print("🔄 Restoring data to PostgreSQL...")
    
    try:
        # Run migrations first
        print("Running migrations...")
        call_command('migrate')
        
        # Load the backup data
        if os.path.exists('data_backup.json'):
            call_command('loaddata', 'data_backup.json')
            print("✅ Data successfully restored to PostgreSQL")
        else:
            print("⚠️  No backup file found. Starting with empty database.")
        return True
    except Exception as e:
        print(f"❌ Error restoring data: {e}")
        return False

def setup_google_oauth():
    """Setup Google OAuth application in the new database"""
    print("🔄 Setting up Google OAuth...")
    
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site
    from decouple import config
    
    try:
        # Get or create site
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': '127.0.0.1:8000',
                'name': 'localhost'
            }
        )
        
        # Get or create Google OAuth app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': config('GOOGLE_OAUTH2_CLIENT_ID', default=''),
                'secret': config('GOOGLE_OAUTH2_CLIENT_SECRET', default=''),
            }
        )
        
        # Add site to the app
        google_app.sites.add(site)
        
        print("✅ Google OAuth application configured")
        return True
    except Exception as e:
        print(f"❌ Error setting up Google OAuth: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Database Migration Script")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'backup':
            backup_sqlite_data()
        elif command == 'restore':
            restore_data_to_postgres()
        elif command == 'setup-oauth':
            setup_google_oauth()
        else:
            print("Usage:")
            print("  python migrate_db.py backup    # Backup SQLite data")
            print("  python migrate_db.py restore   # Restore to PostgreSQL")
            print("  python migrate_db.py setup-oauth # Setup Google OAuth")
    else:
        print("Usage:")
        print("  python migrate_db.py backup    # Backup SQLite data")
        print("  python migrate_db.py restore   # Restore to PostgreSQL")
        print("  python migrate_db.py setup-oauth # Setup Google OAuth")
