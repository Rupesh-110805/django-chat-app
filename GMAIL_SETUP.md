# Gmail SMTP Setup Guide for Django Password Reset

## 🚀 Quick Setup Steps

### 1. **Enable 2-Factor Authentication**
   - Go to: https://myaccount.google.com/security
   - Turn on "2-Step Verification" if not already enabled

### 2. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Or search "App passwords" in Google Account settings
   - Select "Mail" as the app
   - Copy the 16-character password (format: abcd efgh ijkl mnop)

### 3. **Update .env File**
   Replace these values in your `.env` file:
   ```env
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=abcdefghijklmnop  # Your 16-character app password
   DEFAULT_FROM_EMAIL=your-email@gmail.com
   ```

### 4. **Test Email Configuration**
   ```bash
   python manage.py test_email --to your-email@gmail.com
   ```

### 5. **Test Password Reset**
   ```bash
   python manage.py test_forgot_password --email test@example.com
   # Then go to: http://127.0.0.1:8000/accounts/password/reset/
   ```

## 🔧 **Alternative Email Services**

### **Gmail Business/Workspace**
```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### **Outlook/Hotmail**
```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### **Yahoo Mail**
```env
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## 🛠️ **Troubleshooting**

### **"Authentication failed" Error**
- Double-check email and app password
- Make sure 2-step verification is enabled
- Try generating a new app password

### **"Connection refused" Error**
- Check internet connection
- Try disabling firewall/antivirus temporarily
- Verify SMTP settings

### **"Less secure app access" Error**
- Don't use your regular password
- Must use App Password (16 characters)
- Regular password won't work with 2FA enabled

## 📧 **Email Templates Location**
- `templates/account/email/password_reset_key_subject.txt`
- `templates/account/email/password_reset_key_message.txt`

## 🎯 **Production Tips**
- Use environment variables for sensitive data
- Consider using SendGrid, Mailgun, or AWS SES for production
- Set up proper SPF/DKIM records for better deliverability
