#!/bin/bash

# Django Chat App Quick Deployment Script
# This script helps you deploy your Django chat app quickly

echo "🚀 Django Chat App Deployment Helper"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the project root directory (where manage.py is located)"
    exit 1
fi

# Function to deploy to Heroku
deploy_heroku() {
    echo "📦 Preparing Heroku deployment..."
    
    # Check if Heroku CLI is installed
    if ! command -v heroku &> /dev/null; then
        echo "❌ Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli"
        exit 1
    fi
    
    # Get app name
    read -p "Enter your Heroku app name: " app_name
    
    # Initialize git if not already done
    if [ ! -d ".git" ]; then
        echo "🔧 Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit for deployment"
    fi
    
    # Create Heroku app
    echo "🏗️ Creating Heroku app..."
    heroku create $app_name
    
    # Add addons
    echo "🔌 Adding PostgreSQL and Redis addons..."
    heroku addons:create heroku-postgresql:mini -a $app_name
    heroku addons:create heroku-redis:mini -a $app_name
    
    # Set environment variables
    echo "⚙️ Setting environment variables..."
    read -p "Enter your secret key (or press Enter for auto-generated): " secret_key
    if [ -z "$secret_key" ]; then
        secret_key=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    fi
    
    heroku config:set DEBUG=False -a $app_name
    heroku config:set SECRET_KEY="$secret_key" -a $app_name
    heroku config:set SECURE_SSL_REDIRECT=True -a $app_name
    
    # Deploy
    echo "🚀 Deploying to Heroku..."
    git push heroku main
    
    # Run migrations and setup
    echo "🔧 Running post-deployment setup..."
    heroku run python manage.py migrate -a $app_name
    heroku run python manage.py collectstatic --noinput -a $app_name
    
    echo "✅ Deployment complete!"
    echo "🌐 Your app is available at: https://$app_name.herokuapp.com"
    echo "👤 Don't forget to create a superuser: heroku run python manage.py createsuperuser -a $app_name"
}

# Function to deploy to Railway
deploy_railway() {
    echo "📦 Preparing Railway deployment..."
    
    # Check if Railway CLI is installed
    if ! command -v railway &> /dev/null; then
        echo "❌ Railway CLI not found. Installing..."
        npm install -g @railway/cli
    fi
    
    # Initialize Railway project
    echo "🔧 Initializing Railway project..."
    railway login
    railway init
    
    # Add services
    echo "🔌 Adding PostgreSQL and Redis..."
    railway add --plugin postgresql
    railway add --plugin redis
    
    # Deploy
    echo "🚀 Deploying to Railway..."
    railway up
    
    echo "✅ Deployment complete!"
    echo "🌐 Check your Railway dashboard for the app URL"
    echo "⚙️ Don't forget to set environment variables in the Railway dashboard"
}

# Function to prepare for manual deployment
prepare_manual() {
    echo "📦 Preparing files for manual deployment..."
    
    # Create production environment file
    if [ ! -f ".env" ]; then
        cp .env.example .env
        echo "📝 Created .env file from template"
        echo "⚠️ Please edit .env file with your production values"
    fi
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    
    # Collect static files
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
    
    # Run migrations
    echo "🔧 Running migrations..."
    python manage.py migrate
    
    echo "✅ Manual deployment preparation complete!"
    echo "📋 Next steps:"
    echo "   1. Edit .env file with production values"
    echo "   2. Upload files to your server"
    echo "   3. Set up web server (Nginx/Apache)"
    echo "   4. Configure database and Redis"
    echo "   5. Create superuser: python manage.py createsuperuser"
}

# Main menu
echo ""
echo "Choose deployment option:"
echo "1) Heroku (Recommended for beginners)"
echo "2) Railway (Modern alternative)"
echo "3) Prepare for manual deployment"
echo "4) Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        deploy_heroku
        ;;
    2)
        deploy_railway
        ;;
    3)
        prepare_manual
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
