# Email Configuration Guide

## Password Reset System Setup

The password reset system is now implemented and ready to use. Here's how it works:

### 🔧 **Development Setup (Current)**
- Uses `console.EmailBackend` - emails appear in terminal
- No external email service needed
- Good for testing password reset flow

### 🚀 **Production Setup**

#### Option 1: Gmail SMTP (Recommended)
1. Create a Gmail account or use existing one
2. Enable 2-factor authentication
3. Generate an App Password:
   - Go to Google Account settings
   - Security → 2-Step Verification
   - App passwords → Generate password for "Mail"
4. Update `.env` file:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### Option 2: Other Email Services
- **SendGrid**: Professional email service
- **Mailgun**: Developer-friendly email API
- **Amazon SES**: AWS Simple Email Service

### 🧪 **Testing Email**
```bash
# Test email configuration
python manage.py test_email --to your-email@example.com

# Test password reset flow
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.create_user('testuser', 'test@example.com', 'password123')
>>> # Then visit /accounts/password/reset/ in browser
```

### 📧 **How It Works**
1. User clicks "Forgot Password" on login page
2. User enters email address
3. System sends password reset email
4. User clicks link in email
5. User enters new password
6. Password is updated, user can login

### 🔗 **Available URLs**
- `/accounts/password/reset/` - Request password reset
- `/accounts/password/reset/done/` - Confirmation page
- `/accounts/password/reset/key/...` - Reset password form
- `/accounts/password/reset/key/done/` - Success page

### 🎨 **Templates Created**
- `account/password_reset.html` - Reset request form
- `account/password_reset_done.html` - Email sent confirmation
- `account/password_reset_from_key.html` - New password form
- `account/password_reset_from_key_done.html` - Success page
- `account/email/password_reset_key_*.txt` - Email templates

### 🔐 **Security Features**
- Reset links expire after 24 hours
- One-time use tokens
- Email verification required
- Secure password validation

### 🐛 **Troubleshooting**
- Check email settings in `.env`
- Verify SMTP credentials
- Check spam folder for reset emails
- Use console backend for development testing
