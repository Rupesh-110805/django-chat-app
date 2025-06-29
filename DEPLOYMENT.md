# Django Chat App Deployment Guide

## Prerequisites
- Python 3.11+
- Git
- A hosting platform account (Railway, Render, Fly.io, etc.)

**Note**: Heroku discontinued their free tier in November 2022. We recommend Railway as the best alternative.

## 1. Railway Deployment (Recommended - Free $5/month credit)

### Step 1: Install Heroku CLI
1. Download and install Heroku CLI from https://devcenter.heroku.com/articles/heroku-cli
2. Login to Heroku: `heroku login`

### Step 2: Prepare your app
```bash
# Navigate to your project directory
cd c:\Users\rupes\Project\djangochat

# Create a virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Copy environment variables template
copy .env.example .env
# Edit .env with your production values
```

### Step 3: Deploy to Heroku
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-chat-app-name

# Add Heroku Postgres addon
heroku addons:create heroku-postgresql:mini

# Add Heroku Redis addon
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-super-secret-key-here
heroku config:set SECURE_SSL_REDIRECT=True

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Collect static files
heroku run python manage.py collectstatic --noinput
```

Your app will be available at: https://your-chat-app-name.herokuapp.com

## 2. Railway Deployment (Modern alternative)

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
railway login
```

### Step 2: Deploy
```bash
cd c:\Users\rupes\Project\djangochat
railway init
railway up

# Add PostgreSQL database
railway add --plugin postgresql

# Add Redis
railway add --plugin redis

# Set environment variables in Railway dashboard
# Go to https://railway.app/dashboard
# Add: DEBUG=False, SECRET_KEY=your-key, etc.
```

## 3. DigitalOcean App Platform

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Push your code:
```bash
git remote add origin https://github.com/yourusername/django-chat.git
git push -u origin main
```

### Step 2: Deploy on DigitalOcean
1. Go to https://cloud.digitalocean.com/apps
2. Click "Create App"
3. Connect your GitHub repository
4. Configure your app:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `daphne mysite.asgi:application --port $PORT --bind 0.0.0.0`
5. Add PostgreSQL and Redis databases
6. Set environment variables
7. Deploy

## 4. VPS Deployment (Advanced)

### Step 1: Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python, PostgreSQL, Redis, Nginx
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib redis-server nginx

# Create project directory
sudo mkdir -p /var/www/django-chat
sudo chown $USER:$USER /var/www/django-chat
```

### Step 2: Application Setup
```bash
cd /var/www/django-chat
git clone https://github.com/yourusername/django-chat.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with production values
```

### Step 3: Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE djangochat;
CREATE USER djangochat_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE djangochat TO djangochat_user;
\q

# Update DATABASE_URL in .env
DATABASE_URL=postgres://djangochat_user:your_password@localhost:5432/djangochat
```

### Step 4: Configure Services
Create systemd service files:

```bash
# Create Daphne service
sudo nano /etc/systemd/system/django-chat.service
```

Add this content:
```ini
[Unit]
Description=Django Chat Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/django-chat/mysite
Environment=PATH=/var/www/django-chat/venv/bin
ExecStart=/var/www/django-chat/venv/bin/daphne -b 0.0.0.0 -p 8000 mysite.asgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

### Step 5: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/django-chat
```

Add this content:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/django-chat/mysite/staticfiles/;
    }

    location /media/ {
        alias /var/www/django-chat/mysite/media/;
    }
}
```

### Step 6: Start Services
```bash
# Enable and start services
sudo systemctl enable django-chat
sudo systemctl start django-chat

# Enable nginx site
sudo ln -s /etc/nginx/sites-available/django-chat /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Run Django commands
cd /var/www/django-chat/mysite
source ../venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## Environment Variables

Create a `.env` file with these variables:

```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://username:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
SECURE_SSL_REDIRECT=True
```

## Post-Deployment Checklist

1. ✅ Database migrations applied
2. ✅ Static files collected
3. ✅ Superuser created
4. ✅ Environment variables set
5. ✅ SSL certificate configured
6. ✅ Domain name pointed to server
7. ✅ Backup strategy implemented
8. ✅ Monitoring set up

## Troubleshooting

### Common Issues:

1. **Static files not loading**
   - Run `python manage.py collectstatic`
   - Check STATIC_ROOT and STATIC_URL settings

2. **Database connection errors**
   - Verify DATABASE_URL format
   - Check database credentials

3. **WebSocket connection issues**
   - Ensure Redis is running
   - Check CHANNEL_LAYERS configuration

4. **Media files not uploading**
   - Check MEDIA_ROOT permissions
   - Verify file upload limits

### Logs:
- Heroku: `heroku logs --tail`
- Railway: Check Railway dashboard
- VPS: `sudo journalctl -u django-chat -f`

## Maintenance

### Regular Tasks:
- Monitor application performance
- Update dependencies regularly
- Backup database
- Monitor disk space (for media files)
- Review security logs

### Updates:
```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart application
# Heroku: automatic
# Railway: automatic
# VPS: sudo systemctl restart django-chat
```
