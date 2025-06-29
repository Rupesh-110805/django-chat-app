# 🚀 Google OAuth2 Production Deployment Guide

## 📍 **Your Deployed Site:** https://django-chat-app-nhzc.onrender.com

---

## 1️⃣ **Google Cloud Console Configuration**

### **Step 1: Access Google Cloud Console**
1. Go to: https://console.cloud.google.com/
2. Select your project (the one with your current OAuth credentials)
3. Navigate to: **APIs & Services** → **Credentials**

### **Step 2: Update OAuth 2.0 Client ID**
1. Click on your existing OAuth 2.0 Client ID
2. Update the following fields:

#### **Authorized JavaScript origins:**
```
http://localhost:8000
http://127.0.0.1:8000
https://django-chat-app-nhzc.onrender.com
```

#### **Authorized redirect URIs:**
```
http://localhost:8000/accounts/google/login/callback/
http://127.0.0.1:8000/accounts/google/login/callback/
https://django-chat-app-nhzc.onrender.com/accounts/google/login/callback/
```

3. Click **SAVE**

---

## 2️⃣ **Render.com Environment Variables**

### **Step 1: Access Render Dashboard**
1. Go to: https://dashboard.render.com/
2. Select your `django-chat-app-nhzc` service

### **Step 2: Update Environment Variables**
Go to **Environment** tab and add/update these variables:

```bash
# Google OAuth2 Configuration
GOOGLE_OAUTH2_CLIENT_ID=928381654908-n6p7upjh9lslsm1ef0ai5rmgs2qp0kq7.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=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

# Django Settings
DEBUG=False
SECRET_KEY=your-production-secret-key-here
ALLOWED_HOSTS=django-chat-app-nhzc.onrender.com,localhost,127.0.0.1

# Database Configuration (if using PostgreSQL)
DATABASE_URL=your-database-url-here

# Email Configuration for Production
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=rupeshnidadavolu110805@gmail.com
EMAIL_HOST_PASSWORD=pnep qqte irjf vtvb
DEFAULT_FROM_EMAIL=rupeshnidadavolu110805@gmail.com
```

---

## 3️⃣ **Django Site Configuration**

### **Update Django Sites Framework**
Your production app needs to know its domain. Run this in your Django admin or shell:

```python
# In Django shell or admin
from django.contrib.sites.models import Site

# Update the default site
site = Site.objects.get(id=1)
site.domain = 'django-chat-app-nhzc.onrender.com'
site.name = 'Django Chat App'
site.save()
```

---

## 4️⃣ **Social Application Configuration**

### **Add Google Provider in Django Admin**
1. Go to: https://django-chat-app-nhzc.onrender.com/admin/
2. Navigate to: **Social Applications** under **SOCIAL ACCOUNTS**
3. Add a new Social Application:
   - **Provider:** Google
   - **Name:** Google OAuth
   - **Client ID:** `928381654908-n6p7upjh9lslsm1ef0ai5rmgs2qp0kq7.apps.googleusercontent.com`
   - **Secret key:** `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`
   - **Sites:** Select your site (django-chat-app-nhzc.onrender.com)
4. Save

---

## 5️⃣ **Testing Google OAuth**

### **Test URLs:**
- **Login Page:** https://django-chat-app-nhzc.onrender.com/accounts/login/
- **Google Login:** Should show "Sign in with Google" button
- **Redirect After Login:** https://django-chat-app-nhzc.onrender.com/rooms/

### **Test Process:**
1. Visit your login page
2. Click "Sign in with Google"
3. Authorize the app
4. Should redirect back to your chat app

---

## 6️⃣ **Common Issues & Solutions**

### **Issue 1: "redirect_uri_mismatch"**
- **Cause:** Google redirect URI doesn't match
- **Solution:** Ensure exact match in Google Console:
  ```
  https://django-chat-app-nhzc.onrender.com/accounts/google/login/callback/
  ```

### **Issue 2: "invalid_client"**
- **Cause:** Client ID/Secret mismatch
- **Solution:** Double-check environment variables match Google Console

### **Issue 3: "Site matching query does not exist"**
- **Cause:** Django Sites not configured
- **Solution:** Update Site domain in Django admin

### **Issue 4: "Social application not found"**
- **Cause:** Google provider not added in Django admin
- **Solution:** Add Social Application as described in Step 4

---

## 7️⃣ **Security Considerations**

### **Production Settings:**
- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY`
- ✅ HTTPS enforced
- ✅ Secure cookies enabled

### **Environment Variables:**
- ✅ Never commit sensitive data to Git
- ✅ Use Render's environment variables
- ✅ Separate dev/prod configurations

---

## 8️⃣ **Deployment Checklist**

- [ ] Google Console: JavaScript origins updated
- [ ] Google Console: Redirect URIs updated  
- [ ] Render: Environment variables set
- [ ] Django Admin: Social Application created
- [ ] Django Admin: Site domain updated
- [ ] Test: Google login works
- [ ] Test: Redirect works correctly
- [ ] Test: User creation works
- [ ] Test: Blocked user prevention works

---

## 🆘 **Need Help?**

If you encounter issues:

1. **Check Render Logs:**
   ```bash
   # In Render dashboard, go to Logs tab
   ```

2. **Debug Django:**
   - Temporarily set `DEBUG=True` to see detailed errors
   - Check Django admin logs

3. **Test Locally First:**
   - Ensure everything works on localhost
   - Then deploy to production

---

## ✅ **Final Verification**

Your Google OAuth should now work on both:
- **Development:** http://localhost:8000
- **Production:** https://django-chat-app-nhzc.onrender.com

The same Google OAuth app will handle both domains! 🎉
