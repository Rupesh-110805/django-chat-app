#!/bin/bash
# Simple startup script for Render deployment with debugging

set -e  # Exit on any error

echo "=== Starting Django Chat App Deployment ==="

# Ensure packages are installed (fallback)
echo "0. Ensuring packages are installed..."
pip install -r requirements.txt || echo "⚠️ Package installation failed or already done"

# Set Django settings module
export DJANGO_SETTINGS_MODULE=mysite.settings

# Navigate to Django project directory
cd mysite

echo "1. Running database migrations..."
python manage.py migrate --noinput

echo "2. Collecting static files..."
python manage.py collectstatic --noinput

echo "3. Creating superuser if none exists..."
python manage.py create_superuser_if_none || echo "⚠️ Superuser creation failed, but continuing..."

echo "4. Checking if superuser exists and creating backup..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os

# Check existing superusers
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print('=== Existing Superusers ===')
    for su in superusers:
        print(f'✅ Superuser found: {su.username} ({su.email})')
else:
    print('❌ No superuser found!')

# Always create a backup superuser with different name
backup_username = 'chatadmin'
backup_email = 'chatadmin@app.com'
backup_password = 'ChatApp2025!'

# Check if backup superuser already exists
if not User.objects.filter(username=backup_username).exists():
    try:
        backup_user = User.objects.create_superuser(
            username=backup_username,
            email=backup_email,
            password=backup_password
        )
        print(f'✅ Backup superuser created: {backup_username}')
        print(f'   Email: {backup_email}')
        print(f'   Password: {backup_password}')
    except Exception as e:
        print(f'❌ Backup superuser creation failed: {e}')
else:
    print(f'✅ Backup superuser {backup_username} already exists')

# Also try to create the main superuser from environment variables
main_username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
main_email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@chatapp.com')
main_password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123!')

if not User.objects.filter(username=main_username).exists():
    try:
        main_user = User.objects.create_superuser(
            username=main_username,
            email=main_email,
            password=main_password
        )
        print(f'✅ Main superuser created: {main_username}')
        print(f'   Email: {main_email}')
        print(f'   Password: {main_password}')
    except Exception as e:
        print(f'❌ Main superuser creation failed: {e}')
else:
    print(f'✅ Main superuser {main_username} already exists')

print('=== Final Superuser Summary ===')
all_superusers = User.objects.filter(is_superuser=True)
for su in all_superusers:
    print(f'Username: {su.username}, Email: {su.email}')
"

echo "5. Starting server..."
exec daphne -b 0.0.0.0 -p $PORT mysite.asgi:application