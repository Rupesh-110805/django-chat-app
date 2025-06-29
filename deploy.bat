@echo off
echo 🚀 Django Chat App Deployment Helper
echo ====================================

REM Check if we're in the right directory
if not exist "mysite\manage.py" (
    echo ❌ Error: Please run this script from the project root directory
    pause
    exit /b 1
)

echo Please choose deployment type:
echo 1. Backup SQLite data
echo 2. Local PostgreSQL setup
echo 3. Render deployment
echo 4. Railway deployment  
echo 5. Heroku deployment
echo 6. Manual deployment prep
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto backup
if "%choice%"=="2" goto postgres
if "%choice%"=="3" goto render
if "%choice%"=="4" goto railway
if "%choice%"=="5" goto heroku
if "%choice%"=="6" goto manual
echo Invalid choice!
pause
exit /b 1

:backup
echo 📦 Backing up SQLite data...
python migrate_db.py backup
echo ✅ Data backup complete!
goto end

:postgres
echo 🐘 Setting up PostgreSQL...
echo.
echo Please ensure you have PostgreSQL installed and running.
echo You'll need to create a database and user manually.
echo.
echo Example commands to run in PostgreSQL:
echo   CREATE DATABASE chatapp_db;
echo   CREATE USER chatapp_user WITH PASSWORD 'your_password';
echo   GRANT ALL PRIVILEGES ON DATABASE chatapp_db TO chatapp_user;
echo.
set /p db_url="Enter your PostgreSQL DATABASE_URL: "
echo DATABASE_URL=%db_url% >> mysite\.env
echo.
echo 🔄 Running migrations...
cd mysite
python manage.py migrate
echo.
echo 🔄 Restoring data from backup...
cd ..
python migrate_db.py restore
echo.
echo 🔐 Setting up Google OAuth...
python migrate_db.py setup-oauth
echo.
echo ✅ PostgreSQL setup complete!
goto end

:render

echo.
echo Choose deployment option:
echo 1) Heroku (Recommended for beginners)
echo 2) Railway (Modern alternative)
echo 3) Prepare for manual deployment
echo 4) Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto heroku
if "%choice%"=="2" goto railway
if "%choice%"=="3" goto manual
if "%choice%"=="4" goto exit
goto invalid

:heroku
echo 📦 Preparing Heroku deployment...

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI not found. Please install it from https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

set /p app_name="Enter your Heroku app name: "

REM Initialize git if not already done
if not exist ".git" (
    echo 🔧 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit for deployment"
)

echo 🏗️ Creating Heroku app...
heroku create %app_name%

echo 🔌 Adding PostgreSQL and Redis addons...
heroku addons:create heroku-postgresql:mini -a %app_name%
heroku addons:create heroku-redis:mini -a %app_name%

echo ⚙️ Setting environment variables...
set /p secret_key="Enter your secret key (or press Enter for auto-generated): "
if "%secret_key%"=="" (
    for /f %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set secret_key=%%i
)

heroku config:set DEBUG=False -a %app_name%
heroku config:set SECRET_KEY="%secret_key%" -a %app_name%
heroku config:set SECURE_SSL_REDIRECT=True -a %app_name%

echo 🚀 Deploying to Heroku...
git push heroku main

echo 🔧 Running post-deployment setup...
heroku run python manage.py migrate -a %app_name%
heroku run python manage.py collectstatic --noinput -a %app_name%

echo ✅ Deployment complete!
echo 🌐 Your app is available at: https://%app_name%.herokuapp.com
echo 👤 Don't forget to create a superuser: heroku run python manage.py createsuperuser -a %app_name%
goto end

:railway
echo 📦 Preparing Railway deployment...

REM Check if Railway CLI is installed
railway --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Railway CLI not found. Installing...
    npm install -g @railway/cli
)

echo 🔧 Initializing Railway project...
railway login
railway init

echo 🔌 Adding PostgreSQL and Redis...
railway add --plugin postgresql
railway add --plugin redis

echo 🚀 Deploying to Railway...
railway up

echo ✅ Deployment complete!
echo 🌐 Check your Railway dashboard for the app URL
echo ⚙️ Don't forget to set environment variables in the Railway dashboard
goto end

:manual
echo 📦 Preparing files for manual deployment...

REM Create production environment file
if not exist ".env" (
    copy .env.example .env
    echo 📝 Created .env file from template
    echo ⚠️ Please edit .env file with your production values
)

echo 📥 Installing dependencies...
pip install -r requirements.txt

echo 📁 Collecting static files...
python manage.py collectstatic --noinput

echo 🔧 Running migrations...
python manage.py migrate

echo ✅ Manual deployment preparation complete!
echo 📋 Next steps:
echo    1. Edit .env file with production values
echo    2. Upload files to your server
echo    3. Set up web server (Nginx/Apache)
echo    4. Configure database and Redis
echo    5. Create superuser: python manage.py createsuperuser
goto end

:exit
echo 👋 Goodbye!
exit /b 0

:invalid
echo ❌ Invalid choice. Please run the script again.
goto end

:end
pause
