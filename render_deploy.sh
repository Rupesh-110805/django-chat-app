#!/bin/bash
# Deployment script for Render
echo "🚀 Starting deployment process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
python mysite/manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python mysite/manage.py collectstatic --noinput

# Setup Google OAuth if needed
echo "🔐 Setting up Google OAuth..."
python migrate_db.py setup-oauth

echo "✅ Deployment complete!"
