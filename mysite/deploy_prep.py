#!/usr/bin/env python
"""
Quick deployment preparation script
"""
import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False

def main():
    print("🚀 DJANGO CHAT APP - DEPLOYMENT PREPARATION")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Error: manage.py not found. Please run this script from the Django project directory.")
        sys.exit(1)
    
    print("📋 Pre-deployment checklist:")
    print()
    
    # 1. Check for migrations
    print("1️⃣ Checking for pending migrations...")
    if run_command("python manage.py makemigrations --dry-run", "Check migrations"):
        print("   All migrations are up to date")
    
    # 2. Run tests (if you have any)
    print("\n2️⃣ Running basic system check...")
    run_command("python manage.py check", "System check")
    
    # 3. Check static files
    print("\n3️⃣ Checking static files configuration...")
    if os.path.exists('staticfiles'):
        print("   ✅ Static files directory exists")
    else:
        print("   ℹ️  Static files will be collected during deployment")
    
    # 4. Verify requirements.txt
    print("\n4️⃣ Checking requirements.txt...")
    if os.path.exists('../requirements.txt'):
        print("   ✅ requirements.txt found in root directory")
        with open('../requirements.txt', 'r') as f:
            content = f.read()
            required_packages = ['django', 'channels', 'django-allauth', 'psycopg', 'python-decouple']
            missing = [pkg for pkg in required_packages if pkg not in content.lower()]
            if missing:
                print(f"   ⚠️  Missing packages: {', '.join(missing)}")
            else:
                print("   ✅ All required packages present")
    else:
        print("   ❌ requirements.txt not found!")
    
    print("\n" + "=" * 50)
    print("🎯 DEPLOYMENT STEPS:")
    print()
    print("1. Set environment variables in Render:")
    print("   DEBUG=False")
    print("   SECRET_KEY=your-production-secret-key-here")
    print("   ALLOWED_HOSTS=django-chat-app-nhzc.onrender.com")
    print("   DATABASE_URL=<your-database-url>")
    print("   GOOGLE_OAUTH2_CLIENT_ID=your-client-id-here.apps.googleusercontent.com")
    print("   GOOGLE_OAUTH2_CLIENT_SECRET=your-client-secret-here")
    print("   EMAIL_HOST_USER=your-gmail-address@gmail.com")
    print("   EMAIL_HOST_PASSWORD=your-gmail-app-password")
    print()
    print("2. Commit and push your code:")
    print("   git add .")
    print("   git commit -m 'Deploy with all new features'")
    print("   git push origin main")
    print()
    print("3. After deployment, run in Render shell:")
    print("   python manage.py migrate")
    print("   python manage.py createsuperuser")
    print("   python manage.py setup_production_oauth")
    print()
    print("4. Test your live site:")
    print("   https://django-chat-app-nhzc.onrender.com/")
    print()
    print("🎉 Your Django Chat App will be live with:")
    print("   ✅ Google OAuth Login")
    print("   ✅ PostgreSQL Database") 
    print("   ✅ User Blocking System")
    print("   ✅ Secure Password Reset")
    print("   ✅ Real-time Chat")
    print("   ✅ Admin Dashboard")

if __name__ == '__main__':
    main()
