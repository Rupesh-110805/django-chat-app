# Google OAuth2 Setup Instructions

## Setting up Google OAuth2 for your Django Chat App

### 1. Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

### 2. Create a New Project (or use existing)
- Click on the project dropdown at the top
- Click "New Project"
- Give it a name like "Django Chat App"
- Click "Create"

### 3. Enable Google+ API
- In the left sidebar, go to "APIs & Services" > "Library"
- Search for "Google+ API" or "Google Identity"
- Click on it and press "Enable"

### 4. Configure OAuth Consent Screen
- Go to "APIs & Services" > "OAuth consent screen"
- Choose "External" (unless you have a Google Workspace)
- Fill in the required fields:
  - App name: "Django Chat App"
  - User support email: your email
  - Developer contact email: your email
- Add scopes (if asked):
  - ../auth/userinfo.email
  - ../auth/userinfo.profile
- Add test users: your email address

### 5. Create OAuth2 Credentials
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth 2.0 Client IDs"
- Choose "Web application"
- Give it a name: "Django Chat App Client"
- Add Authorized redirect URIs:
  - http://127.0.0.1:8000/accounts/google/login/callback/
  - http://localhost:8000/accounts/google/login/callback/
  - (Add your production domain when deploying)

### 6. Copy Credentials
- After creating, you'll see your Client ID and Client Secret
- Copy these values

### 7. Update Your Django Settings
- Open the `.env` file in your Django project
- Replace the placeholder values:
  ```
  GOOGLE_OAUTH2_CLIENT_ID=your_actual_client_id_here
  GOOGLE_OAUTH2_CLIENT_SECRET=your_actual_client_secret_here
  ```

### 8. Add Social Application in Django Admin
- Start your Django server: `python manage.py runserver`
- Go to: http://127.0.0.1:8000/admin/
- Create a superuser if you haven't: `python manage.py createsuperuser`
- Login to admin
- Go to "Social Applications" > "Add"
- Fill in:
  - Provider: Google
  - Name: Google
  - Client id: (paste your Client ID)
  - Secret key: (paste your Client Secret)
  - Sites: Choose your site (Default: example.com)

### 9. Test the Integration
- Go to: http://127.0.0.1:8000/rooms/login/
- Click "Continue with Google"
- You should be redirected to Google's OAuth flow

### 10. For Production Deployment
- Add your production domain to Google OAuth2 settings
- Update redirect URIs to include your production URLs
- Make sure to use HTTPS in production

## Troubleshooting

### Common Issues:
1. **redirect_uri_mismatch**: Make sure your redirect URI in Google Console exactly matches what Django is sending
2. **invalid_client**: Check that your Client ID and Secret are correct
3. **access_denied**: Make sure you've added yourself as a test user in the OAuth consent screen

### Debug Tips:
- Check Django logs for detailed error messages
- Verify your Google Cloud Console settings
- Make sure the Google+ API is enabled
- Ensure your OAuth consent screen is properly configured

## Security Notes
- Never commit your `.env` file to version control
- Use environment variables for production
- Regularly rotate your OAuth credentials
- Use HTTPS in production
