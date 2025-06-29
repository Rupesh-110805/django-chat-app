# Django Chat App

A real-time chat application built with Django, Django Channels, and WebSockets. Features include public and private chat rooms, user authentication with email validation, Google OAuth integration, message reactions, and user presence tracking.

## Features

### 🔐 Authentication & Security
- **Email Validation**: Comprehensive email validation during registration
  - Format validation using Django's built-in validators
  - Domain existence verification using DNS lookup
  - Duplicate email prevention
  - Support for both `dnspython` and fallback socket validation
- **Google OAuth Integration**: Sign up and log in with Google
- **User Blocking System**: Admin can block/unblock users
- **Secure Password Requirements**: Minimum 8 characters with letters and numbers

### 💬 Chat Features
- **Public Chat Rooms**: Open to all registered users
- **Private Chat Rooms**: Invitation-only rooms with access codes
- **Real-time Messaging**: Instant message delivery using WebSockets
- **Message Reactions**: React to messages with emojis
- **User Presence**: See who's online in each room
- **Message History**: View previous messages when joining rooms

### 🎨 User Interface
- **Dark/Light Mode Support**: Responsive design with theme switching
- **Modern UI**: Clean, intuitive interface with Tailwind CSS
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## Technology Stack

- **Backend**: Django 5.1.1, Django Channels 4.0.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Real-time**: WebSockets with Redis for channel layers
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Authentication**: Django Allauth with Google OAuth2
- **Deployment**: Render, Railway (configured)

## Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd django-chat-app-main
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   
   # On Windows
   .venv\Scripts\activate
   
   # On macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration:**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Generate a new SECRET_KEY using:
   python generate_secret_key.py
   ```

5. **Database Setup:**
   ```bash
   cd mysite
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application:**
   - Main App: https://django-chat-app-nhzc.onrender.com


## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production)
DATABASE_URL=postgresql://user:password@host:port/database

# Google OAuth (optional)
GOOGLE_OAUTH_CLIENT_ID=your-google-client-id
GOOGLE_OAUTH_CLIENT_SECRET=your-google-client-secret

# Redis (for production)
REDIS_URL=redis://localhost:6379

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/` (development)
   - `https://yourdomain.com/accounts/google/login/callback/` (production)
6. Add credentials to Django admin under Social Applications

## Usage

### Creating Chat Rooms

1. **Public Rooms**: 
   - Navigate to "Create Room"
   - Enter room name
   - Select "Public" type
   - All registered users can join

2. **Private Rooms**:
   - Navigate to "Create Room"
   - Enter room name
   - Select "Private" type
   - Share the generated access code with invited users

### Email Validation Features

The app includes comprehensive email validation:

- **Format Checking**: Validates email format and structure
- **Domain Verification**: Checks if the email domain exists and can receive emails
- **Duplicate Prevention**: Ensures each email is only registered once
- **Error Messages**: Provides clear feedback for validation failures

### User Management

**For Administrators:**
- Access `/admin/` to manage users and rooms
- Block/unblock users through the admin panel
- View user activity and room statistics

## File Structure

```
django-chat-app-main/
├── mysite/                     # Main Django project
│   ├── chatapp/               # Chat application
│   │   ├── models.py          # Database models
│   │   ├── views.py           # View functions
│   │   ├── forms.py           # Form definitions with email validation
│   │   ├── consumers.py       # WebSocket consumers
│   │   ├── routing.py         # WebSocket routing
│   │   ├── urls.py            # URL patterns
│   │   ├── admin.py           # Admin configuration
│   │   └── templates/         # HTML templates
│   ├── mysite/                # Project settings
│   │   ├── settings.py        # Django settings
│   │   ├── urls.py            # Main URL configuration
│   │   ├── asgi.py            # ASGI configuration
│   │   └── wsgi.py            # WSGI configuration
│   └── manage.py              # Django management script
├── requirements.txt           # Python dependencies
├── runtime.txt               # Python version for deployment
├── Procfile                  # Process file for deployment
├── render.yaml               # Render deployment configuration
├── railway.json              # Railway deployment configuration
└── README.md                 # This file
```

## API Endpoints

### Authentication
- `GET/POST /rooms/register/` - User registration with email validation
- `GET/POST /rooms/login/` - User login
- `GET /rooms/logout/` - User logout

### Chat Rooms
- `GET /rooms/` - List public rooms
- `GET /rooms/create-room/` - Create new room
- `GET /rooms/private-rooms/` - List private rooms
- `GET /rooms/<slug>/` - Join specific room
- `POST /rooms/<slug>/send/` - Send message (AJAX)

### WebSocket Endpoints
- `ws://localhost:8000/ws/chat/<room_slug>/` - Real-time chat connection

## Deployment

### Render Deployment

1. **Prepare for Deployment:**
   ```bash
   # Ensure all dependencies are in requirements.txt
   pip freeze > requirements.txt
   ```

2. **Deploy to Render:**
   - Connect your GitHub repository to Render
   - Configure environment variables
   - Deploy using the provided `render.yaml` configuration

3. **Post-Deployment:**
   - Run migrations via Render dashboard
   - Create superuser account
   - Configure Google OAuth with production URLs

### Railway Deployment

1. **Deploy to Railway:**
   - Use the provided `railway.json` configuration
   - Set environment variables in Railway dashboard
   - Deploy from GitHub repository

## Development

### Running Tests

```bash
cd mysite
python manage.py test chatapp
```

### Making Changes

1. **Database Changes:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files:**
   ```bash
   python manage.py collectstatic
   ```

3. **Creating Admin User:**
   ```bash
   python manage.py createsuperuser
   ```

## Troubleshooting

### Common Issues

1. **Email Validation Not Working:**
   - Ensure `dnspython` is installed: `pip install dnspython`
   - Check DNS settings if domain validation fails
   - Verify email format meets requirements

2. **WebSocket Connection Failed:**
   - Ensure Redis is running (production)
   - Check ASGI configuration
   - Verify channel layer settings

3. **Google OAuth Issues:**
   - Verify OAuth credentials in admin panel
   - Check authorized redirect URIs
   - Ensure Google+ API is enabled

4. **Database Issues:**
   - Run migrations: `python manage.py migrate`
   - Check database connection settings
   - Verify environment variables

### Debug Mode

Enable debug mode for development:
```env
DEBUG=True
```

**⚠️ Never enable DEBUG in production!**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review Django and Django Channels documentation

## Acknowledgments

- Django and Django Channels communities
- Tailwind CSS for styling
- Google OAuth for authentication
- Redis for WebSocket scaling
- dnspython for email domain validation

---

**Happy Chatting! 🎉**
